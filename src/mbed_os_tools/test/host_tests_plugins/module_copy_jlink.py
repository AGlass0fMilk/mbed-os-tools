# Copyright (c) 2018, Arm Limited and affiliates.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from .host_test_plugins import HostTestPluginBase

jlink_cmd_fmt = 'loadfile {}\n q\n'


class HostTestPluginCopyMethod_Jlink(HostTestPluginBase):

    # Plugin interface
    name = 'HostTestPluginCopyMethod_Jlink'
    type = 'CopyMethod'
    capabilities = ['jlink']
    required_parameters = ['image_path']

    def __init__(self):
        """ ctor
        """
        HostTestPluginBase.__init__(self)

    def is_os_supported(self, os_name=None):
        """ Supports all operating systems as long as JLinkExe is in the user's PATH
        """
        return True
    
    def setup(self, *args, **kwargs):
        """! Configure plugin, this function should be called before plugin execute() method is used.
        """
        self.JLINK_CLI = 'JLinkExe'
        return True

    def execute(self, capability, *args, **kwargs):
        """! Executes capability by name

        @param capability Capability name
        @param args Additional arguments
        @param kwargs Additional arguments

        @details Each capability e.g. may directly just call some command line program or execute building pythonic function

        @return Capability call return value
        """
        result = False
        if self.check_parameters(capability, *args, **kwargs) is True:
            image_path = os.path.normpath(kwargs['image_path'])
            if capability == 'jlink':
                # Example:
                # JLinkExe -device <name> -if SWD -speed 4000 -autoconnect 1 -CommanderScript <script>

                # Create the CommanderScript file
                cmd = ['echo', jlink_cmd_fmt.format(image_path), '>>', '.copy.jcmd']
                self.run_command(cmd)

                # Flash the target using the jcommand
                cmd = [self.JLINK_CLI,
                       '-device', 'STM32G031K8',
                       '-if', 'SWD',
                       '-speed', '4000',
                       '-autoconnect', '1',
                       '-CommanderScript', '.copy.jcmd']
                result = self.run_command(cmd)
                
                # Delete the CommanderScript file
                cmd = ['rm', '.copy.jcmd']
                self.run_command(cmd)
                
                cmd = [self.ST_LINK_CLI,
                       '-p', image_path, '0x08000000',
                       '-V'
                       ]
                result = self.run_command(cmd)
        return result


def load_plugin():
    """ Returns plugin available in this module
    """
    return HostTestPluginCopyMethod_Jlink()
