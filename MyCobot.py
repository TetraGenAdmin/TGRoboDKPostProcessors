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
# for a MyCobot robot
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
# The MyCobot post processor generates Python code compatible with MyCobot robotic arms.
#
#
# Supported Controllers
# 
# ----------------------------------------------------

from robodk import *      # Robot toolbox
#robolink.import_install("serial")
#robolink.import_install("kortex_api", os.environ['PYTHONPATH'] + "/kortex_api-2.2.0.post31-py3-none-any.whl")

# This will force splitting Linear movements into smaller Joint movements
# RDK_COMMANDS = {"MoveLSplitMM": "2", "MoveCSplitMM": "2", "MoveCSplitDeg": "90", "MoveCSplitMinMM": "0"}

# ---------------------------------------------------------------------------------
# Set the minimum number of degrees of freedom that are expected
nDOFs_MIN = 7

# Set the driver version
DRIVER_VERSION = "RoboDK Driver for MyCobot v0.0.0"

# Set to monitor the movement
MONITOR_MOVE = False

# Maximum allowed waiting time during actions (in seconds)
#TIMEOUT_DURATION = 20

# ---------------------------------------------------------------------------------



#------------------------------------------------
# CUSTOM UTILITIES
class DeviceConnection:
    TCP_PORT = 10000
    UDP_PORT = 10001

    @staticmethod
    def createTcpConnection(ip, username="admin", password="admin"):
        """
        returns RouterClient required to create services and send requests to device or sub-devices,
        """
        print("Using TCP connection")
        return DeviceConnection(ip, port=DeviceConnection.TCP_PORT, credentials=(username, password))

    @staticmethod
    def createUdpConnection(ip, username="admin", password="admin"):
        """        
        returns RouterClient that allows to create services and send requests to a device or its sub-devices @ 1khz.
        """
        print("Using UDP connection")
        return DeviceConnection(ip, port=DeviceConnection.UDP_PORT, credentials=(username, password))

    def __init__(self, ipAddress, port=TCP_PORT, credentials = ("","")):
        pass

    def start(self):
        self.transport.connect(self.ipAddress, self.port)

        if (self.credentials[0] != ""):
            from kortex_api.SessionManager import SessionManager
            from kortex_api.autogen.messages import Session_pb2
            
            session_info = Session_pb2.CreateSessionInfo()
            session_info.username = self.credentials[0]
            session_info.password = self.credentials[1]
            session_info.session_inactivity_timeout = 10000   # (milliseconds)
            session_info.connection_inactivity_timeout = 2000 # (milliseconds)

            self.sessionManager = SessionManager(self.router)
            print("Logging as", self.credentials[0], "on device", self.ipAddress)
            self.sessionManager.CreateSession(session_info)

        return self.router

    def finish(self):
        if self.sessionManager != None:
            from kortex_api.RouterClient import RouterClient, RouterClientSendOptions

            router_options = RouterClientSendOptions()
            router_options.timeout_ms = 1000 
            
            self.sessionManager.CloseSession(router_options)

        self.transport.disconnect()

    # Called when entering 'with' statement
    def __enter__(self):        
        return self.start()

    # Called when exiting 'with' statement
    def __exit__(self, exc_type, exc_value, traceback):
        self.finish()
        
#------------------------------------------------


# This class handles communication between this driver (PC) and the robot
class ComRobot:
    """Robot class for programming MyCobot robots"""    
    LAST_MSG = None  # Keep a copy of the last message received
    CONNECTED = False  # Connection status is known at all times
    MYCOBOTAPI = None
    BUFFER_SIZE = None
    #TIMEOUT = None
    #Speed and accelerations
    LINEARSPEED = 100
    LINEARACEL = 30
    JOINTSPEED  = 100
    JOINTACEL  = 80
    LAST_TARGET_JOINTS = []
    
    from robolink import import_install
    
    import_install("pymycobot")
    
    

    def check_for_end_or_abort(self,e):
        """Return a closure checking for END or ABORT notifications

        Arguments:
        e -- event to signal when the action is completed
            (will be set when an END or ABORT occurs)
        """
        from kortex_api.autogen.messages import Base_pb2

        def check(notification, e=e):
            print("EVENT : " + \
                Base_pb2.ActionEvent.Name(notification.action_event))
            if notification.action_event == Base_pb2.ACTION_END \
                    or notification.action_event == Base_pb2.ACTION_ABORT:
                e.set()

        return check


    def joints_to_mycobot(self,jnts):
        return jnts

    def joints_from_mycobot(self,jnts):
        return jnts

    # This is executed when the object is created
    def __init__(self):
        self.BUFFER_SIZE = 512  # bytes
        #self.TIMEOUT = 5 * 60  # seconds: it must be enough time for a movement to complete
        # self.TIMEOUT = 10 # seconds
        self.CONNECTED = False
        self.MYCOBOTAPI = None

    def __del__(self):
        self.disconnect()

    # Disconnect from robot
    def disconnect(self):
        if self.MYCOBOTAPI is not None:
            # Disconnect
            self.MYCOBOTAPI = None

        self.CONNECTED = False
        return True

    # Connect to robot
    def connect(self, ip_com, port=-1):
        self.disconnect()
        print_message('Connecting to robot %s:%i' % (ip_com, port))
        # Create new socket connection
        UpdateStatus(ROBOTCOM_WORKING)        
        sys.stdout.flush()
        
        # https://docs.elephantrobotics.com/docs/gitbook-en/7-ApplicationBasePython/7.3_angle.html
        # MyCobot class initialization requires two parameters:
        #   The first is the serial port string, such as:
        #       linux:  "/dev/ttyUSB0"
        #          or "/dev/ttyAMA0"
        #       windows: "COM3"
        #   The second is the baud rate:: 
        #       M5 version is:  115200
        #
        #    Example:
        #       mycobot-M5:
        #           linux:
        #              mc = MyCobot("/dev/ttyUSB0", 115200)
        #          or mc = MyCobot("/dev/ttyAMA0", 115200)
        #           windows:
        #              mc = MyCobot("COM3", 115200)
        #       mycobot-raspi:
        #           mc = MyCobot(PI_PORT, PI_BAUD)
        #
        # Initiate a MyCobot object
        # Create object code here for windows version
        from pymycobot.mycobot import MyCobot
        #from pymycobot.genre import Angle
        #from pymycobot import PI_PORT, PI_BAUD  # When using the Raspberry Pi version of mycobot, you can refer to these two variables to initialize MyCobot
        self.MYCOBOTAPI = MyCobot(ip_com, 115200)
        UpdateStatus(ROBOTCOM_READY)        
        sys.stdout.flush()
        return True

    def MoveJ(self, joints):        
        #By passing the angle parameter, let each joint of the robotic arm move to the position corresponding to [0, 0, 0, 0, 0, 0]
        self.MYCOBOTAPI.send_angles(joints[:6], 50)
        UpdateStatus(ROBOTCOM_READY)        
        sys.stdout.flush()
        
    def MoveL(self,xyzabc):
        import threading
        """Linear move (joint values provided in degrees)"""
        # Create new action
        from kortex_api.autogen.messages import Base_pb2
        action = Base_pb2.Action()
        action.name = "Linear move from RoboDK"
        action.application_data = ""
        
        x,y,z,rx,ry,rz = xyzabc[:6]
        cartesian_pose = action.reach_pose.target_pose
        cartesian_pose.x = x
        cartesian_pose.y = y
        cartesian_pose.z = z
        cartesian_pose.theta_x = rx
        cartesian_pose.theta_y = ry
        cartesian_pose.theta_z = rz

        e = threading.Event()
        notification_handle = self.base.OnNotificationActionTopic(
            self.check_for_end_or_abort(e),
            Base_pb2.NotificationOptions()
        )
        
        #print("Executing action")
        self.base.ExecuteAction(action)

        #print("Waiting for movement to finish ...")
        while True:
            finished = e.wait(0.02)
            if finished:
                #print("Angular movement completed")
                self.base.Unsubscribe(notification_handle)
                return True
                
            # Monitor joints 
            if MONITOR_MOVE:
                jnts = self.getJoints()
                print_joints(jnts, True)
                pass
            
        self.base.Unsubscribe(notification_handle)
        return False
    
    def MoveC(self,joints):
        raise Exception("Circular move not implemented")
        #try:
        #    self.UARMAPI.set_mode(mode=1) #Mode 1 corresponds to moving
        #    self.UARMAPI.motion_enable(True)
        #    self.UARMAPI.move_circle(pose1=joints[0:6], pose2=joints[7:], percent=50, speed=self.JOINTSPEED, mvacc=self.JOINTACELL, #wait=True)
            #self.LAST_TARGET_JOINTS = joints
        #except Exception as e:
        #    print_message(str(e))
        #    return False
        #return True

    def GripperPosition(self, gripperPosition):
        # Open the gripper the indicated amount
        # Passed:  Integer position between 0 (open) and 1 (closed)

        # Create the GripperCommand we will send
        gripper_command = Base_pb2.GripperCommand()
        finger = gripper_command.gripper.finger.add()

        # Move the gripper
        gripper_command.mode = Base_pb2.GRIPPER_POSITION
        finger.value = gripperPosition
        finger.finger_identifier = 1

        print("Actuating gripper to {:0.2f}...".format(finger.value))
        self.base.SendGripperCommand(gripper_command)

        # Wait for reported position to be reached or speed reaches zero
        gripper_request1 = Base_pb2.GripperRequest()
        gripper_request1.mode = Base_pb2.GRIPPER_POSITION
        gripper_request2 = Base_pb2.GripperRequest()
        gripper_request2.mode = Base_pb2.GRIPPER_SPEED
        while True:
            gripper_measure = self.base.GetMeasuredGripperMovement(gripper_request1)
            gripper_speed = self.base.GetMeasuredGripperMovement(gripper_request2)
            if len(gripper_measure.finger):
                print("Current position is : {0}".format(gripper_measure.finger[0].value))
                if abs(gripper_measure.finger[0].value - gripperPosition) < 0.01:
                    break
                if gripper_speed == 0.0:
                    break
            else: # Else, no finger present in answer, end loop
                break


    def getJoints(self):
        actuator_count = self.base.GetActuatorCount()
        # TODO: Debug data:
        print(actuator_count)
        print("TODO: DEBUG DATA")
        joints = actuator_count.values
        return joints_from_mycobot(joints)
    
    def setSpeed(self, speed_values):
        # speed_values[0] = speed_values[0] # linear speed in mm/s
        # speed_values[1] = speed_values[1] # joint speed in mm/s
        # speed_values[2] = speed_values[2] # linear acceleration in mm/s2
        # speed_values[3] = speed_values[3] # joint acceleration in deg/s2
        if (speed_values[0] != -1):
            self.LINEARSPEED = speed_values[0]

        if (speed_values[1] != -1):
            self.JOINTSPEED = speed_values[1]

        if (speed_values[2] != -1):
            self.LINEARACEL = speed_values[2]

        if (speed_values[3] != -1):
            self.JOINTACEL = speed_values[3]

        return True

    def setTool(self,tool_pose):
        #self.UARMAPI.set_tcp_offset(tool_pose)
        return True

    def Pause(self,timeMS):
        import time
        time.sleep(timeMS/1000)
        return True

    def setRounding(self,rounding):
        return True

    def setDO(self,digital_IO_State):
        return False

    def WaitDI(self,digital_IO_Num):
        return False
        
        #import time
        #start = time.time()
        #ioNumber = digital_IO_Num[0]
        #ioState = self.UARMAPI.get_tgpio_digital(ioNumber)
        #desiredState = digital_IO_Num[1]
        #try:
        #    timeout = digital_IO_Num[2]
        #except Exception as e:
        #    e = e
        #    timeout = 0
#
#        while not (ioState == desiredState) and (time.time() - start) < timeout:
#            ioState = self.UARMAPI.get_tgpio_digital(ioNumber)            
#            time.sleep(0.1)
#        return False


def Robot_Disconnect():
    global ROBOT
    ROBOT.disconnect()




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



# ----------------------------------------------------    
# Object class that handles the robot instructions/syntax
class RobotPost(object):

    #Code generation mode
    # 1 = simulate
    # 2 = Online Programming (run on robot)
    # 3 = Macro generation (RDK.AddProgram)
    POST_CODEGEN_MODE = 1

    #Name of the main function, obtained from first instance of ProgStart being called
    MAIN_PROGRAM_NAME = None

    #Name of the current program being written, only for AddProgram (mode 3)
    #Defaults to robot for api usage (mode 1 and 2)
    CURRENT_PROGRAM_NAME = 'robot'
    
    #----------------------------------------------------
    if POST_CODEGEN_MODE == 3:
        CURRENT_PROGRAM_NAME = 'program'
    
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
        self.ROBOT_NAME = robotname
        self.PROG = []
        self.LOG = ''
        self.nAxes = robot_axes

        self.addline('import sys')
        self.addline('')
        self.addline('def print_message(arg):')
        self.addline('    print(arg)')
        self.addline('def UpdateStatus(arg):')
        self.addline('    pass')
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
            ComRobotLines += inspect.getsourcelines(DeviceConnection)[0]        
            for curLine in ComRobotLines:
                self.addline(curLine.rstrip())
            
        except Exception as e:
            self.addline("raise Exception('Source code not available to add ComRobot class. Contact us at info@robodk.com.')")

        robotName = FilterName(robotname).replace('.', '')
        self.addline('')
        self.addline('')
        self.addline('robot = ComRobot()')
        self.addline('robot.connect(\'' + ip_com + '\', 12345)')
        self.addline('')
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
        self.addline('    global robot')
        self.addline('    # Generating program: ' + prognamesafe)

        self.addline('')
            
        
    def ProgFinish(self, progname):
        self.addline('    return')
        
    def ProgSave(self, folder, progname, ask_user=False, show_result=False):
        if self.MAIN_PROGRAM_NAME is not None:
            self.addline('')
            self.addline('#Call main')
            self.addline(self.MAIN_PROGRAM_NAME + '()')
            

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
        self.addline('    robot.MoveJ([%s])' %  (joints_2_str(joints)) )

    def MoveL(self, pose, joints, conf_RLF=None):
        """Add a linear movement"""
        if pose is None:
            msg = "Linear movement using joint targets is not supported. Change the target type to cartesian or use a joint movement."
            self.addlog(msg)
            self.RunMessage(msg, True)
            return
        
        pose_abs = self.REF_FRAME * pose
        self.addline('    robot.MoveL([%s])' % (joints_2_str(joints) + ',' + mat_2_str(pose) ) )
        
    def MoveC(self, pose1, joints1, pose2, joints2, conf_RLF_1=None, conf_RLF_2=None):
        """Add a circular movement"""    
        if pose1 is None or pose2 is None:
            msg = "Circular movement using joint targets is not supported. Change the target type to cartesian or use a joint movement."
            self.addlog(msg)
            self.RunMessage(msg, True)
            return
        
        self.addline('    robot.MoveC([%s])' % (joints_2_str(joints1) + ',' + mat_2_str(pose1) + ',' + joints_2_str(joints2) + ',' + mat_2_str(pose2)) )        

    def setFrame(self, pose, frame_id=None, frame_name=None):
        """Change the robot reference frame"""
        self.REF_FRAME = pose
        varname = FilterName(frame_name).replace('.', '')
        self.addline('    #%s ref frame set to %s' % (self.ROBOT_NAME,mat_2_str(pose)) )        
        
    def setTool(self, pose, tool_id=None, tool_name=None):
        """Change the robot TCP"""
        self.addline('    robot.setTool([%s])' % (mat_2_str(pose) ) )
        self.addline('')


    def Pause(self, time_ms):
        """Pause the robot program"""
        if time_ms < 0:
            # self.addline('    print(\'STOP\')')
            self.addline('    input("Paused. Press enter to continue")')
        else:
            #self.addline('    import time')
            #self.addline('    time.sleep(%.3f)' % (time_ms*1000))
            # varname = FilterName(self.ROBOT_NAME).replace('.', '')
            self.addline('    robot.Pause(%.0f)' % (time_ms))
    
    def setSpeed(self, speed_mms):
        """Changes the robot speed (in mm/s)"""
        varname = FilterName(self.ROBOT_NAME).replace('.', '')
        self.addline('    robot.setSpeed([%s,-1,-1,-1])' % (str(speed_mms)))

    def setAcceleration(self, accel_mmss):
        """Changes the robot acceleration (in mm/s2)"""
        varname = FilterName(self.ROBOT_NAME).replace('.', '')
        self.addline('    robot.setSpeed([-1,-1,%s,-1])' % (str(accel_mmss)) )

    def setSpeedJoints(self, speed_degs):
        """Changes the robot joint speed (in deg/s)"""
        varname = FilterName(self.ROBOT_NAME).replace('.', '')
        self.addline('    robot.setSpeed([-1,%s,-1,-1])' % (str(speed_degs)) )
    
    def setAccelerationJoints(self, accel_degss):
        """Changes the robot joint acceleration (in deg/s2)"""
        varname = FilterName(self.ROBOT_NAME).replace('.', '')
        self.addline('    robot.setSpeed([-1,-1,-1,%s])' % (str(accel_degss)) )

    def setZoneData(self, zone_mm):
        """Changes the rounding radius (aka CNT, APO or zone data) to make the movement smoother"""
        self.addline('    robot.setRounding(%.3f)' % (zone_mm) )

    def setDO(self, io_var, io_value):
        """Sets a variable (digital output) to a given value"""

        # at this point, io_var and io_value must be string values
        self.addline('    robot.setDO([%s,%s])' % (io_var, io_value))

    def setAO(self, io_var, io_value):
        """Set an Analog Output"""
        self.setDO(io_var, io_value)
        
    def waitDI(self, io_var, io_value, timeout_ms=-1):
        """Waits for a variable (digital input) io_var to attain a given value io_value. Optionally, a timeout can be provided."""
        if timeout_ms > -1:
            timeout_ms = timeout_ms/1000
        self.addline('    robot.WaitDI([%s,%s,%s])' % (io_var, io_value,timeout_ms))
        
    def RunCode(self, code, is_function_call = False):
        """Adds code or a function call"""
        if is_function_call:
            prognamesafe = FilterName(code).replace('.', '')
            code = code.replace(' ','_')
            if "(" in prognamesafe:
                self.addline("    " + prognamesafe)
            else:
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
        
    robot = RobotPost(r"""Quine""",r"""ABB IRB 120-3/0.6""",6, axes_type=['R','R','R','R','R','R'], 
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
