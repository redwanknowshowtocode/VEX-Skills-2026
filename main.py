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
Base = DriveTrain(motor1, motor2,) #sets the drive train to use the two motors

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    # place driver control in this while loop
    while True:
        wait(20, MSEC)

        #sets drive velocity
        Base.set_drive_velocity(controller.axis3.position(), PERCENT)
        
        #finds the position of the vertial axis for the left joystick and moves the robot forward or reverse based on the position of the joystick
        vertical = controller.axis3.position()
        if vertical > 0:
            Base.drive(FORWARD)
        elif vertical < 0:
            Base.drive(REVERSE)
        elif vertical == 0:
            Base.stop()

    #finds the position of the horizontal axis for the left joystick and turns the robot left or right based on the position of the joystick
        horizontal = controller.axis4.position()        
        if horizontal > 0:
            Base.turn(horizontal)
        elif horizontal < 0:
            Base.turn(-horizontal)
        elif horizontal == 0:
            Base.stop()

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()