
from vex import *
from math import pi

# commentformat off
import urandom # type: ignore
# commentformat on

def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

class CycloneRobotState:
    def __init__(self) -> None:
        self.isTimerRunning=False
        self.isFingerDown=True
        self.extramotoron=False
        self.changedIsTimerRunning=False
        self.timerdisplay=0.0
class CycloneRobotCodeApp:
    def __init__(self) -> None:
        self.brain=Brain()
        self.controller_1 = Controller(PRIMARY)
        self.Left = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
        self.Right = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
        self.Chain = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
        self.Finger = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
        self.Extra = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
        wait(30, MSEC)
        self.initializeRandomSeed()
        # add a small delay to make sure we don't print in the middle of the REPL header
        wait(200, MSEC)
        # clear the console to make sure we don't have the REPL in the console
        print("\033[2J")
        self.initialize_constants()
        self.state=CycloneRobotState()
    def initialize_constants(self):
        self.JOYSTICK_DRIVE=self.controller_1.axis3
        self.JOYSTICK_TURN=self.controller_1.axis1

        self.VALUE_DEADZONE=10
        self.VALUE_SIDE="right"

        self.BUTTON_CHAIN_FORWARD=self.controller_1.buttonL1
        self.BUTTON_CHAIN_REVERSE=self.controller_1.buttonL2
        self.BUTTON_EXTRA_MOTOR1=self.controller_1.buttonR1
        self.BUTTON_EXTRA_MOTOR2=self.controller_1.buttonR2
        self.BUTTON_FINGER=self.controller_1.buttonX

        self.VALUE_MULTIPLIER_DRIVE=0.85
        self.VALUE_MULTIPLIER_TURN=0.4
        self.VALUE_MULTIPLIER_CHAIN=1
        self.VALUE_FINGER_POSITION=1.8

        self.VALUE_SINGLE_DEGREE=1597208273
    def initializeRandomSeed(self):
        wait(100, MSEC)
        random = self.brain.battery.voltage(MV) + self.brain.battery.current(CurrentUnits.AMP) * 100 + self.brain.timer.system_high_res()
        urandom.seed(int(random))
    def turn_degrees(self,d,wait=False):
        self.Right.set_position(0,TURNS)
        self.Left.set_position(0,TURNS)
        self.Right.spin_to_position((self.VALUE_SINGLE_DEGREE*d)/200000000000,TURNS,wait=False)
        self.Left.spin_to_position(0-(self.VALUE_SINGLE_DEGREE*d)/200000000000,TURNS,wait=wait)
    def move_forward(self,inches,wait=False):
        self.Right.set_position(0,TURNS)
        self.Left.set_position(0,TURNS)
        self.Right.spin_to_position(0-(inches+1)/(4*pi),TURNS,wait=False)
        self.Left.spin_to_position(0-(inches+1)/(4*pi),TURNS,wait=wait)
    def autonomous(self):
        self.move_forward(-9,True)
        self.turn_degrees(-90,True)
        self.move_forward(-15,True)
        self.turn_degrees(-40,True)
        self.Left.set_velocity(53,PERCENT)
        self.Right.set_velocity(50,PERCENT)
        self.Left.spin(FORWARD)
        self.Right.spin(FORWARD)
        wait(3,SECONDS)
        self.Left.set_velocity(53,PERCENT)
        self.Right.set_velocity(50,PERCENT)
        self.Left.spin(REVERSE)
        self.Right.spin(REVERSE)
        wait(3,SECONDS)
        self.turn_degrees(180,True)
        self.move_forward(-15,True)
        self.turn_degrees(40,True)
        self.Left.set_velocity(53,PERCENT)
        self.Right.set_velocity(50,PERCENT)
        self.Left.spin(FORWARD)
        self.Right.spin(FORWARD)
        wait(2,SECONDS)
        self.Left.set_velocity(50,PERCENT)
        self.Right.set_velocity(50,PERCENT)
        self.Left.spin(REVERSE)
        self.Right.spin(REVERSE)
        wait(1,SECONDS)
        self.Left.stop()
        self.Right.stop()
    def deadzonify(self,inputvalue):
        # Make the input zero if the absolute value
        # is less than the deadzone.

        # Check the absolute value, so that small
        # NEGATIVE values are also ignored
        if abs(inputvalue)<self.VALUE_DEADZONE:
            # If it's less than the deadzone, make it zero.
            return 0
        # Otherwise, don't change it.
        return inputvalue
    def fingercallback(self,wait=True):
        self.state.isFingerDown=not self.state.isFingerDown
        self.Finger.set_velocity(100, PERCENT)
        if self.state.isFingerDown:
            self.Finger.stop()
            self.Finger.spin_to_position(-1*self.VALUE_FINGER_POSITION,TURNS,wait=wait)
        else:
            self.Finger.spin_to_position(0, TURNS,wait=wait)
    def extramotor1(self):
        self.state.extramotoron=not self.state.extramotoron
        if self.state.extramotoron:
            self.Extra.spin(FORWARD)
        else:
            self.Extra.stop()
    def extramotor2(self):
        self.state.extramotoron=not self.state.extramotoron
        if self.state.extramotoron:
            self.Extra.spin(REVERSE)
        else:
            self.Extra.stop()
    def when_started(self):
        if self.controller_1.buttonY.pressing():
            if self.controller_1.buttonX.pressing():
                self.state.isFingerDown=False
                self.Finger.set_position(0,TURNS)
                self.fingercallback()
            elif self.controller_1.buttonB.pressing():
                self.state.isFingerDown=True
                self.Finger.set_position(-1*self.VALUE_FINGER_POSITION,TURNS)
                self.fingercallback()
            self.brain.program_stop()
        self.Chain.set_stopping(HOLD)
        self.controller_1.screen.clear_screen()
        self.controller_1.screen.set_cursor(1,1)
        self.controller_1.screen.print("Please wait")
    def driver_control(self):
        # Clear the screen and tell the user
        # how to start the timer.
        self.timerpressed()
        self.timerreleased()
        self.timerpressed()
        self.timerreleased()
        # Add callbacks for each button and axis
        self.BUTTON_CHAIN_FORWARD.pressed(lambda: self.Chain.spin(FORWARD))
        self.BUTTON_CHAIN_FORWARD.released(self.Chain.stop)
        self.BUTTON_CHAIN_REVERSE.pressed(lambda: self.Chain.spin(REVERSE))
        self.BUTTON_CHAIN_REVERSE.released(self.Chain.stop)
        self.BUTTON_EXTRA_MOTOR1.released(self.extramotor1)
        self.BUTTON_EXTRA_MOTOR2.released(self.extramotor2)
        self.BUTTON_FINGER.released(self.fingercallback)
        self.JOYSTICK_DRIVE.changed(self.setaxis)
        self.JOYSTICK_TURN.changed(self.setaxis)
        # I really should make buttonB a constant, like BUTTON_TIMER
        # or something. And make the callbacks "timerpressed" instead
        # of "timerpressed"
        self.controller_1.buttonB.released(self.timerreleased)
        self.controller_1.buttonB.pressed(self.timerpressed)
        # Make the chain and string go the speed we've defined
        self.Chain.set_velocity(self.VALUE_MULTIPLIER_CHAIN*100,PERCENT)
        # Set left motor and right motor to zero, because of the note below.
        self.Left.set_velocity(0,PERCENT)
        self.Right.set_velocity(0,PERCENT)
        self.Extra.set_velocity(100,PERCENT)
        # When the left and right motors
        # are moving, we need to set_velocity to
        # the controller's input percentage.
        # When the controller is moved, the velocity
        # is changed. The easiest way to do this
        # is to make it always "on", just at 0%.
        self.Left.spin(REVERSE)
        self.Right.spin(FORWARD)
        # Finger should brake when not being moved.
        self.Finger.set_stopping(BRAKE)
        while self.competition.is_autonomous() or self.competition.is_driver_control():
            # While the timer is running,
            # display the timer value on the screen.
            if self.controller_1.buttonA.pressing():
                self.VALUE_MULTIPLIER_DRIVE=200
            else:
                self.VALUE_MULTIPLIER_DRIVE=0.85
            self.controller_1.screen.clear_row(1)
            self.controller_1.screen.set_cursor(1,1)
            if self.state.isTimerRunning:
                self.controller_1.screen.print("B -> stop timer")
                self.state.timerdisplay=self.brain.timer.time(SECONDS)
                self.controller_1.screen.set_cursor(2,1)
                self.controller_1.screen.clear_row(2)
                self.controller_1.screen.print(self.state.timerdisplay)
            else:
                self.controller_1.screen.print("Timer off")
                self.controller_1.screen.set_cursor(2,1)
                self.controller_1.screen.clear_row(2)
                self.controller_1.screen.print(self.state.timerdisplay)
            self.controller_1.screen.set_cursor(3,1)
            self.controller_1.screen.clear_row(3)
            if self.state.isFingerDown:
                self.controller_1.screen.print("Finger open  v")
            else:
                self.controller_1.screen.print("Finger closed ^")
            print(self.Left.temperature())
            print(self.Right.temperature())
            print(self.Chain.temperature())
            print("\n\n\n")
            # Make sure the event loop doesn't get bogged down.
            wait(15,MSEC)
    def setaxis(self):
        # includes drive multiplier AND overall mult
        drive_speed_multiplier=self.VALUE_MULTIPLIER_DRIVE
        # Position of the axis, taking deadzone into account
        axis_position=self.deadzonify(self.JOYSTICK_DRIVE.position())
        # Make the axis inverted, to fix an inverted driving issue we had
        updownpos=drive_speed_multiplier*(0-axis_position)

        # Includes turn multiplier AND overall mult
        turn_speed_multiplier=self.VALUE_MULTIPLIER_TURN
        # Position of the axis, taking deadzone into account
        axis_position=self.deadzonify(self.JOYSTICK_TURN.position())
        # Do the final computations, as above.
        leftrightpos=turn_speed_multiplier*axis_position

        # Make the motors carry out the rotation amounts we defined
        if True: #urandom.rand()>0.5:
            self.Left.set_velocity(updownpos+leftrightpos,PERCENT)
            self.Right.set_velocity(updownpos-leftrightpos,PERCENT)
    def timerpressed(self):
        if self.state.isTimerRunning:
            self.state.isTimerRunning=False
            self.state.changedIsTimerRunning=True
            self.controller_1.screen.clear_screen()
            self.controller_1.screen.set_cursor(2,1)
            self.state.timerdisplay=self.brain.timer.time(SECONDS)
            self.controller_1.screen.set_cursor(1,1)
        else:
            self.state.timerdisplay=0
            self.controller_1.screen.clear_screen()
            self.controller_1.screen.set_cursor(1,1)
            self.controller_1.screen.print("Let go of B to start!")
    def timerreleased(self):
        if not self.state.isTimerRunning:
            if self.state.changedIsTimerRunning:
                self.state.changedIsTimerRunning=False
            else:
                self.brain.timer.clear()
                self.controller_1.screen.set_cursor(1,1)
                self.controller_1.screen.print("Press B to stop")
                self.state.isTimerRunning=True
    def register_competition(self):
        self.when_started()
        self.competition = Competition(self.autonomous, self.autonomous)
def main():
    RobotApp=CycloneRobotCodeApp()
    RobotApp.register_competition()
wait(15,MSEC)
print(__name__)
if __name__=="__main__":
    main()