import os
import tkinter
from tkinter import messagebox
from typing import *
import sqlite3
from datetime import datetime
import smtplib

# from dotenv import load_dotenv

# load_dotenv()
# DBUSER = os.getenv('DBUSER')
# DBPASSWORD = os.getenv('DBPASSWORD')


try:
    db = sqlite3.connect("PhytonProyecto\\login\\src\\mydatabase3.db")
    sqlcursor = db.cursor()
    print("conexion a database exitosa")
    print("version de SQLite: " + sqlite3.version)

    sqlcursor.execute(
        """ 
        CREATE TABLE IF NOT EXISTS usuarios 
            (ID INTEGER PRIMARY KEY AUTOINCREMENT, edad int, dni int, contrasenia varchar(255), email varchar(255) NOT NULL, fechaDeCreacion DATETIME)
    """
    )
    db.commit()

except Exception as exSQL:
    print(exSQL)
# fmt: off
aNum = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
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

    def __eq__(self, otro) -> bool:
        return self.datos["contrasenia"] == otro.datos["contrasenia"]

    def insertDigestedIntoSQLDB(self):
        sqlcursor.execute(
            f"""
            INSERT INTO usuarios (edad, dni, contrasenia, email, fechaDeCreacion)
        VALUES ({hash(self.datos['edad'])}, {hash(self.datos['DNI'])}, {hash(self.datos['contrasenia'])}, {hash(self.datos['email'])}, '{datetime.now()}')
        """
        )
        # for row in sqlcursor.execute("""SELECT * FROM usuarios"""):
        #     print(row)
        db.commit()
        db.close()
        print("datos insertados en la DB")


def readReadingCode():
    for column in sqlcursor.execute("""SELECT * FROM usuarios"""):
        print(column)
    db.commit()
    db.close()


def dataFromDB(
    campoColumna: Literal[
        "edad", "dni", "contrasenia", "email", "ID", "fechaDeCreacion"
    ],
    campoFila,
):
    db = sqlite3.connect("mydatabase3.db")
    sqlcursor = db.cursor()
    dataFromColumn = []

    for row in sqlcursor.execute(f"""SELECT {campoColumna} FROM usuarios"""):
        dataFromColumn.append(row)


def confirmationEmailSend(nuevoID):
    senderEmail = "fcravero@etrr.edu.ar"
    recieverEmail = 4
    pass


# A function to check if a string has invalid passwords.
def invalidPassword(rawStringPassword, boolFlag) -> bool:
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
    print("cotrasenia correcta")
    return False


def invalidEmail(rawStringEmail) -> "True/False":
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


def button1Command(nuevoID, boolFlagInput) -> "nuevoID":
    nuevoID = getInputs(nuevoID, boolFlagInput, campo="ID")
    print("Edad del nuevo ID: " + nuevoID.datos["edad"])
    print("DNI del nuevo ID: " + nuevoID.datos["DNI"])
    print("Contrasenia del nuevo ID: " + nuevoID.datos["contrasenia"])
    print("Email del nuevo ID: " + nuevoID.datos["email"])

    nuevoID.insertDigestedIntoSQLDB()

    del nuevoID


def getInputs(
    nuevoID, boolFlagInput, campo: Literal["edad", "dni", "contrasenia", "email", "ID"]
):
    if campo == "edad":
        return inputEdad.get()
    if campo == "dni":
        return inputDNI.get()
    if campo == "contrasenia":
        if inputContrasenia.get() == "onlyReadDB":
            readReadingCode()
            exit()
        if invalidPassword(inputContrasenia.get(), boolFlag) == True:
            inputContrasenia.delete(0, "end")
            messagebox.showerror(
                "Error",
                "Contrasenia necesita + de 11 caracteres, sin caracteres diferentes a: ~ @ _ / +",
            )
        else:
            return inputContrasenia.get()
    if campo == "email":
        if invalidEmail(inputEmail.get()) == True:
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
    PODER LEER LO INSERTADO QUE ESTA EN LA DB (CASA Y ESC) falta poder elegir que leer con una func
    PODER ENVIAR EMAILS DE CHECKEO(INVESTIGAR)
"""
