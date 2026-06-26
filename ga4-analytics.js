/**
 * NutriScienza — Google Analytics 4 (consent-aware loader)
 * ---------------------------------------------------------
 * Loads GA4 ONLY after the visitor grants "analytics" consent through the
 * cookie banner (cookie-banner.js → window.NS_Cookies / "nsCookieAccepted").
 *
 * Honors the promises made in cookie-policy.html:
 *   • IP anonymization ON (GA4 anonymizes by default; flag kept for clarity)
 *   • Google Signals OFF  (no cross-device / ads data)
 *   • Ad personalization OFF
 *
 * ─────────────────────────────────────────────────────────────────────────
 * SETUP (one step): replace G-XXXXXXXXXX below with your GA4 Measurement ID.
 * Until then this script does nothing. See GA4_Setup_Instructions.md.
 * ─────────────────────────────────────────────────────────────────────────
 */
(function () {
  'use strict';

  var GA_ID = 'G-KTQV8SE2CM'; // NutriScienza GA4 Measurement ID

  // Not configured yet → do nothing.
  if (!GA_ID || GA_ID.indexOf('G-') !== 0 || GA_ID === 'G-XXXXXXXXXX') return;

  function loadGA() {
    if (window.__nsGaLoaded) return;
    window.__nsGaLoaded = true;

    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);

    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }
    window.gtag = gtag;

    // Privacy defaults to match the cookie policy.
    gtag('set', 'allow_ad_personalization_signals', false);
    gtag('js', new Date());
    gtag('config', GA_ID, {
      anonymize_ip: true,
      allow_google_signals: false,
      allow_ad_personalization_signals: false
    });
  }

  // 1) Returning visitor who already accepted analytics → load immediately.
  if (window.NS_Cookies && window.NS_Cookies.hasConsent('analytics')) {
    loadGA();
    return;
  }

  // 2) New visitor → load the moment they click "Accetta tutti" in the banner.
  document.addEventListener('nsCookieAccepted', function (e) {
    if (e && e.detail && e.detail.level === 'all') loadGA();
  });
})();
