# Copyright 2015-2022 - RoboDK Inc. - https://robodk.com/
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ----------------------------------------------------
# This file is a POST PROCESSOR for Robot Offline Programming to generate programs 
# for a KUKA KRC4 robot controller with RoboDK
#
# To edit/test this POST PROCESSOR script file:
# Select "Program"->"Add/Edit Post Processor", then select your post or create a new one.
# You can edit this file using any text editor or Python editor. Using a Python editor allows to quickly evaluate a sample program at the end of this file.
# Python should be automatically installed with RoboDK
#
# You can also edit the POST PROCESSOR manually:
#    1- Open the *.py file with Python IDLE (right click -> Edit with IDLE)
#    2- Make the necessary changes
#    3- Run the file to open Python Shell: Run -> Run module (F5 by default)
#    4- The "test_post()" function is called automatically
# Alternatively, you can edit this file using a text editor and run it with Python
#
# To use a POST PROCESSOR file you must place the *.py file in "C:/RoboDK/Posts/"
# To select one POST PROCESSOR for your robot in RoboDK you must follow these steps:
#    1- Open the robot panel (double click a robot)
#    2- Select "Parameters"
#    3- Select "Unlock advanced options"
#    4- Select your post as the file name in the "Robot brand" box
#
# To delete an existing POST PROCESSOR script, simply delete this file (.py file)
#
# ----------------------------------------------------
# More information about RoboDK Post Processors and Offline Programming here:
#     https://robodk.com/help#PostProcessor
#     https://robodk.com/doc/en/PythonAPI/postprocessor.html
# ----------------------------------------------------

# ----------------------------------------------------
# Description
# The KUKA KRC4 post processor allows you to generate code for KUKA KRC4 controllers. 
# You can easily configure the KRC Version variable to generate code for KRC 2 controllers only.
#
# This post processor inlines the target coordinates inside the linear movements. 
# You can use the KUKA KRC4 DAT version instead to save the targets in a data file instead.

# ----------------------------------------------------
# Import RoboDK tools
from robodk import *

from KUKA_KRC2 import RobotPost as BasePost


# ----------------------------------------------------    
# Object class that handles the robot instructions/syntax

class RobotPost(BasePost):
    # Maximum number of lines per program. It will then generate multiple "pages (files)" if the program is too long
    # This is the default value. You can change this value in RoboDK:
    # Tools-Options-Program-Limit the maximum number of lines per program
    MAX_LINES_X_PROG = 25000

    # Set to True to include subprograms in the main program. Otherwise, programs can be generated separately.
    INCLUDE_SUB_PROGRAMS = True

    # Generate subprograms as new files instead of adding them in the same file (INCLUDE_SUB_PROGRAMS must be set to True)
    SUB_PROGRAMS_AS_FILES = False

    # Set KRC Version (2 or 4)
    # Version 2 for KRC2 controllers or Version 4 for KRC4
    # KRC_VERSION = 2  for KRC2 controllers
    KRC_VERSION = 4

    # Display messages on the teach pendant. This feature is not supported by all controllers and must be disabled for some controllers.
    # SKIP_MESSAGE_POPUPS = True
    SKIP_MESSAGE_POPUPS = False

    # Use the Frame index instead of the pose when the index is provided
    # Example: Set to True and rename your reference to "Frame 2" to use BASE_DATA[2])
    FRAME_INDEX = False

    # Use the Tool index instead of the pose when the index is provided
    # Example: Set to True and rename your tool to "Tool 3" to use TOOL_DATA[3])
    TOOL_INDEX = False

    # Define the move linear keyword (usually LIN)
    # Other examples: SLIN, SPL (use a Spline Block, ...
    # Tip: Add a comment such as start_spl, start_lin or start_slin to change the move command
    LIN_KEYWORD = "LIN"

    # Use SPLINE block (SPL movements). You can change this flag or change the LIN KEYWORD to SPL.
    SPLINE_BLOCK = False

    # Set if we want to have cascaded program calls when program splitting takes place
    # Usually, cascaded is better for older controllers
    # CASCADED_CALLS = True
    # CASCADED_CALLS = False
    CASCADED_CALLS = (KRC_VERSION <= 2)

    # Optionally output configuration and turn flags S and T
    # If we set this to true, the output targets will have the configuration and turn bits added in the movement
    # (for example: S B'010', T B'000001')
    ADD_CONFIG_TURN = False

    # Add a keyword to split subprograms
    # SKIP_PROG_KEYWORD = 'spindle'
    SKIP_PROG_KEYWORD = None

    # Set the name/order of default axes and external axes
    AXES_DATA = ['A1','A2','A3','A4','A5','A6','E1','E2','E3','E4','E5','E6']

    # Program name max length (KRC4 is 24 characters)
    PROG_NAME_LEN = 16

    # Parameters for 3D printing
    # Use a synchronized external axis as an extruder (E1, E2, ... or the last available axis)
    # EXTAXIS_EXTRUDER = False
    EXTAXIS_EXTRUDER = True

    # Use a weld gun as an extruder
    # WELD_EXTRUDER = True
    WELD_EXTRUDER = False

    # Parameters for 3D printing using a custom extruder
    # 3D Printing Extruder Setup Parameters:
    PRINT_E_ANOUT = 5

    PRINT_SPEED_2_SIGNAL = 0.10

    PRINT_FLOW_MAX_SIGNAL = 24

    PRINT_ACCEL_MMSS = -1

