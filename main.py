#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration
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
prev_deg = 0
circumference = 2 * math.pi * wheel_radius
IMU = Inertial(Ports.PORT6) #this is the inertial sensor, it will be used to get the robot's heading
rotation_sensor = Rotation(Ports.PORT18) #this is the rotation sensor, it will be used to get the distance traveled by the robot

#intake motor
Intake_motor = Motor(Ports.PORT3, GearSetting.RATIO_6_1, True)

#transfer system motors
transfer_motor_top1 = Motor(Ports.PORT1, GearSetting.RATIO_6_1, True)
transfer_motor_top2= Motor(Ports.PORT10, GearSetting.RATIO_6_1, True)






def update_position():
    global x, y, theta, prev_deg
    # 1. Distance from tracking wheel
    curr_deg = rotation_sensor.position()
    delta_deg = curr_deg - prev_deg
    prev_deg = curr_deg
    

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

        #slows down as we get closer to the needed angle
        turn_power = Kp * error

        #just in case the turn power stalls, we add more power depending on the error value (overshoots or undershoots)
        if abs(turn_power) < 10:
            turn_power = 10 * (1 if error > 0 else -1)

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
    brain.screen.print("this is the start position ", start_x, start_y)


    # Lock heading
    target_heading = IMU.rotation()
    brain.screen.print("this is the target_heading ", target_heading)
    Kp = 0.5

    while True:
        update_position()

        # How far have we traveled?
        dx = x - start_x
        dy = y - start_y
        traveled = math.sqrt(dx*dx + dy*dy)
        brain.screen.print("this is the traveled distance: ")

        remaining = distance - traveled

        # Minimum and maximum speeds to fix speed when its coming near distance
        max_speed = 50
        min_speed = 5

        # Slow down when close but we have a min there so it does not stall
        speed = max(min_speed, max_speed * (remaining / distance))

        if traveled >= distance:
            brain.screen.print("this is the end of the function")
            break

        # Heading correction
        error = target_heading - IMU.rotation()
        correction = Kp * error
        
        
        brain.screen.print("now driving forwards")
        motorL1.spin(FORWARD, speed + correction, PERCENT)
        motorL2.spin(FORWARD, speed + correction, PERCENT)

        motorR1.spin(FORWARD, speed - correction, PERCENT)
        motorR2.spin(FORWARD, speed - correction, PERCENT)

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
    


    IMU.calibrate()
    while IMU.is_calibrating():
        wait(20, MSEC)

    IMU.reset_heading()

    turn_to_angle(90)
    wait(2, SECONDS)
    turn_to_angle(0)
    wait(2, SECONDS)
    turn_to_angle(-90)
    
    '''
    rotation_sensor.reset_position()
    IMU.reset_heading()

    global x, y, theta, prev_deg
    x = 0
    y = 0
    theta = 0
    prev_deg = 0

    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    
    #a standard vex field is 12ft by 12ft, which is 144 inches by 144 inches, so the max distance the robot can travel in one direction is 144 inches but we are positioned at the bottom middle so we account for that value being at (72,0)
    drive_straight(30)
    '''

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
        
        elif controller.buttonR2.pressing():
            transfer_motor_top1.spin(REVERSE, 100, PERCENT)
        
        elif controller.buttonA.pressing():
            transfer_motor_top2.spin(FORWARD, 100, PERCENT)
        
        elif controller.buttonB.pressing():
            transfer_motor_top2.spin(REVERSE, 100, PERCENT)
        
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