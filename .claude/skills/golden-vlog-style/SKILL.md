---
name: golden-vlog-style
description: Harnoor's favourite style for vlogs and playful reels ("Golden Vlog", from the Neighborsgiving potluck reel v2, Nov 2026). Footage is the hero. At most 3 handmade, Instagram-native overlays (a white marker arrow or circle with 1–3 handwritten words, real-photo cutouts with a white edge, a phone-style text sticker), small uneven lowercase captions whose emphasis changes per beat, a warm golden-hour film grade with grain and halation, 3× speed-ups and J-cuts, crowd sound under the VO and sparse SFX. Use when Harnoor asks for Golden Vlog, "vlog style", a vlog, a playful reel or "the Neighborsgiving style" (warm & witty stays the default for everything else).
---

# Golden Vlog

Harnoor's favourite style for vlogs and playful reels, learned from the Neighborsgiving potluck reel v2 (Nov 25, 2026). His note on v1 was "improve the style so that it doesn't look like a Claude artifact". On v2 he said "i like it … this is my fav for vlogs and playful". Use it for vlogs, events, city walks, food and anything playful. Warm & witty stays the default for everything else.

**The one rule: it should look like a creator made it on their phone, not like a template.** Let the footage be the hero. When in doubt, cut an overlay.

## Overlays (3 at most per reel)

Use only these three kinds, and only where they add information. Never use UI cards, pills, drawn icons, emoji-like vectors, glossy gradients or perfectly centred stacks.

1. **Marker arrow or circle** (`marker_arrow`, `bez`, `scribble_circle`)
   - A white marker stroke, 15 px, round caps. It draws on over 0.45 s, then the arrow head flicks on.
   - It sits on a real moment: down the street at the table, around the dish.
   - Add a 1–3 word label in **Gaegu Bold** handwriting (92 px, tilted about 7°), for example "it keeps going".
   - Aim it where the subject stays put. On a moving shot, follow the line of the scene (a street's vanishing point), not a moving person.
   - Keep the stroke off faces and bodies at its first frame.
2. **Real-photo cutouts** (`cutout_sticker`, `cutouts_layer`)
   - Lift the subject from a frame of his own footage with `kit/lift.swift`, which uses macOS Vision (`swift lift.swift in.png out.png`).
   - They get an IG-style 9 px white cut edge and a soft shadow. They land one per spoken item with a soft spring and a slow sway.
   - Use food, objects and props only. If the lift catches a person, drop that frame (it happened with a lasagna shot).
   - Place them in empty sky or wall, never over faces.
3. **Phone text sticker** (`phone_sticker`, `place_sticker`)
   - A plain IG "Classic" box: a white rounded box with Helvetica Neue Bold at 46 px, left aligned. It fades in and doesn't bounce.
   - Use it for credits ("drone: @handle") and the odd one-line aside.

## Captions (`caption()`)

- Lowercase, 1–3 word chunks, **Poppins SemiBold at 54 px**, white with a soft shadow and no thick outline.
- Keep the capitals on "I", names, places and brands.
- Each chunk is placed **off centre by up to ±60 px and tilted up to ±2°**, seeded per chunk so re-renders match.
- The emphasis rotates per beat, never the same twice in a row:
  - a yellow marker swipe (`#FFD65C`) that wipes in behind the word
  - a big **Instrument Serif Italic** word at 80 px
  - plain ExtraBold
- Captions sit above the head (y ≈ 215). Check each frame: no captions over faces.
- Ship an SRT too.

## Grade

- **LUT** `kit/golden_film.cube` (from `make_lut()`): gold in the highlights, a little teal in deep shadows, opened mids, a film S-curve, faded blacks (0.035), rolled-off whites (0.955) and +12% saturation.
  - Tuned on overcast SF daylight; re-check skin on new light.
  - Install it as `~/Library/Application Support/ProApps/Custom LUTs/Golden Film - <project>.cube`.
- **Film finish, preview only** (`film_finish(lut, dusk_t)`):
  - orange halation on highlights
  - a second, wider glow from the dusk shots on, so evening lights bloom
  - grain and a soft vignette
- FCP gets the LUT only.

## Edit rhythm

- **Vary the pace.** Use one or two 3× speed-ups on the walking or riding b-roll, cutting back to 1× on the arrival. In FCPXML that's a `timeMap` (clip time → source time); in ffmpeg it's `setpts=PTS/3` plus `atempo`.
- **J-cut.** At least one: the next shot's line starts under the current shot (e.g. "wow, there's a…" under a laughing selfie, cut to the sky on "rainbow"). In FCP the lead audio is a connected audio clip below the spine.
- **Cuts.** Cut b-roll on the beat grid, and sync bites on their words. Trim pauses over 0.3 s inside lines.
- **Sound.**
  - Crowd and ambient sound stays up under the VO (b-roll at about −31 dB RMS).
  - The music bed sits at about −25 dB, beat-aligned.
  - SFX are sparse: a marker stroke for the arrow, a soft "put down" per cutout, and one whoosh only where a section changes (into dusk).
  - Use Ocular Sounds: Utility Writing/Marker, Objects on Desk Foley, Foundation Whooshes "Be Gentle".
- **Mix** to −14 LUFS, true peak about −1.5 dBTP.

## VO workflow

1. Transcribe every clip with AssemblyAI (video-use `transcribe.py`). If a clip has an Apple spatial audio track, transcribe `-map 0:a:0` (the AAC track).
2. Keep his real on-camera lines where they're good. Mark lines that may be someone else.
3. Write a short, warm, original VO for the gaps only, in 3–5 lines.
4. **Show Harnoor the script and wait for his OK before spending ElevenLabs credits.** Then generate in "Harnoor's voice" (Multilingual v2) with per-character timestamps, which drive the captions. Five lines cost about 100 credits.
5. Prototype the timing with macOS `say` first; never ship it.

## Borrowed footage

- Only real or public sources, and always credited with a phone text sticker naming the handle ("drone: @handle").
- Download into its own folder. Cut out any burned-in text: find its frames with a brightness check on the caption box, and use only the clean windows. Mute its music.
- Tell Harnoor if it's from a different event or date, and remind him to get the creator's OK.

## Deliverables

- A preview MP4 at 1080×1920, 30 fps, −14 LUFS, with the film finish baked in.
- An FCPXML linked to the original clips and DTD-validated:
  - Lane 1: the "Look Grade" adjustment layer plus Custom LUT.
  - Above it: overlays as ProRes 4444 alpha, then captions.
  - Audio lanes: music, VO, SFX and the J-cut lead.
- The LUT, an SRT, a few frame grabs and a `project.md`. Copy everything to `~/Movies/FCP/<name>-graphics/`.

**FCP notes**

- **The LUT on the GRADE layer is assigned by hand.** The FCPXML can't carry the LUT file. In FCP open the timeline Index, filter to Titles, select GRADE, open the Video inspector, then Custom LUT, and pick it. Background clicks on the timeline don't select clips; the Index does.
- **Instagram/yt-dlp downloads are often VP9**, which FCP shows as "missing plug-in". Make a ProRes 422 copy at the same frame rate (`ffmpeg -c:v prores_ks -profile:v 2 -r 30`) and link that.
- iPhone clips with no rotation tag need `adjust-transform rotation` (negative is clockwise), with the scale computed from the unrotated frame.

## Kit

- `kit/golden_vlog.py`: overlays, captions, `make_lut`, `film_finish`. It's generic, with fonts from this repo.
- `kit/lift.swift`: Vision subject lift for the cutouts.
- `kit/golden_film.cube`: the grade.
- `kit/sample.py`: renders a demo still from a drawn stand-in scene (`python sample.py out.jpg`).
- Sample stills are in `styles/samples/golden-vlog/`.
