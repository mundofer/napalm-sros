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

"""Tests."""

import unittest

from napalm_sros import sros
from napalm_base.test.base import TestConfigNetworkDriver


class   Test:

    def __init__(self):
        device = None

    def testOpen(self):
        hostname = '10.246.212.53'
        username = 'fgf'
        password = 'fgf'

        optional_args = {'port': 830, }
        self.device = sros.SRosDriver(hostname, username, password, timeout=10,
                                             optional_args=optional_args)
        self.device.open()

    def testFacts(self):
        facts = self.device.get_facts()
        print facts

    def testClose(self):
        self.device.close()

    def testAlive(self):
        if self.device.is_alive():
            print "Alive"
        else:
            print "Dead"

    def testCli(self):
        commands = ["show snmp counters","show system alarms"]
        print self.device.cli(commands)

    def testInterfaces(self):
        interfaces = self.device.get_interfaces()
        print interfaces

    def testPorts(self):
        ports = self.device.get_ports()
        print ports

    def testInterfacesIP(self):
        interfaces = self.device.get_interfaces_ip()
        print interfaces

    def testGetConfig(self):
        config = self.device.get_config()
        #self.print_tree(config)
        print config['running']

    def print_tree(self,tree):
        for element in tree.iter():
            print element.tag,element.text

    def testPing(self):
        print self.device.ping("10.246.212.254")

    def testTraceroute(self):
        print self.device.traceroute("10.246.212.254")

    def testUsers(self):
        print self.device.get_users()

def main():
    test =Test()
    test.testOpen()
    """
    test.testFacts()
    test.testAlive()
    test.testCli()
    test.testPorts()
    test.testInterfaces()
    test.testInterfacesIP()
    """
    test.testUsers()
    test.testPing()
    test.testTraceroute()
    test.testGetConfig()
    """
    """
    test.testClose()

if __name__ == "__main__":

    main()