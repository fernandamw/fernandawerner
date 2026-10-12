# fernandawerner.adv.br

Site estático publicado pelo GitHub Pages a partir da branch `main` (domínio em `CNAME`).

## Como editar

- Os `.html` da raiz e das pastas (`crimes-federais/`, `sobre/`, `artigos/...`) são GERADOS. Não edite direto.
- Edite os textos em `_build/` e rode `python3 _build/build.py`:
  - `_build/paginas/*.html`: páginas fixas
  - `_build/artigos/*.html`: um arquivo por artigo (o bloco `<!--meta {...} -->` traz título, descrição, resumo e base legal)
  - `_build/faq.json`: perguntas frequentes (gera a página e os dados estruturados)
  - `_build/situacoes.json`: painel "O que aconteceu?" da página inicial
  - `_build/fases.json`: fases do processo na página de crimes federais
- Visual em `assets/site.css` (identidade Obsidian & Wine) e comportamento em `assets/site.js`.
- Tipografia: Archivo condensada (títulos em maiúsculas e interface), Lora itálica em wine para a palavra de destaque e para citações de lei, IBM Plex Mono para referências legais. Sem cantos arredondados.
- Posicionamento: identidade única em crimes federais; defesa criminal de médicos é área interna (fora do título e do primeiro bloco da página inicial).
- `python3 _build/build.py --previa PASTA` gera cópia navegável com links relativos, para revisão antes de publicar.
- O build também gera `sitemap.xml`, `robots.txt` e `llms.txt`.

## Regras de conteúdo

- Nome profissional: sempre "Fernanda Werner". OAB/SC 69.022.
- Publicidade da advocacia (Provimento 205/2021 do CFOAB e CED, arts. 39 a 47): texto informativo e sóbrio; sem promessa de resultado, sem casos concretos, sem valores de honorários, sem expressões persuasivas ou de autoengrandecimento, sem chamadas de urgência.
- Toda citação legal ou de súmula deve ser conferida na fonte oficial antes de entrar. Não citar jurisprudência não verificada.
- Sem emojis. Evitar "precisão/precisamente", "repousa", "crucial", "vale ressaltar". *Habeas Corpus* em itálico e com iniciais maiúsculas. Cargos com iniciais maiúsculas. Sempre "Advogada Criminalista" e "Tribunais Superiores" com iniciais maiúsculas.
- Artigos: título em forma de pergunta, resposta direta no bloco "Resposta em resumo", base legal listada ao final.
- Nunca publicar endereço residencial.
