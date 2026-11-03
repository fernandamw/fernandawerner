(function () {
  var root = document.documentElement;
  var nav = document.getElementById('nav');
  var btn = document.getElementById('menu-btn');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var raf = window.requestAnimationFrame || function (f) { setTimeout(f, 16); };

  /* ---------- Rolagem: barra, navegação, profundidade ---------- */
  var bar = document.createElement('div');
  bar.className = 'scroll-progress'; bar.setAttribute('aria-hidden', 'true'); bar.innerHTML = '<i></i>';
  document.body.appendChild(bar);
  var barI = bar.firstChild;
  var parallax = [].slice.call(document.querySelectorAll('[data-parallax]'));
  var wa = document.querySelector('.wa');
  var lastY = window.scrollY, ticking = false;

  function frame() {
    ticking = false;
    var y = window.scrollY;
    var max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    barI.style.setProperty('--p', Math.min(1, y / max));
    if (nav) {
      nav.classList.toggle('scrolled', y > 40);
      if (Math.abs(y - lastY) > 6) nav.classList.toggle('away', y > lastY && y > 320 && !root.classList.contains('menu-open'));
    }
    if (wa) wa.classList.toggle('hidden', y < 120 && document.body.classList.contains('intro'));
    if (!reduce) {
      parallax.forEach(function (img) {
        var r = img.getBoundingClientRect();
        if (r.bottom < 0 || r.top > window.innerHeight) return;
        var f = parseFloat(img.getAttribute('data-parallax')) || 0.1;
        var center = r.top + r.height / 2 - window.innerHeight / 2;
        img.style.setProperty('--py', (center * f).toFixed(1) + 'px');
      });
    }
    lastY = y;
  }
  function onScroll() { if (!ticking) { ticking = true; raf(frame); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  frame();

  /* ---------- Menu do celular ---------- */
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

  /* ---------- Entrada ao rolar: blocos, cartões, linhas, títulos palavra a palavra ---------- */
  var io = null;
  if ('IntersectionObserver' in window && !reduce) {
    var vh = window.innerHeight;
    io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        el.classList.remove('pre');
        el.classList.add('drawn');
        el.classList.add('words-in');
        io.unobserve(el);
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -6% 0px' });

    document.querySelectorAll('.reveal, .posts .post, .topics .topic').forEach(function (el, i) {
      if (el.getBoundingClientRect().top > vh * 0.9) {
        el.classList.add('pre');
        el.style.transitionDelay = ((i % 3) * 90) + 'ms';
        io.observe(el);
      }
    });
    document.querySelectorAll('.divider').forEach(function (el) {
      if (el.getBoundingClientRect().top > vh * 0.9) io.observe(el); else el.classList.add('drawn');
    });
    document.querySelectorAll('.section .head h2, .split h2, .cta h2').forEach(function (h) {
      if (h.getBoundingClientRect().top <= vh * 0.9) return;
      var html = h.innerHTML;
      if (/<(?!br|em|\/em)/i.test(html)) return;
      var i = 0;
      h.innerHTML = html.split(/(<br\s*\/?>)/i).map(function (part) {
        if (/^<br/i.test(part)) return part;
        return part.replace(/(<em>)?([^\s<]+)(<\/em>)?/g, function (m, o, w, c) {
          return '<span class="w" style="--i:' + (i++) + '"><i>' + (o || '') + w + (c || '') + '</i></span>';
        });
      }).join('');
      io.observe(h);
    });
  }

  /* ---------- Contadores ---------- */
  var counters = [].slice.call(document.querySelectorAll('[data-count]'));
  if (counters.length && 'IntersectionObserver' in window && !reduce) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, end = parseInt(el.getAttribute('data-count'), 10), fmt = el.getAttribute('data-format');
        var t0 = null, dur = 1400;
        cio.unobserve(el);
        function step(ts) {
          if (!t0) t0 = ts;
          var p = Math.min(1, (ts - t0) / dur); p = 1 - Math.pow(1 - p, 3);
          var v = Math.round(end * p);
          el.textContent = fmt === 'pt' ? v.toLocaleString('pt-BR') : String(v);
          if (p < 1) raf(step);
        }
        raf(step);
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { cio.observe(el); });
  }

  /* ---------- Interação fina: botões magnéticos, luz nos cartões ---------- */
  if (fine && !reduce) {
    document.querySelectorAll('.btn').forEach(function (b) {
      b.classList.add('magnet');
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect();
        var dx = (e.clientX - (r.left + r.width / 2)) / r.width, dy = (e.clientY - (r.top + r.height / 2)) / r.height;
        b.style.transform = 'translate(' + (dx * 6).toFixed(1) + 'px,' + (dy * 6 - 2).toFixed(1) + 'px)';
      });
      b.addEventListener('pointerleave', function () { b.style.transform = ''; });
    });
    document.querySelectorAll('.post, .topic').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        el.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
  }

  /* ---------- Abas: situações e fases ---------- */
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
      if (focus !== null && tabs[i].scrollIntoView) {
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
    if (location.hash) panels.forEach(function (p, k) { if ('#' + p.id === location.hash) start = k; });
    select(start, null);
  });

  /* ---------- Artigo: sumário que acompanha a leitura ---------- */
  var tocLinks = [].slice.call(document.querySelectorAll('.toc a'));
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove('on'); });
          if (map[en.target.id]) map[en.target.id].classList.add('on');
        }
      });
    }, { rootMargin: '-18% 0px -70% 0px' });
    document.querySelectorAll('.prose h2[id]').forEach(function (h) { spy.observe(h); });
    var toc = document.querySelector('details.toc');
    var wide = window.matchMedia('(min-width: 1001px)');
    function syncToc() { if (toc) toc.open = wide.matches; }
    syncToc();
    if (wide.addEventListener) wide.addEventListener('change', syncToc);
    tocLinks.forEach(function (a) { a.addEventListener('click', function () { if (toc && !wide.matches) toc.open = false; }); });
  }

  /* ---------- Perguntas: busca e filtro ---------- */
  var search = document.getElementById('faq-busca');
  if (search) {
    var groups = [].slice.call(document.querySelectorAll('.faq-group'));
    var chips = [].slice.call(document.querySelectorAll('.chip'));
    var empty = document.getElementById('faq-vazio');
    var current = 'todas';
    function norm(s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
    function apply() {
      var q = norm(search.value.trim()), shown = 0;
      groups.forEach(function (g) {
        var okGroup = current === 'todas' || g.dataset.grupo === current, any = 0;
        [].slice.call(g.querySelectorAll('details')).forEach(function (d) {
          var ok = okGroup && (!q || norm(d.textContent).indexOf(q) !== -1);
          d.hidden = !ok; if (ok) any++;
        });
        g.hidden = !any; shown += any;
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
