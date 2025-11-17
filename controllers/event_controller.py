from models.event import Event
from datetime import datetime

class EventController:
    
    @staticmethod
    def validate_title(title):
        if not title or not isinstance(title, str):
            return False
        title = title.strip()
        return len(title) >= 3 and len(title) <= 200
    
    @staticmethod
    def validate_description(description):
        if not description or not isinstance(description, str):
            return False
        description = description.strip()
        return len(description) >= 10 and len(description) <= 2000
    
    @staticmethod
    def validate_location(location):
        if not location or not isinstance(location, str):
            return False
        location = location.strip()
        return len(location) >= 3 and len(location) <= 200
    
    @staticmethod
    def validate_date(date_str):
        if not date_str or not isinstance(date_str, str):
            return False
        
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_visibility(visibility):
        return visibility in ['public', 'private']
    
    @staticmethod
    def create(user_id, title, description, location, date, visibility='private', cover_image=None):
        if not title or not description or not location or not date or not visibility:
            return False, "Todos os campos obrigatórios devem ser preenchidos.", None
        
        if not EventController.validate_title(title):
            return False, "Título deve ter entre 3 e 200 caracteres.", None
        
        if not EventController.validate_description(description):
            return False, "Descrição deve ter entre 10 e 2000 caracteres.", None
        
        if not EventController.validate_location(location):
            return False, "Local deve ter entre 3 e 200 caracteres.", None
        
        if not EventController.validate_date(date):
            return False, "Data inválida. Use o formato YYYY-MM-DD.", None
        
        if not EventController.validate_visibility(visibility):
            return False, "Visibilidade deve ser 'public' ou 'private'.", None
        
        event = Event.create(user_id, title, description, location, date, visibility, cover_image)
        
        if event:
            return True, "Evento criado com sucesso!", event
        else:
            return False, "Erro ao criar evento. Tente novamente.", None
    
    @staticmethod
    def update(event_id, user_id, title, description, location, date, visibility, cover_image=None):
        event = Event.find_by_id(event_id)
        
        if not event:
            return False, "Evento não encontrado.", None
        
        if not event.is_owner(user_id):
            return False, "Você não tem permissão para editar este evento.", None
        
        if not title or not description or not location or not date or not visibility:
            return False, "Todos os campos obrigatórios devem ser preenchidos.", None
        
        if not EventController.validate_title(title):
            return False, "Título deve ter entre 3 e 200 caracteres.", None
        
        if not EventController.validate_description(description):
            return False, "Descrição deve ter entre 10 e 2000 caracteres.", None
        
        if not EventController.validate_location(location):
            return False, "Local deve ter entre 3 e 200 caracteres.", None
        
        if not EventController.validate_date(date):
            return False, "Data inválida. Use o formato YYYY-MM-DD.", None
        
        if not EventController.validate_visibility(visibility):
            return False, "Visibilidade deve ser 'public' ou 'private'.", None
        
        if event.update(title, description, location, date, visibility, cover_image):
            return True, "Evento atualizado com sucesso!", event
        else:
            return False, "Erro ao atualizar evento. Tente novamente.", None
    
    @staticmethod
    def delete(event_id, user_id):
        event = Event.find_by_id(event_id)
        
        if not event:
            return False, "Evento não encontrado."
        
        if not event.is_owner(user_id):
            return False, "Você não tem permissão para excluir este evento."
        
        if event.delete():
            return True, "Evento excluído com sucesso!"
        else:
            return False, "Erro ao excluir evento. Tente novamente."
    
    @staticmethod
    def can_view(event_id, user_id=None):
        event = Event.find_by_id(event_id)
        
        if not event:
            return False, None
        
        if event.visibility == 'public':
            return True, event
        
        if user_id and event.is_owner(user_id):
            return True, event
        
        return False, None
