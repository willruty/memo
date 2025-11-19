# Memo - Sistema de Gerenciamento de Eventos

Sistema web para criação e gerenciamento de eventos com upload de fotos, desenvolvido em Flask (Python).

## Preparação do Projeto para Distribuição

Antes de criar o ZIP do projeto, remova os seguintes arquivos e pastas:

- `__pycache__/` (todas as pastas)
- `*.pyc` (todos os arquivos compilados)
- `memo.db` (banco de dados - será criado automaticamente)
- `uploads/` (pasta de uploads - será criada automaticamente)
- `.vercel/` (se existir - pasta de configuração da Vercel)
- `venv/` ou `.venv/` (ambiente virtual - deve ser criado pelo usuário)

O projeto deve incluir apenas:
- Arquivos `.py` (código fonte)
- Pasta `controllers/`
- Pasta `models/`
- Pasta `views/`
- Pasta `static/` (CSS e imagens)
- `requirements.txt`
- `README.md`
- `.gitignore`

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

1. Extraia o projeto em uma pasta de sua preferência

2. Abra o terminal/prompt de comando na pasta do projeto

3. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
```

4. Ative o ambiente virtual:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```

5. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Configuração

1. O banco de dados SQLite será criado automaticamente na primeira execução
2. Por padrão, o arquivo do banco será `memo.db` na pasta raiz do projeto
3. Para configurar um caminho diferente para o banco de dados, defina a variável de ambiente:
   ```bash
   # Windows
   set DATABASE_PATH=caminho\para\seu\banco.db
   
   # Linux/Mac
   export DATABASE_PATH=/caminho/para/seu/banco.db
   ```

4. Para definir uma chave secreta customizada (recomendado para produção):
   ```bash
   # Windows
   set SECRET_KEY=sua-chave-secreta-aqui
   
   # Linux/Mac
   export SECRET_KEY=sua-chave-secreta-aqui
   ```

## Executando o Projeto

### Opção 1: Usando run.py (com inicialização do banco)
```bash
python run.py
```

### Opção 2: Usando Flask diretamente
```bash
python app.py
```

O servidor será iniciado em: `http://localhost:5001`

## Estrutura do Projeto

```
memo/
├── app.py                  # Aplicação principal Flask
├── run.py                  # Script de inicialização
├── database.py             # Configuração e funções do banco de dados
├── requirements.txt        # Dependências do projeto
├── memo.db                 # Banco de dados SQLite (criado automaticamente)
├── controllers/            # Controladores (lógica de negócio)
│   ├── auth_controller.py
│   ├── event_controller.py
│   └── photo_controller.py
├── models/                 # Modelos de dados
│   ├── user.py
│   ├── event.py
│   └── photo.py
├── views/                  # Templates HTML
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── create_event.html
│   ├── edit_event.html
│   ├── event_details.html
│   └── explore.html
├── static/                 # Arquivos estáticos (CSS, imagens)
│   ├── css/
│   └── img/
└── uploads/                # Pasta para uploads de imagens de capa
```

## Funcionalidades

- **Autenticação:** Cadastro, login e recuperação de senha
- **Eventos:** Criação, edição, visualização e exclusão de eventos
- **Fotos:** Upload de múltiplas fotos por evento
- **Download:** Download individual de fotos ou download em ZIP de todas as fotos de um evento
- **Visibilidade:** Eventos públicos ou privados
- **Explorar:** Visualização de eventos públicos de outros usuários

## Como Usar

1. Acesse `http://localhost:5001` no navegador
2. Crie uma conta através do link "Cadastrar-se"
3. Faça login com suas credenciais
4. No dashboard, clique em "Criar Novo Evento"
5. Preencha os dados do evento e faça upload de uma foto de capa (opcional)
6. Após criar o evento, você pode adicionar fotos na página de detalhes
7. As fotos podem ser baixadas individualmente ou todas juntas em ZIP

## Tecnologias Utilizadas

- **Backend:** Flask 3.0.0
- **Banco de Dados:** SQLite
- **Frontend:** HTML, CSS (Vanilla)
- **Upload de Arquivos:** Werkzeug

## Observações Importantes

- O banco de dados SQLite é criado automaticamente na primeira execução
- As imagens de capa são salvas na pasta `uploads/`
- As fotos dos eventos são armazenadas como BLOB no banco de dados
- Em produção, recomenda-se usar um banco de dados mais robusto (PostgreSQL, MySQL) e armazenamento em nuvem para arquivos

## Solução de Problemas

### Erro ao instalar dependências
Certifique-se de que está usando Python 3.8+ e pip está atualizado:
```bash
python --version
pip install --upgrade pip
```

### Erro de permissão ao criar banco de dados
Verifique se tem permissão de escrita na pasta do projeto

### Porta 5001 já em uso
Altere a porta no arquivo `run.py` ou `app.py` na linha final:
```python
app.run(debug=True, host='0.0.0.0', port=PORTA_DESEJADA)
```

## Licença

Este projeto é de código aberto e está disponível para uso educacional e pessoal.

