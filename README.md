# Tbilisi Home — Expats: Remote Banking Guides

Four ready-to-publish pages for the **Expats** tab on [tbilisihome.ge](https://tbilisihome.ge/), teaching foreign buyers and leads how to start opening a Georgian bank account **before they arrive** — so the in-person part becomes a single ~1-hour branch visit with one of our private bankers.

## Pages

| File | Page |
|---|---|
| `expats/banking-in-georgia.html` | Hub page — how the process works with Tbilisi Home, bank comparison table, universal document checklist |
| `expats/bank-of-georgia-account.html` | Bank of Georgia guide (incl. SOLO) |
| `expats/tbc-bank-account.html` | TBC Bank guide (incl. online pre-registration and TBC Concept) |
| `expats/liberty-bank-account.html` | Liberty Bank guide |
| `expats/style.css` | Shared stylesheet |

Each bank guide has the same structure: at-a-glance box → why this bank → pre-arrival steps → document checklist → what happens at the branch visit → fully-remote power-of-attorney option → FAQ → contact CTA.

## Publishing to tbilisihome.ge (WordPress / Houzez)

1. Create four pages under the **Expats** menu item, e.g.:
   - `/expats/banking-in-georgia/`
   - `/expats/bank-of-georgia-account/`
   - `/expats/tbc-bank-account/`
   - `/expats/liberty-bank-account/`
2. For each page, copy everything inside `<main class="wrap">…</main>` into a Custom HTML block (or the theme's raw-HTML element). The site header/footer in these files are placeholders — the WordPress theme provides the real ones.
3. Add the contents of `expats/style.css` once via **Appearance → Customize → Additional CSS** (or a per-page CSS block).
4. Update the internal links between the guides to the final WordPress URLs, and point the CTA buttons at the site's real contact page (currently `https://tbilisihome.ge/contact/` — swap for WhatsApp/contact form link if preferred).

## Content notes

- All bank facts hedged and current as of **August 2026**; each page carries a "last reviewed" date and a not-legal-advice disclaimer — update the date when facts are re-verified.
- Fees and timelines are given as ranges (e.g. compliance review 2–7 business days, POA route 2–4 weeks) because banks change them; the private bankers should confirm specifics per client.
- TBC is presented as the only bank with public online pre-registration for foreigners; BOG and Liberty remote-start runs through the document pack + private-banker pre-review.
