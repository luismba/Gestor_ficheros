from tkinter import *
from tkinter import ttk
import helpers
import database as db
from tkinter.messagebox import askokcancel, WARNING

class centerWidgetMixin:
        
    def center_widget(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int(ws/2-w/2)
        y = int(hs/2-h/2)
        self.geometry(f"{x}x{h}+{x}+{y}") #WIDTHxHEIGHT+OFFSET_X+OFFSET_Y


class CreateClientWindow(Toplevel, centerWidgetMixin):

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Crear cliente")
        self.build()
        self.center()

        # Para obligar a realizar acción en la ventana:
        self.transient(parent)
        self.grab_set()

    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        Label(frame, text="DNI (2 ints y 1 upper char)").grid(row=0, column=0)
        Label(frame, text="Nombre (de 2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (de 2 a 30 chars)").grid(row=0, column=2)

        # programamos el evento de cubrir el fichero con lambda y un valor para cada campo
        dni = Entry(frame)
        dni.grid(row=1, column=0)
        dni.bind("<KeyRelease>", lambda event: self.validate(event, index=0))
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, index=1))
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, index=2))

        frame = Frame(self)
        frame.pack(pady=10)

        crear = Button(frame, text="Crear", command=self.create_client)
        crear.configure(state=DISABLED)
        crear.grid(row=0, column=0)
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)

        self.validaciones = [0,0,0]
        self.crear = crear  
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido                                                           

    def create_client(self):
        # Añadimos a la clase padre (master) los campos de la subventana de la subclase
        self.master.treeview.insert(
                parent='', index='end', iid=self.dni.get(), 
                values=(self.dni.get(), self.nombre.get(), self.apellido.get()))
        db.Clientes.crear(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close()

    def close(self):
        self.destroy()
        self.update()        

    def validate(self, event, index):
        valor = event.widget.get()
        if index == 0:
            valido = helpers.dni_valido(valor, db.Clientes.lista)
            event.widget.configure({"bg":"Green" if valido else "Red"})
            
        else:
            valido = valor.isalpha() and len(valor)>= 2 and len(valor)<=30
            event.widget.configure({"bg":"Green" if valido else "Red"})

        # Cambia estado botón si los tres campos son válidos, se apoya en lista validaciones
        self.validaciones[index] = valido
        self.crear.config(state=NORMAL if self.validaciones ==[1,1,1,] else DISABLED)
        
class EditClientWindow(Toplevel, centerWidgetMixin):

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Actualizar cliente")
        self.build()
        self.center()

        # Para obligar a realizar acción en la ventana:
        self.transient(parent)
        self.grab_set()

    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        Label(frame, text="DNI (no editable)").grid(row=0, column=0)
        Label(frame, text="Nombre (de 2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (de 2 a 30 chars)").grid(row=0, column=2)

        # programamos el evento de cubrir el fichero con lambda y un valor para cada campo
        dni = Entry(frame)
        dni.grid(row=1, column=0)
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, index=0))
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, index=1))

        cliente = self.master.treeview.focus()
        campos = self.master.treeview.item(cliente, 'values')
        dni.insert(0, campos[0])
        dni.config(state=DISABLED)
        nombre.insert(0, campos[1])
        apellido.insert(0, campos[2])

        frame = Frame(self)
        frame.pack(pady=10)

        actualizar = Button(frame, text="Actualizar", command=self.edit_client)
        actualizar.grid(row=0, column=0)
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)

        self.validaciones = [1,1]
        self.actualizar = actualizar  
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido                                                           

    def edit_client(self):
        cliente = self.master.treeview.focus()
        self.master.treeview.item(cliente, values=(
            self.dni.get(), self.nombre.get(), self.apellido.get()))
        db.Clientes.modificar(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close()

    def close(self):
        self.destroy()
        self.update()        

    def validate(self, event, index):
        valor = event.widget.get()
        if index == 0:
            valido = helpers.isalpha() and len(valor)>= 2 and len(valor)<=30
            event.widget.configure({"bg":"Green" if valido else "Red"})

        # Cambia estado botón si los tres campos son válidos, se apoya en lista validaciones
        self.validaciones[index] = valido
        self.actualizar.config(state=NORMAL if self.validaciones ==[1,1] else DISABLED)
        


class MainWindow(Tk, centerWidgetMixin):

    def __init__(self):
        super().__init__()
        self.title("Gestor de clientes")
        self.build()
        self.center_widget()

    def build(self):
        frame = Frame(self)
        frame.pack()

        # Vista treeview para fichero con clientes
        treeview = ttk.Treeview(frame)
        treeview['columns'] = ('DNI', 'Nombre', 'Apellido')
        treeview.pack()

        # Definición columnas
        treeview.column("#0",width=0,stretch=NO)
        treeview.column("DNI", anchor=CENTER)
        treeview.column("Nombre", anchor=CENTER)
        treeview.column("Apellido", anchor=CENTER)

        # Definición encabezamiento columnas
        treeview.heading("DNI", text="DNI", anchor=CENTER)
        treeview.heading("Nombre", text="Nombre", anchor=CENTER)
        treeview.heading("Apellido", text="Apellido", anchor=CENTER)

        # Añade scroll para visualizar clientes
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        treeview['yscrollcommand'] = scrollbar.set

        for cliente in db.Clientes.lista:
            treeview.insert(
                parent='', index='end', iid=cliente.dni, 
                values=(cliente.dni, cliente.nombre, cliente.apellido))
        treeview.pack()

        frame = Frame(self)
        frame.pack(pady=20)

        Button(frame, text='Crear', command=self.create).grid(row=0, column=0)
        Button(frame, text='Modificar', command=self.edit).grid(row=0, column=1)
        Button(frame, text='Borrar', command=self.delete).grid(row=0, column=2)

        # Para poder usar en el resto de la clase
        self.treeview = treeview

    def delete(self):
        cliente = self.treeview.focus()
        if cliente:
            campos = self.treeview.item(cliente, "values")
            confirmar = askokcancel(
                title = "Confirmar borrado",
                message=f"¿Borrar {campos[1]} {campos[2]}?",
                icon=WARNING)
            if confirmar:
                self.treeview.delete(cliente)
                db.Clientes.borrar(campos[0])

    def create(self):
        CreateClientWindow(self)

    def edit(self):
        # Solo funciona el botón asociado si hay un registro seleccionado
        if self.treeview.focus():
            EditClientWindow(self)



if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()