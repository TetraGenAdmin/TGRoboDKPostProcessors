# -*- coding: UTF-8 -*-
# Copyright 2015-2023 - RoboDK Inc. - https://robodk.com/
#
# This is a compiled post processor. Please contact us at info@robodk.com if you need access to the source code of this post processor.
#
# This file loads the compiled version of the RoboDK post processor for:
#   Motoman Cartesian robot controllers
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
exec("from v" + version_str + ".Motoman_Cartesian import RobotPost as BasePost")

class RobotPost(BasePost):

    # ------------------------ Customize your RoboDK post processor using the following variables ------------------------

    # Set the default maximum number of lines per program.
    # It will then generate multiple "pages (files)". This can be overriden by RoboDK settings.
    MAX_LINES_X_PROG = 2000

    # Set to True to use SETTOOL for setting the tool in the JBI program
    # USE_SETTOOL = False
    USE_SETTOOL = True    # This requires the SETTOOL option from Motoman (paid option)

    # Specify the default UTool Id to use (register).
    # You can also use Numbered tools in RoboDK (for example, a tool named "Tool 2" will use UTOOL number 2)
    ACTIVE_TOOL = 9

    # Set to False to always use pulses (otherwise, it may require a paid option)
    # USE_RELATIVE_JOB = False
    USE_RELATIVE_JOB = True    # This requires the Relative Job option from Motoman

    # Force joint movements to be in Cartesian
    MOVEJ_IN_CARTESIAN = False

    # Generate sub programs with each program
    INCLUDE_SUB_PROGRAMS = True

    # Specify a spare Position register for calculations (Tool, Reference, ...)
    SPARE_PR = 95

    # Set to True to use MFRAME for setting reference frames automatically within the program
    USE_MFRAME = False

    # Specify the default UFrame Id to use (register).
    # You can also use Numbered References in RoboDK (for example, a reference named "Reference 4" will use UFRAME number 4)
    ACTIVE_FRAME = 9

    # Specify if external axes are defined as a separate variable unit
    # (use EC instead of extending the default C register)
    EXTAXES_USE_EC = True

    # Specify if external axes must be moved according to a separate MOVJ command
    EXTAXES_USE_MOVJ = True    # Will output: MOVL C00008 V=166.7  +MOVJ EC00008 VJ=100.00

    # Specify the pulses/degree ratio for the external axes here (index 7,8,...)
    PULSES_X_DEG = [1, 1, 1, 1, 1, 1, 1.0, 1.0, 1, 1]

    # Option to swap a specific axis
    # AXIS_INDEX = [0,1,2,3,4,5,6,7] # example to swap axes 7 and 8 (external axes 1-2)
    AXIS_INDEX = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]    # table is already swaped (final ids)

    # --------------------------------------------------------------------------------------------------------------------

    pass

if __name__== "__main__":
    exec("from v" + version_str + ".Motoman_Cartesian import test_post")
    test_post()

