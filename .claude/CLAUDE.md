# fernandawerner.adv.br

Site estático publicado pelo GitHub Pages a partir da branch `main` (domínio em `CNAME`). `SITE` em `_build/build.py` e o arquivo `CNAME` devem apontar para o domínio que estiver ativo.

## Como editar

- Os `.html` da raiz e das pastas (`crimes-federais/`, `sobre/`, `artigos/...`) são GERADOS. Não edite direto.
- Edite os textos em `_build/` e rode `python3 _build/build.py`:
  - `_build/paginas/*.html`: páginas fixas
  - `_build/artigos/*.html`: um arquivo por artigo (o bloco `<!--meta {...} -->` traz título, descrição, resumo e base legal)
  - `_build/faq.json`: perguntas frequentes (gera a página e os dados estruturados)
  - `_build/situacoes.json`: painel "O que aconteceu?" da página inicial
  - `_build/fases.json`: fases do processo na página de crimes federais
- Visual em `assets/site.css` (identidade Obsidian & Wine) e comportamento em `assets/site.js`.
- Tipografia e visual: os do site original (Cormorant Garamond + DM Sans, fundo obsidian, vinho, textura leve, entrada ao rolar). Fernanda gosta desse visual; não redesenhar.
- Camada de movimento (fim de `assets/site.css` e `assets/site.js`): abertura coreografada na página inicial (classe `intro` no html), profundidade na foto (`data-parallax`), contadores (`data-count`), títulos palavra a palavra, transição entre páginas (view transitions + reserva), botões magnéticos, luz nos cartões, barra de progresso. Tudo respeita `prefers-reduced-motion` e nada esconde texto do HTML (buscadores e IAs leem o mesmo conteúdo).
- Imagens: `.jpg` com `.webp` ao lado, via `<picture>`; pré-carregamento da foto da página inicial; `speculationrules` para pré-renderizar as páginas internas.
- Posicionamento: identidade única em crimes federais; defesa criminal de médicos é área interna (fora do título e do primeiro bloco da página inicial).
- `python3 _build/build.py --previa PASTA` gera cópia navegável com links relativos, para revisão antes de publicar.
- O build também gera `sitemap.xml`, `robots.txt` e `llms.txt`.

## Regras de conteúdo

- Nome profissional visível: sempre "Fernanda Werner" (voltou de "Fernanda Meira" em 09/11/2026). O Instagram segue @fernandameira.adv até ela renomear. O nome de cadastro na OAB, "Fernanda Meira Werner", só nos dados estruturados. OAB/SC 69.022.
- Publicidade da advocacia (Provimento 205/2021 do CFOAB e CED, arts. 39 a 47): texto informativo e sóbrio; sem promessa de resultado, sem casos concretos, sem valores de honorários, sem expressões persuasivas ou de autoengrandecimento, sem chamadas de urgência.
- Toda citação legal ou de súmula deve ser conferida na fonte oficial antes de entrar. Não citar jurisprudência não verificada.
- Sem emojis. Evitar "precisão/precisamente", "repousa", "crucial", "vale ressaltar". *Habeas Corpus* em itálico e com iniciais maiúsculas. Cargos com iniciais maiúsculas. Sempre "Advogada Criminalista" e "Tribunais Superiores" com iniciais maiúsculas.
- Artigos: título em forma de pergunta, resposta direta no bloco "Resposta em resumo", base legal listada ao final.
- Nunca publicar endereço residencial.
