---
name: whatsapp-cold-outreach
description: >-
  Run Nino's fully autonomous WhatsApp cold-outreach bot for property owners on
  myhome.ge — end to end: discover owner listings, send approved Georgian first
  touches from her WhatsApp Business number via WhatsApp Web (Claude in Chrome),
  monitor and answer replies with the approved script branches, collect photos,
  publish the property on tbilisihome.ge, send the live link back to the owner,
  log everything in the Airtable Outreach Log, promote YES-converters to the
  client CRM, and keep the adaptive reply-timing scheduler armed. Use whenever
  Nino says to run outreach, start the daily batch, check outreach replies,
  process owner photos, or fulfil a client request ("I need 1 apartment...").
  Pairs with the tbilisi-home-listing skill for the site-publishing step.
---

# WhatsApp Cold Outreach Bot (myhome.ge owners)

Nino Chagunava runs Tbilisi Home (tbilisihome.ge), a brokerage for foreigners,
expats and international investors. This skill is the standing playbook for her
autonomous cold-outreach pipeline. She has explicitly authorized fully
autonomous operation: sending first touches, replying within the approved
branches, and running the photos → listing → link chain **without asking her
confirmation**. Anything outside the approved branches is HELD and escalated to
her instead.

## 1. Positioning — non-negotiable rules

- **Never use the word "agent"/"agency" (აგენტი/სააგენტო) in Georgian messages.**
  It is a dirty word in this market. Nino is the **founder of Tbilisi Home**,
  with her own website that generates buyer/renter traffic worldwide.
- Value pitch: listing on her site is **free** for the owner; she only earns on
  success — **sales: 3% of price. Rentals: 1 month's rent on a 12-month
  contract, ½ month on a 6-month contract.**
- Mirror the contact's language (Georgian default; English/Russian if they use it).
- Site contact line used in listings: WhatsApp / Viber / Telegram +995555789306.

## 2. Discovery on myhome.ge

URL schema (WebFetch works for discovery; phone reveal needs her logged-in
Chrome and a "Show number" click):

```
https://www.myhome.ge/en/real-estate/{rent|sale}/apartment/tbilisi/{district-slug}/
  ?owner_type=physical&deal_types={2=rent|1=sale}&real_estate_types=1
  &currency_id={1=USD|2=GEL}&CardView=1&cities=1&urbans={47=Saburtalo|38=Vake}
  &districts=4&price_from=&price_to=&page=N
```

Rules:
- Only cards with the **"Owner" badge** (skip "Agent").
- **Scan the description for opt-outs** — "არ ვთანამშრომლობ", "აგენტების
  გარეშე", "I don't work with agents" → skip AND log permanent DNC (by listing
  ID if the number was never revealed). ~50% of Saburtalo rental owners opt out.
- **Dedupe** against the Airtable Outreach Log by phone AND by seller (one owner
  often has several listings).
- Daily volume default: ~5 rentals + 5 sales per district at average 1–2-bedroom
  price points, districts/property type per Nino's daily instruction.

### Client-request funnel ("I need 1 apartment...")
When Nino gives a client brief, 1 needed unit = **cold outreach to at least
10** matching owner listings (≈5 will say yes → ≈3 viewings → 1 chosen).
Budget rule: if she gives only a max budget for a rental, assume min ≈ max −
$200.

Two client-request modes — confirm which one Nino wants:
- **Tenant-in-hand / viewing mode:** the pitch names a specific waiting tenant,
  the goal is a **viewing**, and you do NOT request photos or create a listing.
  Nino schedules the viewing herself. (Default for urgent "I have a tenant now".)
- **Client-sourced listing mode:** use the STANDARD listing pitch (free listing
  + success-fee), and on YES run the full photos → tbilisihome.ge listing → link
  chain, tagging every owner with the lead's name so Nino knows who it's for.
  Nino still schedules the actual showings herself. (This is what "find N
  listings and reach out for {lead}" means when she wants the places genuinely
  listed — e.g. the Laura Queen-Malcolm Didi Digomi campaign.)

## 3. Send mechanics (WhatsApp Web, Claude in Chrome)

- Prefilled URL: `https://web.whatsapp.com/send?phone=995XXXXXXXXX&text=<urlencoded>`
  → wait 15–18 s → **click the composer first** → press Return. If a chat shows
  "Draft:", open it, click composer, Return.
- Or open the chat and type into the composer directly (for replies).
- **Tag every outreach chat with the "Outreach" list** (header "Add to list" →
  Outreach) right after first contact. Reply-monitoring reads only this list.
- **Also tag every outreach chat with the LEAD's NAME as a WhatsApp list**, so
  Nino can see at a glance which client each contacted owner is being sourced
  for. Client-request campaigns use the buyer/renter's name (e.g. a "Laura"
  list, a "Tako" list — create the list on the first contact of that campaign,
  then add each subsequent owner to it). General inventory-building outreach
  that isn't tied to one client keeps just the "Outreach" tag. So a
  campaign owner ends up in TWO lists: Outreach + {Lead Name}.
- **Opening older chats:** WhatsApp Web's search box does not reliably surface
  older/among-many chats by number. To open a specific chat, navigate to
  `https://web.whatsapp.com/send?phone=995XXXXXXXXX` (opens it directly, no
  message needed). Verify the header number before acting.
- **Typing mechanics:** do NOT put `navigate` and the composer `type` in the
  same browser_batch — the composer eats the spaces and sends a spaceless blob.
  Navigate + wait in one call, then click composer + type in a SEPARATE call,
  screenshot to confirm spaces are present, then send. Long Georgian strings
  occasionally still drop spaces — always verify the composer render before
  sending, and if garbled, clear (cmd+a, Backspace) and retype.
- **Closing the list dropdown:** press Escape — do NOT click a blank area of the
  chat to dismiss it, because a stray click can land on a "call back" banner and
  trigger an outbound call dialog. (If a call dialog appears, click Cancel.)
- If a number "isn't on WhatsApp" — dismiss, log in Airtable for Nino to
  call/SMS manually.
- **Before replying in any chat, verify it is an outreach thread** (our first
  touch is visible in the thread). Chats where Nino herself has been messaging
  or calling are her personal conversations — never interject.
- No autonomous sends 00:00–08:30 (queue for 08:30). 09:00–22:00 normal pace.

## 4. Approved script branches (exact Georgian)

First touches (fill in listing specifics; sale/rental/CR variants follow the
same skeleton — rooms, district, price, "მე ნინო ვარ, Tbilisi Home-ის
დამფუძნებელი — ჩვენ უცხოელ [მყიდველებთან/დამქირავებლებთან], ექსპატებთან და
საერთაშორისო ინვესტორებთან ვმუშაობთ...", free listing offer, commission line,
"დაგაინტერესებდათ?").

**Every first touch MUST end with the owner's original listing link on its own
last line** — the exact myhome.ge (or ss.ge) URL the listing was discovered on,
the same URL logged in the Outreach Log's Listing URL field. No label or extra
text around it, just the bare URL as the final line of the message. This is for
Nino: when she calls an owner and they agree to list, she copies that link
straight from the chat and resends it as a new-listing request. Applies to ALL
first-touch variants (sale, rental, and both client-request modes).

Reply branches:
1. **YES → photo request:** "მშვენიერია! გამომიგზავნეთ ფოტოები (სასურველია ორიგინალები, ლოგოს გარეშე) და დღესვე განვათავსებ ჩვენს საიტზე — როგორც კი გამოქვეყნდება, ლინკს გამოგიგზავნით."
2. **Photos received → ack:** "მადლობა! ვამზადებ განცხადებას და ლინკს მალე გამოგიგზავნით."
3. **Listing live → link:** "აი ლინკიც — განცხადება უკვე ჩვენს საიტზეა: [URL] — როგორც კი მყიდველი/დამქირავებელი დაინტერესდება, მაშინვე მოგწერთ."
4. **CR YES → viewing ack:** "მადლობა! დამქირავებელს შევათანხმებ და ნახვის ზუსტ დროს მალე მოგწერთ." (then HOLD for Nino to schedule)
5. **NO → close:** "გასაგებია, ბოდიში შეწუხებისთვის და წარმატებებს გისურვებთ!" → Status "Replied - No", Conv State Closed, DNC.
6. Commission question → restate 3% / 1 month / ½ month, success-only.
7. Who are you → founder of Tbilisi Home, tbilisihome.ge, international traffic.
8. Has agent / exclusive → no conflict, listing with us is free and non-exclusive.
9. Already sold/rented → congratulate + close politely.
10. "Take photos from myhome" → myhome photos carry a watermark; ask for originals without logo.
11. How did you get my number → from their public myhome.ge listing.
12. Agency suspicion → not an agency-model pitch; own site, own clients, success fee only.
13. Voice note / phone call → neutral ack + ESCALATE to Nino.

**Discriminatory owner preferences (e.g. "no Indians", nationality/religion
restrictions) — do NOT escalate; handle silently and professionally.** Nino's
standing policy: respect the owner's stated preference without acknowledging,
endorsing, debating, or moralizing about it, and without digging into their
reasoning. Proceed with the listing/relationship normally; simply do not route
a client of the excluded group to that owner. Tbilisi Home itself never
discriminates on who it represents (race, gender, sex, orientation, disability,
etc.) — but it also doesn't lecture owners or pick fights over their prejudices.
Record the preference factually in the Airtable note (so matching quietly avoids
that group) with zero editorializing. Stay non-discriminatory, stay
professional, move on.

**Escalation (HOLD, never commit):** price negotiations, viewing scheduling
specifics beyond the ack, legal/contract questions, anything off-script.

## 5. Photo → filing chain (owner sends photos)

1. Open the chat, open the first photo in the media viewer.
2. Download via viewer **⋮ → Download**, **one photo at a time with ~4–5 s
   between downloads** — rapid batch clicks trigger Chrome's multiple-download
   block and only the first file lands. Verify the file count in ~/Downloads
   (device_list_dir) matches before moving on.
3. Rename to `{Street-Name-Number}-{n}.jpeg` (album order) and file into
   `~/Documents/Tbilisi Home/Listings/{Street-Name-Number}/`.
   - Preferred: device_bash (mv/cp on the Mac). If device_bash is down, fall
     back to: device_stage_files (Downloads → container) → rename in container
     → SendUserFile → device_commit_files to the Listings subfolder.
   - md5-dedupe before filing.
4. **Sweep the originals**: after the renamed copies are confirmed in Listings,
   move the WhatsApp originals from Downloads into `Downloads/_to_delete/`
   (device_bash `mv` within the same mount — deletes are not permitted, Nino
   empties that folder herself). Downloads should end each chain clean.
5. Send branch-2 ack.

## 6. Listing chain on tbilisihome.ge

Follow the **tbilisi-home-listing** skill (Houzez Create a Listing wizard) with
Nino's standing override: **submit WITHOUT asking her** (she ordered this step
to fire without her). Practical lessons:
- Close the Novamira "Notes Panel" if it pops up; it can swallow clicks.
- The floating "Ask AI" widget overlaps the Next/Submit buttons — if a
  coordinate click does nothing, use find/read_page and click the button ref.
- Text typed immediately after page load can be wiped by a re-render — verify
  with a screenshot; re-type via element refs if a field stayed empty.
- Media cap is 12 images; pick the best 12 (keep one building exterior). Star
  the first thumbnail as cover.
- Location: type the official Georgian street name, pick the autocomplete entry
  whose district matches, sanity-check the map pin.
- Details: Bedrooms/Bathrooms/Area (digits only); Floor goes in Additional
  details (Title "Floor", Value "8 / 16").
- Private Note: owner name, phone, source myhome listing ID, outreach date.
- After submit: open View Property, confirm live, then send branch-3 link to
  the owner.
- **Capture the site Property ID** (the number in the post-submit URL,
  `create-listing?edit_property=NNNNN`) — it goes into the Outreach Log's
  "Site Property ID" field (fldv5NRMfEN1yXXdn).
- **Send the listing to Nino's own WhatsApp** ("Message yourself" chat,
  +995 555 78 93 06) right after publishing, as ONE message (Shift+Enter
  between lines, Enter only at the end), in exactly this format so she can
  forward it straight to clients:

  ```
  For Rent / For Sale
  Price
  Street
  District
  # Bedroom / # Bathrooms
  # sqm
  Floor # / Total Floors
  Link
  ```

## 7. Airtable — Outreach Log (dedupe backbone + scheduler state)

Base **appxZgXiO0OliTQOJ** ("Tbilisi Home Database"), table **tblH9jrB24dAlzwWY**
("Outreach Log"). Fields: Phone fldEHmeegqSS8CWOD (primary/dedupe key), Owner
Name fldqlrXgb0DLhueJL, Listing URL fldR5TBMCzBu2ixlw, District fld2406oRB5SnvpK9,
Deal Type fldAdbUb5dPGqbexr, Rooms fldzioR3N2BZRRClx, Price fldpEl1bvw21jEOc0,
Currency fld6NBaOD3rAMlog3, Status fldho1ER4INCFBixs (Queued / Sent / Replied -
Interested / Photos Received / Listed on Site / Replied - No / Do Not Contact /
Sold Before Contact / Escalated to Nino / No Reply), First Contact
fldEBEzRJ8vrr7NS7, Last Activity fld5o7pnTpJjY7tNN, Reply Latency (min)
fldsoRiagUm9mZYhR, EWMA Latency fldbhjXAPxeN06QQF, Site Listing URL
fld2Ob6y2XbjdTKFv, Site Property ID fldv5NRMfEN1yXXdn (tbilisihome.ge post ID),
Notes fldKjIGnnte53z9ec, Conv State fldO2oI4W9eGxy2KQ
(Burst/Hot/Warm/Cooling/Dormant/Closed), Next Check At fldqy5TB1iYHbN0xB,
Replies Count fldcLa4Dmjyf82FZF. Update on every event; use typecast.

**CRM promotion (YES-converters only):** create a record in **Clients**
tbl81BStSwRPQ2Se2 — Name fldMYdyRjvgGShTc4, Phone fldDSAI4h5IWpS9J5, Lead Type
fld5vi9KQKiClqFyE (Seller/Lessor), Pipeline fld4xrqzbZdttrEyU, Lead Source
fldcbeQU4hclYBOJq = "MyHome.ge", Priority fldMXyESF420f1rAg, Notes
fldWZjUMWZPtXKIsc, Next Action fldYl7EcSEcHKia7M, Next Follow-Up
fldle5wEleutBjyjs. Non-converters stay only in the Outreach Log (numbers game).

## 8. Fluid Scheduler v3.2 (adaptive reply timing)

Per-contact EWMA latency = 0.5·previous + 0.5·latest observed; new contacts
start at the population median. States and check cadence:
- **Burst** (right after our outbound): +5/+12/+25/+45 min
- **Hot** (they replied recently): max(3, 0.5·EWMA) min
- **Warm**: EWMA, then ×1.6 backoff per silent check, cap 15 min
- **Cooling**: 15→60 min; **Dormant**: daily digest, "No Reply" after 3 days,
  one nudge only; **Closed**: never.
Time-of-day: 09:00–22:00 ×1; 22:00–24:00 ×2; 00:00–08:00 ≥60 min and **no
autonomous sends 00:00–08:30** (queue for 08:30).

Re-arm after every watch cycle with **send_later** at the earliest Next Check
At across open conversations (floor 3 min, cap 60). **Never use CronCreate /
local cron tools** — they die with the session. Persist all state in Airtable
so any wake can reconstruct the queue.

## 9. Safety rails

- Only approved branches are sent autonomously; everything else is held with a
  neutral ack and escalated to Nino (WhatsApp voice notes, calls, negotiations,
  legal questions). Discriminatory owner preferences are the exception — NOT
  escalated: respect them silently, proceed professionally, note them factually,
  never endorse or debate (see §4).
- DNC is permanent: opt-out phrases, "Replied - No", or Nino's instruction.
- Never message a chat that isn't a verified outreach thread.
- One nudge maximum for non-responders, then No Reply.
