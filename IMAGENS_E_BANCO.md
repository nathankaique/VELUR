# VÉLOUR - Imagens e Supabase

## Fotos
Atualizadas referências ilustrativas de modelos Porsche 911 Carrera S, Lamborghini Huracán EVO, Porsche 911 Turbo S e Lamborghini Urus S. A fotografia ilustra o modelo, não garante cor, ano exato ou identidade do automóvel à venda. Os demais endereços de foto cadastrados foram mantidos.

Imagens disponíveis dependem de sites externos. Caso o endereço de imagem pare de funcionar, o site mostra “IMAGEM INDISPONÍVEL” sem anunciar que o veículo foi vendido. Veículos cadastrados *sem URL de imagem* mantêm o comportamento original de “VENDIDO”, como solicitado.

Fontes das novas imagens: Wikimedia Commons. Consulte a página de cada arquivo e siga condições de atribuição das licenças. Antes de uso comercial, substitua todas as fotos de demonstração pelas fotos reais autorizadas de cada veículo.

## Banco online
O backend `server.py` suporta PostgreSQL do Supabase pela variável privada `SUPABASE_DATABASE_URL`, sem colocar senhas no JavaScript. Instale `pip install -r requirements.txt`, configure `SUPABASE_DATABASE_URL` no ambiente do servidor e execute `python server.py`. O esquema `supabase/schema.sql` e 20 veículos iniciais são carregados automaticamente **somente quando a tabela estiver vazia**. Se não configurar a conexão, a aplicação usa SQLite local.

Verifique em `/api/health` se o campo `database` é `supabase-postgresql`; `/api/vehicles` deve mostrar o catálogo carregado do banco. O Supabase online atualmente pode estar sem carros até o primeiro início do backend conectado. O site HTML sozinho não efetua conexão com PostgreSQL. Configure HTTPS, cookies seguros e outras proteções antes de produção.

Em atualizações futuras de fotos já cadastradas no Supabase, edite a coluna `image` por registro na tabela `public.vehicles`. Editar somente `seed_vehicles.json` não sobrescreve dados existentes, para proteger edições no banco.
