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
# for Automata EVA robot
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
# The Automata post processor generates Python code compatible with Automata robotic controllers.
#
#
# Supported Controllers
# Automata EVA
# ----------------------------------------------------

from robodk import *      # Robot toolbox

def pose_2_str(pose, joints = None):
    """Prints a pose target"""
    if pose is None:
        pose = eye(4)
    x,y,z,rx,ry,rz = pose.Pose_2_TxyzRxyz()
    str_xyzwpr = 'Pose(%.3f, %.3f, %.3f,  %.3f, %.3f, %.3f)' % (x,y,z,rx*180/pi,ry*180/pi,rz*180/pi)
    return str_xyzwpr

def mat_2_str(mat):
    if mat is None:
        raise Exception('Matrix is empty!')
    returnString = str(mat).split(":\n")[0].strip('(').strip(')').strip('Pose(')
    return returnString

def joints_2_str(joints):
    """Prints a joint target"""
    if joints is None:
        return ""
        
    str = ''
    for i in range(len(joints)):
        str = str + ('%.6f,' % (joints[i]))
    str = str[:-1]
    return str

# Parent: make sure the parent matches
def PoseDistance(pose1, pose2):
    """0.000001"""
    distance_mm = distance(pose1.Pos(), pose2.Pos())
    distance_deg = pose_angle_between(pose1, pose2) * 180 / pi
    return distance_mm + distance_deg



# ----------- communication class for eva robots -------------
# This class handles communication between this driver (PC) and the robot
class ComRobot:
    """Robot class for programming eva robots"""
    LAST_MSG = None  # Keep a copy of the last message received
    CONNECTED = False  # Connection status is known at all times
    #Eva robot variables
    eva = None
    curToolPose = [0,0,0,0,0,0]
    curRounding = -1

    BUFFER_SIZE = None
    TIMEOUT = None
    #Speed and accelerations
    LINEARSPEED = 100
    LINEARACELL = 30
    JOINTSPEED  = 100
    JOINTACELL  = 80
    LAST_TARGET_JOINTS = []



    # This is executed when the object is created
    def __init__(self):
        self.BUFFER_SIZE = 512  # bytes
        self.TIMEOUT = 5 * 60  # seconds: it must be enough time for a movement to complete
        # self.TIMEOUT = 10 # seconds

        # destructor

    def __del__(self):
        self.disconnect()

    # Disconnect from robot
    def disconnect(self):
        self.CONNECTED = False
        if self.eva:
            try:
                self.eva.unlock()
                self.eva = None
            except Exception as e:
                return False
        return True

    # Connect to robot
    def connect(self, ip, port=-1):
        global ROBOT_MOVING
        self.disconnect()
        print_message('Connecting to robot %s' % (ip))
        # Create new socket connection
        UpdateStatus(ROBOTCOM_WORKING)
        try:
            self.eva = Eva(ip, port)
            with self.eva.lock():
                self.eva.control_wait_for_ready()
                self.eva.control_reset_errors()
        except Exception as e:
            print_message(str(e))
            return False

        with self.eva.lock():
            version = self.eva.versions()[0]
            robotName = self.eva.name()
        print_message("API Version:" + str(version))
        print_message("Robot Name:" + str(robotName))

        self.CONNECTED = True
        ROBOT_MOVING = False

        sys.stdout.flush()
        return True

    def recv_acknowledge(self):
        import time
        with self.eva.lock():
            #loop structure taken from lower level api because the functionality needed is not exposed
            while True:
                robot_state = self.eva.data_snapshot()['control']['state']

                if robot_state == 'error':
                    print_message('Error moving robot')
                    return False
                elif robot_state == 'ready':
                    break
                curJoints = self.eva.data_servo_positions()
                print_joints(curJoints,True)
                time.sleep(0.1)
        return True

    def MoveJ(self,joints):
        try:
            jointList = joints[:nDOFs_MIN]
            with self.eva.lock():
                self.eva.control_go_to(jointList)
        except Exception as e:
            print_message(str(e))
            return False
        return True

    def MoveL(self,joints):
        global nDOFs_MIN
        #Do some trickery where you get the current position and tool and position and generate a path with 2 points
        xyzwpr = joints[nDOFs_MIN:]
        try:
            raise Exception('Not yet implemented')
        except Exception as e:
            print_message(str(e))
            return False
        #return True
    
    def MoveC(self,joints):
        try:
            raise Exception('Not yet implemented')
        except Exception as e:
            print_message(str(e))
            return False
        #return True

    def getJoints(self):
        with self.eva.lock():
            jointPosition = self.eva.data_servo_positions()
        return jointPosition

    def setSpeed(self, speed_values):
        if (speed_values[0] != -1):
            self.LINEARSPEED = speed_values[0]

        if (speed_values[1] != -1):
            self.JOINTSPEED = speed_values[1]

        if (speed_values[2] != -1):
            self.LINEARACELL = speed_values[2]

        if (speed_values[3] != -1):
            self.JOINTACELL = speed_values[3]

        return True

    def setTool(self,tool_pose):
        self.curToolPose = tool_pose
        return True

    def Pause(self,timeMS):
        import time
        time.sleep(timeMS/1000)
        return True

    def setRounding(self,rounding):
        self.curRounding = rounding
        return True

    def setDO(self,digital_IO_State):
        with self.eva.lock():
            self.eva.gpio_set(digital_IO_State[0],digital_IO_State[1])
        return True

    def WaitDI(self,digital_IO_Num):
        import time
        start = time.time()
        ioNumber = digital_IO_Num[0]
        desiredState = digital_IO_Num[1]
        try:
            timeout = digital_IO_Num[2]
        except Exception as e:
            e = e
            timeout = 0

        with self.eva.lock():
            ioState = self.eva.gpio_get(ioNumber,'input')

        while not (ioState == desiredState) and (time.time() - start) < timeout:
            with self.eva.lock():
                ioState = self.eva.gpio_get(ioNumber,'input')
            time.sleep(0.1)
        return True

    #def SendCmd(self, cmd, values=None):
    #    """Send a command. Returns True if success, False otherwise."""
    #    # print('SendCmd(cmd=' + str(cmd) + ', values=' + str(values) if values else '' + ')')
    #    # Skip the command if the robot is not connected
    #    if not self.CONNECTED:
    #        UpdateStatus(ROBOTCOM_NOT_CONNECTED)
    #        return False
    #
    #    if not self.send_int(cmd):
    #        print_message("Robot connection broken")
    #        UpdateStatus(ROBOTCOM_NOT_CONNECTED)
    #        return False
    #
    #    if values is None:
    #        return True
    #    elif not isinstance(values, list):
    #        values = [values]
    #
    #    if not self.send_array(values):
    #        print_message("Robot connection broken")
    #        UpdateStatus(ROBOTCOM_NOT_CONNECTED)
    #        return False
    #
    #    return True
        
      
TEMPLATE_CONNECT = """def ConnectRobot():
    # Connect to the robot
    global %s
    ROBOT_IP   = "%s"
    %s = ComRobot()
    while not %s.connect(ROBOT_IP):
        print_message("Retrying connection...")
        import time
        time.sleep(0.5)
            
    print_message("Connected to robot: " + ROBOT_IP)    
    
"""     


# ----------------------------------------------------    
# Object class that handles the robot instructions/syntax
class RobotPost(object):
    
    #Code generation mode
    # 1 = simulate
    # 2 = Online Programming (run on robot)
    # 3 = Macro generation (RDK.AddProgram)
    POST_CODEGEN_MODE = 3

    #Name of the main function, obtained from first instance of ProgStart being called
    MAIN_PROGRAM_NAME = None

    #----------------------------------------------------
    
    #Name of the current program being written, only for AddProgram (mode 3)
    #Defaults to robot for api usage (mode 1 and 2)
    CURRENT_PROGRAM_NAME = ('robot' if POST_CODEGEN_MODE != 3 else 'program')
    
    #Unique Target Couter
    TARGET_COUNT = 0

    # other variables
    PROG_EXT = 'py'        # set the program extension
    ROBOT_POST = ''
    ROBOT_NAME = ''
    PROG_FILES = []
    
    PROG = []
    LOG = ''
    nAxes = 6
    REF_FRAME = eye(4)

    #Need to make the robot object here
    def __init__(self, robotpost=None, robotname=None, robot_axes = 6, ip_com=r"""127.0.0.1""", **kwargs):
        self.ROBOT_POST = robotpost
        #self.ROBOT_NAME = FilterName(robotname).replace('.', '')
        self.ROBOT_NAME = 'robot'
        self.PROG = []
        self.LOG = ''
        self.nAxes = robot_axes

        self.addline('# Program automatically generated by RoboDK using the post processor for Automata EVA robots')
        self.addline('# Run this file with Python to run the program on the robot')
        self.addline('# ')
        self.addline('# Make sure the evasdk Python library is installed or available in the path')
        self.addline('import sys')
        self.addline('from robolink import import_install')
        self.addline('import_install("evasdk")') #installs websockets, zeroconf, requests
        #self.addline('sys.path.insert(0,\"%s\")' % (os.path.normpath(os.path.dirname(__file__)+"\..\Python").replace("\\","/")))
        self.addline('# Import the EVA SDK Python library')
        self.addline('from evasdk import Eva')
        self.addline('import json')
        self.addline('')
        self.addline('')
        self.addline('def print_message(arg):')
        self.addline('    print(arg)')
        self.addline('')
        self.addline('def UpdateStatus(arg):')
        self.addline('    pass')
        self.addline('')
        self.addline('ROBOTCOM_UNKNOWN = -1000')
        self.addline('ROBOTCOM_CONNECTION_PROBLEMS = -3')
        self.addline('ROBOTCOM_DISCONNECTED = -2')
        self.addline('ROBOTCOM_NOT_CONNECTED = -1')
        self.addline('ROBOTCOM_READY = 0')
        self.addline('ROBOTCOM_WORKING = 1')
        self.addline('ROBOTCOM_WAITING = 2')
        self.addline('nDOFs_MIN = %s' % robot_axes)
        self.addline('')
        self.addline('')
        
        try:
            import inspect
            ComRobotLines = inspect.getsourcelines(ComRobot)[0]
            for curLine in ComRobotLines:
                self.addline(curLine.rstrip())
        except Exception as e:
            self.addline("raise Exception('Source code not available to add ComRobot class. Contact us at info@robodk.com')")
    
        self.addline('')
        self.addline('')
        self.addline(TEMPLATE_CONNECT % (self.ROBOT_NAME, ip_com, self.ROBOT_NAME, self.ROBOT_NAME))
        self.addline('')

        for k,v in kwargs.items():
            if k == 'lines_x_prog':
                self.MAX_LINES_X_PROG = v       
        
    def ProgStart(self, progname):
        prognamesafe = FilterName(progname).replace('.', '')
        str_axes = ''
        for i in range(self.nAxes):
            str_axes += ',J%i (deg)' % (i+1)
        if self.MAIN_PROGRAM_NAME is None:
            self.MAIN_PROGRAM_NAME = prognamesafe
        self.addline('')    
        self.addline('# Program Start,' + prognamesafe)
        self.addline('def ' + prognamesafe + '():')
        self.addline('    global ' + FilterName(self.ROBOT_NAME).replace('.', ''))
        self.addline('    # Generating program: ' + prognamesafe)

        self.addline('')
            
        
    def ProgFinish(self, progname):
        self.addline('    return')
        
    def ProgSave(self, folder, progname, ask_user=False, show_result=False):
        if self.MAIN_PROGRAM_NAME is not None:
            self.addline('')
            self.addline('if __name__ == "__main__":')
            self.addline('    # Connect to the robot and run the program')            
            self.addline('    ConnectRobot()')            
            self.addline('    ' + self.MAIN_PROGRAM_NAME + '()')              

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
        #UploadFTP(self.PROG_FILES, robot_ip, remote_path, ftp_user, ftp_pass)
        import subprocess
        import sys
        
        print("POPUP: Running script file")
        sys.stdout.flush()
        
        #subprocess.call([sys.executable, filenameToOpen], shell = False)
        command = 'start "" "' + sys.executable + '" "' + self.PROG_FILES + '"'
        print("Running command: " + command)
        sys.stdout.flush()
        os.system(command)  
        
    def MoveJ(self, pose, joints, conf_RLF=None):
        """Add a joint movement"""
        self.addline('    %s.MoveJ([%s])' %  (self.ROBOT_NAME,joints_2_str(joints)) )

    def MoveL(self, pose, joints, conf_RLF=None):
        """Add a linear movement"""
        if pose is None:
            msg = "Linear movement using joint targets is not supported. Change the target type to cartesian or use a joint movement."
            self.addlog(msg)
            self.RunMessage(msg, True)
            return
        
        pose_abs = self.REF_FRAME * pose
        self.addline('    %s.MoveL([%s])' % (self.ROBOT_NAME, joints_2_str(joints) + ',' + mat_2_str(pose) ) )
        
    def MoveC(self, pose1, joints1, pose2, joints2, conf_RLF_1=None, conf_RLF_2=None):
        """Add a circular movement"""    
        if pose1 is None or pose2 is None:
            msg = "Circular movement using joint targets is not supported. Change the target type to cartesian or use a joint movement."
            self.addlog(msg)
            self.RunMessage(msg, True)
            return
        
        self.addline('    %s.MoveC([%s])' % (self.ROBOT_NAME,joints_2_str(joints1) + ',' + mat_2_str(pose1) + ',' + joints_2_str(joints2) + ',' + mat_2_str(pose2)) )        

    def setFrame(self, pose, frame_id=None, frame_name=None):
        """Change the robot reference frame"""
        self.REF_FRAME = pose
        varname = FilterName(frame_name).replace('.', '')
        self.addline('    #%s ref frame set to %s' % (self.ROBOT_NAME,mat_2_str(pose)) )        
        
    def setTool(self, pose, tool_id=None, tool_name=None):
        """Change the robot TCP"""
        self.addline('    %s.setTool([%s])' % (self.ROBOT_NAME,mat_2_str(pose) ) )
        self.addline('')


    def Pause(self, time_ms):
        """Pause the robot program"""
        if time_ms < 0:
            self.addline('    print(\'STOP\')')
        else:
            self.addline('    import time')
            self.addline('    time.sleep(%.3f)' % (time_ms*1000))
    
    def setSpeed(self, speed_mms):
        """Changes the robot speed (in mm/s)"""
        varname = FilterName(self.ROBOT_NAME).replace('.', '')
        self.addline('    %s.setSpeed([%s,-1,-1,-1])' % (FilterName(self.ROBOT_NAME).replace('.', ''),str(speed_mms)))

    def setAcceleration(self, accel_mmss):
        """Changes the robot acceleration (in mm/s2)"""
        varname = FilterName(self.ROBOT_NAME).replace('.', '')
        self.addline('    %s.setSpeed([-1,-1,%s,-1])' % (FilterName(self.ROBOT_NAME).replace('.', ''),str(accel_mmss)) )

    def setSpeedJoints(self, speed_degs):
        """Changes the robot joint speed (in deg/s)"""
        varname = FilterName(self.ROBOT_NAME).replace('.', '')
        self.addline('    %s.setSpeed([-1,%s,-1,-1])' % (FilterName(self.ROBOT_NAME).replace('.', ''),str(speed_degs)) )
    
    def setAccelerationJoints(self, accel_degss):
        """Changes the robot joint acceleration (in deg/s2)"""
        varname = FilterName(self.ROBOT_NAME).replace('.', '')
        self.addline('    %s.setSpeed([-1,-1,-1,%s])' % (FilterName(self.ROBOT_NAME).replace('.', ''),str(accel_degss)) )

    def setZoneData(self, zone_mm):
        """Changes the rounding radius (aka CNT, APO or zone data) to make the movement smoother"""
        self.addline('    %s.setRounding(%.3f)' % (FilterName(self.ROBOT_NAME).replace('.', ''),zone_mm) )

    def setDO(self, io_var, io_value):
        """Sets a variable (digital output) to a given value"""

        # at this point, io_var and io_value must be string values
        self.addline('    %s.setDO([%s,%s])' % (FilterName(self.ROBOT_NAME).replace('.', ''),io_var, io_value))

    def setAO(self, io_var, io_value):
        """Set an Analog Output"""
        self.setDO(io_var, io_value)
        
    def waitDI(self, io_var, io_value, timeout_ms=-1):
        """Waits for a variable (digital input) io_var to attain a given value io_value. Optionally, a timeout can be provided."""
        if timeout_ms > -1:
            timeout_ms = timeout_ms/1000
        self.addline('    %s.WaitDI([%s,%s,%s])' % (FilterName(self.ROBOT_NAME).replace('.', ''),io_var, io_value,timeout_ms))
        
    def RunCode(self, code, is_function_call = False):
        """Adds code or a function call"""
        if is_function_call:
            prognamesafe = FilterName(code).replace('.', '')
            code = code.replace(' ','_')
            self.addline("    " + prognamesafe + '()')
            #Add a call to this function in the main
            if self.POST_CODEGEN_MODE == 3:
                self.addline('    %s = RDK.Item(\'%s\',ITEM_TYPE_PROGRAM)' % (self.MAIN_PROGRAM_NAME,self.MAIN_PROGRAM_NAME))    
                self.addline('    %s.RunInstruction(\'%s\',INSTRUCTION_CALL_PROGRAM)' % (self.MAIN_PROGRAM_NAME,prognamesafe) )
        else:
            self.addline(code)
        
    def RunMessage(self, message, iscomment = False):
        """Display a message in the robot controller screen (teach pendant)"""
        if iscomment:
            self.addline('    #' + message)
        else:
            self.addline('    print(\'%s\')' % message)
        
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

    def p(xyzrpw):
        x,y,z,r,p,w = xyzrpw
        a = r*math.pi/180.0
        b = p*math.pi/180.0
        c = w*math.pi/180.0
        ca = math.cos(a)
        sa = math.sin(a)
        cb = math.cos(b)
        sb = math.sin(b)
        cc = math.cos(c)
        sc = math.sin(c)
        return Mat([[cb*ca,ca*sc*sb-cc*sa,sc*sa+cc*ca*sb,x],[cb*sa,cc*ca+sc*sb*sa,cc*sb*sa-ca*sc,y],[-sb,cb*sc,cc*cb,z],[0.0,0.0,0.0,1.0]])
        
    robot = RobotPost(r"""Quine""",r"""Automata EVA""",6, axes_type=['R','R','R','R','R','R'], 
    ip_com=r"""192.168.125.1""")

    robot.ProgStart(r"""Prog1""")
    robot.RunMessage(r"""Program generated by RoboDK v4.2.3 for ABB IRB 120-3/0.6 on 08/05/2020 15:54:54""", True)
    robot.RunMessage(r"""Using nominal kinematics.""", True)
    robot.setFrame(p([0.000000,0.000000,0.000000,0.000000,0.000000,0.000000]),-1,r"""ABB IRB 120-3/0.6 Base""")
    robot.setAccelerationJoints(800.000)
    robot.setFrame(p([0.000000,0.000000,0.000000,0.000000,0.000000,0.000000]),-1,r"""ABB IRB 120-3/0.6 Base""")
    robot.setAccelerationJoints(800.000)
    robot.setSpeedJoints(500.000)
    robot.setAcceleration(3000.000)
    robot.setSpeed(500.000)
    robot.MoveJ(p([374.000000,-0.000000,610.000000,-0.000000,90.000000,0.000000]),[-0.000000,-0.836761,4.599793,-0.000000,-3.763032,0.000000],[0.0,0.0,1.0])
    robot.MoveL(p([374.000000,174.400321,610.000000,0.000000,90.000000,0.000000]),[30.005768,9.246934,-6.136218,84.631745,-30.151638,-83.797873],[0.0,0.0,1.0])
    robot.MoveL(p([374.000000,-201.108593,610.000000,0.000000,90.000000,0.000000]),[-33.660539,12.400929,-9.814293,-86.122958,-33.748102,85.340395],[0.0,0.0,1.0])
    robot.MoveJ(p([374.000000,-0.000000,610.000000,-0.000000,90.000000,0.000000]),[-0.000000,-0.836761,4.599793,-0.000000,-3.763032,0.000000],[0.0,0.0,1.0])
    robot.setTool(p([0.000000,0.000000,200.000000,0.000000,0.000000,0.000000]),-1,r"""Paint gun""")
    robot.MoveC(p([374.000000,-0.000000,610.000000,-0.000000,90.000000,0.000000]),[-0.000000,-0.836761,4.599793,-0.000000,-3.763032,0.000000],p([374.000000,-201.108593,610.000000,0.000000,90.000000,0.000000]),[-33.660539,12.400929,-9.814293,-86.122958,-33.748102,85.340395],[0.0,0.0,1.0],[0.0,0.0,1.0])
    robot.setZoneData(10.000)
    robot.setDO(5,1)
    robot.setAO(5,1)
    robot.waitDI(5,1,5000)
    robot.waitDI(5,1,-1)
    robot.RunMessage(r"""Display message""")
    robot.ProgFinish(r"""ajkslfh""")
    for line in robot.PROG:
        print(line)
    if len(robot.LOG) > 0:
        mbox('Program generation LOG:\n\n' + robot.LOG)
    #input("Press Enter to close...")
    #return
    robot.ProgSave(".","Program",True)
    for line in robot.PROG:
        print(line)
    if len(robot.LOG) > 0:
        mbox('Program generation LOG:\n\n' + robot.LOG)

    input("Press Enter to close...")

if __name__ == "__main__":
    """Function to call when the module is executed by itself: test"""
    test_post()
