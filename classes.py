class Cliente:
    def __init__(self, nombre, rut, empresa, comuna, numero, email, metodo_pago):
        self.nombre = nombre
        self.rut = rut
        self.empresa = empresa
        self.comuna = comuna
        self.numero = numero
        self.email = email
        self.metodoPago = metodo_pago


class Usuario:
    def __init__(self, username, nombre, password, perfil):
        self.username = username
        self.nombre = nombre
        self.password = password
        self.perfil = perfil

    def __repr__(self):
        return self.username, self.nombre, self.perfil


class Evento:
    def __init__(self, nombre, asistencia, fecha, hora, rut):
        self.nombre = nombre
        self.asistencia = asistencia
        self.fecha = fecha
        self.hora = hora
        self.rut = rut

    def __repr__(self):
        return self.nombre, self.asistencia, self.fecha, self.hora


class Producto:
    def __init__(self, tipo, valor, stock=9999):
        self.tipo = tipo
        self.valor = valor
        self.stock = stock

    def __repr__(self):
        return self.tipo, self.valor, self.stock


class State:
    def __init__(self, estado=False, username=None):
        self.estado = estado
        self.username = username
