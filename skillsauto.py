
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
        wait(30, MSEC)
        self.initializeRandomSeed()
        # add a small delay to make sure we don't print in the middle of the REPL header
        wait(200, MSEC)
        # clear the console to make sure we don't have the REPL in the console
        print("\033[2J")
        self.initialize_constants()
        self.state=CycloneRobotState()
    def initialize_constants(self):
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
        wait(2.67,SECONDS)
        self.Left.stop()
        self.Right.stop()
        self.move_forward(15,True)
        self.turn_degrees(-60,True)
        self.move_forward(-40,True)
        self.move_forward(25,True)
        self.turn_degrees(-150,True)
        self.move_forward(40,True)
        self.Left.set_velocity(54,PERCENT)
        self.Right.set_velocity(56,PERCENT)
        self.Left.spin(FORWARD)
        self.Right.spin(FORWARD)
        wait(8,SECONDS)
        self.Left.stop()
        self.Right.stop()
    def unusedfunction_imtoolazytocomment(self):
        self.Left.set_velocity(50,PERCENT)
        self.turn_degrees(90,True)
        self.move_forward(-10,True)
        self.turn_degrees(90,True)
        self.move_forward(-15,True)
        self.turn_degrees(45,True)
        self.Left.set_velocity(45,PERCENT)
        self.Right.set_velocity(60,PERCENT)
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
    def fingercallback(self,wait=True):
        self.state.isFingerDown=not self.state.isFingerDown
        self.Finger.set_velocity(100, PERCENT)
        if self.state.isFingerDown:
            self.Finger.stop()
            self.Finger.spin_to_position(-1*self.VALUE_FINGER_POSITION,TURNS,wait=wait)
        else:
            self.Finger.spin_to_position(0, TURNS,wait=wait)
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
        self.controller_1.screen.print("Skills auto")
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