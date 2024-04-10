# -*- coding: UTF-8 -*-
# Copyright 2015-2023 - RoboDK Inc. - https://robodk.com/
#
# This is a compiled post processor. Please contact us at info@robodk.com if you need access to the source code of this post processor.
#
# This file loads the compiled version of the RoboDK post processor for:
#   KUKA KRC4 DAT robot controllers
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
exec("from v" + version_str + ".KUKA_KRC4_DAT import RobotPost as BasePost")

class RobotPost(BasePost):

    # ------------------------ Customize your RoboDK post processor using the following variables ------------------------

    PROG_EXT = "src"    # set the program extension

    # Use the Frame index instead of the pose when the index is provided
    # Example: Set to True and rename your reference to "Frame 2" to use BASE_DATA[2])
    BASE_INDEX = False

    # Use the Tool index instead of the pose when the index is provided
    # Example: Set to True and rename your tool to "Tool 3" to use TOOL_DATA[3])
    TOOL_INDEX = False

    # Default BASE ID to use when the base index is not specified in the reference name and BASE_INDEX is set to True
    DEFAULT_BASE_ID = 1

    # Default TOOL ID to use when the tool index is not specified in the reference name and TOOL_INDEX is set to True
    DEFAULT_TOOL_ID = 1

    # --------------------------------------------------------------------------------------------------------------------

    pass

if __name__== "__main__":
    exec("from v" + version_str + ".KUKA_KRC4_DAT import test_post")
    test_post()

