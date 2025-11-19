from database import get_db, get_cursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

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
                VALUES (?, ?, ?)
            ''', (name, email, password_hash))
            user_id = cursor.lastrowid
            
            conn.commit()
            
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            
            if row:
                return User(
                    id=row['id'],
                    name=row['name'],
                    email=row['email'],
                    password_hash=row['password_hash'],
                    created_at=row['created_at']
                )
            return None
        except sqlite3.IntegrityError:
            return None
    
    @staticmethod
    def find_by_email(email):
        try:
            conn = get_db()
            cursor = get_cursor(conn)
            
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            row = cursor.fetchone()
            
            if row:
                return User(
                    id=row['id'],
                    name=row['name'],
                    email=row['email'],
                    password_hash=row['password_hash'],
                    created_at=row['created_at']
                )
            return None
        except Exception as e:
            raise
    
    @staticmethod
    def find_by_id(user_id):
        conn = get_db()
        cursor = get_cursor(conn)
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        
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
            UPDATE users SET password_hash = ? WHERE id = ?
        ''', (password_hash, self.id))
        
        conn.commit()
        return True
