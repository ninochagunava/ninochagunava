---
name: phone-listing-intake
description: >
  Process properties Nino captured on her phone into real, published listings.
  Trigger when Nino or Jeff says "process phone intake", "check phone intake",
  "anything new from my phone", "I added a property from my phone", or during the
  gm/eod rituals as a standard sweep. Reads rows from the Phone Intake table of the
  Tbilisi Home CRM (submitted via the Airtable mobile app or intake form), creates
  or updates the Owner and Listings records, downloads the photos into the local
  Listings folder, then hands off to the tbilisi-property-listing pipeline to
  cross-post (tbilisihome.ge, myhome.ge, ss.ge, korter.ge, Facebook). This skill
  does the CRM + photo plumbing; the per-site publishing skills do the portals.
---

# Phone Listing Intake — from a phone capture to a live listing

## The system in one paragraph

Nino is out at a viewing. On her phone she opens the **Phone Intake** table
(Airtable mobile app, Tbilisi Home CRM) and creates one row: street + number,
Rent/Sale, price, district, photos straight from the camera roll, and anything
else she can tap in or dictate into **Details / Voice Notes**. That's it — her
part takes two minutes. Later, at the desktop, Claude runs this skill: every row
with Status **📱 New from phone** becomes a proper Owner + Listings record, the
photos land in `~/Documents/Tbilisi Home/Listings/`, and the normal
cross-posting pipeline publishes the property everywhere (with Nino's approval
before anything goes live). The intake row is the capture; the Listings record
is the truth.

## Airtable coordinates

| Thing | ID |
|---|---|
| Base — Tbilisi Home CRM | `appe9jgw9ng4T0nEL` |
| Table — Phone Intake | `tblENve9a48LQaVJK` |
| Table — Listings | `tblqkPfAyl2zf5aAF` |
| Table — Owners | `tbl5gyr35eIyxUQ9u` |

Phone Intake fields (by ID):

| Field | ID | Maps to |
|---|---|---|
| Property (primary) | `fldAwH25yWMyhgVt2` | Listings **Title** (street + short descriptor added by Claude) |
| Photos | `fldpDOFuIMF0oMLRV` | Downloaded to the listing's photo folder |
| Deal Type | `fldqlvWi07hJ96Lb5` | Listings **Deal Type** (same choices: Rent / Sale) |
| Price | `fldEytCuQgrvjiVkg` | Listings **Price** |
| District | `fldTwOoj0STi5uQIl` | Listings **District** (identical 19 choices) |
| Rooms / Bedrooms / Bathrooms | `fldoDk3SzZtyvoaDa` / `fldpvwxq96b9hMmf1` / `fld4388YZzAX7WCqU` | Same-named Listings fields |
| SQM / Floor / Total Floors | `fld7OqzNO17Zc7glM` / `fldlVDE8u3XeXzNEC` / `fldWjM6ZQVfIQFOP5` | Same-named Listings fields |
| Features (multi-select) | `fldq2EXMJaQTCqAL8` | Listings checkboxes **Furnished / AC / Elevator / Balcony / Parking** |
| Condition | `fldpWyr8hNIYC8mOI` | Listings **Condition** |
| Available From | `fldhiE4HnktAmgL0P` | Listings **Available From** |
| Owner Name / Phone / Language | `fld05txxa4lIeRq3y` / `fldyonJlXA7DRnwYu` / `fldy4Vy0w069KZTwV` | Owners record (dedupe by phone first) |
| Commission Terms | `fldSCvpEBKEviVO7u` | Listings **Commission Terms** |
| Term Constraints | `fldlbxFMeHOIqF8QT` | Listings **Term Constraints** |
| Details / Voice Notes | `fldPYnSXnXd0WTZg9` | Parsed into structured fields; leftovers → Listings **Notes** |
| Publish To | `fldXzghC4SRleSIJw` | Which portals to publish (empty = **all** of them — the usual) |
| Status | `fldl7WpTRlkJzKzmu` | Intake pipeline state (see below) |
| Listing (link) | `fld0hINKD4A89EJMk` | Set to the created Listings record when processed |
| Claude Notes | `fldUyuQpfRwtGtpTx` | What Claude did / questions back to Nino |

Status choices: `📱 New from phone` → `Processing` → `✅ Listed`, with
`Needs Info` (blocked on a question) and `Discarded` (Nino changed her mind).

## Processing loop

Run this whenever triggered, and as a standard sweep inside gm/eod:

1. **Fetch work.** List Phone Intake rows where Status = `📱 New from phone`.
   Also re-check `Needs Info` rows — if Nino has since edited the row or
   answered in chat, resume them.
2. **Claim.** Set Status → `Processing` on the rows you're about to handle, so a
   second session doesn't double-process.
3. **Parse the dictation.** Read **Details / Voice Notes** and distribute its
   contents into the structured fields (entrance/apartment → the Listings
   address fields, "has a big balcony" → Balcony, "owner wants long-term" →
   Term Constraints, etc.). Whatever doesn't fit a field goes verbatim into the
   new Listing's **Notes** so nothing is lost.
4. **Dedupe before creating anything.**
   - **Owner:** search Owners by phone number (normalize +995 forms), then by
     name. Match → link it and only fill gaps; no match → create the Owner
     (Name, Phone, Language, Preferred Channel WhatsApp by default).
   - **Listing:** search Listings for the same street + district. If one
     already exists and is live, do NOT create a duplicate — update it if the
     intake row adds anything, link it, note "already listed" in Claude Notes,
     and mark the row `✅ Listed`.
5. **Photos.** Download every attachment from the Photos field into
   `~/Documents/Tbilisi Home/Listings/<street-name-and-number>/` (create the
   folder; keep Nino's usual folder-naming style — match how existing folders
   look before inventing a new pattern). Do this download EARLY in the run:
   Airtable attachment URLs expire about two hours after being fetched, so
   fetch the record and pull the files in the same sitting. Set the Listing's
   **Photos Folder** field to the folder name.
6. **Create the Listing.** Map fields per the table above. Title = street +
   short descriptor in Nino's house style (e.g. "Atenis 16 — 2-room, Vake,
   park view"). Status = `Photos Received` when photos came in, otherwise
   `Awaiting Photos`. Source = `Inbound` unless the notes say she sourced it
   for a client or via cold outreach. Link the Owner.
7. **Link back.** On the intake row set **Listing** to the new record and write
   a one-line summary in **Claude Notes** (what was created, where photos went).
8. **Publish.** Hand off to the **tbilisi-property-listing** skill (or the
   individual portal skills) using the freshly created Listings record and photo
   folder. Respect **Publish To**: empty means all five destinations
   (tbilisihome.ge, myhome.ge, ss.ge, korter.ge, Facebook Page + groups);
   otherwise only the selected ones. All of those skills' own approval gates
   still apply — Nino confirms before any paid or public Publish click.
9. **Close out.** Once live, set intake Status → `✅ Listed`, and fill the
   Listing's **Site URL** / **MyHome URL** as the portal skills report them.

### When something is missing

A row can only be published if it has, at minimum: Property (street), Deal
Type, Price, District, and at least one photo. Missing any of those →
Status `Needs Info`, write the exact question(s) in **Claude Notes**, and
surface it to Nino in chat (or the next gm docket) as a one-liner she can
answer from her phone: "Kakabadze 12 — what's the price, and which floor?"
Never guess a price, never publish without photos, never invent an owner
phone number.

## Guardrails

- **Never delete intake rows** — flip Status to `Discarded` instead. The table
  is the audit trail of what came in from the phone.
- **Approval before publish** stands exactly as in the portal skills: staging a
  listing is autonomous, the live Publish/Post click is Nino's call.
- **Photos expire:** re-fetch the record if more than ~2 hours passed between
  reading it and downloading attachments.
- **One property = one row.** If a row clearly describes two properties, ask
  rather than splitting it yourself.
- **This skill never runs on the phone side.** It needs the Mac (photo folder,
  Claude in Chrome for the portals). From the phone, Nino only captures.
