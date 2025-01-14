import psycopg2
from datetime import datetime
from psycopg2.extras import DictCursor


conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def create_post(conn, post_data):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        query = """
            INSERT INTO posts (title, content, author_id)
            VALUES (%s, %s, %s)
            RETURNING id;
        """
        cursor.execute(query, (post_data['title'], post_data['content'], post_data['author_id']))
        post_id = cursor.fetchone()['id']
    conn.commit()
    return post_id

def add_comment(conn, comment_data):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        query = """
            INSERT INTO comments (post_id, author_id, content)
            VALUES (%s, %s, %s)
            RETURNING id;
        """
        cursor.execute(query, (comment_data['post_id'], comment_data['author_id'], comment_data['content']))
        comment_id = cursor.fetchone()['id']
    conn.commit()
    return comment_id

def get_latest_posts(conn, posts_quantity):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        query_posts = """
            SELECT id, title, content, author_id, created_at
            FROM posts
            ORDER BY created_at DESC
            LIMIT %s;
        """
        cursor.execute(query_posts, (posts_quantity,))
        posts = cursor.fetchall()

        result = []
        for post in posts:
            query_comments = """
                SELECT id, author_id, content, created_at
                FROM comments
                WHERE post_id = %s
                ORDER BY created_at;
            """
            cursor.execute(query_comments, (post['id'],))
            comments = cursor.fetchall()

            result.append({
                'id': post['id'],
                'title': post['title'],
                'content': post['content'],
                'author_id': post['author_id'],
                'created_at': post['created_at'],
                'comments': [
                    {
                        'id': comment['id'],
                        'author_id': comment['author_id'],
                        'content': comment['content'],
                        'created_at': comment['created_at'],
                    }
                    for comment in comments
                ],
            })
    return result
# END
