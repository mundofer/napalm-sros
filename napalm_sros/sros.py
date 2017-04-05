# Copyright 2017 Fernando Garcia. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

"""
Napalm driver for SRos.

Read https://napalm.readthedocs.io for more information.
"""

from napalm_base.base import NetworkDriver
from netmiko import ConnectHandler
from ncclient import manager, NCClientError
import xml.etree.ElementTree as ETree
from StringIO import StringIO
from napalm_base.exceptions import (
    ConnectionException,
    SessionLockedException,
    MergeConfigException,
    ReplaceConfigException,
    CommandErrorException,
    )
import textfsm

#from lxml import etree as ETree
ns = {'sros_ns':'urn:alcatel-lucent.com:sros:ns:yang:cli-content-layer-r13'}

class SRosDriver(NetworkDriver):
    """Napalm driver for SRos."""

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        """Constructor."""
        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout
        self.mgr = None
        self.ssh = None

        if optional_args is None:
            optional_args = {}

    def _getResponse(self,parsed):
        for i in parsed.iter():
            subs = i.tag.split('}')
            if subs[1] == 'response':
                return i.text
        return ''


    def _getInfo(self,info,):
        tree = ETree.Element("oper-data-format-cli-block")
        command = ETree.SubElement(tree,"cli-show")
        command.text=info
        response = self.mgr.get(filter=('subtree',ETree.tostring(tree)))
        parsed = ETree.fromstringlist(response._raw)
        elements = self._getResponse(parsed)
        #elements = response.find("{urn:alcatel-lucent.com:sros:ns:yang:cli-content-layer-r13}response")
        return elements

    def _getModel(self):
        model = ''
        hostname = ''
        serial = ''
        text = self._getInfo("chassis detail")
        lines = text.splitlines()
        for line in lines:
            line.strip()
            fields = line.split(':')
            if fields[0].find("Type") != -1:
                model = fields[1]
            elif fields[0].find("Name") != -1:
                hostname = fields[1]
            elif fields[0].find("Serial number") != -1:
                serial = fields[1]
        return model,hostname,serial

    def _getVersion(self):
        text = self._getInfo("version")
        lines = text.splitlines()
        for line in lines:
            line.strip()
            fields = line.split(' ')
            for field in fields:
                if field.find("TiMOS") != -1:
                    return field
        return ''

    def _getUptime(self):
        text = self._getInfo("uptime")
        fields = text.partition(':')
        return fields[2].strip()

    def _parse(self,text):
        it = ETree.iterparse(StringIO(text))
        for _, el in it:
            if '}' in el.tag:
                el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
            for at in el.attrib.keys(): # strip namespaces of attributes too
                if '}' in at:
                    newat = at.split('}', 1)[1]
                    el.attrib[newat] = el.attrib[at]
                    del el.attrib[at]
        root = it.root
        return root
        #parsed = ETree.fromstringlist(response._raw)

    def _extract_child(self,element,indent,config,level=None,parser=None):
        # if not level, not level requested or leaf none. Append info
        if not level:
            if parser:
                return parser(element)
            else:
                config = config +indent + element.tag
                for attrib in element.attrib.values():
                    config = config  + " "+ attrib
                    config = config + "\n"
        for child in element._children:
            if not level:
                # not level requested of leaf node of request
                config = self._extract_child(child,indent+'  ',config)
            else:
                # recurse only if we're in the requested level tree.
                if child.tag == level[0]:
                    config = self._extract_child(child,indent+'  ',config,level[1:],parser)
        return config

    def _parse_user(self,element):
        the_user = {}
        for children in element._children:
            if children.tag == 'user-name':
                name = children.text
            elif children.tag == 'password':
                the_user['password'] = children.text
            elif children.tag == 'access':
                the_user['level'] = children.text
            the_user['sshkeys'] = []
        return (name, the_user)

    def _extract_config(self,tree):
        config = self._extract_child(tree,'','')
        return config
    """
            for element in tree.iter():
                command = element.tag.split('}')[1]
                config = config +command + " " + element.text+"\n"
            return config
    """

    def _extract_users(self,tree):
        users = self._extract_child(tree,'','',level=["data","configure","system","security","user"],parser=self._parse_user)
        return users

    def open(self):
        """Implementation of NAPALM method open."""
        nokia_sr = {
            'device_type': 'alcatel_sros',
            'ip': self.hostname,
            'username': self.username,
            'password': self.password,
            'port': 22,
            'secret':'',
            'verbose':False,
            'global_delay_factor':10
        }
        self.ssh = ConnectHandler(**nokia_sr)

        try:
            self.mgr = manager.connect_ssh(host=self.hostname,port=830,username=self.username,password=self.password,device_params={'name':'alu'})
        except self.mgr.transport.TransportError as ce:
            raise ConnectionException(ce.message)

    def close(self):
        """Implementation of NAPALM method close."""
        self.ssh.disconnect()
        #self.ssh = None
        self.mgr.close_session()
        #self.mgr = None

    def _lock(self):
        """Lock the config DB."""
        pass

    def _unlock(self):
        """Unlock the config DB."""
        pass

    def is_alive(self):
        # evaluate the state of the underlying SSH connection
        # and also the NETCONF status from PyEZ
        return self.mgr.connected

    def cli(self, commands):

        """
        Will execute a list of commands and return the output in a dictionary format.
        """
        cli_output = {}

        for command in commands:
            cli_output[command] = self.ssh.send_command(command)
        return cli_output

    def get_ports(self):
        # Get list of physical ports
        cliResult = self._getInfo("port detail")
        tpl_file = open("./port.tpl")
        re_table = textfsm.TextFSM(tpl_file)
        dictionary = {}
        results_port = re_table.ParseText(cliResult)
        # now we add the physical ports
        for entry_port in results_port:
            dic_entry = {}
            dic_entry['name'] = entry_port[1]
            dic_entry['is_up'] = entry_port[7]
            dic_entry['is_enabled'] = entry_port[5]
            dic_entry['description'] = entry_port[0]
            dic_entry['last_flapped'] = entry_port[15]
            dic_entry['speed'] = entry_port[2]
            dic_entry['mac_address'] = entry_port[67]
            dictionary[dic_entry['name']] = dic_entry
        return dictionary

    def get_interfaces(self):
        # Get list of logical interfaces
        cliResult = self._getInfo("router interface")
        tpl_file = open("./interface.tpl")
        re_table = textfsm.TextFSM(tpl_file)
        results_if = re_table.ParseText(cliResult)
        cliResult = self._getInfo("port detail")
        tpl_file = open("./port.tpl")
        re_table = textfsm.TextFSM(tpl_file)
        dictionary = {}
        results_port = re_table.ParseText(cliResult)
        # adding elements that have logical interfaces
        for entry_if in results_if:
            dic_entry = {}
            dic_entry['name'] = entry_if[0]
            dic_entry['port'] = entry_if[3]
            for entry_port in results_port:
                if entry_port[1] == entry_if[3]:
                    dic_entry['is_up'] = entry_port[7]
                    dic_entry['is_enabled'] = entry_port[5]
                    dic_entry['description'] = entry_port[0]
                    dic_entry['last_flapped'] = entry_port[15]
                    dic_entry['speed'] = entry_port[2]
                    dic_entry['mac_address'] = entry_port[67]
                    break
            dictionary[dic_entry['name']] = dic_entry

        return dictionary

    def get_interfaces_ip(self):

        """
        Returns all configured IP addresses on all interfaces as a dictionary of dictionaries.
        Keys of the main dictionary represent the name of the interface.
        Values of the main dictionary represent are dictionaries that may consist of two keys
        'ipv4' and 'ipv6' (one, both or none) which are themselvs dictionaries witht the IP
        addresses as keys.
        Each IP Address dictionary has the following keys:
            * prefix_length (int)

        Example::

            {
                u'FastEthernet8': {
                    u'ipv4': {
                        u'10.66.43.169': {
                            'prefix_length': 22
                        }
                    }
                },
                u'Loopback555': {
                    u'ipv4': {
                        u'192.168.1.1': {
                            'prefix_length': 24
                        }
                    },
                    u'ipv6': {
                        u'1::1': {
                            'prefix_length': 64
                        },
                        u'2001:DB8:1::1': {
                            'prefix_length': 64
                        },
                        u'2::': {
                            'prefix_length': 64
                        },
                        u'FE80::3': {
                            'prefix_length': u'N/A'
                        }
                    }
                },
                u'Tunnel0': {
                    u'ipv4': {
                        u'10.63.100.9': {
                            'prefix_length': 24
                        }
                    }
                }
            }
        """
        # Get list of logical interfaces
        cliResult = self._getInfo("router interface")
        tpl_file = open("./interface.tpl")
        re_table = textfsm.TextFSM(tpl_file)
        results_if = re_table.ParseText(cliResult)
        dictionary = {}
        # adding elements that have logical interfaces
        for entry_if in results_if:
            dic_entry = {}
            dic_ipv6 = {}
            dic_ipv4 = {}
            if entry_if[1]:
                dic_prefix = {}
                dic_prefix['prefix_length'] = entry_if[2]
                dic_ipv4[entry_if[1]] = dic_prefix
                dic_entry['ipv4'] = dic_ipv4
            if len(entry_if[3]):
                for prefix,size in zip(entry_if[3],entry_if[4]):
                    dic_prefix = {}
                    dic_prefix['prefix_length'] = size
                    dic_ipv6[prefix] = dic_prefix
                dic_entry['ipv6'] = dic_ipv6

            dictionary[entry_if[0]] = dic_entry
        return dictionary

    def _load_candidate(self, filename, config, overwrite):
        pass

    def load_replace_candidate(self, filename=None, config=None):
        """Open the candidate config and merge."""
        pass

    def load_merge_candidate(self, filename=None, config=None):
        """Open the candidate config and replace."""
        pass

    def compare_config(self):
        """Compare candidate config with running."""
        pass

    def commit_config(self):
        """Commit configuration."""
        pass

    def discard_config(self):
        """Discard changes (rollback 0)."""
        pass

    def rollback(self):
        """Rollback to previous commit."""
        pass

    def get_facts(self):
        """Return facts of the device.
        Returns a dictionary containing the following information:
         * uptime - Uptime of the device in seconds.
         * vendor - Manufacturer of the device.
         * model - Device model.
         * hostname - Hostname of the device
         * fqdn - Fqdn of the device
         * os_version - String with the OS version running on the device.
         * serial_number - Serial number of the device
         * interface_list - List of the interfaces of the device
        """
        model, hostname, serial = self._getModel()
        version = self._getVersion()
        uptime = self._getUptime()
        interfaces = self.get_interfaces()
        interface_list = interfaces.keys()
        return {
            'uptime': uptime,
            'vendor': 'Nokia',
            'model': model,
            'hostname': hostname,
            'fqdn': '',
            'os_version': version,
            'serial_number': serial,
            'interface_list': interface_list
        }

    def get_config(self, retrieve='all'):
        """
        Return the configuration of a device.

        Args:
            retrieve(string): Which configuration type you want to populate, default is all of them.
                The rest will be set to "".

        Returns:
          The object returned is a dictionary with the following keys:
            - running(string) - Representation of the native running configuration
            - candidate(string) - Representation of the native candidate configuration. If the
              device doesnt differentiate between running and startup configuration this will an
              empty string
            - startup(string) - Representation of the native startup configuration. If the
              device doesnt differentiate between running and startup configuration this will an
              empty string
        """

        configs = {}
        # The saved config file is indicated in the bof
        bof_values = self._getInfo('bof')
        tpl_file = open("./bof.tpl")
        re_table = textfsm.TextFSM(tpl_file)
        results_bof = re_table.ParseText(bof_values)[0]
        command = "file type " + results_bof[1]
        #command = "admin display-config"
        readed_saved = self.ssh.send_command(command)
        #readed_saved = ''
        #start = readed_saved.find('configure') + 10
        #end = readed_saved.find('# Finished')
        #configs['startup'] = readed_saved[start:end]
        configs['startup'] = readed_saved
        # Gettig running config
        command = "admin display-config"
        readed_run = self.ssh.send_command(command)
        configs['running'] = readed_run
        configs['candidate'] = ''
        return configs

    def ping(self, destination, source=None, ttl=None, timeout=None,
             size=None, count=None):
        """
        Executes ping on the device and returns a dictionary with the result

        :param destination: Host or IP Address of the destination
        :param source (optional): Source address of echo request
        :param ttl (optional): Maximum number of hops
        :param timeout (optional): Maximum seconds to wait after sending final packet
        :param size (optional): Size of request (bytes)
        :param count (optional): Number of ping request to send

        Output dictionary has one of following keys:

            * success
            * error

        In case of success, inner dictionary will have the followin keys:

            * probes_sent (int)
            * packet_loss (int)
            * rtt_min (float)
            * rtt_max (float)
            * rtt_avg (float)
            * rtt_stddev (float)
            * results (list)

        'results' is a list of dictionaries with the following keys:

            * ip_address (str)
            * rtt (float)

        Example::

            {
                'success': {
                    'probes_sent': 5,
                    'packet_loss': 0,
                    'rtt_min': 72.158,
                    'rtt_max': 72.433,
                    'rtt_avg': 72.268,
                    'rtt_stddev': 0.094,
                    'results': [
                        {
                            'ip_address': u'1.1.1.1',
                            'rtt': 72.248
                        },
                        {
                            'ip_address': '2.2.2.2',
                            'rtt': 72.299
                        }
                    ]
                }
            }

            OR

            {
                'error': 'unknown host 8.8.8.8.8'
            }

        """
        command = "ping " + destination
        if source:
            command = command + " source " + source
        if ttl:
            command = command + " ttl " + ttl
        if timeout:
            command = command + " timeout " + timeout
        if size:
            command = command + " size " + size
        if count:
            command = command + " count " + count
        readed = self.ssh.send_command(command)
        lines = readed.splitlines()
        # if first line start with PING, is a success
        ping_dict = {}
        if 'PING' == lines[1][:4]:
            ping_dict['success'] = {
                                'probes_sent': 0,
                                'packet_loss': 0,
                                'rtt_min': 0.0,
                                'rtt_max': 0.0,
                                'rtt_avg': 0.0,
                                'rtt_stddev': 0.0,
                                'results': []
            }
            tpl_file = open("./ping.tpl")
            re_table = textfsm.TextFSM(tpl_file)
            results = re_table.ParseText(readed)[0]
            ping_dict['success']['probes_sent'] = int(results[0])
            ping_dict['success']['packet_loss'] = int(results[0]) - int(results[1])
            ping_dict['success']['rtt_min'] = float(results[2])
            ping_dict['success']['rtt_max'] = float(results[3])
            ping_dict['success']['rtt_avg'] = float(results[4])
            ping_dict['success']['rtt_stddev'] = float(results[5])
            for ip,rtt in zip(results[6],results[7]):
                ping_dict['success']['results'].append({'ip_address':ip,'rtt':rtt})
        # if any line starts with 'Error'. Return error
        elif 'Error' == lines[1][:5]:
                ping_dict['error'] = lines[1][7:]
        elif 'MINOR' == lines[1][:5]:
                ping_dict['error'] = lines[1][7:]
        return ping_dict

    def traceroute(self,
                   destination,
                   source=None,
                   ttl=None,
                   timeout=None):
        """
        Executes traceroute on the device and returns a dictionary with the result.

        :param destination: Host or IP Address of the destination
        :param source (optional): Use a specific IP Address to execute the traceroute
        :param ttl (optional): Maimum number of hops
        :param timeout (optional): Number of seconds to wait for response

        Output dictionary has one of the following keys:

            * success
            * error

        In case of success, the keys of the dictionary represent the hop ID, while values are
        dictionaries containing the probes results:
            * rtt (float)
            * ip_address (str)
            * host_name (str)

        Example::

            {
                'success': {
                    1: {
                        'probes': {
                            1: {
                                'rtt': 1.123,
                                'ip_address': u'206.223.116.21',
                                'host_name': u'eqixsj-google-gige.google.com'
                            },
                            2: {
                                'rtt': 1.9100000000000001,
                                'ip_address': u'206.223.116.21',
                                'host_name': u'eqixsj-google-gige.google.com'
                            },
                            3: {
                                'rtt': 3.347,
                                'ip_address': u'198.32.176.31',
                                'host_name': u'core2-1-1-0.pao.net.google.com'}
                            }
                        },
                        2: {
                            'probes': {
                                1: {
                                    'rtt': 1.586,
                                    'ip_address': u'209.85.241.171',
                                    'host_name': u'209.85.241.171'
                                    },
                                2: {
                                    'rtt': 1.6300000000000001,
                                    'ip_address': u'209.85.241.171',
                                    'host_name': u'209.85.241.171'
                                },
                                3: {
                                    'rtt': 1.6480000000000001,
                                    'ip_address': u'209.85.241.171',
                                    'host_name': u'209.85.241.171'}
                                }
                            },
                        3: {
                            'probes': {
                                1: {
                                    'rtt': 2.529,
                                    'ip_address': u'216.239.49.123',
                                    'host_name': u'216.239.49.123'},
                                2: {
                                    'rtt': 2.474,
                                    'ip_address': u'209.85.255.255',
                                    'host_name': u'209.85.255.255'
                                },
                                3: {
                                    'rtt': 7.813,
                                    'ip_address': u'216.239.58.193',
                                    'host_name': u'216.239.58.193'}
                                }
                            },
                        4: {
                            'probes': {
                                1: {
                                    'rtt': 1.361,
                                    'ip_address': u'8.8.8.8',
                                    'host_name': u'google-public-dns-a.google.com'
                                },
                                2: {
                                    'rtt': 1.605,
                                    'ip_address': u'8.8.8.8',
                                    'host_name': u'google-public-dns-a.google.com'
                                },
                                3: {
                                    'rtt': 0.989,
                                    'ip_address': u'8.8.8.8',
                                    'host_name': u'google-public-dns-a.google.com'}
                                }
                            }
                        }
                    }

            OR

            {
                'error': 'unknown host 8.8.8.8.8'
            }
            """
        command = "traceroute " + destination
        if source:
            command = command + " source " + source
        if ttl:
            command = command + " ttl " + ttl
        if timeout:
            command = command + " wait " + timeout
        readed = self.ssh.send_command(command)
        lines = readed.splitlines()
        traceroute_dict = {}
        if 'traceroute to' in lines[1]:
            traceroute_dict['success'] = {}
            tpl_file = open("./traceroute.tpl")
            re_table = textfsm.TextFSM(tpl_file)
            results = re_table.ParseText(readed)[0]
            for hop, ip, name, rtt1, rtt2, rtt3 in zip(results[0], results[1], results[2], results[3], results[4],
                                                       results[5]):
                traceroute_dict['success'][hop] = {}
                traceroute_dict['success'][hop]['1'] = {'rtt': rtt1, 'ip_address': ip, 'host_name': name}
                traceroute_dict['success'][hop]['2'] = {'rtt': rtt2, 'ip_address': ip, 'host_name': name}
                traceroute_dict['success'][hop]['3'] = {'rtt': rtt3, 'ip_address': ip, 'host_name': name}
        # if any line starts with 'Error'. Return error
        elif 'Error' == lines[1][:5]:
                traceroute_dict['error'] = lines[1][7:]
        elif 'MINOR' == lines[1][:5]:
                traceroute_dict['error'] = lines[1][7:]
        return traceroute_dict

    def get_users(self):
        """
        Returns a dictionary with the configured users.
        The keys of the main dictionary represents the username. The values represent the details
        of the user, represented by the following keys:
            * level (int)
            * password (str)
            * sshkeys (list)

        The level is an integer between 0 and 15, where 0 is the lowest access and 15 represents
        full access to the device.

        Example::

            {
                'mircea': {
                    'level': 15,
                    'password': '$1$0P70xKPa$z46fewjo/10cBTckk6I/w/',
                    'sshkeys': [
                        'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC4pFn+shPwTb2yELO4L7NtQrKOJXNeCl1je\
                         l9STXVaGnRAnuc2PXl35vnWmcUq6YbUEcgUTRzzXfmelJKuVJTJIlMXii7h2xkbQp0YZIEs4P\
                         8ipwnRBAxFfk/ZcDsN3mjep4/yjN56eorF5xs7zP9HbqbJ1dsqk1p3A/9LIL7l6YewLBCwJj6\
                         D+fWSJ0/YW+7oH17Fk2HH+tw0L5PcWLHkwA4t60iXn16qDbIk/ze6jv2hDGdCdz7oYQeCE55C\
                         CHOHMJWYfN3jcL4s0qv8/u6Ka1FVkV7iMmro7ChThoV/5snI4Ljf2wKqgHH7TfNaCfpU0WvHA\
                         nTs8zhOrGScSrtb mircea@master-roshi'
                    ]
                }
            }
        """
        response = self.mgr.get_config("running")
        parsed = self._parse(response._raw)
        return self._extract_users(parsed)
        return parsed
