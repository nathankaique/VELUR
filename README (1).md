# Biblioteca de componentes VÉLOUR 2.1

Arquivos independentes e na ordem indicada em cada HTML:

1. `tokens.css`: cores, fontes, espaçamento, raios e tamanhos.
2. `buttons.css`: **Componente 01** `vl-btn vl-btn--primary` (ação principal) e **Componente 02** `vl-btn vl-btn--secondary` (ação secundária). São as **únicas duas variantes de botões de ação**. Compatibilidade com `.btn-primary`, `.btn-outline-light`, `.btn-attendance` e `.car-open` do legado.
3. `fields.css`: campos, selects, chips e cards com medidas consistentes.
4. `layout.css`: grid, imagem da filosofia, contatos com hover sem corte e rodapé.
5. `index.html`: catálogo visual da biblioteca, acessível em `/components/` com o servidor rodando.

Recomendação: novas páginas devem usar tokens e classes `vl-*`; mantenha altura de controles em 44px e espaçamento conforme escala 4/8/12/16/24/32/48/64. Menu de administração e abas possuem tratamento contextual, não novas categorias de CTA. Não edite cópias de estilos de botões em folhas antigas: a biblioteca é carregada **por último** para prevalecer sobre CSS preexistente.
