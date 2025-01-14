import psycopg2

conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def make_cars_table(conn):
    sql = '''CREATE TABLE IF NOT EXISTS cars (
        id SERIAL PRIMARY KEY,
        brand VARCHAR(255),
        model VARCHAR(255)
    );'''
    with conn.cursor() as cursor:  
        cursor.execute(sql)

def populate_cars_table(conn, cars):
    sql = '''INSERT INTO cars (brand, model) VALUES (%s, %s);'''
    with conn.cursor() as cursor:  
        cursor.executemany(sql, cars)

def get_all_cars(conn):
    sql = "SELECT * FROM cars ORDER BY brand ASC;"
    with conn.cursor() as cursor:  
        cursor.execute(sql)
        cars = cursor.fetchall()
    return cars
# END
