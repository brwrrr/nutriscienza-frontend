/**
 * NutriScienza — Cookie Consent Banner
 * Drop this script anywhere in <body> or at end of <head>.
 * Consent is stored in localStorage for 180 days.
 * Call NS_Cookies.hasConsent('analytics') to check before loading GA/Pixel.
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'ns_cookie_consent';
  var EXPIRY_DAYS = 180;

  /* ── helpers ── */
  function saveConsent(level) {
    var expires = Date.now() + EXPIRY_DAYS * 864e5;
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ level: level, expires: expires }));
  }

  function loadConsent() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      var obj = JSON.parse(raw);
      if (Date.now() > obj.expires) { localStorage.removeItem(STORAGE_KEY); return null; }
      return obj;
    } catch (e) { return null; }
  }

  /* Public API */
  window.NS_Cookies = {
    hasConsent: function (category) {
      var obj = loadConsent();
      if (!obj) return false;
      if (obj.level === 'all') return true;
      if (obj.level === 'necessary' && category === 'necessary') return true;
      return false;
    }
  };

  /* If consent already given, nothing to show */
  if (loadConsent()) return;

  /* ── CSS ── */
  var style = document.createElement('style');
  style.textContent = [
    '#ns-cookie-banner{',
    '  position:fixed;bottom:0;left:0;right:0;z-index:99999;',
    '  background:#fff;border-top:1px solid #E5E0D3;',
    '  box-shadow:0 -4px 24px rgba(0,0,0,.10);',
    '  font-family:"Inter",-apple-system,sans-serif;',
    '  padding:18px 24px;',
    '  display:flex;align-items:center;justify-content:space-between;gap:20px;',
    '  flex-wrap:wrap;',
    '  animation:nsCookieSlideUp .35s cubic-bezier(.4,0,.2,1);',
    '}',
    '@keyframes nsCookieSlideUp{from{transform:translateY(100%);opacity:0}to{transform:translateY(0);opacity:1}}',
    '#ns-cookie-banner.ns-hiding{animation:nsCookieSlideDown .3s cubic-bezier(.4,0,.2,1) forwards;}',
    '@keyframes nsCookieSlideDown{to{transform:translateY(110%);opacity:0}}',
    '#ns-cookie-text{flex:1;min-width:220px;}',
    '#ns-cookie-text p{font-size:13.5px;color:#6B6B6B;line-height:1.5;margin:0;}',
    '#ns-cookie-text a{color:#2D5F3F;text-decoration:underline;}',
    '#ns-cookie-actions{display:flex;gap:10px;flex-shrink:0;flex-wrap:wrap;}',
    '.ns-btn-accept{',
    '  background:#2D5F3F;color:#fff;border:none;',
    '  padding:10px 22px;border-radius:8px;font-size:14px;font-weight:600;',
    '  cursor:pointer;font-family:inherit;transition:background .2s;',
    '  white-space:nowrap;',
    '}',
    '.ns-btn-accept:hover{background:#1A2E22;}',
    '.ns-btn-necessary{',
    '  background:transparent;color:#2D5F3F;',
    '  border:1.5px solid #2D5F3F;',
    '  padding:10px 20px;border-radius:8px;font-size:14px;font-weight:600;',
    '  cursor:pointer;font-family:inherit;transition:background .2s,color .2s;',
    '  white-space:nowrap;',
    '}',
    '.ns-btn-necessary:hover{background:#2D5F3F;color:#fff;}',
    '@media(max-width:600px){',
    '  #ns-cookie-banner{flex-direction:column;align-items:flex-start;}',
    '  #ns-cookie-actions{width:100%;}',
    '  .ns-btn-accept,.ns-btn-necessary{flex:1;text-align:center;}',
    '}'
  ].join('');
  document.head.appendChild(style);

  /* ── HTML ── */
  var banner = document.createElement('div');
  banner.id = 'ns-cookie-banner';
  banner.setAttribute('role', 'dialog');
  banner.setAttribute('aria-label', 'Consenso cookie');
  banner.innerHTML = [
    '<div id="ns-cookie-text">',
    '  <p>🍪 Utilizziamo cookie per migliorare la tua esperienza e, con il tuo consenso, per analisi e marketing.',
    '  Leggi la nostra <a href="/cookie-policy.html">Cookie Policy</a>.</p>',
    '</div>',
    '<div id="ns-cookie-actions">',
    '  <button class="ns-btn-necessary" id="ns-btn-necessary">Solo necessari</button>',
    '  <button class="ns-btn-accept"    id="ns-btn-accept">Accetta tutti</button>',
    '</div>'
  ].join('');

  /* Append once DOM is ready */
  function attachBanner() {
    document.body.appendChild(banner);

    function dismiss(level) {
      saveConsent(level);
      banner.classList.add('ns-hiding');
      setTimeout(function () { banner.remove(); }, 350);
      /* If analytics accepted, fire your GA / Meta Pixel init here */
      if (level === 'all') {
        var ev = new CustomEvent('nsCookieAccepted', { detail: { level: level } });
        document.dispatchEvent(ev);
      }
    }

    document.getElementById('ns-btn-accept').addEventListener('click', function () { dismiss('all'); });
    document.getElementById('ns-btn-necessary').addEventListener('click', function () { dismiss('necessary'); });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', attachBanner);
  } else {
    attachBanner();
  }
})();
