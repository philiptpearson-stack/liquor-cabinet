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

  // A door that points at a tucked-away card (like the Cabinet Card) opens it
  document.querySelectorAll('a.door[href^="#"]').forEach(a => a.addEventListener('click', () => {
    const t = document.querySelector(a.getAttribute('href'));
    if (t && t.tagName === 'DETAILS') t.open = true;
  }));

  // Pause / play everything, including the crayon line boil
  function setStill(v) {
    root.classList.toggle('still', v);
    btn.textContent = v ? 'Play motion' : 'Pause motion';
    btn.setAttribute('aria-pressed', String(v));
    try { v ? defs.pauseAnimations() : defs.unpauseAnimations(); } catch (e) {}
  }
  btn.addEventListener('click', () => setStill(!root.classList.contains('still')));
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) setStill(true);
})();
