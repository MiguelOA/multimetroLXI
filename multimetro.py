# ****************************************************
# MULTIMETRO VIRTUALIZADO LXI
# DESARROLLADOR: Luis Alberto Barrera Sandoval
# VERSION: 0.5
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
from datetime import date

# *********************************** GLOBAL VARIABLES
idn = 'Multimeter: '
rm = pyvisa.ResourceManager()
rm.list_resources()
inst = None
timeout = 10000     #connection timeout
instName = ""
print(instName)
x = None
y = None
killThread = False
unit = ""
pause = False
flag = False    #Display Thread flag
playState = False
Interval = 1.0
fileSave = None
Ent = None
contData = 10
imaPlay = None
lista = []
flagConn = True
# ****************************************** FUNCTIONS


def fnCheckConnection():
    rm = pyvisa.ResourceManager()
    rm.list_resources()
    try:
        inst = rm.open_resource(instName)
        idn = inst.query("*IDN?")
        messagebox.showinfo(message=idn, title="Identification")
    except:
        messagebox.showinfo(message='No connection', title="Error!")
    



def fnConfRes():
    global x
    global unit
    if(fileSave == None ):
        try:
            global pause
            pause = True
            while flag:
                time.sleep(0.1)
            time.sleep(1)
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
        global y
        if fileSave == None:
            fnConData()
            now = datetime.now()
            today = str(date.today())
            currentTime = now.strftime("%H_%M_%S")
            nameFile = "Save_"+today+"_" + currentTime + ".csv"
            fileSave = open(nameFile, "w")
            measure = fnGetConf()
            Sal = "Tiempo," + measure + "\n"
            fileSave.write(Sal)
            y = threading.Thread(target=fnRecordMeasure, daemon=True)
            print('punto b')
            y.start()
        print('punto c')
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

def fnPlayMenu():
    global playState
    if(not(playState)):
        fnPlay()

def fnPauseMenu():
    global playState
    if(playState):
        fnPlay()



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
    global Ent
    print("Inicio")
    while fileSave != None and inst != None:
        if playState:
            now = datetime.now()
            currentTime = now.strftime("%H:%M:%S")
            Sal = currentTime + "," + Ent + "\n"
            if(OpcNumData.get()):
                if(contData <= 0):
                    fnSave()
                else:
                    contData = contData - 1 
            if(fileSave != None):
                fileSave.write(Sal)
            time.sleep(Interval)
        print('stand by')
    print("Fin")


def thread_Display():
    global inst
    global pause
    global flag
    global Ent
    pause = False
    while not (killThread):
        flag = False
        if(inst != None):
            if not (pause):
                flag = True
                print('b')
                try:
                    Ent = inst.query("READ?").replace("\n", "")
                    Ent += " " + unit
                    inst.query("*OPC?")
                    inst.write("*CLS")
                    if not (pause):
                        lblDisplay.config(text=Ent.replace("\n", ""))
                except:
                    
                    if not (pause):
                        lblDisplay.config(text="Not signal")
                    print("An exception occurred")
        else:
            time.sleep(0.1)
    print('Hilo finalizo')
        

def validationInt(input):
    if input.isdigit() and fileSave == None:
        n = int(input)
        if(n > 0):
            global Interval
            Interval = int(input) /1000.0
            lblInt.config(text="Interval in ms ("+ input +")")
            print("Interval: "+ input)
    return True

def validationData(input):
    if input.isdigit() and fileSave == None:
        n = int(input)
        if(n > 0):
            global contData
            contData = int(input)
            cheNumData.config(text="Numero de data ("+input+")")
    return True



def fnInitConnection():
    global rm
    global inst
    global instName
    global idn
    global unit
    global pause
    global flag
    idn = 'Multimeter: '
    c = 1   #number of connection attempts
    pause = True
    while flag:
        time.sleep(0.1)
    if(inst != None):
        inst.close()
    inst = None
    while(c > 0):
        try:
            inst = rm.open_resource(
                instName, open_timeout=timeout)
            inst.write("*CLS")
            inst.query("*OPC?")
            c = -1
        except:
            c -= 1
    if(c == -1):
        inst.timeout = timeout
        idn += inst.query("*IDN?")
        try:
            config = fnGetConf()
            if(config.find("RES") >= 0):
                unit = "OHM"
            elif (config.find("CURR") >= 0):
                unit = "A"
            elif (config.find("VOLT") >= 0):
                unit = "V"
            else:
                unit = "?"
            on_closing()
        except:
            print("Error de conexion")
        print(inst)
        messagebox.showinfo(title='Info', message='The device is online')
    else:
        messagebox.showinfo(title='ERROR!', message='The device is not aviable')
    window.title(idn)
    pause = False

def fnCloseConn():
    global inst
    global idn
    global window
    idn = 'Multimeter:'
    if(inst != None):
        inst.close
    inst = None
    window.title(idn)
    pass

def fnConnUSB():
    global window_usb
    name = cmbUSB.get()
    if name != 'Seleciona...':
        global instName
        instName = name
        fnInitConnection()
    else:
        messagebox.showinfo(message="Option no selected", title="Error!")
    
def fnConnLAN():
    global instName
    global entIP
    global window_lan
    ip = entIP.get()
    octs = ip.split('.')
    print(octs)
    if(len(octs) == 4):
        for oct in octs:
            if(oct.isnumeric()):
                if(int(oct) > 255):
                    return False
            else:
                return False
        ip = octs[0] + '.' + octs[1] + '.' + octs[2] + '.' + octs[3]
        instName = "TCPIP::" + ip + "::INSTR"
        fnInitConnection()
    return False
    

def on_closing():
    global flagConn
    global window_usb
    global window_lan
    flagConn = True
    if(window_usb != None):
        window_usb.destroy()
        window_usb = None
    if(window_lan != None):
        window_lan.destroy()
        window_lan = None
    print('Liberar ventana') 

def fnUSBBtn():
    global rm
    global lista
    global cmbUSB
    global flagConn
    global window_usb
    if flagConn:
        flagConn = False
        lista = list(rm.list_resources())
        window_usb = Toplevel()
        window_usb.resizable(False,False)
        window_usb.protocol("WM_DELETE_WINDOW", on_closing)
        window_usb.geometry('500x500+10+10')
        window_usb.title('USB connection')
        #Create widget
        cmbUSB = ttk.Combobox(window_usb, values=lista, width=30, state='readonly')
        cmbUSB.set('Select...')
        btn_conectar = Button(window_usb, text='Connect', command=fnConnUSB)
        #Place widget
        cmbUSB.place(x=20,y=20)
        btn_conectar.place(x=20, y =100)


def fnLANBtn():
    global rm
    global entIP
    global flagConn
    global window_lan
    if flagConn:
        flagConn = False
        window_lan = Toplevel()
        window_lan.resizable(False, False)
        window_lan.protocol("WM_DELETE_WINDOW", on_closing)
        window_lan.geometry('500x500+10+10')
        window_lan.title('LAN connection')
        #Create widgets
        entIP = Entry(window_lan, width=15)
        lblIP = Label(window_lan, text='IP Address')
        btn_conectar = Button(window_lan, text='Connect', command=fnConnLAN)
        #place widgets
        entIP.place(x = 20, y = 20)
        lblIP.place(x = 100, y = 20)
        btn_conectar.place(x=20, y =100)


def finalizar():
    global pause
    global killThread
    global fileSave
    global flag
    global window
    pause = True
    while flag:
        time.sleep(0.1)
        print('Esperando...')
        print(flag)
    killThread = True
    try:
        inst.close()
    except:
        print('No hay instrumento')
    if(fileSave != None):
        fileSave.close()
    window.destroy()
    

# ****************************************************
# *********************************************** MAIN
window = Tk()
window.protocol("WM_DELETE_WINDOW", finalizar)
window.geometry("1000x400+10+10")
window.resizable(False, False)
window.title(idn)
print(pause)
cmbUSB = None
entIP = None
window_usb = None
window_lan = None

my_menu = Menu(window)
window.config(menu=my_menu)

file_menu = Menu(my_menu)
my_menu.add_cascade(label='Record', menu=file_menu)
file_menu.add_command(label='Play', command=fnPlayMenu)
file_menu.add_command(label='Pause', command=fnPauseMenu)
file_menu.add_command(label='Save', command=fnSave)

connection_menu = Menu(my_menu)
my_menu.add_cascade(label='Connect', menu=connection_menu)
connection_menu.add_command(label='USB connection', command=fnUSBBtn)
connection_menu.add_command(label='LAN connection', command=fnLANBtn)
connection_menu.add_command(label='Close connection', command=fnCloseConn)

regInt = window.register(validationInt)
regData = window.register(validationData)

imaPlay = PhotoImage(file="./img/play.png")
imaSave = PhotoImage(file="./img/save.png")

OpcNumData = IntVar()
x = threading.Thread(target=thread_Display, daemon=True)


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
                     command=fnCheckConnection, width=15, 
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
cheNumData = Checkbutton(window, text='Number of measurements (10)', 
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
window.mainloop()

# ****************************************************
# ************************************ FINAL DE SCRIPT
