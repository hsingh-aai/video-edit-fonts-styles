# IMG_0027 — hook B (A/B test)

**This folder is variant B of [../img0027-rpn](../img0027-rpn/project.md).** Everything below the hook is the same edit; only the opening changed (Nov 26, 2026, Harnoor: "A/B testing hook with no one is writing code, writing prompt, everyone is building software factories ... start with that hook instead and skip the potato one").

- **Cut:** the Lauren Tan (@poteto) intro (words 396–417) is gone. The reel opens on his own line, "Prompting is dead. Now everyone is creating software factories. What the hell are these?" (108–121, split), then "Episode 1 of Breaking Down Software Factories" (122–128, face, laptop in hand). Everything after moves up 7.77 s; the reel is 76.3 s + end card.
- **Top scene H (HyperFrames, 0–4.53 s):** the intro frame is a wall of five real YouTube thumbnails under "EVERYONE IS BUILDING", slamming in from frame 0, with Cursor's "Build your own Software Factory" last, on "dead", as the hero in the accent outline. On "everyone" the match-cut burst cuts to four of the people building software factories, faces pinned to his head; the hero pops again on "factories" and a "?" lands on "these?". (A first pass opened on struck-out WRITING CODE / WRITING PROMPTS cards; Harnoor swapped them for the thumbnails: more visual.)
- **Thumbnails (real, assets/thumbs, from i.ytimg.com):** SkoT4RkteSA "From AI Coding Agents to the Software Factory" (Factory AI, Arize Observe 2026); tGbjIvvYuHE "How to Build a Software Factory for AI Coding Agents" (Boundary); htM02KMNZnk "WF2026: Software Factories & Keynotes" (AI Engineer); iheWKg2Tkrk "Ship Production Software in Minutes, Not Months" (Eno Reyes, Factory, AI Engineer); rnDm57Py54A "Building your own software factory" (Eric Zakariasson, Cursor, AI Engineer Europe). Titles checked through YouTube oEmbed.
- **Burst:** Eric Zakariasson (Cursor), Eno Reyes (Factory), and the two Boundary hosts, 4 frames each. The face boxes come from Apple Vision on the thumbnails. The credit names the channels only, not the Boundary hosts (not checked).
- **Title:** "SOFTWARE FACTORIES" only, from frame 0 until the burst at 1.53 s. The `1/5` label and the 5 pips on the seam are gone (Harnoor: "Title should be Software Factories, remove 1 out of 5"); the cheat-sheet header is plain "SOFTWARE FACTORIES". The cheat sheet's PROOF row (Lauren Tan) is now "WHO: EVERYONE IS BUILDING ONE".
- **Delivery:** `~/Movies/FCP/img0027-rpn-b-graphics/`. Its FCP project is "IMG_0027 reel: Software Factories, ep. 1 — hook B (RPN pixel)". Version A is untouched.

---

# IMG_0027: Software Factories, step 1 of 5 (RPN pixel, "factory line" series)

Built Nov 25, 2026 with the `/fast` pipeline (sister `img1858-rpn`), plus the PR #16 rules on layers and HyperFrames charts. Harnoor asked to "pull latest from github and edit in best style possible". Source: `~/Downloads/IMG_0027.MOV` (206 s). The reel is cut from the lossless clean copy `~/Movies/FCP/img0027-rpn-graphics/IMG_0027_clean.MOV`.

## Source and style choice
- **Orientation:** ffprobe reports 1920×1080 HEVC at 120 fps, but the stream carries a display matrix with rotation −90°. So it's a **portrait iPhone selfie (1080×1920)**, not landscape, and needs no manual rotation: ffmpeg and FCP both honour the matrix. The FCPXML gives the camera its own 1080×1920, 1/120 s format (`rcam`).
- **Content:** a talking head, the opener of a series ("Episode 1 of Breaking Down Software Factories"). He holds up a laptop with a "cloud software factory" loop diagram in 2–52 s. The rest is face only, with Hindi count-ins and many retakes.
- **Style: RPN pixel (9:16 reel only).** It's the recent default for his talking-head explainers. The split top gives each abstract idea (loop, roles, definition) a built visual, and the series accent and seam make the "episode" feel. Warm & witty is the repo's catch-all default, but his last eight explainer reels are all RPN pixel. No 16:9 cut: the source is portrait.

## Deliverables (`~/Movies/FCP/img0027-rpn-graphics/`)
`img0027_rpn.fcpxml` (FCPXML 1.14, DTD-valid), `img0027_rpn_final.mp4`, `img0027_rpn.srt`, `title.mov` (lane 3 "Title"), `captions.mov` (lane 2), `run_*.mov` graphics (lane 1), `stills/`, `img0027_matchcut_cuts.jpg`, `img0027_contact.jpg`, `img0027-rpn.cube` (the sister's grade: same office, same painting), `blurfill_10.mov` (lane −3).
- Built visuals: `hf/index.html` (HyperFrames 0.8.148, 1080×960, frame index = reel time) → `renders/hf_scenes.mp4` → `renders/hf_frames/`. Rebuild: `npm run render -- -q high --crf 10 -o ../renders/hf_scenes.mp4` in `hf/`, re-extract the frames, then `run.sh img0027-rpn`.
- **Blur fill (new in this pipeline):** on piece 10 ("plus different code review agents") he leans right, and the chin cap stops the zoom before he's centred (a 94 px strip would be open). `finish.py` now centres him anyway and puts a blurred, darker copy of the piece on lane −3 (`blurfill_NN.mov`), in both the preview and the FCPXML, instead of stopping.

## Series spec: Software Factories (5 steps). Reuse as-is for steps 2–5
Harnoor, Nov 25, 2026: "it's going to be 5 step series" and "do fast best visuals". Every step is a `/fast` reel built from **this project as the sister** (`new_reel.py <MOV> --sister img0027-rpn`). Keep everything below; change only what "Per episode" lists.

**Fixed for all 5 (don't change):**
- **Accent** conveyor yellow `#F5E14A`; canvas graphite `#0C0C09`, dot `(34,34,24)`, card `(30,30,22)`, line `(78,76,52)`, glow `(92,80,10)` (`kit.py`).
- **Seam** (`kit.diff_seam`): conveyor belt, a pixel gear at the left, crates riding right, and at the right **5 progress pips**: steps up to this one filled yellow, the rest outlined.
- **Type:** Pixelify Sans caps for words, VT323 for numbers, tags and the part label.
- **Title** (lane 3 "Title", `title.mov`, frame 0 → burst, on the seam of the split open): line 1 = part label `N/5` in VT323 yellow + "SOFTWARE"; line 2 = "FACTORIES" in huge Pixelify Bold. The series name stays the hook. If an episode needs its own hook, swap line 2's word only, max 5 words in all.
- **End card:** cheat sheet titled `SOFTWARE FACTORIES // N OF 5`, five rows (term / loop / roles / key / proof style), the pip seam at the bottom.
- **HF scene look** (`hf/index.html` CSS): dark cards with a 3 px `--line` border that turns yellow (`.live`) on the word; heads 56 px Pixelify; source tag VT323 30 px at y 852; logos are Simple Icons drawn white via `invert(1)`, **blurred until named** (keep `invert(1)` inside the blur tween).
- **SFX kit (Ocular):** tick = `MECHGear_SINGULAR-Small Gears 10` (Mechanica) on named things and marks, −15 dBFS peak; swell = `DSGNWhsh_WHOOSH-Weight` (Foundation) on section changes, −10; burst = touchscreen singles 01/09/02 (Utility) on each cut + "Be Gentle" (Foundation). Cap ≤16 ticks and ≤4 swells a minute.
- **Bed:** "Problem Solver" (Auxjack, Epidemic, `~/Music/documentary es/`), 15 LU under the voice; voice −14 LUFS. The same track on every step is the series' sonic signature.
- **Burst** on the opener: the computing pioneers chain (`assets/burst/`, public domain), landing on his head. Reuse it, or swap in a step-specific chain of 6 if the topic has one (e.g. the people he names).
- **Split framing (Harnoor, Nov 25 2026: "you cropped too much on my face. That should not happen."; rule in style repo PR #23):** `layout.py` split mode uses `s = min(centring need, 670 / (chin - top))`, with **no 1.0 floor** and `SEAM_HEAD = 975`. His head (hair to chin) is about 670 px, ~70% of the lower half, with the collar and shoulders in frame. Side strips get the **lane −3 blur fill** (`blurfill_NN.mov`, a blurred, darker copy of the same piece), **never a zoom-in**. His FCP fix went from 1.0651 to 0.925 scale; the rule gives 0.84–0.99 per piece (about 40–100 px uncovered per side). Face pieces are unchanged.
- **Grade:** `img0027-rpn.cube`. **Camera:** iPhone 120 fps portrait (rotation tag) → the `rcam` 1/120 s format in `finish.py`; blur fill on lane −3 when a split piece can't be centred.
- **CTA:** end on his "follow for step N+1" line, full face.

**Per episode (the only edits):**
1. `kit.py` → `EP = N` (fills the pips, the title's `N/5` and the cheat sheet's `N OF 5`).
2. `cut.py` → `REELS` (drop count-ins, retakes and production notes).
3. **2–4 visuals** (/fast): real full pages or posts for proof (`assets.py`), HyperFrames scenes for data, lists and diagrams (`hf/index.html`, frame index = reel time), faces and logos when he names them.
4. `build.py` → `beats_main()`, `SFX`, `CHEAT` rows; `TITLE` stays.
5. `project.md`: the cut, fact-check flags, names with sources.

**Step 1 (this reel):** what a software factory is, the definition (Zach Lloyd, Warp), the agent review loop, the two new roles, verification. He says "follow for episode 2".

## Look
- Accent **conveyor yellow `#F5E14A`**, new for the series. Canvas graphite `#0C0C09` with a low yellow glow.
- Seam: a conveyor belt (2 px yellow belt on pixel rollers, pixel crates riding right, one in four lit) with a pixel gear at the left.
- Bed: "Problem Solver" (Auxjack, Epidemic, `~/Music/documentary es/`), 15 LU under the voice. Voice −14 LUFS.
- SFX: the sister palette (Ocular Mechanica small gear tick on named things, Foundation "Weight" whoosh on section changes), plus the match-cut burst set (touchscreen singles and "Be Gentle").

## Opening
- **Title:** "1/5 SOFTWARE / FACTORIES" (3 words + part label) on the seam from frame 0 to the burst (1.73 s). Own layer: `title.mov`, lane 3, role "Title". Seam captions stay off while it's up.
- **Hook:** his own instruction in the take ("I think we should put this in intro … first watch this, this is Potato") puts the Lauren Tan line first.
- **Match-cut burst** on "thousands" (1.73–2.53 s): his head → Ada Lovelace → Alan Turing → Grace Hopper → Dorothy Vaughan → Katherine Johnson → Margaret Hamilton (beside her printed code stack) → his head, at 4 frames each. It reads as "from code by hand to factories". All six are public domain on Wikimedia Commons (`assets/burst/SOURCES.json`), credited on a chip.

## Cut (word indices into edit/transcript.json)
| Out | Mode | Line | Visual |
|---|---|---|---|
| 0.0 | split | 396–417 "This is Poteto. She merged thousands of PRs, which was unimaginable, in one month. And that happened with software factory as well." | HF scene L: Lauren Tan, her GitHub avatar, @POTETO, ENGINEER, SPACEXAI; a PR grid fills by "month", then "THOUSANDS OF PRS IN 1 MONTH" |
| 7.8 | face | 108–128 "Prompting is dead … Episode 1 of Breaking Down Software Factories." | laptop in hand → full face |
| 14.9 | face | 418–438 "We have evolved … then prompting Claude … loops of software factories." | face (series update: /fast keeps 4 visuals; the evolution timeline scene was cut) |
| 22.5 | split | 156–183 minus 163–166 (restart) and 172–173 ("still code") "And now, Software Factory, the definition states that it is a code-defined, closed-loop system for continuously measuring and improving cloud coding agents." | real page: AI Engineer's write-up of Zach Lloyd's talk (title, byline, definition); marks on "code-defined, closed-loop system" and "measuring and improving cloud coding agents" |
| 34.3 | split | 184–208 "Think of this way: … goes to GitHub … feedback from now agents instead of humans." | HF scene P: loop ring. YOU WRITE CODE → GitHub (blurred until named) → HUMAN REVIEW crossed out → REVIEW AGENTS |
| 42.0 | split | 244–268 "the whole feedback can be improved by one coding agent plus different code review agents all together in one system. And that's what you build." | same ring closes; CODING AGENT; dot runs the loop; ALL IN ONE SYSTEM → YOU BUILD THE FACTORY |
| 52.0 | split | 283–328 "now there are two job roles … product engineer … factory engineering … loop is working well." | HF scene R: 2 NEW JOB ROLES, 01 PRODUCT ENGINEER, 02 FACTORY ENGINEER (NEW), credited to Zach Lloyd / Warp's "Becoming a factory engineer" |
| 67.3 | face | 329–352 "And you know what comes there? Verification … merge even thousands of PRs a day." | face |
| 76.1 | face | 372–380 "And that's what we can do with software factories." | face |
| 79.1 | face | 474–480 "now follow for episode 2 coming soon." | face |
| 81.6 | end | cheat sheet: the term, the loop, new roles, the key (verification), proof (with the reported range) | Warp and GitHub logos |

Dropped: all Hindi count-ins and chatter (0–25 s); the first four hook takes; the take-1 evolution ("writing loops, which Peter Steinberger and Boris Cherny coined", see flags); "still code"; the "self-sustaining-" restarts (209–243); the "two categories" / "and now, and now" stumbles (269–282); the "20,000 PRs at SpaceX" take (353–371, see flags); the "put this in intro" / "put my footage from before" production notes (381–395, 439–473).
Word ends: every cut ≥120 ms past the word end, then on to a quiet point. Exceptions: "factories." at 21.67 s is cut in the energy valley, because "Now" follows 30 ms later. END_AT puts "day." at 145.60 (199 ms tail).

## Names (checked)
- **Lauren Tan (@poteto):** a SpaceXAI engineer, formerly on React core at Meta. He says "Potato"; ASR heard "Potato"; captions use her handle **POTETO**. Sources: her AI Engineer Code Summit talk "All Code Is Slop (Except Mine)" (Nov 2026, write-ups on moderncreator.app and xiaohu.ai) and github.com/poteto. Avatar from her own GitHub profile (an illustration, not a photo).
- **Zach Lloyd:** founder and CEO of Warp (ai.engineer/code/2026/talks/zach-lloyd; warp.dev blog).
- Claude (Anthropic) and GitHub: logos from Simple Icons (CC0), drawn white.

## Fact-check
- **Definition: OK.** "A code-defined, closed-loop system for measuring and improving cloud coding agents" is Zach Lloyd's definition at the AI Engineer Code Summit (Nov 12, 2026, at 1:04:38), per AI Engineer's write-up, which is the card shown. He adds "continuously", which matches Warp's own framing ("continuously improving") on warp.dev. **He doesn't name Lloyd or Warp**, so the card's byline and the cheat sheet credit him.
- **"Factory engineer" role: OK.** Lloyd's talk is titled "Software Engineering Is Becoming Factory Engineering", and Warp has a post "Becoming a factory engineer" (Nov 19, 2026). "Product engineer" as the other role is Harnoor's framing; no source was checked.
- **FLAG "She merged 20,000 PRs last month at SpaceX" (dropped take):** no source found for 20,000. Reports on Lauren Tan say about 1,000, 2,500 and 3,127 PRs a month (her team: ~11,000 a month). The kept take says "thousands of PRs … in one month", which fits the reports. The card says "THOUSANDS" and tags "REPORTED 1,000–3,127 PRS A MONTH". All of these are secondary sources (X posts, blogs), not her own numbers.
- **FLAG "merge even thousands of PRs a day" (kept, face, no graphic):** no one cited merges thousands a day; the reported numbers are thousands a *month*. It's said as what the loop makes possible, so it stays in his words with no graphic. Re-record as "thousands of PRs a month" if he wants it exact.
- **FLAG "loops, which Peter Steinberger and Boris Cherny coined" (dropped take):** they popularised "design loops, don't prompt" in June 2026 (Steinberger's post; Cherny: "my job is to write loops"), but loops predate them (Geoffrey Huntley's "Ralph" loops), and Addy Osmani named "loop engineering". The kept take (418–438) says the same arc without the attribution.
- **"Episode 1"** and "follow for episode 2": his series. Nothing to check.

## Fixes during the build
- The HF logos went black: the blur-to-sharp tween replaced the `invert(1)` filter. The tween now carries `invert(1) blur(…)`.
- The roles scene had 0.6 s of empty floor before "two": the header now lands at the start of the run, and the 2 pops on the word.

## Series update (Nov 25, 2026, Harnoor via the coordinating session)
- Made it step 1 of 5: `EP, N_EP` in `kit.py`, the part label in the title, pips on the seam, `N OF 5` on the cheat sheet, and the spec above.
- /fast trim to **4 visuals**: Lauren Tan (thousands of PRs), the real definition page, the agent loop (GitHub), the two roles. The evolution timeline (Claude logo) was cut; that line is now full face. HF scene E was removed from `hf/index.html` and re-rendered.

## Framing fix (Nov 25, 2026, Harnoor)
- He fixed the split crop in FCP and exported `~/Movies/FCP Exported/IMG_0027 reel: Software Factories, ep. 1 (RPN pixel).fcpxmld`: every split clip went from scale 1.0651, position (−1.83, −46.90) to 0.925376, (0.179, −37.39). Left untouched. That export predates the series update ("EP.1" title, evolution scene still split, no blur fills); its spine in/out/offsets match this build exactly (same cut).
- `layout.py` now reproduces his framing per piece (above). The rebuild puts the blur fill under all 10 split clips (`blurfill_00`, `04`–`12`) and keeps the series changes. Re-rendered, DTD OK, reopened in FCP as a new project.

## Timings
About 16 min wall clock: setup, transcript, fact-check, captures, the burst fetch, 4 HF scenes (2 renders), 3 pipeline runs.

## Not verified
- Watched frames only (contact sheet, match-cut sheet, stills), not the reel through with sound.
- FCP import checked only by opening it.
