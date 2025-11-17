# Variáveis de Ambiente para Vercel

## Variáveis Obrigatórias

Configure estas variáveis no Vercel Dashboard:
**Settings > Environment Variables**

### 1. DATABASE_URL
```
postgresql://postgres:memothreads123@db.lfweqsjmxtcgiikkhclj.supabase.co:5432/postgres
```

### 2. SECRET_KEY
```
eb16510d9e5bae3983cd3cc8d762fd3190929034e643159037e7d3ba3c47dac6
```

## Como Configurar no Vercel

1. **Acesse o Dashboard:**
   - Vá em: https://vercel.com/dashboard
   - Selecione seu projeto **memo**

2. **Vá em Settings:**
   - Clique em **Settings** no topo
   - Clique em **Environment Variables** no menu lateral

3. **Adicione as Variáveis:**
   - Clique em **Add New**
   - **Key**: `DATABASE_URL`
   - **Value**: `postgresql://postgres:memothreads123@db.lfweqsjmxtcgiikkhclj.supabase.co:5432/postgres`
   - **Environment**: Selecione todas (Production, Preview, Development)
   - Clique em **Save**

   - Clique em **Add New** novamente
   - **Key**: `SECRET_KEY`
   - **Value**: `eb16510d9e5bae3983cd3cc8d762fd3190929034e643159037e7d3ba3c47dac6`
   - **Environment**: Selecione todas (Production, Preview, Development)
   - Clique em **Save**

4. **Redeploy:**
   - Após adicionar as variáveis, vá em **Deployments**
   - Clique nos 3 pontinhos do último deploy
   - Clique em **Redeploy**

## Resumo Rápido

| Variável | Valor |
|----------|-------|
| `DATABASE_URL` | `postgresql://postgres:memothreads123@db.lfweqsjmxtcgiikkhclj.supabase.co:5432/postgres` |
| `SECRET_KEY` | `eb16510d9e5bae3983cd3cc8d762fd3190929034e643159037e7d3ba3c47dac6` |

## Importante

- ✅ Selecione **todas as environments** (Production, Preview, Development)
- ✅ Após adicionar, faça um **Redeploy** para aplicar as mudanças
- ⚠️ A senha do banco está visível aqui - em produção, considere usar Vercel Secrets

