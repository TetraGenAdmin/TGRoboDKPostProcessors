# -*- coding: UTF-8 -*-
# Copyright 2015-2023 - RoboDK Inc. - https://robodk.com/
#
# This is a compiled post processor. Please contact us at info@robodk.com if you need access to the source code of this post processor.
#
# This file loads the compiled version of the RoboDK post processor for:
#   CLOOS robot controllers
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
exec("from v" + version_str + ".CLOOS import RobotPost as BasePost")

class RobotPost(BasePost):

    # ------------------------ Customize your RoboDK post processor using the following variables ------------------------

    # Enter the robot model (needed in the program file)
    ROBOT_MODEL = "310"

    # Enter the serial number (needed in the program file)
    SERIAL_NR = "3511462"

    PROG_EXT = "txt"    # set the program extension

    MAX_LINES_X_PROG = 5000    # maximum number of lines per program. It will then generate multiple "pages (files)". This can be overriden by RoboDK settings.

    SPEED_MMS = 50    # Default speed in mm/s

    INCLUDE_SUB_PROGRAMS = True    # Generate sub programs

    PULSES_ZERO = 4194304    # zero position for pulses

    # Path of the compiler to convert the ASCII file to a binary file
    PATH_MAKE_SP = "C:/Program Files (x86)/CLOOS/"

    # Pulses per degree (provide these in the robot parameters menu: Double click the motoman robot in RoboDK, select "Parameters"
    PULSES_X_DEG = [1, 1, 1, 1, 1, 1]

    # --------------------------------------------------------------------------------------------------------------------

    pass

if __name__== "__main__":
    exec("from v" + version_str + ".CLOOS import test_post")
    test_post()

