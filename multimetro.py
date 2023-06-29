# ****************************************************
# MULTIMETRO VIRTUALIZADO
# DESARROLLADOR: Luis Alberto Barrera Sandoval
# VERSION: 0.1
# URL:
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
c = 5   #Number of connection attempts
rm = pyvisa.ResourceManager()
rm.list_resources()
inst = None
ipAdd = "10.0.9.23"
timeout = 10000
instName = "TCPIP::"+ipAdd+"::INSTR"
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
unidad = ""
pause = False
flag = False
playState = False
Intervalo = 1.0
fileSave = None
Ent = None
contDatos = 0
imaPlay = None
# ****************************************** FUNCTIONS


def fnInitConexion():
    rm = pyvisa.ResourceManager()
    rm.list_resources()
    inst = rm.open_resource(instName)
    idn = inst.query("*IDN?")
    messagebox.showinfo(message=idn, title="Identificacion")


def fnConfRes():
    if(fileSave == None ):
        try:
            global pause
            global unidad
            pause = True
            while flag:
                time.sleep(0.1)
            inst.write("CONF:RES")
            unidad = "Ohm"
            pause = False
        except Exception as e:
            print(e)
            pause = False
    else:
        messagebox.showinfo(message="No se puede realizar mientras se graba", title="Error!")


def fnConfVoltAc():
    if(fileSave == None ):
        try:
            global pause
            pause = True
            while flag:
                time.sleep(0.1)
            inst.write("CONF:VOLT:AC")
            global unidad
            unidad = "V"
            pause = False
        except:
            print("Conf error")
            pause = False
    else:
        messagebox.showinfo(message="No se puede realizar mientras se graba", title="Error!")


def fnConfVoltDc():
    if(fileSave == None ):
        try:
            global pause
            pause = True
            while flag:
                time.sleep(0.1)
            inst.write("CONF:VOLT:DC")
            global unidad
            unidad = "V"
            pause = False
        except:
            print("Conf error")
            pause = False
    else:
        messagebox.showinfo(message="No se puede realizar mientras se graba", title="Error!")


def fnConfCurrAc():
    if(fileSave == None ):
        try:
            global pause
            pause = True
            while flag:
                time.sleep(0.1)
            inst.write("CONF:CURR:AC")
            global unidad
            unidad = "A"
            pause = False
        except:
            print("Conf error")
            pause = False
    else:
        messagebox.showinfo(message="No se puede realizar mientras se graba", title="Error!")


def fnConfCurrDc():
    if(fileSave == None ):
        try:
            global pause
            pause = True
            while flag:
                time.sleep(0.1)
            inst.write("CONF:CURR:DC")
            global unidad
            unidad = "A"
            pause = False
        except:
            print("Conf error")
            pause = False
    else:
        messagebox.showinfo(message="No se puede realizar mientras se graba", title="Error!")


def fnPlay():
    if(unidad != ""):
        global fileSave
        if fileSave == None:
            fnConDatos()
            now = datetime.now()
            currentTime = now.strftime("%H_%M_%S")
            nameFile = "Save" + currentTime + ".csv"
            fileSave = open(nameFile, "w")
            medida = fnGetConf()
            Sal = "Tiempo," + medida + "\n"
            fileSave.write(Sal)
        global playState
        playState = not (playState)
        global imaPlay
        if playState:
            imaPlay = PhotoImage(file="pause.png")
            btnPlay.config(image=imaPlay)
        else:
            imaPlay = PhotoImage(file="play.png")
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
        imaPlay = PhotoImage(file="play.png")
        btnPlay.config(image=imaPlay)
    fnRecordState()

def fnGetConf():
    global pause
    pause = True
    while flag:
        time.sleep(0.1)
    medida = inst.query("CONF?")
    print("Conf completo: "+medida)
    pos = medida.find(" ")
    medida = medida[1:pos]
    inst.write("*CLS")
    inst.query("*OPC?")
    if(medida != "RES" and  medida.find(":") == -1):
        medida = medida + ":DC"
    print("Medida: "+medida)
    pause = False
    return medida



def fnRecordState():
    global fileSave
    global playState
    if(fileSave == None):
        lblRecord.config(text="Record: Null", fg="red")
    elif (playState):
        lblRecord.config(text="Record: Playing", fg="green")
    else:
        lblRecord.config(text="Record: Paused", fg="blue")


def fnApplyInt():   
    s = entInterval.get()
    if(fileSave == None ):
        if(s.isnumeric()):
            global Intervalo
            Intervalo = (int(entInterval.get())) / 1000.0
            s1 = str(Intervalo) + ""
            lblInt.config(text="Interval in ms ("+ s +")")
            print("Intervalo: "+ s1)
        else:
            messagebox.showinfo(message="La entrada es incorrecta, debe ser entera", title="Error!")
    else:
        messagebox.showinfo(message="No se puede realizar mientras se graba", title="Error!")

def fnConDatos():
    if fileSave != None:
        if OpcNumDatos.get():
            OpcNumDatos.set(0)
        else:
            OpcNumDatos.set(1)
        messagebox.showinfo(message="No se puede realizar mientras se graba", title="Error!")
        


def fnRecordMeasure():
    global fileSave
    global playState
    global contDatos
    print("Inicio")
    while not (killThread):
        if playState:
            now = datetime.now()
            currentTime = now.strftime("%H:%M:%S")
            Sal = currentTime + "," + ENT + "\n"
            if(OpcNumDatos.get()):
                if(contDatos <= 0):
                    fnSave()
                else:
                    contDatos = contDatos - 1 
            if(fileSave != None):
                fileSave.write(Sal)
        time.sleep(Intervalo)
    print("Fin")


def thread_Display():
    while not (killThread):
        try:
            if not (pause):
                global flag
                flag = True
                global ENT
                ENT = inst.query("READ?").replace("\n", "")
                ENT += " " + unidad
                inst.query("*OPC?")
                inst.write("*CLS")
                flag = False
                lblDisplay.config(text=ENT.replace("\n", ""))
        except:
            print("An exception occurred")

def validationInt(input):
    if input.isdigit() and fileSave == None:
        global Intervalo
        Intervalo = int(input) /1000.0
        lblInt.config(text="Interval in ms ("+ input +")")
        print("Intervalo: "+ input)
    return True

def validationDatos(input):
    if input.isdigit() and fileSave == None:
        global contDatos
        contDatos = int(input)
        cheNumDatos.config(text="Numero de datos ("+input+")")
    return True


# *************************** MAIN
window = Tk()
window.geometry("1000x600+10+10")
window.resizable(False, False)
window.title(idn)
regInt = window.register(validationInt)
regDatos = window.register(validationDatos)

imaPlay = PhotoImage(file="play.png")
imaSave = PhotoImage(file="save.png")
OpcNumDatos = IntVar()

x = threading.Thread(target=thread_Display)
y = threading.Thread(target=fnRecordMeasure)
try:
    config = fnGetConf()
    if(config.find("RES") >= 0):
        unidad = "OHM"
    elif (config.find("CURR") >= 0):
        unidad = "A"
    elif (config.find("VOLT") >= 0):
        unidad = "V"
except:
    print("Error de conexion")


# generar los widgets
btnACCurrent = Button(window, text="AC Current", command=fnConfCurrAc, width=15, 
    font=("Arial 12 bold"))
btnACVoltage = Button(window, text="AC Voltage", command=fnConfVoltAc, width=15, 
    font=("Arial 12 bold"))
btnDCCurrent = Button(window, text="DC Current", command=fnConfCurrDc, width=15, 
    font=("Arial 12 bold"))
btnDCVoltage = Button(window, text="DC Voltage", command=fnConfVoltDc, width=15, 
    font=("Arial 12 bold"))
btnResistance = Button(window, text="Resistencia", command=fnConfRes, width=15, 
    font=("Arial 12 bold"))
btnConexion = Button(window, text="Revisar conexion", command=fnInitConexion, width=15, 
    font=("Arial 12 bold"))
lblDisplay = Label(
    window, text="texto modificado", 
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
btnApplyInt = Button(window, text="Apply Interval", command=fnApplyInt,
               font="Verdana 12")
lblRecord = Label(window, 
                  text="Record: Null", 
                  font=("Console 18 bold"), 
                  fg="red")
lblInt = Label(window,
               text="Interval in ms ("+ str(int(Intervalo*1000))+")",
               font="Verdana 12")
cheNumDatos = Checkbutton(window, text='Numero de datos (0)', variable=OpcNumDatos, command=fnConDatos,
               font="Verdana 12")
entNumDatos = Entry(window, width=10,
               font="Verdana 12",
               validate='key',
               validatecommand=(regDatos, '%P'))


# posicionamiento de widgets
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
btnApplyInt.place(x=450, y=200)
entNumDatos.place(x=20, y=250)
cheNumDatos.place(x=170, y=250)
lblRecord.place(x=700, y=20)

#Inicio de hilos
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
