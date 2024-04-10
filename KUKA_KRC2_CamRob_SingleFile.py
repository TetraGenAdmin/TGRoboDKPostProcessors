# -*- coding: UTF-8 -*-
# Copyright 2015-2023 - RoboDK Inc. - https://robodk.com/
#
# This is a compiled post processor. Please contact us at info@robodk.com if you need access to the source code of this post processor.
#
# This file loads the compiled version of the RoboDK post processor for:
#   KUKA KRC2 CamRob SingleFile robot controllers
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
exec("from v" + version_str + ".KUKA_KRC2_CamRob_SingleFile import RobotPost as BasePost")

class RobotPost(BasePost):

    # ------------------------ Customize your RoboDK post processor using the following variables ------------------------

    # Set the program file extension:
    PROG_EXT = "src"

    # Include subprograms in the main module:
    # Set to True to include sub programs in the same module
    INCLUDE_SUB_PROGRAMS = True

    # You can also specify the maximum lines of code allowed to include a subprogram in the main/first program
    # If a subprogram exceeds this number of lines of code it will be generated as a separate module
    MAX_SUBPROG_LINES = 500

    # Generate a JOB file as a summary
    GENERATE_JOB_FILE = True

    # Use a synchronized external axis as an extruder (E1, E2, ... or the last available axis)
    # EXTAXIS_EXTRUDER = True
    EXTAXIS_EXTRUDER = True

    PRINT_E_NEW_MOTOR = 0    # External axis value to start controlling the Extruder

    # --------------------------------------------------------------------------------------------------------------------

    pass

if __name__== "__main__":
    exec("from v" + version_str + ".KUKA_KRC2_CamRob_SingleFile import test_post")
    test_post()

