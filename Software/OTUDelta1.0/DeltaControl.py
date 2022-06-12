from tkinter import *
from PIL import ImageTk,Image

#####################################
realBot = True
#####################################


import kinematicsSolver as kin;
import time
import numpy as np
import os

deltaKin = kin.deltaSolver();
pi = np.pi #3.1415927

root = Tk()
root.title("Delta Robot Control Panel")
if "nt" == os.name:
    root.wm_iconbitmap(bitmap = "logo.ico")
else:
    root.wm_iconbitmap(bitmap = "@logo1.xbm")

brandImg = ImageTk.PhotoImage(Image.open("brand.png"))
ImgLabel = Label(image=brandImg, width=800, borderwidth=25)
#ImgLabel.pack()
ImgLabel.grid(row=0, column=0, columnspan=5)

firstText = Label(root, text="Enter Z value:")
firstText.grid(row=1, column=0, columnspan =3, padx=0, pady=10)
a = Entry(root, width=10, borderwidth=5, fg="blue")
a.grid(row=1, column=1, columnspan=2, padx=0, pady=10)
#a.pack()
a.insert(0, "0") #insert text into the box

secondText = Label(root, text="Enter X value:")
secondText.grid(row=3, column=0, columnspan =3, padx=0, pady=10)
b = Entry(root, width=10, borderwidth=5, fg="blue")
b.grid(row=3, column=1, columnspan=2, padx=0, pady=10)
#b.pack()
b.insert(0, "0")

thirdText = Label(root, text="Enter Y value:")
thirdText.grid(row=5, column=0, columnspan =3, padx=165, pady=10)
c = Entry(root, width=10, borderwidth=5, fg="blue")
c.grid(row=5, column=1, columnspan=2, padx=0, pady=10)
#c.pack()
c.insert(0, "0")

velText = Label(root, text="Enter Velocity value:")
velText.grid(row=7, column=0, columnspan =3, padx=0, pady=10)
vel = Entry(root, width=10, borderwidth=5, fg="blue")
vel.grid(row=7, column=1, columnspan=2, padx=0, pady=10)
#c.pack()
vel.insert(0, "2")

accText = Label(root, text="Enter Accerlartion value:")
accText.grid(row=9, column=0, columnspan =3, padx=220, pady=10)
acc = Entry(root, width=10, borderwidth=5, fg="blue")
acc.grid(row=9, column=1, columnspan=2, padx=0, pady=10)
#c.pack()
acc.insert(0, "5")

def connect():
    import robot212_odrive

def calibration():
    import odrive
    from odrive.enums import AXIS_STATE_IDLE, AXIS_STATE_CLOSED_LOOP_CONTROL, AXIS_STATE_FULL_CALIBRATION_SEQUENCE
    import time
    import math
    odrive0 = ('20583883304E')
    odrive1 = ('205739824D4D')


    print("finding odrives...")
    odrv0 = odrive.find_any(serial_number = odrive0)
    odrv1 = odrive.find_any(serial_number = odrive1)
    print("starting calibration all axises ...")
    odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
    odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
    odrv1.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

    while odrv0.axis0.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)

    odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv1.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

    time.sleep(0.5)

    shadow_count0 = odrv0.axis0.encoder.shadow_count
    shadow_count1 = odrv0.axis1.encoder.shadow_count
    shadow_count2 = odrv1.axis0.encoder.shadow_count
    print("axis 0 encoder position is:  ",shadow_count0)
    print("axis 1 encoder position is:  ",shadow_count1)
    print("axis 2 encoder position is:  ",shadow_count2)

    if shadow_count0 >-50 and shadow_count0 <50 and shadow_count1>-50 and shadow_count1 <50 and shadow_count2 >-50 and shadow_count2 <50:

        odrv0.axis0.encoder.set_linear_count(14500)
        odrv0.axis1.encoder.set_linear_count(13500)
        odrv1.axis0.encoder.set_linear_count(14500)
        print ("Calibration Finished")
    else:
        print ("repeat reboot!")

def reboot():

    import odrive
    odrv0 = ('20583883304E')
    odrv1 = ('205739824D4D')
    print("finding an Odrive0...")
    odrive0 = odrive.find_any(serial_number = odrv0)
    print("finding an Odrive1...")
    odrive1 = odrive.find_any(serial_number = odrv1)

    try:
        odrive0.reboot()
    except:
        print('Rebooted 0')
    try:
        odrive1.reboot()
    except:
        print('Rebooted 1')
    # odrive0.reboot()
    # print("rebooted 0")
    # odrive1.reboot()
    # bot.reboot_all()
    print('Now Ready to Calibrate')

def home():
    if realBot:
        import robot212_odrive as bot
    else:
        import robot212_virtual as bot

    thetas = deltaKin.IK((0,0,deltaKin.z))
    bot.trajMoveRad((thetas),0.5,0.5)

def quit():
    root.quit()

def go():
    if realBot:
        import robot212_odrive as bot
    else:
        import robot212_virtual as bot

    z = float(a.get())
    x = float(b.get())
    y = float(c.get())
    velocity = float(vel.get())
    acceleration = float(acc.get())
    thetas = deltaKin.IK((x,y,z))
    bot.trajMoveRad((thetas),velocity,acceleration)





z_array = []
x_array = []
y_array = []
vel_array = []
acc_array = []


def save():

    z_array.append(a.get())

    x_array.append(b.get())

    y_array.append(c.get())

    vel_array.append(vel.get())

    acc_array.append(acc.get())

    # print(len(z_array))


def remove():
    count = len(x_array)
    for i in range(count-1):
        z_array.pop(i)
        x_array.pop(i)
        y_array.pop(i)





def play():
    import robot212_odrive as bot
    list = len(z_array)
    for i in range(list):
        z_float = float(z_array[i])
        x_float = float(x_array[i])
        y_float = float(y_array[i])
        vel_float = float(vel_array[i])
        acc_float = float(acc_array[i])
        thetas = deltaKin.IK((x_float,y_float,z_float))
        bot.trajMoveRad((thetas),vel_float,acc_float)
        time.sleep(1)

def arraylist():

    listz = z_array
    listx = x_array
    listy = y_array
    listvel = vel_array
    listacc = acc_array
    count = len(x_array)
    # print(count)
    for i in range(count):

        space = "||"
        text = listx[i], listy[i], listz[i],space, listvel[i], listacc[i]
    # for i in range(count):
        string = Label(root, text="  X  Y  Z  ||  Vel  Acc")
        list = Label(root, text=text)
        string.grid(row=13, column=1, columnspan=2, padx=10, pady=0)
        list.grid(row=14+i, column=1, columnspan=2, padx=10, pady=10)



def save_function():
    save()
    arraylist()
def remove_function():
    remove()
    arraylist()



# padx and pady for the size of the button, command is to execute function firstlabel (to print button clicked)
# fg is the color of the button text, bg is the background color of the button (can use hex color code)
#firstButton.grid(row=1, column=0)
firstButton = Button(root, text="Go to Position", padx=16, pady=10, command=go, fg="#111E87", bg="#FB732A")
#firstButton.pack()
firstButton.grid(row=1, column=2, columnspan=3, padx=10, pady=5)

homeButton = Button(root, text="Home", padx=16, pady=10, command=home, fg="#111E87", bg="#FB732A")
#firstButton.pack()
homeButton.grid(row=3, column=2, columnspan=3, padx=10, pady=5)

addButton = Button(root, text="Add Point", padx=16, pady=10, command=save_function, fg="#111E87", bg="#FB732A")
#firstButton.pack()
addButton.grid(row=5, column=2, columnspan=3, padx=10, pady=5)

removeButton = Button(root, text="Remove Point", padx=16, pady=10, command=remove_function, fg="#111E87", bg="#FB732A")
#firstButton.pack()
removeButton.grid(row=7, column=2, columnspan=3, padx=10, pady=5)

playButton = Button(root, text="Play", padx=16, pady=10, command=play, fg="#111E87", bg="#FB732A")
#firstButton.pack()
playButton.grid(row=9, column=2, columnspan=3, padx=10, pady=5)

secondButton = Button(root, text="Calibrate", padx=16, pady=10, command=calibration, fg="#111E87", bg="#FB732A")
#secondButton.pack()
secondButton.grid(row=1, column=0, columnspan=1, padx=0, pady=5)

thirdButton = Button(root, text="Connect", padx=16, pady=10, command=connect, fg="#111E87", bg="#FB732A")
#thirdButton.pack()
thirdButton.grid(row=3, column=0, columnspan=1, padx=0, pady=5)

fourthButton = Button(root, text="Reboot", padx=16, pady=10, command=reboot, fg="#111E87", bg="#FB732A")
#thirdButton.pack()
fourthButton.grid(row=5, column=0, columnspan=1, padx=0, pady=5)

quitButton = Button(root, text="Exit Program", command=quit)
#quitButton.pack()
quitButton.grid(row=11, column=1, columnspan=2, padx=10, pady=5)


root.mainloop()

