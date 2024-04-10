# -*- coding: UTF-8 -*-
# Copyright 2015-2023 - RoboDK Inc. - https://robodk.com/
#
# This is a compiled post processor. Please contact us at info@robodk.com if you need access to the source code of this post processor.
#
# This file loads the compiled version of the RoboDK post processor for:
#   Comau C5G robot controllers
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
exec("from v" + version_str + ".Comau_C5G import RobotPost as BasePost")

class RobotPost(BasePost):

    # ------------------------ Customize your RoboDK post processor using the following variables ------------------------

    # Maximum number of lines per program. If exceeded, it will then generate multiple "pages (files)"
    # This is the default setting and it can be changed in Tools-Options-Program
    MAX_LINES_X_PROG = 5000

    # Include subprograms in the main program (same file)
    INCLUDE_SUB_PROGRAMS = True

    # Default fly dist (rounding). Set to >0 to use MOVEFLY
    FLY_DIST = -1

    # Set EXT_POSEXT to define external axes as POSEXT variables (inlined)
    # If set to False, it will use XTNDPOS instead
    EXT_POSEXT = True

    # Program extension
    PROG_EXT = "pdl"

    # --------------------------------------------------------------------------------------------------------------------

    pass

if __name__== "__main__":
    exec("from v" + version_str + ".Comau_C5G import test_post")
    test_post()

