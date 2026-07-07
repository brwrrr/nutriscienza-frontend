# Google Analytics 4 — Setup & Implementation Notes (NutriScienza)

_Last updated: 2026-06-26_

## What this does
Adds Google Analytics 4 (GA4) to nutriscienza.org so you can see **where your
traffic comes from** — direct, organic search, social, referral, paid, plus full
UTM campaign attribution. GA4 captures traffic source automatically; no extra
config is needed for source/medium/campaign reports.

The tag is **consent-aware**: it only fires after a visitor clicks
**"Accetta tutti"** in the existing cookie banner, satisfying GDPR / the Italian
Garante rules. Visitors who choose "Solo necessari" are not tracked.

---

## ✅ STATUS — property created, ID installed

- **GA4 property:** `NutriScienza` (under the existing Analytics account), timezone Italy, currency EUR.
- **Web data stream:** `NutriScienza Web` → https://nutriscienza.org, Enhanced Measurement ON.
- **Measurement ID:** `G-KTQV8SE2CM` — already pasted into `ga4-analytics.js`.

**Only step left: deploy the updated `frontend/` folder to Render, then verify (below).**

---

## Reference: how the property was created (in case you need to redo it)

### 1. Create the GA4 property (~5 min)
1. Go to https://analytics.google.com and sign in with your Google account.
2. **Admin** (bottom-left gear) → **Create** → **Property**.
3. Property name: `NutriScienza`. Set timezone to **Italy (GMT+1)** and currency **EUR**. → Next.
4. Fill business details → **Create**.
5. When prompted to set up a data stream, choose **Web**.
6. Website URL: `https://nutriscienza.org` · Stream name: `NutriScienza Web` → **Create stream**.
7. Copy the **Measurement ID** shown — it looks like `G-XXXXXXXXXX`.

### 2. Paste the ID into the code  — DONE
`ga4-analytics.js` now contains:

```js
var GA_ID = 'G-KTQV8SE2CM'; // NutriScienza GA4 Measurement ID
```

No other file needs editing.

### 3. Keep privacy settings aligned (recommended)
In GA4 **Admin → Data Settings → Data Collection**, leave **Google Signals
OFF** (it is off by default on new properties). The code already disables
Google Signals and ad personalization client-side, matching what
`cookie-policy.html` promises users.

### 4. Deploy
Push/upload the updated `frontend/` folder to your host (Render). After deploy,
open the site, click **"Accetta tutti"** on the banner, then check GA4 →
**Reports → Realtime** — you should see yourself as 1 active user within seconds.

---

## Where to see "where traffic comes from"
In GA4:
- **Reports → Acquisition → Traffic acquisition** — sessions by channel
  (Direct, Organic Search, Organic Social, Referral, Paid, Email…).
- **Reports → Acquisition → User acquisition** — first-touch source for new users.
- Add a **Session source / medium** secondary dimension for granular detail.

### Tag your campaign links with UTMs
For links you share (Instagram bio, email footer, ads), append UTM parameters so
GA4 attributes them correctly. Example:
```
https://nutriscienza.org/?utm_source=instagram&utm_medium=social&utm_campaign=reels_june
```
Build them with Google's Campaign URL Builder:
https://ga-dev-tools.google/campaign-url-builder/

---

## How the implementation works (for future reference)

| File | Role |
|------|------|
| `cookie-banner.js` | Existing consent banner. Exposes `NS_Cookies.hasConsent('analytics')` and fires a `nsCookieAccepted` event on "Accetta tutti". Stores consent in localStorage for 180 days. |
| `ga4-analytics.js` | **New.** Loads gtag.js only when analytics consent exists (returning visitor) or is granted (new visitor via the event). Sets `anonymize_ip`, disables Google Signals + ad personalization. |

**Load order on every page:** `cookie-banner.js` then `ga4-analytics.js`
(banner must define `NS_Cookies` first).

### Pages covered
GA4 is on all **10 public pages**: index, questionario, checkin, grazie,
affiliate, piano_base_esempio, piano_completo_esempio,
privacy-policy, cookie-policy, termini-e-condizioni.
(esempio-piano was removed 2026-07-07.)

**`admin.html` is intentionally excluded** — internal admin sessions would
otherwise pollute your traffic data. (affiliate.html and the two `piano_*_esempio`
pages had no cookie banner before; the banner was added to them too so consent is
consistent site-wide.)

### Why consent-gated and not always-on
nutriscienza.org serves EU users. Under GDPR / ePrivacy and the Garante's cookie
rules, analytics cookies (`_ga`, `_ga_*`) require prior consent. Firing GA4 only
after "Accetta tutti" keeps you compliant; the cookie policy already declares
these cookies.

---

## Verification checklist
- [x] GA4 property `NutriScienza` created, Web stream `NutriScienza Web` added.
- [x] Measurement ID `G-KTQV8SE2CM` pasted into `ga4-analytics.js`.
- [x] Deployed to Render (git push → auto-deploy, 2026-06-26).
- [x] Banner "Accetta tutti" → verified live: gtag.js loaded with G-KTQV8SE2CM,
      page_view sent (anonymize_ip=true, npa=1), confirmed 1 active user + 2 views
      in GA4 Realtime. NOTE: the /g/collect beacon shows HTTP 503 in the network
      panel but data still lands in GA4 — this is cosmetic, not a fault.
- [ ] Banner "Solo necessari" → NO `_ga` cookie set, no Realtime hit (optional
      spot-check in a private window; DevTools → Application → Cookies).
- [ ] Traffic acquisition report populating after 24–48h.
