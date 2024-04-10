# -*- coding: UTF-8 -*-
# Copyright 2015-2023 - RoboDK Inc. - https://robodk.com/
#
# This is a compiled post processor. Please contact us at info@robodk.com if you need access to the source code of this post processor.
#
# This file loads the compiled version of the RoboDK post processor for:
#   Precise robot controllers
#
# More information about RoboDK Post Processors and Offline Programming:
#     https://robodk.com/help#PostProcessor
#     https://robodk.com/doc/en/PythonAPI/postprocessor.html
# ----------------------------------------------------

import sys
import os

import math
from robodk import *

# Detect Python version and post processor
print("Using Python version: " + str(sys.version_info))
path_file = os.path.dirname(__file__).replace(os.sep, "/")
print("RoboDK Post Processor: " + path_file)

# Check if the post is compatible with the Python version
version_str = str(sys.version_info[0]) + str(sys.version_info[1])
path_library = path_file + '/v' + version_str
if not os.path.isdir(path_library):
    msg = "Invalid Python version or post processor not found. Make sure you are using a supported Python version: " + path_library
    msg += "\nSelect Tools-Options-Python and select a supported Python version"
    print(msg)
    raise Exception(msg)

# Load the post processor
exec("from v" + version_str + ".Precise import RobotPost as BasePost")

class RobotPost(BasePost):

    # ------------------------ Customize your RoboDK post processor using the following variables ------------------------

    PROG_EXT = "gpl"    # set the program extension

    # Maximum speed in mm/s (used to convert to percentage of nominal speed)
    # Typically 500 for PF400/PF3400 and 600 for DD4/DD6
    MAX_SPEED_MMS = 500

    # Maximum acceleration in mm/s^2 (used to convert to percentage of nominal acceleration)
    # Typically 2000 for PF400/PF3400, 5000 for DD4/DD6 and 1000 for PF100
    MAX_ACCEL_MMSS = 2000

    # Maximum speed in deg/s (used to convert to percentage of nominal speed)
    # Typically 720 for PF400/PF3400, 600 for DD4/DD6 and 1500 for PF100
    MAX_SPEED_DEGS = 720

    # Maximum acceleration in deg/s^2 (used to convert to percentage of nominal acceleration)
    # Typically 4000 for PF400, 2000 for PF3400, 5000 for DD4/DD6 and 10000 for PF100
    MAX_ACCEL_DEGSS = 4000

    # --------------------------------------------------------------------------------------------------------------------

    pass

if __name__== "__main__":
    exec("from v" + version_str + ".Precise import test_post")
    test_post()

