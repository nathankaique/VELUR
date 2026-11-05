"""Inicia VELOUR conectado ao PostgreSQL, sem salvar a senha em arquivos."""
import os
import sys
import getpass
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
print('===============================================')
print(' VELOUR | CADASTRO E LOGIN NO SUPABASE')
print('===============================================')
print('Projeto: VELOUR. | Supabase PostgreSQL')
print('Apenas a SENHA DO BANCO (Database Password) e necessaria.')
print('Nao cole URI, link ou chave anon aqui.')
print('A senha nao aparece na tela e nao sera gravada em arquivo.')
try:
    password = getpass.getpass('Senha do banco Supabase: ')
except (KeyboardInterrupt, EOFError):
    print('\nOperacao cancelada.')
    sys.exit(1)
if not password.strip():
    print('ERRO: a senha nao pode estar vazia.')
    sys.exit(1)
try:
    import psycopg
    from psycopg.conninfo import make_conninfo
except ImportError:
    print('Falta a biblioteca psycopg. Execute: py -3 -m pip install -r requirements.txt')
    sys.exit(2)

# Session pooler: usuario no formato postgres.<project-ref>.
# make_conninfo faz o escape correto dos caracteres especiais da senha.
conninfo = make_conninfo('', host='aws-1-us-west-2.pooler.supabase.com', port=5432,
                         dbname='postgres', user='postgres.vfqhoatumdawqgxdkuce',
                         password=password, sslmode='require', connect_timeout=12)
password = None
print('Verificando conexao com Supabase...', flush=True)
try:
    with psycopg.connect(conninfo) as db:
        with db.cursor() as cur:
            cur.execute('SELECT count(*) FROM public.customers')
            users = cur.fetchone()[0]
    print(f'CONEXAO OK! Clientes no Supabase: {users}', flush=True)
except Exception as exc:
    message = str(exc).lower()
    if 'password authentication failed' in message or 'invalid password' in message:
        print('ERRO: senha do banco incorreta. Use Database Password, nao a senha do painel.')
    elif 'invalid format for user or db_name' in message or 'einvaliduserinfo' in message:
        print('ERRO: configuracao do pooler nao aceita o usuario/banco. Confira o endereco em Supabase > Connect > Session pooler.')
    elif 'does not exist' in message:
        print('ERRO: a tabela customers nao existe no banco escolhido.')
    else:
        print('ERRO DE CONEXAO:', str(exc))
    sys.exit(3)

print('Iniciando servidor no modo SUPABASE (nao SQLite)...', flush=True)
env = os.environ.copy()
env['SUPABASE_DATABASE_URL'] = conninfo
env['VELOUR_PORT'] = '8765'
env['VELOUR_OPEN_BROWSER'] = '1'
env.pop('VELOUR_SECURE_COOKIES', None)
try:
    subprocess.run([sys.executable, '-u', str(ROOT / 'server.py')], env=env, check=False)
except KeyboardInterrupt:
    print('\nServidor encerrado.')
