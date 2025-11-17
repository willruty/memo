"""
Modelo de Evento.
Gerencia operações relacionadas a eventos no banco de dados Supabase.
"""
from database import get_db

class Event:
    """
    Classe que representa um evento no sistema.
    """
    
    def __init__(self, id=None, user_id=None, title=None, description=None, 
                 location=None, date=None, visibility='private', 
                 cover_image=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.location = location
        self.date = date
        self.visibility = visibility
        self.cover_image = cover_image
        self.created_at = created_at
    
    @staticmethod
    def create(user_id, title, description, location, date, visibility='private', cover_image=None):
        """
        Cria um novo evento no banco de dados.
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO events (user_id, title, description, location, date, visibility, cover_image)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (user_id, title, description, location, date, visibility, cover_image))
            event_id = cursor.fetchone()[0]
            
            conn.commit()
            
            cursor.execute('SELECT * FROM events WHERE id = %s', (event_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return Event(
                    id=row['id'],
                    user_id=row['user_id'],
                    title=row['title'],
                    description=row['description'],
                    location=row['location'],
                    date=row['date'],
                    visibility=row['visibility'],
                    cover_image=row['cover_image'],
                    created_at=row['created_at']
                )
            return None
        except Exception as e:
            conn.close()
            return None
    
    @staticmethod
    def find_by_id(event_id):
        """
        Busca um evento pelo ID.
        """
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM events WHERE id = %s', (event_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Event(
                id=row['id'],
                user_id=row['user_id'],
                title=row['title'],
                description=row['description'],
                location=row['location'],
                date=row['date'],
                visibility=row['visibility'],
                cover_image=row['cover_image'],
                created_at=row['created_at']
            )
        return None
    
    @staticmethod
    def find_by_user(user_id):
        """
        Busca todos os eventos de um usuário.
        """
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM events 
            WHERE user_id = %s 
            ORDER BY date DESC, created_at DESC
        ''', (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        events = []
        for row in rows:
            events.append(Event(
                id=row['id'],
                user_id=row['user_id'],
                title=row['title'],
                description=row['description'],
                location=row['location'],
                date=row['date'],
                visibility=row['visibility'],
                cover_image=row['cover_image'],
                created_at=row['created_at']
            ))
        
        return events
    
    @staticmethod
    def find_public_events(limit=20):
        """
        Busca eventos públicos mais recentes.
        """
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT e.*, u.name as user_name 
            FROM events e
            JOIN users u ON e.user_id = u.id
            WHERE e.visibility = 'public'
            ORDER BY e.date DESC, e.created_at DESC
            LIMIT %s
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        events = []
        for row in rows:
            event = Event(
                id=row['id'],
                user_id=row['user_id'],
                title=row['title'],
                description=row['description'],
                location=row['location'],
                date=row['date'],
                visibility=row['visibility'],
                cover_image=row['cover_image'],
                created_at=row['created_at']
            )
            event.user_name = row['user_name']
            events.append(event)
        
        return events
    
    def update(self, title, description, location, date, visibility, cover_image=None):
        """
        Atualiza os dados do evento.
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            if cover_image:
                cursor.execute('''
                    UPDATE events 
                    SET title = %s, description = %s, location = %s, date = %s, 
                        visibility = %s, cover_image = %s
                    WHERE id = %s
                ''', (title, description, location, date, visibility, cover_image, self.id))
            else:
                cursor.execute('''
                    UPDATE events 
                    SET title = %s, description = %s, location = %s, date = %s, visibility = %s
                    WHERE id = %s
                ''', (title, description, location, date, visibility, self.id))
            
            conn.commit()
            conn.close()
            
            self.title = title
            self.description = description
            self.location = location
            self.date = date
            self.visibility = visibility
            if cover_image:
                self.cover_image = cover_image
            
            return True
        except Exception as e:
            conn.close()
            return False
    
    def delete(self):
        """
        Remove o evento do banco de dados.
        """
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM events WHERE id = %s', (self.id,))
        conn.commit()
        conn.close()
        return True
    
    def is_owner(self, user_id):
        """
        Verifica se o usuário é o dono do evento.
        """
        return self.user_id == user_id
