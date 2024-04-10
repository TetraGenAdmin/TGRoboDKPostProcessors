# -*- coding: UTF-8 -*-
# Copyright 2015-2023 - RoboDK Inc. - https://robodk.com/
#
# This is a compiled post processor. Please contact us at info@robodk.com if you need access to the source code of this post processor.
#
# This file loads the compiled version of the RoboDK post processor for:
#   Elite Robots CS TASK Frame robot controllers
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
exec("from v" + version_str + ".Elite_Robots_CS_TASK_Frame import RobotPost as BasePost")

class RobotPost(BasePost):

    # ------------------------ Customize your RoboDK post processor using the following variables ------------------------

    # Set the default maximum number of lines per program.
    # It will then generate multiple "pages (files)". This can be overriden by RoboDK settings.
    MAX_LINES_X_PROG = 2000

    # Specify the default UTool Id to use (register).
    # You can also use Numbered tools in RoboDK (for example, a tool named "Tool 2" will use UTOOL number 2)
    ACTIVE_TOOL = 9

    # Generate sub programs with each program
    INCLUDE_SUB_PROGRAMS = True

    # Specify a spare Position register for calculations (Tool, Reference, ...)
    SPARE_PR = 95

    # Set to True to use MFRAME for setting reference frames automatically within the program
    USE_MFRAME = False

    # Specify the default UFrame Id to use (register).
    # You can also use Numbered References in RoboDK (for example, a reference named "Reference 4" will use UFRAME number 4)
    ACTIVE_FRAME = 9

    # --------------------------------------------------------------------------------------------------------------------

    pass

if __name__== "__main__":
    exec("from v" + version_str + ".Elite_Robots_CS_TASK_Frame import test_post")
    test_post()

