import os
import time
from os.path import exists
from cryptography.fernet import Fernet
from tkinter import *
from tkinter.ttk import *
import customtkinter
from tkinter import messagebox
from typing import Literal
import sqlite3
from datetime import datetime
import ssl
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()
EMAILPASS = os.getenv("EMAILPASS")
GMAILKEY = os.getenv("GMAILKEY")


sepConsole = """**************************************************"""
# DEFINO DECORADORES


def timer(func):
    def wrapper(*args, **kwargs):
        before = time.perf_counter()
        func(*args, **kwargs)
        print(f"Func tardo: {time.time() - before} seconds")

    return wrapper


def encriptDec(func):
    def wrapper(*args, **kwargs):
        if func(*args, **kwargs) == "cryptography.fernet.InvalidToken":
            print("key invalida, rehacer")

    return wrapper


@encriptDec
def DBEncryptionKeyGenerator():
    try:
        if not exists("PhytonProyecto\\login\\src\\keyFile.key"):
            key = Fernet.generate_key()
            print(key)
            with open("PhytonProyecto\\login\\src\\keyFile.key", "wb") as keyFile:
                keyFile.write(key)
    except Exception as decExc:
        return decExc


def DBEncryptionKeyReader() -> bytes:
    with open("PhytonProyecto\\login\\src\\keyFile.key", "rb") as keyFile:
        keyR = keyFile.read()
        print(keyR)
    return keyR


@encriptDec
def DBEncryptor(fernetObject: Fernet):
    try:
        with open("PhytonProyecto\\login\\src\\mydatabase3.db", "rb") as originalDB:
            original = originalDB.read()

        encrypted = fernetObject.encrypt(original)

        with open("PhytonProyecto\\login\\src\\mydatabase3.db", "wb") as encryptedDB:
            encryptedDB.write(encrypted)
    except Exception as decExc:
        return decExc


@encriptDec
def DBDecryptor(fernetObject: Fernet):
    try:
        with open(
            "PhytonProyecto\\login\\src\\mydatabase3.db", "rb"
        ) as deEncryptionFuncEncryptedDB:
            encrypted = deEncryptionFuncEncryptedDB.read()

        decrypted = fernetObject.decrypt(encrypted)

        with open(
            "PhytonProyecto\\login\\src\\mydatabase3.db", "wb"
        ) as deEncryptionFuncDecryptedDB:
            deEncryptionFuncDecryptedDB.write(decrypted)
    except Exception as decExc:
        return decExc


# ?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|
# ?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|
# ?|?|?|?|?|?|?|?|?| PRIMERAS LINEAS QUE SE VAN A EJECUTAR  ?|?|?|?|?|?|?|?|?|?|?|?|?|
# ?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|
# ?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|s?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|

try:
    DBEncryptionKeyGenerator()
    f = Fernet(DBEncryptionKeyReader())
    with sqlite3.connect("PhytonProyecto\\login\\src\\mydatabase3.db") as db:
        sqlcursor = db.cursor()
        print("conexion a database exitosa")
        print(f"version de SQLite: {sqlite3.version}")
        print(f"{sepConsole}\n\n")
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


# Devuelve el datos miembro en usuarios
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

    def insertDigestedIntoSQLDB(self, f):
        DBDecryptor(f)

        with sqlite3.connect("PhytonProyecto\\login\\src\\mydatabase3.db") as db:
            sqlcursor = db.cursor()
            sqlcursor.execute(
                f"""
                    INSERT INTO usuarios (edad, dni, contrasenia, email, fechaDeCreacion)
                VALUES ('{self.datos['edad']}', '{self.datos['DNI']}', '{self.datos['contrasenia']}', '{self.datos['email']}', '{datetime.now()}')
                """
            )
            print("datos insertados en la DB")

        DBEncryptor(f)


# Read all the table.
def readAllTheTable():
    DBDecryptor(f)

    with sqlite3.connect("PhytonProyecto\\login\\src\\mydatabase3.db") as db:
        sqlcursor = db.cursor()
        for column in sqlcursor.execute("""SELECT * FROM usuarios"""):
            print(column)

    DBEncryptor(f)


# Returns a generator that yields all the data from the database.
def retrieveDataFromDB(
    campoColumna: Literal[
        "edad", "dni", "contrasenia", "email", "ID", "fechaDeCreacion"
    ]
):
    DBDecryptor(f)

    with sqlite3.connect("PhytonProyecto\\login\\src\\mydatabase3.db") as db:
        sqlcursor = db.cursor()
        for columna in sqlcursor.execute(f"""SELECT {campoColumna} FROM usuarios"""):
            yield columna

    DBEncryptor(f)


def confirmationEmailSend(nuevoID):

    senderEmail = "fcravero@etrr.edu.ar"
    recieverEmail = nuevoID.datos["email"]
    subject = "Email de confirmacion"
    message = "hola, confirme su correo electronico"

    em = EmailMessage()
    em["From"] = senderEmail
    em["To"] = recieverEmail
    em["Subject"] = subject
    em.set_content(message)

    context = ssl.create_default_context()

    try:
        with smtplib.SMPT_SSL("smpt.gmail.com", 465, context=context) as smtp:
            smtp.login(senderEmail, GMAILKEY)
            smtp.sendmail(senderEmail, recieverEmail, em.as_string())
    except Exception as exEmail:
        print(exEmail)


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
            f"se ha insertado un caracter invalido o la cantidad de caracteres son menores a 11 en la contrasenia {rawStringPassword}"
        )
        return True
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


@timer
def button1Command(nuevoID, boolFlagInput) -> "nuevoID":
    nuevoID = getInputs(nuevoID, boolFlagInput, campo="ID")
    try:
        print("Edad del nuevo ID: " + nuevoID.datos["edad"])
        print("DNI del nuevo ID: " + nuevoID.datos["DNI"])
        print("Contrasenia del nuevo ID: " + nuevoID.datos["contrasenia"])
        print("Email del nuevo ID: " + nuevoID.datos["email"])
    except Exception as decExc:
        print(str(decExc))
    nuevoID.insertDigestedIntoSQLDB(f)

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
            readAllTheTable()
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


# ?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|
# ?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|
# ?|?|?|?|?|?|?|?|?| PARTE DE TKINTER  ?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|
# ?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|
# ?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|s?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?|?

ventana = customtkinter.CTk()
ventana.geometry("400x580")
ventana.resizable(width=False, height=False)
ventana.title("Felipe Cravero")

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

titulo = customtkinter.CTkLabel(ventana, text="Iniciar sesion", text_font="Sylfaen 25")
titulo.pack(pady=12, padx=10)

inputEdadTitulo = customtkinter.CTkLabel(
    ventana, text="ingresar edad", text_font="Sylfaen 14"
)
inputEdadTitulo.pack(pady=12, padx=10)
inputEdad = customtkinter.CTkEntry(ventana, text_font="Sylfaen 14")
inputEdad.pack(pady=12, padx=10)

inputDNITitulo = customtkinter.CTkLabel(
    ventana, text="ingresar DNI", text_font="Sylfaen 14"
)
inputDNITitulo.pack(pady=12, padx=10)
inputDNI = customtkinter.CTkEntry(ventana, text_font="Sylfaen 14")
inputDNI.pack(pady=12, padx=10)

inputContraseniaTitulo = customtkinter.CTkLabel(
    ventana, text="ingresar contrasenia", text_font="Sylfaen 14"
)
inputContraseniaTitulo.pack(pady=12, padx=10)
inputContrasenia = customtkinter.CTkEntry(ventana, text_font="Sylfaen 14")
inputContrasenia.pack(pady=12, padx=10)

inputEmailTitulo = customtkinter.CTkLabel(
    ventana, text="ingresar email", text_font="Sylfaen 14"
)
inputEmailTitulo.pack(pady=12, padx=10)
inputEmail = customtkinter.CTkEntry(ventana, text_font="Sylfaen 14")
inputEmail.pack(pady=12, padx=10)

sendInput = customtkinter.CTkButton(
    ventana,
    text="enviar",
    width=6,
    height=2,
    command=lambda: button1Command(nuevoID, boolFlagInput),
)
sendInput.pack(pady=12, padx=10)

ventana.mainloop()


"""
IDEAS:
    PODER ENVIAR EMAILS DE CHECKEO(INVESTIGAR)
"""
