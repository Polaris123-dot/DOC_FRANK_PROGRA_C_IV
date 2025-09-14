import mysql.connector
from mysql.connector import Error

def crear_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",        # Servidor (si usas Workbench local, es localhost)
            user="root",             # Tu usuario de MySQL
            password="1234", # Contraseña que pusiste en la instalación
            database="persona"      # El nombre de tu base de datos
        )
        if conexion.is_connected():
            print("✅ Conexión exitosa a la base de datos")
            return conexion
    except Error as e:
        print(f"❌ Error al conectar: {e}")
        return None

def insertar_persona(idpersona, nombre, apellidos, edad, direccion, correo):
    conexion = crear_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """INSERT INTO persona (idpersona, nombre, apellidos, edad, direccion, correo) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            valores = (idpersona, nombre, apellidos, edad, direccion, correo)
            cursor.execute(query, valores)
            conexion.commit()
            print("✅ Persona insertada correctamente")
        except Error as e:
            print(f"❌ Error al insertar persona: {e}")
        finally:
            cursor.close()
            conexion.close()


def insertar_usuario(idusuario, password, usuario, estado, fecha_registro):
    conexion = crear_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """INSERT INTO usuario (idusuario, password, usuario, estado, fecha_registro) 
                       VALUES (%s, %s, %s, %s, %s)"""
            valores = (idusuario, password, usuario, estado, fecha_registro)
            cursor.execute(query, valores)
            conexion.commit()
            print("✅ Usuario insertado correctamente")
        except Error as e:
            print(f"❌ Error al insertar usuario: {e}")
        finally:
            cursor.close()
            conexion.close()


def relacionar_persona_usuario(idpersona, idusuario):
    conexion = crear_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """INSERT INTO persona_has_usuario (persona_idpersona, usuario_idusuario) 
                       VALUES (%s, %s)"""
            valores = (idpersona, idusuario)
            cursor.execute(query, valores)
            conexion.commit()
            print("✅ Relación persona-usuario insertada correctamente")
        except Error as e:
            print(f"❌ Error al insertar relación: {e}")
        finally:
            cursor.close()
            conexion.close()


# Ejemplo de uso
if __name__ == "__main__":
    insertar_persona(2, "Javier", "Ramírez", "25", "Av. Principal 123", "carlos@mail.com")
    insertar_usuario(2, "USU123", "carlosr", 1, "2025-09-09")
    relacionar_persona_usuario(2, 2)
