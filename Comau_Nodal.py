# -*- coding: UTF-8 -*-
# Copyright 2015-2023 - RoboDK Inc. - https://robodk.com/
#
# This is a compiled post processor. Please contact us at info@robodk.com if you need access to the source code of this post processor.
#
# This file loads the compiled version of the RoboDK post processor for:
#   Comau Nodal robot controllers
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
exec("from v" + version_str + ".Comau_Nodal import RobotPost as BasePost")

class RobotPost(BasePost):

    # ------------------------ Customize your RoboDK post processor using the following variables ------------------------

    # Set to False to use MoveJ for joint movements using pose data
    MOVEJ_USES_JOINTS = True

    # Default speed in mm/s
    SPEED_MMS = 100

    # Default speed variable for linear movements, in mm/s
    SPEEDDATA = "VLMax"

    # Default speed variable for joint movements, in deg/s
    SPEEDDATA_J = "VJMax"

    # Default rounding (zone data)
    ZONEDATA = "ZFine"

    ZONEDATAJOINT = "ZJFine"

    # Default tool
    TOOLDATA = "T0"

    # Default reference
    WOBJDATA = "F0"

    # In general, one tab equals 2 spaces, 4 spaces or a tab
    ONETAB = "  "

    # Add the variable names you want to skip
    CUSTOM_RESERVED_NAMES = []

    # Set EXT_POSEXT to define external axes as POSEXT variables (inlined)
    # If set to False, it will use XTNDPOS instead
    EXT_POSEXT = False

    # Set the program file extension:
    PROG_EXT = "pdl"

    PROG_EXT_DATA = "lsv"

    # Default WeaveData used for Arc welding
    ARC_WEAVEDATA = "WeaveData"

    # Default SeamData used for Arc welding
    ARC_SEAMDATA = "SeamData"

    # Set if we want to generate the main/first program as a Main() program. The name of the main/first program will be replaced by Main()
    # Example: PROC Main() instead of PROG Prog1()
    # FIRST_PROG_AS_MAIN = False # It will generate PROG Prog1() (or the name set in the RoboDK program)
    FIRST_PROG_AS_MAIN = True    # It will generate PROG Main()

    # Default maximum number of lines per program. If a program exceeds this value it will then generate multiple "pages" (files)
    # This value can also be set in Tools-Options-Program-Maximum number of lines per program.
    MAX_LINES_X_PROG = 20000

    # Include subprograms in the main module:
    # Set to True to include sub programs in the same module
    INCLUDE_SUB_PROGRAMS = False

    # Enter the axes ratio for external axes, if required
    # RATIO_EXTAX = [1,1,1,1,1,1,  -1,1,1]
    RATIO_EXTAX = None

    # Enter the external axes indexes. For example, if you use one external axis mapped to index ext axis 5, you can use:
    # EXTAXES_IDX = [4,5]
    EXTAXES_IDX = [0, 1, 2, 3, 4, 5]

    # Init routine for programs
    init_routine = r"""
  $ORNT_TYPE := RS_WORLD
  $MOVE_TYPE := JOINT
  $JNT_MTURN := TRUE
  $CNFG_CARE := TRUE
  $TURN_CARE := TRUE
  $SING_CARE := FALSE
  $TERM_TYPE := NOSETTLE
  $FLY_TYPE := FLY_CART
  $FLY_TRAJ := FLY_PASS
  $STRESS_PER:= 65
"""

    # --------------------------------------------------------------------------------------------------------------------

    pass

if __name__== "__main__":
    exec("from v" + version_str + ".Comau_Nodal import test_post")
    test_post()

