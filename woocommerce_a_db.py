#!/usr/bin/env python3
from woocommerce import API
from config import CLIENT_KEY, CLIENT_SECRET, URL
from funciones import db_connection

def is_order_in_db(cursor, order):
    cursor.execute(f'SELECT id_order FROM int_ref_products WHERE id_order = {order["id"]};')
    data = cursor.fetchone()[0]
    
    return bool(data)

def main():
    wcapi = API(
        url=URL,
        consumer_key=CLIENT_KEY,
        consumer_secret=CLIENT_SECRET,
        version="wc/v3"
    )

    orders = wcapi.get("orders").json()
    conn = db_connection()
    cursor = conn.cursor()
    
    for order in orders:
        if not is_order_in_db(cursor, order):
            for item in order["line_items"]:
                cursor.execute(f'''SELECT id_product FROM int_ref WHERE id_wc = {item["product_id"]};''')
                internal_product_id = cursor.fetchone()[0]
                
                cursor.execute(f'INSERT INTO int_ref_products (id_product, id_order) VALUES ({internal_product_id}, {order["id"]});')
                conn.commit()
                internal_order_id = cursor.lastrowid
                
                new_product_row = {
                    "id_order": order["id"],
                    "id_product": int(internal_product_id),
                    "quantity": item["quantity"],
                    "total_price": item["total"],
                    "subtotal_price": item["subtotal"]
                }
                
                cursor.execute(f'''INSERT INTO orders (id_order_int, quantity, total_price, subtotal_price) 
                                VALUES ({internal_order_id}, {new_product_row["quantity"]}, {new_product_row["total_price"]}, {new_product_row["subtotal_price"]});''')

                conn.commit()
                
            cursor.execute(f'SELECT id_order FROM int_ref_products WHERE id_order_int = {internal_order_id};')
            order_id = cursor.fetchone()[0]

            new_row = {
                "id_order": order_id,
                "total_sale_price": order["total"],
                "sh_name": order["billing"]["first_name"],
                "sh_surnames": order["billing"]["last_name"],
                "sh_company": order["billing"]["company"],
                "sh_address1": order["billing"]["address_1"],
                "sh_address2": order["billing"]["address_2"],
                "sh_city": order["billing"]["city"],
                "sh_state": order["billing"]["state"],
                "sh_postcode": order["billing"]["postcode"],
                "sh_country": order["billing"]["country"],
                "sh_email": order["billing"]["email"],
                "sh_phone": order["billing"]["phone"]
            }
            
            cursor.execute(f'''INSERT INTO sales (id_order, total_sale_price, sh_name, sh_surnames, sh_company, sh_address1, sh_address2, sh_city, sh_state, sh_postcode, sh_country, sh_email, sh_phone) 
                            VALUES ({new_row["id_order"]}, {new_row["total_sale_price"]}, "{new_row["sh_name"]}", "{new_row["sh_surnames"]}", 
                            "{new_row["sh_company"]}", "{new_row["sh_address1"]}", "{new_row["sh_address2"]}", 
                            "{new_row["sh_city"]}", "{new_row["sh_state"]}", "{new_row["sh_postcode"]}", 
                            "{new_row["sh_country"]}", "{new_row["sh_email"]}", "{new_row["sh_phone"]}");''')

            conn.commit()        
    conn.close()

        
if __name__ == "__main__":
    main()