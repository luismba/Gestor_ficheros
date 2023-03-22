import os
import helpers
import database as db

def iniciar():

    while True:
        helpers.limpiar_pantalla()

        print('-----------------------')
        print('Bienvenidos al gestor')
        print('-----------------------')
        print('(1) Listar clientes')
        print('(2) Buscar clientes')
        print('(3) Añadir un cliente')
        print('(4) Modificar un cliente')
        print('(5) Borrar un cliente')
        print('(6) Salir')
        print('-----------------------')

        opcion = input('> ')

        helpers.limpiar_pantalla()

        if opcion == '1':
            print('Listando a los clientes')
            for cliente in db.Clientes.lista:
                print(cliente)

        elif opcion == '2':
            print('Buscando a los clientes')
            dni = helpers.leer_texto(3,3,"DNI (2 int y 1 char)").upper()
            cliente = db.Cliente.buscar(dni)
            print(cliente) if cliente else print("Cliente no encontrado")

        elif opcion == '3':
            print('Añadiendo cliente')
            dni = None
            while True:
                dni = helpers.leer_texto(3,3,"DNI (2 int y 1 char)").upper()
                if helpers.dni_valido(dni, db.Clientes.lista):
                    break
            nombre = helpers.leer_texto(2,30,"Nombre (2 a 30 char)").capitalize()
            apellido = helpers.leer_texto(2,30,"Apellidos (2 a 30 char)").capitalize()
            db.Clientes.crear(dni, nombre, apellido)

        elif opcion == '4':
            print('Modificando cliente')
            dni = helpers.leer_texto(3,3,"DNI (2 int y 1 char)").upper()
            cliente = db.Clientes.buscar(dni)
            if cliente:
                nombre = helpers.leer_texto(
                    2,30,"DNI (2 a 30 char) [{cliente.nombre}]").capitalize()
                apellido = helpers.leer_texto(
                    2,30,"DNI (2 a 30 char) [{cliente.apellido}]").capitalize()
                db.Clientes.modificar(cliente.dni, nombre, apellido)
                print('Cliente modificado correctamente')
            else:
                print('Cliente modificado correctamente')

        elif opcion == '5':
            print('Borrando cliente')
            dni = helpers.leer_texto(3,3,"DNI (2 int y 1 char)").upper()
            if db.Clientes.borrar(dni):
                print("Cliente borrado correctamente")
            else:
                print('Cliente no encontrado')

        elif opcion == '6':
            print('Adiós')
            break

        input('\nPresiona ENTER para continuar...')

