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
motorL1 = Motor(Ports.PORT11, GearSetting.RATIO_6_1, False)
motorL2 = Motor(Ports.PORT12, GearSetting.RATIO_6_1, False)
motorR1 = Motor(Ports.PORT19, GearSetting.RATIO_6_1, True)
motorR2 = Motor(Ports.PORT20, GearSetting.RATIO_6_1, True)
#odometry variables
x = 0.0
y = 0.0
theta = 0.0 #measured in radians
wheel_radius = 2 #in inches
circumference = 2 * math.pi * wheel_radius
IMU = Inertial(Ports.PORT6) #this is the inertial sensor, it will be used to get the robot's heading
rotation_sensor = Rotation(Ports.PORT18) #this is the rotation sensor, it will be used to get the distance traveled by the robot

#intake motor
Intake_motor = Motor(Ports.PORT3, GearSetting.RATIO_6_1, True)

#transfer system motors
transfer_motor_top1 = Motor(Ports.PORT1, GearSetting.RATIO_6_1, True)
transfer_motor_top2= Motor(Ports.PORT10, GearSetting.RATIO_6_1, True)






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
    Kp = 0.5  # proportional gain, tune this

    while True:
        current = IMU.rotation()
        error = target_angle - current

        # Stop when close enough
        if abs(error) < 1:
            break

        turn_power = Kp * error

        motorL1.spin(FORWARD, -turn_power, PERCENT)
        motorL2.spin(FORWARD, -turn_power, PERCENT)

        motorR1.spin(FORWARD, turn_power, PERCENT)
        motorR2.spin(FORWARD, turn_power, PERCENT)


        wait(20, MSEC)

    motorL1.stop()
    motorL2.stop()
    motorR1.stop()
    motorR2.stop()

def drive_straight(distance):
    global x, y

    # Reset tracking wheel reference
    start_x = x
    start_y = y

    # Lock heading
    target_heading = IMU.rotation()
    Kp = 0.6

    while True:
        update_position()

        # How far have we traveled?
        dx = x - start_x
        dy = y - start_y
        traveled = math.sqrt(dx*dx + dy*dy)

        if traveled >= distance:
            break

        # Heading correction
        error = target_heading - IMU.rotation()
        correction = Kp * error

        motorL1.spin(FORWARD, 50 + correction, PERCENT)
        motorL2.spin(FORWARD, 50 + correction, PERCENT)

        motorR1.spin(FORWARD, 50 - correction, PERCENT)
        motorR2.spin(FORWARD, 50 - correction, PERCENT)

        wait(20, MSEC)

    motorL1.stop()
    motorL2.stop()

    motorR1.stop()
    motorR2.stop()

        

def go_to_point(target_x, target_y):
    global x, y

    # 1. Compute angle to target
    angle = math.degrees(math.atan2(target_y - y, target_x - x))

    # 2. Turn to face that angle
    turn_to_angle(angle)

    # 3. Compute distance to target
    dx = target_x - x
    dy = target_y - y
    distance = math.sqrt(dx*dx + dy*dy)

    # 4. Drive straight to it
    drive_straight(distance)


def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")

    #a standard vex field is 12ft by 12ft, which is 144 inches by 144 inches, so the max distance the robot can travel in one direction is 144 inches but we are positioned at the bottom middle so we account for that value being at (72,0)
    go_to_point(72, 144)
    go_to_point(-72, 144)
    go_to_point(-72, 0)
    go_to_point(72, 0)

    #test auto


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
        motorR1.spin(FORWARD, drive_right, PERCENT)
        motorR2.spin(FORWARD, drive_right, PERCENT)

        sleep(5)

def intake_task():
    #this is where you would put the code to control the intake, it would be similar to the drive task but with different motors and controls
    while True:
        wait(20, MSEC)
        if controller.buttonL1.pressing():
            Intake_motor.spin(FORWARD, 100, PERCENT)
        
        elif controller.buttonL2.pressing():
            Intake_motor.spin(REVERSE, 100, PERCENT)            
        
        elif controller.buttonR1.pressing():
            transfer_motor_top1.spin(FORWARD, 100, PERCENT)
            transfer_motor_top2.spin(FORWARD, 100, PERCENT)
        
        elif controller.buttonR2.pressing():
            transfer_motor_top1.spin(REVERSE, 100, PERCENT)
            transfer_motor_top2.spin(REVERSE, 100, PERCENT)
        
        elif controller.buttonA.pressing():
            transfer_motor_top2.spin
        
        else:
            Intake_motor.stop()
            transfer_motor_top1.stop()
            transfer_motor_top2.stop()


# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()

# run the drive task as a separate thread so that it can run at the same time as the user control and autonomous functions
#task2 = Thread(autonomous)
task1 = Thread(drive_task)
task3 = Thread(intake_task)