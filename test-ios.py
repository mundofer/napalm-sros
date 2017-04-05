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

from napalm import get_network_driver
get_network_driver('ios')


class   Test:

    def __init__(self):
        device = None

    def testOpen(self):
        hostname = '172.16.123.3'
        username = 'tog'
        password = 'tog'

        #optional_args = {'port': 830, }
        driver = get_network_driver('ios')
        self.device = driver(hostname,username,password)

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

    def testGetConfig(self):
        config = self.device.get_config()
        print config

def main():
    test =Test()
    test.testOpen()
    test.testFacts()
    test.testAlive()
    #test.testCli()
    test.testInterfaces()
    test.testGetConfig()
    test.testClose()

if __name__ == "__main__":
    main()