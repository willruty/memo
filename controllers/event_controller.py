"""
Controller de Eventos.
Gerencia criação, edição, exclusão e listagem de eventos.
"""
from models.event import Event
from datetime import datetime

class EventController:
    """
    Controller responsável por operações de eventos.
    """
    
    @staticmethod
    def validate_title(title):
        """
        Valida título do evento.
        
        Args:
            title: Título a ser validado
        
        Returns:
            bool: True se o título for válido
        """
        if not title or not isinstance(title, str):
            return False
        title = title.strip()
        return len(title) >= 3 and len(title) <= 200
    
    @staticmethod
    def validate_description(description):
        """
        Valida descrição do evento.
        
        Args:
            description: Descrição a ser validada
        
        Returns:
            bool: True se a descrição for válida
        """
        if not description or not isinstance(description, str):
            return False
        description = description.strip()
        return len(description) >= 10 and len(description) <= 2000
    
    @staticmethod
    def validate_location(location):
        """
        Valida local do evento.
        
        Args:
            location: Local a ser validado
        
        Returns:
            bool: True se o local for válido
        """
        if not location or not isinstance(location, str):
            return False
        location = location.strip()
        return len(location) >= 3 and len(location) <= 200
    
    @staticmethod
    def validate_date(date_str):
        """
        Valida data do evento.
        
        Args:
            date_str: Data em formato string (YYYY-MM-DD)
        
        Returns:
            bool: True se a data for válida
        """
        if not date_str or not isinstance(date_str, str):
            return False
        
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_visibility(visibility):
        """
        Valida visibilidade do evento.
        
        Args:
            visibility: 'public' ou 'private'
        
        Returns:
            bool: True se a visibilidade for válida
        """
        return visibility in ['public', 'private']
    
    @staticmethod
    def create(user_id, title, description, location, date, visibility='private', cover_image=None):
        """
        Cria um novo evento.
        
        Args:
            user_id: ID do usuário criador
            title: Título do evento
            description: Descrição do evento
            location: Local do evento
            date: Data do evento
            visibility: 'public' ou 'private'
            cover_image: Nome do arquivo da imagem de capa (opcional)
        
        Returns:
            tuple: (success: bool, message: str, event: Event|None)
        """
        # Validações
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
        
        # Cria o evento
        event = Event.create(user_id, title, description, location, date, visibility, cover_image)
        
        if event:
            return True, "Evento criado com sucesso!", event
        else:
            return False, "Erro ao criar evento. Tente novamente.", None
    
    @staticmethod
    def update(event_id, user_id, title, description, location, date, visibility, cover_image=None):
        """
        Atualiza um evento existente.
        
        Args:
            event_id: ID do evento
            user_id: ID do usuário (para verificar permissão)
            title: Novo título
            description: Nova descrição
            location: Novo local
            date: Nova data
            visibility: Nova visibilidade
            cover_image: Nova imagem de capa (opcional)
        
        Returns:
            tuple: (success: bool, message: str, event: Event|None)
        """
        # Busca o evento
        event = Event.find_by_id(event_id)
        
        if not event:
            return False, "Evento não encontrado.", None
        
        # Verifica permissão
        if not event.is_owner(user_id):
            return False, "Você não tem permissão para editar este evento.", None
        
        # Validações
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
        
        # Atualiza o evento
        if event.update(title, description, location, date, visibility, cover_image):
            return True, "Evento atualizado com sucesso!", event
        else:
            return False, "Erro ao atualizar evento. Tente novamente.", None
    
    @staticmethod
    def delete(event_id, user_id):
        """
        Exclui um evento.
        
        Args:
            event_id: ID do evento
            user_id: ID do usuário (para verificar permissão)
        
        Returns:
            tuple: (success: bool, message: str)
        """
        # Busca o evento
        event = Event.find_by_id(event_id)
        
        if not event:
            return False, "Evento não encontrado."
        
        # Verifica permissão
        if not event.is_owner(user_id):
            return False, "Você não tem permissão para excluir este evento."
        
        # Exclui o evento
        if event.delete():
            return True, "Evento excluído com sucesso!"
        else:
            return False, "Erro ao excluir evento. Tente novamente."
    
    @staticmethod
    def can_view(event_id, user_id=None):
        """
        Verifica se o usuário pode visualizar o evento.
        
        Args:
            event_id: ID do evento
            user_id: ID do usuário (opcional)
        
        Returns:
            tuple: (can_view: bool, event: Event|None)
        """
        event = Event.find_by_id(event_id)
        
        if not event:
            return False, None
        
        # Eventos públicos podem ser vistos por qualquer um
        if event.visibility == 'public':
            return True, event
        
        # Eventos privados só podem ser vistos pelo dono
        if user_id and event.is_owner(user_id):
            return True, event
        
        return False, None

