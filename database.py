"""
Módulo de configuração e inicialização do banco de dados Supabase PostgreSQL.
"""
import os
import psycopg2
from psycopg2.extras import DictCursor
from urllib.parse import urlparse
from werkzeug.security import generate_password_hash

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

def get_db():
    """
    Obtém conexão com o banco de dados Supabase PostgreSQL.
    """
    parsed = urlparse(DATABASE_URL)
    conn = psycopg2.connect(
        database=parsed.path[1:],
        user=parsed.username,
        password=parsed.password,
        host=parsed.hostname,
        port=parsed.port
    )
    return conn

def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas necessárias.
    """
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            location TEXT NOT NULL,
            date DATE NOT NULL,
            visibility TEXT NOT NULL DEFAULT 'private',
            cover_image TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS photos (
            id SERIAL PRIMARY KEY,
            event_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_user_id ON events(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_visibility ON events(visibility)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_photos_event_id ON photos(event_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
    
    conn.commit()
    conn.close()
    print("Banco de dados Supabase inicializado com sucesso!")

def create_sample_data():
    """
    Cria dados de exemplo para testes (opcional).
    """
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as count FROM users')
    count = cursor.fetchone()['count']
    
    if count == 0:
        password_hash = generate_password_hash('admin123')
        cursor.execute('''
            INSERT INTO users (name, email, password_hash)
            VALUES (%s, %s, %s)
        ''', ('Usuário Admin', 'admin@memo.com', password_hash))
        
        conn.commit()
        print("Dados de exemplo criados!")
    
    conn.close()

if __name__ == '__main__':
    init_db()
    create_sample_data()
