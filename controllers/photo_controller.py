from models.photo import Photo
from models.event import Event
import os
from werkzeug.utils import secure_filename
import uuid

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

class PhotoController:
    
    @staticmethod
    def allowed_file(filename):
        if not filename:
            return False
        
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    @staticmethod
    def upload(event_id, user_id, file):
        if not file or not file.filename:
            return False, "Nenhum arquivo foi enviado.", None
        
        if not PhotoController.allowed_file(file.filename):
            return False, "Tipo de arquivo não permitido. Use apenas imagens (PNG, JPG, JPEG, GIF, WEBP).", None
        
        event = Event.find_by_id(event_id)
        
        if not event:
            return False, "Evento não encontrado.", None
        
        if not event.is_owner(user_id):
            return False, "Você não tem permissão para adicionar fotos a este evento.", None
        
        try:
            file.seek(0)
            binary_data = file.read()
            file.seek(0)
            
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            content_type_map = {
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png',
                'gif': 'image/gif',
                'webp': 'image/webp'
            }
            content_type = content_type_map.get(file_extension, 'image/jpeg')
            
            original_filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
            
            photo = Photo.create(event_id, unique_filename, binary_data, content_type)
            
            if photo:
                return True, "Foto enviada com sucesso!", photo
            else:
                return False, "Erro ao salvar foto no banco de dados.", None
        except Exception as e:
            return False, f"Erro ao fazer upload da foto: {str(e)}", None
    
    @staticmethod
    def delete(photo_id, user_id):
        photo = Photo.find_by_id(photo_id)
        
        if not photo:
            return False, "Foto não encontrada."
        
        event = Event.find_by_id(photo.event_id)
        
        if not event:
            return False, "Evento não encontrado."
        
        if not event.is_owner(user_id):
            return False, "Você não tem permissão para excluir esta foto."
        
        if photo.delete():
            return True, "Foto excluída com sucesso!"
        else:
            return False, "Erro ao excluir foto. Tente novamente."
    
    @staticmethod
    def upload_cover_image(file, upload_folder, old_filename=None):
        if not file or not file.filename:
            return False, "Nenhum arquivo foi enviado.", None
        
        if not PhotoController.allowed_file(file.filename):
            return False, "Tipo de arquivo não permitido. Use apenas imagens (PNG, JPG, JPEG, GIF, WEBP).", None
        
        if old_filename:
            old_path = os.path.join(upload_folder, old_filename)
            if os.path.exists(old_path):
                try:
                    os.remove(old_path)
                except Exception:
                    pass
        
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"cover_{uuid.uuid4().hex}.{file_extension}"
        
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        file_path = os.path.join(upload_folder, unique_filename)
        
        try:
            file.save(file_path)
            return True, "Foto de capa enviada com sucesso!", unique_filename
        except Exception as e:
            return False, f"Erro ao fazer upload da foto de capa: {str(e)}", None
