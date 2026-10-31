// The Liquor Cabinet: page extras. Everything here is optional polish.
// The pages animate on CSS alone; this file only adds the Pause button,
// the reading bar, and pausing scenes while they're off screen.
(() => {
  const root = document.documentElement;
  root.classList.add('js');
  const btn = document.getElementById('motion');
  const defs = document.getElementById('defs');
  const fill = document.getElementById('fill');

  // Reading progress
  function progress() {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    fill.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, window.scrollY / max) : 1) + ')';
  }
  window.addEventListener('scroll', progress, { passive: true });
  window.addEventListener('resize', progress);
  progress();

  // Scenes only move while they're on screen, so each one starts fresh when you arrive
  const figs = [...document.querySelectorAll('.fig')];
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => entries.forEach(e => e.target.classList.toggle('on', e.isIntersecting)), { threshold: 0.35 });
    figs.forEach(f => io.observe(f));
  } else {
    figs.forEach(f => f.classList.add('on'));
  }

  // Doors you've opened get a crayon check mark (remembered on this device only)
  try {
    const key = 'lc:visited', clean = p => p.replace(/index\.html$/, '');
    const seen = new Set(JSON.parse(localStorage.getItem(key) || '[]'));
    seen.add(clean(location.pathname));
    localStorage.setItem(key, JSON.stringify([...seen]));
    document.querySelectorAll('a.door:not([href^="#"])').forEach(a => {
      if (seen.has(clean(new URL(a.getAttribute('href'), location.href).pathname))) a.classList.add('visited');
    });
  } catch (e) {}

  // "Back to the bottle" on a shared page (like Fermentation) returns to whichever bottle sent you,
  // to the spot you left (like the back button). Without a referrer it goes to the link's own default.
  try {
    const from = document.referrer && new URL(document.referrer);
    if (from && from.origin === location.origin && from.pathname !== location.pathname)
      document.querySelectorAll('a[data-back]').forEach(a => {
        a.href = from.href;
        a.addEventListener('click', e => { if (history.length > 1) { e.preventDefault(); history.back(); } });
      });
  } catch (e) {}

  // A "Back" link (at the end of the story, or up in the bar) that points at the page you just came
  // from works like the back button: you land where you left off, not at the top.
  try {
    const from = document.referrer && new URL(document.referrer), clean = p => p.replace(/index\.html$/, '');
    if (from && from.origin === location.origin)
      document.querySelectorAll('.back a:not([data-back]), a.bar-back:not([data-back])').forEach(a => {
        if (clean(new URL(a.href, location.href).pathname) === clean(from.pathname))
          a.addEventListener('click', e => { if (history.length > 1) { e.preventDefault(); history.back(); } });
      });
  } catch (e) {}

  // Following a link into another page starts you at the top of it. Some viewers (the private
  // preview, for one) carry the last page's scroll position over, which dropped readers mid-story.
  // The back button and "Back to the bottle" still return you to where you were.
  const FRESH = 'lc:fresh';
  document.addEventListener('click', e => {
    const a = e.target.closest && e.target.closest('a[href]');
    if (!a || e.defaultPrevented || a.hasAttribute('data-back') || a.target === '_blank' || a.getAttribute('href').startsWith('#')) return;
    try {
      const to = new URL(a.href, location.href);
      if (to.origin === location.origin && to.pathname !== location.pathname) sessionStorage.setItem(FRESH, to.pathname);
    } catch (err) {}
  });
  try {
    if (sessionStorage.getItem(FRESH) === location.pathname) {
      sessionStorage.removeItem(FRESH);
      let hold = true;
      const top = () => { if (hold) window.scrollTo(0, 0); };
      ['wheel', 'touchstart', 'keydown'].forEach(t => window.addEventListener(t, () => { hold = false; }, { once: true, passive: true }));
      top();
      requestAnimationFrame(top);
      window.addEventListener('load', top, { once: true });
      [100, 300, 700].forEach(ms => setTimeout(top, ms));
    }
  } catch (e) {}

  // A door that points at a tucked-away card (like the Cabinet Card) opens it
  document.querySelectorAll('a.door[href^="#"]').forEach(a => a.addEventListener('click', () => {
    const t = document.querySelector(a.getAttribute('href'));
    if (t && t.tagName === 'DETAILS') t.open = true;
  }));

  // Pause / play everything, including the crayon line boil
  function setStill(v) {
    root.classList.toggle('still', v);
    btn.innerHTML = (v ? 'Play' : 'Pause') + '<span class="long"> motion</span>';
    btn.setAttribute('aria-label', v ? 'Play motion' : 'Pause motion');
    btn.setAttribute('aria-pressed', String(v));
    try { v ? defs.pauseAnimations() : defs.unpauseAnimations(); } catch (e) {}
  }
  btn.addEventListener('click', () => setStill(!root.classList.contains('still')));
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) setStill(true);
})();
