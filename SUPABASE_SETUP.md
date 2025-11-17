# Configuração do Supabase

## Informações do Projeto

- **URL do Projeto**: https://lfweqsjmxtcgiikkhclj.supabase.co
- **Anon Key**: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxmd2Vxc2pteHRjZ2lpa2toY2xqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMzOTc0MDUsImV4cCI6MjA3ODk3MzQwNX0.CUC3oB-jN_WaX5o8IBcYowfS40DeUhZCC3wTAqzryVw

## Connection String

```
postgresql://postgres:memothreads123@db.lfweqsjmxtcgiikkhclj.supabase.co:5432/postgres
```

## Configuração Local

Para desenvolvimento local, configure a variável de ambiente:

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

## Inicializar o Banco de Dados

Após configurar as variáveis de ambiente, execute:

```bash
python database.py
```

Isso criará todas as tabelas necessárias no Supabase.

## Configuração no Vercel

No dashboard do Vercel, configure as seguintes variáveis de ambiente:

- `DATABASE_URL`: `postgresql://postgres:memothreads123@db.lfweqsjmxtcgiikkhclj.supabase.co:5432/postgres`
- `SECRET_KEY`: Gere uma chave secreta aleatória (use: `python -c "import secrets; print(secrets.token_hex(32))"`)
