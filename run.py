import menu
import sys
import ui

if __name__ == '__main__':
    # Modo terminal en ejecucion de programa
    if len(sys.argv) > 1 and sys.argv[1] =="-t":
        menu.iniciar()
    # Modo interfaz gráfica
    else:
        app = ui.MainWindow()
        app.mainloop()
