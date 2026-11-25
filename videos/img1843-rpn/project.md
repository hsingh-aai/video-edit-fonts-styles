# img1843-rpn: token budgets per engineer (FAST RPN pixel, new "token budget" look)

Source `~/Downloads/IMG_1843.MOV` (91 s, retake-heavy). Cut from `~/Movies/FCP/img1843-rpn-graphics/IMG_1843_clean.MOV`.
Final 43.0 s (40.5 s speech + 2.5 s cheat sheet). Built Nov 24, 2026 with `/fast`, sister img1827-rpn.

## Look
- Accent **mint #3DF5A0** (new). Canvas deep green-black #070E0B, mint glow.
- Seam: "token meter": pixel coin stacks of varying height on a 2 px mint line, pixel `$` at the left.
- Bed: ES "Payday" (Jon Bjork), 15 LU under the voice. Voice −14.0 LUFS, LRA 1.7.
- Not the IMG_1805 series look: the topic is token budgets across companies; Jensen is only the hook.

## Opening title (new rule)
- "**$250K IN / TOKENS**" with the white NVIDIA logo on line 1 (3 words + logo). Pixelify Bold for TOKENS, VT323 mint for $250K.
- On screen from frame 0 (slides in, settled by ~frame 12) until the burst at 3.53 s. Placed above his head; captions stay low (y 1500), so no clash.
- Own layer: `title.mov` (ProRes 4444 alpha, 106 frames) on **lane 3**, clip name "Title: $250K IN TOKENS", role "Title".

## Cut
| # | mode | words | line |
|---|---|---|---|
| 1 | face | 83–108 | "Engineers should get $250,000 in tokens. That's what Jensen Huang said. But let's talk about … Fortune 500." (title + burst) |
| 2 | split | 113–139 | Tesla $800 … Microsoft $10,000 (chart, columns marked as named) |
| 3 | face | 140–150 | "But Nvidia, I'm gonna come back to it in a second." |
| 4 | split | 157–172 | no-limit list (Anthropic … Cognition marked), then "But Nvidia, max 50,000 tokens" (NVIDIA $35,000–$50,000 marked) |
| 5 | face | 182–193 | "How much tokens you get? Let me know in the comments below." |

Dropped: all count-ins and the retakes before word 83; "Max $200 per month" (109–112); Disney "up to $50,000" (151–156); "So Jensen's promise is not fulfilled at Nvidia yet" (173–181). See flags.

## Burst
Six Jensen Huang photos from img1805 (Anders Eidesvik, Commons, CC BY 4.0, credited on frame), 4 frames each, B0 = 3.53 s on "Jensen", inside face piece 1 → out at 4.33 s back on the same head. Moved from ~2 s to 3.5 s so the title owns the opening and the burst lands on the name. Match-cut sheet: all rows on the ring.

## Visuals (2 + title + burst)
1. The Information chart, top crop (headline + bars + logos): Tesla, Uber, Atlassian, Rippling, Apple, Microsoft columns marked on the names. Tag "THE INFORMATION · TOKEN BUDGET PER ENGINEER, MONTHLY".
2. The Information chart, lower crop: NVIDIA/Disney labels + "Companies with no limit set" grid; six no-limit cells marked as named, then NVIDIA's $35,000–$50,000.
3. Cheat sheet: $250K/yr bar, NVIDIA $35–50K/mo, big tech, no limit, the range.

## Fact-check (chart = The Information; Jensen = All-In podcast at GTC 2026)
- Jensen: he'd be "deeply alarmed" if a $500K engineer didn't consume $250K of tokens **a year** (Tom's Hardware, AOL/BI coverage). Kept line says "$250,000 in tokens" ✓.
- Tesla $800 ✓, Uber $2,000 ✓, Atlassian $2,000 ✓, Rippling $2,000 ✓, Apple $4,000 ✓, Microsoft $10,000 ✓ (all per month).
- Unlimited: Anthropic, OpenAI, Snowflake, Oracle, Replit, Cognition ✓ (all in the chart's no-limit list).
- **FLAG, dropped:** "Max $200 per month": no company at $200; lowest is Workday $100–$300.
- **FLAG, dropped:** "Disney, up to $50,000": chart says $50–$25,000.
- **FLAG, kept with chart:** "Nvidia, max 50,000 tokens": the chart says **dollars**, $35,000–$50,000 a month. Caption reads what he said; the marked chart shows $.
- **FLAG, dropped:** "Jensen's promise is not fulfilled at Nvidia yet": $35–50K/month = $420–600K a year, *above* Jensen's $250K a year. The payoff is backwards. Suggest re-recording a closer (e.g. "Nvidia already pays up to $600K a year in tokens").

## Timings
Setup + transcript 17:23 → FCP open 17:29 (plus ~2 min reading before setup). Single render pass, no fixes needed.

## Not verified
- Didn't watch the MP4 through in real time; checked the contact sheet (22 frames), the match-cut sheet and the 1.0 s still.
- Not confirmed in the FCP UI that the "Title" role imports cleanly (DTD-valid; `role` is allowed on `<video>`).
- The Information article itself wasn't opened (paywalled); the numbers come from the chart Harnoor attached.

## Own charts in place of the screenshots (HyperFrames, Nov 24 2026)
Harnoor: "try creating your own visuals rather than screenshots" + "blur the logos that are not talked about and slowly reveal".
- `hf/index.html` (HyperFrames 0.8.148, 1080x960, the reel's floor + mint + Pixelify/VT323) renders `renders/hf_charts.mp4`; `build.py` reads its frames (`renders/hf_frames/`, scene A = 0-413, scene B = 414-749) for the two split runs. Rebuild: `npm run render -- -q high --crf 10 -o ../renders/hf_charts.mp4` in `hf/`, re-extract frames, then `run.sh`.
- Scene A, bars (9.77-23.57 s): Workday $100-300 · Tesla $800 · Uber $2K · Atlassian $2K · Rippling $2K · Autodesk $2.5K · Apple $4K · Microsoft $10K. Everything sits blurred from frame 0; each named company sharpens on its word and its bar grows with a count-up. Workday and Autodesk are never named, so they stay blurred.
- Scene B, no-limit grid (26.53-37.73 s): all 11 no-limit companies are tiles. The six he names (Anthropic, OpenAI, Snowflake, Oracle, Replit, Cognition) sharpen with a mint border on the word; AWS, Blackstone, HubSpot, Meta and Palantir stay blurred. "∞ UNLIMITED" stamps on "unlimited", then the grid steps back and NVIDIA takes the frame with "$50K, MAX A MONTH · RANGE $35-50K" on "50,000". That shows the chart's dollars, not his "tokens" (still flagged).
- Logos: Simple Icons 13.21.0 (CC0), drawn white (`hf/assets/logos/SOURCES.md`). The Microsoft squares are CSS; Rippling, Workday, Blackstone and Cognition are text.
