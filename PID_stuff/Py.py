# No

MIN_OUTPUT=5
I_MAX=100

class PidCtrl:
    def __init__(self):
        self.gainP=0
        self.gainI=0
        self.gainD=0
        
        self.integral=0
        self.lastInput=0

        self.target=0
        self.output=0

        self.log=False # nobody cares

clamp=lambda num,mini,maxi: min(max(num,mini),maxi)

clamp_motor=lambda e: e
def pid_update(ctrl,latest):

    error=ctrl.target-latest
    termP=ctrl.gainP*error
    ctrl.integral+=error
    # Clamp the integral value
    ctrl.integral=clamp(ctrl.integral, -I_MAX, I_MAX)
    termI=ctrl.gainI * ctrl.integral
    termD=ctrl.gainD * (latest - ctrl.lastInput)
    ctrl.lastInput=latest
    ctrl.output = clamp_motor(termP+termI-termD)
    if (abs(ctrl.output) < MIN_OUTPUT):

        ctrl.output=0

    if ctrl.log:
        pass # nobody cares