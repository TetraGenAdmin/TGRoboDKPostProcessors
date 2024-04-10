# -*- coding: UTF-8 -*-
# Copyright 2015-2023 - RoboDK Inc. - https://robodk.com/
#
# This is a compiled post processor. Please contact us at info@robodk.com if you need access to the source code of this post processor.
#
# This file loads the compiled version of the RoboDK post processor for:
#   Techman Remote robot controllers
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
exec("from v" + version_str + ".Techman_Remote import RobotPost as BasePost")

class RobotPost(BasePost):

    # ------------------------ Customize your RoboDK post processor using the following variables ------------------------

    # Robot IP (should be provided by RoboDK when the program is generated)
    ROBOT_IP = "192.168.1.100"

    MAX_LINES_X_PROG = 1000000000.0    # 250    # Maximum number of lines per program. If the number of lines is exceeded, the program will be executed step by step by RoboDK

    PROG_EXT = "script"    # set the program extension

    SPEED_MMS = 50    # default speed for linear moves in m/s

    SPEED_PERCENT = 10    # default speed for joint moves in percentage

    SPEED_DEGS = 30    # default speed for joint moves in deg/s

    ACCEL_MMSS = 100    # default acceleration for lineaer moves in mm/ss

    ACCEL_DEGSS = 200    # default acceleration for joint moves in deg/ss

    ROUNDING = 1    # default blend radius as a percentage

    USE_MOVEP = False

    TAB_CHAR = ""

    # --------------------------------------------------------------------------------------------------------------------

    pass

if __name__== "__main__":
    exec("from v" + version_str + ".Techman_Remote import test_post")
    test_post()

