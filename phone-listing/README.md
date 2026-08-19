# Listing Properties from the Phone

The system that lets Nino capture a property on her phone in ~2 minutes and have
it published everywhere (tbilisihome.ge, myhome.ge, ss.ge, korter.ge, Facebook)
without touching a laptop at the viewing.

## How it works

```
📱 PHONE (Nino, at the viewing)          💻 DESKTOP (Claude, later)
─────────────────────────────           ─────────────────────────────
Airtable app → Tbilisi Home CRM         "process phone intake"
→ Phone Intake table → + New row        → creates Owner + Listing records
   • street + number                    → downloads photos into
   • Rent/Sale, price, district           ~/Documents/Tbilisi Home/Listings/
   • photos from camera roll            → drafts GE/EN/RU descriptions
   • dictate the rest into              → cross-posts via the existing
     "Details / Voice Notes"              listing skills (with approval
                                          before anything goes live)
```

The bridge is a new **Phone Intake** table in the **Tbilisi Home CRM** Airtable
base (`appe9jgw9ng4T0nEL`, table `tblENve9a48LQaVJK`) — already created and
live. New rows start at Status **📱 New from phone**; Claude's processing moves
them to **✅ Listed** and links the real Listings record, so the table doubles
as an audit trail of everything captured in the field.

## Phone setup (one time, ~3 minutes)

1. Install the **Airtable app** (iOS/Android) and sign in with the account that
   has the Tbilisi Home CRM.
2. Open **Tbilisi Home CRM → Phone Intake**. Tap ⭐ to favorite the base so it's
   on the app home screen.
3. Optional but recommended — an even faster entry form: on the desktop, open
   the Phone Intake table → **Forms** → create a form view with the fields in
   this order: Property, Deal Type, Price, District, Photos, Details / Voice
   Notes (everything else collapsed/optional) → **Share form** → open the link
   on the phone → *Add to Home Screen*. One tap from the home screen straight
   into a blank intake form. (Airtable's API can't create form views, which is
   why this step is manual.)

## Capturing a property (the 2-minute drill)

Required for publishing — everything else can wait:

- **Property** — street + number ("Atenis 16")
- **Deal Type** — Rent or Sale
- **Price**
- **District**
- **Photos** — straight from the camera roll; first photo = cover

Then dump everything else into **Details / Voice Notes** with dictation:
entrance and apartment number, floor, what the owner said about commission and
terms, the view, quirks. Claude sorts it into the right CRM fields — nothing
dictated is lost. Owner name + phone go in their own fields if known.

**Publish To** stays empty for the normal "everywhere" cross-post; pick specific
sites only when the owner restricts where it may appear.

## Processing (desktop)

Say **"process phone intake"** (or it runs as part of the gm/eod sweeps).
Claude then, per row:

1. Dedupes the owner by phone, creates/updates the **Owners** record.
2. Dedupes against existing **Listings** (street + district) so nothing is
   ever double-published.
3. Downloads the photos into the local Listings folder and creates the
   **Listings** record with Nino's title style.
4. Runs the cross-posting pipeline for the sites in **Publish To** (empty =
   all five). Every existing approval gate still applies — the live
   Publish/Post click is always Nino's.
5. Marks the row **✅ Listed** and links the Listing — or **Needs Info** with
   the exact question in **Claude Notes** if price/photos/district are missing,
   so Nino can answer from her phone.

Full mechanics, field-by-field mapping, and guardrails:
[`skills/phone-listing-intake/SKILL.md`](skills/phone-listing-intake/SKILL.md).
Install it by copying the `skills/phone-listing-intake/` folder into the skills
directory Claude uses on the Mac (`~/.claude/skills/`).

## Design choices

- **Airtable, not a new app** — the CRM is already the source of truth and the
  Airtable mobile app handles camera-roll photo upload natively, offline
  drafts included. No new logins, nothing to maintain.
- **Intake table separate from Listings** — a half-typed phone capture never
  pollutes the real Listings table that matching and the portals depend on;
  Claude promotes rows only when they're complete.
- **Select options mirror Listings exactly** (districts, Rent/Sale,
  languages), so promotion is a clean copy, never a translation.
- **Photos ride the Airtable record** to get from phone to Mac — no AirDrop,
  no WhatsApp-to-self. Claude files them into the same
  `~/Documents/Tbilisi Home/Listings/` folders the portal skills already use.
  (One quirk handled in the skill: Airtable attachment URLs expire ~2 hours
  after fetching, so photos are downloaded at the start of every processing
  run.)
- **The Telegram-bot Inbox stays for quick text notes** ("met Saber, wants
  340k"); Phone Intake is for the structured case where a property should
  become a listing — the difference is photos and fields.
