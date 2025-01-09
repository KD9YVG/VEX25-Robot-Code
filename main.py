###########################
## AUTONOMUS AROUND LINE 137 ##
###########################

#region VEXcode Generated Robot Configuration
from vex import *
import urandom # type: ignore

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
Left = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
Right = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
Chain = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
String = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)
Finger = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)


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

from math import pi

# Start constants

# Define axis3, the left stick up/down,
# as the stick to drive forward and backwards.
AXIS_DRIVE_FORWARD_AND_BACKWARD=controller_1.axis3

# Define axis1, the right stick left/right,
# as the stick to turn the robot.
AXIS_TURN_LEFT_AND_RIGHT=controller_1.axis1

# Set the deadzone for the controller,
# so that if any analog input is less than the deadzone,
# it is ignored.
DEADZONE=10

# Define the buttons to control the chain.
# All of the controls are grouped so that
# it is easier to visualize and modify.
BUTTON_CHAIN_FORWARD=controller_1.buttonL1
BUTTON_CHAIN_REVERSE=controller_1.buttonL2
BUTTON_STRING_FORWARD=controller_1.buttonR1
BUTTON_STRING_REVERSE=controller_1.buttonR2

# Buttons for finger movements
BUTTON_FINGER=controller_1.buttonX

# Define the speed multipliers. These should
# be values between 0 and 1.

# Speed multiplier of the whole drivetrain,
# usually should not change.
NUMBER_OVERALL_SPEED=1

# Multiplier for forward and backward
NUMBER_DRIVE_SPEED=0.85

# Multiplier for turning
NUMBER_TURN_SPEED=0.4

# Speed to move the string at
NUMBER_STRING_SPEED=0.1
NUMBER_STRING_HARDSTOP=0
# IMPORTANT NOTE: The string and chain
# use digital inputs, so the string
# is not able to move faster or slower
# than this speed.

# Set this to 0.15 if you need to adjust
# the hardstop.

# Speed to move the chain at. See the note
# above about digital inputs.
NUMBER_CHAIN_SPEED=1

SINGLE_DEGREE=1597208273

#endregion constants

# Variable to check whether the timer is currently runnning
isgoing = False
isfingerdown = True

def turn_degrees(d,wait=False):
    Right.set_position(0,TURNS)
    Left.set_position(0,TURNS)
    Right.spin_to_position((SINGLE_DEGREE*d)/200000000000,TURNS,wait=False)
    Left.spin_to_position(0-(SINGLE_DEGREE*d)/200000000000,TURNS,wait=wait)

def move_forward(inches,wait=False):
    Right.set_position(0,TURNS)
    Left.set_position(0,TURNS)
    Right.spin_to_position(0-(inches+1)/(4*pi),TURNS,wait=False)
    Left.spin_to_position(0-(inches+1)/(4*pi),TURNS,wait=wait)
def fun():
    Chain.set_velocity(75,PERCENT)
    Chain.spin(REVERSE)
    move_forward(80,True)
    wait(10, SECONDS)
    Chain.stop()
#fun()
def autonomous_old():
    Chain.set_velocity(100,PERCENT)
    Chain.spin(REVERSE)
    move_forward(10,True)
    wait(10, SECONDS)
    # turn_degrees(-90,True)

def autonomous():
    move_forward(-36,True)
    fingercallback()
    Chain.set_velocity(100,PERCENT)
    Chain.spin(REVERSE)
    wait(1, SECONDS)
    Chain.spin(FORWARD)
    wait(1,SECONDS)
    Chain.stop()
    fingercallback()
    move_forward(20, True)
    turn_degrees(-90, True)
    move_forward(-30,True)

def deadzonify(inputvalue):
    # Make the input zero if the absolute value
    # is less than the deadzone.

    # Check the absolute value, so that small
    # NEGATIVE values are also ignored
    if abs(inputvalue)<DEADZONE:
        # If it's less than the deadzone, make it zero.
        return 0
    # Otherwise, don't change it.
    return inputvalue

def fingercallback():
    global isfingerdown
    isfingerdown=not isfingerdown
    Finger.set_velocity(100, PERCENT)
    if isfingerdown:
        Finger.spin_to_position(0, TURNS,wait=True)
        ## Finger.set_velocity(0.0001,PERCENT)
        ## Finger.spin(FORWARD)
    else:
        Finger.stop()
        Finger.spin_to_position(-0.2,TURNS,wait=True)
fingercallback()

autonomous()
#COCKROACH WAS HERE

def when_started():
    # Clear the screen and tell the user
    # how to start the timer.
    controller_1.screen.clear_screen()
    controller_1.screen.set_cursor(1,1)
    controller_1.screen.print("Hold B for timer")
    # Add callbacks for each button and axis
    BUTTON_CHAIN_FORWARD.pressed(lambda: Chain.spin(FORWARD))
    BUTTON_CHAIN_FORWARD.released(Chain.stop)
    BUTTON_CHAIN_REVERSE.pressed(lambda: Chain.spin(REVERSE))
    BUTTON_CHAIN_REVERSE.released(Chain.stop)
    BUTTON_STRING_FORWARD.pressed(lambda: String.spin(FORWARD))
    BUTTON_STRING_FORWARD.released(String.stop)
    BUTTON_STRING_REVERSE.pressed(lambda: String.spin(REVERSE))
    BUTTON_STRING_REVERSE.released(String.stop)
    ##BUTTON_FINGER_DOWN.pressed(lambda: Finger.spin(REVERSE))
    ##BUTTON_FINGER_DOWN.released(Finger.stop)
    ##BUTTON_FINGER_UP.pressed(lambda: Finger.spin(FORWARD))
    ##BUTTON_FINGER_UP.released(Finger.stop)
    BUTTON_FINGER.released(fingercallback)
    AXIS_DRIVE_FORWARD_AND_BACKWARD.changed(setaxis)
    AXIS_TURN_LEFT_AND_RIGHT.changed(setaxis)
    # I really should make buttonB a constant, like BUTTON_TIMER
    # or something. And make the callbacks "timerpressed" instead
    # of "Apressed"
    controller_1.buttonB.released(Areleased)
    controller_1.buttonB.pressed(Apressed)
    # Make the chain and string go the speed we've defined
    Chain.set_velocity(NUMBER_CHAIN_SPEED*100,PERCENT) 
    String.set_velocity(NUMBER_STRING_SPEED*100,PERCENT)
    # Set left motor and right motor to zero, because of the note below.
    Left.set_velocity(0,PERCENT)
    Right.set_velocity(0,PERCENT)
    # When the left and right motors
    # are moving, we need to set_velocity to
    # the controller's input percentage.
    # When the controller is moved, the velocity
    # is changed. The easiest way to do this
    # is to make it always "on", just at 0%.
    Left.spin(REVERSE)
    Right.spin(FORWARD)
    # Finger should brake when not being moved.
    Finger.set_stopping(BRAKE)
    while True:
        ## print(Finger.position(TURNS))
        ## print(String.position(DEGREES)) # Debugging to figure out the hardstop for the string

        # If the string is below the hardstop, move it there, but, not if left is pressed.
        if String.position(DEGREES)<NUMBER_STRING_HARDSTOP and not controller_1.buttonLeft.pressing():
            String.spin_to_position(NUMBER_STRING_HARDSTOP+4,DEGREES,wait=False)
            print("Hardstop triggered")

        ## print(brain.timer.time(SECONDS)) # Debugging from the old timer
        if isgoing: # While the timer is running, display the timer value on the screen.
            controller_1.screen.clear_row(1)
            controller_1.screen.set_cursor(2,1)
            controller_1.screen.print(brain.timer.time(SECONDS))
        wait(15,MSEC) # Make sure the event loop doesn't get bogged down.

def setaxis(): # Callback when any axis is changed
    drive_speed_multiplier=(NUMBER_OVERALL_SPEED*NUMBER_DRIVE_SPEED) # includes drive multiplier AND overall mult
    axis_position=deadzonify(AXIS_DRIVE_FORWARD_AND_BACKWARD.position()) # Position of the axis, taking deadzone into account
    updownpos=drive_speed_multiplier*(0-axis_position) # Make the axis inverted, to fix an inverted driving issue we had

    turn_speed_multiplier=(NUMBER_OVERALL_SPEED*NUMBER_TURN_SPEED) # includes turn multiplier AND overall mult
    axis_position=deadzonify(AXIS_TURN_LEFT_AND_RIGHT.position()) # Position of the axis, taking deadzone into account
    leftrightpos=turn_speed_multiplier*axis_position               # Do the final computations, as above.

    Left.set_velocity(updownpos+leftrightpos,PERCENT)              # Make the motors actually do the positions.
    Right.set_velocity(updownpos-leftrightpos,PERCENT)

justchangedisgoing=False # Make sure the timer isn't started on press, and stopped on the same release.

def Apressed(): # Callback when timer button pressed
    global isgoing,justchangedisgoing
    if isgoing:
        isgoing=False
        justchangedisgoing=True            #Get ready and show how to time
        controller_1.screen.clear_screen()
        controller_1.screen.set_cursor(2,1)
        controller_1.screen.print(str(brain.timer.time(SECONDS)))
        controller_1.screen.set_cursor(1,1)
        controller_1.screen.print("Hold B for timer")
    else:
        controller_1.screen.clear_screen()    # Display message showing how to start
        controller_1.screen.set_cursor(1,1)
        controller_1.screen.print("Let go of B to start!")

def Areleased(): # Callback when timer button released
    global isgoing,justchangedisgoing
    if not isgoing:
        if justchangedisgoing:
            justchangedisgoing=False
        else:
            brain.timer.clear()                       # Clear timer, and inform user how to stop.
            controller_1.screen.set_cursor(1,1)
            controller_1.screen.print("Press B to stop")
            isgoing=True

Chain.set_stopping(HOLD)  # Make intake hold its position when stopped
String.set_stopping(HOLD)

wait(15,MSEC)

competition = Competition(when_started, autonomous) # Define the competition for VEX to do whatever with