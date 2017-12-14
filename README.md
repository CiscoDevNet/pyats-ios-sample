# pyats-ios-sample
Here’s a full test script in pyATS with local libraries that connects to a
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

    +-------------+          Eth0/0 <-> Eth0/0           +-------------+
    |             | ------------------------------------ |             |
    |    ios1     |                                      |    ios2     |
    |             | ------------------------------------ |             |
    +-------------+          Eth0/1 <-> Eth0/1           +-------------+
```

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
