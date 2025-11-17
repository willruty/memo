# Troubleshooting - Erro 500 no Vercel

## Erro: FUNCTION_INVOCATION_FAILED (500)

### Possíveis Causas e Soluções

#### 1. ✅ Variáveis de Ambiente Não Configuradas

**Sintoma:** Erro 500 logo após o deploy

**Solução:**
1. Acesse: https://vercel.com/dashboard
2. Selecione seu projeto **memo**
3. Vá em **Settings > Environment Variables**
4. Verifique se estas variáveis estão configuradas:
   - `DATABASE_URL`: `postgresql://postgres:memothreads123@db.lfweqsjmxtcgiikkhclj.supabase.co:5432/postgres`
   - `SECRET_KEY`: `eb16510d9e5bae3983cd3cc8d762fd3190929034e643159037e7d3ba3c47dac6`
5. **IMPORTANTE:** Selecione todas as environments (Production, Preview, Development)
6. Após adicionar, faça um **Redeploy**

#### 2. ✅ Tabelas Não Criadas no Supabase

**Sintoma:** Erro ao acessar qualquer página

**Solução:**
1. Acesse: https://supabase.com/dashboard/project/lfweqsjmxtcgiikkhclj
2. Vá em **SQL Editor**
3. Execute o script `supabase_schema.sql`
4. Verifique se as tabelas foram criadas em **Table Editor**

#### 3. ✅ Connection String Incorreta

**Sintoma:** Erro de conexão no log

**Solução:**
1. No Supabase Dashboard, vá em **Settings > Database**
2. Copie a **Connection string** exata (URI)
3. Atualize a variável `DATABASE_URL` no Vercel
4. Faça um Redeploy

#### 4. ✅ Verificar Logs de Erro

**Como ver os logs:**
1. No Vercel Dashboard, vá em **Deployments**
2. Clique no último deploy
3. Clique em **Functions** ou **Logs**
4. Procure por mensagens de erro específicas

### Checklist de Verificação

- [ ] Variáveis de ambiente configuradas no Vercel
- [ ] Tabelas criadas no Supabase
- [ ] Connection string correta
- [ ] Redeploy feito após configurar variáveis
- [ ] Logs verificados para erros específicos

### Comandos Úteis

**Testar conexão localmente:**
```powershell
$env:DATABASE_URL="postgresql://postgres:memothreads123@db.lfweqsjmxtcgiikkhclj.supabase.co:5432/postgres"
python test_connection.py
```

**Verificar variáveis no Vercel via CLI:**
```bash
vercel env ls
```

### Próximos Passos

1. Verifique os logs do Vercel para ver o erro exato
2. Confirme que as variáveis de ambiente estão configuradas
3. Certifique-se de que as tabelas foram criadas no Supabase
4. Faça um novo deploy após corrigir os problemas

