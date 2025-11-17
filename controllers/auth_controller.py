"""
Controller de Autenticação.
Gerencia login, registro, logout e recuperação de senha.
"""
from models.user import User
from werkzeug.security import generate_password_hash
import re

class AuthController:
    """
    Controller responsável por operações de autenticação.
    """
    
    @staticmethod
    def validate_email(email):
        """
        Valida formato de email.
        
        Args:
            email: Email a ser validado
        
        Returns:
            bool: True se o email for válido
        """
        if not email or not isinstance(email, str):
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password(password):
        """
        Valida senha (mínimo 6 caracteres).
        
        Args:
            password: Senha a ser validada
        
        Returns:
            bool: True se a senha for válida
        """
        if not password or not isinstance(password, str):
            return False
        return len(password) >= 6
    
    @staticmethod
    def validate_name(name):
        """
        Valida nome (mínimo 3 caracteres).
        
        Args:
            name: Nome a ser validado
        
        Returns:
            bool: True se o nome for válido
        """
        if not name or not isinstance(name, str):
            return False
        name = name.strip()
        return len(name) >= 3
    
    @staticmethod
    def register(name, email, password, confirm_password):
        """
        Registra um novo usuário.
        
        Args:
            name: Nome do usuário
            email: Email do usuário
            password: Senha
            confirm_password: Confirmação da senha
        
        Returns:
            tuple: (success: bool, message: str, user: User|None)
        """
        # Validações
        if not name or not email or not password or not confirm_password:
            return False, "Todos os campos são obrigatórios.", None
        
        if not AuthController.validate_name(name):
            return False, "Nome deve ter no mínimo 3 caracteres.", None
        
        if not AuthController.validate_email(email):
            return False, "Email inválido.", None
        
        if not AuthController.validate_password(password):
            return False, "Senha deve ter no mínimo 6 caracteres.", None
        
        if password != confirm_password:
            return False, "As senhas não coincidem.", None
        
        # Verifica se email já existe
        existing_user = User.find_by_email(email)
        if existing_user:
            return False, "Este email já está cadastrado.", None
        
        # Cria o usuário
        user = User.create(name, email, password)
        
        if user:
            return True, "Usuário cadastrado com sucesso!", user
        else:
            return False, "Erro ao cadastrar usuário. Tente novamente.", None
    
    @staticmethod
    def login(email, password):
        """
        Realiza login do usuário.
        
        Args:
            email: Email do usuário
            password: Senha do usuário
        
        Returns:
            tuple: (success: bool, message: str, user: User|None)
        """
        # Validações
        if not email or not password:
            return False, "Email e senha são obrigatórios.", None
        
        if not AuthController.validate_email(email):
            return False, "Email inválido.", None
        
        # Busca o usuário
        user = User.find_by_email(email)
        
        if not user:
            return False, "Email ou senha incorretos.", None
        
        # Verifica a senha
        if not user.verify_password(password):
            return False, "Email ou senha incorretos.", None
        
        return True, "Login realizado com sucesso!", user
    
    @staticmethod
    def reset_password(email, new_password, confirm_password):
        """
        Redefine a senha do usuário.
        
        Args:
            email: Email do usuário
            new_password: Nova senha
            confirm_password: Confirmação da nova senha
        
        Returns:
            tuple: (success: bool, message: str)
        """
        # Validações
        if not email or not new_password or not confirm_password:
            return False, "Todos os campos são obrigatórios."
        
        if not AuthController.validate_email(email):
            return False, "Email inválido."
        
        if not AuthController.validate_password(new_password):
            return False, "Senha deve ter no mínimo 6 caracteres."
        
        if new_password != confirm_password:
            return False, "As senhas não coincidem."
        
        # Busca o usuário
        user = User.find_by_email(email)
        
        if not user:
            return False, "Email não encontrado."
        
        # Atualiza a senha
        if user.update_password(new_password):
            return True, "Senha redefinida com sucesso!"
        else:
            return False, "Erro ao redefinir senha. Tente novamente."

