/**
 * NutriScienza affiliate tracker.
 *
 * Add this single tag (no other changes needed) to:
 *   - index.html
 *   - questionario.html
 *   - any page in the funnel
 *
 *   <script src="/affiliate-tracker.js" defer></script>
 *
 * Behaviour:
 *   1. On page load: if URL contains ?ref=CODE, validate the format and
 *      store it in localStorage with a 60-day expiry.
 *   2. Last-click attribution: a fresh ?ref= overwrites a previous one.
 *   3. On the intake POST, the questionnaire JS picks up the ref and
 *      includes it as `affiliateRef` in the body. We expose a global
 *      helper `window.NSAffiliate.getRef()` so the existing form code
 *      can read it without a refactor.
 *
 * Zero-risk principles:
 *   - No mutation of existing form code beyond adding the field
 *   - All operations wrapped in try/catch
 *   - Failure is silent: a tracking issue must NEVER block checkout
 */
(function () {
  'use strict';

  var KEY = 'ns_aff_ref';
  var TTL_MS = 60 * 24 * 60 * 60 * 1000; // 60 giorni
  var REF_PATTERN = /^[A-Z0-9_-]{3,40}$/i;

  function nowMs() { return Date.now(); }

  function store(ref) {
    try {
      localStorage.setItem(KEY, JSON.stringify({
        ref: ref.toUpperCase(),
        exp: nowMs() + TTL_MS,
      }));
    } catch (e) { /* localStorage disabled — drop silently */ }
  }

  function read() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return null;
      var obj = JSON.parse(raw);
      if (!obj || !obj.ref || !obj.exp) return null;
      if (obj.exp < nowMs()) {
        localStorage.removeItem(KEY);
        return null;
      }
      return obj.ref;
    } catch (e) { return null; }
  }

  function captureFromUrl() {
    try {
      var p = new URLSearchParams(window.location.search);
      var raw = p.get('ref');
      if (!raw) return;
      raw = raw.trim();
      if (REF_PATTERN.test(raw)) {
        store(raw);
      }
    } catch (e) { /* ignore */ }
  }

  // Esegui subito alla caricamento
  captureFromUrl();

  // Esponi helper globale per il codice del questionario
  window.NSAffiliate = {
    getRef: function () { return read(); },
    clear: function () { try { localStorage.removeItem(KEY); } catch (e) {} },
  };
})();
