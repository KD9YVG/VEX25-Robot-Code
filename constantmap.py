import json

class Constant:
    def __init__(self):
        pass
    def __getattr__(self,name):
        setattr(self,name,Constant())
        return getattr(self,name)

def code(c):
    return {"type":"code","data":c}

CONST=Constant()
CONST.JOYSTICK.DRIVE=code("controller_1.axis3")
CONST.JOYSTICK.TURN=code("controller_1.axis1")

CONST.VALUE.DEADZONE=10
CONST.VALUE.SIDE="right"

CONST.BUTTON.CHAIN.FORWARD=code("controller_1.buttonL1")
CONST.BUTTON.CHAIN.REVERSE=code("controller_1.buttonL2")
CONST.BUTTON.EXTRA.BUTTON1=code("controller_1.buttonR1")
CONST.BUTTON.EXTRA.BUTTON2=code("controller_1.buttonR2")
CONST.BUTTON.FINGER=code("controller_1.buttonX")

CONST.VALUE.MULTIPLIER.DRIVE=0.85
CONST.VALUE.MULTIPLIER.TURN=0.4
CONST.VALUE.MULTIPLIER.CHAIN=1
CONST.VALUE.FINGER_POSITION=1.4

CONST.VALUE.SINGLE_DEGREE=1597208273

def gen_map(c):
    if type(c)==Constant:
        map="{"
        for i in c.__dict__:
            map+=repr(i)
            map+=":"
            map+=gen_map(c.__dict__[i])
            map+=","
        map=map[:-1]+"}"
    elif type(c)==dict:
        if c["type"]=="code":
            return c["data"]
    else:
        return repr(c)
    return map

print(gen_map(CONST))