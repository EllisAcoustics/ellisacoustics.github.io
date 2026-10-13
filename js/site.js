/* ==========================================================================
   ellisacoustics.github.io: shared behaviour
   The theme itself is set by a tiny inline script in each page's <head>, so
   the page never flashes the wrong colours. This file adds the switch, keeps
   the tab icon and browser bar in step with it, and says hello in the console.
   ========================================================================== */
(() => {
  const root = document.documentElement;
  const toggle = document.querySelector('.theme-toggle');

  // Tab icon and browser bar follow the theme, including the visitor's own choice from the switch
  const syncChrome = () => {
    const dark = root.getAttribute('data-theme') === 'dark';
    document.querySelectorAll('meta[name="theme-color"]').forEach((m) => m.setAttribute('content', dark ? '#0B0B0C' : '#FFFFFF'));
    document.querySelectorAll('link[rel="icon"][type="image/svg+xml"]').forEach((l) => l.setAttribute('href', dark ? 'favicon.svg' : 'favicon-light.svg'));
    if (toggle) toggle.setAttribute('aria-checked', dark ? 'true' : 'false');
  };
  if (toggle) toggle.addEventListener('click', () => window.__setTheme && window.__setTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'));
  new MutationObserver(syncChrome).observe(root, { attributes: true, attributeFilter: ['data-theme'] });
  syncChrome();

  // For the developers who open the console
  try {
    console.log(
      '%c▁▂▃▅▇█▇▅▃▂▁▂▃▅▇▅▃▂▁  Max Ellis · psychoacoustics\n%cHand-built: no frameworks, no trackers, no cookies. The CV PDF is printed from these pages.\nLooking for someone who can hear the future? ellisacoustics.github.io/contact',
      'font: 600 13px ui-monospace, monospace; color: #3FAE3A',
      'font: 12px ui-monospace, monospace; color: inherit'
    );
  } catch (e) {}
})();
