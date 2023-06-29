# ****************************************************
# MULTIMETRO VIRTUALIZADO LXI
# DESARROLLADOR: Luis Alberto Barrera Sandoval
# VERSION: 0.2
# URL: https://github.com/MiguelOA/multimetroLXI
# NOTAS
# ****************************************************
# ******************************************* LIBRARYS

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pyvisa
import time
import threading
from datetime import datetime

# *********************************** GLOBAL VARIABLES
idn = 'Multimeter: '
c = 5   #number of connection attempts
rm = pyvisa.ResourceManager()
rm.list_resources()
inst = None
ipAdd = "10.0.9.23" #ip address
timeout = 10000     #connection timeout
instName = "TCPIP::" + ipAdd + "::INSTR"
print(instName)
while(c > 0):
    try:
        inst = rm.open_resource(
            instName, open_timeout=timeout)
        inst.write("*CLS")
        inst.query("*OPC?")
        c = -1
    except:
        inst = None
        c -= 1
if(c == -1):
    inst.timeout = timeout
    idn += inst.query("*IDN?")
    c
print(c)
x = None
y = None
killThread = False
unit = ""
pause = False
flag = False
playState = False
Interval = 1.0
fileSave = None
Ent = None
contData = 0
imaPlay = None

# ****************************************** FUNCTIONS


def fnInitConnection():
    rm = pyvisa.ResourceManager()
    rm.list_resources()
    inst = rm.open_resource(instName)
    idn = inst.query("*IDN?")
    messagebox.showinfo(message=idn, title="Identification")


def fnConfRes():
    if(fileSave == None ):
        try:
            global pause
            global unit
            pause = True
            while flag:
                time.sleep(0.1)
            inst.write("CONF:RES")
            unit = "Ohm"
            pause = False
        except Exception as e:
            print(e)
            pause = False
    else:
        messagebox.showinfo(message="This action cannot be performed "+
                            "while recording is in progress", title="Error!")


def fnConfVoltAc():
    if(fileSave == None ):
        try:
            global pause
            pause = True
            while flag:
                time.sleep(0.1)
            inst.write("CONF:VOLT:AC")
            global unit
            unit = "V"
            pause = False
        except:
            print("Conf error")
            pause = False
    else:
        messagebox.showinfo(message="This action cannot be performed "+
                            "while recording is in progress", title="Error!")


def fnConfVoltDc():
    if(fileSave == None ):
        try:
            global pause
            pause = True
            while flag:
                time.sleep(0.1)
            inst.write("CONF:VOLT:DC")
            global unit
            unit = "V"
            pause = False
        except:
            print("Conf error")
            pause = False
    else:
        messagebox.showinfo(message="This action cannot be performed "+
                            "while recording is in progress", title="Error!")


def fnConfCurrAc():
    if(fileSave == None ):
        try:
            global pause
            pause = True
            while flag:
                time.sleep(0.1)
            inst.write("CONF:CURR:AC")
            global unit
            unit = "A"
            pause = False
        except:
            print("Conf error")
            pause = False
    else:
        messagebox.showinfo(message="This action cannot be performed "+
                            "while recording is in progress", title="Error!")


def fnConfCurrDc():
    if(fileSave == None ):
        try:
            global pause
            pause = True
            while flag:
                time.sleep(0.1)
            inst.write("CONF:CURR:DC")
            global unit
            unit = "A"
            pause = False
        except:
            print("Conf error")
            pause = False
    else:
        messagebox.showinfo(message="This action cannot be performed "+
                            "while recording is in progress", title="Error!")


def fnPlay():
    if(unit != ""):
        global fileSave
        if fileSave == None:
            fnConData()
            now = datetime.now()
            currentTime = now.strftime("%H_%M_%S")
            nameFile = "Save" + currentTime + ".csv"
            fileSave = open(nameFile, "w")
            measure = fnGetConf()
            Sal = "Tiempo," + measure + "\n"
            fileSave.write(Sal)
        global playState
        playState = not (playState)
        global imaPlay
        if playState:
            imaPlay = PhotoImage(file="./img/pause.png")
            btnPlay.config(image=imaPlay)
        else:
            imaPlay = PhotoImage(file="./img/play.png")
            btnPlay.config(image=imaPlay)
        fnRecordState()
    

def fnSave():
    global fileSave
    global playState
    global imaPlay
    if(fileSave != None):
        fileSave.close()
        fileSave = None
        playState = False
        imaPlay = PhotoImage(file="./img/play.png")
        btnPlay.config(image=imaPlay)
    fnRecordState()

def fnGetConf():
    global pause
    pause = True
    while flag:
        time.sleep(0.1)
    measure = inst.query("CONF?")
    print("All Conf: "+measure)
    pos = measure.find(" ")
    measure = measure[1:pos]
    inst.write("*CLS")
    inst.query("*OPC?")
    if(measure != "RES" and  measure.find(":") == -1):
        measure = measure + ":DC"
    print("Measure: "+measure)
    pause = False
    return measure



def fnRecordState():
    global fileSave
    global playState
    if(fileSave == None):
        lblRecord.config(text="Record: Null", fg="red")
    elif (playState):
        lblRecord.config(text="Record: Playing", fg="green")
    else:
        lblRecord.config(text="Record: Paused", fg="blue")


def fnConData():
    if fileSave != None:
        if OpcNumData.get():
            OpcNumData.set(0)
        else:
            OpcNumData.set(1)
        messagebox.showinfo(message="This action cannot be performed "+
                            "while recording is in progress", title="Error!")
        


def fnRecordMeasure():
    global fileSave
    global playState
    global contData
    print("Inicio")
    while not (killThread):
        if playState:
            now = datetime.now()
            currentTime = now.strftime("%H:%M:%S")
            Sal = currentTime + "," + ENT + "\n"
            if(OpcNumData.get()):
                if(contData <= 0):
                    fnSave()
                else:
                    contData = contData - 1 
            if(fileSave != None):
                fileSave.write(Sal)
        time.sleep(Interval)
    print("Fin")


def thread_Display():
    while not (killThread):
        if not (pause):
            global flag
            flag = True
            try:
                global ENT
                ENT = inst.query("READ?").replace("\n", "")
                ENT += " " + unit
                inst.query("*OPC?")
                inst.write("*CLS")
                if(not(pause)):
                    lblDisplay.config(text=ENT.replace("\n", ""))
            except:
                if(not(pause)):
                    lblDisplay.config(text="Not signal")
                print("An exception occurred")
            flag = False

def validationInt(input):
    if input.isdigit() and fileSave == None:
        global Interval
        Interval = int(input) /1000.0
        lblInt.config(text="Interval in ms ("+ input +")")
        print("Interval: "+ input)
    return True

def validationData(input):
    if input.isdigit() and fileSave == None:
        global contData
        contData = int(input)
        cheNumData.config(text="Numero de data ("+input+")")
    return True

# ****************************************************
# *********************************************** MAIN
window = Tk()
window.geometry("1000x400+10+10")
window.resizable(False, False)
window.title(idn)
regInt = window.register(validationInt)
regData = window.register(validationData)

imaPlay = PhotoImage(file="./img/play.png")
imaSave = PhotoImage(file="./img/save.png")

OpcNumData = IntVar()
x = threading.Thread(target=thread_Display)
y = threading.Thread(target=fnRecordMeasure)

try:
    config = fnGetConf()
    if(config.find("RES") >= 0):
        unit = "OHM"
    elif (config.find("CURR") >= 0):
        unit = "A"
    elif (config.find("VOLT") >= 0):
        unit = "V"
except:
    print("Error de conexion")

# ********************************* Widgets generation
btnACCurrent = Button(window, text="AC Current",
                      command=fnConfCurrAc, width=15, 
    font=("Arial 12 bold"))
btnACVoltage = Button(window, text="AC Voltage",
                      command=fnConfVoltAc, width=15, 
    font=("Arial 12 bold"))
btnDCCurrent = Button(window, text="DC Current",
                      command=fnConfCurrDc, width=15, 
    font=("Arial 12 bold"))
btnDCVoltage = Button(window, text="DC Voltage",
                      command=fnConfVoltDc, width=15, 
    font=("Arial 12 bold"))
btnResistance = Button(window, text="Resistance",
                       command=fnConfRes, width=15, 
    font=("Arial 12 bold"))
btnConexion = Button(window, text="Check connection",
                     command=fnInitConnection, width=15, 
    font=("Arial 12 bold"))
lblDisplay = Label(
    window, text="Not signal", 
    font=("Verdana 36 italic"), 
    fg="green",
    background='black',
    width=21
)

btnPlay = Button(window, command=fnPlay, image=imaPlay)
btnSave = Button(window, command=fnSave, image=imaSave)
entInterval = Entry(window, width=10,
               font="Verdana 12",
               validate='key',
               validatecommand=(regInt, '%P'))
lblRecord = Label(window, 
                  text="Record: Null", 
                  font=("Console 18 bold"), 
                  fg="red")
lblInt = Label(window,
               text="Interval in ms ("+ str(int(Interval*1000))+")",
               font="Verdana 12")
cheNumData = Checkbutton(window, text='Number of measurements (0)', 
                          variable=OpcNumData, command=fnConData,
               font="Verdana 12")
entNumData = Entry(window, width=10,
               font="Verdana 12",
               validate='key',
               validatecommand=(regData, '%P'))


# ********************************* Widget positioning
lblDisplay.place(x=20, y=20)
btnACCurrent.place(x=20, y=90)
btnDCCurrent.place(x=20, y=130)
btnACVoltage.place(x=200, y=90)
btnDCVoltage.place(x=200, y=130)
btnResistance.place(x=380, y=90)
btnConexion.place(x=380, y=130)
btnPlay.place(x=560, y=90)
btnSave.place(x=560, y=130)
entInterval.place(x=20, y=200)
lblInt.place(x=170, y=200)
entNumData.place(x=20, y=250)
cheNumData.place(x=170, y=250)
lblRecord.place(x=700, y=20)
# ************************************** Threads start
x.start()
y.start()

if(c == -1):
    window.mainloop()
    pause = True
    while flag:
        time.sleep(0.1)
    killThread = True
    inst.close()
killThread = True
if(fileSave != None):
    fileSave.close()
x.join()
y.join()

# ****************************************************
# ************************************ FINAL DE SCRIPT
