import requests
import pandas as pd
from woocommerce import API
from config import CLIENT_KEY, CLIENT_SECRET, PRODUCTS_SHEET, CONTACTS_SHEET, URL
from funciones import *
import io


def add_products():
    products = [] # Lista donde se alamecenaran los productos procesados
    
    # Descarga CSV
    csv = download_csv(PRODUCTS_SHEET)
    if csv is None:
        print("Error: Failed to connect to Google Sheets...")
        return
    
    # Leemos CSV de una variable string (el io se dedica a falsificar un archivo)
    df = pd.read_csv(io.StringIO(csv.decode("utf-8")), sep=",")

    # Convertimos el objeto de pandas DataFrame a un diccionario python
    data = df.to_dict()
    
    # Rotamos el diccionario generado por pandas en un formato más fácil de usar
    # El vector va asi
    # cada posicion del vector tiene un diccionario
    # este diccionario tiene un elemento por cada columna del excel 
    for i in range(0, len(df)):
        product = {}
        for key in data.keys():
            product[key.lower()] = df[key][i]
        
        products.append(product)            

    # Inicializamos la api de woocommerce
    wcapi = API(
        url=URL,
        consumer_key=CLIENT_KEY,
        consumer_secret=CLIENT_SECRET,
        version="wc/v3"
    )
    
    # Vamos añadiendo las cosas a woocommerce
    for product in products:
        if not is_product_in_db(conn, product["id"]):
            print(f'No esta en la base de datos el producto: {product["id"]}')
            data = {
                "name": product["name"],
                "type": "simple",
                "regular_price": str(float(product["price"])),
                "description": str(product["description"]),  # Sacar de la base de datos, lpm
                "short_description": str(product["description"]),
                "categories": [],
                "images": []
            }
            
            resp = wcapi.post("products", data).json()
            add_product_to_db(conn, data, product["id"], resp["id"])

def add_contacts():
    contacts = [] # Vector donde se guardan los contactos
    
    # Obtener el CSV de Google Sheets
    csv = download_csv(CONTACTS_SHEET)
    if csv is None:
        print("Error: Failed to connect to Google Sheets...")
        return
    
    # Leemos el CSV con pandas
    df = pd.read_csv(io.StringIO(csv.decode("utf-8")), sep=",")
    data = df.to_dict()
    
    # Rotamos el dataframe de pandas para que cada elemento sea un diccionario en un array
    for i in range(0, len(df)):
        contact = {}
        for key in data.keys():
            contact[key.lower()] = df[key][i]
        
        contacts.append(contact)
    
    # Comprobar y añadir, usamos el ID proporcionado por odoo como base
    for contact in contacts:
        if not is_contact_in_db(conn, contact["id"]):
            add_contact_to_db(conn, contact)
            

if __name__ == "__main__":
    conn = db_connection() # Conectar
    add_products() # Añadir productos
    add_contacts() # Añadir contactos
    conn.close() # Desconectar
