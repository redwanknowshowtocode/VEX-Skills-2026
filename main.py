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
motor1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
motor2 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
motor3 = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
motor4 = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)

left_motors = [motor1, motor2]
right_motors = [motor3, motor4]
Base = DriveTrain(left_motors, right_motors) #sets the drive train to use the four motors

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
        drive_right = controller.axis2.position()

        deadband = 15
        if abs(drive_left) < deadband:
            drive_left = 0
        if abs(drive_right) < deadband:
            drive_right = 0

        # The drivetrain
        Base.drive(drive_left, drive_right, PERCENT) #this is the command to control the drive train, it takes in the left and right values and the units (percent in this case)
        '''motor1.spin(FORWARD, drive_left, PERCENT)
        motor2.spin(FORWARD, drive_left, PERCENT)
        motor3.spin(FORWARD, drive_right, PERCENT)
        motor4.spin(FORWARD, drive_right, PERCENT)
        '''

        sleep(5)
     
# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()

# run the drive task as a separate thread so that it can run at the same time as the user control and autonomous functions
task1 = Thread(drive_task)