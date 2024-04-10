# -*- coding: UTF-8 -*-
# Copyright 2015-2023 - RoboDK Inc. - https://robodk.com/
#
# This is a compiled post processor. Please contact us at info@robodk.com if you need access to the source code of this post processor.
#
# This file loads the compiled version of the RoboDK post processor for:
#   Universal Robots Conveyor robot controllers
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
exec("from v" + version_str + ".Universal_Robots_Conveyor import RobotPost as BasePost")

class RobotPost(BasePost):

    # ------------------------ Customize your RoboDK post processor using the following variables ------------------------

    MAX_LINES_X_PROG = 250    # Maximum number of lines per program. If the number of lines is exceeded, the program will be executed step by step by RoboDK

    PROG_EXT = "script"    # set the program extension

    SPEED_MS = 0.3    # default speed for linear moves in m/s

    SPEED_RADS = 0.75    # default speed for joint moves in rad/s

    ACCEL_MSS = 3    # default acceleration for lineaer moves in m/ss

    ACCEL_RADSS = 1.2    # default acceleration for joint moves in rad/ss

    BLEND_RADIUS_M = 0.001    # default blend radius in meters (corners smoothing)

    MOVEC_MIN_RADIUS = 1    # minimum circle radius to output (in mm). It does not take into account the Blend radius

    MOVEC_MAX_RADIUS = 10000    # maximum circle radius to output (in mm). It does not take into account the Blend radius

    USE_MOVEP = False

    PULSES_X_MM = 10    # Ticks/pulses per millimeter

    # --------------------------------------------------------------------------------------------------------------------

    pass

if __name__== "__main__":
    exec("from v" + version_str + ".Universal_Robots_Conveyor import test_post")
    test_post()
