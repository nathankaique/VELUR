# Supabase + VÉLOUR

O projeto usa a API Python existente. **O banco PostgreSQL do Supabase será criado automaticamente na primeira execução do servidor** após configurar a credencial de conexão. Não é necessário rodar SQL manualmente. As 8 tabelas já foram criadas no projeto remoto **VELOUR.**. A ligação do servidor Python ao banco requer a URL privada do PostgreSQL configurada no ambiente em que o site rodará. Os 20 veículos de demonstração serão carregados automaticamente no primeiro início conectado ao banco.

1. Abra o projeto existente **VELOUR.** em https://supabase.com/dashboard.
2. Copie **Connect → Connection string → URI** no dashboard. Em redes IPv4, escolha **Session pooler**. Nunca coloque esse endereço no HTML ou JavaScript público.
3. Instale: `pip install -r requirements.txt`.
4. No terminal PowerShell, antes de iniciar, configure as variáveis (troque os valores):
   ```powershell
   $env:SUPABASE_DATABASE_URL='postgresql://USUARIO:SENHA@HOST:5432/postgres?sslmode=require'
   $env:VELOUR_ADMIN_USER='admin'
   $env:VELOUR_ADMIN_PASSWORD='SENHA_ADMIN_FORTE_12_CARACTERES_OU_MAIS'
   $env:VELOUR_SECURE_COOKIES='0' # apenas para testar em http://127.0.0.1
   python server.py
   ```
5. Abra `http://127.0.0.1:8000/` e verifique as 8 tabelas no **Table Editor** do Supabase. Os 20 veículos ilustrativos são inseridos apenas se o catálogo estiver vazio. As tabelas são criadas novamente apenas se estiverem ausentes.

**Segurança:** RLS está ativada em todas as tabelas, sem acesso direto concedido a `anon` e `authenticated`. Os clientes navegam pela API Python, que mantém hashes de senha, sessões via cookies HttpOnly e autorização administrativa. Os usuários desse sistema não são usuários de Supabase Auth. Não exponha `SUPABASE_DATABASE_URL`, credenciais administrativas ou banco de produção; mantenha backups. A aplicação ainda exige proteção contra brute force, CSRF, HTTPS e revisão LGPD antes da publicação pública.

**Modo local:** sem `SUPABASE_DATABASE_URL`, o projeto continua funcionando com SQLite, inclusive os testes originais.

## Verificação
Acesse `http://127.0.0.1:8000/api/health` e confira `database: supabase-postgresql`. No dashboard, veja `public.vehicles` após iniciar o servidor. Em produção, use HTTPS e `VELOUR_SECURE_COOKIES=1`.

**Limite atual:** os testes automatizados usaram SQLite local. Não foi executado teste ponta a ponta com a conexão PostgreSQL remota, pois a senha/URI do banco não é exposta pela integração do ChatGPT.
