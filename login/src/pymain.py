from asyncio.windows_events import NULL
import math
import os
import tkinter
from tkinter import messagebox
from typing import *
import sqlite3
from datetime import datetime

# from dotenv import load_dotenv

# load_dotenv()
# DBUSER = os.getenv('DBUSER')
# DBPASSWORD = os.getenv('DBPASSWORD')

# try:
db = sqlite3.connect("mydatabase3")
sqlcursor = db.cursor()
print("conexion a database exitosa")
print("version de SQLite: " + sqlite3.version)

sqlcursor.execute(
    """CREATE TABLE IF NOT EXISTS usuarios 
    (id integer auto_increment primary key, nombre varchar(255), edad int, contrasenia varchar(255), email varchar(255), fechaDeCreacion timestamp)"""
)
dateToday = datetime.now()
sqlcursor.execute(
    f"""INSERT INTO 'usuarios' VALUES
        (?, 'peres', '33', 'holaC', 'hola', ?)""",
    (NULL, dateToday),
)
db.commit()
db.close()

# except Exception as ex:
#     print(ex)
# fmt: off
aNum = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
aABC = ('Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ', 'Z', 'X', 'C', 'V', 'B', 'N', 'M')
aAbc = ('q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ñ', 'z', 'x', 'c', 'v', 'b', 'n', 'm')
aChar = ('~', '@', '_', '/', '+', '.')
# fmt: on

boolFlag = False
boolFlagInput = False
nuevoID = 0

ventana = tkinter.Tk()
ventana.geometry("600x400")
ventana.title("Felipe Cravero")


class datosMiembro:
    def __init__(self, iEdad: int, iDNI: int, iContrasenia: str, iEmail: str):
        """constructor"""
        self.datos = {}
        self.datos["edad"] = iEdad
        self.datos["DNI"] = iDNI
        self.datos["contrasenia"] = iContrasenia
        self.datos["email"] = iEmail

    def SLQinsertionWithHashing(self, datos):
        digestedEdad = hash(datos["edad"])
        digestedDNI = hash(datos["DNI"])
        digestedContrasenia = hash(datos["contrasenia"])
        digestedEmail = hash(datos["email"])

        sqlcursor.execute(
            f"""INSERT INTO usuarios VALUES
            ({datos['edad']}, {datos['DNI']}, {datos['contrasenia']}, {datos['email']}, datetime('now'))"""
        )
        db.commit()


def invalidPasswordCheck(rawStringPassword, boolFlag) -> "True/False":
    checkPCont = 0
    for x in rawStringPassword:
        if len(rawStringPassword) < 11:
            boolFlag = True
            break
        if x not in aABC and x not in aAbc and x not in aChar and x not in aNum:
            checkPCont += 1
    if checkPCont != 0 or boolFlag == True:
        rawStringPassword = " "
        print(
            f"se ha insertado un caracter invalido o la cantidad de caracteres son menores a 11 {rawStringPassword}"
        )
        return True
    return False


def invalidEmailCheck(rawStringEmail) -> "True/False":
    checkECont = 0
    if (
        rawStringEmail.__contains__("@gmail.com")
        or rawStringEmail.__contains__("@etrr.edu.ar")
        or rawStringEmail.__contains__("@yahoo.com")
    ) == False:
        checkECont += 1
    for y in rawStringEmail:
        if y not in aABC and y not in aAbc and y not in aChar and y not in aNum:
            checkECont += 1
    if checkECont != 0:
        print("no es un email valido")
        return True
    return False


# def encriptionFunc(stringForEncryption):
#     key = Fernet.generate_key()
#     encryptKey = Fernet(key)
#     encryptedString = encryptKey.encrypt(bytes(stringForEncryption))
#     print(encryptedString)
#     return encryptedString, encryptKey
# def deencriptionFunc(stringForDecryption, decryptKey):
#     decryptKey.decrypt(stringForDecryption)
# def hashingFunc(stringForHashing: str) -> "hash":
#     return hash(stringForHashing)


def button1Command(nuevoID, boolFlagInput) -> "nuevoID":
    nuevoID = getInputs(nuevoID, boolFlagInput, campo="ID")
    print("Edad del nuevo ID: " + nuevoID.datos["edad"])
    print("DNI del nuevo ID: " + nuevoID.datos["DNI"])
    print("Contrasenia del nuevo ID: " + nuevoID.datos["contrasenia"])
    print("Email del nuevo ID: " + nuevoID.datos["email"])
    # encString, encKey = encriptionFunc(nuevoID.datos["contrasenia"])
    # print(nuevoID.datos["contrasenia"])
    # deencriptionFunc(encKey, encKey)
    # print(nuevoID.datos["contrasenia"])
    return nuevoID


def getInputs(
    nuevoID, boolFlagInput, campo: Literal["edad", "dni", "contrasenia", "email", "ID"]
):
    if campo == "edad":
        return inputEdad.get()
    if campo == "dni":
        return inputDNI.get()
    if campo == "contrasenia":
        if invalidPasswordCheck(inputContrasenia.get(), boolFlag) == True:
            inputContrasenia.delete(0, "end")
            messagebox.showerror(
                "Error",
                "Contrasenia necesita + de 11 caracteres, sin caracteres diferentes a: ~ @ _ / +",
            )
        else:
            return inputContrasenia.get()
    if campo == "email":
        if invalidEmailCheck(inputEmail.get()) == True:
            inputEmail.delete(0, "end")
            messagebox.showerror("Error", "Email ingresado invalido")
        else:
            return inputEmail.get()
    if campo == "ID":
        nuevoID = datosMiembro(
            iEdad=getInputs(nuevoID, boolFlagInput, campo="edad"),
            iDNI=getInputs(nuevoID, boolFlagInput, campo="dni"),
            iContrasenia=getInputs(nuevoID, boolFlagInput, campo="contrasenia"),
            iEmail=getInputs(nuevoID, boolFlagInput, campo="email"),
        )
        return nuevoID


titulo = tkinter.Label(ventana, text="Iniciar sesion", font="Sylfaen 25")
titulo.grid(row=0, column=0)

inputEdadTitulo = tkinter.Label(ventana, text="ingresar edad", font="Sylfaen 14")
inputEdadTitulo.grid(row=1, column=1)
inputEdad = tkinter.Entry(ventana, font="Sylfaen 14")
inputEdad.grid(row=2, column=1)

inputDNITitulo = tkinter.Label(ventana, text="ingresar DNI", font="Sylfaen 14")
inputDNITitulo.grid(row=3, column=1)
inputDNI = tkinter.Entry(ventana, font="Sylfaen 14")
inputDNI.grid(row=4, column=1)

inputContraseniaTitulo = tkinter.Label(
    ventana, text="ingresar contrasenia", font="Sylfaen 14"
)
inputContraseniaTitulo.grid(row=5, column=1)
inputContrasenia = tkinter.Entry(ventana, font="Sylfaen 14")
inputContrasenia.grid(row=6, column=1)

inputEmailTitulo = tkinter.Label(ventana, text="ingresar email", font="Sylfaen 14")
inputEmailTitulo.grid(row=7, column=1)
inputEmail = tkinter.Entry(ventana, font="Sylfaen 14")
inputEmail.grid(row=8, column=1)

sendInput = tkinter.Button(
    ventana,
    text="enviar",
    width=6,
    height=2,
    command=lambda: button1Command(nuevoID, boolFlagInput),
)
sendInput.grid(row=9, column=1)


ventana.mainloop()

"""
IDEAS:
    DES/ENCRIPTAR (ESC Y CASA) 
    TERMINAR INSERCION A DATABASE SQL FALTA PODER LEER LO INSERTADO (CASA Y ESC)
    X TERMINAR EMAIL Y CONTRASENIA CHECK (CASA Y ESC) LISTOOO
    PODER ENVIAR EMAILS DE CHECKEO(INVESTIGAR)
"""
