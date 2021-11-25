import tkinter as tk

from classes import *
from funcs import *


def main():
    state = State()
    eventList = []
    itemList = []
    listadoUsers = []
    clientList = []

    itemList.append(Producto("Canape", 500))
    itemList.append(Producto("Minipizza", 1000))
    itemList.append(Producto("Miniempanada", 1000))
    itemList.append(Producto("Sushi", 1000))
    itemList.append(Producto("Minichacarero", 1000))
    itemList.append(Producto("Jugo", 500))
    itemList.append(Producto("Bebida", 500))
    itemList.append(Producto("Pisco sour", 1500))
    itemList.append(Producto("Champagne", 1500))
    itemList.append(Producto("Vino", 2000))

    def clearWindow():
        for widgets in frame.winfo_children():
            widgets.destroy()
        for widgets in auxFrame.winfo_children():
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

    def signUp(nombre, username, password, option):
        if option.get() == 1:
            perfil = "Funcionario"
        else:
            perfil = "Gestor"
        newUser = Usuario(username, nombre, password, perfil)
        listadoUsers.append(newUser)
        loggedInWindow()

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

        boton1 = tk.Button(frame, text="Aceptar", command=lambda: signUp(caja_name.get(),
                                                                         caja_user.get(), caja_pass.get(), option))
        boton1.pack()

        boton2 = tk.Button(auxFrame, text="Volver", command=loggedInWindow)
        boton2.pack(side=tk.BOTTOM)

    def mostrarLista(lista):
        clearWindow()
        i = 0
        if type(lista[0]) is Usuario:
            tk.Label(frame, text="Usuario").grid(row=0, column=0)
            tk.Label(frame, text="Nombre").grid(row=0, column=1)
            tk.Label(frame, text="Perfil").grid(row=0, column=2)
        elif type(lista[0]) is Evento:
            tk.Label(frame, text="Evento").grid(row=0, column=0)
            tk.Label(frame, text="Asistencia").grid(row=0, column=1)
            tk.Label(frame, text="Fecha").grid(row=0, column=2)
            tk.Label(frame, text="Hora").grid(row=0, column=3)
        elif type(lista[0]) is Producto:
            tk.Label(frame, text="Tipo").grid(row=0, column=0)
            tk.Label(frame, text="Valor").grid(row=0, column=1)
            tk.Label(frame, text="Stock").grid(row=0, column=2)
        elif type(lista[0]) is Cliente:
            tk.Label(frame, text="Nombre").grid(row=0, column=0)
            tk.Label(frame, text="RUT").grid(row=0, column=1)
            tk.Label(frame, text="Empresa").grid(row=0, column=2)
            tk.Label(frame, text="Teléfono").grid(row=0, column=3)
            tk.Label(frame, text="E-Mail").grid(row=0, column=4)
            tk.Label(frame, text="Método de pago").grid(row=0, column=5)

        for elemento in lista:
            i += 1
            j = -1
            for word in elemento.__repr__():
                j += 1
                tk.Label(frame, text=word).grid(row=i, column=j, padx=10, sticky=tk.W)

        boton2 = tk.Button(auxFrame, text="Volver", command=loggedInWindow)
        boton2.pack(side=tk.BOTTOM)

    def registerClient(nombre, rut, empresa, mail, ciudad, telefono, metodo):
        if metodo == 1:
            m = "Tarjeta"
        elif metodo == 2:
            m = "Efectivo"
        elif metodo == 3:
            m = "Cheque"
        else:
            m = "Transferencia"
        newClient = Cliente(nombre, rut, empresa, ciudad, telefono, mail, m)
        clientList.append(newClient)
        loggedInWindow()

    def registerClientWindow(rut=""):
        clearWindow()

        tk.Label(frame, text="Ingrese rut del cliente").pack()
        caja_rut = tk.Entry(frame)
        caja_rut.insert(tk.END, rut)
        caja_rut.pack()

        tk.Label(frame, text="Ingrese nombre del cliente").pack()
        caja_name = tk.Entry(frame)
        caja_name.pack()

        tk.Label(frame, text="Ingrese empresa").pack()
        caja_empresa = tk.Entry(frame)
        caja_empresa.pack()

        tk.Label(frame, text="Ingrese comuna").pack()
        caja_city = tk.Entry(frame)
        caja_city.pack()

        tk.Label(frame, text="Ingrese número de teléfono").pack()
        caja_phone = tk.Entry(frame)
        caja_phone.pack()

        tk.Label(frame, text="Ingrese comuna").pack()
        caja_mail = tk.Entry(frame)
        caja_mail.pack()

        option = tk.IntVar()
        paymentFrame = tk.Frame(frame)
        paymentFrame.pack()
        tk.Radiobutton(paymentFrame, text="Tarjeta", variable=option, value=1).pack(side=tk.LEFT)
        tk.Radiobutton(paymentFrame, text="Efectivo", variable=option, value=2).pack(side=tk.LEFT)
        tk.Radiobutton(paymentFrame, text="Cheque", variable=option, value=3).pack(side=tk.LEFT)
        tk.Radiobutton(paymentFrame, text="Transferencia", variable=option, value=4).pack(side=tk.LEFT)

        boton1 = tk.Button(frame, text="Aceptar", command=lambda: registerClient(caja_name.get(),
                                                                                 caja_rut.get(), caja_empresa.get(),
                                                                                 caja_mail.get(), caja_city.get(),
                                                                                 caja_phone.get(), option))
        boton1.pack()

        boton2 = tk.Button(auxFrame, text="Volver", command=loggedInWindow)
        boton2.pack(side=tk.BOTTOM)

    def registrarEvento(nombre, asistencia, fecha, hora, _rut):
        newEvent = Evento(nombre, asistencia, fecha, hora, _rut)
        bul = False
        for cliente in clientList:
            if cliente.rut == _rut:
                bul = True
        eventList.append(newEvent)
        if bul:
            loggedInWindow()
        else:
            registerClientWindow(_rut)

    def registrarEventoWindow():
        # _day = "0"
        #
        # def setDay(dia):
        #     global _day
        #     _day = dia
        #     print(dia)
        #
        # def popMenu(mes):
        #     i = 0
        #     for widgets in timeFrame.winfo_children():
        #         i += 1
        #         if i == 3:
        #             widgets.destroy()
        #     newChoices = []
        #     if mes in ["Enero", "Marzo", "Mayo", "Julio", "Agosto", "Octubre", "Diciembre"]:
        #         dias = 31
        #     elif mes in ["Abril", "Junio", "Septiembre", "Noviembre"]:
        #         dias = 30
        #     else:
        #         dias = 28
        #     for i in range(dias):
        #         newChoices.append(str(i+1))
        #     day = tk.StringVar()
        #     day.set(newChoices[0])
        #     d = tk.OptionMenu(timeFrame, day, *newChoices, command=lambda *args: setDay(day.get()))
        #     d.pack(side=tk.LEFT)

        clearWindow()

        tk.Label(frame, text="Ingrese rut del cliente que hace la reserva, sin puntos y con guion").pack()
        caja_rut = tk.Entry(frame)
        caja_rut.pack()

        tk.Label(frame, text="Ingrese nombre del nuevo evento").pack()
        caja_event = tk.Entry(frame)
        caja_event.pack()

        tk.Label(frame, text="Ingrese cantidad de asistentes").pack()
        caja_asis = tk.Entry(frame)
        caja_asis.pack()
        reg = ventana.register(callback)
        caja_asis.config(validate="key", validatecommand=(reg, '%P'))

        timeFrame = tk.Frame(frame)
        tk.Label(frame, text="Ingrese cantidad de asistentes").pack()
        monthChoices = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        month = tk.StringVar()
        month.set(monthChoices[0])
        m = tk.OptionMenu(timeFrame, month, *monthChoices)
        dayChoices = []
        for i in range(31):
            dayChoices.append(str(i + 1))
        day = tk.StringVar()
        day.set(dayChoices[0])
        d = tk.OptionMenu(timeFrame, day, *dayChoices)
        d.pack(side=tk.LEFT)
        m.pack(side=tk.LEFT)

        hourChoices = ["10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30",
                       "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30",
                       "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00"]
        hour = tk.StringVar()
        hour.set(hourChoices[0])
        h = tk.OptionMenu(timeFrame, hour, *hourChoices)
        h.pack(side=tk.RIGHT, padx=10)

        timeFrame.pack()

        boton1 = tk.Button(frame, text="Aceptar", command=lambda: registrarEvento(caja_event.get(),
                                                                                  int(caja_asis.get()),
                                                                                  month.get() + ', ' + day.get(),
                                                                                  hour.get(),
                                                                                  caja_rut.get()))
        boton1.pack()

        boton2 = tk.Button(auxFrame, text="Volver", command=loggedInWindow)
        boton2.pack(side=tk.BOTTOM)

    def agregarProducto(tipo, valor):
        newProduct = Producto(tipo, valor)
        itemList.append(newProduct)
        loggedInWindow()

    def agregarProductoWindow():
        clearWindow()

        tk.Label(frame, text="Ingrese nombre del producto").pack()
        caja_name = tk.Entry(frame)
        caja_name.pack()

        tk.Label(frame, text="Ingrese su precio por unidad").pack()
        caja_precio = tk.Entry(frame)
        caja_precio.pack()

        reg = ventana.register(callback)
        caja_precio.config(validate="key", validatecommand=(reg, '%P'))

        boton1 = tk.Button(frame, text="Aceptar", command=lambda: agregarProducto(caja_name.get(),
                                                                                  int(caja_precio.get())))
        boton1.pack()

        boton2 = tk.Button(auxFrame, text="Volver", command=loggedInWindow)
        boton2.pack(side=tk.BOTTOM)

    def loggedInWindow():
        clearWindow()
        saludo = tk.Label(frame)
        saludo["text"] = "Hola, " + state.username
        saludo.pack()
        tk.Label(frame).pack()

        if getProfile(state.username, listadoUsers) == 'Funcionario':
            eventFrame = tk.Frame(frame)
            eventFrame.pack(pady=10)
            botonNewEvent = tk.Button(eventFrame, text="Nuevo evento", command=registrarEventoWindow)
            botonNewEvent.pack()
            botonEventList = tk.Button(eventFrame, text="Ver lista de eventos", command=lambda: mostrarLista(eventList))
            botonEventList.pack()

        if getProfile(state.username, listadoUsers) == 'Gestor':
            botonListadoUsers = tk.Button(frame, text="Ver usuarios", command=lambda: mostrarLista(listadoUsers))
            botonListadoUsers.pack()

            botonEventList = tk.Button(frame, text="Ver lista de eventos", command=lambda: mostrarLista(eventList))
            botonEventList.pack()

            botonItemList = tk.Button(frame, text="Ver lista de productos", command=lambda: mostrarLista(itemList))
            botonItemList.pack()

            botonClientList = tk.Button(frame, text="Ver lista de clientes",
                                        command=lambda: mostrarLista(clientList))
            botonClientList.pack()

        if getProfile(state.username, listadoUsers) == 'Administrador':
            userFrame = tk.Frame(frame)
            userFrame.pack(pady=10)
            botonRegistro = tk.Button(userFrame, text="Registrar usuario", command=signUpWindow)
            botonRegistro.pack()
            botonListadoUsers = tk.Button(userFrame, text="Ver usuarios", command=lambda: mostrarLista(listadoUsers))
            botonListadoUsers.pack()

            eventFrame = tk.Frame(frame)
            eventFrame.pack(pady=10)
            botonNewEvent = tk.Button(eventFrame, text="Nuevo evento", command=registrarEventoWindow)
            botonNewEvent.pack()
            botonEventList = tk.Button(eventFrame, text="Ver lista de eventos", command=lambda: mostrarLista(eventList))
            botonEventList.pack()

            itemFrame = tk.Frame(frame)
            itemFrame.pack(pady=10)
            botonAgregarProducto = tk.Button(itemFrame, text="Nuevo producto", command=agregarProductoWindow)
            botonAgregarProducto.pack()
            botonItemList = tk.Button(itemFrame, text="Ver lista de productos", command=lambda: mostrarLista(itemList))
            botonItemList.pack()

            clientFrame = tk.Frame(frame)
            clientFrame.pack()
            botonRegistrarCliente = tk.Button(clientFrame, text="Registrar cliente", command=registerClientWindow)
            botonRegistrarCliente.pack()
            botonClientList = tk.Button(clientFrame, text="Ver lista de clientes",
                                        command=lambda: mostrarLista(clientList))
            botonClientList.pack()

        boton = tk.Button(auxFrame, text="Cerrar sesión", command=logOut)
        boton.pack()

    admin = Usuario('admin', 'admin', '0000', 'Administrador')

    listadoUsers.append(admin)

    ventana = tk.Tk()
    auxFrame = tk.Frame(ventana)
    ventana.geometry("600x450")
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
    auxFrame.pack()
    setIndex()
    ventana.mainloop()


if __name__ == '__main__':
    main()
