> **Supabase:** as 8 tabelas foram criadas no projeto VELOUR. Consulte `SUPABASE_SETUP.md` para configurar a conexão do servidor e importar automaticamente os 20 veículos.

# VÉLOUR Private Motors | Versão 2.0

Projeto de demonstração acadêmica de marketplace de veículos premium, ampliado com API, banco de dados SQLite, painel administrativo, catálogo persistente, fichas individuais e captação de contatos.

## Requisitos

- Python 3.10 ou superior. Não é preciso instalar bibliotecas externas.
- Navegador moderno e internet para Google Fonts, Bootstrap, vídeo e fotos hospedadas em terceiros.

## Instalação no Windows (PowerShell)

Abra a pasta `velour-marketplace` no VS Code. No terminal PowerShell:

```powershell
$env:VELOUR_ADMIN_USER="admin"
$env:VELOUR_ADMIN_PASSWORD="CrieUmaSenhaForteComMaisDe12Caracteres!"
python server.py
```

Se `python` não funcionar, experimente `py server.py`.

Abra **http://127.0.0.1:8000/** no navegador. Painel em **http://127.0.0.1:8000/admin.html**. Não abra o HTML por `file://` ou Live Server, pois a API do banco é servida pelo Python.

**Importante:** a senha precisa ser definida antes da primeira execução. Se o banco for criado sem senha, nenhum administrador inicial será configurado. Em uma instalação de teste recém-criada, remova o arquivo `data/velour.db`, defina a senha e execute novamente. Se já tiver cadastros, não remova o banco: faça backup e crie a conta com procedimento administrativo controlado.

## Funcionalidades

- Página inicial responsiva com vídeos, busca, categorias e ordenação.
- Catálogo de 20 veículos de demonstração importados na primeira inicialização para o SQLite.
- Filtros avançados por ano mínimo, km máxima, combustível e transmissão.
- Favoritos no navegador, cards com fallback de imagem, compartilhamento.
- Ficha de veículo `veiculo.html?id=1`, com informações e solicitação de atendimento.
- Formulários de compra/visita e apresentação para venda, salvos na API com número de protocolo.
- Consentimento de contato e página informativa sobre privacidade.
- Área da equipe com login, autenticação por cookie de sessão, CRUD de veículos, status e listagem de contatos e propostas.
- Auditoria básica das alterações administrativas.

## Mapa de fluxos

```text
Início -> Busca/Filtros -> Catálogo -> Ficha do veículo -> Registrar interesse -> Protocolo
Início -> Quero anunciar -> Dados e consentimento -> Protocolo -> Painel de propostas
Área da equipe -> Login -> Veículos -> Criar/Editar/Excluir
Área da equipe -> Login -> Interesses/Propostas -> Atualizar status
```

## Rotas

- `GET /api/health`
- `GET /api/vehicles`
- `GET /api/vehicles/:id`
- `POST /api/leads`
- `POST /api/proposals`
- `POST /api/admin/login`, `POST /api/admin/logout`, `GET /api/admin/me`
- `GET/POST /api/admin/vehicles`
- `PATCH/DELETE /api/admin/vehicles/:id`
- `GET /api/admin/leads`, `PATCH /api/admin/leads/:id`
- `GET /api/admin/proposals`, `PATCH /api/admin/proposals/:id`

O banco inicial `data/velour.db` é criado automaticamente. Nunca publique, envie ou compartilhe um banco que contenha dados pessoais de contatos reais.

## Configurações

No `script.js`, troque `CONFIG.whatsappNumber` por um número comercial legítimo. Sem isso, os links de contato direcionam para o e-mail demonstrativo. Antes de comercializar, substitua também o e-mail, textos, preços e fotos ilustrativas e verifique licenças de mídia.

Variáveis opcionais: `VELOUR_HOST` (padrão 127.0.0.1), `VELOUR_PORT` (8000), `VELOUR_DB` (caminho SQLite), `VELOUR_SECURE_COOKIES=1` (em HTTPS), `VELOUR_ADMIN_USER`, `VELOUR_ADMIN_PASSWORD` (somente primeira criação).

## Limitações e cuidados

**O projeto é uma base funcional para desenvolvimento e avaliação local, não um software auditado para produção.** Não há transação de pagamento, simulador financeiro real, compra concluída, envio automático de e-mails/SMS, disponibilidade em tempo real externa, upload próprio de fotos, favoritos em nuvem ou cadastro de compradores. Solicitações de visita não são agendamentos confirmados. Os campos de mídia usam URLs remotas.

Antes de hospedar publicamente: configurar HTTPS e proxy, cookies seguros, limites de requisição e bloqueio de ataques de login, CSRF token em formulários autenticados, proteção contra spam, autenticação reforçada, revisão de segurança, backups, LGPD/política jurídica definitiva, registros de consentimento, métricas e testes de acessibilidade. Use um banco robusto e serviços de armazenamento/entrega apropriados se houver escala de produção.

## Arquivos

- `index.html`, `style.css`, `script.js`: vitrine.
- `veiculo.html`, `veiculo.js`: ficha individual.
- `admin.html`, `admin.css`, `admin.js`: equipe.
- `privacidade.html`: nota informativa.
- `server.py`: API e SQLite.
- `data/seed_vehicles.json`: catálogo ilustrativo de partida.
- `tests/test_api.py`: testes automatizados básicos.

## Atualização 2.1: componentes padronizados

A pasta `components/` reúne tokens, dois botões oficiais, campos e estilos de composição; veja a vitrine em `http://127.0.0.1:8000/components/`. Componente 01 é primário; Componente 02 é secundário. A página inicial ganhou rodapé organizado em quatro áreas, tratamento do hover de WhatsApp/e-mail e enquadramento responsivo da foto da seção Nossa filosofia. Dados comerciais reais não foram inventados; configure o canal de contato antes de publicar. Leia `components/README.md`.


## VÉLOUR 2.2 — Acesso de clientes
- Página única `conta.html` com abas **01 Entrar** e **02 Criar conta**, vinculadas a `components/auth.css` e `components/auth.js`.
- Link **Entrar / Minha conta** no cabeçalho principal.
- Backend real: `POST /api/account/register`, `POST /api/account/login`, `POST /api/account/logout`, `GET /api/account/me`.
- Contas armazenadas em SQLite, senha com PBKDF2 e sal aleatório; cookie HttpOnly de sete dias.
- A conta do cliente não dá acesso ao painel administrativo. Favoritos permanecem no navegador, sem sincronização por conta nesta versão.
- Para produção: configurar HTTPS e `VELOUR_SECURE_COOKIES=1`; adicionar recuperação de senha, verificação de e-mail, limitação de tentativas e política final de privacidade.
- Botões têm exatamente duas variantes em `components/buttons.css`, altura mínima 44px e raio 8px.
