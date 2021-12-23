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

    def seleccionarTabla(self, tabla):
        if tabla != 'usuario':
            sql = 'select * from {}'.format(tabla)
        else:
            sql = 'select id, username, nombre, perfil from usuario'
        try:
            self.cursor.execute(sql)
            request = self.cursor.fetchall()
            return request

        except Exception as e:
            raise

    def seleccionarBD(self, columns, tabla, conditions):
        i = 0
        columnString = ''
        if type(columns) is not str:
            for col in columns:
                if i >= 1:
                    columnString += ','
                columnString = columnString + col
                i += 1
        else:
            columnString = columns
        sql = 'select {} from {} where {}'.format(columnString, tabla, conditions)
        print(sql)
        try:
            self.cursor.execute(sql)
            request = self.cursor.fetchone()
            return request

        except Exception as e:
            raise

    def ingresar(self, tabla, columns, values):
        i = 0
        valueString = ''
        columnString = ''
        for val in values:
            if i >= 1:
                valueString += ','
            if type(val) is str:
                valueString = valueString + "'" + val + "'"
            else:
                valueString = valueString + str(val)
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

    def actualizar(self,tabla, columns, values, id):
        i = 0
        valueString = ''
        columnString = ''
        for val in values:
            if i >= 1:
                valueString += ','
            if type(val) is str:
                valueString = valueString + "'" + val + "'"
            else:
                valueString = valueString + str(val)
            i += 1
        j = 0
        for col in columns:
            if j >= 1:
                columnString += ','
            columnString = columnString + col
            j += 1
        sql = "update {} set {} = {} where id={}".format(tabla, columnString, valueString,id)

        try:
            self.cursor.execute(sql)
            self.conexion.commit()
        except Exception as e:
            raise

    def borrar(self, value, column, tabla):
        sql = "delete from {} where {} = {}".format(tabla, column, value)
        try:
            self.cursor.execute(sql)
            self.conexion.commit()
        except Exception as e:
            raise

    def cerrar(self):
        self.conexion.close()

