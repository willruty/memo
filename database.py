import os
import sys

try:
    import psycopg2 as psycopg
    from psycopg2.extras import DictCursor, RealDictCursor
    PSYCOPG_VERSION = 2
except ImportError:
    try:
        import psycopg
        PSYCOPG_VERSION = 3
    except ImportError:
        raise ImportError("Instale psycopg2-binary: pip install psycopg2-binary")

def get_db():
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        error_msg = "DATABASE_URL environment variable is required."
        print(f"ERRO: {error_msg}", file=sys.stderr)
        raise ValueError(error_msg)
    
    try:
        from urllib.parse import urlparse
        parsed = urlparse(DATABASE_URL)
        db_path = parsed.path[1:] if parsed.path else 'postgres'
        if '?' in db_path:
            db_path = db_path.split('?')[0]
        
        hostname = parsed.hostname
        resolved_ip = None
        original_hostname = hostname
        
        try:
            import socket
            addr_info = socket.getaddrinfo(hostname, parsed.port or 5432, socket.AF_UNSPEC, socket.SOCK_STREAM)
            if addr_info:
                ipv4 = [a for a in addr_info if a[0] == socket.AF_INET]
                if ipv4:
                    resolved_ip = ipv4[0][4][0]
                else:
                    ipv6 = [a for a in addr_info if a[0] == socket.AF_INET6]
                    if ipv6:
                        resolved_ip = ipv6[0][4][0]
        except Exception as dns_error:
            if 'db.' in hostname and 'supabase.co' in hostname and 'pooler' not in hostname:
                print(f"⚠️  DNS falhou para {hostname}, usando pooler automaticamente...", file=sys.stderr)
                project_ref = hostname.split('.')[1]
                pooler_host = 'aws-1-sa-east-1.pooler.supabase.com'
                pooler_user = f'postgres.{project_ref}'
                try:
                    pooler_addr = socket.getaddrinfo(pooler_host, 6543, socket.AF_UNSPEC, socket.SOCK_STREAM)
                    if pooler_addr:
                        ipv4_pooler = [a for a in pooler_addr if a[0] == socket.AF_INET]
                        if ipv4_pooler:
                            resolved_ip = ipv4_pooler[0][4][0]
                            hostname = pooler_host
                            from urllib.parse import urlunparse
                            new_netloc = f'{pooler_user}:{parsed.password}@{resolved_ip}:6543'
                            DATABASE_URL = urlunparse((
                                parsed.scheme,
                                new_netloc,
                                '/postgres',
                                parsed.params,
                                parsed.query,
                                parsed.fragment
                            ))
                            parsed = urlparse(DATABASE_URL)
                            db_path = 'postgres'
                            print(f"✅ Usando pooler: {pooler_host} -> {resolved_ip}", file=sys.stderr)
                except Exception as pooler_error:
                    print(f"❌ Pooler também falhou: {pooler_error}", file=sys.stderr)
        
        if resolved_ip:
            hostname = resolved_ip
        
        if 'pooler.supabase.com' in original_hostname or 'pooler.supabase.com' in hostname:
            if 'postgres.' in (parsed.username or ''):
                db_user = parsed.username
            else:
                if 'db.' in original_hostname:
                    project_ref = original_hostname.split('.')[1]
                    db_user = f'postgres.{project_ref}'
                else:
                    db_user = parsed.username or 'postgres'
        else:
            db_user = parsed.username or 'postgres'
        
        conn_params = {
            'database': db_path,
            'user': db_user,
            'password': parsed.password or '',
            'host': hostname,
            'port': parsed.port or 5432,
            'connect_timeout': 10
        }
        
        if 'supabase.co' in original_hostname or 'pooler.supabase.com' in original_hostname or 'pooler.supabase.com' in hostname:
            conn_params['sslmode'] = 'require'
        
        conn = psycopg.connect(**conn_params)
        
        if PSYCOPG_VERSION == 2:
            try:
                conn.set_client_encoding('UTF8')
            except:
                pass
        
        return conn
    except Exception as e:
        import traceback
        error_msg = f"Erro ao conectar ao banco de dados: {e}\n{traceback.format_exc()}"
        print(f"ERRO: {error_msg}", file=sys.stderr)
        raise ConnectionError(f"Erro ao conectar ao banco de dados: {e}. Verifique se DATABASE_URL está correto.")

def get_cursor(conn=None):
    if conn is None:
        conn = get_db()
    
    if PSYCOPG_VERSION == 2:
        return conn.cursor(cursor_factory=RealDictCursor)
    else:
        return conn.cursor()

def init_db():
    conn = get_db()
    cursor = get_cursor(conn)
    
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
            binary_data BYTEA,
            content_type TEXT DEFAULT 'image/jpeg',
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        DO $$ 
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name='photos' AND column_name='binary_data') THEN
                ALTER TABLE photos ADD COLUMN binary_data BYTEA;
            END IF;
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name='photos' AND column_name='content_type') THEN
                ALTER TABLE photos ADD COLUMN content_type TEXT DEFAULT 'image/jpeg';
            END IF;
        END $$;
    ''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_user_id ON events(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_visibility ON events(visibility)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_photos_event_id ON photos(event_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
    
    conn.commit()
    conn.close()
    print("Banco de dados Supabase inicializado com sucesso!")

def create_sample_data():
    conn = get_db()
    cursor = get_cursor(conn)
    
    cursor.execute('SELECT COUNT(*) as count FROM users')
    result = cursor.fetchone()
    count = result['count'] if isinstance(result, dict) else result[0]
    
    if count == 0:
        from werkzeug.security import generate_password_hash
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
