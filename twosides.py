import os,winsound

def do(side):
    main=open("main.py").read()
    if side=="l":
        main=main.replace('self.VALUE_SIDE="right"','self.VALUE_SIDE="left"')
    else:
        main=main.replace('self.VALUE_SIDE="left"','self.VALUE_SIDE="right"')
    open("main.py","w").write(main)
    print("Left" if side=="l" else "Right","configured.")

success=True
winsound.Beep(500,500)
do("l")
print("Uploading left/slot 1")
open(".gitignored/Left.py","w").write(open("main.py").read())
r=os.system("c:\\Users\\kwate\\.vscode\\extensions\\vexrobotics.vexcode-0.6.1\\resources\\tools\\vexcom\\win32\\vexcom.exe --slot 1 --write .gitignored/Left.py --progress")
if r==0:
    winsound.Beep(600,500)
else:
    winsound.Beep(400,500)
    success=False
os.remove(".gitignored/Left.py")
print("\n")
do("r")
print("Uploading right/slot 2")
open(".gitignored/Right.py","w").write(open("main.py").read())
r=os.system("c:\\Users\\kwate\\.vscode\\extensions\\vexrobotics.vexcode-0.6.1\\resources\\tools\\vexcom\\win32\\vexcom.exe --slot 2 --write .gitignored/Right.py --progress")
os.remove(".gitignored/Right.py")
if r==0:
    winsound.Beep(600,500)
else:
    winsound.Beep(400,500)
    success=False
exit(int(success))