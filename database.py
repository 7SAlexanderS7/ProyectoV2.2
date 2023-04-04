import mysql.connector as db
import json

with open('keys.json') as json_file:# Aqui abrimos el archivo .json y lo asignamos a una variable.
    keys = json.load(json_file)# Cargamos en la variable keys la lectura del archivo json.

def convertToBinaryData(filename):
    try:
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData
    except:
        return 0

def write_file(data, path):
    with open(path, 'wb') as file:
        file.write(data)

def registerUser(name, photo):
    id = 0
    inserted = 0

    try:
        con = db.connect(host=keys["host"], user=keys["user"], password=keys["password"], database=keys["database"])# Aqui obtenemos la conexion con la base de datos.
        cursor = con.cursor()# Devuelve un resultado si o si para metodos de insertar.
        sql = "INSERT INTO `user`(name, photo) VALUES (%s,%s)"# Creamos una sentencia de sql para insertar el nombre y la foto.
        pic = convertToBinaryData(photo)# Aqui llamamos a la funcion para convertir a datos binarios la imagen y la almacenamos en una variable.

        if pic:# Pregunta si en la funcion convertToBinaryData no retorna 0, entonces....
            cursor.execute(sql, (name, pic))# Ejecuta la sentencia de sql e inserta el nombre y la foto.
            con.commit()# Confirmamos la insercion debido a que estamos insertando datos.
            inserted = cursor.rowcount# Nos avisa si el usuario se ha insertado correctamente o no.
            id = cursor.lastrowid# Obtenemos el ultimo id insertado.
    except db.Error as e:#Aqui imprimos un mensaje si sale error.
        print(f"Fallo al insertar la imagen: {e}")
    finally:# Cierra la conexion 
        if con.is_connected():
            cursor.close()
            con.close()
    return {"id": id, "affected":inserted}# Returna el id y el insert 

def getUser(name, path):
    id = 0
    rows = 0

    try:
        con = db.connect(host=keys["host"], user=keys["user"], password=keys["password"], database=keys["database"])
        cursor = con.cursor()
        sql = "SELECT * FROM `user` WHERE name = %s"

        cursor.execute(sql, (name,))
        records = cursor.fetchall()

        for row in records:
            id = row[0]
            write_file(row[2], path)
        rows = len(records)
    except db.Error as e:
        print(f"Fallo al leer la imagen: {e}")
    finally:
        if con.is_connected():
            cursor.close()
            con.close()
    return {"id": id, "affected": rows}
