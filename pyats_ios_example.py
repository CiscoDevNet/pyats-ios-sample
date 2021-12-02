#!/bin/env python

'''pyats_ios_example.py

This is a testscript example intended to walk users through basic Cisco IOS
device connection, command execution and result verification using pyATS.


Arguments:
    This script requires one script argument (testbed) to be passed in when run
    under standalone execution for demonstration purposes.
    testbed: the path to testbed yaml file

Topology:

    +-------------+          Eth0/0 <-> Eth0/0           +-------------+
    |             | ------------------------------------ |             |
    |    ios1     |                                      |    ios2     |
    |             | ------------------------------------ |             |
    +-------------+          Eth0/1 <-> Eth0/1           +-------------+

Testing:
    This script performs the following tests for demonstration purposes.

    - router connection: basic device connection test

    - `ping` command: basic device ping test; logs ping result.

    - interface count verification

        - execute `show version` command: basic command execution and data
                                          parsing; extract ethernet and serial
                                          interface counts; logs interface
                                          counts.

        - execute `show ip interface brief` command: basic command execution and
                                                     data parsing; extract all
                                                     ethernet and serial
                                                     interfaces; logs number of
                                                     interface counts.

        - verify ethernet and serial interface counts from above commands.

    - router disconnect: basic device disconnect test

Examples:
    # to run under standalone execution
    bash$ python pyats_ios_example.py --testbed pyats_ios_example.yaml

References:
   For the complete and up-to-date user guide on pyATS, visit:
    https://developer.cisco.com/site/pyats/docs/
'''

#
# optional author information
#
__author__ = 'Wei Chen <weiche3@cisco.com>'
__copyright__ = 'Copyright 2017, Cisco Systems'
__email__ = 'pyats-support@cisco.com'
__date__= 'Nov 15, 2017'


#
# import statements
#
import re
import logging

from ats import aetest
from ats.log.utils import banner

#
# create a logger for this testscript
#
logger = logging.getLogger(__name__)

#
# Common Setup Section
#
class common_setup(aetest.CommonSetup):
    '''Common Setup Section

    Defines subsections that performs configuration common to the entire script.

    '''

    @aetest.subsection
    def check_topology(self,
                       testbed,
                       ios1_name = 'ios1',
                       ios2_name = 'ios2'):
        '''
        check that we have at least two devices and a link between the devices
        If so, mark the next subsection for looping.
        '''

        # abort/fail the testscript if no testbed was provided
        if not testbed or not testbed.devices:
            self.failed('No testbed was provided to script launch',
                        goto = ['exit'])

        # abort/fail the testscript if no matching device was provided
        for ios_name in (ios1_name, ios2_name):
            if ios_name not in testbed:
                self.failed('testbed needs to contain device {ios_name}'.format(
                                        ios_name=ios_name,
                                    ),
                            goto = ['exit'])

        ios1 = testbed.devices[ios1_name]
        ios2 = testbed.devices[ios2_name]

        # add them to testscript parameters
        self.parent.parameters.update(ios1 = ios1, ios2 = ios2)

        # get corresponding links
        links = ios1.find_links(ios2)
        assert len(links) >= 1, 'require one link between ios1 and ios2'

        # save link as uut link parameter
        self.parent.parameters['uut_link'] = links.pop()


    @aetest.subsection
    def establish_connections(self, steps, ios1, ios2):
        '''
        establish connection to both devices
        '''

        with steps.start('Connecting to Router-1'):
            ios1.connect()

        with steps.start('Connecting to Router-2'):
            ios2.connect()

        # abort/fail the testscript if any device isn't connected
        if not ios1.connected or not ios2.connected:
            self.failed('One of the two devices could not be connected to',
                        goto = ['exit'])

    @aetest.subsection
    def marking_interface_count_testcases(self, testbed):
        '''
        mark the VerifyInterfaceCountTestcase for looping.
        '''
        # ignore CML terminal_server
        devices = [d for d in testbed.devices.keys() if 'terminal_server' not in d]

        logger.info(banner('Looping VerifyInterfaceCountTestcase'
                           ' for {}'.format(devices)))

        # dynamic loop marking on testcase
        aetest.loop.mark(VerifyInterfaceCountTestcase, device = devices)


#
# Ping Testcase: leverage dual-level looping
#
@aetest.loop(device = ('ios1', 'ios2'))
class PingTestcase(aetest.Testcase):
    '''Ping test'''

    groups = ('basic', 'looping')

    @aetest.setup
    def setup(self, device, uut_link):
        destination = []
        parsed_dict = self.parent.parameters[device].parse('show ip interface brief')
        for intf in uut_link.interfaces:
            intf_ip = parsed_dict['interface'][intf.name]['ip_address']
            if intf_ip not in destination:
               destination.append(intf_ip)

        # apply loop to next section
        aetest.loop.mark(self.ping, destination = destination)


    @aetest.test
    def ping(self, device, destination):
        '''
        ping destination ip address from device

        Sample of ping command result:

        ping
        Protocol [ip]:
        Target IP address: 10.10.10.2
        Repeat count [5]:
        Datagram size [100]:
        Timeout in seconds [2]:
        Extended commands [n]: n
        Sweep range of sizes [n]: n
        Type escape sequence to abort.
        Sending 5, 100-byte ICMP Echos to 10.10.10.2, timeout is 2 seconds:
        !!!!!
        Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/1 ms

        '''

        try:
            # store command result for later usage
            result = self.parameters[device].ping(destination)

        except Exception as e:
            # abort/fail the testscript if ping command returns any exception
            # such as connection timeout or command failure
            self.failed('Ping {} from device {} failed with error: {}'.format(
                                destination,
                                device,
                                str(e),
                            ),
                        goto = ['exit'])
        else:
            # extract success rate from ping result with regular expression
            match = re.search(r'Success rate is (?P<rate>\d+) percent', result)
            success_rate = match.group('rate')
            # log the success rate
            logger.info(banner('Ping {} with success rate of {}%'.format(
                                        destination,
                                        success_rate,
                                    )
                               )
                        )

#
# Verify Interface Count Testcase
#
class VerifyInterfaceCountTestcase(aetest.Testcase):
    '''Verify interface count test'''

    groups = ('basic', 'looping')

    @aetest.test
    def extract_interface_count(self, device):
        '''
        extract interface counts from `show version`

        Sample of show version command result:

        show version
        Cisco IOS Software, IOSv Software (VIOS-ADVENTERPRISEK9-M), Version 15.6(2)T, RELEASE SOFTWARE (fc2)
        Technical Support: http://www.cisco.com/techsupport
        Copyright (c) 1986-2016 by Cisco Systems, Inc.
        Compiled Tue 22-Mar-16 16:19 by prod_rel_team


        ROM: Bootstrap program is IOSv

        ios2 uptime is 1 hour, 17 minutes
        System returned to ROM by reload
        System image file is "flash0:/vios-adventerprisek9-m"
        Last reload reason: Unknown reason

        <....>

        Cisco IOSv (revision 1.0) with  with 484609K/37888K bytes of memory.
        Processor board ID 9QTSICFAZS7Q2I61N8WNZ
        2 Gigabit Ethernet interfaces
        DRAM configuration is 72 bits wide with parity disabled.
        256K bytes of non-volatile configuration memory.
        2097152K bytes of ATA System CompactFlash 0 (Read/Write)
        0K bytes of ATA CompactFlash 1 (Read/Write)
        0K bytes of ATA CompactFlash 2 (Read/Write)
        10080K bytes of ATA CompactFlash 3 (Read/Write)



        Configuration register is 0x0

        '''

        try:
            # store execution result for later usage
            result = self.parameters[device].execute('show version')

        except Exception as e:
            # abort/fail the testscript if show version command returns any
            # exception such as connection timeout or command failure
            self.failed('Device {} \'show version\' failed: {}'.format(device,
                                                                       str(e)),
                        goto = ['exit'])
        else:
            # extract interfaces counts from `show version`
            match = re.search(r'(?P<ethernet>\d+) Gigabit Ethernet interfaces\r\n', result)
            ethernet_intf_count = int(match.group('ethernet'))
            # log the interface counts
            logger.info(banner('\'show version\' returns {} ethernet interfaces'
                                            .format(
                                            ethernet_intf_count

                                        )
                               )
                        )
            # add them to testcase parameters
            self.parameters.update(ethernet_intf_count = ethernet_intf_count,
                                   serial_intf_count = 0)

    @aetest.test
    def verify_interface_count(self,
                               device,
                               ethernet_intf_count = 0,
                               serial_intf_count = 0):
        '''
        verify interface counts with `show ip interface brief`

        Sample of show ip interface brief command result:

        show ip interface brief
        Interface                  IP-Address      OK? Method Status                Protocol
        GigabitEthernet0/0         unassigned      YES unset  administratively down down
        GigabitEthernet0/1         10.10.10.2      YES manual up                    up
        '''

        try:
            # store execution result for later usage
            result = self.parameters[device].execute('show ip interface brief')

        except Exception as e:
            # abort/fail the testscript if show ip interface brief command
            # returns any exception such as connection timeout or command
            # failure
            self.failed('Device {} \'show ip interface brief\' failed: '
                            '{}'.format(device, str(e)),
                        goto = ['exit'])
        else:
            # extract ethernet interfaces
            ethernet_interfaces = re.finditer(r'\r\nGigabitEthernet\d+/\d+\s+', result)
            # total number of ethernet interface
            len_ethernet_interfaces = len(tuple(ethernet_interfaces))

            # log the ethernet interface counts
            logger.info(banner('\'show ip interface brief\' returns {} ethernet'
                               ' interfaces'.format(len_ethernet_interfaces)))

            # compare the ethernet interface count between
            # `show ip interface brief` and `show version`
            assert len_ethernet_interfaces == ethernet_intf_count



class common_cleanup(aetest.CommonCleanup):
    '''disconnect from ios routers'''

    @aetest.subsection
    def disconnect(self, steps, ios1, ios2):
        '''disconnect from both devices'''

        with steps.start('Disconnecting from Router-1'):
            ios1.disconnect()

        with steps.start('Disconnecting from Router-2'):
            ios2.disconnect()

        if ios1.connected or ios2.connected:
            # abort/fail the testscript if device connection still exists
            self.failed('One of the two devices could not be disconnected from',
                        goto = ['exit'])


if __name__ == '__main__':

    # local imports
    import argparse
    from ats.topology import loader

    parser = argparse.ArgumentParser(description = "standalone parser")
    parser.add_argument('--testbed', dest = 'testbed',
                        type = loader.load)
    # parse args
    args, unknown = parser.parse_known_args()

    # and pass all arguments to aetest.main() as kwargs
    aetest.main(**vars(args))
