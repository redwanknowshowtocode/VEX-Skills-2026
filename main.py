# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       AdrianNapa                                                   #
# 	Created:      2/17/2026, 11:47:20 AM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

        
# Library imports
from vex import *

brain = Brain()
controller = Controller()

#these are the motor for the drive train, you can change the ports and gear settings as needed but the default gear setting is 18:1 and the default direction is forward (false)
#SmartDrive will be set up later
motorL1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
motorL2 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
motorsupportL = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
motorR3 = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
motorR4 = Motor(Ports.PORT12, GearSetting.RATIO_18_1, True)
motorSupportR = Motor(Ports.PORT13, GearSetting.RATIO_18_1, True)
left_motor = MotorGroup(motorL1, motorL2, motorsupportL)
right_motor = MotorGroup(motorR3, motorR4, motorSupportR)
Base = DriveTrain(left_motor, right_motor) #sets the drive train to use the four motors

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("user controls")
    

def drive_task():
    drive_left = 0
    drive_right = 0

    brain.screen.clear_screen()
    brain.screen.print("driver control")
    # place driver control in this while loop
    while True:
        wait(20, MSEC)
        drive_left = controller.axis3.position()
        drive_right = controller.axis2.position() + 5

        deadband = 15
        if abs(drive_left) < deadband:
            drive_left = 0
        if abs(drive_right) < deadband:
            drive_right = 0

        # The drivetrain
       # Base.drive(drive_left, drive_right, PERCENT) #this is the command to control the drive train, it takes in the left and right values and the units (percent in this case)
        motorL1.spin(FORWARD, drive_left, PERCENT)
        motorL2.spin(FORWARD, drive_left, PERCENT)
        motorsupportL.spin(FORWARD, drive_left, PERCENT)
        motorR3.spin(FORWARD, drive_right, PERCENT)
        motorR4.spin(FORWARD, drive_right, PERCENT)
        motorSupportR.spin(FORWARD, drive_right, PERCENT)
        

        sleep(5)
     
# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()

# run the drive task as a separate thread so that it can run at the same time as the user control and autonomous functions
task1 = Thread(drive_task)