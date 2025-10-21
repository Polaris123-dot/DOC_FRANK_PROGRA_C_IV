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

# Ejemplo de uso
if __name__ == "__main__":
    conexion = crear_conexion()
    if conexion:
        conexion.close()
