#!/usr/bin/env python3
"""Gera o site fernandawerner.adv.br a partir dos textos em _build/.

Uso:
    python3 _build/build.py                 # gera o site na raiz do repositório
    python3 _build/build.py --previa PASTA  # gera cópia navegável fora do domínio (links relativos)

Onde editar:
    _build/paginas/*.html   páginas fixas (início, áreas, sobre, perguntas, artigos, 404)
    _build/artigos/*.html   um arquivo por artigo
    _build/faq.json         perguntas frequentes (alimenta a página e os dados estruturados)
    _build/situacoes.json   painel "O que aconteceu?" da página inicial
    _build/fases.json       fases do processo na página de crimes federais

Nunca edite os .html da raiz diretamente: eles são sobrescritos a cada geração.
"""
import argparse
import html
import json
import re
import shutil
import unicodedata
from pathlib import Path

BUILD = Path(__file__).resolve().parent
REPO = BUILD.parent

SITE = "https://fernandawerner.adv.br"
NOME = "Fernanda Werner"
ESCRITORIO = "Fernanda Werner — Advocacia Criminal Federal"
OAB = "OAB/SC 69.022"
FONE_EXIBE = "(47) 3170-2300"
FONE_E164 = "+554731702300"
WA = "https://wa.me/554731702300"
EMAIL = "advfernanda@icloud.com"
INSTAGRAM = "https://www.instagram.com/fernandawerner.adv/"
CIDADE = "Balneário Camboriú/SC"

NAV = [
    ("crimes-federais/", "Crimes federais"),
    ("defesa-criminal-de-medicos/", "Defesa de médicos"),
    ("sobre/", "Sobre"),
    ("perguntas-frequentes/", "Perguntas"),
    ("artigos/", "Artigos"),
]

CATEGORIAS = {
    "crimes-federais": "Crimes federais",
    "defesa-criminal-de-medicos": "Defesa criminal de médicos",
}

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]

WA_SVG = ('<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>')
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'


# ---------------------------------------------------------------- leitura

def ler(path):
    """Devolve (meta, corpo) de um arquivo que começa com <!--meta {json} -->."""
    texto = path.read_text(encoding="utf-8")
    m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->\s*", texto, re.S)
    if not m:
        raise SystemExit(f"{path}: falta o bloco <!--meta {{...}} --> no início")
    return json.loads(m.group(1)), texto[m.end():]


def data_extenso(iso):
    a, m, d = iso.split("-")
    return f"{int(d)} de {MESES[int(m) - 1]} de {a}"


def sem_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


# ---------------------------------------------------------------- dados estruturados

def pessoa():
    return {
        "@type": "Person",
        "@id": f"{SITE}/#fernanda-werner",
        "name": NOME,
        "jobTitle": "Advogada Criminalista",
        "description": ("Advogada Criminalista inscrita na OAB/SC sob o nº 69.022, com escritório em "
                        "Balneário Camboriú/SC. Atua na defesa em crimes de competência federal."),
        "url": f"{SITE}/sobre/",
        "image": f"{SITE}/assets/fernanda-werner.jpg",
        "email": EMAIL,
        "telephone": FONE_E164,
        "address": {"@type": "PostalAddress", "addressLocality": "Balneário Camboriú",
                    "addressRegion": "SC", "addressCountry": "BR"},
        "identifier": {"@type": "PropertyValue", "propertyID": "OAB/SC", "value": "69022"},
        "hasCredential": [
            {"@type": "EducationalOccupationalCredential", "credentialCategory": "Inscrição profissional",
             "name": "Ordem dos Advogados do Brasil, Seccional de Santa Catarina, nº 69.022"},
            {"@type": "EducationalOccupationalCredential", "credentialCategory": "Pós-graduação",
             "name": "Pós-graduação em Ciências Criminais"},
        ],
        "knowsLanguage": "pt-BR",
        "knowsAbout": [
            "Direito Penal", "Direito Processual Penal", "Crimes federais",
            "Crimes contra o sistema financeiro nacional", "Lavagem de dinheiro",
            "Crimes contra a ordem tributária", "Operações da Polícia Federal",
            "Habeas Corpus", "Recursos ao STJ e ao STF", "Execução penal",
            "Defesa criminal de médicos", "Responsabilidade penal médica",
            "Processo ético-profissional médico",
        ],
        "worksFor": {"@id": f"{SITE}/#escritorio"},
        "sameAs": [INSTAGRAM],
    }


def escritorio():
    return {
        "@type": ["LegalService", "Attorney"],
        "@id": f"{SITE}/#escritorio",
        "name": ESCRITORIO,
        "url": f"{SITE}/",
        "image": f"{SITE}/assets/fernanda-werner.jpg",
        "logo": f"{SITE}/favicon-512.png",
        "description": ("Escritório de advocacia criminal em Balneário Camboriú/SC. Defesa em crimes de "
                        "competência federal, na Justiça Federal e nos Tribunais Superiores."),
        "telephone": FONE_E164,
        "email": EMAIL,
        "address": {"@type": "PostalAddress", "addressLocality": "Balneário Camboriú",
                    "addressRegion": "SC", "addressCountry": "BR"},
        "areaServed": [{"@type": "Country", "name": "Brasil"},
                       {"@type": "State", "name": "Santa Catarina"},
                       {"@type": "City", "name": "Balneário Camboriú"}],
        "founder": {"@id": f"{SITE}/#fernanda-werner"},
        "employee": {"@id": f"{SITE}/#fernanda-werner"},
        "knowsAbout": ["Advocacia criminal", "Crimes federais", "Operações da Polícia Federal", "Defesa criminal de médicos"],
        "sameAs": [INSTAGRAM],
        "contactPoint": {"@type": "ContactPoint", "contactType": "Atendimento", "telephone": FONE_E164,
                         "email": EMAIL, "availableLanguage": "Portuguese", "areaServed": "BR"},
    }


def website():
    return {"@type": "WebSite", "@id": f"{SITE}/#site", "url": f"{SITE}/", "name": ESCRITORIO,
            "inLanguage": "pt-BR", "publisher": {"@id": f"{SITE}/#escritorio"}}


def migalhas(trilha):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": nome, "item": f"{SITE}/{caminho}"}
        for i, (caminho, nome) in enumerate(trilha)]}


def jsonld(nos):
    dados = {"@context": "https://schema.org", "@graph": nos}
    return ('<script type="application/ld+json">'
            + json.dumps(dados, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
            + "</script>")


# ---------------------------------------------------------------- blocos reutilizados

X = '<span class="x" aria-hidden="true"></span>'


def slug(s):
    s = unicodedata.normalize("NFD", sem_tags(s).lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def cartao_artigo(a):
    return (f'<a class="post reveal" href="{{{{root}}}}artigos/{a["slug"]}/">'
            f'<span class="cat">{CATEGORIAS[a["categoria"]]}</span>'
            f'<h3>{a["titulo"]}</h3><p>{a["chamada"]}</p>'
            f'<span class="more">Ler o artigo</span></a>')


def bloco_faq(itens):
    out = ['<div class="faq">']
    for it in itens:
        out.append(f'<details><summary><span>{it["q"]}</span>{X}</summary>'
                   f'<div class="answer">{it["a"]}</div></details>')
    out.append("</div>")
    return "\n".join(out)


def bloco_abas(itens, prefixo, rotulo, em_linha=False):
    """Abas acessíveis. Sem JavaScript, todos os painéis ficam visíveis em sequência."""
    cls = "tabs tabs--line" if em_linha else "tabs"
    botoes, paineis = [], []
    for i, it in enumerate(itens):
        tid, pid = f"{prefixo}-aba-{it['key']}", f"{prefixo}-{it['key']}"
        num = f'<span class="n">{i + 1:02d}</span>' if em_linha else ""
        botoes.append(f'<button class="tab" role="tab" id="{tid}" aria-controls="{pid}" '
                      f'aria-selected="{"true" if i == 0 else "false"}"><span>{num}{it["aba"]}</span></button>')
        colunas = ""
        if it.get("colunas"):
            partes = []
            for col in it["colunas"]:
                tag = "ol" if col.get("ordenada") else "ul"
                lis = "".join(f"<li>{x}</li>" for x in col["itens"])
                partes.append(f'<div><h4>{col["titulo"]}</h4><{tag}>{lis}</{tag}></div>')
            colunas = f'<div class="cols">{"".join(partes)}</div>'
        link = ""
        if it.get("link"):
            link = f'<a class="more" href="{{{{root}}}}{it["link"]["href"]}">{it["link"]["rotulo"]}</a>'
        paineis.append(
            f'<section class="panel" role="tabpanel" id="{pid}" aria-labelledby="{tid}" tabindex="0">'
            f'<h3>{it["titulo"]}</h3><p>{it["texto"]}</p>{colunas}'
            f'<div class="foot"><span class="ref">{it["ref"]}</span>{link}</div></section>')
    return (f'<div class="{cls}" data-tabs><div class="tablist" role="tablist" aria-label="{rotulo}">'
            f'{"".join(botoes)}</div><div class="panels">{"".join(paineis)}</div></div>')


def bloco_contato(alt=False):
    cls = "section cta section--alt" if alt else "section cta"
    return f'''
<section class="{cls}" id="contato">
  <div class="wrap grid">
    <div class="reveal">
      <span class="eyebrow">Contato</span>
      <h2>Fale com o escritório</h2>
      <p>Atendimento presencial em {CIDADE} e por videoconferência em todo o país. As informações recebidas são tratadas sob sigilo profissional, mesmo que não haja contratação.</p>
      <a class="btn" href="{WA}" target="_blank" rel="noopener">WhatsApp {ARROW}</a>
    </div>
    <div class="reveal">
      <dl>
        <div><dt>WhatsApp</dt><dd><a href="{WA}" target="_blank" rel="noopener">{FONE_EXIBE}</a></dd></div>
        <div><dt>E-mail</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
        <div><dt>Instagram</dt><dd><a href="{INSTAGRAM}" target="_blank" rel="noopener">@fernandawerner.adv</a></dd></div>
        <div><dt>Escritório</dt><dd>{CIDADE}</dd></div>
      </dl>
      <p class="privacy">Comunicações relativas ao exercício da advocacia são invioláveis (Lei 8.906/1994, art. 7º, II) e protegidas pelo dever de sigilo profissional (Código de Ética e Disciplina da OAB, arts. 35 a 38).</p>
    </div>
  </div>
</section>'''


# ---------------------------------------------------------------- moldura da página

FONTES = ("https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..700"
          "&family=IBM+Plex+Mono:wght@400;500&family=Lora:ital,wght@0,400..700;1,400..700&display=swap")


def moldura(meta, corpo, nos_schema, previa):
    caminho = meta["path"]
    canonical = f"{SITE}/{caminho}" if caminho != "404.html" else f"{SITE}/"
    titulo = meta["title"]
    desc = meta["description"]
    ativo = meta.get("nav", "")
    og_type = meta.get("og_type", "website")
    solid = "" if meta.get("hero") else " solid"

    def atual(p):
        return ' aria-current="page"' if p.strip("/") == ativo else ""

    links = "".join(f'<li><a href="{{{{root}}}}{p}"{atual(p)}>{n}</a></li>' for p, n in NAV)
    painel = "".join(f'<a class="item" href="{{{{root}}}}{p}"{atual(p)}>{n}</a>' for p, n in [("", "Início")] + NAV)
    rodape = "".join(f'<li><a href="{{{{root}}}}{p}">{n}</a></li>' for p, n in [("", "Início")] + NAV)

    robots = '<meta name="robots" content="noindex">' if meta.get("noindex") or previa else \
        '<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">'
    aviso = '<div class="preview-flag">Prévia · não publicada</div>' if previa else ""
    progresso = '<div class="progress" aria-hidden="true"><i></i></div>' if meta.get("progresso") else ""

    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{html.escape(titulo)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="author" content="{NOME}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="{ESCRITORIO}">
<meta property="og:title" content="{html.escape(meta.get("og_title", titulo))}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0D0D0F">
<link rel="icon" type="image/x-icon" href="{{{{root}}}}favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="{{{{root}}}}favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="{{{{root}}}}favicon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="{{{{root}}}}apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTES}" rel="stylesheet">
<link rel="stylesheet" href="{{{{root}}}}assets/site.css">
<script>document.documentElement.classList.add('js')</script>
{jsonld(nos_schema)}
</head>
<body>
<a class="skip" href="#conteudo">Ir para o conteúdo</a>
{progresso}
<header class="nav{solid}" id="nav">
  <a href="{{{{root}}}}" class="brand" aria-label="Fernanda Werner, início">Fernanda <em>Werner</em></a>
  <nav aria-label="Principal"><ul class="nav-links">{links}</ul></nav>
  <a href="{WA}" target="_blank" rel="noopener" class="btn nav-cta">Contato</a>
  <button class="menu-btn" id="menu-btn" aria-label="Abrir menu" aria-expanded="false" aria-controls="menu-panel"><span></span><span></span><span></span></button>
</header>
<div class="menu-panel" id="menu-panel">
  {painel}
  <a class="btn" href="{WA}" target="_blank" rel="noopener">WhatsApp {ARROW}</a>
  <span class="ref">{OAB} · {CIDADE}</span>
</div>

<main id="conteudo">
{corpo}
</main>

<footer class="footer">
  <div class="wrap">
    <div class="top">
      <div><span class="brand">Fernanda <em>Werner</em></span><span class="ref">Advocacia Criminal Federal · {OAB} · {CIDADE}</span></div>
      <ul class="footer-nav">{rodape}</ul>
    </div>
    <div class="legal">
      <p>O conteúdo deste site tem caráter informativo e não substitui a análise individual de cada caso por advogado.</p>
      <p>© 2026 Fernanda Werner. {OAB}.</p>
    </div>
  </div>
</footer>

<div class="wa"><a href="{WA}" target="_blank" rel="noopener" aria-label="Contato pelo WhatsApp">{WA_SVG}</a></div>
{aviso}
<script src="{{{{root}}}}assets/site.js" defer></script>
</body>
</html>
'''


def resolver_links(pagina, caminho, previa):
    """Troca {{root}} pelo prefixo certo. Na prévia, usa links relativos com index.html."""
    if not previa:
        return pagina.replace("{{root}}", "/")
    prefixo = "../" * caminho.count("/")
    pagina = pagina.replace("{{root}}", prefixo)

    def fix(m):
        url = m.group(2)
        if re.match(r"^(https?:|mailto:|#|tel:)", url):
            return m.group(0)
        base, _, ancora = url.partition("#")
        if base == "" or base.endswith("/"):
            return f'{m.group(1)}{base}index.html{"#" + ancora if ancora else ""}"'
        return m.group(0)
    return re.sub(r'(href=")([^"]*)"', fix, pagina)


def sumario(corpo):
    """Dá id a cada <h2> do artigo e devolve (corpo, itens do sumário)."""
    itens, usados = [], set()

    def troca(m):
        texto = m.group(1)
        s = slug(texto)
        while s in usados:
            s += "-2"
        usados.add(s)
        itens.append((s, sem_tags(texto)))
        return f'<h2 id="{s}">{texto}</h2>'
    return re.sub(r"<h2>(.*?)</h2>", troca, corpo, flags=re.S), itens


# ---------------------------------------------------------------- geração

def gerar(saida, previa):
    artigos = []
    for f in sorted((BUILD / "artigos").glob("*.html")):
        meta, corpo = ler(f)
        meta["corpo"] = corpo
        artigos.append(meta)
    artigos.sort(key=lambda a: (a["data"], -a.get("ordem", 0)), reverse=True)
    faq = json.loads((BUILD / "faq.json").read_text(encoding="utf-8"))
    todas = [it for g in faq for it in g["itens"]]
    situacoes = json.loads((BUILD / "situacoes.json").read_text(encoding="utf-8"))
    fases = json.loads((BUILD / "fases.json").read_text(encoding="utf-8"))

    def faq_completo():
        chips = ['<button class="chip" type="button" data-grupo="todas" aria-pressed="true">Todas</button>']
        grupos = []
        for g in faq:
            gid = slug(g["grupo"])
            chips.append(f'<button class="chip" type="button" data-grupo="{gid}" aria-pressed="false">{g["grupo"]}</button>')
            grupos.append(f'<div class="faq-group" data-grupo="{gid}"><h2>{g["grupo"]}</h2>{bloco_faq(g["itens"])}</div>')
        lupa = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
                '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>')
        return (f'<div class="faq-tools"><div class="faq-search">{lupa}'
                f'<input type="search" id="faq-busca" placeholder="Buscar nas perguntas (ex.: silêncio, busca, CRM)" '
                f'aria-label="Buscar nas perguntas" autocomplete="off"></div>'
                f'<div class="chips" role="group" aria-label="Filtrar por assunto">{"".join(chips)}</div></div>'
                + "\n".join(grupos)
                + '<p class="faq-empty" id="faq-vazio" hidden>Nenhuma pergunta encontrada. Tente outra palavra.</p>')

    def substituir(corpo):
        corpo = corpo.replace("{{wa}}", WA).replace("{{arrow}}", ARROW).replace("{{x}}", X)
        corpo = corpo.replace("{{contato_alt}}", bloco_contato(True))
        corpo = corpo.replace("{{contato}}", bloco_contato())
        corpo = corpo.replace("{{situacoes}}", bloco_abas(situacoes, "situacao", "Situações"))
        corpo = corpo.replace("{{fases}}", bloco_abas(fases, "fase", "Fases do processo", em_linha=True))
        corpo = corpo.replace("{{artigos_recentes}}", "\n".join(cartao_artigo(a) for a in artigos[:3]))
        corpo = corpo.replace("{{artigos_todos}}", "\n".join(cartao_artigo(a) for a in artigos))
        for cat in CATEGORIAS:
            corpo = corpo.replace("{{artigos:%s}}" % cat,
                                  "\n".join(cartao_artigo(a) for a in artigos if a["categoria"] == cat))
        corpo = corpo.replace("{{faq_destaque}}", bloco_faq([it for it in todas if it.get("destaque")]))
        corpo = corpo.replace("{{faq_completo}}", faq_completo())
        return corpo

    paginas = []  # (caminho, html)
    urls = []     # (caminho, lastmod)

    # páginas fixas
    for f in sorted((BUILD / "paginas").glob("*.html")):
        meta, corpo = ler(f)
        caminho = meta["path"]
        nos = [website(), escritorio(), pessoa()]
        pagina_no = {"@type": meta.get("schema_type", "WebPage"), "@id": f"{SITE}/{caminho}#pagina",
                     "url": f"{SITE}/{caminho}", "name": meta["title"], "description": meta["description"],
                     "inLanguage": "pt-BR", "isPartOf": {"@id": f"{SITE}/#site"},
                     "about": {"@id": f"{SITE}/#escritorio"}}
        if meta.get("schema_type") == "ProfilePage":
            pagina_no["mainEntity"] = {"@id": f"{SITE}/#fernanda-werner"}
        if meta.get("schema_type") == "FAQPage":
            pagina_no["mainEntity"] = [
                {"@type": "Question", "name": sem_tags(it["q"]),
                 "acceptedAnswer": {"@type": "Answer", "text": sem_tags(it["a"])}} for it in todas]
        if caminho == "artigos/":
            pagina_no["@type"] = "CollectionPage"
            pagina_no["hasPart"] = [{"@type": "Article", "headline": a["titulo"],
                                     "url": f"{SITE}/artigos/{a['slug']}/"} for a in artigos]
        nos.append(pagina_no)
        if caminho not in ("", "404.html"):
            nos.append(migalhas([("", "Início"), (caminho, meta.get("crumb", meta["title"]))]))
        paginas.append((caminho, moldura(meta, substituir(corpo), nos, previa)))
        if caminho != "404.html":
            urls.append((caminho, meta.get("atualizado", "2026-10-12")))

    # artigos
    for a in artigos:
        caminho = f"artigos/{a['slug']}/"
        cat_nome = CATEGORIAS[a["categoria"]]
        base = "".join(f"<li>{b}</li>" for b in a.get("base_legal", []))
        outros = [o for o in artigos if o["slug"] != a["slug"]]
        outros.sort(key=lambda o: o["categoria"] != a["categoria"])
        texto, itens = sumario(a["corpo"])
        minutos = max(2, round(len(sem_tags(a["resumo"] + texto).split()) / 200))
        toc = "".join(f'<li><a href="#{s}">{t}</a></li>' for s, t in itens)
        corpo = f'''
<section class="page-hero page-hero--article">
  <div class="wrap">
    <ol class="crumbs"><li><a href="{{{{root}}}}">Início</a></li><li><a href="{{{{root}}}}artigos/">Artigos</a></li><li><a href="{{{{root}}}}{a["categoria"]}/">{cat_nome}</a></li></ol>
    <h1>{a["titulo"]}</h1>
    <p class="byline"><span>Por <a href="{{{{root}}}}sobre/">Fernanda Werner</a>, Advogada Criminalista, {OAB}</span><span><time datetime="{a["data"]}">{data_extenso(a["data"])}</time></span><span>Leitura de {minutos} min</span></p>
  </div>
</section>
<div class="wrap article">
  <details class="toc" open>
    <summary>Neste artigo</summary>
    <ol>{toc}</ol>
  </details>
  <article class="col">
    <div class="answer-box">
      <span class="eyebrow">Resposta em resumo</span>
      {a["resumo"]}
    </div>
    <div class="prose">
{texto}
    </div>
    <div class="legal-base">
      <h2>Base legal citada</h2>
      <ul>{base}</ul>
    </div>
    <div class="author">
      <img src="{{{{root}}}}assets/fernanda-werner-retrato.jpg" alt="Fernanda Werner" width="80" height="80" loading="lazy">
      <div>
        <div class="name">Fernanda Werner</div>
        <p>Advogada Criminalista, {OAB}, com escritório em {CIDADE}. Atua em crimes de competência federal. <a href="{{{{root}}}}sobre/">Perfil completo</a></p>
      </div>
    </div>
    <p class="disclaimer">Texto informativo, baseado na legislação vigente na data de publicação. Não substitui a análise do caso concreto por advogado.</p>
  </article>
</div>
<section class="section section--alt">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Continue lendo</span><h2>Outros artigos</h2></div>
    <div class="posts">{"".join(cartao_artigo(o) for o in outros[:3])}</div>
  </div>
</section>
{bloco_contato()}'''
        meta = {"path": caminho, "title": f'{a["titulo"]} | {NOME}', "og_title": a["titulo"],
                "description": a["descricao"], "nav": "artigos", "og_type": "article", "progresso": True}
        nos = [website(), escritorio(), pessoa(), {
            "@type": "Article", "@id": f"{SITE}/{caminho}#artigo", "headline": a["titulo"],
            "description": a["descricao"], "abstract": sem_tags(a["resumo"]),
            "url": f"{SITE}/{caminho}", "mainEntityOfPage": f"{SITE}/{caminho}",
            "datePublished": a["data"], "dateModified": a.get("atualizado", a["data"]),
            "inLanguage": "pt-BR", "articleSection": cat_nome,
            "image": f"{SITE}/assets/og.jpg",
            "author": {"@id": f"{SITE}/#fernanda-werner"},
            "publisher": {"@id": f"{SITE}/#escritorio"},
            "isPartOf": {"@id": f"{SITE}/#site"},
        }, migalhas([("", "Início"), ("artigos/", "Artigos"), (caminho, a["titulo"])])]
        paginas.append((caminho, moldura(meta, substituir(corpo), nos, previa)))
        urls.append((caminho, a.get("atualizado", a["data"])))

    # grava
    for caminho, pagina in paginas:
        destino = saida / (caminho + "index.html" if caminho == "" or caminho.endswith("/") else caminho)
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(resolver_links(pagina, caminho, previa), encoding="utf-8")

    # sitemap, robots, llms.txt
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for caminho, lastmod in urls:
        sm.append(f"  <url><loc>{SITE}/{caminho}</loc><lastmod>{lastmod}</lastmod></url>")
    sm.append("</urlset>")
    (saida / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")

    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
            "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "CCBot",
            "meta-externalagent", "Amazonbot", "Bingbot", "Googlebot"]
    rb = ["# fernandawerner.adv.br — leitura liberada para buscadores e assistentes de IA", ""]
    for b in bots:
        rb += [f"User-agent: {b}", "Allow: /", ""]
    rb += ["User-agent: *", "Allow: /", "", f"Sitemap: {SITE}/sitemap.xml", ""]
    (saida / "robots.txt").write_text("\n".join(rb), encoding="utf-8")

    ll = [f"# {ESCRITORIO}", "",
          "> Fernanda Werner é Advogada Criminalista, inscrita na OAB/SC sob o nº 69.022, com escritório em "
          "Balneário Camboriú/SC. Atua na defesa em crimes de competência federal: investigações da Polícia "
          "Federal, ações penais na Justiça Federal e recursos ao TRF-4, ao STJ e ao STF. Atendimento presencial "
          "em Balneário Camboriú e por videoconferência em todo o Brasil.",
          "",
          "## Dados profissionais", "",
          f"- Nome profissional: {NOME}",
          "- Profissão: Advogada Criminalista",
          "- Inscrição: OAB/SC 69.022",
          "- Formação: pós-graduação em Ciências Criminais",
          "- Área principal: crimes federais (sistema financeiro nacional, lavagem de dinheiro, crimes tributários, "
          "descaminho e contrabando, crimes contra a Previdência e a Administração Pública federal, tráfico transnacional)",
          "- Outras áreas: defesa criminal de médicos; recursos aos Tribunais Superiores; execução penal",
          f"- Localização: {CIDADE}, Brasil",
          f"- WhatsApp: {FONE_EXIBE}",
          f"- E-mail: {EMAIL}",
          f"- Site: {SITE}/",
          f"- Instagram: {INSTAGRAM}",
          "",
          "## Páginas principais", "",
          f"- [Crimes federais]({SITE}/crimes-federais/): matérias, fases do processo e onde os casos tramitam",
          f"- [Defesa criminal de médicos]({SITE}/defesa-criminal-de-medicos/): situações atendidas e relação entre as esferas criminal, ética e cível",
          f"- [Sobre]({SITE}/sobre/): perfil profissional de Fernanda Werner",
          f"- [Perguntas frequentes]({SITE}/perguntas-frequentes/): respostas diretas, com a base legal",
          "",
          "## Artigos", ""]
    for a in artigos:
        ll.append(f"- [{a['titulo']}]({SITE}/artigos/{a['slug']}/): {a['chamada']}")
    ll += ["", "## Observação", "",
           "O conteúdo do site é informativo e não substitui a análise individual de cada caso por advogado.", ""]
    (saida / "llms.txt").write_text("\n".join(ll), encoding="utf-8")

    if previa:
        shutil.copytree(REPO / "assets", saida / "assets", dirs_exist_ok=True)
        for f in ["favicon.ico", "favicon-32.png", "favicon-192.png", "favicon-512.png", "apple-touch-icon.png"]:
            shutil.copy(REPO / f, saida / f)
    return [c for c, _ in paginas]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--previa", metavar="PASTA", help="gera cópia navegável com links relativos nesta pasta")
    args = ap.parse_args()
    destino = Path(args.previa).resolve() if args.previa else REPO
    destino.mkdir(parents=True, exist_ok=True)
    feitas = gerar(destino, bool(args.previa))
    print(f"{len(feitas)} páginas geradas em {destino}")
    for c in feitas:
        print("  /" + c)
