# -*- coding: UTF-8 -*-
# Copyright 2015-2023 - RoboDK Inc. - https://robodk.com/
#
# This is a compiled post processor. Please contact us at info@robodk.com if you need access to the source code of this post processor.
#
# This file loads the compiled version of the RoboDK post processor for:
#   JAKA robot controllers
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
exec("from v" + version_str + ".JAKA import RobotPost as BasePost")

class RobotPost(BasePost):

    # ------------------------ Customize your RoboDK post processor using the following variables ------------------------

    # Default maximum number of lines per program. If a program exceeds this value it will then generate multiple "pages" (files)
    # This value can also be set in Tools-Options-Program-Maximum number of lines per program.
    MAX_LINES_X_PROG = 1000000000.0

    PROG_EXT = "jks"    # Set the program extension

    PROG_EXT_ZU = "zu"    # Set the Zu file extension

    PROG_EXT_ZUS = "zus"    # Set the Zus (sub programs) file extension

    # Default speed for linear moves in mm/s
    SPEED_MMS = 250

    # Default speed for joint moves in deg/s
    SPEED_DEGS = 60

    # Default acceleration for linear moves in mm/s^2
    ACCEL_MMSS = 250

    # Default acceleration for joint moves in deg/s^2
    ACCEL_DEGSS = 200

    # Default blend radius in millimeters (corners smoothing)
    BLEND_RADIUS_MM = 1.0

    # Minimum circle radius to output (in mm). It does not take into account the Blend radius
    MOVEC_MIN_RADIUS = 1

    # Maximum circle radius to output (in mm). It does not take into account the Blend radius
    MOVEC_MAX_RADIUS = 10000

    # --------------------------------------------------------------------------------------------------------------------

    pass

if __name__== "__main__":
    exec("from v" + version_str + ".JAKA import test_post")
    test_post()

