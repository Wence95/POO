import pymysql


class BaseDatos:
    def __init__(self):
        self.conexion = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='bdpy'
        )
        self.cursor = self.conexion.cursor()
        print("Conexion bd correcta")

    def seleccionarBD(self, id):
        sql = 'select id, nombre, edad from registro where id={}'.format(id)
        try:
            self.cursor.execute(sql)
            usuario = self.cursor.fetchone()

            print("id: ", usuario[0])
            print("nombre: ", usuario[1])
            print("edad: ", usuario[2])

        except Exception as e:
            raise

    def ingresar(self, tabla, values):
        i = 0
        valueString = ''
        for val in values:
            if i >= 1:
                valueString += ','
            valueString += valueString + val
            i += 1
        sql = "insert into {} (id,nombre,edad) values ({})".format(id,tabla, valueString)
        try:
            self.cursor.execute(sql)
            self.conexion.commit()
        except Exception as e:
            print("El valor ya existe",e)
            raise

    def actualizar(self,id,nombre):
        sql = "update registro set nombre='{}' where id={}".format(nombre,id)

        try:
            self.cursor.execute(sql)
            self.conexion.commit()
        except Exception as e:
            raise

    def borrar(self,id):
        sql = "delete from registro where id = {}".format(id)
        try:
            self.cursor.execute(sql)
            self.conexion.commit()
        except Exception as e:
            raise

    def cerrar(self):
        self.conexion.close()


basedat = BaseDatos()
basedat.ingresar('usuario', ('pepe', 'pepe', 'pepe', 'pepe'))
