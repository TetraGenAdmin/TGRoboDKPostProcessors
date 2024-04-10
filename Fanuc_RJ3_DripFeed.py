# -*- coding: UTF-8 -*-
# Copyright 2015-2023 - RoboDK Inc. - https://robodk.com/
#
# This is a compiled post processor. Please contact us at info@robodk.com if you need access to the source code of this post processor.
#
# This file loads the compiled version of the RoboDK post processor for:
#   Fanuc RJ3 DripFeed robot controllers
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
exec("from v" + version_str + ".Fanuc_RJ3_DripFeed import RobotPost as BasePost")

class RobotPost(BasePost):

    # ------------------------ Customize your RoboDK post processor using the following variables ------------------------

    # maximum number of lines per program. It will then generate multiple "pages" (files).
    # This setting can be overriden by RoboDK settings (Tools-Options-Program)
    MAX_LINES_X_PROG = 9999

    # Generate sub programs
    INCLUDE_SUB_PROGRAMS = True

    # set default joint speed (percentage of the total speed)
    JOINT_SPEED = "20%"

    # set default cartesian speed motion
    SPEED = "200mm/sec"

    # set default CNT value (all motion until smooth value is changed)
    # CNT_VALUE = 'CNT5' # 5% smoothing (set CNT1-CNT100)
    CNT_VALUE = "FINE"

    # Set the acceleration value. For example: ACC20 or empty
    ACCEL_VALUE = ""

    # Active UFrame Id (register)
    ACTIVE_UF = 9

    # Active UTool Id (register)
    ACTIVE_UT = 9

    # Spare Position register for calculations (such as setting UFRAME and UTOOL)
    SPARE_PR = 9

    # Set the maximum index to use when linking to existing Frame IDs. This is a safety feature as linking to non valid IDs can make the controller behave unexpectedly
    MAX_FRAME_ID = 9

    # Set the maximum index to use when linking to existing Tool IDs. This is a safety feature as linking to non valid IDs can make the controller behave unexpectedly
    MAX_TOOL_ID = 9

    # Custom string to add at the end of each linear movement. For example: Offset,PR[1], or COORD
    CUSTOM_STRING = ""

    # Custom string to add at the end of each joint movement. For example: Offset,PR[1], or COORD
    CUSTOM_STRING_J = ""

    # Set the turntable grup (usually GP2 or GP3)
    TURNTABLE_GROUP = "GP2"    # TURNTABLE_GROUP = 'GP3'

    # Always use RoboDK user frames (references)
    USE_ROBODK_UFRAME = False

    # Always use RoboDK tool frames (tools)
    USE_ROBODK_UTOOL = False

    # Set to True to generate programs compatible with RJ3 controllers (small difference in the program header, program names should have less than 6-8 characters)
    FANUC_RJ3_COMPATIBLE = True

    # Max program characters:
    MAX_PROG_CHARS = 6

    # Compile LS program to TP programs
    # More help here: https://robodk.com/doc/en/Robots-Fanuc.html#LSvsTP
    # Set the path to Roboguide WinOLPC tools, alternatively, set to None to prevent generating TP files
    # This step is ignored if the path does not exist
    PATH_MAKE_TP = "C:/Program Files (x86)/FANUC/WinOLPC/bin/"    # PATH_MAKE_TP = None # Ignore program compilation

    # Generate a drip feeder program: this will split long programs in subprograms and load them to the controller as they are executed
    # Set a file name to use an automatic dripfeeder: Files will be sent over FTP as they are executed
    # Right click a program and select "Send Program to Robot" to trigger the dripfeeding automatically
    DRIPFEED_FILE_NAME = "Fanuc_SendProgram_DripFeed.py"

    # Always force user input to save the folder
    FORCE_POPUP_SAVE = True

    # Set to True for a 5-axis robot arm that is modelled like a 6-axis robot
    # This flag is automatically set to True for 5-axis robots such as the Fanuc LR Mate 100i
    IS_5DOF_ARM = False

    # --------------------------------------------------------------------------------------------------------------------

    pass

if __name__== "__main__":
    exec("from v" + version_str + ".Fanuc_RJ3_DripFeed import test_post")
    test_post()

