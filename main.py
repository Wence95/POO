import tkinter

from classes import *
from funcs import *


def main():
    state = State()
    eventList = []
    itemList = []
    listadoUsers = []
    print(state.estado)

    def clearWindow():
        for widgets in frame.winfo_children():
            widgets.destroy()

    def logOut():
        state.estado = False
        state.username = None
        clearWindow()
        setIndex()

    def getUserPassword(username, password):
        for widgets in msg.winfo_children():
            widgets.destroy()
        if checkUserPass(username, password, listadoUsers):
            state.username = username
            state.estado = True
            clearWindow()
            loggedInWindow()
        else:
            etiqueta = tkinter.Label(msg)
            etiqueta.pack()
            etiqueta["text"] = "Usuario o contraseña inválidos"

    def signUp():
        pass

    def mostrarLista(lista):
        pass

    def registrarEvento():
        pass

    def agregarProducto():
        pass

    def loggedInWindow():
        saludo = tkinter.Label(frame)
        saludo["text"] = "Hola, " + state.username
        saludo.pack()

        if getProfile(state.username, listadoUsers) == 'admin':
            userFrame = tkinter.Frame(frame)
            userFrame.pack()
            botonRegistro = tkinter.Button(userFrame, text="Registrar usuario", command=signUp)
            botonRegistro.pack()
            botonListadoUsers = tkinter.Button(userFrame, text="Ver usuarios", command=lambda: mostrarLista(listadoUsers))
            botonListadoUsers.pack()

            eventFrame = tkinter.Frame(frame)
            eventFrame.pack(pady=20)
            botonNewEvent = tkinter.Button(eventFrame, text="Nuevo evento", command=registrarEvento())
            botonNewEvent.pack()
            botonEventList = tkinter.Button(eventFrame, text="Ver lista de eventos", command=lambda: mostrarLista(eventList))
            botonEventList.pack()

            itemFrame = tkinter.Frame(frame)
            itemFrame.pack()
            botonAgregarProducto = tkinter.Button(itemFrame, text="Nuevo producto", command=agregarProducto())
            botonAgregarProducto.pack()
            botonItemList = tkinter.Button(itemFrame, text="Ver lista de productos", command=lambda: mostrarLista(itemList))
            botonItemList.pack()

        boton = tkinter.Button(frame, text="Cerrar sesión", command=logOut)
        boton.pack(side=tkinter.BOTTOM)

    admin = Usuario('admin', 'admin', '0000', 'admin')

    listadoUsers.append(admin)

    ventana = tkinter.Tk()
    ventana.geometry("300x300")
    frame = tkinter.Frame(ventana)
    msg = tkinter.Frame(ventana)

    def setIndex():
        user_msg = tkinter.Label(frame)
        user_msg["text"] = "Ingrese usuario"
        user_msg.pack()

        caja_user = tkinter.Entry(frame)
        caja_user.pack()

        pass_msg = tkinter.Label(frame)
        pass_msg["text"] = "Ingrese contraseña"
        pass_msg.pack()

        caja_pass = tkinter.Entry(frame, show="*")
        caja_pass.pack()

        boton = tkinter.Button(frame, text="Ingresar", command=lambda: getUserPassword(caja_user.get(), caja_pass.get()))
        boton.pack()
        msg.pack()

    frame.pack(fill=tkinter.BOTH, expand=True)
    setIndex()
    ventana.mainloop()


if __name__ == '__main__':
    main()
