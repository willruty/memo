# Memo - Sistema de Memórias

Sistema web para guardar memórias de eventos, viagens e festas, permitindo que usuários criem eventos privados ou públicos e façam upload e download de fotos desses eventos.

## 🚀 Tecnologias

- **Backend**: Python 3.x com Flask
- **Frontend**: HTML5 e CSS3 (JavaScript mínimo - menos de 30%)
- **Banco de Dados**: PostgreSQL (Supabase)
- **Arquitetura**: MVC (Model-View-Controller)
- **Deploy**: Vercel

## 📋 Requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. Clone ou baixe este repositório

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:

**Windows (PowerShell):**
```powershell
$env:DATABASE_URL="postgresql://postgres:memothreads123@db.lfweqsjmxtcgiikkhclj.supabase.co:5432/postgres"
$env:SECRET_KEY="sua-chave-secreta-aqui"
```

**Linux/Mac:**
```bash
export DATABASE_URL="postgresql://postgres:memothreads123@db.lfweqsjmxtcgiikkhclj.supabase.co:5432/postgres"
export SECRET_KEY="sua-chave-secreta-aqui"
```

4. Inicialize o banco de dados:
```bash
python database.py
```

5. Execute a aplicação:
```bash
python app.py
```

6. Acesse no navegador:
```
http://localhost:5000
```

**Nota**: Veja `SUPABASE_SETUP.md` para instruções detalhadas sobre como obter a connection string do Supabase.

## 📁 Estrutura do Projeto

```
/memo
    /models
        user.py          # Modelo de usuário
        event.py         # Modelo de evento
        photo.py         # Modelo de foto
        __init__.py
    /controllers
        auth_controller.py      # Controller de autenticação
        event_controller.py     # Controller de eventos
        photo_controller.py     # Controller de fotos
        __init__.py
    /views
        base.html              # Template base
        home.html              # Página inicial
        explore.html           # Explorar eventos públicos
        how_it_works.html      # Como funciona
        login.html             # Login
        register.html          # Cadastro
        reset_password.html    # Redefinir senha
        dashboard.html         # Painel do usuário
        create_event.html      # Criar evento
        edit_event.html        # Editar evento
        event_details.html     # Detalhes do evento
    /static
        /css
            style.css          # Estilos CSS
        /img
    /uploads                   # Pasta de uploads de fotos
    app.py                     # Aplicação Flask principal
    database.py                # Configuração do banco de dados
    requirements.txt           # Dependências Python
    README.md                  # Este arquivo
```

## 🎯 Funcionalidades

### CRUD de Usuários
- ✅ Cadastro com senha hasheada
- ✅ Login com sessões
- ✅ Perfil do usuário
- ✅ Esqueci minha senha

### CRUD de Eventos
- ✅ Criar evento (nome, descrição, local, data, privacidade)
- ✅ Editar evento
- ✅ Excluir evento
- ✅ Listar eventos (próprios e públicos)

### CRUD de Fotos
- ✅ Upload de fotos
- ✅ Download de fotos
- ✅ Excluir fotos
- ✅ Vincular foto a evento

## 🔒 Regras de Negócio

- Apenas imagens são aceitas nos uploads (PNG, JPG, JPEG, GIF, WEBP)
- Eventos privados só podem ser vistos pelo dono
- Usuário logado pode visualizar apenas seus eventos privados
- Sessões obrigatórias após login
- Nenhum campo vazio é aceito (validações nos controllers)
- Senhas são hasheadas usando Werkzeug

## 📄 Páginas

### Páginas Públicas (antes do login)
- **Home**: Explica o Memo, destaque visual, texto institucional
- **Explorar Eventos**: Lista eventos públicos mais recentes
- **Como Funciona**: Explica criação de eventos, upload e privacidade

### Páginas de Autenticação
- **Login**: Sistema de login com validações
- **Cadastro**: Registro de novos usuários
- **Redefinir Senha**: Recuperação de senha

### Páginas Protegidas (após login)
- **Dashboard**: Lista de eventos do usuário
- **Criar Evento**: Formulário de criação
- **Editar Evento**: Formulário de edição
- **Detalhes do Evento**: Visualização completa com fotos

## 🗄️ Banco de Dados

### Tabelas

**users**
- id (INTEGER PRIMARY KEY)
- name (TEXT NOT NULL)
- email (TEXT NOT NULL UNIQUE)
- password_hash (TEXT NOT NULL)
- created_at (TIMESTAMP)

**events**
- id (INTEGER PRIMARY KEY)
- user_id (INTEGER NOT NULL, FOREIGN KEY)
- title (TEXT NOT NULL)
- description (TEXT NOT NULL)
- location (TEXT NOT NULL)
- date (DATE NOT NULL)
- visibility (TEXT NOT NULL DEFAULT 'private')
- cover_image (TEXT)
- created_at (TIMESTAMP)

**photos**
- id (INTEGER PRIMARY KEY)
- event_id (INTEGER NOT NULL, FOREIGN KEY)
- filename (TEXT NOT NULL)
- uploaded_at (TIMESTAMP)

## 🔐 Segurança

- Senhas hasheadas com Werkzeug
- Validação de campos em todos os formulários
- Proteção de rotas com decorator `@login_required`
- Verificação de permissões para edição/exclusão
- Sanitização de nomes de arquivos
- Limite de tamanho de arquivo (16MB)

## 👤 Usuário de Exemplo

Após inicializar o banco de dados, um usuário de exemplo é criado:
- **Email**: admin@memo.com
- **Senha**: admin123

## 📝 Notas

- O sistema usa PostgreSQL (Supabase) como banco de dados
- As fotos são salvas na pasta `uploads/`
- Para produção no Vercel, configure as variáveis de ambiente
- Veja `DEPLOYMENT.md` para instruções de deploy

## 🐛 Solução de Problemas

**Erro ao criar banco de dados:**
- Verifique se tem permissões de escrita no diretório
- Execute `python database.py` manualmente

**Erro ao fazer upload:**
- Verifique se a pasta `uploads/` existe e tem permissões de escrita
- Verifique o tamanho do arquivo (máximo 16MB)

**Erro de importação:**
- Certifique-se de que todas as dependências estão instaladas: `pip install -r requirements.txt`
- Verifique se está executando a partir do diretório raiz do projeto

## 📞 Suporte

Para dúvidas ou problemas, verifique:
1. Se todas as dependências estão instaladas
2. Se o banco de dados foi inicializado
3. Se as permissões de arquivo estão corretas

## 📄 Licença

Este projeto foi desenvolvido como sistema educacional.

