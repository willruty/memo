"""
Controller de Fotos.
Gerencia upload, download e exclusão de fotos.
"""
from models.photo import Photo
from models.event import Event
import os
from werkzeug.utils import secure_filename
import uuid

# Extensões permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

class PhotoController:
    """
    Controller responsável por operações de fotos.
    """
    
    @staticmethod
    def allowed_file(filename):
        """
        Verifica se o arquivo tem extensão permitida.
        
        Args:
            filename: Nome do arquivo
        
        Returns:
            bool: True se a extensão for permitida
        """
        if not filename:
            return False
        
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    @staticmethod
    def upload(event_id, user_id, file, upload_folder):
        """
        Faz upload de uma foto para um evento.
        
        Args:
            event_id: ID do evento
            user_id: ID do usuário (para verificar permissão)
            file: Arquivo enviado
            upload_folder: Pasta onde salvar o arquivo
        
        Returns:
            tuple: (success: bool, message: str, photo: Photo|None)
        """
        # Validações
        if not file or not file.filename:
            return False, "Nenhum arquivo foi enviado.", None
        
        if not PhotoController.allowed_file(file.filename):
            return False, "Tipo de arquivo não permitido. Use apenas imagens (PNG, JPG, JPEG, GIF, WEBP).", None
        
        # Verifica se o evento existe e se o usuário tem permissão
        event = Event.find_by_id(event_id)
        
        if not event:
            return False, "Evento não encontrado.", None
        
        if not event.is_owner(user_id):
            return False, "Você não tem permissão para adicionar fotos a este evento.", None
        
        # Gera nome único para o arquivo
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        
        # Cria a pasta de uploads se não existir
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # Salva o arquivo
        file_path = os.path.join(upload_folder, unique_filename)
        
        try:
            file.save(file_path)
            
            # Cria registro no banco de dados
            photo = Photo.create(event_id, unique_filename)
            
            if photo:
                return True, "Foto enviada com sucesso!", photo
            else:
                # Remove o arquivo se falhar ao salvar no banco
                if os.path.exists(file_path):
                    os.remove(file_path)
                return False, "Erro ao salvar foto no banco de dados.", None
        except Exception as e:
            return False, f"Erro ao fazer upload da foto: {str(e)}", None
    
    @staticmethod
    def delete(photo_id, user_id, upload_folder):
        """
        Exclui uma foto.
        
        Args:
            photo_id: ID da foto
            user_id: ID do usuário (para verificar permissão)
            upload_folder: Pasta onde o arquivo está salvo
        
        Returns:
            tuple: (success: bool, message: str)
        """
        # Busca a foto
        photo = Photo.find_by_id(photo_id)
        
        if not photo:
            return False, "Foto não encontrada."
        
        # Verifica se o usuário tem permissão (através do evento)
        event = Event.find_by_id(photo.event_id)
        
        if not event:
            return False, "Evento não encontrado."
        
        if not event.is_owner(user_id):
            return False, "Você não tem permissão para excluir esta foto."
        
        # Remove o arquivo físico
        file_path = os.path.join(upload_folder, photo.filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                pass  # Continua mesmo se não conseguir remover o arquivo
        
        # Remove do banco de dados
        if photo.delete():
            return True, "Foto excluída com sucesso!"
        else:
            return False, "Erro ao excluir foto. Tente novamente."
    
    @staticmethod
    def get_file_path(filename, upload_folder):
        """
        Obtém o caminho completo do arquivo.
        
        Args:
            filename: Nome do arquivo
            upload_folder: Pasta onde o arquivo está salvo
        
        Returns:
            str: Caminho completo do arquivo ou None se não existir
        """
        if not filename:
            return None
        
        file_path = os.path.join(upload_folder, filename)
        
        if os.path.exists(file_path):
            return file_path
        
        return None
    
    @staticmethod
    def upload_cover_image(file, upload_folder, old_filename=None):
        """
        Faz upload de uma imagem de capa para um evento.
        
        Args:
            file: Arquivo enviado
            upload_folder: Pasta onde salvar o arquivo
            old_filename: Nome do arquivo antigo (para remover se existir)
        
        Returns:
            tuple: (success: bool, message: str, filename: str|None)
        """
        # Validações
        if not file or not file.filename:
            return False, "Nenhum arquivo foi enviado.", None
        
        if not PhotoController.allowed_file(file.filename):
            return False, "Tipo de arquivo não permitido. Use apenas imagens (PNG, JPG, JPEG, GIF, WEBP).", None
        
        # Remove arquivo antigo se existir
        if old_filename:
            old_path = os.path.join(upload_folder, old_filename)
            if os.path.exists(old_path):
                try:
                    os.remove(old_path)
                except Exception:
                    pass  # Continua mesmo se não conseguir remover
        
        # Gera nome único para o arquivo
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"cover_{uuid.uuid4().hex}.{file_extension}"
        
        # Cria a pasta de uploads se não existir
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # Salva o arquivo
        file_path = os.path.join(upload_folder, unique_filename)
        
        try:
            file.save(file_path)
            return True, "Foto de capa enviada com sucesso!", unique_filename
        except Exception as e:
            return False, f"Erro ao fazer upload da foto de capa: {str(e)}", None

