# -*- coding: UTF-8 -*-
# Copyright 2015-2023 - RoboDK Inc. - https://robodk.com/
#
# This is a compiled post processor. Please contact us at info@robodk.com if you need access to the source code of this post processor.
#
# This file loads the compiled version of the RoboDK post processor for:
#   Universal Robots MoveP robot controllers
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
exec("from v" + version_str + ".Universal_Robots_MoveP import RobotPost as BasePost")

class RobotPost(BasePost):

    # ------------------------ Customize your RoboDK post processor using the following variables ------------------------

    # Include custom header to program.
    INCLUDE_HEADER = True

    # Set to True to use MoveP, set to False to use MoveL
    USE_MOVEP = True

    # Set to True to use the reference frame as a pose and pose_trans to premultiply all targets
    # Set to False to output all targets with respect to the robot base
    USE_RELATIVE_TARGETS = True

    # If True, it will attempt to upload using SFTP. It requires PYSFTP (pip install pysftp. Important: It requires Visual Studio Community C++ 10.0)
    UPLOAD_SFTP = False

    # Set True to automatically filter blending (CB3 or prior), set to False to leave it up to the controller to adjust the blending as needed
    # Leave this to default (None) to automatically detect the appropriate action
    BLENDING_CHECK = None

    # Force accurate move before we trigger program calls, speed changes or changing digital outputs
    MOVE_ACCURATE_CALLS = True

    # default speed for linear moves in m/s
    SPEED_MS = 0.25

    # default speed for joint moves in rad/s
    SPEED_RADS = 0.75

    # default acceleration for lineaer moves in m/ss
    ACCEL_MSS = 1.2

    # default acceleration for joint moves in rad/ss
    ACCEL_RADSS = 1.2

    # default blend radius in meters (corners smoothing)
    BLEND_RADIUS_M = 0.001

    # 5000    # Maximum number of lines per program. If the number of lines is exceeded, the program will be executed step by step by RoboDK
    MAX_LINES_X_PROG = 1000000000.0

    # minimum circle radius to output (in mm). It does not take into account the Blend radius
    MOVEC_MIN_RADIUS = 1

    # maximum circle radius to output (in mm). It does not take into account the Blend radius
    MOVEC_MAX_RADIUS = 10000

    # Maximum speeds and accelerations allowed by the controller (otherwise it throws a speed error)
    MAX_SPEED_MS = 3.0

    MAX_SPEED_DEGS = 180

    MAX_ACCEL_MSS = 15.0

    MAX_ACCEL_DEGSS = 2291.8

    # Set or change the main header
    HEADER = """
  #
  # TO REMOVE HEADER:
  # Go to "Program" -> "Post-Processor Editor"
  # Select "Universal Robots" 
  # Set "INCLUDE_HEADER" to "False"
  #
  #--------------------------
  # Add any default subprograms here
  # For example, to drive a gripper as a program call:
  # def Gripper_Open():
  #   ...
  # end
  #
  # Example to drive a spray gun:
  def SprayOn(value):
    # use the value as an output:
    DO_SPRAY = 5
    if value == 0:
      set_standard_digital_out(DO_SPRAY, False)
    else:
      set_standard_digital_out(DO_SPRAY, True)
    end
  end

  # Example to drive an extruder:
  def Extruder(value):
    # use the value as an output:
    if value < 0:
      # stop extruder
    else:
      # start extruder
    end
  end
  
  # Example to move an external axis
  def MoveAxis(value):
    # use the value as an output:
    DO_AXIS_1 = 1
    DI_AXIS_1 = 1
    if value <= 0:
      set_standard_digital_out(DO_AXIS_1, False)
      
      # Wait for digital input to change state
      #while (get_standard_digital_in(DI_AXIS_1) != False):
      #  sync()
      #end
    else:
      set_standard_digital_out(DO_AXIS_1, True)
      
      # Wait for digital input to change state
      #while (get_standard_digital_in(DI_AXIS_1) != True):
      #  sync()
      #end
    end
  end
  #--------------------------
"""

    # --------------------------------------------------------------------------------------------------------------------

    pass

if __name__== "__main__":
    exec("from v" + version_str + ".Universal_Robots_MoveP import test_post")
    test_post()

