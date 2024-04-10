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
# in generic CSV format
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
# The CSV post processor generates simple CSV-formatted files for generic robotic and automation controllers.
# This post processor is versatile and can be used in applications requiring straightforward data import and export.
#
#
# Supported Controllers
# 
# ----------------------------------------------------

# ----------------------------------------------------
# Import RoboDK tools
from robodk import *

# ----------------------------------------------------
def pose_2_str(pose, joints = None):
    """Prints a pose target"""
    if pose is None:
        return ",,,,,"
    [x,y,z,r,p,w] = Pose_2_Staubli(pose)        
    str_xyzwpr = '%.3f,%.3f,%.3f,%.3f,%.3f,%.3f' % (x,y,z,r,p,w)
    return str_xyzwpr
    
def joints_2_str(joints):
    """Prints a joint target"""
    if joints is None:
        return ""
        
    str = ''
    for i in range(len(joints)):
        str = str + ('%.6f,' % (joints[i]))
    str = str[:-1]
    return str

# ----------------------------------------------------    
# Object class that handles the robot instructions/syntax
class RobotPost(object):

    PROG_EXT = 'csv'        # set the program extension
    
    # ----------------------------------------------------    

    
    # other variables
    ROBOT_POST = ''
    ROBOT_NAME = ''
    PROG_FILES = []
    
    SPEED_MMS = 100
    PROG = []
    LOG = ''
    nAxes = 6
    REF_FRAME = eye(4)
    
    # The _TargetName variable is automatically set by RoboDK before each call to MoveL or MoveJ if a named targett exists in RoboDK
    # If a target does not exist, this variable is set to None
    # Important: To enable this feature you must select Tools-Options-Program-Export target names
    _TargetName = None

    
    def __init__(self, robotpost=None, robotname=None, robot_axes = 6, **kwargs):
        self.ROBOT_POST = robotpost
        self.ROBOT_NAME = robotname
        self.PROG = []
        self.LOG = ''
        self.nAxes = robot_axes
        for k,v in kwargs.items():
            if k == 'lines_x_prog':
                self.MAX_LINES_X_PROG = v       
        
    def ProgStart(self, progname):
        str_axes = ''
        for i in range(self.nAxes):
            str_axes += ',J%i (deg)' % (i+1)
        self.addline('Instruction,X (mm),Y (mm),Z (mm),Rx (deg),Ry (deg),Rz (deg)' + str_axes)
        self.addline('Program Start,' + progname)
        
    def ProgFinish(self, progname):
        self.addline('Program Finish,' + progname)
        
    def ProgSave(self, folder, progname, ask_user=False, show_result=False):
        progname = progname + '.' + self.PROG_EXT
        if ask_user or not DirExists(folder):
            filesave = getSaveFile(folder, progname, 'Save program as...')
            if filesave is not None:
                filesave = filesave.name
            else:
                return
        else:
            filesave = folder + '/' + progname
        fid = open(filesave, "w")
        for line in self.PROG:
            fid.write(line + '\n')
        fid.close()
        print('SAVED: %s\n' % filesave)
        self.PROG_FILES = filesave
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
            
            if len(self.LOG) > 0:
                mbox('Program generation LOG:\n\n' + self.LOG)
    
    def ProgSendRobot(self, robot_ip, remote_path, ftp_user, ftp_pass):
        """Send a program to the robot using the provided parameters. This method is executed right after ProgSave if we selected the option "Send Program to Robot".
        The connection parameters must be provided in the robot connection menu of RoboDK"""
        UploadFTP(self.PROG_FILES, robot_ip, remote_path, ftp_user, ftp_pass)
        
    def MoveJ(self, pose, joints, conf_RLF=None):
        """Add a joint movement"""
        tname = ""
        if self._TargetName is not None:
            # Enable exporting target names in: Tools-Options-Program-Export Target Names
            tname = "," + self._TargetName
            
        self.addline('Move Joints,%s,%s%s' % (pose_2_str(pose), joints_2_str(joints), tname))
        
    def MoveL(self, pose, joints, conf_RLF=None):
        """Add a linear movement"""
        tname = ""
        if self._TargetName is not None:
            # Enable exporting target names in: Tools-Options-Program-Export Target Names
            tname = "," + self._TargetName
            
        self.addline('Move Linear,%s,%s%s' % (pose_2_str(pose), joints_2_str(joints), tname))
        
    def MoveC(self, pose1, joints1, pose2, joints2, conf_RLF_1=None, conf_RLF_2=None):
        """Add a circular movement"""    
        tname1 = ""
        tname2 = ""
        if self._TargetName is not None:
            # Enable exporting target names in: Tools-Options-Program-Export Target Names
            if self._TargetName[0] is not None:
                tname1 = "," + self._TargetName[0]
            if self._TargetName[1] is not None:
                tname2 = "," + self._TargetName[1]
            
        self.addline('Move Circular (1),%s,%s%s' % (pose_2_str(pose1), joints_2_str(joints1),tname1))
        self.addline('Move Circular (2),%s,%s%s' % (pose_2_str(pose2), joints_2_str(joints2),tname2))
        
    def setFrame(self, pose, frame_id=None, frame_name=None):
        """Change the robot reference frame"""
        self.REF_FRAME = pose
        self.addline('Set Reference,' + pose_2_str(pose))
        
    def setTool(self, pose, tool_id=None, tool_name=None):
        """Change the robot TCP"""
        self.addline('Set Tool,' + pose_2_str(pose))
        
    def Pause(self, time_ms):
        """Pause the robot program"""
        if time_ms < 0:
            self.addline('Stop')
        else:
            self.addline('Pause (ms),%.3f' % time_ms)
    
    def setSpeed(self, speed_mms):
        """Changes the robot speed (in mm/s)"""
        self.addline('Set Speed (mm/s),%.3f' % speed_mms)
        #self.addline('F%.3f' % (speed_mms*60))
    
    def setAcceleration(self, accel_mmss):
        """Changes the robot acceleration (in mm/s2)"""
        self.addline('Set Acceleration (mm/s2),%.3f' % accel_mmss)
    
    def setSpeedJoints(self, speed_degs):
        """Changes the robot joint speed (in deg/s)"""
        self.addline('Set Joint Speed (deg/s),%.3f' % speed_degs)
    
    def setAccelerationJoints(self, accel_degss):
        """Changes the robot joint acceleration (in deg/s2)"""
        self.addline('Set Joint Acceleration (deg/s2),%.3f' % accel_degss)
        
    def setZoneData(self, zone_mm):
        """Changes the rounding radius (aka CNT, APO or zone data) to make the movement smoother"""
        self.addline('Set Rounding,%.3f' % zone_mm)

    def setDO(self, io_var, io_value):
        """Sets a variable (digital output) to a given value"""
        if type(io_var) != str:  # set default variable name if io_var is a number
            io_var = 'OUT[%s]' % str(io_var)
        if type(io_value) != str: # set default variable value if io_value is a number
            if io_value > 0:
                io_value = '1'
            else:
                io_value = '0'

        # at this point, io_var and io_value must be string values
        self.addline('Set DO,%s,%s' % (io_var, io_value))

    def setAO(self, io_var, io_value):
        """Set an Analog Output"""
        self.setDO(io_var, io_value)
        
    def waitDI(self, io_var, io_value, timeout_ms=-1):
        """Waits for a variable (digital input) io_var to attain a given value io_value. Optionally, a timeout can be provided."""
        if type(io_var) != str:  # set default variable name if io_var is a number
            io_var = 'IN[%s]' % str(io_var)
        if type(io_value) != str: # set default variable value if io_value is a number
            if io_value > 0:
                io_value = '1'
            else:
                io_value = '0'

        # at this point, io_var and io_value must be string values
        if timeout_ms < 0:
            self.addline('Wait DI,%s,%s' % (io_var, io_value))
        else:
            self.addline('Wait DI,%s,%s,%.1f' % (io_var, io_value, timeout_ms))
        
    def RunCode(self, code, is_function_call = False):
        """Adds code or a function call"""
        if is_function_call:
            code = code.replace(' ','_')
            self.addline("Run Program," + code)
        else:
            self.addline(code)
        
    def RunMessage(self, message, iscomment = False):
        """Display a message in the robot controller screen (teach pendant)"""
        if iscomment:
            self.addline('Comment,' + message)
        else:
            self.addline('Show Message,%s' % message)
        
# ------------------ private ----------------------                
    def addline(self, newline):
        """Add a program line"""
        self.PROG.append(newline)
        
    def addlog(self, newline):
        """Add a log message"""
        self.LOG = self.LOG + newline + '\n'

# -------------------------------------------------
# ------------ For testing purposes ---------------   
def Pose(xyzrpw):
    [x,y,z,r,p,w] = xyzrpw
    a = r*math.pi/180
    b = p*math.pi/180
    c = w*math.pi/180
    ca = math.cos(a)
    sa = math.sin(a)
    cb = math.cos(b)
    sb = math.sin(b)
    cc = math.cos(c)
    sc = math.sin(c)
    return Mat([[cb*ca, ca*sc*sb - cc*sa, sc*sa + cc*ca*sb, x],[cb*sa, cc*ca + sc*sb*sa, cc*sb*sa - ca*sc, y],[-sb, cb*sc, cc*cb, z],[0,0,0,1]])

def test_post():
    """Test the post with a basic program"""

    robot = RobotPost()

    robot.ProgStart("Program")
    robot.RunMessage("Program generated by RoboDK using a custom post processor", True)
    robot.setFrame(Pose([807.766544, -963.699898, 41.478944, 0, 0, 0]))
    robot.setTool(Pose([62.5, -108.253175, 100, -60, 90, 0]))
    robot.MoveJ(Pose([200, 200, 500, 180, 0, 180]), [-46.18419, -6.77518, -20.54925, 71.38674, 49.58727, -302.54752] )
    robot.MoveL(Pose([200, 250, 348.734575, 180, 0, -150]), [-41.62707, -8.89064, -30.01809, 60.62329, 49.66749, -258.98418] )
    robot.MoveL(Pose([200, 200, 262.132034, 180, 0, -150]), [-43.73892, -3.91728, -35.77935, 58.57566, 54.11615, -253.81122] )
    robot.RunMessage("Setting air valve 1 on")
    robot.RunCode("TCP_On", True)
    robot.Pause(1000)
    robot.MoveL(Pose([200, 250, 348.734575, 180, 0, -150]), [-41.62707, -8.89064, -30.01809, 60.62329, 49.66749, -258.98418] )
    robot.MoveL(Pose([250, 300, 278.023897, 180, 0, -150]), [-37.52588, -6.32628, -34.59693, 53.52525, 49.24426, -251.44677] )
    robot.MoveL(Pose([250, 250, 191.421356, 180, 0, -150]), [-39.75778, -1.04537, -40.37883, 52.09118, 54.15317, -246.94403] )
    robot.RunMessage("Setting air valve off")
    robot.RunCode("TCP_Off", True)
    robot.Pause(1000)
    robot.MoveL(Pose([250, 300, 278.023897, 180, 0, -150]), [-37.52588, -6.32628, -34.59693, 53.52525, 49.24426, -251.44677] )
    robot.MoveL(Pose([250, 200, 278.023897, 180, 0, -150]), [-41.85389, -1.95619, -34.89154, 57.43912, 52.34162, -253.73403] )
    robot.MoveL(Pose([250, 150, 191.421356, 180, 0, -150]), [-43.82111, 3.29703, -40.29493, 56.02402, 56.61169, -249.23532] )
    robot.MoveJ(None, [-46.18419, -6.77518, -20.54925, 71.38674, 49.58727, -302.54752] )
    robot.ProgFinish("Program")
    # robot.ProgSave(".","Program",True)
    for line in robot.PROG:
        print(line)
    if len(robot.LOG) > 0:
        mbox('Program generation LOG:\n\n' + robot.LOG)

    input("Press Enter to close...")

if __name__ == "__main__":
    """Function to call when the module is executed by itself: test"""
    test_post()
