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

    def seleccionarBD(self, columns, tabla, conditions):
        i = 0
        columnString = ''
        for col in columns:
            if i >= 1:
                columnString += ','
            columnString = columnString + col
            i += 1
        sql = 'select {} from {} where {}'.format(columnString, tabla, conditions)
        print(sql)
        try:
            self.cursor.execute(sql)
            usuario = self.cursor.fetchone()
            print(usuario)

        except Exception as e:
            raise

    def ingresar(self, tabla, columns, values):
        i = 0
        valueString = ''
        columnString = ''
        for val in values:
            if i >= 1:
                valueString += ','
            valueString = valueString + "'" + val + "'"
            i += 1
        j = 0
        for col in columns:
            if j >= 1:
                columnString += ','
            columnString = columnString + col
            j += 1
        sql = "insert into {} ({}) values ({})".format(tabla,columnString, valueString)
        print(sql)
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

