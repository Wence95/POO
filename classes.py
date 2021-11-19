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


class Evento:
    def __init__(self, nombre, asistencia, fecha, hora):
        self.nombre = nombre
        self.asistencia = asistencia
        self.fecha = fecha
        self.hora = hora


class Producto:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor


class State:
    def __init__(self, estado=False, username=None):
        self.estado = estado
        self.username = username
