# Guia de Deploy no Vercel com Supabase

Este guia explica como fazer deploy do Memo no Vercel usando Supabase como banco de dados.

## Pré-requisitos

1. Conta no [Vercel](https://vercel.com)
2. Projeto criado no [Supabase](https://supabase.com)

## Configuração do Supabase

### 1. Connection String Configurada

A connection string já está configurada:
```
postgresql://postgres:memothreads123@db.lfweqsjmxtcgiikkhclj.supabase.co:5432/postgres
```

### 2. Inicializar o Banco de Dados

Execute localmente para criar as tabelas:

**Windows (PowerShell):**
```powershell
$env:DATABASE_URL="postgresql://postgres:memothreads123@db.lfweqsjmxtcgiikkhclj.supabase.co:5432/postgres"
python database.py
```

**Linux/Mac:**
```bash
export DATABASE_URL="postgresql://postgres:memothreads123@db.lfweqsjmxtcgiikkhclj.supabase.co:5432/postgres"
python database.py
```

Ou use o SQL Editor do Supabase para executar as queries de criação de tabelas.

## Deploy no Vercel

### Via CLI

1. Instale o Vercel CLI:
```bash
npm i -g vercel
```

2. Faça login:
```bash
vercel login
```

3. No diretório do projeto:
```bash
vercel
```

4. Siga as instruções do CLI

### Via Dashboard

1. Acesse [vercel.com](https://vercel.com)
2. Clique em **Add New Project**
3. Conecte seu repositório Git
4. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: ./
   - **Build Command**: (deixe vazio)
   - **Output Directory**: (deixe vazio)

## Variáveis de Ambiente no Vercel

No dashboard do Vercel, vá em **Settings** > **Environment Variables** e adicione:

```
DATABASE_URL=postgresql://postgres:memothreads123@db.lfweqsjmxtcgiikkhclj.supabase.co:5432/postgres
SECRET_KEY=sua-chave-secreta-aleatoria
```

**Importante:**
- Para gerar `SECRET_KEY`: `python -c "import secrets; print(secrets.token_hex(32))"`

## Inicializar Banco de Dados Após Deploy

Após o primeiro deploy, você precisa inicializar as tabelas. Você pode:

1. **Via Script Local** (Recomendado):
   - Configure `DATABASE_URL` localmente
   - Execute: `python database.py`

2. **Via SQL Editor do Supabase**:
   - Acesse o SQL Editor no Supabase
   - Execute as queries de criação de tabelas do `database.py`

## Estrutura de Arquivos

```
memo/
├── api/
│   └── index.py          ← Entry point do Vercel
├── vercel.json           ← Configuração do Vercel
├── app.py
├── database.py
├── requirements.txt
└── ...
```

## Verificações Pós-Deploy

1. Acesse sua URL do Vercel
2. Teste:
   - Criar conta
   - Fazer login
   - Criar evento
   - Upload de fotos
   - Visualizar eventos públicos/privados

## Troubleshooting

### Erro: "DATABASE_URL not found"
- Verifique se a variável está configurada no Vercel
- Certifique-se de que está no formato correto

### Erro: "Connection refused"
- Verifique se a senha está correta na connection string
- No Supabase: Settings > Database > Connection Pooling (use a connection string de pool se disponível)

### Uploads não funcionam
- Vercel tem limitações de filesystem em serverless
- Considere usar Vercel Blob Storage ou AWS S3 para produção

## Atualizações

Para atualizar o deploy:
```bash
vercel --prod
```

Ou faça push para o branch principal conectado ao Vercel.
