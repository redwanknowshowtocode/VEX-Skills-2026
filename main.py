#endregion VEXcode Generated Robot Configuration
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
import math

brain = Brain()
controller = Controller()

#these are the motor for the drive train, you can change the ports and gear settings as needed but the default gear setting is 18:1 and the default direction is forward (false)
#SmartDrive will be set up later
motorL1 = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
motorL2 = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
motorR3 = Motor(Ports.PORT19, GearSetting.RATIO_18_1, True)
motorR4 = Motor(Ports.PORT20, GearSetting.RATIO_18_1, True)
#odometry variables
x = 0.0
y = 0.0
theta = 0.0 #measured in radians
wheel_radius = 2 #in inches
circumference = 2 * math.pi * wheel_radius
IMU = Inertial(Ports.PORT6) #this is the inertial sensor, it will be used to get the robot's heading
rotation_sensor = Rotation(Ports.PORT18) #this is the rotation sensor, it will be used to get the distance traveled by the robot



def update_position():
    global x, y, theta, previous_degree
    # 1. Distance from tracking wheel
    curr_deg = rotation_sensor.position()
    prev_deg = curr_deg
    delta_deg = curr_deg - prev_deg
    

    delta_rot = delta_deg / 360.0
    delta_s = delta_rot * circumference  # forward distance in inches

    # 2. Heading from IMU
    theta = math.radians(IMU.rotation())

    # 3. Convert local movement to global movement
    dx = delta_s * math.cos(theta)
    dy = delta_s * math.sin(theta)
    # 4. Update global position
    x += dx
    y += dy

def turn_to_angle(target_angle):
    current_angle = IMU.heading
    error = target_angle - current_angle
    while abs(error) > 2:  # Allowable error of 2 degree
        turn_speed = max(min(error * 0.5, 100), -100)  # Proportional control
        motorL1.spin(FORWARD, turn_speed, PERCENT)
        motorL2.spin(FORWARD, turn_speed, PERCENT)
        motorR3.spin(FORWARD, -turn_speed, PERCENT)
        motorR4.spin(FORWARD, -turn_speed, PERCENT)
        wait(20, MSEC)
        current_angle = IMU.heading
        error = target_angle - current_angle

def drive_straight(distance): 
    rotation_sensor.reset_position()
    IMU.reset_heading()
    target_distance = distance

    deadband = 1 #to keep the heading straight and locked while it drives straight, we have a deadband
    while True:
        if abs(IMU.heading()) < deadband:



        

def drive_to_point(target_x, target_y):
    pass

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    origin = (0, 0)

    #a standard vex field is 12ft by 12ft, which is 144 inches by 144 inches, so the max distance the robot can travel in one direction is 144 inches but we are positioned at the bottom middle so we account for that value being at (72,0)
    top_right_corner = (72, 144 )
    top_left_corner = (-72, 144)
    bottom_left_corner = (-72, 0)
    bottom_right_corner = (72, 0)

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
        drive_left = controller.axis3.position() + 15
        drive_right = controller.axis2.position() + 5

        deadband = 16
        if abs(drive_left) < deadband:
            drive_left = 0
        if abs(drive_right) < deadband:
            drive_right = 0


        #Base.drive(FORWARD) #this is the command to control the drive train, it takes in the left and right values and the units (percent in this case)
        motorL1.spin(FORWARD, drive_left, PERCENT)
        motorL2.spin(FORWARD, drive_left, PERCENT)
        motorR3.spin(FORWARD, drive_right, PERCENT)
        motorR4.spin(FORWARD, drive_right, PERCENT)

        sleep(5)
     
# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()

# run the drive task as a separate thread so that it can run at the same time as the user control and autonomous functions
#task1 = Thread(drive_task)
task2 = Thread(drive_straight(10))