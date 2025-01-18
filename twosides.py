import os

def do(side):
    main=open("main.py").read()
    if side=="l":
        main=main.replace('AUTO_SIDE="right"','AUTO_SIDE="left"')
    else:
        main=main.replace('AUTO_SIDE="left"','AUTO_SIDE="right"')

    import json
    vex=json.load(open(".vscode/vex_project_settings.json"))
    vex["project"]["name"]="Left" if side=="l" else "Right"
    vex["project"]["slot"]=1 if side=="l" else 2

    print("Left" if side=="l" else "Right","configured.")

    json.dump(vex,open(".vscode/vex_project_settings.json","w"))


do("l")
print("Uploading left/slot 1")
open("Left.py","w").write(open("main.py").read())
os.system("c:\\Users\\kwate\\.vscode\\extensions\\vexrobotics.vexcode-0.6.1\\resources\\tools\\vexcom\\win32\\vexcom.exe --slot 1 --write Left.py --icon 2 COM3 --progress")
do("r")
print("Uploading right/slot 2")
open("Right.py","w").write(open("main.py").read())
os.system("c:\\Users\\kwate\\.vscode\\extensions\\vexrobotics.vexcode-0.6.1\\resources\\tools\\vexcom\\win32\\vexcom.exe --slot 2 --write Right.py --icon 2 COM3 --progress")
os.remove("Left.py")
os.remove("Right.py")