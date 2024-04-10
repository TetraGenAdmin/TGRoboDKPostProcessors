# -*- coding: UTF-8 -*-
# Copyright 2015-2023 - RoboDK Inc. - https://robodk.com/
#
# This is a compiled post processor. Please contact us at info@robodk.com if you need access to the source code of this post processor.
#
# This file loads the compiled version of the RoboDK post processor for:
#   AUBO robot controllers
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
exec("from v" + version_str + ".AUBO import RobotPost as BasePost")

class RobotPost(BasePost):

    # ------------------------ Customize your RoboDK post processor using the following variables ------------------------

    SPEED_MS = 0.25    # default speed for linear moves in m/s

    SPEED_RADS = 0.3    # default speed for joint moves in rad/s

    ACCEL_MSS = 0.25    # default acceleration for lineaer moves in m/s^2

    ACCEL_RADSS = 1.1    # default acceleration for joint moves in rad/s^2

    BLEND_RADIUS_M = 0.001    # default blend radius in meters (corners smoothing)

    LINEAR_SPEED_MAX = 2000.0    # Maximum linear speed used to convert to %, in mm/s. i.e. 1000/2000=50%

    LINEAR_ACCEL_MAX = 4000.0    # Maximum linear acceleration used to convert to %, in mm/s^2. i.e. 2000/4000=50%

    JOINT_SPEED_MAX = 150.0    # Maximum joint speed (all joints) used to convert to %, in deg/s. i.e. 75/150=50%

    JOINT_ACCEL_MAX = 1000.0    # Maximum joint acceleration (all joints) used to convert to %, in deg/s^2. i.e. 500/1000=50%

    CIRCULAR_SPEED_MAX = 2000.0    # Maximum circular speed used to convert to %, in mm/s. i.e. 1000/2000=50%

    CIRCULAR_ACCEL_MAX = 2000.0    # Maximum circular acceleration used to convert to %, in mm/s^2. i.e. 1000/2000=50%

    # --------------------------------------------------------------------------------------------------------------------

    pass

if __name__== "__main__":
    exec("from v" + version_str + ".AUBO import test_post")
    test_post()

