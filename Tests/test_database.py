import unittest
import database as db
import copy
import helpers
import config
import csv

class TestDatabase(unittest.TestCase):

    def setUp(self):
        db.Clientes.lista = [
            db.Cliente('20J', 'Pedro', 'García'),
            db.Cliente('78K', 'Paula', 'Gómez'),
            db.Cliente('52P', 'Ana', 'Martínez')
        ]

    def test_buscar_cliente(self):
        cliente_existe = db.Clientes.buscar('20J')
        cliente_no_existe = db.Clientes.buscar('45O')
        self.assertIsNotNone(cliente_existe)
        self.assertIsNone(cliente_no_existe)

    def test_crear_cliente(self):
        cliente = db.Clientes.crear('47U','Pepe','Gómez')
        self.assertEqual(len(db.Clientes.lista),4)
        self.assertEqual(cliente.dni,'47U')
        self.assertEqual(cliente.nombre,'Pepe')
        self.assertEqual(cliente.apellido,'Gómez')

    def test_modificar_cliente(self):
        cliente_a_modificar = copy.copy(db.Clientes.buscar('78K'))
        cliente_modificado = db.Clientes.modificar('78K', 'María', 'Gómez')
        self.assertEqual(cliente_a_modificar.nombre, 'Paula')
        self.assertEqual(cliente_modificado.nombre, 'María')

    def test_borrar_cliente(self):
        cliente_borrado = db.Clientes.borrar('78K')
        busca_cliente_borrado = db.Clientes.buscar('78K')
        self.assertEqual(cliente_borrado.dni,'78K')
        self.assertIsNone(busca_cliente_borrado)

    def test_dni_valido(self):
        self.assertTrue(helpers.dni_valido('00A', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('00558A', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('F369', db.Clientes.lista))
        self.assertTrue(helpers.dni_valido('48Z', db.Clientes.lista))
        
    def test_escritura_csv(self):
        db.Clientes.borrar('20J')
        db.Clientes.borrar('78K')
        db.Clientes.modificar('52P', 'Pedro','Pascal')

        dni, nombre, apellido = None, None, None
        with open(config.DATABASE_PATH, newline='\n') as fichero:
            reader = csv.reader(fichero, delimiter=';')
            dni, nombre, apellido = next(reader)

        self.assertEqual(dni,'52P')
        self.assertEqual(nombre,'Pedro')
        self.assertEqual(apellido,'Pascal')
        
