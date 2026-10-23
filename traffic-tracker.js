/**
 * NutriScienza traffic tracker (first-touch attribution).
 *
 * Add this single tag (no other changes needed) to every funnel page:
 *   - index.html
 *   - questionario.html
 *
 *   <script src="/traffic-tracker.js" defer></script>
 *
 * Behaviour:
 *   1. On the FIRST page the visitor lands on, capture utm_source/medium/campaign
 *      (from ?utm_* params), the external referrer, and the landing page path.
 *   2. First-touch wins: once stored, a later visit does NOT overwrite it
 *      (so the source that originally brought the customer gets the credit).
 *      Expires after 60 days.
 *   3. The questionnaire JS reads window.NSTraffic.get() and includes the fields
 *      in the intake POST. The backend stores them on the order and shows
 *      source -> signups -> paid revenue in the admin "Traffico" tab.
 *
 * Zero-risk principles:
 *   - All operations wrapped in try/catch; failure is silent.
 *   - A tracking issue must NEVER block checkout.
 */
(function () {
  'use strict';

  // GDPR/ePrivacy: salviamo nel browser SOLO con consenso analitico ('all').
  // Senza consenso il dato resta in memoria (vale solo per la pagina corrente).
  var mem = null;
  function consented() {
    try { var o = JSON.parse(localStorage.getItem('ns_cookie_consent'));
      return !!(o && o.level === 'all' && Date.now() < o.expires); } catch (e) { return false; }
  }

  var KEY = 'ns_traffic';
  var TTL_MS = 60 * 24 * 60 * 60 * 1000; // 60 giorni

  function nowMs() { return Date.now(); }

  function read() {
    if (!consented()) return mem;
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return null;
      var obj = JSON.parse(raw);
      if (!obj || !obj.exp) return null;
      if (obj.exp < nowMs()) { localStorage.removeItem(KEY); return null; }
      return obj.data || null;
    } catch (e) { return null; }
  }

  function store(data) {
    mem = data;
    if (!consented()) return;
    try {
      localStorage.setItem(KEY, JSON.stringify({ data: data, exp: nowMs() + TTL_MS }));
    } catch (e) { /* localStorage disabled — drop silently */ }
  }

  function clean(v, max) {
    if (!v) return null;
    v = String(v).trim();
    if (!v) return null;
    return v.slice(0, max || 120);
  }

  function externalReferrer() {
    try {
      var r = document.referrer || '';
      if (!r) return null;
      // Ignora i referrer interni (stesso host) — ci interessa la sorgente esterna.
      var host = new URL(r).hostname;
      if (host && host === window.location.hostname) return null;
      return clean(r, 400);
    } catch (e) { return null; }
  }

  function captureFirstTouch() {
    try {
      if (read()) return; // first-touch già registrato
      var p = new URLSearchParams(window.location.search);
      var data = {
        utmSource: clean(p.get('utm_source')),
        utmMedium: clean(p.get('utm_medium')),
        utmCampaign: clean(p.get('utm_campaign')),
        referrer: externalReferrer(),
        // ns_lp = pagina d'arrivo originale, passata nel link quando non c'è consenso
        landingPage: clean(p.get('ns_lp') || (window.location.pathname + window.location.search), 400)
      };
      // Inferenza leggera: se non c'è utm_source ma c'è un referrer esterno,
      // usa il dominio del referrer come sorgente (es. google, instagram).
      if (!data.utmSource && data.referrer) {
        try {
          data.utmSource = clean(new URL(data.referrer).hostname.replace(/^www\./, ''));
          data.utmMedium = data.utmMedium || 'referral';
        } catch (e) { /* ignore */ }
      }
      // Salva solo se c'è almeno un segnale (evita righe vuote inutili).
      if (data.utmSource || data.referrer) store(data);
    } catch (e) { /* ignore */ }
  }

  captureFirstTouch();

  // Senza consenso non salviamo nulla nel browser: per non perdere la provenienza
  // tra homepage/guide e questionario la passiamo nei link interni (parametri URL,
  // nessuna memorizzazione sul dispositivo).
  function decorateLinks() {
    try {
      if (consented()) return;
      var t = mem || {};
      var ref = (window.NSAffiliate && window.NSAffiliate.getRef()) || null;
      var params = {};
      if (t.utmSource) params.utm_source = t.utmSource;
      if (t.utmMedium) params.utm_medium = t.utmMedium;
      if (t.utmCampaign) params.utm_campaign = t.utmCampaign;
      if (t.landingPage && (t.utmSource || ref)) params.ns_lp = t.landingPage;
      if (ref) params.ref = ref;
      if (!Object.keys(params).length) return;
      var links = document.querySelectorAll('a[href]');
      for (var i = 0; i < links.length; i++) {
        var a = links[i], raw = a.getAttribute('href');
        if (!raw || raw.charAt(0) === '#' || /^(mailto|tel|javascript):/i.test(raw)) continue;
        var u = new URL(raw, window.location.href);
        if (u.origin !== window.location.origin) continue;
        if (u.pathname === window.location.pathname) continue;           // ancore nella stessa pagina
        if (/(privacy|cookie|termini|esempio)/.test(u.pathname)) continue;
        if (!/(\/|\.html)$/.test(u.pathname)) continue;
        for (var k in params) { if (!u.searchParams.has(k)) u.searchParams.set(k, params[k]); }
        a.setAttribute('href', u.pathname.replace(/^\//, '') + u.search + u.hash);
      }
    } catch (e) { /* mai bloccare la navigazione */ }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', decorateLinks);
  else decorateLinks();

  window.addEventListener('ns:consent', function (e) {
    if (e.detail === 'all') { if (mem) store(mem); }
    else { try { localStorage.removeItem(KEY); } catch (x) {} }
  });

  window.NSTraffic = {
    get: function () { return read() || {}; },
    clear: function () { try { localStorage.removeItem(KEY); } catch (e) {} }
  };
})();
