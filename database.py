import os
import sqlite3
import threading

_thread_local = threading.local()
DB_PATH = os.getenv('DATABASE_PATH', 'memo.db')

def get_db():
    if hasattr(_thread_local, 'conn') and _thread_local.conn:
        try:
            _thread_local.conn.execute('SELECT 1')
            return _thread_local.conn
        except:
            _thread_local.conn = None
    
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON')
        _thread_local.conn = conn
        return conn
    except Exception as e:
        raise ConnectionError(f"Erro ao conectar ao banco de dados: {e}")

def close_db():
    if hasattr(_thread_local, 'conn') and _thread_local.conn:
        try:
            _thread_local.conn.close()
        except:
            pass
        finally:
            _thread_local.conn = None

def get_cursor(conn=None):
    if conn is None:
        conn = get_db()
    return conn.cursor()

def migrate_db():
    conn = get_db()
    cursor = get_cursor(conn)
    
    try:
        cursor.execute("PRAGMA table_info(photos)")
        photo_columns = [row[1] for row in cursor.fetchall()]
        
        if 'user_id' not in photo_columns:
            cursor.execute('ALTER TABLE photos ADD COLUMN user_id INTEGER')
            cursor.execute('UPDATE photos SET user_id = (SELECT user_id FROM events WHERE events.id = photos.event_id LIMIT 1) WHERE user_id IS NULL')
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        pass

def init_db():
    conn = get_db()
    cursor = get_cursor(conn)
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            binary_data BLOB,
            content_type TEXT DEFAULT 'image/jpeg',
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(event_id, user_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_follows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            follower_id INTEGER NOT NULL,
            following_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (following_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(follower_id, following_id),
            CHECK(follower_id != following_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event_participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(event_id, user_id)
        )
    ''')
    
    conn.commit()
    
    migrate_db()
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_user_id ON events(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_visibility ON events(visibility)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_photos_event_id ON photos(event_id)')
    try:
        cursor.execute("PRAGMA table_info(photos)")
        photo_columns = [row[1] for row in cursor.fetchall()]
        if 'user_id' in photo_columns:
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_photos_user_id ON photos(user_id)')
    except:
        pass
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_comments_event_id ON comments(event_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_comments_user_id ON comments(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_likes_event_id ON likes(event_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_likes_user_id ON likes(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
    
    conn.commit()

def create_sample_data():
    conn = get_db()
    cursor = get_cursor(conn)
    
    cursor.execute('SELECT COUNT(*) as count FROM users')
    result = cursor.fetchone()
    count = result['count'] if hasattr(result, 'keys') else result[0]
    
    if count == 0:
        from werkzeug.security import generate_password_hash
        password_hash = generate_password_hash('admin123')
        cursor.execute('''
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
        ''', ('Usuário Admin', 'admin@memo.com', password_hash))
        
        conn.commit()

def call_procedure_get_event_stats(event_id):
    conn = get_db()
    cursor = get_cursor(conn)
    
    cursor.execute('''
        SELECT 
            e.id,
            e.title,
            COUNT(DISTINCT p.id) as total_photos,
            COUNT(DISTINCT c.id) as total_comments,
            COUNT(DISTINCT l.id) as total_likes,
            COUNT(DISTINCT ep.user_id) as total_participants
        FROM events e
        LEFT JOIN photos p ON e.id = p.event_id
        LEFT JOIN comments c ON e.id = c.event_id
        LEFT JOIN likes l ON e.id = l.event_id
        LEFT JOIN event_participants ep ON e.id = ep.event_id
        WHERE e.id = ?
        GROUP BY e.id, e.title
    ''', (event_id,))
    
    result = cursor.fetchone()
    if result:
        return {
            'event_id': result['id'],
            'title': result['title'],
            'total_photos': result['total_photos'],
            'total_comments': result['total_comments'],
            'total_likes': result['total_likes'],
            'total_participants': result['total_participants']
        }
    return None

def call_procedure_get_user_activity(user_id):
    conn = get_db()
    cursor = get_cursor(conn)
    
    cursor.execute('''
        SELECT 
            u.id,
            u.name,
            (SELECT COUNT(*) FROM events WHERE user_id = u.id) as total_events,
            (SELECT COUNT(*) FROM photos WHERE user_id = u.id) as total_photos,
            (SELECT COUNT(*) FROM comments WHERE user_id = u.id) as total_comments,
            (SELECT COUNT(*) FROM likes WHERE user_id = u.id) as total_likes_given,
            (SELECT COUNT(*) FROM user_follows WHERE follower_id = u.id) as total_following,
            (SELECT COUNT(*) FROM user_follows WHERE following_id = u.id) as total_followers
        FROM users u
        WHERE u.id = ?
    ''', (user_id,))
    
    result = cursor.fetchone()
    if result:
        return {
            'user_id': result['id'],
            'name': result['name'],
            'total_events': result['total_events'],
            'total_photos': result['total_photos'],
            'total_comments': result['total_comments'],
            'total_likes_given': result['total_likes_given'],
            'total_following': result['total_following'],
            'total_followers': result['total_followers']
        }
    return None

if __name__ == '__main__':
    init_db()
    create_sample_data()
