---
name: fast-rpn
description: Harnoor's FAST RPN-pixel reel workflow, a finished 9:16 reel in about 12 minutes. It reuses the newest sister reel's pipeline, adds a match-cut burst at ~2 s and 2–4 key visuals at most (the source page that proves the claim, plus a number or logo card), and keeps everything else full face with captions. Use when Harnoor types "/fast <video>", or asks for a "quick RPN", "fast RPN", "do it fast" or "fast reel" edit of a talking-head clip.
---

# /fast: quick RPN-pixel reel

The first build was IMG_1805, "Jensen Huang is back as Nvidia CEO" (Nov 23, 2026): **11.5 min** from start to a DTD-valid FCPXML opened in Final Cut. The reference project is `video-edit-fonts-styles/videos/img1805-rpn/` (`project.md` has the cut, the fact-check and the timings).

This skill covers **speed and scope only**. For the look, read the repo's `rpn-style` skill (RPN pixel variant section). For the burst, read `match-cut-intro` (on `origin/main`: `git show origin/main:.claude/skills/match-cut-intro/SKILL.md`, no pull). Don't restate their rules here.

## Stage order (with IMG_1805 times)

| # | Stage | Time | How |
|---|---|---|---|
| 1 | Set up + transcript | 0:40 | `~/.cache/fast-rpn/venv/bin/python ~/.claude/skills/fast/kit/new_reel.py <MOV> [--sister img1827-rpn]`. This copies the scripts, extracts audio, runs AssemblyAI, and prints indexed words plus a frame strip (`edit/strip.png`). |
| 2 | Quick fact-check, **main claim only** | 1:00 | 2–4 `WebSearch` calls in one turn. Find the primary source (company release, filing, official page) and flag the rest. Don't research deeply. |
| 3 | Fetch assets **in parallel** | 1:00 | Run in one Bash call with `&` + `wait`: the source-page capture (headless Chrome) and the burst images (Commons API, recipe below). |
| 4 | Look at the frame strip, plan beats | 1:45 | Object in hand = full face. Pick 2–4 visuals. Everything else is face. |
| 5 | Edit 5 config spots (next section) | 1:45 | — |
| 6 | Test stills | 0:20 | `build.py main stills 2.5 5 20 …`: look at the sheet once. |
| 7 | Render, audio, FCPXML, stills, DTD check, open FCP | ~1:30 | `~/.claude/skills/fast/kit/run.sh <slug> [still times]`. Set `NO_OPEN=1` while iterating so FCP doesn't import duplicates; open once at the end. |
| 8 | Review contact sheet + match-cut sheet, fix, rerun 7 | ~2:50 | Read `img<N>_contact.jpg` and `img<N>_matchcut_cuts.jpg`. |
| 9 | Notes | 1:00 | `videos/<slug>/project.md` (cut, visuals, fact-check flags, timings, not verified). |

## What to change after copying the sister scripts (and nothing else)

`new_reel.py` copies `transcribe cut layout faces kit build finish audio assets stills` from the sister reel (default `img1827-rpn`: the leanest one, no `drawn.py`, and it has the burst cover fill and the face-mode layout fix) and renames the IMG ids. Then edit:
1. **`cut.py` → `REELS`**: `(src, first_word, last_word, mode)` with modes `split` / `face` / `full`. Use `SKIP` for stumbles inside a range. Drop count-ins and retakes.
2. **`kit.py`**: a **new accent** (unless Harnoor asks for "the previous X video style": then keep the sister's accent, seam, LUT and SFX untouched so it reads as a series, as IMG_1827 did) (used so far: amber, cyan, lilac, red, clay, magenta, lime, boot blue `#6F8CFF`), the canvas tint (`GRAPH/BOX/DOT` + the glow RGB in `floor`), and `diff_seam` (a seam motif tied to the topic, drawn in ~10 lines).
3. **`assets.py` → `PNG`**: the page crop box + marker rects in raw capture px. To measure them, draw a 100 px grid, show the image at half size and **double the displayed coordinates**. Check by eye whether the mark lands on the right words.
4. **`build.py`**: `PORTRAITS` (file, Vision face box), `BU` credit, `B0`, `beats_main()` (2–4 entries: `page(...)`, a number card, a logo card), `CHEAT` rows. Set `SIGN = []` unless you want the big-word sign-off.
5. **`audio.py` → `BED`**: one track from `~/Music/documentary es/`, chosen to fit the story (IMG_1805: "1 Up" for a comeback).

`layout.py` (face centring, hair under the seam) and `finish.py` (FCPXML) need no edits. (From img1805 or older sisters: if `finish.py` stops with "needs a blurred backdrop" on a **face** piece, the head sits high in the source; in `layout.py` face mode use `oy = min(0.0, FACE_HEAD - s * top)`.) Set `FULL_HEAD = {}` unless he's turning to the camera.

## Minimal-visuals rule
- **Match-cut burst at ~2 s** (6–8 images × 4 frames). Put it **inside one camera piece**, so it cuts out of and back into the *same* head. If the burst straddles a face→split change, the first or last cut won't match (IMG_1805, first pass). `build.py` splits the face run around the burst automatically.
- **2–4 key visuals:** the one page or post that proves the main claim (reuse it for a second marked line with `co=True` for the magnified callout), plus a number card where a stat lands and/or a logo card where a name lands.
- **Everything else is full face with captions.** No custom drawn diagrams. Unverified claims get no graphic.

## Parallel asset fetch (match cuts)
```python
# Commons: query licences + 1280 px thumbs in ONE API call, then download with 2 workers + retry (8 workers -> HTTP 429)
q = 'https://commons.wikimedia.org/w/api.php?' + urlencode(dict(action='query', generator='search', gsrsearch='<subject>',
    gsrnamespace=6, gsrlimit=50, prop='imageinfo', iiprop='url|extmetadata|size', iiurlwidth=1280,
    iiextmetadatafilter='LicenseShortName|Artist', format='json'))
# keep LicenseShortName in {Public domain, PD-*, CC0, CC BY x.x}; drop CC BY-SA; credit CC BY authors on the chip
```
- Prefer public domain, then official logos (reuse `videos/*/assets/logos/`, see their `SOURCES.md`), then CC BY with credit. Use a generic User-Agent, never Harnoor's email.
- Face boxes: `~/.cache/fast-rpn/faces_all <files…>` prints `path x y w h` (top-left px), so all photos take one call.
- Page capture: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --window-size=1000,1600 --screenshot=out.png URL`. SEC.gov blocks headless capture (and the in-app browser blocks sec.gov), so use the company's own newsroom copy of the release. Don't spoof a User-Agent.

## Non-negotiables
- ALL CAPS Pixelify Sans captions, VT323 for numbers, a **new** accent each reel.
- Face centred to 0 px, hair 40–70 px under the seam (`layout.py` does it from the Vision boxes).
- Words finish: ≥120 ms after the word end, then run on to a quiet point (`cut.py`). Check the `tail`/`valley` column it prints.
- Names spelled right, checked against an official source. Quick fact-check of the main claim only, and **flag** shaky lines in `project.md` rather than researching them.
- Tweets and posts shown whole, no meta labels. Object-in-hand beats are full face.
- Ocular SFX (`~/Music/Ocular_Sounds/`) + one bed from `~/Music/documentary es/` at 15 LU under the voice; voice at −14 LUFS.
- AssemblyAI transcript (key in `~/.config/assemblyai/config.json`, never printed).

## Deliverables and checks (`~/Movies/FCP/<slug>-graphics/`)
- `img<N>_rpn.fcpxml` (1.14, real source in/out, 1/30 s grid; `finish.py` exits on off-grid values), validated with `xmllint --dtdvalid ~/.cache/fast-rpn/FCPXMLv1_14.dtd` (copied from `Final Cut Pro.app/Contents/Frameworks/Interchange.framework/Versions/A/Resources/`; xmllint can't read it in place because of the spaces in the path).
- `img<N>_rpn_final.mp4` (H.264, everything baked in), `img<N>_rpn.srt`, `stills/` (3+), `img<N>_matchcut_cuts.jpg` (every overlay row: both shapes on the green ring), `img<N>_contact.jpg`.
- Read both sheets before calling it done. Say whether you watched the reel through or only checked frames.

## Lessons from IMG_1827 (12.6 min, 135 s source full of retakes)
- **Retake-heavy source:** pick the cleanest take per line from the indexed words; drop every "okay / and now" block. Move the line that names the subject to the top when the chronological opener doesn't, so the burst lands on the name at ~2 s.
- **Burst photos with a big face** (Vision box wider than ~2× his face width) get scaled down and leave an edge open. `build.py` (img1827+) puts a blurred cover copy of the photo under each frame; still prefer photos whose face is a similar size.
- **Read time:** a chip that lands on the last word of a split piece is on screen for under 0.5 s. Land it on an earlier word ("versus", not "spirit") so it holds ≥1.5 s.
- **Correct, don't amplify:** when a kept line is wrong (e.g. "4 affairs he confirmed" vs 1 admitted + 2 reported), prefer the take that says less, put no graphic on it, and put the sourced number on the cheat sheet.
- **Final Cut can't use the source as-is:** FCP 13 showed a red "Missing Plug-in" slate on IMG_1827 (an H.264 MOV re-saved by QuickTime Player: audio track first, 5 `mebx` metadata tracks), and it may also lack permission to read ~/Desktop. `new_reel.py` now cuts every reel from `~/Movies/FCP/<slug>-graphics/IMG_<N>_clean.MOV`, a lossless `-c copy` remux with video + audio only (same timing, rotation kept). This fixed it.
- `finish.py` (img1827+) leaves the bare Custom LUT effect out of the FCPXML unless `FCP_LUT=1` (removed while chasing the slate above; not proven to be a cause). The grade is baked into the MP4; in FCP add Custom LUT by hand and pick the `.cube`.
- Never leave a bare `cat` (or anything that reads stdin) in a chained Bash command: it hangs until the timeout.
- Reuse captures and burst photos from a sister reel on the same story instead of refetching (copy `assets/dl/*_raw.png`, `assets/burst/`).

## Environment
- Python: `~/.cache/fast-rpn/venv` (Pillow, numpy, pymupdf). System python has no PIL. Recreate it with `uv venv ~/.cache/fast-rpn/venv && uv pip install -p ~/.cache/fast-rpn/venv/bin/python pillow numpy pymupdf`.
- `~/.cache/fast-rpn/faces_all` is the Apple Vision face tool, copied from an older session scratchpad. If it's missing, look for `faces_all` in `/private/tmp/claude-501/*/*/scratchpad/`.
- zsh doesn't word-split `$VAR` in `for t in $T`. Use `${=T}`.

> Repo copy of the user-scope skill at `~/.claude/skills/fast/` (named `fast-rpn` here so it does not shadow `/fast`). Keep the two in sync.
