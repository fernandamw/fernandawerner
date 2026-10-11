# fernandawerner.adv.br

Site estático publicado pelo GitHub Pages a partir da branch `main` (domínio em `CNAME`).

## Como editar

- Os `.html` da raiz e das pastas (`crimes-federais/`, `sobre/`, `artigos/...`) são GERADOS. Não edite direto.
- Edite os textos em `_build/` e rode `python3 _build/build.py`:
  - `_build/paginas/*.html`: páginas fixas
  - `_build/artigos/*.html`: um arquivo por artigo (o bloco `<!--meta {...} -->` traz título, descrição, resumo e base legal)
  - `_build/faq.json`: perguntas frequentes (gera a página e os dados estruturados)
- Visual em `assets/site.css` (identidade Obsidian & Wine) e comportamento em `assets/site.js`.
- `python3 _build/build.py --previa PASTA` gera cópia navegável com links relativos, para revisão antes de publicar.
- O build também gera `sitemap.xml`, `robots.txt` e `llms.txt`.

## Regras de conteúdo

- Nome profissional: sempre "Fernanda Werner". OAB/SC 69.022.
- Publicidade da advocacia (Provimento 205/2021 do CFOAB e CED, arts. 39 a 47): texto informativo e sóbrio; sem promessa de resultado, sem casos concretos, sem valores de honorários, sem expressões persuasivas ou de autoengrandecimento, sem chamadas de urgência.
- Toda citação legal ou de súmula deve ser conferida na fonte oficial antes de entrar. Não citar jurisprudência não verificada.
- Sem emojis. Evitar "precisão/precisamente", "repousa", "crucial", "vale ressaltar". *Habeas Corpus* em itálico e com iniciais maiúsculas. Cargos com iniciais maiúsculas.
- Artigos: título em forma de pergunta, resposta direta no bloco "Resposta em resumo", base legal listada ao final.
- Nunca publicar endereço residencial.
