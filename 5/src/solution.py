import psycopg2
from datetime import datetime
from psycopg2.extras import DictCursor


conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def create_post(conn, post_data):
    with conn.cursor() as cursor:
        query = """
            INSERT INTO posts (title, content, author_id)
            VALUES (%s, %s, %s) RETURNING id;
        """
        cursor.execute(query, (post_data['title'], post_data['content'], post_data['author_id']))
        post_id = cursor.fetchone()[0]
        conn.commit()
        return post_id

def add_comment(conn, comment_data):
    with conn.cursor() as cursor:
        query = """
            INSERT INTO comments (post_id, author_id, content)
            VALUES (%s, %s, %s) RETURNING id;
        """
        cursor.execute(query, (comment_data['post_id'], comment_data['author_id'], comment_data['content']))
        comment_id = cursor.fetchone()[0]
        conn.commit()
        return comment_id

def get_latest_posts(conn, n):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        query = """
            SELECT p.id, p.title, p.content, p.author_id, p.created_at
            FROM posts p
            ORDER BY p.created_at DESC
            LIMIT %s;
        """
        cursor.execute(query, (n,))
        posts = cursor.fetchall()

        result = []
        for post in posts:
            post_id = post['id']
            cursor.execute("""
                SELECT c.id, c.author_id, c.content, c.created_at
                FROM comments c
                WHERE c.post_id = %s;
            """, (post_id,))
            comments = cursor.fetchall()

            comments_list = [
                {
                    'id': comment['id'],
                    'author_id': comment['author_id'],
                    'content': comment['content'],
                    'created_at': comment['created_at']
                } for comment in comments
            ]

            result.append({
                'id': post['id'],
                'title': post['title'],
                'content': post['content'],
                'author_id': post['author_id'],
                'created_at': post['created_at'],
                'comments': comments_list
            })

        return result
# END
