import tkinter as tk
import pymysql

from classes import *
from funcs import *
from database import *


def main():
    db = BaseDatos()
    state = State()

    # itemList.append(Producto("Canape", 500))
    # itemList.append(Producto("Minipizza", 1000))
    # itemList.append(Producto("Miniempanada", 1000))
    # itemList.append(Producto("Sushi", 1000))
    # itemList.append(Producto("Minichacarero", 1000))
    # itemList.append(Producto("Jugo", 500))
    # itemList.append(Producto("Bebida", 500))
    # itemList.append(Producto("Pisco sour", 1500))
    # itemList.append(Producto("Champagne", 1500))
    # itemList.append(Producto("Vino", 2000))

    def getProfile(usuario):
        profile = db.seleccionarBD('perfil', 'usuario', "username='"+usuario+"'")
        return profile[0]

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
        userpass = db.seleccionarBD(('username', 'contraseña'), 'usuario',
                         "username='"+username+"' AND contraseña='"+password+"'")
        print(userpass)
        if userpass is not None:
            state.username = username
            state.estado = True
            loggedInWindow()
        # if checkUserPass(username, password, listadoUsers):
        #     state.username = username
        #     state.estado = True
        #     loggedInWindow()

        else:
            etiqueta = tk.Label(msg)
            etiqueta.pack()
            etiqueta["text"] = "Usuario o contraseña inválidos"

    def eliminarElemento(tabla, elemento):
        if tabla == 'cliente':
            db.borrar(elemento, 'rut', tabla)
        elif tabla == 'evento':
            db.borrar(elemento, 'id_evento', tabla)
        elif tabla == 'producto':
            db.borrar(elemento, 'id_producto', tabla)
        else:
            db.borrar(elemento, 'id', tabla)
        mostrarLista(tabla)

    def editarElemento(elemento, tabla):
        if tabla == 'producto':
            valores = db.seleccionarBD(('tipo', 'valor', 'stock'), tabla, "id_producto='"+str(elemento)+"'")
            editarProductoWindow(elemento, valores[0], valores[1], valores[2])
        elif tabla == 'cliente':
            valores = db.seleccionarBD(('nombre', 'rut', 'empresa', 'comuna', 'numero', 'email', 'metodo_pago'),
                                       tabla, "rut='" + str(elemento) + "'")
            if valores[6] == "Tarjeta":
                modo = 1
            elif valores[6] == "Efectivo":
                modo = 2
            elif valores[6] == "Cheque":
                modo = 3
            else:
                modo = 4
            editClientWindow(elemento, valores[0], valores[1], valores[2],
                                 valores[3], valores[4], valores[5], modo)
        elif tabla == 'evento':
            valores = db.seleccionarBD(('rut', 'nombre', 'asistencia', 'fecha'))
            editEventoWindow(valores[0], valores[1], str(valores[2]),
                                  valores[3])
        if tabla == 'usuario':
            if elemento.perfil == "Funcionario":
                p = 1
            else:
                p = 2
            signUpWindow(p, elemento.username, elemento.nombre)

    def signUp(nombre, username, password, option):
        if option.get() == 1:
            perfil = "Funcionario"
        else:
            perfil = "Gestor"
        newUser = Usuario(username, nombre, password, perfil)
        db.ingresar('usuario', ('username', 'nombre', 'contraseña', 'perfil'), newUser.__repr__())
        loggedInWindow()

    def signUpWindow(o=1, user="", name=""):
        clearWindow()
        option = tk.IntVar()
        option.set(o)
        upperFrame = tk.Frame(frame)

        upperFrame.pack(side=tk.TOP)
        tk.Radiobutton(upperFrame, text="Funcionario", variable=option, value=1).pack(side=tk.LEFT)
        tk.Radiobutton(upperFrame, text="Gestor de informes", variable=option, value=2).pack(side=tk.LEFT)

        tk.Label(frame, text="Ingrese nuevo nombre de usuario").pack()
        caja_user = tk.Entry(frame)
        caja_user.insert(tk.END, user)
        caja_user.pack()

        tk.Label(frame, text="Ingrese contraseña").pack()
        caja_pass = tk.Entry(frame, show="*")

        caja_pass.pack()

        tk.Label(frame, text="Ingrese nombre completo").pack()
        caja_name = tk.Entry(frame)
        caja_name.insert(tk.END, name)
        caja_name.pack()

        boton1 = tk.Button(frame, text="Aceptar", command=lambda: signUp(caja_name.get(),
                                                                         caja_user.get(), caja_pass.get(), option))
        boton1.pack()

        boton2 = tk.Button(auxFrame, text="Volver", command=loggedInWindow)
        boton2.pack(side=tk.BOTTOM)

    def detalleEvento(evento):
        clearWindow()
        tk.Label(frame, text="Precio unitario").grid(row=0, column=0)
        tk.Label(frame, text="Producto").grid(row=0, column=1)
        tk.Label(frame, text="Cantidad").grid(row=0, column=2)
        tk.Label(frame, text="Total por producto").grid(row=0, column=3)
        suma = 0
        j = 0
        precio = 0
        nombre = ""
        subtotal = 0
        for producto in evento.productos:
            j += 1
            for p in itemList:
                if producto["producto"] == p.tipo:
                    precio = p.valor
                    nombre = p.tipo
                    subtotal = precio * producto["cantidad"]
                    break
                else:
                    precio = 0
                    nombre = 0
            tk.Label(frame, text=str(precio)).grid(row=j, column=0)
            tk.Label(frame, text=nombre).grid(row=j, column=1)
            tk.Label(frame, text=str(producto["cantidad"])).grid(row=j, column=2)
            tk.Label(frame, text=str(subtotal)).grid(row=j, column=3)
            suma += subtotal
        tk.Label(frame, text="Total").grid(row=j+1, column=0)
        tk.Label(frame, text=str(suma)).grid(row=j+2, column=0)

    def pefunction(q, p, evento, lista):
        lista.remove(evento)
        dicc = {"cantidad": int(q),
                "producto": p}
        evento.productos.append(dicc)
        lista.append(evento)
        loggedInWindow()

    def producto_evento(evento, lista):
        clearWindow()
        tk.Label(frame, text="Agruegue un producto y su cantidad").pack()
        plist = []
        nlist = []
        minimo = evento.asistencia * 3
        product = tk.StringVar()
        cant = tk.StringVar()
        for producto in itemList:
            plist.append(producto.tipo)
        tk.OptionMenu(frame, product, *plist).pack()
        for i in range(minimo-1, 3500):
            nlist.append(str(i+1))
        tk.OptionMenu(frame, cant, *nlist).pack()

        boton1 = tk.Button(frame, text="Aceptar", command=lambda: pefunction(cant.get(),
                                                                             product.get(), evento, lista))
        boton1.pack()

    def mostrarLista(tabla):
        clearWindow()
        i = 0
        if tabla == 'usuario':
            tk.Label(frame, text = "id").grid(row=0, column=0)
            tk.Label(frame, text="Usuario").grid(row=0, column=1)
            tk.Label(frame, text="Nombre").grid(row=0, column=2)
            tk.Label(frame, text="Perfil").grid(row=0, column=3)
        elif tabla == 'evento':
            tk.Label(frame, text = "id").grid(row=0, column=0)
            tk.Label(frame, text="Evento").grid(row=0, column=1)
            tk.Label(frame, text="Asistencia").grid(row=0, column=2)
            tk.Label(frame, text="Fecha").grid(row=0, column=3)
            tk.Label(frame, text="Hora").grid(row=0, column=4)
        elif tabla == 'producto':
            tk.Label(frame, text = "id").grid(row=0, column=0)
            tk.Label(frame, text="Tipo").grid(row=0, column=1)
            tk.Label(frame, text="Valor").grid(row=0, column=2)
            tk.Label(frame, text="Stock").grid(row=0, column=3)
        elif tabla == 'cliente':
            tk.Label(frame, text="RUT").grid(row=0, column=0)
            tk.Label(frame, text="Nombre").grid(row=0, column=1)
            tk.Label(frame, text="Empresa").grid(row=0, column=2)
            tk.Label(frame, text="Comuna").grid(row=0, column=3)
            tk.Label(frame, text="Numero").grid(row=0, column=4)
            tk.Label(frame, text="email").grid(row=0, column=5)
            tk.Label(frame, text="Método de pago").grid(row=0, column=6)

        lista = db.seleccionarTabla(tabla)
        for elemento in lista:
            i += 1
            j = -1
            for word in elemento:
                j += 1
                tk.Label(frame, text=word).grid(row=i, column=j, padx=10, sticky=tk.W)
            if getProfile(state.username) == 'Administrador':
                if tabla == 'usuario':
                    if elemento[3] != "Administrador":
                        # noinspection PyShadowingNames
                        tk.Button(frame, text="Eliminar",
                                  command=lambda elemento=elemento:
                                  eliminarElemento(tabla, elemento[0])).grid(row=i, column=j+1)
                        # noinspection PyShadowingNames
                        tk.Button(frame, text="Editar",
                                  command=lambda elemento=elemento:
                                  editarElemento(elemento[0], tabla)).grid(row=i, column=j+2)
                else:
                    # noinspection PyShadowingNames
                    tk.Button(frame, text="Eliminar",
                              command=lambda elemento=elemento:
                              eliminarElemento(tabla, elemento[0])).grid(row=i, column=j+1)
                    # noinspection PyShadowingNames
                    tk.Button(frame, text="Editar",
                              command=lambda elemento=elemento: editarElemento(elemento[0], tabla)).grid(row=i,
                                                                                                      column=j + 2)

            if not (getProfile(state.username) == "Gestor"):
                if tabla == 'evento':
                    # noinspection PyShadowingNames
                    tk.Button(frame, text="Agregar producto",
                              command=lambda elemento=elemento: producto_evento(elemento[0],
                                                                                tabla)).grid(row=i, column=j + 3)
                    # noinspection PyShadowingNames
                    tk.Button(frame, text="Detalle",
                              command=lambda elemento=elemento: detalleEvento(elemento[0])).grid(row=i, column=j + 4)

        boton2 = tk.Button(auxFrame, text="Volver", command=loggedInWindow)
        boton2.pack(side=tk.BOTTOM)

    def updateClient(nombre, rut, empresa, mail, ciudad, telefono, metodo, id):
        if metodo == 1:
            m = "Tarjeta"
        elif metodo == 2:
            m = "Efectivo"
        elif metodo == 3:
            m = "Cheque"
        else:
            m = "Transferencia"
        newClient = Cliente(nombre, rut, empresa, ciudad, telefono, mail, m)
        db.actualizar('cliente', ('rut', 'nombre', 'empresa', 'comuna', 'numero', 'email', 'metodo_pago'),
                    newClient.__repr__(), id)
        loggedInWindow()

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
        db.ingresar('cliente', ('nombre', 'rut', 'empresa', 'comuna', 'numero', 'email', 'metodo_pago'),
                    newClient.__repr__())
        loggedInWindow()

    def editClientWindow(id, rut="", name="", empresa="", comuna="", numero="", mail="", modo=1):
        clearWindow()

        tk.Label(frame, text="Ingrese rut del cliente").pack()
        caja_rut = tk.Entry(frame)
        caja_rut.insert(tk.END, rut)
        caja_rut.pack()

        tk.Label(frame, text="Ingrese nombre del cliente").pack()
        caja_name = tk.Entry(frame)
        caja_name.insert(tk.END, name)
        caja_name.pack()

        tk.Label(frame, text="Ingrese empresa").pack()
        caja_empresa = tk.Entry(frame)
        caja_empresa.insert(tk.END, empresa)
        caja_empresa.pack()

        tk.Label(frame, text="Ingrese comuna").pack()
        caja_city = tk.Entry(frame)
        caja_city.insert(tk.END, comuna)
        caja_city.pack()

        tk.Label(frame, text="Ingrese número de teléfono").pack()
        caja_phone = tk.Entry(frame)
        caja_phone.insert(tk.END, numero)
        caja_phone.pack()

        tk.Label(frame, text="Ingrese mail").pack()
        caja_mail = tk.Entry(frame)
        caja_mail.insert(tk.END, mail)
        caja_mail.pack()

        option = tk.IntVar()
        paymentFrame = tk.Frame(frame)
        paymentFrame.pack()
        tk.Radiobutton(paymentFrame, text="Tarjeta", variable=option, value=1).pack(side=tk.LEFT)
        tk.Radiobutton(paymentFrame, text="Efectivo", variable=option, value=2).pack(side=tk.LEFT)
        tk.Radiobutton(paymentFrame, text="Cheque", variable=option, value=3).pack(side=tk.LEFT)
        tk.Radiobutton(paymentFrame, text="Transferencia", variable=option, value=4).pack(side=tk.LEFT)
        option.set(modo)

        boton1 = tk.Button(frame, text="Editar", command=lambda: updateClient(caja_name.get(),
                                                                                 caja_rut.get(), caja_empresa.get(),
                                                                                 caja_mail.get(), caja_city.get(),
                                                                                 caja_phone.get(), option.get(), id))
        boton1.pack()

        boton2 = tk.Button(auxFrame, text="Volver", command=loggedInWindow)
        boton2.pack(side=tk.BOTTOM)

    def registerClientWindow(rut="", name="", empresa="", comuna="", numero="", mail="", modo=1):
        clearWindow()

        tk.Label(frame, text="Ingrese rut del cliente").pack()
        caja_rut = tk.Entry(frame)
        caja_rut.insert(tk.END, rut)
        caja_rut.pack()

        tk.Label(frame, text="Ingrese nombre del cliente").pack()
        caja_name = tk.Entry(frame)
        caja_name.insert(tk.END, name)
        caja_name.pack()

        tk.Label(frame, text="Ingrese empresa").pack()
        caja_empresa = tk.Entry(frame)
        caja_empresa.insert(tk.END, empresa)
        caja_empresa.pack()

        tk.Label(frame, text="Ingrese comuna").pack()
        caja_city = tk.Entry(frame)
        caja_city.insert(tk.END, comuna)
        caja_city.pack()

        tk.Label(frame, text="Ingrese número de teléfono").pack()
        caja_phone = tk.Entry(frame)
        caja_phone.insert(tk.END, numero)
        caja_phone.pack()

        tk.Label(frame, text="Ingrese mail").pack()
        caja_mail = tk.Entry(frame)
        caja_mail.insert(tk.END, mail)
        caja_mail.pack()

        option = tk.IntVar()
        paymentFrame = tk.Frame(frame)
        paymentFrame.pack()
        tk.Radiobutton(paymentFrame, text="Tarjeta", variable=option, value=1).pack(side=tk.LEFT)
        tk.Radiobutton(paymentFrame, text="Efectivo", variable=option, value=2).pack(side=tk.LEFT)
        tk.Radiobutton(paymentFrame, text="Cheque", variable=option, value=3).pack(side=tk.LEFT)
        tk.Radiobutton(paymentFrame, text="Transferencia", variable=option, value=4).pack(side=tk.LEFT)
        option.set(modo)

        boton1 = tk.Button(frame, text="Aceptar", command=lambda: registerClient(caja_name.get(),
                                                                                 caja_rut.get(), caja_empresa.get(),
                                                                                 caja_mail.get(), caja_city.get(),
                                                                                 caja_phone.get(), option.get()))
        boton1.pack()

        boton2 = tk.Button(auxFrame, text="Volver", command=loggedInWindow)
        boton2.pack(side=tk.BOTTOM)

    def registrarEvento(id, nombre, asistencia, fecha_hora, _rut):
        db.actualizar('evento', ('nombre', 'asistencia', 'fecha', 'rut'), (nombre, asistencia, fecha_hora, _rut), id)
        # if bul:
        #    loggedInWindow()
        # else:
        #    registerClientWindow(_rut)

    def registrarEvento(nombre, asistencia, fecha_hora, _rut):
        db.ingresar('evento', ('nombre', 'asistencia', 'fecha', 'rut'),(nombre, asistencia, fecha_hora, _rut))
        # if bul:
        #    loggedInWindow()
        # else:
        #    registerClientWindow(_rut)

    def editEventoWindow(id, rut="", event="", asis="", fecha="2022-01-01 10:00:00", mes="Enero", dia="1", hora="10:00"):
        clearWindow()

        tk.Label(frame, text="Ingrese rut del cliente que hace la reserva, sin puntos y con guion").pack()
        caja_rut = tk.Entry(frame)
        caja_rut.insert(tk.END, rut)
        caja_rut.pack()

        tk.Label(frame, text="Ingrese nombre del nuevo evento").pack()
        caja_event = tk.Entry(frame)
        caja_event.insert(tk.END, event)
        caja_event.pack()

        tk.Label(frame, text="Ingrese cantidad de asistentes").pack()
        caja_asis = tk.Entry(frame)
        caja_asis.insert(tk.END, asis)
        caja_asis.pack()
        reg = ventana.register(callback)
        caja_asis.config(validate="key", validatecommand=(reg, '%P'))

        # timeFrame = tk.Frame(frame)
        tk.Label(frame, text="Ingrese fecha y hora del evento (YYYY-MM-DD HH:MI:SS)").pack()
        caja_time = tk.Entry(frame)
        caja_time.insert(tk.END, fecha)
        caja_time.pack()

        boton1 = tk.Button(frame, text="Aceptar", command=lambda: registrarEvento(id, caja_event.get(),
                                                                                  int(caja_asis.get()),
                                                                                  caja_time.get(),
                                                                                  caja_rut.get()))
        boton1.pack()

        boton2 = tk.Button(auxFrame, text="Volver", command=loggedInWindow)
        boton2.pack(side=tk.BOTTOM)

    def registrarEventoWindow(rut="", event="", asis="", fecha="2022-01-01 10:00:00"):
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
        caja_rut.insert(tk.END, rut)
        caja_rut.pack()

        tk.Label(frame, text="Ingrese nombre del nuevo evento").pack()
        caja_event = tk.Entry(frame)
        caja_event.insert(tk.END, event)
        caja_event.pack()

        tk.Label(frame, text="Ingrese cantidad de asistentes").pack()
        caja_asis = tk.Entry(frame)
        caja_asis.insert(tk.END, asis)
        caja_asis.pack()
        reg = ventana.register(callback)
        caja_asis.config(validate="key", validatecommand=(reg, '%P'))

        # timeFrame = tk.Frame(frame)
        tk.Label(frame, text="Ingrese fecha y hora del evento (YYYY-MM-DD HH:MI:SS)").pack()
        caja_time = tk.Entry(frame)
        caja_time.insert(tk.END, fecha)
        caja_time.pack()
        # monthChoices = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        #                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        # month = tk.StringVar()
        # month.set(mes)
        # m = tk.OptionMenu(timeFrame, month, *monthChoices)
        # dayChoices = []
        # for i in range(31):
        #     dayChoices.append(str(i + 1))
        # day = tk.StringVar()
        # day.set(dia)
        # d = tk.OptionMenu(timeFrame, day, *dayChoices)
        # d.pack(side=tk.LEFT)
        # m.pack(side=tk.LEFT)
        #
        # hourChoices = ["10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30",
        #                "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30",
        #                "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00"]
        # hour = tk.StringVar()
        # hour.set(hora)
        # h = tk.OptionMenu(timeFrame, hour, *hourChoices)
        # h.pack(side=tk.RIGHT, padx=10)
        #
        # timeFrame.pack()

        boton1 = tk.Button(frame, text="Aceptar", command=lambda: registrarEvento(caja_event.get(),
                                                                                  int(caja_asis.get()),
                                                                                  caja_time.get(),
                                                                                  caja_rut.get()))
        boton1.pack()

        boton2 = tk.Button(auxFrame, text="Volver", command=loggedInWindow)
        boton2.pack(side=tk.BOTTOM)

    def agregarProducto(tipo, valor, stock=9999):
        db.ingresar('producto', ('tipo', 'valor', 'stock'), (tipo, valor, stock))
        loggedInWindow()

    def agregarProductoWindow(nombre="", precio="", stock=""):
        clearWindow()

        tk.Label(frame, text="Ingrese nombre del producto").pack()
        caja_name = tk.Entry(frame)
        caja_name.insert(tk.END, nombre)
        caja_name.pack()

        tk.Label(frame, text="Ingrese su precio por unidad").pack()
        caja_precio = tk.Entry(frame)
        caja_precio.insert(tk.END, precio)
        caja_precio.pack()

        reg = ventana.register(callback)
        caja_precio.config(validate="key", validatecommand=(reg, '%P'))

        tk.Label(frame, text="Ingrese el stock del producto").pack()
        caja_stock = tk.Entry(frame)
        caja_stock.insert(tk.END, stock)
        caja_stock.pack()

        caja_stock.config(validate="key", validatecommand=(reg, '%P'))

        boton1 = tk.Button(frame, text="Aceptar", command=lambda: agregarProducto(caja_name.get(),
                                                                                  int(caja_precio.get()),
                                                                                  int(caja_stock.get())))
        boton1.pack()

        boton2 = tk.Button(auxFrame, text="Volver", command=loggedInWindow)
        boton2.pack(side=tk.BOTTOM)

    def editarProducto(id, tipo, valor, stock=9999):
        db.actualizar('producto', ('tipo', 'valor', 'stock'), (tipo, valor, stock), id)
        loggedInWindow()

    def editarProductoWindow(id, nombre="", precio="", stock=""):
        clearWindow()

        tk.Label(frame, text="Ingrese nombre del producto").pack()
        caja_name = tk.Entry(frame)
        caja_name.insert(tk.END, nombre)
        caja_name.pack()

        tk.Label(frame, text="Ingrese su precio por unidad").pack()
        caja_precio = tk.Entry(frame)
        caja_precio.insert(tk.END, precio)
        caja_precio.pack()

        reg = ventana.register(callback)
        caja_precio.config(validate="key", validatecommand=(reg, '%P'))

        tk.Label(frame, text="Ingrese el stock del producto").pack()
        caja_stock = tk.Entry(frame)
        caja_stock.insert(tk.END, stock)
        caja_stock.pack()

        caja_stock.config(validate="key", validatecommand=(reg, '%P'))

        boton1 = tk.Button(frame, text="Editar", command=lambda: editarProducto(id, caja_name.get(),
                                                                                  int(caja_precio.get()),
                                                                                  int(caja_stock.get())))
        boton1.pack()

        boton2 = tk.Button(auxFrame, text="Volver", command=loggedInWindow)
        boton2.pack(side=tk.BOTTOM)

    def loggedInWindow():
        clearWindow()
        saludo = tk.Label(frame)
        saludo["text"] = "Hola, " + state.username
        saludo.pack()
        tk.Label(frame).pack()

        if getProfile(state.username) == 'Funcionario':
            eventFrame = tk.Frame(frame)
            eventFrame.pack(pady=10)
            botonNewEvent = tk.Button(eventFrame, text="Nuevo evento", command=registrarEventoWindow)
            botonNewEvent.pack()
            botonEventList = tk.Button(eventFrame, text="Ver lista de eventos", command=lambda: mostrarLista('evento'))
            botonEventList.pack()

        if getProfile(state.username) == 'Gestor':
            botonListadoUsers = tk.Button(frame, text="Ver usuarios", command=lambda: mostrarLista('usuario'))
            botonListadoUsers.pack()

            botonEventList = tk.Button(frame, text="Ver lista de eventos", command=lambda: mostrarLista('evento'))
            botonEventList.pack()

            botonItemList = tk.Button(frame, text="Ver lista de productos", command=lambda: mostrarLista('producto'))
            botonItemList.pack()

            botonClientList = tk.Button(frame, text="Ver lista de clientes",
                                        command=lambda: mostrarLista('cliente'))
            botonClientList.pack()

        if getProfile(state.username) == 'Administrador':
            userFrame = tk.Frame(frame)
            userFrame.pack(pady=10)
            botonRegistro = tk.Button(userFrame, text="Registrar usuario", command=signUpWindow)
            botonRegistro.pack()
            botonListadoUsers = tk.Button(userFrame, text="Ver usuarios", command=lambda: mostrarLista('usuario'))
            botonListadoUsers.pack()

            eventFrame = tk.Frame(frame)
            eventFrame.pack(pady=10)
            botonNewEvent = tk.Button(eventFrame, text="Nuevo evento", command=registrarEventoWindow)
            botonNewEvent.pack()
            botonEventList = tk.Button(eventFrame, text="Ver lista de eventos", command=lambda: mostrarLista('evento'))
            botonEventList.pack()

            itemFrame = tk.Frame(frame)
            itemFrame.pack(pady=10)
            botonAgregarProducto = tk.Button(itemFrame, text="Nuevo producto", command=agregarProductoWindow)
            botonAgregarProducto.pack()
            botonItemList = tk.Button(itemFrame, text="Ver lista de productos", command=lambda: mostrarLista('producto'))
            botonItemList.pack()

            clientFrame = tk.Frame(frame)
            clientFrame.pack()
            botonRegistrarCliente = tk.Button(clientFrame, text="Registrar cliente", command=registerClientWindow)
            botonRegistrarCliente.pack()
            botonClientList = tk.Button(clientFrame, text="Ver lista de clientes",
                                        command=lambda: mostrarLista('cliente'))
            botonClientList.pack()

        boton = tk.Button(auxFrame, text="Cerrar sesión", command=logOut)
        boton.pack()

    ventana = tk.Tk()
    auxFrame = tk.Frame(ventana)
    ventana.geometry("800x450")
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
