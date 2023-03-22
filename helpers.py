import os
import platform # librería para funciones relacionadas con SO
import re

def limpiar_pantalla():
    if platform.system() == "Windows":
        os.system('cls') # En windows se usa cls en terminal
    else:
        os.system('clear')

def leer_texto(longitud_min=0, longitud_max=100, mensaje=None):
    print(mensaje) if mensaje else None
    while True:
        texto = input("> ")
        if len(texto) >= longitud_min and len(texto) <= longitud_max:
            return texto

def dni_valido(dni, lista):
    if not re.match('[0-9]{2}[A-Z]$',dni):
        return False
    for client in lista:
        if client.dni == dni:
            print("DNI usado por otro cliente")
            return False
    return True
