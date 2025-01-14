import psycopg2
from psycopg2.extras import execute_values

conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def batch_insert(conn, list_of_products):
    sql = '''INSERT INTO products (name, price, quantity) VALUES %s;'''
    with conn.cursor() as cursor:  
         execute_values(cursor, sql, [(product['name'], product['price'], product['quantity']) for product in list_of_products])

def get_all_products(conn):
    sql = "SELECT * FROM products ORDER BY price DESC;"
    with conn.cursor() as cursor:  
        cursor.execute(sql)
        products = cursor.fetchall()
    return products
# END
