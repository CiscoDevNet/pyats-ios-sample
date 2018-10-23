import sys
from IPython import embed
import logging
import unicon

from genie.conf import Genie
from ats.topology import loader
from genie.abstract import Lookup
from genie.libs import ops # noqa





if __name__ == '__main__':

    # local imports
    import argparse

    parser = argparse.ArgumentParser(description="standalone parser")
    parser.add_argument('--testbed', default='./default_testbed.yaml',
                        dest='testbed', type=loader.load)
    parser.add_argument('--device', dest='device_name')

    args, unknown = parser.parse_known_args()

    device_name = args.device_name

    # pyats testbed != genie testbed
    genie_testbed = Genie.init(args.testbed)

    # this gives us device_name as Device Object e.g dist1
    vars()[device_name] = genie_testbed.devices[device_name]
    # or we can also just use `device`
    device = vars()[device_name]

    # logger = logging.getLogger("UNICON")
    # unicon.logs.remove_stream_handler(logging)

    # connect to the device (quietly)
    import time
    print("pyATS and Genie are about to profile the device and create structured data for "
          "you to use")
    time.sleep(10)
    device.connect()


    # work with an abstracted device model
    abstract = Lookup.from_device(device)

    # interface info is always a good place to start..
    interfaces = abstract.ops.interface.interface.Interface(device)
    interfaces.learn()

    print("""

    Welcome to the device object tutorial, as you may have noticed, Genie was
    busy profiling all of the interfaces of your device.  you can access them via

    interfaces.info

    you can interact with your device using either `device` or the device name
    you specified with --device

    You can start by exploring some of the common operations available for the
    device by typing

    dir(device)

    you can also explore the rest of the genie models at:

    https://pubhub.devnetcloud.com/media/pyats-packages/docs/genie/genie_libs/#/models

    Enjoy!

    """)


    embed()
