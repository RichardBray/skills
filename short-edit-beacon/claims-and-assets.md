# Claims and assets

## What a graphic may state

- Every number or statement on screen is checked at its source first. For
  Alexandria: dump the live page with the headless browser
  (`chrome-headless-shell --headless --virtual-time-budget=12000 --dump-dom <url>`)
  and read the counts (`/providers`: providers and tools; `/categories/jobs`:
  job providers and the "open roles" banner).
- Read a job posting in full before saying anything about it: years asked
  for, contract or permanent, "this is a pipeline, not an opening". If the
  spoken line contradicts the page (for example "you can apply right now"
  over a posting that is not an opening), say so in the report and propose
  cutting or re-recording the line. Do not edit the user's words.
- A claim the user records or asks to show that cannot be verified (a "100M
  data sources" figure): prefer a verified number. If the user still wants it,
  show it and flag it in the report.
- Check a take ends on its last word: the transcript can stop one short, so
  read the mic RMS after the last word (a quick wav check). A missing "it" is
  a re-record, not a caption.
- Never put a number from a different age, date or scope next to a photo
  (a 1984 portrait under "age 18"); label a photo's real age or change it.
- Recreated screens are labelled as recreations in the report, and show
  results that really came back.

## Photos, logos, documents

- Photos and logos from Wikimedia Commons: query the API with a descriptive
  user agent, read `LicenseShortName` (Public domain, CC0, CC BY...), keep the
  credit for the description. Avoid mugshots and anything unflattering.
  Direct downloads from CDNs that answer Access Denied are not worked around:
  use another source.
- Logos only from the vendor's own files or Commons; app icons from the iTunes
  Search API.
- Crop addresses and phone numbers off any document shown (a resume photo).
- Do not show unrelated or adult-industry employers in job lists; crop the
  list to start below them. LinkedIn only from the public guest pages, never
  behind a login.
- Real-page screenshots: `scripts/shot-clean.ts` (cookie walls dim the page
  otherwise). 400 CSS px wide.

## Generated B-roll

- Never generate a real, identifiable person in an invented scene. Use a
  generic stand-in ("a teenage programmer in a 1974 computer lab") and say it
  is one.
- `broll_add` over the section (region `[0, 0, 1080, 960]` in the halves
  layout), `broll_estimate`, then `broll_generate`. Seedance 2.5: about
  $0.22 per second, about 4 minutes for a 5 s clip.

## Firecrawl brand (graphics about Firecrawl)

Source: `~/fc/firebrain/packages/brand` (Alloy's brand package; Alloy Studio
itself is not needed). Video surface: Paper `#f9f9f9` page with Ash `#e0e0e0`
grid lines, heat orange `#fa5d19`, graphite `#262626`, Suisse Intl for text
(`assets/SuisseIntl-*.woff2`), Geist Mono for `[ BRACKET ]` labels,
logos in `assets/logos/` (`lockup-primary.svg`). No fades on motion graphics:
they cut in and pop in.
