# IMG_1858: Applied Compute's $4.5B deal (FAST RPN pixel, "acquired" look)

Built with `/fast` on Nov 24, 2026, sister `img1843-rpn`. Source `~/Downloads/IMG_1858.MOV` (187 s, many count-ins and retakes); cut from the lossless clean copy `~/Movies/FCP/img1858-rpn-graphics/IMG_1858_clean.MOV`.

## Deliverables (`~/Movies/FCP/img1858-rpn-graphics/`)
`img1858_rpn.fcpxml` (FCPXML 1.14, DTD-valid, opened in Final Cut), `img1858_rpn_final.mp4` (74.3 s), `img1858_rpn.srt`, `title.mov` (lane 3 "Title"), `captions.mov` (lane 2), `run_*.mov` graphics (lane 1), `stills/` (1.0 s title still included), `img1858_matchcut_cuts.jpg`, `img1858_contact.jpg`, `img1858-rpn.cube`.

## Look
- Accent **signal orange `#FF5A1F`** (Applied Compute's and Palo Alto Networks' shared brand orange; new for the series).
- Seam: an acquisition merge, pixel chevrons marching right on a 2 px orange line, a pixel infinity loop (the AC mark) at the left. Canvas: ember black `#0E0907` with a low orange glow.
- Bed: "Computer Wiz" (Marten Moses, Epidemic) 15 LU under the voice; voice −14.0 LUFS, LRA 1.8. SFX: sister palette (gear tick on marks, weighted whoosh on new cards, burst touch singles + "Be Gentle").

## Opening title
Applied Compute mark + **"$4.5B STANFORD" / "DROPOUT"** (3 words), frame 0 → 3.6 s, above his head. Own layer: `title.mov`, lane 3, role "Title".

## Cut (word indices into edit/transcript.json)
| Out | Mode | Line |
|---|---|---|
| 0.0 | face | 62–84 "This 23-year-old Stanford dropout just closed the acquisition deal worth $4.5 billion for a company he started 18 months ago. How that happened?" (phone in hand: full face) |
| 3.6 | burst | on "acquisition": his head → Yash Patil → Nikesh Arora ×3 → his head (4 images × 5 frames) |
| 10.5 | split | 123–136 + 157–176 "Yash, Rhythm, and Linden … went to Stanford … worked at OpenAI … deadly combination" → **Linden Li's launch post** (marks: @ypatil125 @rhythmrg / left OpenAI / insanely talent-dense) |
| 24.6 | face | 182–210 third-party models → "combine infrastructure, data, compute … and sell it" |
| 32.7 | face | 263–269, 284–300 Cognition, Microsoft; "why not we optimize for you with your own data?" |
| 45.9 | full | 339–353 "And now Palo Alto Networks … by purchasing it" → **Yash Patil's Nov 18 post, full text, full screen** (marks: "signed a definitive agreement" on "And now", "acquired by Palo Alto Networks for $4.5B!" on "Palo Alto Networks is trying"; captions at y 1700) |
| 52.5 | face | 354–388 Fireworks hack and his read of the motive (no graphic) |
| 64.7 | split | 389–399 "one of the biggest exit offers" → **TBPN "ACQUIRED" post** (mark: "Palo Alto Networks agrees to acquire Applied Compute for $4.5B") |
| 68.0 | face | 400–403, 408–419 "Another cool Stanford story. What do you all think? Let me know in the comments below." |
| 71.3 | end | cheat sheet (deal, not closed, founders, $0 → $100M ARR, Fireworks context) |
Dropped: all "1, 2, 3, go" count-ins, the "closed an acquisition offer" retakes, the first founders take (cut off at "around the age of"), the DoorDash analogy (211–262), "trillion-dollar company" aside, "They took their data … promise they gave" (301–338), "What are you all-".

## Board items (`assets/board/`, from `applied board.excalidraw`)
Story order on the board: b00 deal post (Yash, Nov 18) · b04 Linden launch post (Oct 29, 2025) · b05 @appliedcompute launch post · b06 TBPN "ACQUIRED" (Nov 18) · b07 Yash launch post with team photo · b09 Yash "$100M run rate / $350M at $3.25B" (Nov 2) · b10 "nothing without its people" (Nov 19) · b08 "services businesses can scale like software" (Nov 22); b01–b03 are 140 px avatars.
**Used:** b04, b00, b06 as cards (b04 and b00 rebuilt with full text, see below); b06's thumbnail faces in the burst; the AC mark cut from b05 for the title and cheat sheet. Not used: b07, b08, b09, b10 (he never says ARR, the raise or the services line in the kept cut; the $100M ARR / $3.25B facts went to the cheat sheet).

## Fact-check
- **Deal:** Palo Alto Networks signed a definitive agreement on Nov 18, 2026 to acquire Applied Compute for $4.5B in stock, subject to adjustments; close expected in PANW fiscal Q3 2027 (quarter ending Apr 30, 2027), subject to approvals; Yash Patil to become Co-Chief AI Officer after close (PANW 8-K exhibit 99.2; SC Media, CSO Online, BankInfoSecurity).
- **FLAG "just closed the acquisition deal":** wrong, it's signed, not closed. Every take says "closed", so it stays in his words; the card he's over marks "signed a definitive agreement" and the cheat sheet says NOT CLOSED. Re-record "just signed a deal to be acquired" if he wants it exact.
- Founders: Yash Patil, Rhythm Garg, Linden Li, all ex-OpenAI (Linden's own post), Stanford (press). Captions use the right spellings (ASR heard "Riddhiman, Landon" in a dropped take).
- **FLAG "23-year-old Stanford dropout":** Yash's age 23 comes from Forbes Italy only; "dropout" is from press bios, not an official page. His own board says ages and "Stanford dropout" were not verified. Kept as his line, no graphic; the title uses "dropout" but no age.
- "18 months": company blog says <18 months after founding (Nov 2); Yash said "just over 18 months" (Nov 18). OK.
- Cognition and Microsoft as customers: named in Applied Compute's posts (board notes; Microsoft in the Nov 2 post). Not independently checked.
- Fireworks AI "just hacked": true, two incidents (detected Oct 6; second disclosed Nov 9, 2026; Unit 42 investigating per reports). **FLAG:** his reading that PANW bought Applied Compute *because* of Fireworks is his opinion; no graphic on it.
- "one of the biggest exit offers": reported as PANW's second-biggest deal ever (after CyberArk). OK as opinion.

## Timings
~9 min wall clock from setup to final render (setup+transcript, board extraction, fact-check, cut, cards, 2 renders).

## Not verified
- Watched frames only (contact sheet, match-cut sheet, stills), not the reel through with sound.
- The "story." end cut (END_AT 184.62) was set from the envelope, not by ear.
- Final Cut import not checked visually beyond opening it.

## Fix 1 (Nov 24, 2026, approved by Harnoor): posts shown whole
- The board screenshots of Linden's launch post and Yash's deal post stopped at "Show more", and X's embed truncates them the same way; headless Chrome can't render x.com and the syndication JSON was not used. Full text read from each post page on x.com (in-app browser, logged out) and rebuilt by `scripts/postcard.py`: real header cropped from the board screenshot, exact full text in SF Pro on the screenshot's own bg, date line, marks found by phrase. Attached media (Linden's quoted @appliedcompute post, Yash's logo image) left off, as before.
- Linden: still in the split, now 960 px wide with the whole text (marks: @ypatil125 @rhythmrg / left OpenAI / insanely talent-dense). Yash: four paragraphs, too long for the top half, so that beat is now full screen. TBPN's post was already whole (no change).
- Re-rendered, DTD OK, reopened in Final Cut. **Stale:** the first import ("IMG_1858 reel: Applied Compute $4.5B deal", opened ~19:23) still has the truncated cards and the split deal beat; delete it and keep the new one.
- Post stills: `stills/img1858_14.50.jpg`, `img1858_24.30.jpg` (Linden, all marks), `img1858_50.00.jpg` (Yash full screen), `img1858_67.90.jpg` (TBPN).

## Fix 2 (Nov 24, 2026, Harnoor): more visuals for infra / data / compute, plus founder photos
Beyond /fast's 2–4 cap, as asked. Title and burst unchanged; the opening (phone in hand) stays full face.
| Out | Was | Now |
|---|---|---|
| 10.6–14.1 | Linden post | **Founders**: Yash, Rhythm, Linden, each face hard-cut on his name, held as a row through "all three went to Stanford" (their own 400 px X profile photos, `assets/founders/SOURCES.md`; name under each, tag "PHOTOS: THEIR X PROFILES") |
| 14.1–24.6 | Linden post | Linden post (full text) cuts in on "all three worked at OpenAI"; marks names → left OpenAI → insanely talent-dense |
| 32.1–36.2 | face | **Infrastructure / data / compute**: hard cut on each word: server racks (Carl Lender, CC BY 2.0) → rack cabling at NERSC (Derrick Coetzee, CC0) → NVIDIA H100 boards (Geekerwan, CC BY 3.0, cropped) → all three side by side on "all together and sell it" (`assets/infra/SOURCES.json`) |
| 36.2–45.9 | face | **Yash's Nov 2 update post, full text** (rebuilt by postcard.py: the board shot stopped at "Show more"): marks "Cognition," and "Microsoft," on the names, "custom model training + production inference" on "why not we optimize for you" |
- Not added: Applied Compute's site (appliedcompute.com is blocked by the org's browser policy, so not captured another way); the Fireworks breach page (bleepingcomputer.com blocked too), so the Fireworks stretch stays face. Their long launch post is too long to show whole, so not used. No separate number card: the Nov 2 post carries the $100M / $3.25B with its source; the cheat sheet repeats them with logos.
- SFX trimmed to 12.1/min (founders cut silently on names). Re-rendered, DTD OK, reopened in Final Cut. **Stale imports:** the 19:23 and the Fix 1 (~21:57) imports; keep only the newest.
