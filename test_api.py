"""Testes de integração HTTP com banco isolado. Rodar: python -m unittest discover -s tests"""
import os,sys,unittest,tempfile,threading,json
from pathlib import Path
from http.server import ThreadingHTTPServer
from urllib.request import urlopen,Request
from urllib.error import HTTPError

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
os.environ['VELOUR_DB']=str(Path(tempfile.mkdtemp())/'test.db')
os.environ['VELOUR_ADMIN_PASSWORD']='UmaSenhaDeTesteSegura1234!'
import server
server.DB=Path(os.environ['VELOUR_DB'])

class APITest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  server.init_db();cls.srv=ThreadingHTTPServer(('127.0.0.1',0),server.Handler)
  cls.base='http://127.0.0.1:'+str(cls.srv.server_port)
  cls.worker=threading.Thread(target=cls.srv.serve_forever,daemon=True);cls.worker.start()
 @classmethod
 def tearDownClass(cls):cls.srv.shutdown();cls.srv.server_close()
 def req(self,path,body=None,method='GET',cookie=None):
  headers={'Content-Type':'application/json'}
  if cookie:headers['Cookie']=cookie
  rq=Request(self.base+path,data=json.dumps(body).encode() if body is not None else None,headers=headers,method=method)
  try:
   with urlopen(rq) as res:return res.status,json.load(res),res.headers
  except HTTPError as e:return e.code,json.load(e),e.headers
 def test_catalog_and_detail(self):
  status,data,_=self.req('/api/vehicles');self.assertEqual(status,200);self.assertEqual(len(data['items']),20)
  code,v,_=self.req('/api/vehicles/1');self.assertEqual(code,200);self.assertEqual(v['brand'],'Porsche')
 def test_lead_validation_and_create(self):
  p={'name':'Teste','phone':'(41) 99999-9999','interest':'Agendar uma visita','vehicle_id':1,'consent':True}
  status,d,_=self.req('/api/leads',p,'POST');self.assertEqual(status,201);self.assertTrue(d['protocol'].startswith('INT-'))
  p['consent']=False;status,_,_=self.req('/api/leads',p,'POST');self.assertEqual(status,400)
 def test_admin_auth_and_permissions(self):
  status,_,_=self.req('/api/admin/vehicles');self.assertEqual(status,401)
  status,_,h=self.req('/api/admin/login',{'username':'admin','password':'UmaSenhaDeTesteSegura1234!'},'POST');self.assertEqual(status,200)
  cookie=h.get('Set-Cookie').split(';',1)[0]
  status,d,_=self.req('/api/admin/vehicles',cookie=cookie);self.assertEqual(status,200);self.assertEqual(len(d['items']),20)
 def test_proposal(self):
  status,d,_=self.req('/api/proposals',{'name':'Maria','phone':'41999999999','car':'BMW M3 2024','details':'Teste','consent':True},'POST');self.assertEqual(status,201)
if __name__=='__main__':unittest.main()
