/* VÉLOUR Private Motors — demonstração front-end. Personalize o WhatsApp em CONFIG. */
const CONFIG = {
  whatsappNumber: '5511999999999', // Troque pelo número real com código do país e DDD, somente números.
  currency: 'BRL',
  locale: 'pt-BR'
};

let vehicles = [
 {id:1,brand:'Porsche',model:'911 Carrera S',year:2024,km:4200,price:1190000,category:'Esportivo',fuel:'Gasolina',transmission:'PDK automático',color:'Cinza Ártico',power:'450 cv',tag:'Seleção VÉLOUR',image:'https://commons.wikimedia.org/wiki/Special:FilePath/2024_Porsche_911_992_Carrera_S.jpg?width=1100',description:'A essência do esportivo alemão: engenharia de precisão, resposta imediata e um design que permanece relevante em qualquer época. Unidade selecionada para quem valoriza a experiência ao volante.'},
 {id:2,brand:'Mercedes-AMG',model:'GT 63 S 4MATIC+',year:2023,km:8900,price:1090000,category:'Esportivo',fuel:'Gasolina',transmission:'Automático',color:'Preto Obsidiana',power:'639 cv',tag:'Performance',image:'https://upload.wikimedia.org/wikipedia/commons/f/fe/Mercedes-AMG_GT_63_S_%28Facelift%29_1X7A7353.jpg',description:'Performance de superesportivo com refinamento de gran turismo. Um conjunto que combina potência, conforto e presença marcante.'},
 {id:3,brand:'Range Rover',model:'Autobiography',year:2024,km:6100,price:1190000,category:'SUV',fuel:'Híbrido',transmission:'Automático',color:'Santorini Black',power:'530 cv',tag:'Conforto absoluto',image:'https://autoimage.capitalone.com/dealer/2024-Land_Rover-Range_Rover-Autobiography-SALK1BE98RA236680-vauto_SALK1BE98RA236680_MP90461-1e7daebe041b5eec60f9439f09181ef4-bg_2.jpg?height=700&width=1000',description:'Sofisticação, tecnologia e capacidade em uma presença imponente. Interior acolhedor e condução refinada para todos os caminhos.'},
 {id:4,brand:'BMW',model:'M3 Competition',year:2024,km:3200,price:799000,category:'Sedã',fuel:'Gasolina',transmission:'Automático',color:'Verde Isle of Man',power:'510 cv',tag:'Baixa km',image:'https://images.dealersync.com/2968/Photos/1088036/20240127041827102_20240126_150434.jpg?_=3aa6650f6379a4ee9748ab1810724c73774e3736',description:'Um sedã esportivo que entrega precisão e emoção sem abrir mão da usabilidade. Acerto de chassi e motor para uma experiência visceral.'},
 {id:5,brand:'Ferrari',model:'Portofino M',year:2022,km:5800,price:2390000,category:'Conversível',fuel:'Gasolina',transmission:'Automático',color:'Rosso Corsa',power:'620 cv',tag:'Ícone italiano',image:'https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Ferrari_Portofino_M_IMG_4351.jpg/1280px-Ferrari_Portofino_M_IMG_4351.jpg',description:'A experiência de um grand tourer italiano com a liberdade de dirigir a céu aberto. Linhas esculturais e performance de alto nível.'},
 {id:6,brand:'Audi',model:'RS Q8 Performance',year:2025,km:2700,price:1090000,category:'SUV',fuel:'Gasolina',transmission:'Tiptronic',color:'Cinza Daytona',power:'640 cv',tag:'Performance',image:'https://imgd-ct.aeplcdn.com/1056x660/n/cw/ec/197993/rs-q8-facelift-left-front-three-quarter.jpeg?isig=0&q=85',description:'A versatilidade de um SUV de luxo com desempenho digno de um esportivo. Tecnologia, espaço e força em um pacote sofisticado.'},
 {id:7,brand:'Lamborghini',model:'Huracán EVO',year:2022,km:3900,price:3290000,category:'Esportivo',fuel:'Gasolina',transmission:'LDF automático',color:'Verde Mantis',power:'640 cv',tag:'Peça extraordinária',image:'https://commons.wikimedia.org/wiki/Special:FilePath/Lamborghini_Huracan_EVO_RWD.jpg?width=1100',description:'Design dramático, sonoridade inconfundível e engenharia de supercarro. Uma máquina criada para transformar cada trajeto em ocasião.'},
 {id:8,brand:'Porsche',model:'Cayenne Turbo GT',year:2023,km:7400,price:1390000,category:'SUV',fuel:'Gasolina',transmission:'Tiptronic S',color:'Branco Carrara',power:'659 cv',tag:'SUV esportivo',image:'https://img.goo-net.com/sss/magazine/2023/04/19/1681881054.jpg',description:'Uma combinação rara de espaço, luxo e comportamento esportivo. Feito para quem quer desempenho sem limitar a rotina.'},
 {id:9,brand:'BMW',model:'M8 Competition Convertible',year:2023,km:5200,price:1190000,category:'Conversível',fuel:'Gasolina',transmission:'Automático',color:'Azul Marina Bay',power:'625 cv',tag:'Grand touring',image:'https://mediapool.bmwgroup.com/cache/P9/201909/P90368340/P90368340-the-new-bmw-m8-competition-convertible-in-colour-brands-hatch-grey-and-20-m-light-alloy-wheels-star--2247px.jpg',description:'Elegância de um conversível de alto luxo aliada à força de um V8. Um convite para aproveitar a estrada com todos os sentidos.'},
 {id:10,brand:'Maserati',model:'Quattroporte Trofeo',year:2022,km:9800,price:899000,category:'Sedã',fuel:'Gasolina',transmission:'Automático',color:'Nero Ribelle',power:'580 cv',tag:'Elegância italiana',image:'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Maserati_Quattroporte_VI_Trofeo_Retro_Classics_2024_IMG_9027.jpg/1280px-Maserati_Quattroporte_VI_Trofeo_Retro_Classics_2024_IMG_9027.jpg',description:'Um sedã de personalidade única, com linhas italianas e um caráter esportivo que se revela ao dirigir.'},
 {id:11,brand:'Mercedes-AMG',model:'G 63',year:2024,km:1800,price:1890000,category:'SUV',fuel:'Gasolina',transmission:'Automático',color:'Branco Polar',power:'585 cv',tag:'Muito exclusivo',image:'https://upload.wikimedia.org/wikipedia/commons/0/0f/Mercedes-AMG_G_63_%2851856977905%29.jpg',description:'Um ícone de presença inconfundível. Combina capacidade, luxo artesanal e desempenho em uma silhueta reconhecida em qualquer lugar.'},
 {id:12,brand:'Aston Martin',model:'DBX707',year:2024,km:1900,price:2390000,category:'SUV',fuel:'Gasolina',transmission:'Automático',color:'Verde Racing',power:'707 cv',tag:'SUV de alta performance',image:'https://images.pistonheads.com/nimg/45984/blobid0.jpg',description:'Um SUV de luxo com motor V8 biturbo, acabamento artesanal e uma condução que equilibra conforto e performance.'},
 {id:13,brand:'Porsche',model:'911 Turbo S',year:2024,km:2100,price:1890000,category:'Esportivo',fuel:'Gasolina',transmission:'PDK automático',color:'Prata GT',power:'650 cv',tag:'Performance icônica',image:'https://commons.wikimedia.org/wiki/Special:FilePath/2023_Porsche_911_Turbo_S_1.jpg?width=1100',description:'Um 911 de altíssimo desempenho, com tração integral, aceleração contundente e usabilidade para o dia a dia.'},
 {id:14,brand:'Ferrari',model:'296 GTB',year:2023,km:1600,price:3490000,category:'Esportivo',fuel:'Híbrido plug-in',transmission:'Dupla embreagem',color:'Rosso Corsa',power:'830 cv',tag:'Tecnologia híbrida',image:'https://commons.wikimedia.org/wiki/Special:FilePath/Ferrari_296_GTB.jpg?width=1100',description:'Berlinetta híbrida que combina motor V6 biturbo e propulsão elétrica em uma experiência esportiva de nova geração.'},
 {id:15,brand:'Lamborghini',model:'Urus S',year:2024,km:2800,price:2690000,category:'SUV',fuel:'Gasolina',transmission:'Automático',color:'Nero Noctis',power:'666 cv',tag:'SUV superesportivo',image:'https://commons.wikimedia.org/wiki/Special:FilePath/2024_Lamborghini_Urus_S.jpg?width=1100',description:'Um SUV de personalidade marcante, com motor V8 biturbo, posição de condução elevada e desempenho esportivo.'},
 {id:16,brand:'McLaren',model:'720S',year:2022,km:3900,price:2990000,category:'Esportivo',fuel:'Gasolina',transmission:'SSG de 7 marchas',color:'Laranja McLaren',power:'720 cv',tag:'Engenharia de pista',image:'https://upload.wikimedia.org/wikipedia/commons/6/6c/McLaren_720S_Orange.jpg',description:'Supercarro leve e aerodinâmico, projetado para respostas rápidas e alto desempenho em estrada e pista.'},
 {id:17,brand:'Bentley',model:'Continental GT Speed Convertible',year:2023,km:4300,price:2790000,category:'Conversível',fuel:'Gasolina',transmission:'Automático',color:'Azul Imperial',power:'659 cv',tag:'Grand touring de luxo',image:'https://s3.amazonaws.com/dcmcarimages/car-images/Bentley/Continental-GT-Speed/650393/SCBDT4ZG4NC003590_1_7338.jpg',description:'Gran turismo de luxo com acabamento refinado, alto conforto e potência para viagens longas com personalidade.'},
 {id:18,brand:'Rolls-Royce',model:'Cullinan',year:2023,km:3500,price:4890000,category:'SUV',fuel:'Gasolina',transmission:'Automático',color:'Preto Diamante',power:'571 cv',tag:'Luxo sob medida',image:'https://autocentrumgroup.pl/wp-content/uploads/2024/10/2019_Rolls-Royce_Cullinan_V12_Automatic_6.75_Front-scaled.jpg',description:'SUV de ultra luxo que prioriza conforto, materiais nobres e uma experiência de viagem silenciosa e sofisticada.'},
 {id:19,brand:'BMW',model:'X6 M Competition',year:2024,km:2400,price:1190000,category:'SUV',fuel:'Gasolina',transmission:'Automático M Steptronic',color:'Cinza Brooklyn',power:'625 cv',tag:'M Performance',image:'https://upload.wikimedia.org/wikipedia/commons/9/98/BMW_X6_M_Competition_%28G06%29_IMG_3572.jpg',description:'SUV cupê com preparação M, motor V8 e comportamento dinâmico pensado para unir presença e performance.'},
 {id:20,brand:'Mercedes-Benz',model:'S 580 4MATIC',year:2024,km:1700,price:1090000,category:'Sedã',fuel:'Gasolina híbrido leve',transmission:'Automático 9G-TRONIC',color:'Preto Obsidiana',power:'503 cv',tag:'Conforto executivo',image:'https://img.sm360.ca/ir/w800h600/images/promo/humberviewgroup-941/204489/36953837_09266_11482664_15126977031759350871469.jpg',description:'Sedã executivo de alto luxo, com foco em conforto, tecnologia embarcada e refinamento para viagens.'}
];

const state = {category:'Todos',search:'',brand:'',price:'',sort:'featured',yearMin:'',kmMax:'',fuel:'',transmission:'',favorites:loadFavorites(),showFavorites:false,visible:6,selectedVehicle:null};
const $ = (selector,root=document)=>root.querySelector(selector);
const $$ = (selector,root=document)=>[...root.querySelectorAll(selector)];
const money = value => new Intl.NumberFormat(CONFIG.locale,{style:'currency',currency:CONFIG.currency,maximumFractionDigits:0}).format(value);
const number = value => new Intl.NumberFormat(CONFIG.locale).format(value);
function loadFavorites(){try{return JSON.parse(localStorage.getItem('velour-favorites')||'[]')}catch{return []}}
function saveFavorites(){try{localStorage.setItem('velour-favorites',JSON.stringify(state.favorites))}catch{} $('#favCount').textContent=state.favorites.length}
function showToast(message){$('#toastMessage').textContent=message;bootstrap.Toast.getOrCreateInstance($('#appToast'),{delay:2800}).show()}
function safeText(value){return String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function initBrands(){const select=$('#brandFilter');[...new Set(vehicles.map(v=>v.brand))].sort().forEach(brand=>{const option=document.createElement('option');option.value=brand;option.textContent=brand;select.append(option)})}
function filteredVehicles(){let list=vehicles.filter(v=>{const text=`${v.brand} ${v.model} ${v.year} ${v.category}`.toLowerCase();const matchesText=text.includes(state.search.toLowerCase());const matchesBrand=!state.brand||v.brand===state.brand;const matchesCategory=state.category==='Todos'||v.category===state.category;const matchesPrice=!state.price||(()=>{const [min,max]=state.price.split('-').map(Number);return v.price>=min&&v.price<=max})();const matchesAdvanced=(!state.yearMin||v.year>=Number(state.yearMin))&&(!state.kmMax||v.km<=Number(state.kmMax))&&(!state.fuel||v.fuel===state.fuel)&&(!state.transmission||v.transmission===state.transmission);const matchesFavorite=!state.showFavorites||state.favorites.includes(v.id);return matchesText&&matchesBrand&&matchesCategory&&matchesPrice&&matchesAdvanced&&matchesFavorite});switch(state.sort){case'priceAsc':list.sort((a,b)=>a.price-b.price);break;case'priceDesc':list.sort((a,b)=>b.price-a.price);break;case'yearDesc':list.sort((a,b)=>b.year-a.year);break;case'kmAsc':list.sort((a,b)=>a.km-b.km);break;default:list.sort((a,b)=>a.id-b.id)}return list}
function isSold(v){return v.status==='vendido'||!String(v.image||'').trim()}
function markSold(card){
 if(!card||card.classList.contains('is-sold'))return;
 card.classList.add('is-sold');
 const image=card.querySelector('.car-image');if(image){image.removeAttribute('src');image.alt='Veículo vendido';}
 const cover=card.querySelector('.car-image-wrap');if(cover){cover.classList.add('sold-image');cover.dataset.fallback='VENDIDO';}
 const tag=card.querySelector('.car-tag');if(tag)tag.textContent='Vendido';
 const priceLabel=card.querySelector('.car-price-label');if(priceLabel)priceLabel.textContent='Status';
 const price=card.querySelector('.car-price');if(price)price.textContent='Vendido';
 const link=card.querySelector('.car-open');if(link){link.removeAttribute('href');link.replaceWith(Object.assign(document.createElement('span'),{className:'sold-message',textContent:'Este veículo já foi vendido'}));}
 const specs=card.querySelector('.car-specs');if(specs){const note=document.createElement('p');note.className='sold-note';note.textContent='Unidade indisponível. Explore outros veículos da coleção.';specs.after(note)}
}
function showUnavailableImage(card){
 if(!card||card.classList.contains('is-sold'))return;
 const img=card.querySelector('img.car-image');
 if(img){img.classList.add('image-unavailable');img.removeAttribute('src');img.alt='Imagem indisponível';}
 const cover=card.querySelector('.car-image-wrap');
 if(cover)cover.dataset.fallback='IMAGEM INDISPONÍVEL';
}
function updateSoldCards(){document.querySelectorAll('.car-card').forEach(card=>{if(card.dataset.sold==='true')markSold(card);const img=card.querySelector('img.car-image');if(img&&img.complete&&img.naturalWidth===0)showUnavailableImage(card)})}
$('#carGrid').addEventListener('error',e=>{if(e.target.matches('img.car-image'))showUnavailableImage(e.target.closest('.car-card'))},true);
function renderCars(){const list=filteredVehicles();const shown=list.slice(0,state.visible);$('#resultCount').textContent=state.showFavorites?`${list.length} favorito${list.length===1?'':'s'}`:`${list.length} veículo${list.length===1?'':'s'} na coleção`;$('#carGrid').innerHTML=shown.map(v=>`<article class="car-card card" data-sold="${isSold(v)}"><div class="car-image-wrap" data-fallback="${safeText(v.brand+' '+v.model)}"><img class="car-image" src="${safeText(v.image||'')}" alt="${safeText(v.brand+' '+v.model)}" loading="lazy" decoding="async" onerror="this.onerror=null;this.classList.add('image-unavailable');this.alt='Imagem indisponível: ${safeText(v.brand+' '+v.model)}';this.removeAttribute('src')"><span class="car-tag">${safeText(v.tag)}</span><button class="favorite-btn ${state.favorites.includes(v.id)?'active':''}" data-favorite="${v.id}" aria-label="${state.favorites.includes(v.id)?'Remover dos':'Adicionar aos'} favoritos" aria-pressed="${state.favorites.includes(v.id)}">${state.favorites.includes(v.id)?'♥':'♡'}</button></div><div class="car-info card-body"><div class="car-brand">${safeText(v.brand)}</div><h3 class="car-title">${safeText(v.model)}</h3><div class="car-specs"><span>◷ ${v.year}</span><span>↗ ${number(v.km)} km</span><span>⚙ ${safeText(v.transmission)}</span></div><div class="car-footer"><div><div class="car-price-label">A partir de</div><div class="car-price">${money(v.price)}</div></div><a class="car-open" href="veiculo.html?id=${v.id}">Ver ficha completa ↗</a></div></div></article>`).join('');$('#emptyState').classList.toggle('d-none',list.length>0);$('#carGrid').classList.toggle('d-none',list.length===0);$('#loadMore').classList.toggle('d-none',list.length<=state.visible);$('#loadMore').textContent=`Carregar mais veículos ↓`;$('#favoritesNav').setAttribute('aria-label',state.showFavorites?'Voltar à coleção':'Ver favoritos');updateSoldCards()}
function toggleFavorite(id){const idx=state.favorites.indexOf(id);if(idx>=0){state.favorites.splice(idx,1);showToast('Veículo removido dos favoritos.')}else{state.favorites.push(id);showToast('Veículo salvo nos favoritos.')}saveFavorites();renderCars()}
function openDetails(id){const v=vehicles.find(item=>item.id===id);if(!v)return;state.selectedVehicle=v;$('#carModalBody').innerHTML=`<div class="modal-image-wrap" data-fallback="${safeText(v.brand+' '+v.model)}"><img class="modal-car-image" src="${v.image}" alt="${safeText(v.brand+' '+v.model)}" loading="eager" decoding="async" onerror="this.onerror=null;this.classList.add('image-unavailable');this.alt='Imagem indisponível: ${safeText(v.brand+' '+v.model)}';this.removeAttribute('src')"></div><div class="car-brand">${safeText(v.brand)} · ${v.year}</div><h2 class="modal-car-title" id="carModalTitle">${safeText(v.model)}</h2><div class="modal-car-price">${money(v.price)}</div><p class="modal-description">${safeText(v.description)}</p><div class="modal-spec-grid"><div class="modal-spec"><small>Quilometragem</small><strong>${number(v.km)} km</strong></div><div class="modal-spec"><small>Potência</small><strong>${safeText(v.power)}</strong></div><div class="modal-spec"><small>Combustível</small><strong>${safeText(v.fuel)}</strong></div><div class="modal-spec"><small>Transmissão</small><strong>${safeText(v.transmission)}</strong></div><div class="modal-spec"><small>Cor</small><strong>${safeText(v.color)}</strong></div><div class="modal-spec"><small>Categoria</small><strong>${safeText(v.category)}</strong></div></div><div class="d-flex flex-wrap gap-2"><button class="btn btn-primary flex-grow-1" id="askAboutCar">Tenho interesse neste veículo <span>↗</span></button><button class="btn btn-outline-light" id="shareCar">Compartilhar</button></div><p class="privacy-note">Informações e disponibilidade devem ser confirmadas com a equipe VÉLOUR. Imagens ilustrativas nesta demonstração.</p>`;bootstrap.Modal.getOrCreateInstance($('#carModal')).show()}
function openContact(vehicle){state.selectedVehicle=vehicle||null;$('#contactCarName').textContent=vehicle?`Interesse em: ${vehicle.brand} ${vehicle.model} — ${money(vehicle.price)}`:'Conte um pouco sobre o que você procura.';bootstrap.Modal.getOrCreateInstance($('#contactModal')).show()}
function whatsappUrl(message){return `https://wa.me/${CONFIG.whatsappNumber}?text=${encodeURIComponent(message)}`}
function validWhatsAppConfigured(){return /^\d{10,15}$/.test(CONFIG.whatsappNumber)&&!CONFIG.whatsappNumber.endsWith('9999999999')}
function contactWhatsApp(message){if(validWhatsAppConfigured()){window.open(whatsappUrl(message),'_blank','noopener,noreferrer')}else{const mail=`mailto:atendimento@velour.com.br?subject=${encodeURIComponent('Contato VÉLOUR')}&body=${encodeURIComponent(message+'\n\nConfigure o número real de WhatsApp em script.js para habilitar o contato direto.')}`;window.location.href=mail;showToast('Configure o WhatsApp real no script.js. Abrindo alternativa por e-mail.') }}
function clearFilters(){state.category='Todos';state.search='';state.brand='';state.price='';state.showFavorites=false;state.visible=6;state.yearMin='';state.kmMax='';state.fuel='';state.transmission='';['yearMin','kmMax','fuelFilter','transmissionFilter'].forEach(id=>{$('#'+id).value=''});$('#searchText').value='';$('#brandFilter').value='';$('#priceFilter').value='';$$('.chip').forEach(c=>c.classList.toggle('active',c.dataset.category==='Todos'));renderCars()}
$('#searchForm').addEventListener('submit',e=>{e.preventDefault();state.search=$('#searchText').value.trim();state.brand=$('#brandFilter').value;state.price=$('#priceFilter').value;state.visible=6;state.showFavorites=false;renderCars();$('#estoque').scrollIntoView({behavior:'smooth'})});
$('#categoryChips').addEventListener('click',e=>{const button=e.target.closest('[data-category]');if(!button)return;state.category=button.dataset.category;state.visible=6;state.showFavorites=false;$$('.chip').forEach(c=>c.classList.toggle('active',c===button));renderCars()});
$('#sortSelect').addEventListener('change',e=>{state.sort=e.target.value;renderCars()});$('#carGrid').addEventListener('click',e=>{const fav=e.target.closest('[data-favorite]');const details=e.target.closest('[data-details]');if(fav)toggleFavorite(Number(fav.dataset.favorite));if(details)openDetails(Number(details.dataset.details))});
$('#loadMore').addEventListener('click',()=>{state.visible+=3;renderCars()});$('#clearFilters').addEventListener('click',clearFilters);$('#favoritesNav').addEventListener('click',()=>{state.showFavorites=!state.showFavorites;state.visible=6;state.search='';state.brand='';state.price='';$('#searchText').value='';$('#brandFilter').value='';$('#priceFilter').value='';state.category='Todos';$$('.chip').forEach(c=>c.classList.toggle('active',c.dataset.category==='Todos'));renderCars();$('#estoque').scrollIntoView({behavior:'smooth'});if(state.showFavorites&&state.favorites.length===0)showToast('Você ainda não salvou favoritos. Toque no coração de um veículo.')});
$('#carModalBody').addEventListener('click',async e=>{if(e.target.closest('#askAboutCar')){bootstrap.Modal.getOrCreateInstance($('#carModal')).hide();openContact(state.selectedVehicle)}if(e.target.closest('#shareCar')){const v=state.selectedVehicle;const shareText=`Conheça o ${v.brand} ${v.model} (${v.year}) na VÉLOUR — ${money(v.price)}.`;try{if(navigator.share)await navigator.share({title:`${v.brand} ${v.model} | VÉLOUR`,text:shareText,url:location.href+'#estoque'});else if(navigator.clipboard){await navigator.clipboard.writeText(shareText);showToast('Resumo copiado para compartilhar.')}else showToast(shareText)}catch(err){if(err.name!=='AbortError')showToast('Não foi possível compartilhar agora.')}}});
async function apiSubmit(path,payload){
  const res=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  const data=await res.json();if(!res.ok)throw new Error(data.error||'Não foi possível registrar.');return data;
}
function setSubmitState(form,busy){const b=form.querySelector('[type="submit"]');b.disabled=busy;b.dataset.label ||= b.textContent;b.textContent=busy?'Registrando...':b.dataset.label}
$('#contactForm').addEventListener('submit',async e=>{
  e.preventDefault();const f=e.currentTarget;setSubmitState(f,true);
  const v=state.selectedVehicle;
  try{
    const data=await apiSubmit('/api/leads',{name:$('#buyerName').value,phone:$('#buyerPhone').value,interest:$('#buyerInterest').value,vehicle_id:v?v.id:null,scheduled_for:$('#scheduledFor').value,consent:$('#buyerConsent').checked});
    bootstrap.Modal.getOrCreateInstance($('#contactModal')).hide();f.reset();showToast(`Solicitação registrada: ${data.protocol}. Aguarde a confirmação da equipe.`)
  }catch(err){showToast(err.message)}finally{setSubmitState(f,false)}
});
$('#sellerForm').addEventListener('submit',async e=>{
  e.preventDefault();const f=e.currentTarget;setSubmitState(f,true);
  try{const data=await apiSubmit('/api/proposals',{name:$('#sellerName').value,phone:$('#sellerPhone').value,car:$('#sellerCar').value,details:$('#sellerMessage').value,consent:$('#sellerConsent').checked});f.reset();showToast(`Apresentação registrada: ${data.protocol}. A equipe poderá entrar em contato.`)}
  catch(err){showToast(err.message)}finally{setSubmitState(f,false)}
});
$('#whatsappLink').addEventListener('click',e=>{e.preventDefault();contactWhatsApp('Olá! Gostaria de conversar com a equipe VÉLOUR sobre os veículos disponíveis.')});
$('#sellerPhone').addEventListener('input',e=>formatPhone(e.target));$('#buyerPhone').addEventListener('input',e=>formatPhone(e.target));function formatPhone(input){let digits=input.value.replace(/\D/g,'').slice(0,11);if(digits.length>10)input.value=digits.replace(/(\d{2})(\d{5})(\d{4})/,'($1) $2-$3');else if(digits.length>6)input.value=digits.replace(/(\d{2})(\d{4})(\d{0,4})/,'($1) $2-$3');else if(digits.length>2)input.value=digits.replace(/(\d{2})(\d{0,5})/,'($1) $2')}
// Hero com vídeo stock de supercarro em circuito, sem player nem marca d'água do YouTube.
// O vídeo começa mudo por regra dos navegadores; a primeira interação tenta ativar o áudio do próprio arquivo.
const heroVideo = $('#heroVideo');
if (heroVideo) {
  let soundEnabled = false;
  const enableOriginalVideoSound = () => {
    if (soundEnabled) return;
    heroVideo.muted = false;
    heroVideo.volume = 0.85;
    const playback = heroVideo.play();
    if (playback && typeof playback.then === 'function') {
      playback.then(() => {
        soundEnabled = true;
        const hint = $('#heroSoundHint');
        if (hint) hint.textContent = 'SOM DO CLIPE ATIVADO · SUPERCAR EM MOVIMENTO';
        document.removeEventListener('pointerdown', enableOriginalVideoSound);
        document.removeEventListener('keydown', enableOriginalVideoSound);
        document.removeEventListener('touchstart', enableOriginalVideoSound);
      }).catch(() => { heroVideo.muted = true; });
    } else {
      soundEnabled = true;
    }
  };
  document.addEventListener('pointerdown', enableOriginalVideoSound, {passive:true});
  document.addEventListener('keydown', enableOriginalVideoSound);
  document.addEventListener('touchstart', enableOriginalVideoSound, {passive:true});
}
$('#year').textContent=new Date().getFullYear();saveFavorites();
function configureFacets(){const options=(id,values)=>{const el=$('#'+id);const first=el.options[0];el.replaceChildren(first);[...new Set(values)].sort().forEach(value=>el.add(new Option(value,value)))};options('fuelFilter',vehicles.map(v=>v.fuel));options('transmissionFilter',vehicles.map(v=>v.transmission));$('#brandFilter').replaceChildren(new Option('Todas as marcas',''));initBrands()}
$('#applyAdvanced').addEventListener('click',()=>{state.yearMin=$('#yearMin').value;state.kmMax=$('#kmMax').value;state.fuel=$('#fuelFilter').value;state.transmission=$('#transmissionFilter').value;state.visible=6;renderCars()});
async function initCatalog(){
  // Sem servidor, conservar os veículos ilustrativos já definidos neste arquivo.
  try {
    const response = await fetch('/api/vehicles', {headers:{Accept:'application/json'}});
    if (!response.ok) throw Error('API indisponível');
    const data = await response.json();
    if (!Array.isArray(data.items)) throw Error('Resposta inválida');
    vehicles = data.items;
  } catch (error) {
    console.warn('VÉLOUR: catálogo ilustrativo local. API indisponível.',error);
  }
  configureFacets();
  renderCars();
}
initCatalog();

// Reutiliza o mesmo fluxo de contato do WhatsApp no rodapé.
document.getElementById("footerWhatsapp")?.addEventListener("click", e=>{e.preventDefault();document.getElementById("whatsappLink")?.click()});
