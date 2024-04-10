# -*- coding: UTF-8 -*-
# Copyright 2015-2023 - RoboDK Inc. - https://robodk.com/
#
# This is a compiled post processor. Please contact us at info@robodk.com if you need access to the source code of this post processor.
#
# This file loads the compiled version of the RoboDK post processor for:
#   Epson RC robot controllers
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
exec("from v" + version_str + ".Epson_RC import RobotPost as BasePost")

class RobotPost(BasePost):

    # ------------------------ Customize your RoboDK post processor using the following variables ------------------------

    # Set the program file extension
    # PROG_EXT = 'gpl'
    PROG_EXT = "prg"

    # Set to True to use "Local " coordinate systems
    # Set to False to not use any Local coordinate systems, the targets will be exported with respect to the base
    USE_FRAMES = True

    # Set to True to add the configuration flag /L /R to the Cartesian movements
    # This applies to Scara robots only
    ADD_MOVEL_CONFIG = True

    # Set to true to force exporting joint moves using Cartesian coordinates instead of joint values
    FORCE_MOVEJCARTESIAN = False

    # Set the default local id to use
    # Example, RoboDK will output "Local 1" if default local id is 1
    # However, if you have a number in your reference frame (for example, "Frame 2"), the ID of the reference will be used instead
    DEFAULT_LOCAL_ID = 1

    # Set the default TLSet id to use
    # Example, RoboDK will output "TLSet 1" if default tool id is 1
    # However, if you have a number in your reference frame (for example, "Tool 3"), the ID of the reference will be used instead
    DEFAULT_TOOL_ID = 1

    # --------------------------------------------------------------------------------------------------------------------

    pass

if __name__== "__main__":
    exec("from v" + version_str + ".Epson_RC import test_post")
    test_post()

