# Ball AI — Workout Share Cards (v4c) — Cursor implementation prompt

**Branch:** Stay on the **same branch already used for this work** (typically `update/3.1.3` for the iOS share-card update). Do not cut a new branch from a different base. Do not retarget the PR. Use normal commits; never rebase or squash-merge.

**Deliverable:** Ship the v4c share-card look in-app (SwiftUI `ImageRenderer` → 540×960 story + 640×640 thumb JPEG). Concept-only mocks live in Drive; match those layouts.

**Concept pack (viewable):** https://drive.google.com/drive/folders/1eoNiTS9PgKRaNEhwR0xPV3sgXgerNrBb  
**Zip:** https://drive.google.com/file/d/1AUC1nPzPIFUEbzbFX1Rqchsg8e0Hgjnh/view  
**Contact sheet:** https://drive.google.com/file/d/1ExI-ilIay_tScl7YHezsSM9SZBAAJsVg/view

**CEO locks already in product:**
- No streak, XP, OVR, level, or profile on the card
- Open-photo Strava-style (photo visible top ~50–55%)
- Powered by Ball AI **bubble top-left, large** (52pt on story)
- Drill name **top-right** (small glass capsule)
- Real workout stats + shooting heat maps where applicable
- Bubble asset already on `main` via PR #371 (`PoweredBy` / PoweredByBallAI)

---

# v4c UPDATE: drill name moved top-right (CEO). Everything else = v4b.

# v4b UPDATE (CEO, Nov 3 2026) — overrides layout below
"These cards take too much space… the middle one [Infinite Handles] is the best because I can see shit." → ALL cards use Infinite-Handles density.
- Photo must be clearly visible in the top ~50–55% of the story card. All stats live in the bottom ~45%; no full-width panels above mid-card.
- **Powered by Ball AI bubble: TOP-LEFT, large** — 52pt tall on 540×960 (40pt on 640² thumb), 20pt inset. No footer branding.
- Drill title: small glass capsule (14pt bold caps + accent dot) **TOP-RIGHT** (v4c), 20pt inset, vertically centered on the Powered-by bubble; shrink font to fit if long.
- Shot drills: heat map is a **half-width (50%) glass inset bottom-left**; hero FG%/FINISH% (92pt) + 2 chips stacked to its right; one row of up to 4 compact chips (66pt tall) along the bottom.
- Dribbling: unchanged from v4 Infinite Handles — hero 170pt centered + 2×3 chips (104pt) at bottom.
- Rate my form/handles: one compact bottom glass card — overall (104pt) + "/10" + "POTENTIAL n" on the left, ProgressView bars (40pt rows) on the right.
- Glass a touch lighter than v4: tint #10141E @ ~40–47%.
Reference renders: pack-v4b `share/`, `thumb/`, `gen4b.py`, `manifest.json`.

---

**Public image refs (anyone can view — raw GitHub):**
- Contact sheet (all 37 stories): https://raw.githubusercontent.com/JulienrBourgeois/ball-ai-share-cards-v4c/master/contact-sheet-share-all37.jpg
- Contact sheet (thumbs): https://raw.githubusercontent.com/JulienrBourgeois/ball-ai-share-cards-v4c/master/contact-sheet-thumb-all37.jpg
- **Hero / match this:** Infinite Handles → https://raw.githubusercontent.com/JulienrBourgeois/ball-ai-share-cards-v4c/master/share/dribbling/bally-s-infinite-handles-share.jpg
- Handles with Gru → https://raw.githubusercontent.com/JulienrBourgeois/ball-ai-share-cards-v4c/master/share/dribbling/handleswithgru-share.jpg
- Rate My Form → https://raw.githubusercontent.com/JulienrBourgeois/ball-ai-share-cards-v4c/master/share/shooting/rate-my-form-share.jpg
- Infinite Shootaround → https://raw.githubusercontent.com/JulienrBourgeois/ball-ai-share-cards-v4c/master/share/shooting/bally-s-infinite-shootaround-share.jpg
- Infinite Finishing → https://raw.githubusercontent.com/JulienrBourgeois/ball-ai-share-cards-v4c/master/share/finishing/bally-s-infinite-finishing-share.jpg
- Full pack browse: https://github.com/JulienrBourgeois/ball-ai-share-cards-v4c
- Raw root: https://raw.githubusercontent.com/JulienrBourgeois/ball-ai-share-cards-v4c/master/
- Per-drill story path: `https://raw.githubusercontent.com/JulienrBourgeois/ball-ai-share-cards-v4c/master/share/<category>/<slug>-share.jpg`
- Per-drill thumb path: `https://raw.githubusercontent.com/JulienrBourgeois/ball-ai-share-cards-v4c/master/thumb/<category>/<slug>-thumb.jpg`


# Ball AI Workout Share Cards — v4 (Photo BG + Strava stats-sticker + SwiftUI glass)

Implement in SwiftUI (ImageRenderer → 540×960 story share; 640×640 square thumb, JPEG ~0.85).
Reference renders: this folder `share/<category>/*.jpg`, `thumb/…`, `manifest.json` (hero/tiles/background per drill), `gen4.py` (exact geometry).

## Hard rules (unchanged from v3)
- NEVER show streak, XP, OVR, level, avatar or profile on the card.
- Minimal copy: tiny drill-title pill, ONE big hero number + short accent label, short chip labels, Powered by Ball AI **bubble top-left large** (PoweredByBallAI / Image("PoweredBy") asset) — no footer mark.
- Numbers come straight from the finished workout (same mapping as v3 `spec()`):
  - Shooting / defense / athleticism with shots: hero FG% ; chips MAKES m/a, SCORE, MAX MULTI, 3PT% (or PAINT%), STEPS, GRADE/TIME (max 6).
  - Finishing: hero FINISH % ; same chips minus 3PT.
  - Dribbling: hero DRIBBLES ; chips SCORE, CLEAN %, BEST RUN, MAX MULTI, MOVES, TIME.
  - Rate my form / handles: overall /10 + dimension bars + POTENTIAL chip.
- Shot heat map from `shots[].courtLocation` (2000×1429 half-court px), 9 zones, cold→hot (blue→amber→red), zone % if ≥3 att, ● make / × miss pins.

## v4 visual direction (CEO)
1. **Background = real photo** (user's session photo/frame when available; else category stock: court, hoop at sunset, gym, athlete with ball). Aspect-fill, no heavy blur. Photo is the star (Strava/Nike Run Club/Whoop share feel, not a poster).
2. Scrim: top fade black 0→60% over top 22%; bottom LinearGradient clear→black ~88% starting ~36% height; soft radial vignette (~55%).
3. **Glass chrome = `.ultraThinMaterial`** look: background blur ~11pt, charcoal/navy tint `#10141E` @ 47–59%, white 20% hairline stroke, faint top sheen, soft drop shadow (black 40%, y+4, r 9).
   - Corner radii: chips 18pt, heat-map card 22pt, breakdown card 24pt, title pill capsule.
4. Layout (story):
   - Top: capsule pill (accent dot + drill title, 17pt bold caps).
   - Shot drills: hero 128pt Barlow Condensed Black (or SF Compressed Black) with soft shadow → frosted heat-map inset card (full width −24pt margins) with legend → 2×3 glass chips → footer bubble.
   - Dribbling: photo shows through top ~half; hero 170pt + label → 2×3 chips.
   - Breakdown: one glass card bottom-anchored: overall 150pt, "/10" label, ProgressView-style bars (7pt track white 16%, fill accent), POTENTIAL chip.
5. Accents: shooting #FF8A1F, dribbling #22D3EE, finishing #2DD4A7, defense #A855F7, athleticism #F43F5E. White text everywhere else.
6. Thumb 640²: heat card left 58% + hero/2 chips right + 4 chips bottom; dribbling = hero + 2×3 chips; breakdown = overall left, bars right inside one glass card.

## SwiftUI sketch
```swift
ZStack {
  Image(uiImage: bg).resizable().scaledToFill()
  LinearGradient(stops:[.init(color:.black.opacity(0.6),location:0),.init(color:.clear,location:0.22),
                        .init(color:.clear,location:0.36),.init(color:.black.opacity(0.88),location:0.9)],
                 startPoint:.top,endPoint:.bottom)
  VStack(spacing:14){ TitlePill(); Spacer(); HeroNumber(); CourtShotMap(shots).glassCard(22); ChipGrid(tiles); PoweredByBallAI() }
    .padding(24)
}.frame(width:540,height:960)
extension View { func glassCard(_ r:CGFloat)->some View {
  background(.ultraThinMaterial.opacity(0.9)).background(Color(hex:0x10141E).opacity(0.5))
  .clipShape(RoundedRectangle(cornerRadius:r,style:.continuous))
  .overlay(RoundedRectangle(cornerRadius:r,style:.continuous).stroke(.white.opacity(0.2),lineWidth:1))
  .shadow(color:.black.opacity(0.4),radius:9,y:4) } }
```
Note: ImageRenderer does not render live `Material` blur — pre-blur the BG crop behind each panel (CIGaussianBlur) or render via UIGraphicsImageRenderer of a hosted view snapshot.

## Photo credits (concept only, Wikimedia Commons; see bgs/CREDITS.txt). Replace with licensed / user photos before ship.
shooting-indoor | File:Amplus Basketball Court - October 2023.jpg
outdoor-dusk | File:The basketball court at dusk.jpg
hoop-sunset | File:2009-365-10 Sunset on the Hoop (3186039611).jpg
ball-hoop-sunset | File:Basketball going into a basketball hoop with sunset in background.jpg
athlete-playground | File:A Basketball player training on the playground.jpg
streetball | File:The Vladivostok Streetball Association DVIDS278601.jpg
court-portrait | File:Basketball court, Mid Street Recreation Ground, Nutfield, Surrey - May 2026 - 02.jpg
gym-portrait | File:Basketball Court at Jamia Millia Islamia Sports Complex 4.jpg
dribble-sidewalk | File:Boy dribbling a Basketball at a Sidewalk in downtown Taichung.jpg
