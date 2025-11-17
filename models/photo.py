"""
Modelo de Foto.
Gerencia operações relacionadas a fotos no banco de dados Supabase.
"""
from database import get_db

class Photo:
    """
    Classe que representa uma foto no sistema.
    """
    
    def __init__(self, id=None, event_id=None, filename=None, uploaded_at=None):
        self.id = id
        self.event_id = event_id
        self.filename = filename
        self.uploaded_at = uploaded_at
    
    @staticmethod
    def create(event_id, filename):
        """
        Cria um novo registro de foto no banco de dados.
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO photos (event_id, filename)
                VALUES (%s, %s)
                RETURNING id
            ''', (event_id, filename))
            photo_id = cursor.fetchone()[0]
            
            conn.commit()
            
            cursor.execute('SELECT * FROM photos WHERE id = %s', (photo_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return Photo(
                    id=row['id'],
                    event_id=row['event_id'],
                    filename=row['filename'],
                    uploaded_at=row['uploaded_at']
                )
            return None
        except Exception as e:
            conn.close()
            return None
    
    @staticmethod
    def find_by_id(photo_id):
        """
        Busca uma foto pelo ID.
        """
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM photos WHERE id = %s', (photo_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Photo(
                id=row['id'],
                event_id=row['event_id'],
                filename=row['filename'],
                uploaded_at=row['uploaded_at']
            )
        return None
    
    @staticmethod
    def find_by_event(event_id):
        """
        Busca todas as fotos de um evento.
        """
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM photos 
            WHERE event_id = %s 
            ORDER BY uploaded_at DESC
        ''', (event_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        photos = []
        for row in rows:
            photos.append(Photo(
                id=row['id'],
                event_id=row['event_id'],
                filename=row['filename'],
                uploaded_at=row['uploaded_at']
            ))
        
        return photos
    
    def delete(self):
        """
        Remove a foto do banco de dados.
        """
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM photos WHERE id = %s', (self.id,))
        conn.commit()
        conn.close()
        return True
