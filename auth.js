const el=id=>document.getElementById(id);const msg=(s,error=false)=>{el('authMessage').textContent=s;el('authMessage').classList.toggle('error',error)};
const tabs=[['login','tabLogin','loginPanel'],['register','tabRegister','registerPanel']];
function switchTab(tab){tabs.forEach(([name,button,panel])=>{const selected=name===tab;el(button).classList.toggle('active',selected);el(button).setAttribute('aria-selected',String(selected));el(panel).hidden=!selected});el('authHeading').textContent=tab==='login'?'Acesse sua conta':'Cadastre-se na VÉLOUR';msg('');history.replaceState(null,'','#'+tab)}
el('tabLogin').onclick=()=>switchTab('login');el('tabRegister').onclick=()=>switchTab('register');
async function api(path,body){const res=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json'},credentials:'same-origin',body:JSON.stringify(body)});const data=await res.json();if(!res.ok)throw new Error(data.error||'Não foi possível concluir.');return data}
function showAccount(user){el('authForms').hidden=true;el('currentAccount').hidden=false;el('welcomeName').textContent='Olá, '+user.name.split(' ')[0]+'!';el('welcomeEmail').textContent=user.email}
async function submitForm(event,type){event.preventDefault();const button=event.target.querySelector('[type=submit]');button.disabled=true;msg('');try{const isRegister=type==='register';const body=isRegister?{name:el('registerName').value.trim(),email:el('registerEmail').value.trim(),password:el('registerPassword').value,consent:el('registerConsent').checked}:{email:el('loginEmail').value.trim(),password:el('loginPassword').value};if(isRegister && body.password.length < 6)throw new Error('A senha do cliente precisa ter no mínimo 6 caracteres');const data=await api('/api/account/'+(isRegister?'register':'login'),body);showAccount(data.user)}catch(err){msg(err.message,true)}finally{button.disabled=false}}
el('loginPanel').addEventListener('submit',ev=>submitForm(ev,'login'));el('registerPanel').addEventListener('submit',ev=>submitForm(ev,'register'));
el('logoutButton').addEventListener('click',async()=>{try{await api('/api/account/logout',{});el('currentAccount').hidden=true;el('authForms').hidden=false;el('loginPanel').reset();el('registerPanel').reset();switchTab('login')}catch(err){alert(err.message)}});
if(location.hash==='#register')switchTab('register');fetch('/api/account/me',{credentials:'same-origin'}).then(r=>r.json()).then(d=>{if(d.user)showAccount(d.user)}).catch(()=>{});

// A visibilidade é controlada exclusivamente pelo botão correspondente.
// O input permanece no DOM, preservando o texto e a posição do cursor.
for (const button of document.querySelectorAll('.vl-password-toggle')) {
  const field = document.getElementById(button.getAttribute('data-for'));
  if (!field) continue;
  const refresh = () => {
    const visible = field.type === 'text';
    button.classList.toggle('is-visible', visible);
    button.setAttribute('aria-pressed', String(visible));
    button.setAttribute('aria-label', visible ? 'Ocultar senha' : 'Mostrar senha');
    button.setAttribute('title', visible ? 'Ocultar senha' : 'Mostrar senha');
  };
  button.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M2 12s3.7-6 10-6 10 6 10 6-3.7 6-10 6S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/><path class="vl-eye-slash" d="M4 4 20 20"/></svg>';
  refresh();
  button.addEventListener('click', (event) => {
    event.preventDefault();
    const start = field.selectionStart;
    const end = field.selectionEnd;
    field.type = field.type === 'password' ? 'text' : 'password';
    refresh();
    field.focus({preventScroll: true});
    try { if (start != null && end != null) field.setSelectionRange(start, end); } catch (_) {}
  });
}
