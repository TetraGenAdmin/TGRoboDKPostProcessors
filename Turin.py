# -*- coding: UTF-8 -*-
# Copyright 2015-2023 - RoboDK Inc. - https://robodk.com/
#
# This is a compiled post processor. Please contact us at info@robodk.com if you need access to the source code of this post processor.
#
# This file loads the compiled version of the RoboDK post processor for:
#   Turin robot controllers
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
exec("from v" + version_str + ".Turin import RobotPost as BasePost")

class RobotPost(BasePost):

    # ------------------------ Customize your RoboDK post processor using the following variables ------------------------

    # Set the output program extension (for multiple files, handle separately)
    PROG_EXT = "txt"

    # Default speed for linear moves in mm/s
    SPEED_MMS = 250

    # Maximum speed for linear moves in mm/s (to convert in %)
    MAX_SPEED_MMS = 5000

    # Default speed for joint moves in deg/s
    SPEED_DEGS = 500

    # Maximum speed for joint moves in deg/s (to convert in %)
    MAX_SPEED_DEGS = 5000

    # Default acceleration for linear moves in mm/s^2
    ACCEL_MMSS = 1500

    # Maximum acceleration for linear moves in mm/s^2 (to convert in %)
    MAX_ACCEL_MMSS = 5000

    # Default acceleration for joint moves in deg/s^2
    ACCEL_DEGSS = 200

    # Maximum acceleration for joint moves in deg/s^2 (to convert in %)
    MAX_ACCEL_DEGSS = 2000

    # Default blend radius in millimeters
    BLEND_RADIUS_MM = 0.0

    # Maximum blend radius in millimeters (to convert to %)
    MAX_BLEND_RADIUS_MM = 100

    # --------------------------------------------------------------------------------------------------------------------

    pass

if __name__== "__main__":
    exec("from v" + version_str + ".Turin import test_post")
    test_post()

