# -*- coding: UTF-8 -*-
# Copyright 2015-2023 - RoboDK Inc. - https://robodk.com/
#
# This is a compiled post processor. Please contact us at info@robodk.com if you need access to the source code of this post processor.
#
# This file loads the compiled version of the RoboDK post processor for:
#   Robostar robot controllers
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
exec("from v" + version_str + ".Robostar import RobotPost as BasePost")

class RobotPost(BasePost):

    # ------------------------ Customize your RoboDK post processor using the following variables ------------------------

    # Set the default maximum number of lines per program.
    # It will then generate multiple "pages (files)". This can be overriden by RoboDK settings.
    MAX_LINES_X_PROG = 1900

    # Set the default maximum number of points per program
    # It will then generate multiple "pages (files)" (this setting will not be overriden by RoboDK)
    # Default is 1000
    MAX_PNT_X_PROG = 1000

    # Specify the default Tool Id to use (register).
    # You can also use Numbered tools in RoboDK (for example, a tool named "Tool 2" will use TOOL number 2)
    ACTIVE_TOOL = 0

    # Default active reference frame (base assumed)
    # You can also use Numbered frames in RoboDK (for example, a reference named "Frame 3" will use BASE number 3)
    ACTIVE_FRAME = 0

    # Robot Arm ID
    ARM_ID = 0

    # Set to True to always use joint output
    # FORCE_JOINT_OUTPUT = True # POS
    FORCE_JOINT_OUTPUT = False    # XPOS or UPOS

    # Output Cartesian targets with respect to the reference frame or with respect to a coordinate system
    # Important: this is only valid if FORCE_JOINT_OUTPUT == False
    # CALC_BASE_TARGETS = True # XPOS
    CALC_BASE_TARGETS = False    # UPOS

    # Force joint movements to be in Cartesian
    MOVEJ_IN_CARTESIAN = False

    # Generate sub programs with each program
    INCLUDE_SUB_PROGRAMS = True

    # Configuration behavior for Shoulder
    CONFIG_SHOULDER = None    # Provided by RoboDK

    # Configuration behavior for Elbow
    CONFIG_ELBOW = None    # Provided by RoboDK

    # Configuration behavior for Shoulder
    CONFIG_WRIST = None    # Provided by RoboDK

    # Default configuration for joint moves (should not be required)
    CONFIG_JOINTS = "000"

    # Specify a spare Position register for calculations (Tool, Reference, ...)
    SPARE_PR = 95

    # Specify the pulses/degree ratio for the external axes here (index 7,8,...)
    PULSES_X_DEG = [1, 1, 1, 1, 1, 1, 1.0, 1.0, 1, 1]

    # Option to swap a specific axis
    AXIS_INDEX = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]    # table is already swaped (final ids)

    # --------------------------------------------------------------------------------------------------------------------

    pass

if __name__== "__main__":
    exec("from v" + version_str + ".Robostar import test_post")
    test_post()

