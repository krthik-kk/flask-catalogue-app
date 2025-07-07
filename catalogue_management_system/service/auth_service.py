from util.db_get_connection import get_connection

class AuthService:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor(dictionary=True)

    def authenticate(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        user = self.cursor.fetchone()
        return user is not None
