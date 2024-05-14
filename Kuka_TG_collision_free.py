#### Copyright 2015-2020 - RoboDK Inc. - https://robodk.com/
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
# for a KUKA robot using RoboDK. This post includes support for KRC2 and KRC4 controller
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
# Import RoboDK tools
from robodk import *




# Change the main header here
DEFAULT_HEADER_MAIN = '''
;FOLD Declaration
   DECL EKI_STATUS RET
   DECL BOOL weld_ret
   DECL INT DIALOGANSWER
   INT i
   INT count
   INT part_id
   
   INT numOfToolPaths
   INT numOfCapturePoses
   
   FRAME tcp
   FRAME baseFrame
   FRAME moveFrame
   
   
;ENDFOLD (Declaration)

; GLOBAL INTERRUPT DECL 3 WHEN $STOPMESS==TRUE DO IR_STOPM ( )
; INTERRUPT ON 3

;FOLD Initialise and set default speed
BAS (#INITMOV,0)
BAS (#VEL_PTP,100)
BAS (#ACC_PTP,20)
$VEL.CP=0.2
BAS (#TOOL,0)
BAS (#BASE,0)
;ENDFOLD

;;FOLD STARTPOS
;$BWDSTART = FALSE
;PDAT_ACT = PDEFAULT
;BAS(#PTP_DAT)
;FDAT_ACT = {TOOL_NO 0,BASE_NO 0,IPO_FRAME #BASE}
;BAS(#FRAMES)
;;ENDFOLD

$ADVANCE = 3

;FOLD ---- Quickly skip BCO ----
; PTP $AXIS_ACT 
;ENDFOLD

;FOLD ---- GO HOME ----
; PTP {A1 0.000, A2 -90.000, A3 90.000, A4 0.000, A5 0.000, A6 0.000, E1 0, E2 0, E3 0, E4 0, E5 0, E6 0}
;ENDFOLD

count = 0
part_id =10
i=1
numOfToolPaths =1
numOfCapturePoses = 1
tcp = TOOL_DATA[2] ; tcp large
baseFrame = $NULLFRAME
moveFrame = $NULLFRAME


baseFrame = $NULLFRAME 
$BASE = baseFrame
$TOOL = tcp


RET=EKI_Init("TGXmlConfig")
RET=EKI_Open("TGXmlConfig")


wait for $Flag[1]
;MsGDialoG(DIALOGANSWER,"Make sure there is no tool.","SAFETY_CHECK",,,,,,,,"Yes")
$FLAG[2] =False
RET=EKI_SetInt("TGXmlConfig","Robot/PartID/@ID", part_id)
RET = EKI_Send("TGXmlConfig","Robot")
RET = EKI_ClearBuffer("TGXmlConfig", "Robot");
wait for $FLAG[2];handshake
$FLAG[2] =False
RET = EKI_ClearBuffer("TGXmlConfig", "Sensor");

wait sec 0.5

;capture starts here
; need to know number of capture poses


RET=EKI_SetInt("TGXmlConfig","Robot/PartID/@ID", part_id)
RET = EKI_Send("TGXmlConfig","Robot")
RET = EKI_ClearBuffer("TGXmlConfig", "Robot");
wait for $FLAG[2];handshake
$FLAG[2] =False
RET = EKI_ClearBuffer("TGXmlConfig", "Sensor");

wait for $FLAG[2]
$FLAG[2] =False
RET=EKI_GetFrame("TGXmlConfig","Sensor/BaseFrame", moveFrame) 
RET=EKI_GetInt("TGXmlConfig","Sensor/Data/@NumberOfToolPaths",numOfCapturePoses)
RET = EKI_ClearBuffer("TGXmlConfig", "Sensor");
RET=EKI_SetInt("TGXmlConfig","Robot/PartID/@ID", part_id);handshake
RET = EKI_Send("TGXmlConfig","Robot")
RET = EKI_ClearBuffer("TGXmlConfig", "Robot");


;;;;;;;;;;;;

PTP {A1 -11.27,A2 -70.18,A3 82.40,A4 -1.82,A5 80.83,A6 -4.90,E1 0.00000} 

$TOOL = TOOL_DATA[2]
$BASE = $NULLFRAME
$VEL.CP = 1
self.addline('$LOAD = LOAD_DATA[1]')

FOR i = 1 to numOfCapturePoses
    wait for $FLAG[2]
    $FLAG[2] =False
    RET=EKI_GetFrame("TGXmlConfig","Sensor/BaseFrame", moveFrame) 
    RET=EKI_GetInt("TGXmlConfig","Sensor/Data/@NumberOfToolPaths",numOfCapturePoses)
    RET = EKI_ClearBuffer("TGXmlConfig", "Sensor");
    RET=EKI_SetInt("TGXmlConfig","Robot/PartID/@ID", part_id);handshake
    RET = EKI_Send("TGXmlConfig","Robot")
    RET = EKI_ClearBuffer("TGXmlConfig", "Robot");



    LIN moveFrame

        wait sec 1
    RET=EKI_SetInt("TGXmlConfig","Robot/PartID/@ID", part_id)
    RET = EKI_Send("TGXmlConfig","Robot")
    RET = EKI_ClearBuffer("TGXmlConfig", "Robot");
    wait for $FLAG[2];handshake
    $FLAG[2] =False
    RET = EKI_ClearBuffer("TGXmlConfig", "Sensor");






ENDFOR


RET=EKI_SetInt("TGXmlConfig","Robot/PartID/@ID", part_id)
RET = EKI_Send("TGXmlConfig","Robot")
RET = EKI_ClearBuffer("TGXmlConfig", "Robot");
wait for $FLAG[2];handhsake
$FLAG[2] =False
RET = EKI_ClearBuffer("TGXmlConfig", "Sensor");


wait for $FLAG[2]
$FLAG[2] =False
MsGDialoG(DIALOGANSWER,"Make sure there is no tool.","SAFETY_CHECK",,,,,,,,"Yes")
RET=EKI_GetFrame("TGXmlConfig","Sensor/BaseFrame", baseFrame)
$BASE = baseFrame   
RET=EKI_GetInt("TGXmlConfig","Sensor/Data/@NumberOfToolPaths",numOfToolPaths)
RET = EKI_ClearBuffer("TGXmlConfig", "Sensor");
RET=EKI_SetInt("TGXmlConfig","Robot/PartID/@ID", part_id);handshake
RET = EKI_Send("TGXmlConfig","Robot")
RET = EKI_ClearBuffer("TGXmlConfig", "Robot");
wait sec 1

$BASE = $NULLFRAME

'''


mainn = '''
baseFrame = $NULLFRAME 
$BASE = baseFrame
$TOOL = tcp


RET=EKI_Init("TGXmlConfig")
RET=EKI_Open("TGXmlConfig")


wait for $Flag[1]
;MsGDialoG(DIALOGANSWER,"Make sure there is no tool.","SAFETY_CHECK",,,,,,,,"Yes")
$FLAG[2] =False
RET=EKI_SetInt("TGXmlConfig","Robot/PartID/@ID", part_id)
RET = EKI_Send("TGXmlConfig","Robot")
RET = EKI_ClearBuffer("TGXmlConfig", "Robot");
wait for $FLAG[2];handshake
$FLAG[2] =False
RET = EKI_ClearBuffer("TGXmlConfig", "Sensor");

wait sec 0.5

;capture starts here
; need to know number of capture poses


RET=EKI_SetInt("TGXmlConfig","Robot/PartID/@ID", part_id)
RET = EKI_Send("TGXmlConfig","Robot")
RET = EKI_ClearBuffer("TGXmlConfig", "Robot");
wait for $FLAG[2];handshake
$FLAG[2] =False
RET = EKI_ClearBuffer("TGXmlConfig", "Sensor");

wait for $FLAG[2]
$FLAG[2] =False
RET=EKI_GetFrame("TGXmlConfig","Sensor/BaseFrame", moveFrame) 
RET=EKI_GetInt("TGXmlConfig","Sensor/Data/@NumberOfToolPaths",numOfCapturePoses)
RET = EKI_ClearBuffer("TGXmlConfig", "Sensor");
RET=EKI_SetInt("TGXmlConfig","Robot/PartID/@ID", part_id);handshake
RET = EKI_Send("TGXmlConfig","Robot")
RET = EKI_ClearBuffer("TGXmlConfig", "Robot");


;;;;;;;;;;;;

PTP {A1 -11.27,A2 -70.18,A3 82.40,A4 -1.82,A5 80.83,A6 -4.90,E1 0.00000} 

$TOOL = TOOL_DATA[2]
$BASE = $NULLFRAME
$VEL.CP = 1
$LOAD = LOAD_DATA[1]

FOR i = 1 to numOfCapturePoses
    wait for $FLAG[2]
    $FLAG[2] =False
    RET=EKI_GetFrame("TGXmlConfig","Sensor/BaseFrame", moveFrame) 
    RET=EKI_GetInt("TGXmlConfig","Sensor/Data/@NumberOfToolPaths",numOfCapturePoses)
    RET = EKI_ClearBuffer("TGXmlConfig", "Sensor");
    RET=EKI_SetInt("TGXmlConfig","Robot/PartID/@ID", part_id);handshake
    RET = EKI_Send("TGXmlConfig","Robot")
    RET = EKI_ClearBuffer("TGXmlConfig", "Robot");



    LIN moveFrame

        wait sec 1
    RET=EKI_SetInt("TGXmlConfig","Robot/PartID/@ID", part_id)
    RET = EKI_Send("TGXmlConfig","Robot")
    RET = EKI_ClearBuffer("TGXmlConfig", "Robot");
    wait for $FLAG[2];handshake
    $FLAG[2] =False
    RET = EKI_ClearBuffer("TGXmlConfig", "Sensor");






ENDFOR


RET=EKI_SetInt("TGXmlConfig","Robot/PartID/@ID", part_id)
RET = EKI_Send("TGXmlConfig","Robot")
RET = EKI_ClearBuffer("TGXmlConfig", "Robot");
wait for $FLAG[2];handhsake
$FLAG[2] =False
RET = EKI_ClearBuffer("TGXmlConfig", "Sensor");


wait for $FLAG[2]
$FLAG[2] =False
MsGDialoG(DIALOGANSWER,"Make sure there is no tool.","SAFETY_CHECK",,,,,,,,"Yes")
RET=EKI_GetFrame("TGXmlConfig","Sensor/BaseFrame", baseFrame)
$BASE = baseFrame   
RET=EKI_GetInt("TGXmlConfig","Sensor/Data/@NumberOfToolPaths",numOfToolPaths)
RET = EKI_ClearBuffer("TGXmlConfig", "Sensor");
RET=EKI_SetInt("TGXmlConfig","Robot/PartID/@ID", part_id);handshake
RET = EKI_Send("TGXmlConfig","Robot")
RET = EKI_ClearBuffer("TGXmlConfig", "Robot");
wait sec 1

$BASE = $NULLFRAME
''' 


DEFAULT_HEADER_SAFE_MOVE = '''

; GLOBAL INTERRUPT DECL 3 WHEN $STOPMESS==TRUE DO IR_STOPM ( )
; INTERRUPT ON 3

;FOLD Initialise and set default speed
BAS (#INITMOV,0)
BAS (#VEL_PTP,100)
BAS (#ACC_PTP,100)
$VEL.CP=0.2
BAS (#TOOL,0)
BAS (#BASE,0)
;ENDFOLD

;;FOLD STARTPOS
;$BWDSTART = FALSE
;PDAT_ACT = PDEFAULT
;BAS(#PTP_DAT)
;FDAT_ACT = {TOOL_NO 0,BASE_NO 0,IPO_FRAME #BASE}
;BAS(#FRAMES)
;;ENDFOLD

$ADVANCE = 5

;FOLD ---- Quickly skip BCO ----
; PTP $AXIS_ACT 
;ENDFOLD

;FOLD ---- GO HOME ----
; PTP {A1 0.000, A2 -90.000, A3 90.000, A4 0.000, A5 0.000, A6 0.000, E1 0, E2 0, E3 0, E4 0, E5 0, E6 0}
;ENDFOLD
$BASE = $NULLFRAME

'''




DEFAULT_HEADER = '''
DECL EKI_STATUS RET
DECL BOOL weld_ret
FRAME baseFrame

; GLOBAL INTERRUPT DECL 3 WHEN $STOPMESS==TRUE DO IR_STOPM ( )
; INTERRUPT ON 3

;FOLD Initialise and set default speed
BAS (#INITMOV,0)
BAS (#VEL_PTP,100)
BAS (#ACC_PTP,20)
$VEL.CP=0.2
BAS (#TOOL,0)
BAS (#BASE,0)
;ENDFOLD

;;FOLD STARTPOS
;$BWDSTART = FALSE
;PDAT_ACT = PDEFAULT
;BAS(#PTP_DAT)
;FDAT_ACT = {TOOL_NO 0,BASE_NO 0,IPO_FRAME #BASE}
;BAS(#FRAMES)
;;ENDFOLD

$ADVANCE = 5

;FOLD ---- Quickly skip BCO ----
; PTP $AXIS_ACT 
;ENDFOLD

;FOLD ---- GO HOME ----
; PTP {A1 0.000, A2 -90.000, A3 90.000, A4 0.000, A5 0.000, A6 0.000, E1 0, E2 0, E3 0, E4 0, E5 0, E6 0}
;ENDFOLD

'''


defaultt =  '''
baseFrame = $NULLFRAME


;RET=EKI_SetInt("XmlConfig","Robot/PartID/@ID", part_id);handshake
RET = EKI_Send("TGXmlConfig","Robot")
RET = EKI_ClearBuffer("TGXmlConfig", "Robot");
wait for $FLAG[2]
$FLAG[2] = False
RET = EKI_ClearBuffer("TGXmlConfig", "Sensor");


wait for $FLAG[2]
$FLAG[2] = False
RET=EKI_GetFrame("TGXmlConfig","Sensor/BaseFrame", baseFrame)
$BASE = baseFrame   

RET = EKI_ClearBuffer("TGXmlConfig", "Sensor");
;RET=EKI_SetInt("XmlConfig","Robot/PartID/@ID", part_id);handshake
RET = EKI_Send("TGXmlConfig","Robot")
RET = EKI_ClearBuffer("TGXmlConfig", "Robot");

IF baseFrame.X == 10000 THEN
    RETURN
ENDIF

'''

DEFAULT_CODE_TOOL_ON = '''
;FOLD TURN_ON WELDING
;--- WELDING TURN_ON ---
WAIT SEC 1
$OUT[16] = TRUE
;---CONFIRM WELDING ON ---
;WAIT FOR $IN[1] == TRUE
;--- PLASMA WELDING_ON ---

;ENDFOLD
'''

DEFAULT_CODE_TOOL_OFF = '''
;FOLD TURN_OFF WELDING
;--- WELDING TURN_OFF ---
$OUT[16] = FALSE
;---CONFIRM WELDING OFF ---
;WAIT FOR $IN[1] == FALSE
WAIT SEC 1
;--- WELDING TURN_FALSE ---
;ENDFOLD
'''

    
# ----------------------------------------------------    
# Object class that handles the robot instructions/syntax
# Important: This is the default KUKA KRC2 Post used as a reference for all other posts
class RobotPost(object):
    """Robot post object"""  

    current_program_name = ""

    base_frame_should_be_called = False

    # ------------------------------------------------------------------------
    # ------------------- KUKA POST PROCESSOR CONFIGURATION ------------------
    # Maximum number of lines per program. It will then generate multiple "pages (files)" if the program is too long
    # This is the default value. You can change this value in RoboDK:
    # Tools-Options-Program-Limit the maximum number of lines per program
    MAX_LINES_X_PROG = 250000  

    # Set to True to include subprograms in the main program. Otherwise, programs can be generated separately.
    INCLUDE_SUB_PROGRAMS = True # Set to True to include subprograms in the same file
    
    # Generate subprograms as new files instead of adding them in the same file (INCLUDE_SUB_PROGRAMS must be set to True)
    SUB_PROGRAMS_AS_FILES = False

    # Set KRC Version (2 or 4)
    # Version 2 for KRC2 controllers or Version 4 for KRC4
    #KRC_VERSION = 2  # for KRC2 controllers
    KRC_VERSION = 4  # for KRC4 controllers
    
    # Display messages on the teach pendant. This feature is not supported by all controllers and must be disabled for some controllers.
    SKIP_MESSAGE_POPUPS = False
    #SKIP_MESSAGE_POPUPS = True    
    
    # Use frame index if provided (example: rename your reference to Frame 2 to use BASE_DATA[2])
    FRAME_INDEX = False
    
    # Use Tool index if provided (example: rename your tool to Tool 3 to use TOOL_DATA[3])
    TOOL_INDEX = False

    # Set if we want to have cascaded program calls when program splitting takes place
    # Usually, cascaded is better for older controllers
    CASCADED_CALLS = (KRC_VERSION <= 2)
    # CASCADED_CALLS = True
    # CASCADED_CALLS = False

    # Optionally output configuration and turn flags S and T
    # If we set this to true, the output targets will have the configuration and turn bits added in the movement 
    # (for example: S B'010', T B'000001')
    ADD_CONFIG_TURN = True
    
    # Add a keyword to split subprograms
    # SKIP_PROG_KEYWORD = 'spindle'
    SKIP_PROG_KEYWORD = None

    # File extension: set the program extension
    PROG_EXT = 'src'

    # Program name max length (KRC4 is 24 characters)
    PROG_NAME_LEN = 16

    # ------- Parameters for 3D printing --------
    # Use a synchronized external axis as an extruder (E1, E2, ... or the last available axis)
    EXTAXIS_EXTRUDER = True
    #EXTAXIS_EXTRUDER = False

    # Use a weld gun as an extruder
    #WELD_EXTRUDER = True
    WELD_EXTRUDER = False

    # Parameters for 3D printing using a custom extruder
    # 3D Printing Extruder Setup Parameters:
    PRINT_E_ANOUT = 5              # Analog Output ID to command the extruder flow
    PRINT_SPEED_2_SIGNAL = 0.10 # Ratio to convert the speed/flow to an analog output signal
    PRINT_FLOW_MAX_SIGNAL = 24  # Maximum signal to provide to the Extruder
    PRINT_ACCEL_MMSS = -1      # Acceleration, -1 assumes constant speed if we use rounding/blending

    # ----------------------------------------------------  

    # Change the main header here
    HEADER = DEFAULT_HEADER
    HEADER_MAIN = DEFAULT_HEADER_MAIN
    HEADER_SAFE_MOVE = DEFAULT_HEADER_SAFE_MOVE

    CODE_TOOL_ON = DEFAULT_CODE_TOOL_ON

    CODE_TOOL_OFF = DEFAULT_CODE_TOOL_OFF
    
    # Set the order of external axes
    AXES_DATA = ['A1','A2','A3','A4','A5','A6','E1','E2','E3','E4','E5','E6']
    
    #-----------------------------------------------------------
    #-----------------------------------------------------------
    # ----------------------------------------------------
    def filtername_len(self, name):
        return FilterName(name[:self.PROG_NAME_LEN], 'P')
        
    def pose_2_str(self, pose):
        """Converts a pose target to a string"""
        if pose is None:
            raise Exception("Unable to create a Linear movement (LIN) using a Joint Target. Use a Cartesian target instead.")
        #[x,y,z,w,p,r] = Pose_2_KUKA(pose)
        #return ('X %.3f, Y %.3f, Z %.3f, A %.3f, B %.3f, C %.3f' % (x,y,z,w,p,r)) # old version had to be switched
        [x,y,z,r,p,w] = pose_2_xyzrpw(pose)
        return ('X %.3f,Y %.3f,Z %.3f,A %.3f,B %.3f,C %.3f' % (x,y,z,w,p,r))

    def pose_2_str_ext(self,pose,joints):
        njoints = len(joints)
        if njoints <= 6:
            return self.pose_2_str(pose)
        else:     
            extaxes = ''
            for i in range(njoints-6):
                extaxes = extaxes + (',%s %.5f' % (self.AXES_DATA[i+6], joints[i+6]))
            return self.pose_2_str(pose) + extaxes
        
    def angles_2_str(self,angles):
        """Prints a joint target"""
        str = ''
        #if self.KRC_VERSION >= 4:
        #    str = 'AXIS: '       
        
        for i in range(len(angles)):
            str = str + ('%s %.5f,' % (self.AXES_DATA[i], angles[i]))
        str = str[:-1]
        return str

          
    def conf_2_str(self,confRLF):
        if confRLF is None:
            return "'B010'"
        strconf = ""
        if confRLF[2] > 0:
            strconf = strconf + '1'
        else:
            strconf = strconf + '0'
            
        if confRLF[1] == 0:
            strconf = strconf + '1'
        else:
            strconf = strconf + '0'
            
        if confRLF[0] > 0:
            strconf = strconf + '1'
        else:
            strconf = strconf + '0'
        
        return "'B%s'" % strconf    
        
    def joints_2_turn_str(self,joints):
        if joints is None:
            return "'B000000'"
            
        strturn = ""
        for i in range(len(joints)):
            if joints[i] < 0:
                strturn = '1' + strturn
            else:
                strturn = '0' + strturn
        return "'B%s'" % strturn  
    
    #------------------------------------------------
    #------------------------------------------------
    #------------------------------------------------
    
    # other variables
    ROBOT_POST = ''
    ROBOT_NAME = ''
    lines_x_prog = MAX_LINES_X_PROG
    
    # Multiple program files variables
    PROG_NAME = 'unknown' # single program name
    PROG_NAMES = []
    PROG_FILES = []    
    PROG_LIST = []
    nLines = 0
    nProgs = 0
    AutoCreateMain = True
    
    PROG = []
    LOG = ''
    nAxes = 6
    APO_VALUE = 1
    C_DIS = ''#' C_DIS'
    C_PTP = ''#' C_PTP'
    
    PROG_CALLS = []
    PROG_CALLS_LIST = []    
    
    # Default speed
    SPEED_MMS = 500
    
    ARC_ON = False
       
    # Internal 3D Printing Parameters
    PRINT_POSE_LAST = None # Last pose printed
    PRINT_E_LAST = 0 # Last Extruder length
    PRINT_E_NEW = None # New Extruder Length
    PRINT_E_NEW_MOTOR = 0 # External axis value to start controlling the external axis
    PRINT_LAST_SIGNAL = None # Last extruder signal
    
    def __init__(self, robotpost=None, robotname=None, robot_axes = 6, **kwargs):
        self.ROBOT_POST = robotpost
        self.ROBOT_NAME = robotname
        self.PROG = []
        self.LOG = ''
        self.nAxes = robot_axes
        for k,v in kwargs.items():
            if k == 'lines_x_prog':
                self.lines_x_prog = v       
        
    def ProgStart(self, progname, new_page = False):
        progname = self.filtername_len(progname)
        progname_i = progname
        if new_page:
            nPages = len(self.PROG_LIST)
            if nPages == 0:
                progname_i = progname
            else:
                progname_i = "%s%i" % (self.PROG_NAME, nPages)
            
        else:
            #self.PROG_NAME = progname
            #self.nProgs = self.nProgs + 1
            #self.PROG_NAMES = []
            #if self.nProgs > 1 and not self.INCLUDE_SUB_PROGRAMS:
            #    return
        
            self.PROG_NAME = progname
            self.nProgs = self.nProgs + 1
            #self.PROG_NAMES = []
            if self.nProgs > 1:
                if not self.INCLUDE_SUB_PROGRAMS:
                    # Stop adding programs
                    return
                else:
                    self.AutoCreateMain = False
                    if not self.SUB_PROGRAMS_AS_FILES:
                        # Stop adding programs
                        self.PROG_NAMES = []
                    else:
                        # Important!! We can't have cascaded calls if we are including sub programs (one or the other)
                        print("Warning! Adding subprograms and automatic program splitting is not supported")                    

        self.PROG_NAMES.append(progname_i)    
        self.base_frame_should_be_called = True
        
        self.programe_name_last_4_character = ""
        
        if len(self.PROG_NAME) >=4:
            self.programe_name_last_4_character = self.PROG_NAME[-4:]
                


        if self.programe_name_last_4_character == "Main":
            self.addline('DEF %s ( )' % progname_i)
        else:
            self.addline('DEF %s ( )' % progname_i)
            # txt = self.part_name+progname_i
            # self.addline('DEF %s ( )' % txt)
        if not new_page:
            if self.KRC_VERSION < 4:
                # KRC2 needs this EXT declaration
                self.PROG.append('EXT BAS (BAS_COMMAND :IN,REAL :IN )');

            
            
             
            if self.programe_name_last_4_character == "Main":    
                self.PROG.append(self.HEADER_MAIN)
            elif self.PROG_NAME[0].lower() == 's':
                self.PROG.append(self.HEADER_SAFE_MOVE)
            else:
                self.PROG.append(self.HEADER)
            #if self.nAxes > 6:
            #    self.addline('$ACT_EX_AX = %i' % (self.nAxes-6))
        #else:
        #    self.PROG += '*PROGDEFS*\n'
        
    #def ProgFinish(self, progname, new_page = False):        
    #    if new_page:
    #        self.PROG.append("END")
    #        self.PROG_LIST.append(self.PROG)
    #        self.PROG_CALLS_LIST.append(self.PROG_CALLS)
    #        self.PROG = []
    #        self.PROG_CALLS = []
    #        self.nLines = 0
    
    def ProgFinish(self, progname, new_page = False):    
        if self.PROG[-1] == "END":
            return   
        if new_page or (self.INCLUDE_SUB_PROGRAMS and self.SUB_PROGRAMS_AS_FILES):
            self.PROG.append("END")
            self.PROG_LIST.append(self.PROG)
            self.PROG_CALLS_LIST.append(self.PROG_CALLS)
            self.PROG = []
            self.PROG_CALLS = []
            self.nLines = 0
        else:
            self.PROG.append("END")
        
    def progsave(self, filesave): 
        #progname = progname + '.' + self.PROG_EXT                
        #filesave = folder + '/' + progname
        
        ext_defs = ''   
        if self.KRC_VERSION < 4:
            for prog_nm in self.PROG_CALLS:
                ext_defs += "EXT %s()\n" % prog_nm
        
        if len(ext_defs) > 0 and len(self.PROG) > 1:
            self.PROG.insert(1, ext_defs)
            self.PROG.insert(1, "\n; External program calls:")            
            
        with open(filesave, "w", encoding="utf-8", errors="replace") as fid:
            #fid.write("&ACCESS RVP\n")
            #fid.write("&REL 1\n")
            #fid.write("&COMMENT Generated by RoboDK\n")
            fid.write("&ACCESS RVP\n")
            fid.write("&REL 1\n") #fid.write("&REL 29\n")
            fid.write("&PARAM TEMPLATE = C:\\KRC\\Roboter\\Template\\vorgabe\n")
            fid.write("&PARAM EDITMASK = *\n")
            for line in self.PROG:
                fid.write(line)
                fid.write("\n")

        print('SAVED: %s\n' % filesave) # tell RoboDK the path of the saved file
        self.PROG_FILES.append(filesave)
        
    def ProgSave(self, folder, progname, ask_user = False, show_result = False):
        progname = self.filtername_len(progname)
        if ask_user or not DirExists(folder):
            folder = getSaveFolder(folder,'Select a directory to save your program')
            if folder is None:
                # The user selected the Cancel button
                return
        
        # Remember the files to display
        files_display = []           
        
        if len(self.PROG_LIST) >= 1:
            if self.nLines > 0:
                self.ProgFinish(progname, True)  

            npages = len(self.PROG_LIST)
            
            # Check if we are generating subprograms as files (in this case, automatic splitting is not supported)
            if self.AutoCreateMain:            
                if self.CASCADED_CALLS:                
                    for i in range(npages-1):
                        prog_call_next = self.PROG_NAMES[i+1]
                        self.PROG_CALLS_LIST[i].append(prog_call_next)
                        self.PROG_LIST[i].insert(-1, "\n; Continue running program as cascaded execution")
                        self.PROG_LIST[i].insert(-1, prog_call_next+"()\n")
                        
                else:
                    progname_main = progname + "Main"
                    mainprog = []
                    mainprog.append("DEF %s ( )" % progname_main)
                    for i in range(npages):
                        self.PROG = self.PROG_LIST[i]
                        mainprog.append("%s()" % self.PROG_NAMES[i])
                        
                    # mainprog.append("END")
                    self.PROG = mainprog
                    filesave = folder + '/' + progname_main + '.' + self.PROG_EXT
                    files_display.append(filesave)
                    self.progsave(filesave)
                        
            for i in range(npages):
                self.PROG = self.PROG_LIST[i]
                self.PROG_CALLS = self.PROG_CALLS_LIST[i]
                filesave = folder + '/' + self.PROG_NAMES[i] + '.' + self.PROG_EXT
                files_display.append(filesave)
                self.progsave(filesave)
                
        else:
            # self.PROG.append("END")
            filesave = folder + '/' + progname + '.' + self.PROG_EXT
            files_display.append(filesave)
            self.progsave(filesave)
            
            
        #-------------------------------------------------------        
        # open file with default application
        if show_result:
            # Do not display too many files
            if len(files_display) > 4:
                files_display = files_display[:4]
                
            if type(show_result) is str:
                # Open file with provided application
                import subprocess
                p = subprocess.Popen([show_result] + files_display)
            elif type(show_result) is list:
                import subprocess
                p = subprocess.Popen(show_result + files_display)   
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
            
    def calculate_time(self, distance, Vmax, Amax=-1):
        """Calculate the time to move a distance with Amax acceleration and Vmax speed"""
        if Amax < 0:
            # Assume constant speed (appropriate smoothing/rounding parameter must be set)
            Ttot = distance/Vmax
        else:
            # Assume we accelerate and decelerate
            tacc = Vmax/Amax;
            Xacc = 0.5*Amax*tacc*tacc;
            if distance <= 2*Xacc:
                # Vmax is not reached
                tacc = sqrt(distance/Amax)
                Ttot = tacc*2
            else:
                # Vmax is reached
                Xvmax = distance - 2*Xacc
                Tvmax = Xvmax/Vmax
                Ttot = 2*tacc + Tvmax
        return Ttot
            
    def new_move(self, new_pose):                        
        """Implement the action on the extruder for 3D printing, if applicable"""
        if self.WELD_EXTRUDER or self.EXTAXIS_EXTRUDER:
            return
            
        if self.PRINT_E_NEW is None or new_pose is None:
            return
            
        # Skip the first move and remember the pose
        if self.PRINT_POSE_LAST is None:
            self.PRINT_POSE_LAST = new_pose
            return          

        # Calculate the increase of material for the next movement
        add_material = self.PRINT_E_NEW - self.PRINT_E_LAST
        self.PRINT_E_LAST = self.PRINT_E_NEW
        
        # Calculate the robot speed and Extruder signal
        extruder_signal = 0
        if add_material > 0:
            distance_mm = norm(subs3(self.PRINT_POSE_LAST.Pos(), new_pose.Pos()))
            # Calculate movement time in seconds
            time_s = self.calculate_time(distance_mm, self.SPEED_MMS, self.PRINT_ACCEL_MMSS)
            
            # Avoid division by 0
            if time_s > 0:
                # This may look redundant but it allows you to account for accelerations and we can apply small speed adjustments
                speed_mms = distance_mm / time_s
                
                # Calculate the extruder speed in RPM*Ratio (self.PRINT_SPEED_2_SIGNAL)
                extruder_signal = speed_mms * self.PRINT_SPEED_2_SIGNAL
        
        # Make sure the signal is within the accepted values
        extruder_signal = max(0,min(self.PRINT_FLOW_MAX_SIGNAL, extruder_signal))
        
        # Update the extruder speed when required
        if self.PRINT_LAST_SIGNAL is None or abs(extruder_signal - self.PRINT_LAST_SIGNAL) > 1e-6:
            self.PRINT_LAST_SIGNAL = extruder_signal
            # Use the built-in setDO function to set an analog output
            #self.setDO(PRINT_E_ANOUT, "%.3f" % extruder_signal)
            # Use customized code for the output
            self.addline('$ANOUT[%i]=%.3f' % (self.PRINT_E_ANOUT, extruder_signal))
            # Use customized program call
            #self.addline('ExtruderSpeed(%.3f)' % extruder_signal)
        
        # Remember the last pose
        self.PRINT_POSE_LAST = new_pose
    
    def MoveJ(self, pose, joints, conf_RLF=None):
        if self.base_frame_should_be_called == True:
            self.base_frame_should_be_called = False
            if self.programe_name_last_4_character == "Main":
                    
                self.PROG.append(mainn)
                # self.addline('$TOOL = {FRAME: ' + self.pose_2_str(self.torch_tcp) + '}')
                self.addline('$TOOL = TOOL_DATA[8]')
                self.addline('$LOAD = LOAD_DATA[1]')
            elif self.PROG_NAME[0].lower() == 's':
                self.addline('$TOOL = TOOL_DATA[8]')
                self.addline('$LOAD = LOAD_DATA[1]')
            else:
                
                self.PROG.append(defaultt)
                # self.addline('$TOOL = {FRAME: ' + self.pose_2_str(self.torch_tcp) + '}')
                self.addline('$TOOL = TOOL_DATA[8]')
                self.addline('$LOAD = LOAD_DATA[1]')


        """Add a joint movement"""
        if self.EXTAXIS_EXTRUDER:
            joints.append(self.PRINT_E_NEW_MOTOR)
            
        # self.addline('PTP {' + self.angles_2_str(joints) + '}' + self.C_PTP)
        str_config = ''
        if self.ADD_CONFIG_TURN:
            str_config = ', S %s, T %s' % (self.conf_2_str(conf_RLF), self.joints_2_turn_str(joints))
            
        self.addline('PTP {' + self.pose_2_str(pose) + str_config +'}' + self.C_PTP)
        
    def MoveL(self, pose, joints, conf_RLF=None):
        if self.base_frame_should_be_called == True:
            self.base_frame_should_be_called = False
            if self.programe_name_last_4_character == "Main":
                    
                self.PROG.append(mainn)
                # self.addline('$TOOL = {FRAME: ' + self.pose_2_str(self.torch_tcp) + '}')
                self.addline('$TOOL = TOOL_DATA[8]')
                self.addline('$LOAD = LOAD_DATA[1]')
            elif self.PROG_NAME[0].lower() == 's':
                self.addline('$TOOL = TOOL_DATA[8]')
                self.addline('$LOAD = LOAD_DATA[1]')
            else:
                
                self.PROG.append(defaultt)
                # self.addline('$TOOL = {FRAME: ' + self.pose_2_str(self.torch_tcp) + '}')
                self.addline('$TOOL = TOOL_DATA[8]')
                self.addline('$LOAD = LOAD_DATA[1]')
        """Add a linear movement"""
        self.new_move(pose) # used for 3D printing
        
        if self.EXTAXIS_EXTRUDER:
            joints.append(self.PRINT_E_NEW_MOTOR)
        
        # Optionally, add configuration data
        str_config = ''
        if self.ADD_CONFIG_TURN:
            str_config = ', S %s, T %s' % (self.conf_2_str(conf_RLF), self.joints_2_turn_str(joints))
            
        self.addline('LIN {' + self.pose_2_str_ext(pose,joints) + str_config + '}' + self.C_DIS)
        
    def MoveC(self, pose1, joints1, pose2, joints2, conf_RLF_1=None, conf_RLF_2=None):
        if self.base_frame_should_be_called == True:
            self.base_frame_should_be_called = False
            if self.programe_name_last_4_character == "Main":
                    
                self.PROG.append(mainn)
                # self.addline('$TOOL = {FRAME: ' + self.pose_2_str(self.torch_tcp) + '}')
                self.addline('$TOOL = TOOL_DATA[8]')
                self.addline('$LOAD = LOAD_DATA[1]')
            elif self.PROG_NAME[0].lower() == 's':
                self.addline('$TOOL = TOOL_DATA[8]')
                self.addline('$LOAD = LOAD_DATA[1]')
            else:
                
                self.PROG.append(defaultt)
                # self.addline('$TOOL = {FRAME: ' + self.pose_2_str(self.torch_tcp) + '}')
                self.addline('$TOOL = TOOL_DATA[8]')
                self.addline('$LOAD = LOAD_DATA[1]')
        """Add a circular movement"""
        self.new_move(pose2) # used for 3D printing
        
        if self.EXTAXIS_EXTRUDER:
            joints2.append(self.PRINT_E_NEW_MOTOR)
        
        str_config1 = ''
        str_config2 = ''
        if self.ADD_CONFIG_TURN:
            str_config1 = ' S %s, T %s' % (self.conf_2_str(conf_RLF_1), self.joints_2_turn_str(joints))
            str_config2 = ' S %s, T %s' % (self.conf_2_str(conf_RLF_2), self.joints_2_turn_str(joints))
        
        self.addline('CIRC {' + self.pose_2_str_ext(pose1,joints1) + str_config1 + '},{' + self.pose_2_str_ext(pose2,joints2) + str_config2 + '}' + self.C_DIS)
        
    def setFrame(self, pose, frame_id, frame_name):
        """Change the robot reference frame"""
        self.addline('; ---- Setting reference (Base) ----')
        if self.nAxes > 6:
            # Code to output if the robot has an external axis:
            
            # option 1:
            #self.addline('$BASE = EK (MACHINE_DEF[2].ROOT, MACHINE_DEF[2].MECH_TYPE, { %s })' % self.pose_2_str(pose))    

            # option 2:            
            #self.addline('$BASE=EK(EX_AX_DATA[1].ROOT,EX_AX_DATA[1].EX_KIN, { %s })' % self.pose_2_str(pose))
            
            # Option 3:
            self.addline('; Using external axes')
            self.addline('; $BASE=EK(EX_AX_DATA[1].ROOT,EX_AX_DATA[1].EX_KIN,EX_AX_DATA[1].OFFSET)')
            self.addline('; $ACT_EX_AX= %i' % (self.nAxes - 6))
            #return
            
        if frame_name is not None and frame_name.endswith("Base"): 
            # Usually for the robot base frame
            frame_id = 1
            self.BASE_ID = frame_id
            self.addline('$BASE = {FRAME: ' + self.pose_2_str(pose) + '}')
            self.addline('; BASE_DATA[%i] = {FRAME: %s}' % (self.BASE_ID, self.pose_2_str(pose)))
            self.addline('; $BASE = BASE_DATA[%i]' % (self.BASE_ID))
            
        elif frame_id is not None and frame_id >= 1: 
            # specified ID reference frame (for example a reference frame named "Frame 2" -> frame_id = 2
            self.BASE_ID = frame_id
            self.addline('; BASE_DATA[%i] = {FRAME: %s}' % (self.BASE_ID, self.pose_2_str(pose)))            
            if self.FRAME_INDEX:
                self.addline('; $BASE = {FRAME: ' + self.pose_2_str(pose) + '}')            
                self.addline('$BASE = BASE_DATA[%i]' % (self.BASE_ID))
            else:
                self.addline('$BASE = {FRAME: ' + self.pose_2_str(pose) + '}')            
                self.addline('; $BASE = BASE_DATA[%i]' % (self.BASE_ID))
            
        else: 
            # unspecified ID reference frame
            self.BASE_ID = 1
            self.addline('$BASE = {FRAME: ' + self.pose_2_str(pose) + '}')
            
        self.addline('; --------------------------')
        
    def setTool(self, pose, tool_id, tool_name):
        """Change the robot TCP"""        
        self.addline('; ---- Setting tool (TCP) ----')
        self.torch_tcp = pose
        if tool_id is not None and tool_id >= 1:
            # specified ID tool (for example, a tool named "Tool 3" -> tool_id = 3
            self.TOOL_ID = tool_id      
            self.addline('; TOOL_DATA[%i] = {FRAME: %s}' % (self.TOOL_ID, self.pose_2_str(pose)))                        
            if self.TOOL_INDEX:
                self.addline('; $TOOL = {FRAME: ' + self.pose_2_str(pose) + '}')            
                self.addline('$TOOL = TOOL_DATA[%i]' % (self.TOOL_ID))
            else:
                self.addline('$TOOL = {FRAME: ' + self.pose_2_str(pose) + '}')            
                self.addline('; $TOOL = TOOL_DATA[%i]' % (self.TOOL_ID))
            
        else:
            self.TOOL_ID = 1 # Default Tool ID
            self.addline('$TOOL = {FRAME: ' + self.pose_2_str(pose) + '}')
            
        self.addline('; --------------------------')

        

        





        
    def Pause(self, time_ms):
        """Pause the robot program"""
        if time_ms <= 0:
            self.addline('HALT')
        else:
            self.addline('WAIT SEC %.3f' % (time_ms*0.001))
        
    def setSpeed(self, speed_mms):
        """Changes the robot speed (in mm/s)"""
        self.SPEED_MMS = speed_mms
        self.addline('$VEL.CP = %.5f' % (speed_mms/1000.0))
    
    def setAcceleration(self, accel_mmss):
        """Changes the current robot acceleration"""
        self.addline('$ACC.CP = %.5f' % (accel_mmss/1000.0))
                
    def setSpeedJoints(self, speed_degs):
        """Changes the robot joint speed (in deg/s)"""
        self.addline('$VEL.ORI1 = %.5f' % speed_degs)
        self.addline('$VEL.ORI2 = %.5f' % speed_degs)
    
    def setAccelerationJoints(self, accel_degss):
        """Changes the robot joint acceleration (in deg/s2)"""
        self.addline('$ACC.ORI1 = %.5f' % accel_degss)
        self.addline('$ACC.ORI2 = %.5f' % accel_degss)
        
    def setZoneData(self, zone_mm):
        """Changes the zone data approach (makes the movement more smooth)"""
        self.APO_VALUE = zone_mm
        if zone_mm >= 0:
            self.addline('$APO.CPTP = %.3f' % min(100,zone_mm))
            self.addline('$APO.CDIS = %.3f' % zone_mm)
            self.C_DIS = ' C_DIS'
            self.C_PTP = ' C_PTP'
        else:
            self.C_DIS = ''
            self.C_PTP = ''
        
    def setDO(self, io_var, io_value):
        """Set a Digital Output"""
        if type(io_var) != str:  # set default variable name if io_var is a number
            io_var = '$OUT[%s]' % str(io_var)        
        if type(io_value) != str: # set default variable value if io_value is a number            
            if io_value > 0:
                io_value = 'TRUE'
            else:
                io_value = 'FALSE'
        
        # at this point, io_var and io_value must be string values
        self.addline('%s=%s' % (io_var, io_value))
        
    def setAO(self, io_var, io_value):
        """Set an Analog Output"""
        if type(io_var) != str:
            io_var = '$ANOUT[%s]' % str(io_var)
            
        self.setDO(io_var, io_value)
        
    def waitDI(self, io_var, io_value, timeout_ms=-1):
        """Waits for an input io_var to attain a given value io_value. Optionally, a timeout can be provided."""
        if type(io_var) != str:  # set default variable name if io_var is a number
            io_var = '$IN[%s]' % str(io_var)        
        if type(io_value) != str: # set default variable value if io_value is a number            
            if io_value > 0:
                io_value = 'TRUE'
            else:
                io_value = 'FALSE'
        
        # at this point, io_var and io_value must be string values
        if timeout_ms < 0:
            self.addline('WAIT FOR (%s==%s)' % (io_var, io_value))
        else:
            self.addline('START_TIMER:')
            self.addline('$TIMER_STOP[1]=TRUE')
            self.addline('$TIMER_FLAG[1]=FALSE')
            self.addline('$TIMER[1]=%.3f' % (float(timeout_ms)*0.001))
            self.addline('$TIMER_STOP[1]=FALSE')
            self.addline('WAIT FOR (%s==%s OR $TIMER_FLAG[1])' % (io_var, io_value))
            self.addline('$TIMER_STOP[1]=TRUE')
            self.addline('IF $TIMER_FLAG[1]== TRUE THEN')
            self.addline('    HALT ; Timed out!')
            self.addline('    GOTO START_TIMER')
            self.addline('ENDIF')      
        
    def RunCode(self, code, is_function_call = False):
        """Adds code or a function call"""
        if self.SKIP_PROG_KEYWORD is not None and self.SKIP_PROG_KEYWORD.lower() in code.lower():
            self.addline(';' + code)
            return
            
        if is_function_call:
            code_lower = code.lower()
            if code_lower.startswith("extruder("):            
                # If the program call is Extruder(123.56), we extract the number as a string and convert it to a number                
                e_new = float(code[9:-1]) # it needs to retrieve the extruder length from the program call
                
                if e_new > 0.0 and not self.ARC_ON:
                    if self.WELD_EXTRUDER:
                        self.ARC_ON = True
                        self.addline(self.CODE_TOOL_ON)
                    
                elif e_new <= 0.0 and self.ARC_ON:
                    if self.WELD_EXTRUDER:
                        self.ARC_ON = False
                        self.addline(self.CODE_TOOL_OFF)
                    
                #print("Extruder: %.3f" % e_new)
                # Do not generate the program call
                self.PRINT_E_NEW = e_new
                self.PRINT_E_NEW_MOTOR += max(0,self.PRINT_E_NEW-self.PRINT_E_LAST)
                #self.addline('Print: E %.3f' % self.PRINT_E_NEW)
                return
                
            elif code_lower.startswith('arc_on') or code_lower.startswith('arcstart'):
                if not self.ARC_ON:
                    self.ARC_ON = True
                    self.addline(self.CODE_TOOL_ON)
                return
                
            elif code_lower.startswith('arc_off') or code_lower.startswith('arcend'):
                if self.ARC_ON:
                    self.ARC_ON = False
                    self.addline(self.CODE_TOOL_OFF)
                return
            
            elif code_lower.startswith('weld_on') or code_lower.startswith('weld_on'):
                if not self.ARC_ON:
                    self.ARC_ON = True
                    self.addline("weld_ret = weld_on()")
                return
            elif code_lower.startswith('weld_off') or code_lower.startswith('weld_off'):
                if self.ARC_ON:
                    self.ARC_ON = False
                    self.addline("weld_ret = weld_off()")
                return

            

        
            code = code.replace(' ','_')
            if not code.endswith(')'):
                code = self.filtername_len(code)
                code = code + '()'
                
            fcn_def = code
            if '(' in fcn_def:
                fcn_def = fcn_def.split('(')[0]
            if not (fcn_def in self.PROG_CALLS):
                self.PROG_CALLS.append(fcn_def)
                
            self.addline(code)
        else:
            self.addline(code)
        
    def RunMessage(self, message, iscomment = False):
        """Add a comment or a popup message"""
        if iscomment or self.SKIP_MESSAGE_POPUPS:
            self.addline('; ' + message)
        else:
            self.addline('Wait for StrClear($LOOP_MSG[])')
            self.addline('$LOOP_CONT = TRUE')
            self.addline('$LOOP_MSG[] = "%s"' % message)
            
# ------------------ private ----------------------                       
    def addline(self, newline):
        """Add a program line"""
        if self.nProgs > 1 and not self.INCLUDE_SUB_PROGRAMS:
            return
        
        if self.nLines > self.lines_x_prog:
            self.nLines = 0
            self.ProgFinish(self.PROG_NAME, True)
            self.ProgStart(self.PROG_NAME, True)

        self.PROG.append(newline)
        self.nLines = self.nLines + 1
        
    def addlog(self, newline):
        """Add a log message"""
        if self.nProgs > 1 and not self.INCLUDE_SUB_PROGRAMS:
            return
            
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

    robot = RobotPost('Kuka_custom', 'Generic Kuka')

    robot.ProgStart("Program")
    robot.RunMessage("Program generated by RoboDK", True)
    robot.setFrame(Pose([807.766544, -963.699898, 41.478944, 0, 0, 0]), 4, "Frame 4")
    robot.setTool(Pose([62.5, -108.253175, 100, -60, 90, 0]), 2, "Tool 2")
    robot.MoveJ(Pose([200, 200, 500, 180, 0, 180]), [-46.18419, -6.77518, -20.54925, 71.38674, 49.58727, -302.54752] )
    robot.MoveL(Pose([200, 250, 348.734575, 180, 0, -150]), [-41.62707, -8.89064, -30.01809, 60.62329, 49.66749, -258.98418] )
    robot.MoveL(Pose([200, 200, 262.132034, 180, 0, -150]), [-43.73892, -3.91728, -35.77935, 58.57566, 54.11615, -253.81122] )
    robot.RunMessage("Setting air valve 1 on")
    robot.RunCode("ArcStart(1)", True)
    robot.Pause(1000)
    robot.MoveL(Pose([200, 250, 348.734575, 180, 0, -150]), [-41.62707, -8.89064, -30.01809, 60.62329, 49.66749, -258.98418] )
    robot.MoveL(Pose([250, 300, 278.023897, 180, 0, -150]), [-37.52588, -6.32628, -34.59693, 53.52525, 49.24426, -251.44677] )
    robot.MoveL(Pose([250, 250, 191.421356, 180, 0, -150]), [-39.75778, -1.04537, -40.37883, 52.09118, 54.15317, -246.94403] )
    robot.RunMessage("Setting air valve off")
    robot.RunCode("ArcEnd()", True)
    robot.Pause(1000)
    robot.MoveL(Pose([250, 300, 278.023897, 180, 0, -150]), [-37.52588, -6.32628, -34.59693, 53.52525, 49.24426, -251.44677] )
    robot.MoveL(Pose([250, 200, 278.023897, 180, 0, -150]), [-41.85389, -1.95619, -34.89154, 57.43912, 52.34162, -253.73403] )
    robot.MoveL(Pose([250, 150, 191.421356, 180, 0, -150]), [-43.82111, 3.29703, -40.29493, 56.02402, 56.61169, -249.23532] )
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
