# pyats-ios-sample

# Introduction

This repo provides a demonstration of Cisco pyATS with a NetDevOps style workflow.

# Requirements

* Python 2.7
* Docker

# Workflow

### Make sure virl cli is configured

```
export VIRL_HOST=myvirlserver.change.me
```

### Clone this repo / create virtualenv / install requirements

```
git clone https://github.com/kecorbin/pyats-ios-sample
cd pyats-ios-sample
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

```

### Launch topology

```
virl up
```
It may take a minute to boot the nodes, make sure that you allow enough time for
the topology to boot. This can be verified using the `virl ls` and `virl nodes`
commands

#### Sample outputs

```
virl ls

Running Simulations
╒═════════════════════════════════╤══════════╤════════════════════════════╤═══════════╕
│ Simulation                      │ Status   │ Launched                   │ Expires   │
╞═════════════════════════════════╪══════════╪════════════════════════════╪═══════════╡
│ pyats-ios-sample_default_UbI56G │ ACTIVE   │ 2017-12-13T22:02:36.810310 │           │
╘═════════════════════════════════╧══════════╧════════════════════════════╧═══════════╛

virl nodes


    Here is a list of all the running nodes

╒═══════════╤══════════╤═════════╤═════════════╤════════════╤══════════════════════╤════════════════════╕
│ Node      │ Type     │ State   │ Reachable   │ Protocol   │ Management Address   │ External Address   │
╞═══════════╪══════════╪═════════╪═════════════╪════════════╪══════════════════════╪════════════════════╡
│ ~mgmt-lxc │ mgmt-lxc │ ACTIVE  │ REACHABLE   │ ssh        │ 10.255.0.154         │ 10.94.238.236      │
├───────────┼──────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ ios2      │ IOSv     │ ACTIVE  │ UNREACHABLE │ telnet     │ 10.255.0.156         │ N/A                │
├───────────┼──────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ ios1      │ IOSv     │ ACTIVE  │ UNREACHABLE │ telnet     │ 10.255.0.155         │ N/A                │
╘═══════════╧══════════╧═════════╧═════════════╧════════════╧══════════════════════╧════════════════════╛

```

### Generate pyATS testbed inventory

The virlutils package provides us an easy way of dynamically generating a testbed
definition with the accurate connectivity information for the simulation.

```
virl generate pyats
```


### Verify

Launch pyATS test suite

```
make test
```

#### Sample output

```
2017-12-13T23:01:17: %EASYPY-INFO: +------------------------------------------------------------------------------+
2017-12-13T23:01:17: %EASYPY-INFO: |                             Task Result Summary                              |
2017-12-13T23:01:17: %EASYPY-INFO: +------------------------------------------------------------------------------+
2017-12-13T23:01:17: %EASYPY-INFO: __task1: pyats_ios_example.commonSetup                                    PASSED
2017-12-13T23:01:17: %EASYPY-INFO: __task1: pyats_ios_example.PingTestcase[device=ios1]                      PASSED
2017-12-13T23:01:17: %EASYPY-INFO: __task1: pyats_ios_example.PingTestcase[device=ios2]                      PASSED
2017-12-13T23:01:17: %EASYPY-INFO: __task1: pyats_ios_example.VerifyInterfaceCountTestcase[device=ios1]      PASSED
2017-12-13T23:01:17: %EASYPY-INFO: __task1: pyats_ios_example.VerifyInterfaceCountTestcase[device=ios2]      PASSED
2017-12-13T23:01:17: %EASYPY-INFO: __task1: pyats_ios_example.commonCleanup                                  PASSED
2017-12-13T23:01:17: %EASYPY-INFO:
2017-12-13T23:01:17: %EASYPY-INFO: +------------------------------------------------------------------------------+
2017-12-13T23:01:17: %EASYPY-INFO: |                             Task Result Details                              |
2017-12-13T23:01:17: %EASYPY-INFO: +------------------------------------------------------------------------------+
2017-12-13T23:01:17: %EASYPY-INFO: __task1: pyats_ios_example
2017-12-13T23:01:17: %EASYPY-INFO: |-- commonSetup                                                           PASSED
2017-12-13T23:01:17: %EASYPY-INFO: |   |-- check_topology                                                    PASSED
2017-12-13T23:01:17: %EASYPY-INFO: |   |-- establish_connections                                             PASSED
2017-12-13T23:01:17: %EASYPY-INFO: |   |   |-- Step 1: Connecting to Router-1                                PASSED
2017-12-13T23:01:17: %EASYPY-INFO: |   |   `-- Step 2: Connecting to Router-2                                PASSED
2017-12-13T23:01:17: %EASYPY-INFO: |   `-- marking_interface_count_testcases                                 PASSED
2017-12-13T23:01:17: %EASYPY-INFO: |-- PingTestcase[device=ios1]                                             PASSED
2017-12-13T23:01:17: %EASYPY-INFO: |   |-- ping[destination=10.10.10.1]                                      PASSED
2017-12-13T23:01:17: %EASYPY-INFO: |   `-- ping[destination=10.10.10.2]                                      PASSED
2017-12-13T23:01:17: %EASYPY-INFO: |-- PingTestcase[device=ios2]                                             PASSED
2017-12-13T23:01:17: %EASYPY-INFO: |   |-- ping[destination=10.10.10.1]                                      PASSED
2017-12-13T23:01:17: %EASYPY-INFO: |   `-- ping[destination=10.10.10.2]                                      PASSED
2017-12-13T23:01:17: %EASYPY-INFO: |-- VerifyInterfaceCountTestcase[device=ios1]                             PASSED
2017-12-13T23:01:17: %EASYPY-INFO: |   |-- extract_interface_count                                           PASSED
2017-12-13T23:01:17: %EASYPY-INFO: |   `-- verify_interface_count                                            PASSED
2017-12-13T23:01:17: %EASYPY-INFO: |-- VerifyInterfaceCountTestcase[device=ios2]                             PASSED
2017-12-13T23:01:17: %EASYPY-INFO: |   |-- extract_interface_count                                           PASSED
2017-12-13T23:01:17: %EASYPY-INFO: |   `-- verify_interface_count                                            PASSED
2017-12-13T23:01:17: %EASYPY-INFO: `-- commonCleanup                                                         PASSED
2017-12-13T23:01:17: %EASYPY-INFO:     `-- disconnect                                                        PASSED
2017-12-13T23:01:17: %EASYPY-INFO:         |-- Step 1: Disconnecting from Router-1                           PASSED
2017-12-13T23:01:17: %EASYPY-INFO:         `-- Step 2: Disconnecting from Router-2                           PASSED
2017-12-13T23:01:17: %EASYPY-INFO: No SMTP server information configured, ignoring sending notification email.
2017-12-13T23:01:17: %EASYPY-INFO: Done!

```

# pyATS details

This repo contains a full test script in pyATS with local libraries that connects to a
testbed of IOS devices, and runs various test cases that parses command outputs,
collects router information, and report them in log.

## General Information

- Website: https://developer.cisco.com/site/pyats/
- Bug Tracker: https://github.com/CiscoTestAutomation/pyats/issues
- Documentation: https://developer.cisco.com/site/pyats/docs/

## Arguments

This script requires one script argument `testbed` to be passed in when run
under standalone execution for demonstration purposes.
testbed: the path to testbed yaml file

This script requires one script argument `testbed_file` and two optional
script argument `ios1` and `ios2` to be passed in when run under easypy for
demonstration purposes.

    testbed_file: the path to testbed yaml file
    ios1: the device name defined in the testbed yaml file, if modified
    ios2: the device name defined in the testbed yaml file, if modified

## Topology

```

    +-------------+                                      +-------------+
    |             |                                      |             |
    |    ios1     | ------------------------------------ |    ios2     |
    |             |          Gig0/1 <-> Gig0/1           |             |
    +-------------+                                      +-------------+

## Testing

This script performs the following tests for demonstration purposes.

- router connection: basic device connection test
- `ping` command: basic device ping test; logs ping result.
- interface count verification
  - execute `show version` command: basic command execution and data
    parsing; extract ethernet and serial interface counts; logs interface
    counts.
  - execute `show ip interface brief` command: basic command execution and
    data parsing; extract all ethernet and serial interfaces; logs number of
    interface counts.
  - verify ethernet and serial interface counts from above commands.
- router disconnect: basic device disconnect test

## Examples

```
# to run under standalone execution
$ python pyats_ios_example.py --testbed pyats_ios_example.yaml

# to run under easypy
$ easypy pyats_ios_example_job.py -testbed_file pyats_ios_example.yaml
```

References:
   For the complete and up-to-date user guide on pyATS, visit:
    https://developer.cisco.com/site/pyats/docs/