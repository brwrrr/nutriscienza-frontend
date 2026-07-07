# NutriScienza — Deployment Guide (no Git required)

This guide deploys everything from a fresh machine using only a browser and the Render dashboard. No Git, no GitHub.

---

## What you're deploying

| Part | Where | Notes |
|---|---|---|
| FastAPI backend | Render Web Service | Python 3.11, free tier fine to start |
| Daily cron (scheduler) | Render Cron Job | Same repo, different start command |
| Static frontend | Render Static Site **or** any host (Netlify, Cloudflare Pages) | Plain HTML — no build step |
| Database | SQLite file on Render disk | Upgrade to Postgres later if needed |

---

## Step 1 — Prepare the files on this machine

1. Open Finder → navigate to the `Nutriscienza/outputs/backend/` folder.
2. Create a copy of `.env.example` named `.env` and fill in all values (see section below).
3. Zip the **entire `backend/` folder** → right-click → "Compress". You'll get `backend.zip`.
4. Separately, zip the **`outputs/` folder root** (all `.html`, `.js` files) → `frontend.zip`.

### `.env` values you need before deployment

```
ANTHROPIC_API_KEY=sk-ant-…
STRIPE_SECRET_KEY=sk_live_…        # or sk_test_ for testing
STRIPE_WEBHOOK_SECRET=whsec_…      # created in Step 3
RESEND_API_KEY=re_…
STRIPE_PRICE_BASE=price_…          # one-time price ID
STRIPE_PRICE_COMPLETO=price_…      # monthly recurring price ID
STRIPE_PRICE_COACH=price_…         # monthly recurring price ID
BASE_URL=https://nutriscienza.org
FROM_EMAIL=NutriScienza <piani@nutriscienza.org>
SUPPORT_EMAIL=supporto@nutriscienza.org
ADMIN_EMAIL=info@marcinpiwowarczyk.com
DATABASE_URL=sqlite:///./nutriscienza.db
```

---

## Step 2 — Deploy the backend on Render

### 2a. Create a Web Service (manual deploy)

1. Go to [render.com](https://render.com) → **New → Web Service**.
2. Choose **"Deploy an existing image or upload files"** → select **"Manual deploy / upload"**.
   - If Render asks for a Git repo, choose **"Public Git repository"** and use a throwaway GitHub repo (see note at end) OR use Render's **"Upload files"** option if available on your plan.
   - **Simplest path**: create a free GitHub account on another machine, push the `backend/` folder, connect it here. You only need to do this once — after that Render auto-deploys on every push.
3. Settings:
   - **Name**: `nutriscienza-api`
   - **Runtime**: Python 3
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Root directory**: `/` (the zip is already the backend folder)
4. Under **Environment** → add all variables from your `.env` file (one by one, or paste as a bulk env file).
5. Click **Deploy**.

### 2b. Note the backend URL

Once running, Render gives you a URL like:  
`https://nutriscienza-api.onrender.com`

You'll need this for the Stripe webhook (Step 3) and optionally in `API_BASE` in `questionario.html` (see Step 5).

---

## Step 3 — Configure Stripe webhooks

1. Stripe Dashboard → **Developers → Webhooks → Add endpoint**.
2. Endpoint URL: `https://nutriscienza-api.onrender.com/webhook`
3. Events to listen for:
   - `checkout.session.completed`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
   - `customer.subscription.deleted`
4. Copy the **Signing secret** (`whsec_…`) and add it to Render as `STRIPE_WEBHOOK_SECRET`.

---

## Step 4 — Add the Cron Job (monthly plan refresh)

1. Render Dashboard → **New → Cron Job**.
2. Same service / same repo as the web service.
3. Settings:
   - **Name**: `nutriscienza-scheduler`
   - **Command**: `python -m app.scheduler`
   - **Schedule**: `0 7 * * *` (runs every day at 07:00 UTC)
4. Add the same environment variables as the web service.

---

## Step 5 — Deploy the frontend

### Option A — Render Static Site (simplest, same platform)

1. Render → **New → Static Site**.
2. Upload / connect the frontend files (all `.html`, `.js` files from `outputs/`).
3. Set **Publish directory** to `/` (root of the zip).
4. **Custom domain**: add `nutriscienza.org` and follow Render's DNS instructions.

### Option B — Netlify (drag-and-drop, no account needed)

1. Go to [app.netlify.com/drop](https://app.netlify.com/drop).
2. Drag the folder containing all your `.html` and `.js` files onto the page.
3. Netlify gives you an instant URL. Then add your custom domain in Site Settings.

### Option C — Cloudflare Pages

1. Cloudflare Dashboard → **Pages → Create a project → Upload assets**.
2. Drag the folder. Set `index.html` as the root.

### Rename `nutriscienza.html` → `index.html`

Before uploading the frontend, rename `nutriscienza.html` to `index.html`. This ensures `nutriscienza.org/` loads the landing page automatically. (Note: `esempio-piano.html` was removed 2026-07-07 — a `_redirects` file now 301s the old URL to `/#piani`.)

---

## Step 6 — Update `API_BASE` in `questionario.html`

Open `questionario.html` and find:

```javascript
const API_BASE = '';   // same-origin when served from the same domain
```

If your frontend and backend are on the same domain (e.g., behind a reverse proxy), leave it as `''`.

If they're on different domains (e.g., frontend on Netlify, backend on Render), change it to:

```javascript
const API_BASE = 'https://nutriscienza-api.onrender.com';
```

---

## Step 7 — DNS for nutriscienza.org

Point your domain to wherever you're hosting the frontend:

| Host | DNS record type | Value |
|---|---|---|
| Render Static Site | CNAME | `<your-site>.onrender.com` |
| Netlify | CNAME | `<your-site>.netlify.app` |
| Cloudflare Pages | CNAME | `<your-project>.pages.dev` |

For the apex domain (`nutriscienza.org` without www), use an ALIAS / ANAME record if your DNS provider supports it, or a Cloudflare proxied A record.

---

## Step 8 — Smoke test checklist

- [ ] `https://nutriscienza.org` loads the landing page
- [ ] "Inizia ora" buttons open `questionario.html` with the correct `?piano=` param pre-selected
- [ ] Complete a test checkout with Stripe test card `4242 4242 4242 4242`
- [ ] `grazie.html` loads after payment
- [ ] Plan PDF arrives in email within a few minutes
- [ ] Check Render logs (`nutriscienza-api` → Logs) for any errors
- [ ] Stripe Dashboard shows the test payment in Payments

---

## Transferring files without GitHub

If you'd rather avoid GitHub entirely for the first deploy:

1. **Render "Upload" option**: some Render plans allow direct zip upload. Check your plan tier.
2. **Netlify drop** (frontend only, as above — zero account needed).
3. **SFTP**: if you have SSH access to any VPS, `scp` the zip and run the server directly.
4. **GitHub from another machine**: takes 5 minutes — `git init`, `git add .`, `git commit -m "init"`, create a GitHub repo, `git push`. Then connect Render to it. After the first push, Render auto-deploys on every subsequent push from any machine.

---

## Ongoing updates

To update the site after making changes:
- **Backend**: push to GitHub (or re-zip and re-upload) → Render auto-deploys.
- **Frontend**: drag-and-drop the updated files onto Netlify/Cloudflare, or push to the repo.
- **`.env` / secrets**: edit directly in Render's Environment tab — no re-deploy needed for env changes.
