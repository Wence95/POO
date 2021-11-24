import tkinter as tk

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
        # Evitar repetición de mensaje "Usuario o contraseña inválidos"
        for widgets in msg.winfo_children():
            widgets.destroy()
        if checkUserPass(username, password, listadoUsers):
            state.username = username
            state.estado = True
            loggedInWindow()
        else:
            etiqueta = tk.Label(msg)
            etiqueta.pack()
            etiqueta["text"] = "Usuario o contraseña inválidos"

    def signUp():
        pass

    def signUpWindow():
        clearWindow()
        option = tk.IntVar()
        upperFrame = tk.Frame(frame)
        upperFrame.pack(side=tk.TOP)
        tk.Radiobutton(upperFrame, text="Funcionario", variable=option, value=1).pack(side=tk.LEFT)
        tk.Radiobutton(upperFrame, text="Gestor de informes", variable=option, value=2).pack(side=tk.LEFT)

        tk.Label(frame, text="Ingrese nuevo nombre de usuario").pack()
        caja_user = tk.Entry(frame)
        caja_user.pack()

        tk.Label(frame, text="Ingrese contraseña").pack()
        caja_pass = tk.Entry(frame, show="*")
        caja_pass.pack()

        tk.Label(frame, text="Ingrese nombre completo").pack()
        caja_name = tk.Entry(frame)
        caja_name.pack()

        boton1 = tk.Button(frame, text="Aceptar", command=signUp)
        boton1.pack()

        boton2 = tk.Button(frame, text="Volver", command=loggedInWindow)
        boton2.pack(side=tk.BOTTOM)

    def mostrarLista(lista):
        pass

    def registrarEvento():
        pass

    def agregarProducto():
        pass

    def loggedInWindow():
        clearWindow()
        saludo = tk.Label(frame)
        saludo["text"] = "Hola, " + state.username
        saludo.pack()

        if getProfile(state.username, listadoUsers) == 'admin':
            userFrame = tk.Frame(frame)
            userFrame.pack()
            botonRegistro = tk.Button(userFrame, text="Registrar usuario", command=signUpWindow)
            botonRegistro.pack()
            botonListadoUsers = tk.Button(userFrame, text="Ver usuarios", command=lambda: mostrarLista(listadoUsers))
            botonListadoUsers.pack()

            eventFrame = tk.Frame(frame)
            eventFrame.pack(pady=20)
            botonNewEvent = tk.Button(eventFrame, text="Nuevo evento", command=registrarEvento())
            botonNewEvent.pack()
            botonEventList = tk.Button(eventFrame, text="Ver lista de eventos", command=lambda: mostrarLista(eventList))
            botonEventList.pack()

            itemFrame = tk.Frame(frame)
            itemFrame.pack()
            botonAgregarProducto = tk.Button(itemFrame, text="Nuevo producto", command=agregarProducto())
            botonAgregarProducto.pack()
            botonItemList = tk.Button(itemFrame, text="Ver lista de productos", command=lambda: mostrarLista(itemList))
            botonItemList.pack()

        boton = tk.Button(frame, text="Cerrar sesión", command=logOut)
        boton.pack(side=tk.BOTTOM)

    admin = Usuario('admin', 'admin', '0000', 'admin')

    listadoUsers.append(admin)

    ventana = tk.Tk()
    ventana.geometry("300x300")
    frame = tk.Frame(ventana)
    msg = tk.Frame(ventana)

    def setIndex():
        user_msg = tk.Label(frame)
        user_msg["text"] = "Ingrese usuario"
        user_msg.pack()

        caja_user = tk.Entry(frame)
        caja_user.pack()

        pass_msg = tk.Label(frame)
        pass_msg["text"] = "Ingrese contraseña"
        pass_msg.pack()

        caja_pass = tk.Entry(frame, show="*")
        caja_pass.pack()

        boton = tk.Button(frame, text="Ingresar", command=lambda: getUserPassword(caja_user.get(), caja_pass.get()))
        boton.pack()
        msg.pack()

    frame.pack(fill=tk.BOTH, expand=True)
    setIndex()
    ventana.mainloop()


if __name__ == '__main__':
    main()
