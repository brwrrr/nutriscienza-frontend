/*
 * lead-box.js — riquadro "guida gratuita" riutilizzabile nelle pagine guida.
 * Uso: <div data-ns-lead></div> + <script src="lead-box.js" defer></script>
 * Invia a POST /api/lead (stesso flusso della landing ordine-dei-cibi.html):
 * email transazionale con la guida sempre; sequenza email SOLO con la spunta.
 * Il testo del consenso è identico alla landing → stessa CONSENT_VERSION.
 * Se cambi il testo della casella, cambia anche CONSENT_VERSION (qui e nella landing).
 */
(function () {
  var API_BASE = (location.hostname === 'localhost' || location.hostname.indexOf('127.') === 0)
    ? 'http://localhost:8000' : 'https://nutriscienza-api.onrender.com';
  var CONSENT_VERSION = 'guide-2026-10-28';
  var GUIDE = 'ordine-dei-cibi';

  var CSS = ''
    + '.nsl{margin-top:28px;background:#FBF9F4;border:1px solid #E5E0D3;border-left:4px solid #C9A66B;border-radius:14px;padding:28px 30px;color:#2A2A2A;text-align:left}'
    + '.nsl .nsl-k{font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:#A88349;font-weight:700;margin:0 0 6px}'
    + '.nsl h3{font-size:22px;color:#2D5F3F;margin:0 0 8px;line-height:1.25}'
    + '.nsl p{font-size:15px;line-height:1.55;margin:0 0 14px;max-width:none}'
    + '.nsl-row{display:flex;gap:10px;flex-wrap:wrap}'
    + '.nsl-row input[type=email]{flex:1 1 220px;min-width:0;padding:13px 14px;border:1px solid #CFC8B6;border-radius:8px;font-size:16px;font-family:inherit;background:#fff;color:#2A2A2A}'
    + '.nsl-row input[type=email]:focus{outline:2px solid #2D5F3F;outline-offset:1px}'
    + '.nsl-btn{flex:0 0 auto;background:#2D5F3F;color:#fff;border:0;border-radius:8px;padding:13px 22px;font-size:16px;font-weight:700;font-family:inherit;cursor:pointer;text-decoration:none;display:inline-block}'
    + '.nsl-btn:hover{background:#1A2E22;color:#fff}.nsl-btn[disabled]{opacity:.6;cursor:default}'
    + '.nsl-check{display:flex;gap:10px;align-items:flex-start;font-size:13.5px;font-weight:400;line-height:1.5;margin:14px 0 0;color:#2A2A2A;cursor:pointer}'
    + '.nsl-check input{margin:3px 0 0;padding:0;flex:0 0 auto;width:16px;height:16px}'
    + '.nsl-legal{font-size:12px!important;color:#6B6B6B;margin:12px 0 0!important}'
    + '.nsl-legal a{color:#2D5F3F}'
    + '.nsl-err{display:none;color:#B3261E;font-size:14px!important;margin:10px 0 0!important}'
    + '.nsl-lbl{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}'
    + '.nsl-ok{display:none}';

  function source() {
    var p = new URLSearchParams(location.search);
    var t = (window.NSTraffic && window.NSTraffic.get()) || {};
    return {
      utmSource: p.get('utm_source') || t.utmSource || null,
      utmMedium: p.get('utm_medium') || t.utmMedium || null,
      utmCampaign: p.get('utm_campaign') || t.utmCampaign || null,
      referrer: t.referrer || (document.referrer && document.referrer.indexOf(location.host) === -1 ? document.referrer : null),
      landingPage: (location.pathname + location.search).slice(0, 400)
    };
  }

  function build(host, n) {
    var id = 'nsl' + n;
    host.className = (host.className ? host.className + ' ' : '') + 'nsl';
    host.innerHTML = ''
      + '<form novalidate>'
      + '<p class="nsl-k">Guida gratuita · PDF</p>'
      + '<h3>L\'ordine giusto nel piatto</h3>'
      + '<p>Stessi cibi, ordine diverso: cosa dicono gli studi su ordine dei cibi e glicemia e come applicarlo a pasta, pizza e colazione. 5 pagine, fonti scientifiche incluse. Te la inviamo subito via email.</p>'
      + '<div class="nsl-row">'
      + '<label class="nsl-lbl" for="' + id + '-email">La tua email</label>'
      + '<input type="email" id="' + id + '-email" name="email" autocomplete="email" placeholder="nome@email.it" required>'
      + '<button type="submit" class="nsl-btn">Inviami la guida →</button>'
      + '</div>'
      + '<label class="nsl-check"><input type="checkbox" name="marketing">'
      + '<span>Sì, voglio ricevere altri consigli pratici e le offerte di NutriScienza via email (al massimo due a settimana, cancellazione con un clic). <em>Facoltativo.</em></span></label>'
      + '<p class="nsl-err" role="alert"></p>'
      + '<p class="nsl-legal">Usiamo la tua email per inviarti la guida richiesta e, solo se hai spuntato la casella, per i nostri consigli e offerte. Nessuna cessione a terzi. Dettagli nell\'<a href="privacy-policy.html#guide" target="_blank" rel="noopener">informativa privacy</a>.</p>'
      + '</form>'
      + '<div class="nsl-ok" role="status">'
      + '<p class="nsl-k">Guida in arrivo</p>'
      + '<h3>Controlla la tua email</h3>'
      + '<p>L\'abbiamo inviata a <strong class="nsl-to"></strong>. Guarda anche nello spam o nella scheda Promozioni. Puoi anche scaricarla subito:</p>'
      + '<a class="nsl-btn" target="_blank" rel="noopener" href="' + API_BASE + '/api/guide/' + GUIDE + '/download?c=pagina">Scarica la guida (PDF)</a>'
      + '</div>';

    var form = host.querySelector('form'), err = host.querySelector('.nsl-err'),
        btn = form.querySelector('button'), input = form.querySelector('input[type=email]');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = input.value.trim();
      err.style.display = 'none';
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
        err.textContent = 'Inserisci un indirizzo email valido.'; err.style.display = 'block'; return;
      }
      btn.disabled = true; btn.textContent = 'Invio in corso…';
      var s = source();
      fetch(API_BASE + '/api/lead', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: email,
          marketingConsent: form.querySelector('input[name=marketing]').checked,
          consentVersion: CONSENT_VERSION,
          guide: GUIDE,
          utmSource: s.utmSource, utmMedium: s.utmMedium, utmCampaign: s.utmCampaign,
          referrer: s.referrer, landingPage: s.landingPage
        })
      }).then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        host.querySelector('.nsl-to').textContent = email;
        form.style.display = 'none';
        host.querySelector('.nsl-ok').style.display = 'block';
        if (typeof window.gtag === 'function') window.gtag('event', 'generate_lead', { lead_source: 'guida_inline', page: location.pathname });
      }).catch(function () {
        err.textContent = 'Non siamo riusciti a inviare la richiesta. Riprova tra poco o scrivici a supporto@nutriscienza.org.';
        err.style.display = 'block';
        btn.disabled = false; btn.textContent = 'Inviami la guida →';
      });
    });
  }

  function init() {
    var hosts = document.querySelectorAll('[data-ns-lead]');
    if (!hosts.length) return;
    var st = document.createElement('style'); st.textContent = CSS; document.head.appendChild(st);
    for (var i = 0; i < hosts.length; i++) build(hosts[i], i);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
