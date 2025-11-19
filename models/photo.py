from database import get_db, get_cursor

class Photo:
    
    def __init__(self, id=None, event_id=None, filename=None, binary_data=None, content_type=None, uploaded_at=None):
        self.id = id
        self.event_id = event_id
        self.filename = filename
        self.binary_data = binary_data
        self.content_type = content_type or 'image/jpeg'
        self.uploaded_at = uploaded_at
    
    @staticmethod
    def create(event_id, user_id, filename, binary_data, content_type='image/jpeg'):
        conn = get_db()
        cursor = get_cursor(conn)
        
        try:
            cursor.execute('''
                INSERT INTO photos (event_id, user_id, filename, binary_data, content_type)
                VALUES (?, ?, ?, ?, ?)
            ''', (event_id, user_id, filename, binary_data, content_type))
            photo_id = cursor.lastrowid
            
            conn.commit()
            
            cursor.execute('SELECT * FROM photos WHERE id = ?', (photo_id,))
            row = cursor.fetchone()
            
            if row:
                binary_data = row['binary_data']
                if binary_data is not None:
                    if isinstance(binary_data, memoryview):
                        binary_data = bytes(binary_data)
                    elif not isinstance(binary_data, bytes):
                        binary_data = bytes(binary_data)
                
                return Photo(
                    id=row['id'],
                    event_id=row['event_id'],
                    filename=row['filename'],
                    binary_data=binary_data,
                    content_type=row['content_type'] if row['content_type'] else 'image/jpeg',
                    uploaded_at=row['uploaded_at']
                )
            return None
        except Exception as e:
            return None
    
    @staticmethod
    def find_by_id(photo_id):
        conn = get_db()
        cursor = get_cursor(conn)
        
        cursor.execute('SELECT * FROM photos WHERE id = ?', (photo_id,))
        row = cursor.fetchone()
        
        if row:
            binary_data = row['binary_data']
            if binary_data is not None:
                if isinstance(binary_data, memoryview):
                    binary_data = bytes(binary_data)
                elif not isinstance(binary_data, bytes):
                    binary_data = bytes(binary_data)
            
            return Photo(
                id=row['id'],
                event_id=row['event_id'],
                filename=row['filename'],
                binary_data=binary_data,
                content_type=row['content_type'] if row['content_type'] else 'image/jpeg',
                uploaded_at=row['uploaded_at']
            )
        return None
    
    @staticmethod
    def find_by_event(event_id):
        conn = get_db()
        cursor = get_cursor(conn)
        
        cursor.execute('''
            SELECT * FROM photos 
            WHERE event_id = ? 
            ORDER BY uploaded_at DESC
        ''', (event_id,))
        
        rows = cursor.fetchall()
        
        photos = []
        for row in rows:
            binary_data = row['binary_data']
            if binary_data is not None:
                if isinstance(binary_data, memoryview):
                    binary_data = bytes(binary_data)
                elif not isinstance(binary_data, bytes):
                    binary_data = bytes(binary_data)
            
            photos.append(Photo(
                id=row['id'],
                event_id=row['event_id'],
                filename=row['filename'],
                binary_data=binary_data,
                content_type=row['content_type'] if row['content_type'] else 'image/jpeg',
                uploaded_at=row['uploaded_at']
            ))
        
        return photos
    
    def delete(self):
        conn = get_db()
        cursor = get_cursor(conn)
        
        cursor.execute('DELETE FROM photos WHERE id = ?', (self.id,))
        conn.commit()
        return True
