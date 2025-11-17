"""
Modelo de Usuário.
Gerencia operações relacionadas a usuários no banco de dados Supabase.
"""
from database import get_db
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2

class User:
    """
    Classe que representa um usuário do sistema.
    """
    
    def __init__(self, id=None, name=None, email=None, password_hash=None, created_at=None):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
    
    @staticmethod
    def create(name, email, password):
        """
        Cria um novo usuário no banco de dados.
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            password_hash = generate_password_hash(password)
            
            cursor.execute('''
                INSERT INTO users (name, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING id
            ''', (name, email, password_hash))
            user_id = cursor.fetchone()[0]
            
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
        """
        Busca um usuário pelo email.
        """
        conn = get_db()
        cursor = conn.cursor()
        
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
        """
        Busca um usuário pelo ID.
        """
        conn = get_db()
        cursor = conn.cursor()
        
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
        """
        Verifica se a senha fornecida corresponde ao hash armazenado.
        """
        return check_password_hash(self.password_hash, password)
    
    def update_password(self, new_password):
        """
        Atualiza a senha do usuário.
        """
        conn = get_db()
        cursor = conn.cursor()
        
        password_hash = generate_password_hash(new_password)
        cursor.execute('''
            UPDATE users SET password_hash = %s WHERE id = %s
        ''', (password_hash, self.id))
        
        conn.commit()
        conn.close()
        return True
    
    def update_profile(self, name, email):
        """
        Atualiza nome e email do usuário.
        """
        conn = get_db()
        cursor = conn.cursor()
        
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
        """
        Remove o usuário do banco de dados.
        """
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM users WHERE id = %s', (self.id,))
        conn.commit()
        conn.close()
        return True
