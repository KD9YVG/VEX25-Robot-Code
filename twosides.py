import os

def do(side):
    main=open("main.py").read()
    if side=="l":
        main=main.replace('AUTO_SIDE="right"','AUTO_SIDE="left"')
    else:
        main=main.replace('AUTO_SIDE="left"','AUTO_SIDE="right"')

    print("Left" if side=="l" else "Right","configured.")


do("l")
print("Uploading left/slot 1")
open("Left.py","w").write(open("main.py").read())
os.system("c:\\Users\\kwate\\.vscode\\extensions\\vexrobotics.vexcode-0.6.1\\resources\\tools\\vexcom\\win32\\vexcom.exe --slot 1 --write Left.py COM3 --progress")
do("r")
print("Uploading right/slot 2")
open("Right.py","w").write(open("main.py").read())
os.system("c:\\Users\\kwate\\.vscode\\extensions\\vexrobotics.vexcode-0.6.1\\resources\\tools\\vexcom\\win32\\vexcom.exe --slot 2 --write Right.py COM3 --progress")
os.remove("Left.py")
os.remove("Right.py")