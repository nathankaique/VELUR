import unittest, json, tempfile, os, sys, threading
from pathlib import Path
from http.server import ThreadingHTTPServer
from urllib.request import Request,urlopen
from urllib.error import HTTPError
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import server
class CustomerAuthTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory();cls.previous=server.DB;server.DB=Path(cls.tmp.name)/'users.db';server.init_db()
  cls.srv=ThreadingHTTPServer(('127.0.0.1',0),server.Handler);cls.thread=threading.Thread(target=cls.srv.serve_forever,daemon=True);cls.thread.start()
 @classmethod
 def tearDownClass(cls):
  cls.srv.shutdown();cls.srv.server_close();server.DB=cls.previous;cls.tmp.cleanup()
 def req(self,path,body=None,cookie=None):
  headers={'Content-Type':'application/json'}
  if cookie:headers['Cookie']=cookie
  request=Request(f'http://127.0.0.1:{self.srv.server_port}'+path,data=json.dumps(body).encode() if body is not None else None,headers=headers,method='POST' if body is not None else 'GET')
  try:response=urlopen(request)
  except HTTPError as e:response=e
  with response:return response.status,json.load(response),response.headers
 def test_full_account_flow(self):
  data={'name':'Cliente Exemplo','email':'cliente@example.com','password':'123456','consent':True}
  status,created,headers=self.req('/api/account/register',data)
  self.assertEqual(status,201);self.assertEqual(created['user']['name'],'Cliente Exemplo')
  cookie=headers.get('Set-Cookie').split(';')[0]
  self.assertIn('HttpOnly',headers.get('Set-Cookie'))
  self.assertEqual(self.req('/api/account/me',cookie=cookie)[1]['user']['email'],data['email'])
  self.assertEqual(self.req('/api/account/register',data)[0],409)
  self.assertEqual(self.req('/api/account/login',{'email':data['email'],'password':'999999'})[0],401)
  self.assertEqual(self.req('/api/account/login',{'email':data['email'],'password':data['password']})[0],200)
  self.assertIsNone(self.req('/api/admin/me',cookie=cookie)[1]['admin'])
  self.assertEqual(self.req('/api/account/logout',{},cookie=cookie)[0],200)
  self.assertIsNone(self.req('/api/account/me',cookie=cookie)[1]['user'])
 def test_six_char_letters_numbers_and_duplicate_email(self):
  data={'name':'Teste Novo','email':'NOVA@Example.com','password':'abc123','consent':True}
  self.assertEqual(self.req('/api/account/register',data)[0],201)
  self.assertEqual(self.req('/api/account/register',{**data,'email':'nova@example.com'})[0],409)
  self.assertEqual(self.req('/api/account/login',{'email':'NOVA@example.com','password':'abc123'})[0],200)
 def test_weak_password_and_consent(self):
  data={'name':'Outro','email':'outro@example.com','password':'123','consent':True}
  self.assertEqual(self.req('/api/account/register',data)[0],400)
  data['password']='abc123';data['consent']=False
  self.assertEqual(self.req('/api/account/register',data)[0],400)
if __name__=='__main__':unittest.main()
