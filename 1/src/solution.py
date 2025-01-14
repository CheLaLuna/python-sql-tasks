import psycopg2

conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def add_movies(conn):
    sql = "INSERT INTO movies (title, release_year, duration) VALUES ('Godfather', 1972, 175), ('The Green Mile', 1999, 189);"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit() 
    cursor.close()

def get_all_movies(conn):
    sql = "SELECT * FROM movies;"
    cursor = conn.cursor()
    cursor.execute(sql)
    movies = cursor.fetchall()
    cursor.close()
    return movies 
# END
