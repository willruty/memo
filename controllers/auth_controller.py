from models.user import User
from werkzeug.security import generate_password_hash
import re

class AuthController:
    
    @staticmethod
    def validate_email(email):
        if not email or not isinstance(email, str):
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password(password):
        if not password or not isinstance(password, str):
            return False
        return len(password) >= 6
    
    @staticmethod
    def validate_name(name):
        if not name or not isinstance(name, str):
            return False
        name = name.strip()
        return len(name) >= 3
    
    @staticmethod
    def register(name, email, password, confirm_password):
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
        
        existing_user = User.find_by_email(email)
        if existing_user:
            return False, "Este email já está cadastrado.", None
        
        user = User.create(name, email, password)
        
        if user:
            return True, "Usuário cadastrado com sucesso!", user
        else:
            return False, "Erro ao cadastrar usuário. Tente novamente.", None
    
    @staticmethod
    def login(email, password):
        if not email or not password:
            return False, "Email e senha são obrigatórios.", None
        
        if not AuthController.validate_email(email):
            return False, "Email inválido.", None
        
        user = User.find_by_email(email)
        
        if not user:
            return False, "Email ou senha incorretos.", None
        
        if not user.verify_password(password):
            return False, "Email ou senha incorretos.", None
        
        return True, "Login realizado com sucesso!", user
    
    @staticmethod
    def reset_password(email, new_password, confirm_password):
        if not email or not new_password or not confirm_password:
            return False, "Todos os campos são obrigatórios."
        
        if not AuthController.validate_email(email):
            return False, "Email inválido."
        
        if not AuthController.validate_password(new_password):
            return False, "Senha deve ter no mínimo 6 caracteres."
        
        if new_password != confirm_password:
            return False, "As senhas não coincidem."
        
        user = User.find_by_email(email)
        
        if not user:
            return False, "Email não encontrado."
        
        if user.update_password(new_password):
            return True, "Senha redefinida com sucesso!"
        else:
            return False, "Erro ao redefinir senha. Tente novamente."
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.find_by_id(user_id)
    
    @staticmethod
    def update_profile(user_id, name, email):
        user = User.find_by_id(user_id)
        if not user:
            return False, "Usuário não encontrado.", None
        
        if not AuthController.validate_name(name):
            return False, "Nome deve ter no mínimo 3 caracteres.", None
        
        if not AuthController.validate_email(email):
            return False, "Email inválido.", None
        
        if user.update_profile(name, email):
            updated_user = User.find_by_id(user_id)
            return True, "Perfil atualizado com sucesso!", updated_user
        else:
            return False, "Erro ao atualizar perfil. Email já está em uso.", None
    
    @staticmethod
    def change_password(user_id, current_password, new_password, confirm_password):
        user = User.find_by_id(user_id)
        if not user:
            return False, "Usuário não encontrado."
        
        if not user.verify_password(current_password):
            return False, "Senha atual incorreta."
        
        if not AuthController.validate_password(new_password):
            return False, "Senha deve ter no mínimo 6 caracteres."
        
        if new_password != confirm_password:
            return False, "As senhas não coincidem."
        
        if user.update_password(new_password):
            return True, "Senha alterada com sucesso!"
        else:
            return False, "Erro ao alterar senha. Tente novamente."
