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
Manages a Nokia configuration as a tree.

Read https://napalm.readthedocs.io for more information.
"""

class ConfElement:
    """
    Each element
    """

    def __

class ConfTree:

    def __init__(self, source):
        """
        :param source: source config file in text form to be parded
        :return: nothing
        First we can have the prolog, <?xml... (optional)
        And then the root element that must be rpc-reply followed by a child name data
        If that structure is not meet, we generate an error.
        """
        # Convert to list of lines
        lines = source.splitlines()
        if not self._check_prolog(lines[0]):
            raise (Exception("Incorrect config format returned"))


    def _check_prolog(self,line):
        """
        :param line: first line of xml config
        :return: True if line valid, False if not valid
        """
        correct, elements = self._get
