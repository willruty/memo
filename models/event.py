from database import get_db, get_cursor

class Event:
    
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
        conn = get_db()
        cursor = get_cursor(conn)
        
        try:
            cursor.execute('''
                INSERT INTO events (user_id, title, description, location, date, visibility, cover_image)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, title, description, location, date, visibility, cover_image))
            event_id = cursor.lastrowid
            
            conn.commit()
            
            cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
            row = cursor.fetchone()
            
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
            return None
    
    @staticmethod
    def find_by_id(event_id):
        conn = get_db()
        cursor = get_cursor(conn)
        
        cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
        row = cursor.fetchone()
        
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
        conn = get_db()
        cursor = get_cursor(conn)
        
        cursor.execute('''
            SELECT * FROM events 
            WHERE user_id = ? 
            ORDER BY date DESC, created_at DESC
        ''', (user_id,))
        
        rows = cursor.fetchall()
        
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
        conn = get_db()
        cursor = get_cursor(conn)
        
        cursor.execute('''
            SELECT e.*, u.name as user_name,
                   (SELECT COUNT(*) FROM likes WHERE event_id = e.id) as likes_count,
                   (SELECT COUNT(*) FROM comments WHERE event_id = e.id) as comments_count,
                   (SELECT COUNT(*) FROM photos WHERE event_id = e.id) as photos_count
            FROM events e
            JOIN users u ON e.user_id = u.id
            WHERE e.visibility = 'public'
            ORDER BY e.date DESC, e.created_at DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        
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
            event.likes_count = row['likes_count']
            event.comments_count = row['comments_count']
            event.photos_count = row['photos_count']
            events.append(event)
        
        return events
    
    @staticmethod
    def find_popular_events(limit=10):
        conn = get_db()
        cursor = get_cursor(conn)
        
        cursor.execute('''
            SELECT e.*, u.name as user_name,
                   COUNT(DISTINCT l.id) as likes_count,
                   COUNT(DISTINCT c.id) as comments_count,
                   COUNT(DISTINCT p.id) as photos_count,
                   (COUNT(DISTINCT l.id) + COUNT(DISTINCT c.id) * 2 + COUNT(DISTINCT p.id)) as popularity_score
            FROM events e
            JOIN users u ON e.user_id = u.id
            LEFT JOIN likes l ON e.id = l.event_id
            LEFT JOIN comments c ON e.id = c.event_id
            LEFT JOIN photos p ON e.id = p.event_id
            WHERE e.visibility = 'public'
            GROUP BY e.id, e.title, e.description, e.location, e.date, e.visibility, e.cover_image, e.created_at, e.user_id, u.name
            ORDER BY popularity_score DESC, e.date DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        
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
            event.likes_count = row['likes_count']
            event.comments_count = row['comments_count']
            event.photos_count = row['photos_count']
            event.popularity_score = row['popularity_score']
            events.append(event)
        
        return events
    
    def update(self, title, description, location, date, visibility, cover_image=None):
        conn = get_db()
        cursor = get_cursor(conn)
        
        try:
            if cover_image:
                cursor.execute('''
                    UPDATE events 
                    SET title = ?, description = ?, location = ?, date = ?, 
                        visibility = ?, cover_image = ?
                    WHERE id = ?
                ''', (title, description, location, date, visibility, cover_image, self.id))
            else:
                cursor.execute('''
                    UPDATE events 
                    SET title = ?, description = ?, location = ?, date = ?, visibility = ?
                    WHERE id = ?
                ''', (title, description, location, date, visibility, self.id))
            
            conn.commit()
            
            self.title = title
            self.description = description
            self.location = location
            self.date = date
            self.visibility = visibility
            if cover_image:
                self.cover_image = cover_image
            
            return True
        except Exception as e:
            return False
    
    def delete(self):
        conn = get_db()
        cursor = get_cursor(conn)
        
        cursor.execute('DELETE FROM events WHERE id = ?', (self.id,))
        conn.commit()
        return True
    
    def is_owner(self, user_id):
        return self.user_id == user_id
