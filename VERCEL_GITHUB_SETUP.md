# Como Resolver o Problema de Autorização GitHub na Vercel

## Problema
Ao tentar conectar o repositório GitHub na Vercel, aparece a opção de "git scope" mas ao abrir o GitHub não aparece como opção para autorizar.

## Soluções

### Solução 1: Autorizar Manualmente via GitHub Settings

1. **Acesse o GitHub:**
   - Vá em: https://github.com/settings/applications
   - Ou: GitHub > Settings > Applications > Authorized OAuth Apps

2. **Procure por "Vercel":**
   - Se encontrar, clique e verifique as permissões
   - Se não encontrar, continue com a Solução 2

3. **Revogue e Reautorize:**
   - Clique em "Revoke" se já existir
   - Volte para a Vercel e tente conectar novamente

### Solução 2: Conectar via GitHub OAuth App

1. **Na Vercel:**
   - Vá em: https://vercel.com/account/integrations
   - Clique em "Add GitHub"
   - Isso abrirá uma nova janela de autorização

2. **Autorize a Vercel:**
   - Selecione os repositórios que deseja dar acesso
   - Ou selecione "All repositories"
   - Clique em "Authorize"

3. **Volte para criar o projeto:**
   - Agora tente criar o projeto novamente
   - O repositório `willruty/memo` deve aparecer na lista

### Solução 3: Usar Vercel CLI (Alternativa)

Se continuar com problemas, use o CLI:

1. **Instale o Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Faça login:**
   ```bash
   vercel login
   ```
   - Isso abrirá o navegador para autorizar

3. **No diretório do projeto:**
   ```bash
   cd D:\Development\memo
   vercel
   ```

4. **Siga as instruções:**
   - Link to existing project? **No**
   - Project name: **memo**
   - Directory: **./**
   - Override settings? **No**

5. **Configure as variáveis de ambiente:**
   - Acesse: https://vercel.com/dashboard
   - Vá em seu projeto > Settings > Environment Variables
   - Adicione:
     - `DATABASE_URL`: `postgresql://postgres:memothreads123@db.lfweqsjmxtcgiikkhclj.supabase.co:5432/postgres`
     - `SECRET_KEY`: `eb16510d9e5bae3983cd3cc8d762fd3190929034e643159037e7d3ba3c47dac6`

### Solução 4: Verificar Permissões do GitHub

1. **Verifique se o repositório é público ou privado:**
   - Se for privado, certifique-se de que a Vercel tem acesso

2. **No GitHub:**
   - Vá em: https://github.com/settings/installations
   - Verifique se "Vercel" está instalado
   - Se não estiver, instale e dê as permissões necessárias

## Dica Importante

Se nada funcionar, tente:
1. Limpar o cache do navegador
2. Usar uma janela anônima/privada
3. Tentar em outro navegador
4. Usar o Vercel CLI (Solução 3) que é mais confiável

