# Como Criar as Tabelas no Supabase

## Método 1: SQL Editor (Recomendado)

1. Acesse: https://supabase.com/dashboard/project/lfweqsjmxtcgiikkhclj
2. No menu lateral, clique em **SQL Editor**
3. Clique em **New query**
4. Copie e cole todo o conteúdo do arquivo `supabase_schema.sql`
5. Clique em **Run** (ou pressione Ctrl+Enter)
6. Você verá a mensagem "Success. No rows returned"

## Método 2: Via Script Python Local

1. Configure a variável de ambiente:
   ```powershell
   $env:DATABASE_URL="postgresql://postgres:memothreads123@db.lfweqsjmxtcgiikkhclj.supabase.co:5432/postgres"
   ```

2. Execute:
   ```powershell
   python database.py
   ```

## Verificar se as Tabelas Foram Criadas

No Supabase Dashboard:
1. Vá em **Table Editor** no menu lateral
2. Você deve ver as tabelas: `users`, `events`, `photos`

