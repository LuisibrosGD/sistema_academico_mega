from database.conexion import *
from vista import login



if __name__ == "__main__":
    query = "SELECT * FROM usuarios"
    respuesta = ejecutar_select(query)
    print(respuesta)
