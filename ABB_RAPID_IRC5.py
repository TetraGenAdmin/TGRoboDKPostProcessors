# -*- coding: UTF-8 -*-
# Copyright 2015-2023 - RoboDK Inc. - https://robodk.com/
#
# This is a compiled post processor. Please contact us at info@robodk.com if you need access to the source code of this post processor.
#
# This file loads the compiled version of the RoboDK post processor for:
#   ABB RAPID IRC5 robot controllers
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
exec("from v" + version_str + ".ABB_RAPID_IRC5 import RobotPost as BasePost")

class RobotPost(BasePost):

    # ------------------------ Customize your RoboDK post processor using the following variables ------------------------

    # Set the program file extension:
    # PROG_EXT = 'prg' # S4 (older controllers)
    PROG_EXT = "mod"    # IRC5 (newer controllers)

    # Set if we want to generate the main/first program as a Main() program. The name of the main/first program will be replaced by Main()
    # Example: PROC Main() instead of PROG Prog1()
    # FIRST_PROG_AS_MAIN = False # It will generate PROG Prog1() (or the name set in the RoboDK program)
    FIRST_PROG_AS_MAIN = True    # It will generate PROG Main()

    # Default maximum number of lines per program. If a program exceeds this value it will then generate multiple "pages" (files)
    # This value can also be set in Tools-Options-Program-Maximum number of lines per program.
    # MAX_LINES_X_PROG = 5000  # recommended for S4:  5000
    MAX_LINES_X_PROG = 20000    # recommended for IRC5: 20000

    # Include subprograms in the main module:
    # Set to True to include sub programs in the same module
    INCLUDE_SUB_PROGRAMS = True

    # Specify the maximum lines of code allowed to include a subprogram in the main/first program
    # If a subprogram exceeds this number of lines of code it will be generated as a separate program file (module)
    MAX_SUBPROG_LINES = 500

    # External dripfeed: set to True if you use an external tool to load the programs (such as RAPBOX):
    # EXTERNAL_DRIPFEEDER = True # It will not generate a main program to load subprograms. Each subprogram will be called Main(). This is suitable for RAPBOX.
    EXTERNAL_DRIPFEEDER = False    # It will generate a main program to load subprograms.

    # Remote path to place programs in the robot controller
    # When program splitting takes place we need this path to load programs on the fly
    RAPID_REMOTE_PATH = "/hd0a/Enter-Serial-Number/HOME/RoboDK"

    # Set if you want to ignore the setup of the turntable (or external axis) on the controller
    # If you set it to True it means the controller will not be aware of the axis
    # (you can't move using a synchronized movement and the turntable will not hold the wobjdata)
    TURNTABLE_IGNORE = False    # default: False

    # Specify the mechanical unit name for linear track and/or turntable, if required.
    # This name will be added to the wobjdata variable
    # MECHANICAL_UNIT_NAME = 'T6003'
    # MECHANICAL_UNIT_NAME = 'STN1'
    MECHANICAL_UNIT_NAME = "Turntable_Mechanical_Unit_Name"

    # Set to False to use MoveJ for joint movements instead of MoveAbsJ
    MOVEJ_AS_MOVEABSJ = True

    # Enter the axes ratio for external axes, if required
    # AXES_RATIO = [1,1,1,1,1,1,  -1,1,1]
    AXES_RATIO = None

    # Enter the external axes indexes. For example, if you use one external axis mapped to index ext axis 5, you can use:
    # EXTAXES_IDX = [4,5]
    EXTAXES_IDX = [0, 1, 2, 3, 4, 5]

    # Default speed
    SPEED_MMS = 500

    # Default speed variable
    # Example: [500,500,5000,1000]
    SPEEDDATA = "v500"

    # Default rounding
    ZONEDATA = "z1"

    # Default tool
    TOOLDATA = "tool0"

    # Default reference
    WOBJDATA = "wobj0"

    # --------------------------------------------------------------------------------------------------------------------

    pass

if __name__== "__main__":
    exec("from v" + version_str + ".ABB_RAPID_IRC5 import test_post")
    test_post()

