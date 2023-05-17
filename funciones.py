import requests
import pymysql
from config import HOST, USER, PASSWORD, DB

# Descarga CSV de Google Docs
def download_csv(key: str):
    data = requests.get("https://docs.google.com/spreadsheet/ccc?key=" + key + "&output=csv")
    if data.ok:
        return data.content

# Conectarse a la base de datos, devuelve un objeto de Connection
def db_connection():
    connection = pymysql.connect(
        host = HOST,
        port = 3306,
        user = USER,
        passwd = PASSWORD,
        db = DB
    )
    
    return connection

# comprobar si el producto que quereños añadir existe en la base de datos
def is_product_in_db(connection, id):
    cursor = connection.cursor()
    
    cursor.execute(
        f'SELECT id_odoo FROM int_ref WHERE id_odoo = {id};'
    )
    
    result = cursor.fetchone()
    
    return bool(result)

# Comprobar si el contacto que queremos añadir existe ya en la base de datos
def is_contact_in_db(connection, id):
    cursor = connection.cursor()
    cursor.execute(
        f'SELECT id FROM contacts WHERE id = {id};'
    )
    
    result = cursor.fetchone()
    
    return bool(result)

# Añade un producto a la base de datos
def add_product_to_db(connection, data, id_odoo, id_wc):
    cursor = connection.cursor()
    
    cursor.execute(
        f"""INSERT INTO products (name, regular_price, description, images)
            VALUES ('{data["name"]}', {data["regular_price"]}, '{data["description"]}', '{data["images"]}');"""   
    )
    
    cursor.execute(
        f'INSERT INTO int_ref (id_product, id_odoo, id_wc) VALUES ({cursor.lastrowid}, {id_odoo}, {id_wc});'
    )
    
    connection.commit()

# Añade un contacto a la base de datos
def add_contact_to_db(connection, contact):
    cursor = connection.cursor()
    
    cursor.execute(
        f'INSERT INTO contacts (id, name, email, phone) VALUES ({contact["id"]}, "{contact["nombre"]}", "{contact["correo"]}", "{contact["telefono"]}");'
    )
    
    connection.commit()