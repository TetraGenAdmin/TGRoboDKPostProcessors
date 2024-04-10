# Copyright 2015 - RoboDK Inc. - https://robodk.com/
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
# The RoboDK Quine post processors outputs the intermediary (generic) code to be parsed by the post processor.
# This code is usually found in %TEMP%.
#
# Supported Controllers
#
# ----------------------------------------------------

# Import RoboDK tools
from robodk.robomath import *
from robodk.robodialogs import *
from robodk.robofileio import *

import inspect
from pathlib import Path
import shutil


def get_caller_filepath():
    # Get the first file in the stack that is not this file
    file_path = Path(__file__).absolute()
    caller_path = None
    for s in inspect.stack():
        caller_path = Path(s.filename)
        if caller_path != file_path:
            break
    return caller_path


# ----------------------------------------------------
# Object class that handles the robot instructions/syntax
class RobotPost(object):

    # ----------------------------------------------------
    PROG_EXT = 'py'

    def __init__(self, *args, **kwargs):
        self.caller_filepath = get_caller_filepath()

    def ProgStart(self, *args, **kwargs):
        pass

    def ProgFinish(self, *args, **kwargs):
        pass

    def ProgSave(self, folder, progname, ask_user=False, show_result=False, *args, **kwargs):
        progname = progname + self.caller_filepath.suffix
        if ask_user or not DirExists(folder):
            filesave = getSaveFile(folder, progname, 'Save program as...')
            if filesave is not None:
                filesave = filesave.name
            else:
                return
        else:
            filesave = folder + '/' + progname

        shutil.copyfile(self.caller_filepath.as_posix(), filesave)
        print('SAVED: %s\n' % filesave)

        #---------------------- show result
        if show_result:
            if type(show_result) is str:
                # Open file with provided application
                import subprocess
                p = subprocess.Popen([show_result, filesave])
            elif type(show_result) is list:
                import subprocess
                p = subprocess.Popen(show_result + [filesave])
            else:
                # open file with default application
                import os
                os.startfile(filesave)

    def ProgSendRobot(self, *args, **kwargs):
        pass

    def MoveJ(self, *args, **kwargs):
        pass

    def MoveL(self, *args, **kwargs):
        pass

    def MoveC(self, *args, **kwargs):
        pass

    def setFrame(self, *args, **kwargs):
        pass

    def setTool(self, *args, **kwargs):
        pass

    def Pause(self, *args, **kwargs):
        pass

    def setSpeed(self, *args, **kwargs):
        pass

    def setAcceleration(self, *args, **kwargs):
        pass

    def setSpeedJoints(self, *args, **kwargs):
        pass

    def setAccelerationJoints(self, *args, **kwargs):
        pass

    def setZoneData(self, *args, **kwargs):
        pass

    def setDO(self, *args, **kwargs):
        pass

    def setAO(self, *args, **kwargs):
        pass

    def waitDI(self, *args, **kwargs):
        pass

    def RunCode(self, *args, **kwargs):
        pass

    def RunMessage(self, *args, **kwargs):
        pass


def test_post():
    pass


if __name__ == "__main__":
    test_post()
