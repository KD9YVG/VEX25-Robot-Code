#region default definitions and config
from vex import *
from math import pi

# commentformat off
import urandom # type: ignore
# commentformat on

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
Left = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
Right = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
Chain = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
Finger = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
Extra = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)


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

#endregion default definitions and config

class dumbobj:
    def __init__(self,d):
        pass
    def __getattr__(self,name):
        raise NameError("Name "+name+" is not defined.")

JOYSTICK_DRIVE=controller_1.axis3
JOYSTICK_TURN=controller_1.axis1

VALUE_DEADZONE=10
VALUE_SIDE="right"

BUTTON_CHAIN_FORWARD=controller_1.buttonL1
BUTTON_CHAIN_REVERSE=controller_1.buttonL2
BUTTON_EXTRA_MOTOR1=controller_1.buttonR1
BUTTON_EXTRA_MOTOR2=controller_1.buttonR2
BUTTON_FINGER=controller_1.buttonX

VALUE_MULTIPLIER_DRIVE=0.85
VALUE_MULTIPLIER_TURN=0.4
VALUE_MULTIPLIER_CHAIN=1
VALUE_FINGER_POSITION=1.4

VALUE_SINGLE_DEGREE=1597208273



# Variable to check whether the timer is currently runnning
isgoing = False
isfingerdown = True

def turn_degrees(d,wait=False):
    Right.set_position(0,TURNS)
    Left.set_position(0,TURNS)
    Right.spin_to_position((VALUE_SINGLE_DEGREE*d)/200000000000,TURNS,wait=False)
    Left.spin_to_position(0-(VALUE_SINGLE_DEGREE*d)/200000000000,TURNS,wait=wait)

def move_forward(inches,wait=False):
    Right.set_position(0,TURNS)
    Left.set_position(0,TURNS)
    Right.spin_to_position(0-(inches+1)/(4*pi),TURNS,wait=False)
    Left.spin_to_position(0-(inches+1)/(4*pi),TURNS,wait=wait)

def autonomous_old():
    Chain.set_velocity(100,PERCENT)
    Chain.spin(REVERSE)
    move_forward(10,True)
    wait(10, SECONDS)
    # turn_degrees(-90,True)

# If it ain't broke, don't fix it.
def autonomous():
    brain.screen.print("Auto running")
    fingercallback(False)
    move_forward(-36,True)
    fingercallback()
    #move_forward(2)
    Chain.set_velocity(100,PERCENT)
    Chain.spin(REVERSE)
    wait(3, SECONDS)
    Chain.spin(FORWARD)
    fingercallback()
    move_forward(20, True)
    fingercallback()
    Chain.stop()
    turn_degrees(75 if VALUE_SIDE=="right" else -75, True)
    move_forward(-30,True)

def deadzonify(inputvalue):
    # Make the input zero if the absolute value
    # is less than the deadzone.

    # Check the absolute value, so that small
    # NEGATIVE values are also ignored
    if abs(inputvalue)<VALUE_DEADZONE:
        # If it's less than the deadzone, make it zero.
        return 0
    # Otherwise, don't change it.
    return inputvalue
def fingercallback(wait=True):
    global isfingerdown
    isfingerdown=not isfingerdown
    Finger.set_velocity(100, PERCENT)
    if isfingerdown:
        Finger.spin_to_position(0, TURNS,wait=wait)
    else:
        Finger.stop()
        Finger.spin_to_position(-1*VALUE_FINGER_POSITION,TURNS,wait=wait)
fingercallback()
fingercallback()

#COCKROACH WAS HERE

extramotoron=False
def extramotor1():
    global extramotoron
    extramotoron=not extramotoron
    if extramotoron:
        Extra.spin(FORWARD)
    else:
        Extra.stop()
def extramotor2():
    global extramotoron
    extramotoron=not extramotoron
    if extramotoron:
        Extra.spin(REVERSE)
    else:
        Extra.stop()

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
    BUTTON_EXTRA_MOTOR1.released(extramotor1)
    BUTTON_EXTRA_MOTOR2.released(extramotor2)
    BUTTON_FINGER.released(fingercallback)
    JOYSTICK_DRIVE.changed(setaxis)
    JOYSTICK_TURN.changed(setaxis)
    # I really should make buttonB a constant, like BUTTON_TIMER
    # or something. And make the callbacks "timerpressed" instead
    # of "timerpressed"
    controller_1.buttonB.released(timerreleased)
    controller_1.buttonB.pressed(timerpressed)
    # Make the chain and string go the speed we've defined
    Chain.set_velocity(VALUE_MULTIPLIER_CHAIN*100,PERCENT)
    # Set left motor and right motor to zero, because of the note below.
    Left.set_velocity(0,PERCENT)
    Right.set_velocity(0,PERCENT)
    Extra.set_velocity(100,PERCENT)
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
    while competition.is_autonomous() or competition.is_driver_control():
        # While the timer is running,
        # display the timer value on the screen.
        if isgoing:
            controller_1.screen.clear_row(1)
            controller_1.screen.set_cursor(2,1)
            controller_1.screen.print(brain.timer.time(SECONDS))
        # Make sure the event loop doesn't get bogged down.
        wait(15,MSEC)

# Callback when any axis is changed
def setaxis():
    # includes drive multiplier AND overall mult
    drive_speed_multiplier=VALUE_MULTIPLIER_DRIVE
    # Position of the axis, taking deadzone into account
    axis_position=deadzonify(JOYSTICK_TURN.position())
    # Make the axis inverted, to fix an inverted driving issue we had
    updownpos=drive_speed_multiplier*(0-axis_position)

    # Includes turn multiplier AND overall mult
    turn_speed_multiplier=VALUE_MULTIPLIER_TURN
    # Position of the axis, taking deadzone into account
    axis_position=deadzonify(JOYSTICK_TURN.position())
    # Do the final computations, as above.
    leftrightpos=turn_speed_multiplier*axis_position

    # Make the motors carry out the rotation amounts we defined
    if True: #urandom.rand()>0.5:
        Left.set_velocity(updownpos+leftrightpos,PERCENT)
        Right.set_velocity(updownpos-leftrightpos,PERCENT)
    #else:
    #    Right.set_velocity(updownpos-leftrightpos,PERCENT)
    #    Left.set_velocity(updownpos+leftrightpos,PERCENT)
# Make sure the timer isn't started on press,
# and then stopped on the same release.
justchangedisgoing=False

# Callback when timer button pressed
def timerpressed():
    global isgoing,justchangedisgoing
    if isgoing:
        # Get ready and show how to time
        isgoing=False
        justchangedisgoing=True
        controller_1.screen.clear_screen()
        controller_1.screen.set_cursor(2,1)
        controller_1.screen.print(str(brain.timer.time(SECONDS)))
        controller_1.screen.set_cursor(1,1)
        controller_1.screen.print("Hold B for timer")
    else:
        # Display message showing how to start
        controller_1.screen.clear_screen()
        controller_1.screen.set_cursor(1,1)
        controller_1.screen.print("Let go of B to start!")

# Callback when timer button released
def timerreleased():
    global isgoing,justchangedisgoing
    if not isgoing:
        if justchangedisgoing:
            justchangedisgoing=False
        else:
            # Clear timer, and inform user how to stop.
            brain.timer.clear()
            controller_1.screen.set_cursor(1,1)
            controller_1.screen.print("Press B to stop")
            isgoing=True

# Make intake hold its position when stopped
Chain.set_stopping(HOLD)

wait(15,MSEC)

# Define the competition object so that the field
# can find our driver control and autonomous functions
competition = Competition(when_started, autonomous)
