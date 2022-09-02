import os
from asyncio.windows_events import NULL
import tkinter
from tkinter import messagebox
from typing import Literal
import sqlite3
from datetime import datetime
#from dotenv import load_dotenv

#load_dotenv()
#DBUSER = os.getenv('DBUSER')
#DBPASSWORD = os.getenv('DBPASSWORD')

try:
    db = sqlite3.connect('database/mydatabase')
    sqlcursor = db.cursor()
    

    if db.is_connected():
        print('conexion a database exitosa')
        print(sqlite3.version)
        info_db = db.get_server_info()
        print(info_db)
    
except Exception as ex:
    print(ex)

aNum = (1, 2, 3, 4, 5, 6, 7, 8, 9)
aABC = ('Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ', 'Z', 'X', 'C', 'V', 'B', 'N', 'M')
aAbc = ('q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ñ', 'z', 'x', 'c', 'v', 'b', 'n', 'm')
aChar = ('~', '@', '_', '/', '+')

cuentas = {}
print (cuentas)
boolFlag = False
boolFlagInput = False
nuevoID = 0

ventana = tkinter.Tk()
ventana.geometry('600x400')
ventana.title('Felipe Cravero')

class datosMiembro:   
    def __init__(self, 
            iEdad : int, 
            iDNI : int, 
            iContrasenia : str, 
            iEmail : str
        ):
        """constructor"""
        self.datos = {}
        self.datos['edad'] = iEdad
        self.datos['DNI'] = iDNI
        self.datos['contrasenia'] = iContrasenia
        self.datos['email'] = iEmail

    def invalidPasswordCheck(self, boolFlag):
        checkPCont = 0
        for x in self.datos['contrasenia']:
            if len(self.datos['contrasenia']) < 11:
                #print("cantidad de caracteres debe ser superior a 11"); 
                boolFlag = True
                break
            if x not in aABC and x not in aAbc and x not in aChar and x not in aNum: checkPCont += 1 
        if checkPCont != 0 or boolFlag == True: 
            self.datos['contrasenia'] = " "
            print('se ha insertado un caracter invalido o la cantidad de caracteres son menores a 11' + self.datos['contrasenia']+ 'asdasdasd')
            return True
        return False

    def invalidEmailCheck(self):
        checkECont = 0
        for y in self.datos['email']:
            if y not in aABC and y not in aAbc and y not in aChar and y not in aNum: checkECont += 1 
        if checkECont != 0 : 
            print('se ha insertado un caracter incorrecto')
            self.datos['email'] = " "
            return True
        return False

def invalidPasswordCheck(rawStringPassword, boolFlag):
        checkPCont = 0
        for x in rawStringPassword:
            if len(rawStringPassword) < 11:
                #print("cantidad de caracteres debe ser superior a 11"); 
                boolFlag = True
                break
            if x not in aABC and x not in aAbc and x not in aChar and x not in aNum: checkPCont += 1 
        if checkPCont != 0 or boolFlag == True: 
            rawStringPassword = " "
            print('se ha insertado un caracter invalido o la cantidad de caracteres son menores a 11' + rawStringPassword)
            return True
        return False

def invalidEmailCheck(rawStringEmail):
        checkECont = 0
        if rawStringEmail.__contains__('@') == False: 
            checkECont += 1
        for y in rawStringEmail:
            if y not in aABC and y not in aAbc and y not in aChar and y not in aNum: checkECont += 1 
        if checkECont != 0 : 
            print('no es un email valido')
            return True
        return False

def button1Command (nuevoID, cuentas, boolFlagInput):
    nuevoID = getInputs(nuevoID, boolFlagInput, campo = 'ID')
    cuentas[nuevoID.datos['email']] = nuevoID
    print('Edad del nuevo ID: ' + nuevoID.datos['edad'])
    print('DNI del nuevo ID: ' + nuevoID.datos['DNI'])
    print('Contrasenia del nuevo ID: ' + nuevoID.datos['contrasenia'])
    print('Email del nuevo ID: ' + nuevoID.datos['email'])
    print(len(nuevoID.datos['contrasenia']))
    return nuevoID

def getInputs (nuevoID, boolFlagInput, campo : Literal['edad', 'dni', 'contrasenia', 'email', 'ID']):
    if campo == 'edad': 
        return inputEdad.get()
    if campo == 'dni':
        return inputDNI.get()
    if campo == 'contrasenia':
        if invalidPasswordCheck(inputContrasenia.get(), boolFlag) == True :
            inputContrasenia.delete(0,'end')
            messagebox.showerror('Error' , 'necesita + de 11 caracteres, sin caracteres diferentes a: ~ @ _ / +')
        else:
            return inputContrasenia.get()
    if campo == 'email':
        if invalidEmailCheck(inputEmail.get()) == True :
            inputEmail.delete(0,'end')
            messagebox.showerror('Error', 'Email ingresado invalido')
    if campo == 'ID':
        nuevoID = datosMiembro(
            iEdad = getInputs(nuevoID, boolFlagInput, campo = 'edad'),
            iDNI = getInputs(nuevoID, boolFlagInput, campo = 'dni'),
            iContrasenia = getInputs(nuevoID, boolFlagInput, campo = 'contrasenia'), 
            iEmail = getInputs(nuevoID, boolFlagInput, campo = 'email')
            )
        return nuevoID

titulo = tkinter.Label(ventana, text = 'Iniciar sesion', font = 'Sylfaen 25')
titulo.grid(row = 0, column = 0)

inputEdadTitulo = tkinter.Label(ventana, text = 'ingresar edad', font = 'Sylfaen 14')
inputEdadTitulo.grid(row = 1, column = 1)
inputEdad = tkinter.Entry(ventana, font = 'Sylfaen 14')
inputEdad.grid(row = 2, column = 1)

inputDNITitulo = tkinter.Label(ventana, text = 'ingresar DNI', font = 'Sylfaen 14')
inputDNITitulo.grid(row=3, column=1)
inputDNI = tkinter.Entry(ventana, font = 'Sylfaen 14')
inputDNI.grid(row = 4, column = 1)

inputContraseniaTitulo = tkinter.Label(ventana, text = 'ingresar contrasenia', font = 'Sylfaen 14')
inputContraseniaTitulo.grid(row = 5, column = 1)
inputContrasenia = tkinter.Entry(ventana, font = 'Sylfaen 14')
inputContrasenia.grid(row = 6, column = 1)

inputEmailTitulo = tkinter.Label(ventana, text = 'ingresar email', font = 'Sylfaen 14')
inputEmailTitulo.grid(row = 7, column = 1)
inputEmail = tkinter.Entry(ventana, font = 'Sylfaen 14')
inputEmail.grid(row = 8, column = 1)

sendInput = tkinter.Button (ventana, text = 'enviar', width = 6, height = 2, command = lambda : button1Command(nuevoID, cuentas, boolFlagInput))
sendInput.grid(row = 9, column = 1)


ventana.mainloop()

"""
IDEAS:
    DES/ENCRIPTAR (ESC Y CASA)
    TERMINAR INSERCION A DATABASE SQL FALTA PODER LEER LO INSERTADO (CASA Y ESC)
    TERMINAR EMAIL Y CONTRASENIA CHECK (CASA Y ESC)
    PODER ENVIAR EMAILS DE CHECKEO
"""