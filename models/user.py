from database import get_db, get_cursor
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2

class User:
    
    def __init__(self, id=None, name=None, email=None, password_hash=None, created_at=None):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
    
    @staticmethod
    def create(name, email, password):
        conn = get_db()
        cursor = get_cursor(conn)
        
        try:
            password_hash = generate_password_hash(password)
            
            cursor.execute('''
                INSERT INTO users (name, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING id
            ''', (name, email, password_hash))
            result = cursor.fetchone()
            user_id = result['id'] if isinstance(result, dict) else result[0]
            
            conn.commit()
            
            cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return User(
                    id=row['id'],
                    name=row['name'],
                    email=row['email'],
                    password_hash=row['password_hash'],
                    created_at=row['created_at']
                )
            return None
        except psycopg2.IntegrityError:
            conn.close()
            return None
    
    @staticmethod
    def find_by_email(email):
        conn = get_db()
        cursor = get_cursor(conn)
        
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                id=row['id'],
                name=row['name'],
                email=row['email'],
                password_hash=row['password_hash'],
                created_at=row['created_at']
            )
        return None
    
    @staticmethod
    def find_by_id(user_id):
        conn = get_db()
        cursor = get_cursor(conn)
        
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                id=row['id'],
                name=row['name'],
                email=row['email'],
                password_hash=row['password_hash'],
                created_at=row['created_at']
            )
        return None
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def update_password(self, new_password):
        conn = get_db()
        cursor = get_cursor(conn)
        
        password_hash = generate_password_hash(new_password)
        cursor.execute('''
            UPDATE users SET password_hash = %s WHERE id = %s
        ''', (password_hash, self.id))
        
        conn.commit()
        conn.close()
        return True
    
    def update_profile(self, name, email):
        conn = get_db()
        cursor = get_cursor(conn)
        
        try:
            cursor.execute('''
                UPDATE users SET name = %s, email = %s WHERE id = %s
            ''', (name, email, self.id))
            
            conn.commit()
            conn.close()
            
            self.name = name
            self.email = email
            return True
        except psycopg2.IntegrityError:
            conn.close()
            return False
    
    def delete(self):
        conn = get_db()
        cursor = get_cursor(conn)
        
        cursor.execute('DELETE FROM users WHERE id = %s', (self.id,))
        conn.commit()
        conn.close()
        return True
