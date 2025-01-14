import psycopg2
from psycopg2.extras import DictCursor


conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def get_order_sum(conn, month):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        query = """
            SELECT c.customer_name, SUM(o.total_amount) AS total_spent
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            WHERE EXTRACT(MONTH FROM o.order_date) = %s
            GROUP BY c.customer_name
        """
        
        cursor.execute(query, (month,))
        
        result = cursor.fetchall()

    output = []
    for row in result:
        customer_name = row['customer_name']  
        total_amount = row['total_spent']  
        output.append(f"Покупатель {customer_name} совершил покупок на сумму {total_amount}")

    return "\n".join(output)
# END
