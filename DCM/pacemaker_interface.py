from tkinter import *
from tkinter import messagebox
import ast
from turtle import bgcolor
from matplotlib.pyplot import fill
from numpy import size
from pip import main
from pyparsing import col

# Egram imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

import serial
import struct
import platform
import time


root = Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg='#fff')
root.resizable(False, False)

def signin():
    username=user.get()
    password=code.get()

    global connection_status
    connection_status = 0
    
    file=open('datasheet.txt','r')
    d=file.read()
    r=ast.literal_eval(d)
    file.close()

#########################################################################
#---------------PACEMAKER PAGE-------------------------------------------
#########################################################################

    # Finds the username and password from the database necessary for login
    if username in r.keys() and password==r[username]:
        
        if platform.system() == 'Windows':
            frdm_port = 'COM4'
        else:
            frdm_port = "dev/tty.usbmodem0006210000001"
        try:
            # Open the serial port
            pacemaker = serial.Serial(frdm_port, 115200)
            print("Connected to pacemaker on port: " + frdm_port)
            connection_status = 1
        except:
            print("Could not open serial port")
            # exit()
            connection_status = 0
    
        def write_to_pacemaker(modename):
            # AOO
            if (modename == 0):
                cur_mode = 0
            # AAI
            elif (modename == 1):
                cur_mode = 1
            # VOO
            elif (modename == 2):
                cur_mode = 2
            # VVI
            else:
                cur_mode = 3       

            # Parameter Packing
            set = b'\x16'
            sync = b'\x55'
            lower_rate_limit = struct.pack("H", int(lrl.get()))
            atr_amp = struct.pack('f', int(apar.get()))
            vent_amp = struct.pack('f', int(vpar.get()))
            atr_pw = struct.pack("H", int(apw.get()))
            vent_pw = struct.pack("H", int(vpw.get()))
            atr_cmp_pwm = struct.pack("H", 75)
            vent_cmp_pwm = struct.pack("H", 75)
            vent_rp = struct.pack("H" ,int(vrp.get()))
            atr_rp = struct.pack("H", int(arp.get()))
            mode = struct.pack("H", cur_mode)

            Signal_set  = set  + lower_rate_limit + atr_amp + vent_amp + atr_pw + vent_pw + atr_cmp_pwm + vent_cmp_pwm +  vent_rp + atr_rp + mode
            Signal_echo = sync + lower_rate_limit + atr_amp + vent_amp + atr_pw + vent_pw + atr_cmp_pwm + vent_cmp_pwm +  vent_rp + atr_rp + mode

            pacemaker.write(Signal_set)		# Send the config to the pacemaker
            pacemaker.write(Signal_echo)	# Receive the config from the pacemaker

        #--------------------Reading Serial Data---------------

        def read_from_pacemaker():
            data = pacemaker.read(80)
            lrl_rev = int(struct.unpack('d', data[0:8])[0])
            atr_amp_rev = struct.unpack('d', data[8:16])[0]
            vent_amp_rev = struct.unpack('d', data[16:24])[0]
            atr_pw_rev = int(struct.unpack('d', data[24:32])[0])
            vent_pw_rev = int(struct.unpack('d', data[32:40])[0])
            atr_cmp_pwm_rev = int(struct.unpack('d', data[40:48])[0])
            vent_cmp_pwm_rev = int(struct.unpack('d', data[48:56])[0])
            vent_rp_rev = int(struct.unpack('d', data[56:64])[0])
            atr_rp_rev = int(struct.unpack('d', data[64:72])[0])
            mode_rev = int(struct.unpack('d', data[72:80])[0])

            print("From the board:")
            print("Lower Rate Limit = ", lrl_rev)
            print("ATR Amplitude = ", atr_amp_rev)
            print("VENT Amplitude = ", vent_amp_rev)
            print("ATR Pulse Width = ", atr_pw_rev)
            print("VENT Pulse Width = ", vent_pw_rev)
            print("ATR CMP PWM = ", atr_cmp_pwm_rev)
            print("VENT CMP PWM = ", vent_cmp_pwm_rev)
            print("ATR Refractory Period = ", atr_rp_rev)
            print("VENT Refractory Period = ", vent_rp_rev)
            print("Mode = ", mode_rev)

        #--------------------Egram Interface (Incomplete)---------------
        
        # Demonstrates that atr and vent data is retrieved from pacemaker
        def get_egram():
 
            pacemaker.write(b"\x66" + b"\x00"*24)
            data = pacemaker.read(80)
            atr_signal = struct.unpack('d', data[0:8])[0]
            vent_signal = struct.unpack('d', data[8:16])[0]
            print("ATR Signal = ", atr_signal)
            print("VENT Signal = ", vent_signal)           


        #     list_yA = []
        #     list_yV = []

        #     def getEgram(): 

        #         global count
                
        #         global list_yA
        #         global list_yV

        #         def egram():
                    
        #             count = 0

        #             pacemaker.write(b"\x66" + b"\x00"*24)
        #             data = pacemaker.read(80)
        #             atr_signal = struct.unpack('d', data[0:8])[0]
        #             vent_signal = struct.unpack('d', data[8:16])[0]
        #             print("ATR Signal = ", atr_signal)
        #             print("VENT Signal = ", vent_signal)

        #             list_yA = list_yA.append((atr_signal-0.5)*3.3)
        #             list_yV = list_yV.append((vent_signal-0.5)*3.3)

        #             count += 1

        #             x = [(count+j) for j in range(150)]
        #             axs[0].cla()
        #             axs[1].cla()
        #             axs[0].set_yticks([-4,-3.5,-3.0,-2.5,-2.0,-1.5,-1.0,-0.5,0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0])
        #             axs[0].set_ylim(-4, 4)
        #             axs[1].set_yticks([-4,-3.5,-3.0,-2.5,-2.0,-1.5,-1.0,-0.5,0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0])
        #             axs[1].set_ylim(-4, 4)
        #             axs[0].grid()
        #             axs[1].grid()
        #             axs[0].set_ylabel("Amplitude(mV)")
        #             axs[1].set_xlabel("Time(msec)")
        #             axs[1].set_ylabel("Amplitude(mV)")
        #             axs[0].plot(x, list_yA, c='r', label='Artial',linewidth=3.0)
        #             axs[1].plot(x, list_yV, c='b', label='Ventricular',linewidth=3.0)
        #             axs[0].set_title('Atrial')
        #             axs[1].set_title('Ventricular')

        #             fig, axs = plt.subplots(2)
        #             animate = animation.FuncAnimation(fig, egram, interval=150)
        #             plt.show()

        #--------------------Login Page---------------

        screen = Tk()           
        screen.geometry('1300x600')
        screen.title('Main')
         
        # Create a Button
        btn = Button(screen, text = 'Exit', bd = '5', command = screen.destroy)
        btn.pack(side = 'bottom')  


        # Title
        title = Label(screen, text="Pacemaker GUI", bg="#670000", fg="white")
        title.pack(side="top")
        title.config(font =("Courier", 14), justify="center")

        # Container for Parameters
        mainContainer = LabelFrame(screen, bg="#670000")
        mainContainer.pack(expand="yes", fill="both", side="bottom")

        #--------------------User Info---------------
        
        # Container for Current User Information
        userContainer = LabelFrame(mainContainer, text="User Info", bg="#670000", pady=5, font=("Courier", 15), fg="white")
        userContainer.grid(row = 1, column = 1, columnspan = 4, rowspan = 1)

        # Current User
        cur_user = Label(userContainer, text = "Username:  " + username, bg = "#670000", padx = 30, pady = 10, fg = "white")
        cur_user.grid(row = 1, column = 1)

        # Default current mode display
        cur_mode = Label(userContainer, text = "Current Mode: ", bg = "#670000", padx = 30, pady = 10, fg = "white")
        cur_mode.grid(row = 1, column = 4)

        #--------------------Workspace---------------

        #Container for Current Workspace Information
        workspaceContainer = LabelFrame(mainContainer, text="Workspace", bg="#670000", pady=5, font=("Courier", 15), fg="white")
        workspaceContainer.grid(row = 1, column = 4, columnspan = 5, rowspan = 1)

        # Current Workspace
        cur_workspace = Label(workspaceContainer, text = "Workspace:  ", bg = "#670000", padx = 20, pady = 10, fg = "white")
        cur_workspace.grid(row = 1, column = 1, columnspan=2)

        

        def changeData(self):
            if (value_inside.get() == "Add New Workspace"):
                newWorkspace['state'] = "normal"
            else:
                newWorkspace['state'] = "disabled"
                #print(value_inside.get())
                changeParamters(value_inside.get())

        def savedata():
            mode = modename['text']
            lrl_val = w1.get()
            url_val = w2.get()

            if ((int(lrl_val) < int(url_val)) and (mode != "")):
                if (value_inside.get() != "Add New Workspace"):
                    dataFile = open("datafile.txt", "r")
                    lines = dataFile.readlines()
                    dataFile.close()
                    dataFile = open("datafile.txt", "w")
                    for i in range(len(lines)):
                        line = lines[i].split()
                        lines.remove('\n')
                        for j in range(len(line)):
                            if (line[j] == value_inside.get()):
                                lines[i] = value_inside.get() + " " + getData(mode) + "\n"
                                
                                break

                    lines.remove("\n")                    
                    dataFile.writelines(lines)
                    dataFile.close()
                else:
                    if(newWorkspace.get() != ""):
                        dataFile = open("datafile.txt", "a")
                        dataFile.write("\n" + newWorkspace.get() + " " + getData(mode))
                        updateWorkspaceList(newWorkspace.get())
                        dataFile.close()
                    else:
                        print ("Enter a workspace name")

        def changeParamters(workspace):
            dataFile = open("datafile.txt", "r")
            line = dataFile.readline()
            line = line.split()
            while (line[0] != workspace):
                line = dataFile.readline()
                line = line.split()
            lrl.set(line[1])
            url.set(line[2])
            apar.set(line[3])
            apw.set(line[4])
            vpar.set(line[5])
            vpw.set(line[6])
            vrp.set(line[7])
            arp.set(line[8])
            if (line[9] == "OFF"):
                modetype(0)
            elif (line[9] == "AOO"):
                modetype(1)
            elif (line[9] == "VVI"):
                modetype(2)
            elif (line[9] == "VOO"):
                modetype(3)
            else:
                modetype(4)

        def updateWorkspaceList(newWorkspace):
            workspacesFile = open("workspacesList.txt", "r")
            wslist = workspacesFile.readline()
            workspacesFile.close()
            workspacesFile = open("workspacesList.txt", "w")
            workspacesFile.write(((wslist).rstrip('\n') + "," + newWorkspace))
            workspacesFile.close()
            workspacesFile = open("workspacesList.txt", "r")
            wslist2 = workspacesFile.readline()
            workspacesFile.close()
            wslist3 = wslist.split(",")
            print (wslist2)
            wslist3[-1] = wslist3[-1].strip()
            workspaceList[:] = wslist3[:]
                  
        # Options Menu for Workspace

        wsfile = open("workspacesList.txt", "r")
        line = wsfile.readline()
        workspaceList = line.split(",")
        workspaceList[-1] = workspaceList[-1].strip()
        wsfile.close()

        value_inside = StringVar(workspaceContainer)

        workspace_opmenu = OptionMenu(workspaceContainer, value_inside, *workspaceList, command=changeData)
        workspace_opmenu.grid(row = 1, column= 4, columnspan=2)

        #Create a New Workspace
        newWorkspaceValue = StringVar(workspaceContainer)
        newWorkspace = Entry(workspaceContainer, textvariable=newWorkspaceValue, bd=3, state=DISABLED)
        newWorkspace.grid(row=1, column=6, padx=10)

        

       

        # FIRST HALF OF PARAMETERS

        parmContainer = LabelFrame(mainContainer, text="Parameters", bg="#670000", pady=60, font=("Courier", 15), fg="white")
        parmContainer.grid(row=2, column=2, columnspan=8, rowspan=3)

        parm1 = Label(parmContainer, text="Lower Rate Limit (ppm)", bg="#670000", padx=65,  pady=10, fg="white")
        parm1.grid(row=1, column=2)

        lrl = DoubleVar(parmContainer)
        w1 = Spinbox(parmContainer, from_=30, to=175, bg="white", textvariable=lrl)
        w1.grid(row=2, column=2)

        parm2 = Label(parmContainer, text="Upper Rate Limit (ppm)", bg="#670000", padx=65,  pady=10, fg="white")
        parm2.grid(row=1, column=4)

        url = DoubleVar(parmContainer)
        w2 = Spinbox(parmContainer, from_=w1.get(), to=175, bg="white", textvariable=url)
        w2.grid(row=2, column=4)
    
        parm3 = Label(parmContainer, text="Atrial Pulse Amplitude Regulated (V) ", bg="#670000", padx=65,  pady=10, fg="white")
        parm3.grid(row=1, column=6)

        apar = DoubleVar(parmContainer)
        w3 = Spinbox(parmContainer, from_=0.1, to=5, increment=0.1, bg="white", textvariable=apar)
        w3.grid(row=2, column=6)

        parm4 = Label(parmContainer, text="Atrial Pulse Width (ms)", bg="#670000", padx=65,  pady=10, fg="white")
        parm4.grid(row=1, column=8)

        apw = DoubleVar(parmContainer)
        w4 = Spinbox(parmContainer, from_=1, to=30, increment=1, bg="white", textvariable=apw)
        w4.grid(row=2, column=8)

        # SECOND HALF OF PARAMETERS

        parm5 = Label(parmContainer, text="Ventricular Pulse Amplitude Regulated (V)", bg="#670000", padx=65,  pady=10, fg="white")
        parm5.grid(row=3, column=2)

        vpar = DoubleVar(parmContainer)
        w5 = Spinbox(parmContainer, from_=0.1, to=5, increment=0.1, bg="white", textvariable=vpar)
        w5.grid(row=4, column=2)

        parm6 = Label(parmContainer, text="Ventricular Pulse Width (ms)", bg="#670000", padx=65,  pady=10, fg="white")
        parm6.grid(row=3, column=4)

        vpw = DoubleVar(parmContainer)
        w6 = Spinbox(parmContainer, from_=1, to=30, increment=1, bg="white", textvariable=vpw)
        w6.grid(row=4, column=4)

        parm7 = Label(parmContainer, text="Ventricular Refractory Period (ms)", bg="#670000", padx=65,  pady=10, fg="white")
        parm7.grid(row=3, column=6)

        vrp = DoubleVar(parmContainer)
        w7 = Spinbox(parmContainer, from_=150, to=500, increment=10, bg="white", textvariable=vrp)
        w7.grid(row=4, column=6)


        parm8 = Label(parmContainer, text="Atrial Refractory Period (ms)", bg="#670000", padx=65,  pady=10, fg="white")
        parm8.grid(row=3, column=8)

        arp = DoubleVar(parmContainer)
        w8 = Spinbox(parmContainer, from_=150, to=500, increment=10, bg="white", textvariable=arp)
        w8.grid(row=4, column=8)
      
        # DCM and Device Connection

        # Container for Button
        dcm_device = Frame(mainContainer, bg="#670000", pady=60)
        dcm_device.grid(row=6, column=2)


        # Label
        dcm_device_label = Label(dcm_device, text = "DCM and Device Connection", bg="#670000", borderwidth=2, relief="flat", font =("Courier", 14), justify="center", fg="white")
        dcm_device_label.grid(row=7, column=2, sticky=W)


        def connection(widget,connection_status):
            if connection_status == 0:
                widget['bg'] = 'white'
                root.overrideredirect(1)
                root.withdraw()
                messagebox.showerror('Invalid','Please connect to a port')
                root.destroy()

            else:
                time.sleep(2)
                widget['bg'] = 'medium sea green'
                connect = Label(dcm_device, text="Connected", bg="#670000", padx=5,  pady=5, fg="white")
                connect.grid(row=7,column=4)


        frame = Frame(dcm_device, height=20, width=65)
        button = Button(dcm_device, text="  Connect ", bg="#670000", relief="groove", font =("Courier", 10), fg="white")
        button['command'] = lambda wgt=frame : connection(wgt, connection_status)
        no_connect = Label(dcm_device, text="No Connection", bg="#670000", padx=5,  pady=5, fg="white")
        no_connect.grid(row=7,column=4)

        frame.grid(row=7, column=3)
        button.grid(row=8, column=3)

        # When a DIFFERENT Pacemaker is approached than was previously interrogated

        #Container for Button
        pacemaker_type = Frame(mainContainer, bg="#670000", pady=30, borderwidth=2)
        pacemaker_type.grid(row=6, column=4)

        # Label
        lbl = Label(pacemaker_type, text = "Pacemaker Type: ", bg="#670000", borderwidth=2, relief="flat", font =("Courier", 14), justify="center", fg="white")
        lbl.grid(row=6, column=4, sticky=W)

        # Temporary button to show DCM and Device Connection
        def change_type(widget):
            if (widget['text'] == 'Pacemaker 2'):
                widget['text'] = 'Pacemaker 1'
            else:
                widget['text'] = 'Pacemaker 2'
    
        pacemaker_type_label = Label(pacemaker_type, text="Pacemaker 1", bg="#670000", font =("Courier", 14), justify="center", fg="white")

        pm_button = Button(pacemaker_type, text="Switch Pacemakers", bg="#670000", relief="groov", font=("Courier", 10), fg="white")
        pm_button['command'] = lambda wgt=pacemaker_type_label : change_type(wgt)

        pacemaker_type_label.grid(row=6, column=6)
        pm_button.grid(row=7, column=6)
 
        # MODES

        # Container for Button
        modes = LabelFrame(mainContainer, text="Modes", bg="#670000", pady=5, borderwidth=2, font=("Courier", 14), fg="white")
        modes.grid(row=6, column=6, columnspan=3, rowspan=3)

        modename = Label(mainContainer, text="")

        # OFF MODE BUTTON
        offbtn = Button(modes, text="OFF", relief="solid", font=("Courier", 10), fg="black", height=5, width=2, bg="white", padx=10)
        offbtn.grid(row=6, column=6, sticky=W, rowspan=2, padx=5)

        
        
        # When OFF is pressed, these modes are enabled/disabled
        def offmodes():
            w1['state'] = "disabled"
            w2['state'] = "disabled"
            w3['state'] = "disabled"
            w4['state'] = "disabled"
            w5['state'] = "disabled"
            w6['state'] = "disabled"
            w7['state'] = "disabled"
            w8['state'] = "disabled"
        
        def modetype(x):
            if (x == 0):
                modename['text'] = "OFF"
                cur_mode['text'] = "Current Mode: OFF" 

            elif (x == 1):
                modename["text"] = 'AOO'
                cur_mode['text'] = "Current Mode: AOO"

            elif (x == 2):
                modename["text"] = 'VVI'
                cur_mode['text'] = "Current Mode: VVI"

            elif (x == 3):
                modename["text"] = 'VOO'
                cur_mode['text'] = "Current Mode: VOO"

            else:
                modename["text"] = 'AAI'
                cur_mode['text'] = "Current Mode: AAI"


        offbtn['command'] = lambda x=0:[offmodes(),modetype(x)]


        frame.grid(row=7, column=3)
        button.grid(row=8, column=3)

        # AOO MODE BUTTON
        aoobtn = Button(modes, text="AOO", relief="solid", font=("Courier", 10), fg="black", height=2, width=3, bg="white", padx=10)
        aoobtn.grid(row=7, column=7, padx=5, pady=5)

        # When AOO is pressed, these modes are enabled/disabled
        def aoomodes():
            w1['state'] = "normal"
            w2['state'] = "normal"
            w3['state'] = "normal"
            w4['state'] = "disabled"
            w5['state'] = "normal"
            w6['state'] = "disabled"
            w7['state'] = "disabled"
            w8['state'] = "disabled"


        aoobtn['command'] = lambda x=1:[aoomodes(),modetype(x)]

        # VVI MODE BUTTON
        vvibtn = Button(modes, text="VVI", relief="solid", font=("Courier", 10), fg="black", height=2, width=3, bg="white", padx=10)
        vvibtn.grid(row=6, column=7, padx=5, pady=5)

        # When VVI is pressed, these modes are enabled/disabled
        def vvimodes():
            w1['state'] = "normal"
            w2['state'] = "normal"
            w3['state'] = "disabled"
            w4['state'] = "normal"
            w5['state'] = "disabled"
            w6['state'] = "normal"
            w7['state'] = "normal"
            w8['state'] = "disabled"


        vvibtn['command'] = lambda x=2:[vvimodes(),modetype(x)]

         # VOO MODE BUTTON
        voobtn = Button(modes, text="VOO", relief="solid", font=("Courier", 10), fg="black", height=2, width=3, bg="white", padx=10)
        voobtn.grid(row=6, column=8, padx=5, pady=5)

        # When VOO is pressed, these modes are enabled/disabled
        def voomodes():
            w1['state'] = "normal"
            w2['state'] = "normal"
            w3['state'] = "disabled"
            w4['state'] = "normal"
            w5['state'] = "disabled"
            w6['state'] = "normal"
            w7['state'] = "disabled"
            w8['state'] = "disabled"
           

        voobtn['command'] = lambda x=3:[voomodes(),modetype(x)]

        aaibtn = Button(modes, text="AAI", relief="solid", font=("Courier", 10), fg="black", height=2, width=3, bg="white", padx=10)
        aaibtn.grid(row=7, column=8, padx=5, pady=5)

        def aaimodes():
            w1['state'] = "normal"
            w2['state'] = "normal"
            w3['state'] = "normal"
            w4['state'] = "disabled"
            w5['state'] = "normal"
            w6['state'] = "disabled"
            w7['state'] = "disabled"
            w8['state'] = "normal"


        aaibtn['command'] = lambda x=4:[aaimodes(),modetype(x)]


        def senddata():
            
            if (modename['text'] == "AAI"):
                data = w1.get() + " " + w2.get() + " " + w3.get() + " " + "0" + " " + w5.get() + " " + "0" + " " + "0" + " " + w8.get() + " " + modename['text']
                write_to_pacemaker(1)

            elif (modename['text'] == "AOO"):
                data = w1.get() + " " + w2.get() + " " + w3.get() + " " + "0" + " " + w5.get() + " " + "0" + " " + "0" + " " + "0" + " " + modename['text']
                write_to_pacemaker(0)

            elif (modename['text'] == "VOO"):
                data = w1.get() + " " + w2.get() + " " + "0" + " " + w4.get() + " " + '0' + " " + w6.get() + " " + "0" + " " + "0" + " " + modename['text']
                write_to_pacemaker(2)

            elif (modename['text'] == "VVI"):
                data = w1.get() + " " + w2.get() + " " + '0' + " " + w4.get() + " " + "0" + " " + w6.get() + " " + w7.get() + " " + "0" + " " + modename['text']
                write_to_pacemaker(3)

            else:
                data = "0 0 0 0 0 0 0 0 " + modename['text']

            print (data)
        
        def getData(mode):
            # ser = serial.Serial('COM3')
            if (mode == "AAI"):
                data = w1.get() + " " + w2.get() + " " + w3.get() + " " + "0" + " " + w5.get() + " " + "0" + " " + "0" + " " + w8.get() + " " + modename['text']

            elif (mode == "AOO"):
                data = w1.get() + " " + w2.get() + " " + w3.get() + " " + "0" + " " + w5.get() + " " + "0" + " " + "0" + " " + "0" + " " + modename['text']

            elif (mode == "VOO"):
                data = w1.get() + " " + w2.get() + " " + "0" + " " + w4.get() + " " + '0' + " " + w6.get() + " " + "0" + " " + "0" + " " + modename['text']

            elif (mode == "VVI"):
                data = w1.get() + " " + w2.get() + " " + '0' + " " + w4.get() + " " + "0" + " " + w6.get() + " " + w7.get() + " " + "0" + " " + modename['text']
                
            else:
                data = "0 0 0 0 0 0 0 0 " + modename['text']

            return (data)    
                    
           
        egrambutton = Button(parmContainer, text="Egram", bg="#670000", relief="groove", font =("Courier", 10), fg="white", command = get_egram)
        egrambutton.grid(row=1, column=5)

        sendbutton = Button(parmContainer, text="Send", bg="#670000", relief="groove", font =("Courier", 10), fg="white", command = senddata)
        sendbutton.grid(row=2, column=5)

        savebutton = Button(parmContainer, text="Save", bg="#670000", relief="groove", font =("Courier", 10), fg="white", command = savedata)
        savebutton.grid(row=3, column=5)

        screen.mainloop()

    else:
        messagebox.showerror('Invalid','invalid username or password')

#########################################################################
#---------------END OF PACEMAKER PAGE------------------------------------
#########################################################################

#########################################################################
#---------------SIGNUP PAGE----------------------------------------------
#########################################################################

def signup_command():

    window=Toplevel(root)
    window.title('SignUp')
    window.geometry('925x500+300+200')
    window.configure(bg='#fff')
    window.resizable(False, False)

    # Implementation for writing user information to database
    def signup():

        # Obtains all input from user
        username=user.get()
        password=code.get()
        verify_password=verify.get()

        invalid_flag = 0
        invalid_password_flag = 0
        duplicate_user_flag = 0

        # Checks if the username has any special characters
        for i in range(len(username)):

            # Uses method ".isalnum()" to determine if the string contains A-Z and 0-9 without any special characters or spaces
            username_flag = username[i].isalnum()

            if (username_flag == False):
                invalid_flag += 1
            else:
                i += 1

         # Checks if the password has any spaces
        for i in range(len(password)):

            if (password[i] == " "):
                invalid_password_flag += 1
            else:
                i += 1
        
         # Checks if the verified password has any spaces
        for i in range(len(verify_password)):

            if (verify_password[i] == " "):
                invalid_password_flag += 1
            else:
                i += 1

        # Checks if username satisfies 4-25 character limit
        if (len(username) >= 4 and len(username) <= 25):

            # Checks if all user input is valid and contains no special characters or spaces 
            if (invalid_flag == 0):

                # Checks if the password contains any spaces 
                if (invalid_password_flag == 0):

                    # Checks if both passwords match
                    if (password == verify_password):

                        try:

                            file = open('datasheet.txt','r+')
                            d = file.read()
                            r = ast.literal_eval(d)

                            temp_file = open('datasheet.txt')
                            temp_r = ast.literal_eval(temp_file.read())
                            temp_file.close()

                            dict2 = {username:password}
                            r.update(dict2)
                            file.truncate(0)
                            file.close()

                            # Gets number of active users before anything is set to the database
                            num_users = len(r)

                            # Checks if user limit is at 10
                            if (num_users < 11):

                                # Checks if the username is a duplicate
                                if username in temp_r:
                                    duplicate_user_flag = 1
                                    messagebox.showerror('Invalid','This username already exists')

                                else:
                                    # Writing new user information to database
                                    file = open('datasheet.txt','w')
                                    w = file.write(str(r))

                                    messagebox.showinfo('Signup','Successfully signed up!')
                                    window.destroy()
                            else:
                                messagebox.showerror('Invalid','User limit has been reached (10)')
                                window.destroy()
                        except:
                            file=open('datasheet.txt','w')
                            pp = str({'Username':'password'})
                            file.write(pp)
                            file.close()
                    else:
                        messagebox.showerror('Invalid','Verified password does not match')
                        window.destroy()

                    # If duplicate user is detected, textfile is rewritten only when empty
                    if (duplicate_user_flag == 1):
                        file = open('datasheet.txt', 'w')
                        file.write(str(temp_r))
                        file.close()
                else:
                    messagebox.showerror('Invalid','Your password cannot contain any spaces')
                    window.destroy()
            else:
                messagebox.showerror('Invalid','Your username cannot contain any special characters or spaces')
                window.destroy()        
        else:
            messagebox.showerror('Invalid','Your username must contain 4-25 characters')
            window.destroy()

    def sign():
        window.destroy()

    # Pacemaker logo display
    img = PhotoImage(file = 'images\pace-logo.png')
    Label(window, image=img, bg='white').place(x=10,y=50)

    frame = Frame(window,width=500,height=500,bg="white")
    frame.place(x=480,y=70)

    heading=Label(frame,text='Sign up',fg='maroon',bg='white',font=('Microsoft YaHei UI Regular',23,'bold'))
    heading.place(x=110,y=0)


    def on_enter(e):
        user.delete(0,'end')

    def on_leave(e):
        name=user.get()
        if name =='':
            user.insert(0,'Username')

    user = Entry(frame,width=25,fg='black',border=0,bg="white",font=('Microsoft YaHei UI Light', 11))
    user.place(x=30,y=60)
    user.insert(0,'Username')
    user.bind('<FocusIn>',on_enter)
    user.bind('<FocusOut>',on_leave)

    Frame(frame,width=295,height=2,bg="black").place(x=25, y=90)

    def on_enter(e):
        code.delete(0,'end')

    def on_leave(e):
        name=code.get()
        if name =='':
            code.insert(0,'Password')

    code = Entry(frame,width=25,fg='black',show="*",border=0,bg="white",font=('Microsoft YaHei UI Light', 11))
    code.place(x=30,y=130)
    code.insert(0,'Password')
    code.bind('<FocusIn>',on_enter)
    code.bind('<FocusOut>',on_leave)

    Frame(frame,width=295,height=2,bg="black").place(x=25, y=160)

    def on_enter(e):
        verify.delete(0,'end')

    def on_leave(e):
        name=verify.get()
        if name =='':
            verify.insert(0,'Verify Password')

    verify = Entry(frame,width=25,fg='black',show="*",border=0,bg="white",font=('Microsoft YaHei UI Light', 11))
    verify.place(x=30,y=200)
    verify.insert(0,'Verify Password')
    verify.bind('<FocusIn>',on_enter)
    verify.bind('<FocusOut>',on_leave)

    Frame(frame,width=295,height=2,bg="black").place(x=25, y=230)

    Button(frame,width=39,pady=7,text='Sign up',bg='maroon',fg='white',border=0,command=signup).place(x=35,y=270)
    label=Label(frame,text="I have an account",fg='black',bg='white',font=('Microsoft YaHei UI Light',9))
    label.place(x=75,y=320)

    signin = Button(frame,width=6,text='Sign in',border=0,bg='white',cursor='hand2',fg='maroon',command=sign)
    signin.place(x=185,y=320)

    window.mainloop()

#########################################################################
#----------------END OF SIGNUP PAGE--------------------------------------
#########################################################################



#########################################################################
#----------------LOGIN PAGE----------------------------------------------
#########################################################################

img = PhotoImage(file = 'images\pace-logo.png')
Label(root, image = img, bg = 'white').place(x=10,y=50)

frame = Frame(root,width=500,height=500,bg="white")
frame.place(x=480,y=70)

heading=Label(frame,text='Welcome to',fg='maroon',bg='white',font=('Microsoft YaHei UI Regular',23,'bold'))
heading.place(x=30,y=0)

heading=Label(frame,text='Pacemaker!',fg='maroon',bg='white',font=('Microsoft YaHei UI Regular',23,'bold'))
heading.place(x=30,y=40)

heading=Label(frame,text='Sign in',fg='maroon',bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=30,y=80)


# Username interface
def on_enter(e):
    user.delete(0,'end')

def on_leave(e):
    name=user.get()
    if name =='':
        user.insert(0,'Username')

user = Entry(frame,width=25,fg='black',border=0,bg="white",font=('Microsoft YaHei UI Light', 11))
user.place(x=30,y=140)
user.insert(0,'Username')
user.bind('<FocusIn>',on_enter)
user.bind('<FocusOut>',on_leave)

Frame(frame,width=295,height=2,bg="black").place(x=25, y=170)

# Password interface
def on_enter(e):
    code.delete(0,'end')

def on_leave(e):
    name=code.get()
    if name =='':
        code.insert(0,'Password')


code = Entry(frame,width=25,fg='black', show="*",border=0,bg="white",font=('Microsoft YaHei UI Light', 11))
code.place(x=30,y=210)

code.insert(0,'Password')
code.bind('<FocusIn>',on_enter)
code.bind('<FocusOut>',on_leave)

Frame(frame,width=295,height=2,bg="black").place(x=25, y=240)


Button(frame,width=39,pady=7,text='Sign in',bg='maroon',fg='white',border=0,command=signin).place(x=35,y=270)
label=Label(frame,text="Don't have an account?",fg='black',bg='white',font=('Microsoft YaHei UI Light',9))
label.place(x=75,y=320)

sign_up = Button(frame,width=6,text='Sign up',border=0,bg='white',cursor='hand2',fg='maroon',command = signup_command)
sign_up.place(x=215,y=320)

root.mainloop()

#########################################################################
#----------------END OF LOGIN PAGE---------------------------------------
#########################################################################