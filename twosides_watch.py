import time,os
while 1:
    c=open("main.py").read()
    while 1:
        new=open("main.py").read()
        time.sleep(5)
        new2=open("main.py").read()
        if new==new2 and new!=c:
            os.system("python twosides.py")
            break