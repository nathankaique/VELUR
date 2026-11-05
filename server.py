"""VÉLOUR: API Python com PostgreSQL Supabase ou SQLite para desenvolvimento."""
import os, json, sqlite3, secrets, hashlib, hmac, mimetypes, re, time, socket, sys, webbrowser, threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit, parse_qs
from datetime import datetime, timezone
from decimal import Decimal

SUPABASE_DATABASE_URL = os.getenv("SUPABASE_DATABASE_URL", "").strip()
try:
    from psycopg.errors import UniqueViolation as PG_UNIQUE_VIOLATION
except ImportError:
    class PG_UNIQUE_VIOLATION(Exception): pass

ROOT = Path(__file__).resolve().parent
DB = Path(os.getenv('VELOUR_DB', str(ROOT/'data'/'velour.db')))
HOST = os.getenv('VELOUR_HOST', '127.0.0.1')
PORT = int(os.getenv('VELOUR_PORT', '8765'))
MAX_BODY = 150_000

class PgResult:
    def __init__(self, cursor, lastrowid=None):
        self.cursor = cursor
        self.lastrowid = lastrowid
        self.rowcount = cursor.rowcount
    def fetchone(self):
        return self.cursor.fetchone()
    def fetchall(self):
        return self.cursor.fetchall()

class PgConnection:
    def __init__(self, conn): self.conn = conn
    def __enter__(self): self.conn.__enter__(); return self
    def __exit__(self, *args): return self.conn.__exit__(*args)
    def execute(self, query, params=()):
        from psycopg.rows import dict_row
        # All placeholders in the existing API are parameterized SQLite-style "?".
        query = query.replace('?', '%s')
        insert_id = query.lstrip().upper().startswith('INSERT INTO') and 'RETURNING' not in query.upper()
        if insert_id and any(('INSERT INTO '+x) in query.upper() for x in ('VEHICLES', 'LEADS', 'PROPOSALS', 'CUSTOMERS', 'ADMINS', 'AUDIT')):
            query += ' RETURNING id'
        cur = self.conn.execute(query, params)
        new_id = cur.fetchone()['id'] if insert_id and 'RETURNING id' in query else None
        return PgResult(cur, new_id)
    def executemany(self, query, params):
        with self.conn.cursor() as cursor: cursor.executemany(query.replace('?', '%s'), params)

def connect():
    if SUPABASE_DATABASE_URL:
        try:
            import psycopg
            from psycopg.rows import dict_row
        except ImportError as exc:
            raise RuntimeError('Instale psycopg: pip install -r requirements.txt') from exc
        return PgConnection(psycopg.connect(SUPABASE_DATABASE_URL, row_factory=dict_row, connect_timeout=10))
    c=sqlite3.connect(DB,timeout=10)
    c.row_factory=sqlite3.Row
    c.execute('PRAGMA foreign_keys=ON')
    return c

def hash_password(value,salt=None):
    salt=salt or secrets.token_hex(16)
    key=hashlib.pbkdf2_hmac('sha256',value.encode(),bytes.fromhex(salt),280000)
    return salt+':'+key.hex()

def verify_password(password,stored):
    try:
        salt,_=stored.split(':',1)
        return hmac.compare_digest(hash_password(password,salt),stored)
    except (ValueError,TypeError): return False

def init_db():
    if SUPABASE_DATABASE_URL:
        initialize_supabase()
        return
    DB.parent.mkdir(parents=True,exist_ok=True)
    with connect() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS vehicles(
          id INTEGER PRIMARY KEY, brand TEXT NOT NULL, model TEXT NOT NULL,
          year INTEGER NOT NULL, km INTEGER NOT NULL, price REAL NOT NULL,
          category TEXT NOT NULL, fuel TEXT NOT NULL, transmission TEXT NOT NULL,
          color TEXT NOT NULL, power TEXT NOT NULL, tag TEXT NOT NULL,
          image TEXT NOT NULL, description TEXT NOT NULL,
          status TEXT NOT NULL DEFAULT 'disponivel', created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS leads(
          id INTEGER PRIMARY KEY AUTOINCREMENT,vehicle_id INTEGER,
          name TEXT NOT NULL,phone TEXT NOT NULL,interest TEXT NOT NULL,
          scheduled_for TEXT,consent INTEGER NOT NULL DEFAULT 0,
          status TEXT NOT NULL DEFAULT 'novo',created_at TEXT DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY(vehicle_id) REFERENCES vehicles(id) ON DELETE SET NULL
        );
        CREATE TABLE IF NOT EXISTS proposals(
          id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,phone TEXT NOT NULL,
          car TEXT NOT NULL,details TEXT,consent INTEGER NOT NULL DEFAULT 0,
          status TEXT NOT NULL DEFAULT 'novo',created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS customers(
          id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
          email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL,
          created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS customer_sessions(
          token_hash TEXT PRIMARY KEY, customer_id INTEGER NOT NULL,
          expires INTEGER NOT NULL,
          FOREIGN KEY(customer_id) REFERENCES customers(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS admins(
          id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL,
          password_hash TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS sessions(
          token_hash TEXT PRIMARY KEY,admin_id INTEGER NOT NULL,expires INTEGER NOT NULL,
          FOREIGN KEY(admin_id) REFERENCES admins(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS audit(
          id INTEGER PRIMARY KEY AUTOINCREMENT,admin_id INTEGER,action TEXT NOT NULL,
          target TEXT NOT NULL, target_id INTEGER,created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        if db.execute('SELECT COUNT(*) AS n FROM vehicles').fetchone()['n']==0:
            items=json.loads((ROOT/'data'/'seed_vehicles.json').read_text(encoding='utf-8'))
            columns=['id','brand','model','year','km','price','category','fuel','transmission','color','power','tag','image','description']
            db.executemany('INSERT INTO vehicles('+','.join(columns)+') VALUES('+','.join('?' for _ in columns)+')',[[v[k] for k in columns] for v in items])
        if db.execute('SELECT COUNT(*) AS n FROM admins').fetchone()['n']==0:
            pw=os.getenv('VELOUR_ADMIN_PASSWORD')
            if pw and len(pw)>=12:
                db.execute('INSERT INTO admins(username,password_hash) VALUES(?,?)',(os.getenv('VELOUR_ADMIN_USER','admin'),hash_password(pw)))
            else:
                print('AVISO: somente o ADMINISTRADOR exige 12+ caracteres. Cadastro de CLIENTE aceita 6+ caracteres. Configure VELOUR_ADMIN_PASSWORD para ativar o painel.')

def initialize_supabase():
    # Migrations are idempotent; applied only on the trusted Python server.
    ddl = (ROOT/'supabase'/'schema.sql').read_text(encoding='utf-8')
    with connect() as db:
        with db.conn.cursor() as cursor:
            cursor.execute(ddl, prepare=False)
        if db.execute('SELECT COUNT(*) AS n FROM vehicles').fetchone()['n'] == 0:
            items=json.loads((ROOT/'data'/'seed_vehicles.json').read_text(encoding='utf-8'))
            cols=['id','brand','model','year','km','price','category','fuel','transmission','color','power','tag','image','description']
            db.executemany('INSERT INTO vehicles('+','.join(cols)+') VALUES('+','.join('?' for _ in cols)+')', [[v[k] for k in cols] for v in items])
            db.execute("SELECT setval(pg_get_serial_sequence('vehicles','id'), (SELECT MAX(id) FROM vehicles))")
        if db.execute('SELECT COUNT(*) AS n FROM admins').fetchone()['n'] == 0:
            pw=os.getenv('VELOUR_ADMIN_PASSWORD')
            if pw and len(pw)>=12:
                db.execute('INSERT INTO admins(username,password_hash) VALUES(?,?)', (os.getenv('VELOUR_ADMIN_USER','admin'),hash_password(pw)))
            else: print('AVISO: somente o ADMINISTRADOR exige 12+ caracteres. Cadastro de CLIENTE aceita 6+ caracteres.')

def clean_text(obj,key,max_len=200,required=True):
    val=obj.get(key,'')
    if not isinstance(val,str): raise ValueError(f'{key}: formato inválido')
    val=val.strip()
    if required and not val:raise ValueError(f'{key}: campo obrigatório')
    if len(val)>max_len:raise ValueError(f'{key}: muito longo')
    return val

def phone_field(v):
    digits=re.sub(r'\D','',v)
    if not 10<=len(digits)<=13:raise ValueError('WhatsApp deve ter DDD e número válido')
    return digits

def vehicle_payload(data):
    v={}
    for field,limit in [('brand',80),('model',100),('category',35),('fuel',55),('transmission',65),('color',55),('power',30),('tag',80),('image',1500),('description',3000)]:v[field]=clean_text(data,field,limit)
    for field in ('year','km','price'):
        try:v[field]=int(data[field]) if field!='price' else float(data[field])
        except (ValueError,TypeError,KeyError):raise ValueError(f'{field}: número inválido')
    if not 1950<=v['year']<=datetime.now().year+2 or not 0<=v['km']<=2_000_000 or not 1000<=v['price']<=100_000_000:raise ValueError('Ano, quilometragem ou preço fora do intervalo permitido')
    if not v['image'].startswith('https://'):raise ValueError('Imagem deve usar URL HTTPS')
    v['status']=clean_text(data,'status',25)
    if v['status'] not in ('disponivel','reservado','vendido','rascunho'):raise ValueError('Status inválido')
    return v

class Handler(BaseHTTPRequestHandler):
    server_version='Velour/3.3'
    def log_message(self,*a):pass
    def headers_common(self,mime='application/json; charset=utf-8'):
        self.send_header('Content-Type',mime)
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','strict-origin-when-cross-origin')
        self.send_header('X-Frame-Options','DENY')
        self.send_header('Cache-Control','no-store')
    def respond(self,status,payload,cookie=None):
        body=json.dumps(payload,ensure_ascii=False,default=lambda v: v.isoformat() if isinstance(v,(datetime,)) else float(v) if isinstance(v,Decimal) else str(v)).encode()
        self.send_response(status);self.headers_common();self.send_header('Content-Length',str(len(body)))
        if cookie:self.send_header('Set-Cookie',cookie)
        self.end_headers();self.wfile.write(body)
    def body(self):
        try:n=int(self.headers.get('Content-Length','0'))
        except ValueError:raise ValueError('Tamanho inválido')
        if not 0<n<=MAX_BODY:raise ValueError('Corpo vazio ou muito grande')
        try:obj=json.loads(self.rfile.read(n))
        except json.JSONDecodeError:raise ValueError('JSON inválido')
        if not isinstance(obj,dict):raise ValueError('Objeto JSON esperado')
        return obj
    def current_admin(self):
        raw=self.headers.get('Cookie','')
        token=re.search(r'(?:^|;\s*)velour_session=([0-9a-f]{64})(?:;|$)',raw)
        if not token:return None
        with connect() as db:
            row=db.execute('SELECT a.id,a.username FROM admins a JOIN sessions s ON s.admin_id=a.id WHERE s.token_hash=? AND s.expires>?',(hashlib.sha256(token.group(1).encode()).hexdigest(),int(time.time()))).fetchone()
            return dict(row) if row else None
    def current_customer(self):
        raw=self.headers.get('Cookie','')
        match=re.search(r'(?:^|;\s*)velour_customer=([0-9a-f]{64})(?:;|$)',raw)
        if not match:return None
        with connect() as db:
            record=db.execute('SELECT c.id,c.name,c.email FROM customers c JOIN customer_sessions s ON s.customer_id=c.id WHERE s.token_hash=? AND s.expires>?',(hashlib.sha256(match.group(1).encode()).hexdigest(),int(time.time()))).fetchone()
            return dict(record) if record else None
    def customer_cookie(self,token,max_age=604800):
        secure='; Secure' if os.getenv('VELOUR_SECURE_COOKIES')=='1' else ''
        return f'velour_customer={token}; HttpOnly; SameSite=Lax; Path=/; Max-Age={max_age}{secure}'
    def require_admin(self):
        admin=self.current_admin()
        if not admin:raise PermissionError('Acesso administrativo necessário')
        return admin
    def origin_check(self):
        origin=self.headers.get('Origin')
        host=self.headers.get('Host','')
        if origin and origin not in ('http://'+host,'https://'+host):raise PermissionError('Origem não autorizada')
    def do_GET(self):
        path=urlsplit(self.path).path
        try:
            if path.startswith('/api/'):
                if path=='/api/health':
                    with connect() as db: db.execute('SELECT 1').fetchone()
                    return self.respond(200,{'ok':True,'version':'3.3','database':'supabase-postgresql' if SUPABASE_DATABASE_URL else 'local-sqlite'})
                if path=='/api/vehicles':
                    with connect() as db:
                        rows=db.execute("SELECT * FROM vehicles WHERE status!='rascunho' AND status!='vendido' ORDER BY id").fetchall()
                        return self.respond(200,{'items':[dict(r) for r in rows]})
                if re.fullmatch(r'/api/vehicles/\d+',path):
                    with connect() as db:r=db.execute('SELECT * FROM vehicles WHERE id=?',(int(path.rsplit('/',1)[-1]),)).fetchone()
                    return self.respond(200,dict(r)) if r else self.respond(404,{'error':'Veículo não encontrado'})
                if path=='/api/account/me':return self.respond(200,{'user':self.current_customer()})
                if path=='/api/admin/me':return self.respond(200,{'admin':self.current_admin()})
                if path=='/api/admin/vehicles':
                    self.require_admin()
                    with connect() as db:rows=db.execute('SELECT * FROM vehicles ORDER BY id DESC').fetchall()
                    return self.respond(200,{'items':[dict(r) for r in rows]})
                if path in ('/api/admin/leads','/api/admin/proposals'):
                    self.require_admin();table='leads' if path.endswith('leads') else 'proposals'
                    with connect() as db:rows=db.execute('SELECT * FROM '+table+' ORDER BY id DESC LIMIT 500').fetchall()
                    return self.respond(200,{'items':[dict(r) for r in rows]})
                return self.respond(404,{'error':'Rota não encontrada'})
            if path=='/':path='/index.html'
            target=(ROOT/path.lstrip('/')).resolve()
            if not target.is_relative_to(ROOT) or target.parts[:len((ROOT/'data').parts)]==(ROOT/'data').parts or target.name in ('server.py','README.md','requirements.txt','SUPABASE_SETUP.md') or any(part.startswith('.') for part in target.relative_to(ROOT).parts) or 'supabase' in target.relative_to(ROOT).parts or 'tests' in target.relative_to(ROOT).parts or target.suffix in ('.db','.py','.sqlite','.json'):
                return self.respond(403,{'error':'Acesso negado'})
            if not target.is_file():return self.respond(404,{'error':'Arquivo não encontrado'})
            content=target.read_bytes();mime=mimetypes.guess_type(target.name)[0] or 'application/octet-stream'
            if mime.startswith('text/') or mime=='application/javascript':mime+='; charset=utf-8'
            self.send_response(200);self.headers_common(mime);self.send_header('Content-Length',str(len(content)));self.end_headers();self.wfile.write(content)
        except PermissionError as e:self.respond(401,{'error':str(e)})
        except Exception as e:self.respond(500,{'error':'Erro interno do servidor'});print('GET ERROR',e)
    def do_POST(self):self.write_action('POST')
    def do_PATCH(self):self.write_action('PATCH')
    def do_DELETE(self):self.write_action('DELETE')
    def write_action(self,method):
        path=urlsplit(self.path).path
        try:
            self.origin_check()
            data=self.body() if method!='DELETE' else {}
            if path=='/api/account/register' and method=='POST':
                name=clean_text(data,'name',100)
                email=clean_text(data,'email',254).lower()
                password=clean_text(data,'password',256)
                if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+",email):raise ValueError('Informe um e-mail válido')
                if len(password)<6:raise ValueError('A senha do cliente precisa ter no mínimo 6 caracteres (letras, números ou símbolos)')
                if data.get('consent') is not True:raise ValueError('Leia e aceite a política de privacidade')
                with connect() as db:
                    try:
                        cur=db.execute('INSERT INTO customers(name,email,password_hash) VALUES(?,?,?)',(name,email,hash_password(password)))
                    except (sqlite3.IntegrityError, PG_UNIQUE_VIOLATION):return self.respond(409,{'error':'Este e-mail já está cadastrado'})
                    token=secrets.token_hex(32)
                    db.execute('INSERT INTO customer_sessions(token_hash,customer_id,expires) VALUES(?,?,?)',(hashlib.sha256(token.encode()).hexdigest(),cur.lastrowid,int(time.time())+604800))
                return self.respond(201,{'ok':True,'user':{'id':cur.lastrowid,'name':name,'email':email}},self.customer_cookie(token))
            if path=='/api/account/login' and method=='POST':
                email=clean_text(data,'email',254).lower()
                password=clean_text(data,'password',256)
                with connect() as db:
                    r=db.execute('SELECT * FROM customers WHERE email=?',(email,)).fetchone()
                    if not r or not verify_password(password,r['password_hash']):return self.respond(401,{'error':'E-mail ou senha inválidos'})
                    token=secrets.token_hex(32)
                    db.execute('INSERT INTO customer_sessions(token_hash,customer_id,expires) VALUES(?,?,?)',(hashlib.sha256(token.encode()).hexdigest(),r['id'],int(time.time())+604800))
                return self.respond(200,{'ok':True,'user':{'id':r['id'],'name':r['name'],'email':email}},self.customer_cookie(token))
            if path=='/api/account/logout' and method=='POST':
                match=re.search(r'velour_customer=([0-9a-f]{64})',self.headers.get('Cookie',''))
                with connect() as db:
                    if match:db.execute('DELETE FROM customer_sessions WHERE token_hash=?',(hashlib.sha256(match.group(1).encode()).hexdigest(),))
                return self.respond(200,{'ok':True},self.customer_cookie('',0))
            if path=='/api/admin/login' and method=='POST':
                user=clean_text(data,'username',80);pw=clean_text(data,'password',500)
                with connect() as db:
                    r=db.execute('SELECT * FROM admins WHERE username=?',(user,)).fetchone()
                    if not r or not verify_password(pw,r['password_hash']):return self.respond(401,{'error':'Usuário ou senha inválidos'})
                    token=secrets.token_hex(32)
                    db.execute('INSERT INTO sessions(token_hash,admin_id,expires) VALUES(?,?,?)',(hashlib.sha256(token.encode()).hexdigest(),r['id'],int(time.time())+28800))
                secure='; Secure' if os.getenv('VELOUR_SECURE_COOKIES')=='1' else ''
                return self.respond(200,{'ok':True},f'velour_session={token}; HttpOnly; SameSite=Strict; Path=/; Max-Age=28800{secure}')
            if path=='/api/admin/logout' and method=='POST':
                self.require_admin();match=re.search(r'velour_session=([0-9a-f]{64})',self.headers.get('Cookie',''))
                with connect() as db:
                    if match:db.execute('DELETE FROM sessions WHERE token_hash=?',(hashlib.sha256(match.group(1).encode()).hexdigest(),))
                return self.respond(200,{'ok':True},'velour_session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0')
            if path=='/api/leads' and method=='POST':
                name=clean_text(data,'name',120);phone=phone_field(clean_text(data,'phone',30));interest=clean_text(data,'interest',90)
                if interest not in ('Agendar uma visita','Solicitar mais informações','Simular financiamento','Avaliar meu usado na troca'):raise ValueError('Tipo de interesse inválido')
                if data.get('consent') is not True:raise ValueError('É necessário aceitar o uso dos dados para contato')
                v_id=data.get('vehicle_id');scheduled=clean_text(data,'scheduled_for',50,False)
                if scheduled and interest!='Agendar uma visita':raise ValueError('Agendamento não aplicável')
                if v_id is not None:
                    try:v_id=int(v_id)
                    except (ValueError,TypeError):raise ValueError('Veículo inválido')
                    with connect() as db:
                        if not db.execute("SELECT id FROM vehicles WHERE id=? AND status='disponivel'",(v_id,)).fetchone():raise ValueError('Veículo indisponível')
                with connect() as db:
                    cur=db.execute('INSERT INTO leads(vehicle_id,name,phone,interest,scheduled_for,consent) VALUES(?,?,?,?,?,1)',(v_id,name,phone,interest,scheduled))
                    return self.respond(201,{'ok':True,'protocol':f'INT-{cur.lastrowid:06d}','message':'Solicitação registrada. A equipe deverá analisar e entrar em contato.'})
            if path=='/api/proposals' and method=='POST':
                name=clean_text(data,'name',120);phone=phone_field(clean_text(data,'phone',30));car=clean_text(data,'car',200);details=clean_text(data,'details',1500,False)
                if data.get('consent') is not True:raise ValueError('É necessário aceitar o uso dos dados para contato')
                with connect() as db:
                    cur=db.execute('INSERT INTO proposals(name,phone,car,details,consent) VALUES(?,?,?,?,1)',(name,phone,car,details))
                    return self.respond(201,{'ok':True,'protocol':f'VEN-{cur.lastrowid:06d}','message':'Proposta registrada para análise.'})
            if path=='/api/admin/vehicles' and method=='POST':
                admin=self.require_admin();v=vehicle_payload(data);cols=list(v)
                with connect() as db:
                    cur=db.execute('INSERT INTO vehicles('+','.join(cols)+') VALUES('+','.join('?' for _ in cols)+')',[v[k] for k in cols]);db.execute('INSERT INTO audit(admin_id,action,target,target_id) VALUES(?,?,?,?)',(admin['id'],'create','vehicle',cur.lastrowid))
                    return self.respond(201,{'ok':True,'id':cur.lastrowid})
            m=re.fullmatch(r'/api/admin/vehicles/(\d+)',path)
            if m and method in ('PATCH','DELETE'):
                admin=self.require_admin();v_id=int(m.group(1))
                with connect() as db:
                    if not db.execute('SELECT id FROM vehicles WHERE id=?',(v_id,)).fetchone():return self.respond(404,{'error':'Veículo não encontrado'})
                    if method=='DELETE':db.execute('DELETE FROM vehicles WHERE id=?',(v_id,))
                    else:
                        v=vehicle_payload(data);db.execute('UPDATE vehicles SET '+','.join(k+'=?' for k in v)+' WHERE id=?',(*v.values(),v_id))
                    db.execute('INSERT INTO audit(admin_id,action,target,target_id) VALUES(?,?,?,?)',(admin['id'],method.lower(),'vehicle',v_id))
                return self.respond(200,{'ok':True})
            m=re.fullmatch(r'/api/admin/(leads|proposals)/(\d+)',path)
            if m and method=='PATCH':
                admin=self.require_admin();table,idx=m.group(1),int(m.group(2));status=clean_text(data,'status',25)
                if status not in ('novo','em_contato','concluido','arquivado'):raise ValueError('Status inválido')
                with connect() as db:
                    result=db.execute('UPDATE '+table+' SET status=? WHERE id=?',(status,idx))
                    if not result.rowcount:return self.respond(404,{'error':'Registro não encontrado'})
                    db.execute('INSERT INTO audit(admin_id,action,target,target_id) VALUES(?,?,?,?)',(admin['id'],'status',table,idx))
                return self.respond(200,{'ok':True})
            return self.respond(404,{'error':'Rota não encontrada'})
        except ValueError as e:self.respond(400,{'error':str(e)})
        except PermissionError as e:self.respond(401,{'error':str(e)})
        except Exception as e:print('WRITE ERROR',e);self.respond(500,{'error':'Erro interno do servidor'})

if __name__=='__main__':
    try:
        init_db()
        print('Banco de dados pronto: ' + ('Supabase PostgreSQL' if SUPABASE_DATABASE_URL else 'SQLite local (modo demonstracao)'), flush=True)
    except Exception as exc:
        print(f'ERRO AO PREPARAR O BANCO: {type(exc).__name__}: {exc}', flush=True)
        print('Confira o arquivo GUIA_RAPIDO_WINDOWS.txt. O servidor nao foi iniciado.', flush=True)
        sys.exit(1)
    try:
        server = ThreadingHTTPServer((HOST, PORT), Handler)
    except OSError as exc:
        print(f'ERRO AO ABRIR A PORTA {PORT}: {exc}', flush=True)
        print('A porta pode estar ocupada ou bloqueada. Execute INICIAR_VELOUR.bat ou configure VELOUR_PORT.', flush=True)
        sys.exit(2)
    url = f'http://{HOST}:{server.server_port}/'
    print(f'VELOUR PRONTO: {url}', flush=True)
    print('Deixe esta janela aberta. Para parar, pressione Ctrl+C.', flush=True)
    print('CADASTRO DE CLIENTE: senha com 6 ou mais caracteres | ADMIN: 12 ou mais.', flush=True)
    if os.getenv('VELOUR_OPEN_BROWSER', '0') == '1':
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Servidor encerrado.', flush=True)
    finally:
        server.server_close()
