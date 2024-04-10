# -*- coding: UTF-8 -*-
# Copyright 2015-2023 - RoboDK Inc. - https://robodk.com/
#
# This is a compiled post processor. Please contact us at info@robodk.com if you need access to the source code of this post processor.
#
# This file loads the compiled version of the RoboDK post processor for:
#   Techman robot controllers
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
exec("from v" + version_str + ".Techman import RobotPost as BasePost")

class RobotPost(BasePost):

    # ------------------------ Customize your RoboDK post processor using the following variables ------------------------

    # Maximum number of lines per program. If the number of lines is exceeded, the program will be executed step by step by RoboDK
    MAX_LINES_X_PROG = 1000000000.0    # 5000

    # Show zip file on program generation
    SHOW_PROGRAM_ZIP = True

    # Show text file on program generation
    SHOW_PROGRAM_TXT = True

    # Set to True to skip comments
    SKIP_COMMENTS = False

    # Include subprograms in the same program
    INCLUDE_SUBPROGS = True

    # Use the robot base or a reference frame
    USE_ROBOT_BASE = False

    # Use targets as offsets
    USE_TARGET_OFFSETS = False

    # Number of instructions to stack vertically before creating a new column
    VERTICAL_INS = 8

    # Set the maximum speed in DEG/s (percentage speed will be calculated accordingly)
    MAX_SPEED_DEGS = 1000

    # Set the maximum speed in MM/s (percentage speed will be calculated accordingly)
    MAX_SPEED_MMS = 1200

    # Set default payload for the robot movements
    OBJECT_PAYLOAD = 2

    # Set default rounding (radius in mm), set to -1 for accurate movements (point to point)
    ROUNDING_MM = 1

    # Set the default password (5 chars minimum)
    # Warning: if set to None, the password will match the program name (filled with numbers to reach a minimum of 8 characters)
    # Warning: if the password is changed, TMFlow may not accept it and ask for a new password
    SET_PASSWORD = "robodk1234"

    # Set to true to ask the user for a password
    ASK_PASSWORD = False

    # Set to 0 to not save a ZIP file
    # Set to 1 to save a zip file using TMExportZip
    # Set to 2 to save a zip file without using TMExportZip
    # ZIP_TYPE = 0
    ZIP_TYPE = 1

    # --------------------------------------------------------------------------------------------------------------------

    pass

if __name__== "__main__":
    exec("from v" + version_str + ".Techman import test_post")
    test_post()

