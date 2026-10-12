(function () {
  var root = document.documentElement;
  var nav = document.getElementById('nav');
  var btn = document.getElementById('menu-btn');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Navegação: fundo ao rolar; some ao descer e volta ao subir */
  var lastY = window.scrollY;
  var bar = document.querySelector('.progress i');
  var article = document.querySelector('.article .col');
  function onScroll() {
    var y = window.scrollY;
    if (nav) {
      nav.classList.toggle('scrolled', y > 40);
      var down = y > lastY && y > 320;
      if (Math.abs(y - lastY) > 6) nav.classList.toggle('away', down && !root.classList.contains('menu-open'));
    }
    if (bar && article) {
      var top = article.getBoundingClientRect().top + y - 120;
      var total = article.offsetHeight - window.innerHeight * 0.6;
      var p = Math.max(0, Math.min(1, (y - top) / Math.max(1, total)));
      bar.style.transform = 'scaleX(' + p + ')';
    }
    lastY = y;
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* Menu do celular */
  function closeMenu() {
    root.classList.remove('menu-open');
    if (btn) { btn.setAttribute('aria-expanded', 'false'); btn.setAttribute('aria-label', 'Abrir menu'); }
  }
  if (btn) {
    btn.addEventListener('click', function () {
      var open = root.classList.toggle('menu-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    });
    document.querySelectorAll('#menu-panel a').forEach(function (a) { a.addEventListener('click', closeMenu); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });
  }

  /* Abas: situações e fases do processo */
  document.querySelectorAll('[data-tabs]').forEach(function (box) {
    var tabs = [].slice.call(box.querySelectorAll('[role="tab"]'));
    var panels = [].slice.call(box.querySelectorAll('[role="tabpanel"]'));
    function select(i, focus) {
      tabs.forEach(function (t, k) {
        var on = k === i;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        panels[k].hidden = !on;
      });
      if (focus) tabs[i].focus();
      if (tabs[i].scrollIntoView && focus !== null) {
        try { tabs[i].scrollIntoView({ block: 'nearest', inline: 'center', behavior: reduce ? 'auto' : 'smooth' }); } catch (e) {}
      }
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(i, false); });
      t.addEventListener('keydown', function (e) {
        var k = e.key, n = tabs.length;
        if (k === 'ArrowRight' || k === 'ArrowDown') { e.preventDefault(); select((i + 1) % n, true); }
        else if (k === 'ArrowLeft' || k === 'ArrowUp') { e.preventDefault(); select((i - 1 + n) % n, true); }
        else if (k === 'Home') { e.preventDefault(); select(0, true); }
        else if (k === 'End') { e.preventDefault(); select(n - 1, true); }
      });
    });
    var start = 0;
    if (location.hash) {
      panels.forEach(function (p, k) { if ('#' + p.id === location.hash || '#' + (p.dataset.key || '') === location.hash) start = k; });
    }
    select(start, null);
  });

  /* Luz que acompanha o cursor nos cartões */
  if (window.matchMedia && window.matchMedia('(hover: hover)').matches) {
    document.querySelectorAll('.post').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        el.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
  }

  /* Entrada ao rolar: só o que está abaixo da dobra */
  var reveals = [].slice.call(document.querySelectorAll('.reveal'));
  if ('IntersectionObserver' in window && !reduce) {
    var vh = window.innerHeight;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.remove('pre'); io.unobserve(en.target); }
      });
    }, { threshold: 0.06, rootMargin: '0px 0px -4% 0px' });
    reveals.forEach(function (el) {
      if (el.getBoundingClientRect().top > vh * 0.92) { el.classList.add('pre'); io.observe(el); }
    });
  }

  /* Sumário do artigo: destaca a seção em leitura */
  var tocLinks = [].slice.call(document.querySelectorAll('.toc a'));
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var heads = [].slice.call(document.querySelectorAll('.prose h2[id]'));
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove('on'); });
          if (map[en.target.id]) map[en.target.id].classList.add('on');
        }
      });
    }, { rootMargin: '-18% 0px -70% 0px' });
    heads.forEach(function (h) { spy.observe(h); });
    var toc = document.querySelector('details.toc');
    var wide = window.matchMedia('(min-width: 1001px)');
    function syncToc() { if (toc) toc.open = wide.matches; }
    syncToc();
    if (wide.addEventListener) wide.addEventListener('change', syncToc);
    tocLinks.forEach(function (a) { a.addEventListener('click', function () { if (toc && !wide.matches) toc.open = false; }); });
  }

  /* Perguntas: busca e filtro por assunto */
  var search = document.getElementById('faq-busca');
  if (search) {
    var groups = [].slice.call(document.querySelectorAll('.faq-group'));
    var chips = [].slice.call(document.querySelectorAll('.chip'));
    var empty = document.getElementById('faq-vazio');
    var current = 'todas';
    function norm(s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
    function apply() {
      var q = norm(search.value.trim());
      var shown = 0;
      groups.forEach(function (g) {
        var okGroup = current === 'todas' || g.dataset.grupo === current;
        var any = 0;
        [].slice.call(g.querySelectorAll('details')).forEach(function (d) {
          var ok = okGroup && (!q || norm(d.textContent).indexOf(q) !== -1);
          d.hidden = !ok;
          if (ok) any++;
        });
        g.hidden = !any;
        shown += any;
      });
      if (empty) empty.hidden = shown > 0;
    }
    search.addEventListener('input', apply);
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        current = c.dataset.grupo;
        chips.forEach(function (o) { o.setAttribute('aria-pressed', o === c ? 'true' : 'false'); });
        apply();
      });
    });
  }
})();
