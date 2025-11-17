"""
Aplicação Flask principal do sistema Memo.
Gerencia todas as rotas e requisições HTTP.
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from functools import wraps
import os
from database import init_db
from controllers.auth_controller import AuthController
from controllers.event_controller import EventController
from controllers.photo_controller import PhotoController
from models.event import Event
from models.photo import Photo

# Configuração da aplicação
app = Flask(__name__, template_folder='views', static_folder='static')
app.secret_key = os.getenv('SECRET_KEY', 'memo-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Inicializa o banco de dados (com tratamento de erro)
try:
    init_db()
except Exception as e:
    print(f"Aviso: Erro ao inicializar banco de dados: {e}")
    print("O banco será inicializado na primeira requisição.")

# Cria a pasta de uploads se não existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def login_required(f):
    """
    Decorator para proteger rotas que requerem autenticação.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa fazer login para acessar esta página.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== ROTAS PÚBLICAS ====================

@app.route('/')
def home():
    """
    Página inicial do sistema.
    """
    return render_template('home.html')


@app.route('/explorar')
def explore():
    """
    Página de exploração de eventos públicos.
    """
    events = Event.find_public_events(limit=20)
    return render_template('explore.html', events=events)


@app.route('/como-funciona')
def how_it_works():
    """
    Página explicativa sobre como o sistema funciona.
    """
    return render_template('how_it_works.html')


# ==================== ROTAS DE AUTENTICAÇÃO ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Página de login e processamento de login.
    """
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        success, message, user = AuthController.login(email, password)
        
        if success and user:
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            flash(message, 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(message, 'error')
    
    # Se já estiver logado, redireciona para o dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def register():
    """
    Página de cadastro e processamento de registro.
    """
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        success, message, user = AuthController.register(name, email, password, confirm_password)
        
        if success and user:
            flash(message, 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'error')
    
    # Se já estiver logado, redireciona para o dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')


@app.route('/redefinir-senha', methods=['GET', 'POST'])
def reset_password():
    """
    Página de redefinição de senha.
    """
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        success, message = AuthController.reset_password(email, new_password, confirm_password)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'error')
    
    return render_template('reset_password.html')


@app.route('/logout')
def logout():
    """
    Faz logout do usuário e limpa a sessão.
    """
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('home'))


# ==================== ROTAS DE EVENTOS (PROTEGIDAS) ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """
    Painel do usuário com lista de seus eventos.
    """
    user_id = session['user_id']
    events = Event.find_by_user(user_id)
    return render_template('dashboard.html', events=events)


@app.route('/evento/criar', methods=['GET', 'POST'])
@login_required
def create_event():
    """
    Criação de novo evento.
    """
    if request.method == 'POST':
        user_id = session['user_id']
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        location = request.form.get('location', '').strip()
        date = request.form.get('date', '').strip()
        visibility = request.form.get('visibility', 'private').strip()
        
        cover_image = None
        # Processa upload da imagem de capa se fornecida
        if 'cover_image' in request.files:
            file = request.files['cover_image']
            if file and file.filename:
                success, message, filename = PhotoController.upload_cover_image(
                    file, app.config['UPLOAD_FOLDER']
                )
                if success:
                    cover_image = filename
                else:
                    flash(message, 'error')
        
        success, message, event = EventController.create(
            user_id, title, description, location, date, visibility, cover_image
        )
        
        if success and event:
            flash(message, 'success')
            return redirect(url_for('event_details', event_id=event.id))
        else:
            flash(message, 'error')
    
    return render_template('create_event.html')


@app.route('/evento/<int:event_id>')
def event_details(event_id):
    """
    Detalhes de um evento específico.
    """
    user_id = session.get('user_id')
    can_view, event = EventController.can_view(event_id, user_id)
    
    if not can_view or not event:
        flash('Evento não encontrado ou você não tem permissão para visualizá-lo.', 'error')
        if user_id:
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('explore'))
    
    photos = Photo.find_by_event(event_id)
    return render_template('event_details.html', event=event, photos=photos)


@app.route('/evento/<int:event_id>/editar', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    """
    Edição de um evento existente.
    """
    user_id = session['user_id']
    event = Event.find_by_id(event_id)
    
    if not event:
        flash('Evento não encontrado.', 'error')
        return redirect(url_for('dashboard'))
    
    if not event.is_owner(user_id):
        flash('Você não tem permissão para editar este evento.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        location = request.form.get('location', '').strip()
        date = request.form.get('date', '').strip()
        visibility = request.form.get('visibility', 'private').strip()
        
        cover_image = event.cover_image  # Mantém a imagem atual por padrão
        
        # Processa upload da nova imagem de capa se fornecida
        if 'cover_image' in request.files:
            file = request.files['cover_image']
            if file and file.filename:
                success, message, filename = PhotoController.upload_cover_image(
                    file, app.config['UPLOAD_FOLDER'], event.cover_image
                )
                if success:
                    cover_image = filename
                else:
                    flash(message, 'error')
        
        success, message, updated_event = EventController.update(
            event_id, user_id, title, description, location, date, visibility, cover_image
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('event_details', event_id=event_id))
        else:
            flash(message, 'error')
    
    return render_template('edit_event.html', event=event)


@app.route('/evento/<int:event_id>/excluir', methods=['POST'])
@login_required
def delete_event(event_id):
    """
    Exclusão de um evento.
    """
    user_id = session['user_id']
    
    success, message = EventController.delete(event_id, user_id)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('dashboard'))


# ==================== ROTAS DE FOTOS (PROTEGIDAS) ====================

@app.route('/evento/<int:event_id>/upload', methods=['POST'])
@login_required
def upload_photo(event_id):
    """
    Upload de fotos para um evento (suporta múltiplos arquivos).
    """
    user_id = session['user_id']
    
    if 'photo' not in request.files:
        flash('Nenhum arquivo foi enviado.', 'error')
        return redirect(url_for('event_details', event_id=event_id))
    
    files = request.files.getlist('photo')
    
    if not files or all(f.filename == '' for f in files):
        flash('Nenhum arquivo foi selecionado.', 'error')
        return redirect(url_for('event_details', event_id=event_id))
    
    success_count = 0
    error_count = 0
    error_messages = []
    
    for file in files:
        if file.filename:
            success, message, photo = PhotoController.upload(
                event_id, user_id, file, app.config['UPLOAD_FOLDER']
            )
            
            if success:
                success_count += 1
            else:
                error_count += 1
                error_messages.append(message)
    
    # Mensagens de feedback
    if success_count > 0:
        if success_count == 1:
            flash(f'{success_count} foto enviada com sucesso!', 'success')
        else:
            flash(f'{success_count} fotos enviadas com sucesso!', 'success')
    
    if error_count > 0:
        if error_count == 1:
            flash(f'{error_count} foto não pôde ser enviada.', 'error')
        else:
            flash(f'{error_count} fotos não puderam ser enviadas.', 'error')
        if error_messages:
            flash(error_messages[0], 'error')
    
    return redirect(url_for('event_details', event_id=event_id))


@app.route('/download/<filename>')
def download_file(filename):
    """
    Download de arquivo (foto) do sistema.
    """
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=False
    )


@app.route('/foto/<int:photo_id>/excluir', methods=['POST'])
@login_required
def delete_photo(photo_id):
    """
    Exclusão de uma foto.
    """
    user_id = session['user_id']
    photo = Photo.find_by_id(photo_id)
    
    if not photo:
        flash('Foto não encontrada.', 'error')
        return redirect(url_for('dashboard'))
    
    success, message = PhotoController.delete(
        photo_id, user_id, app.config['UPLOAD_FOLDER']
    )
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('event_details', event_id=photo.event_id))


# ==================== INICIALIZAÇÃO ====================

if __name__ == '__main__':
    # Inicializa o banco de dados
    init_db()
    
    # Executa a aplicação
    app.run(debug=True, host='0.0.0.0', port=5000)

