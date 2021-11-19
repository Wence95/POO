import tkinter

from classes import *
from funcs import *


def main():
    state = State()
    listadoUsers = []

    def getState(username, password, listado):
        if checkUserPass(username, password, listado):
            state.username = username
            state.estado = True
            etiqueta["text"] = "on"
        else:
            etiqueta["text"] = "ingrese usuario valido"

    admin = Usuario('admin', 'admin', '0000', 'admin')

    listadoUsers.append(admin)

    ventana = tkinter.Tk()
    user_msg = tkinter.Label(ventana)
    user_msg["text"] = "Ingrese usuario"
    user_msg.pack()

    caja_user = tkinter.Entry(ventana)
    caja_user.pack()

    pass_msg = tkinter.Label(ventana)
    pass_msg["text"] = "Ingrese contraseña"
    pass_msg.pack()

    caja_pass = tkinter.Entry(ventana)
    caja_pass.pack()

    boton = tkinter.Button(ventana, text="click", command=lambda: getState(caja_user.get(), caja_pass.get(), listadoUsers))
    boton.pack()

    etiqueta = tkinter.Label(ventana)
    etiqueta.pack()

    ventana.mainloop()


if __name__ == '__main__':
    main()
