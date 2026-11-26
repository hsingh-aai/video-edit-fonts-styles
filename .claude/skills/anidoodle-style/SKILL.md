---
name: anidoodle-style
description: Pointer and house rules for the outside style "anidoodle" (alexgreensh/anidoodle, Apache-2.0). Hand-drawn art written as code in 32 styles (pencil and watercolour, coloured pencil, marker comic, risograph, woodcut, sumi-e, chalkboard, cyanotype blueprint, cut paper, embroidery, pixel art, toy brick and more), where every picture draws itself mark by mark in the order an artist works. It renders stills, draw-on films, loops, alpha WebM/APNG stickers and launch films in 9:16 or 16:9. Use only when Harnoor asks for anidoodle, "the doodle style", "hand-drawn that draws itself" or a drawing timelapse, or picks it from an outside-styles suggestion. Never a default.
---

# anidoodle (outside style)

**Source:** [alexgreensh/anidoodle](https://github.com/alexgreensh/anidoodle) by Alex Greenshpun. Checked on Nov 25, 2026. Nothing from the repo's code is copied into this one. This file only says how to use it with Harnoor's rules.

**Licence:** Apache License 2.0, © 2026 Alex Greenshpun. If the repo's code or files are redistributed, keep the licence and its `NOTICE` file and mark changed files. Our gallery frame [styles/screenshots/anidoodle.jpg](../../../styles/screenshots/anidoodle.jpg) is the repo's own `assets/styles.jpg` contact sheet, scaled down, credited to the author under Apache-2.0. Third-party parts carry their own terms:
- The optional sound pack (`soundfetch.mjs`, 373 MB) holds VCSL instrument samples (CC0) and OpenAIR room impulses (**CC BY 4.0, attribution required**). Download it only if Harnoor says yes. If its rooms are used, credit "OpenAIR, Audio Lab, University of York, CC BY 4.0" in `project.md` and the description.
- `engine/assets/refs/vangogh-almond-blossom.jpg` is public domain.

**What it looks like:** an illustration that draws itself. Nothing fades in: pencil lines go down first, then washes spread from where the brush touched, a woodblock prints the keyblock and then each colour, and pixel art blocks in and then shades. The last frame of the film is the finished still, pixel for pixel. The same seeded code always renders the same picture, at any size.

## When to use it

- **By name only.** Harnoor asks for anidoodle, "the doodle style", a drawing timelapse or "hand-drawn that draws itself". Or the outside-styles step in CLAUDE.md suggests it and he picks it.
- **Good fits:** a "how it works" beat drawn as a chalkboard or blueprint; a full-screen board where an idea sketches itself while he explains it; a small alpha sticker (an object drawing itself) in the chest band; a 9:16 launch-style film for one of his builds.
- **Bad fits:** proof beats. Real pages, posts, apps and products always get the real capture.
- Pick one of the 32 styles per piece (its `references/styles.md` has a guide for choosing one) and keep it for the whole video.

## Install and render

Needs Node 20+, Playwright Chromium and ffmpeg (all on this Mac as of Nov 25, 2026).

```text
/plugin marketplace add alexgreensh/anidoodle
/plugin install anidoodle@alexgreensh-anidoodle
```

To drive the engine yourself, scaffold a project in the video's folder (not in this repo):

```bash
node <anidoodle>/engine/tools/scaffold.mjs ./anidoodle --still hero --film intro --format 9x16 --duration 8
cd anidoodle && npm install && npx playwright-core install chromium
node tools/still.mjs  hero  --out out/hero.png --scale 2   # approve the look on one still first
node tools/render.mjs intro --out out/intro.webm           # alpha kept (VP9)
node tools/gate.mjs   intro                                # determinism, contract and dead-air check
```

- Use `--format 9x16` (1080×1920) for reels and `16x9` for long form, at 30 fps.
- FCP doesn't read VP9 alpha WebM well. Convert every overlay to ProRes 4444 with alpha before it goes on a lane: `ffmpeg -c:v libvpx-vp9 -i out/intro.webm -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le out/intro.mov` (the `-c:v libvpx-vp9` before `-i` keeps the alpha).
- It has a `hyperframes` backend, so a drawing can live inside one of this repo's HyperFrames compositions on the same timeline.
- Its launch kit can add captions and music. Leave those off: captions and sound come from Harnoor's active style.

## Harnoor's rules on top

- **Fonts:** any lettering in the drawing uses this repo's pairings (`fonts/`, README pairings) or the active style's caption font, not the engine's default hand.
- **Safe zones (9:16):** keep anything to be read out of the face area (y 460–1060). Use the top band (y 80–430) or chest band (y 1110–1580) for stickers. A full-screen board with no face can use the whole frame, with platform UI margins.
- **No text over the face.** A drawing may sit beside or below the head; words never cross the eyes or mouth.
- **Captions** stay the active style's captions (warm & witty by default), above the head, on their own lane. Never bake them into the drawing.
- **Layering:** each anidoodle clip is its own alpha `.mov` on a named FCPXML lane (for example "anidoodle – chalkboard"), separate from Title, captions and other graphics. Snap every offset and start to the 1/30 s grid.
- **Pacing:** a draw-on beat is about the drawing finishing on the payoff word. Time the last mark to that word and then hold the finished still for at least 1.5 s. Entrances still settle within 10 frames, and one thing moves at a time.
- **Sound:** the repo can compose a score and has its own SFX kit. Use them only if Harnoor asks; otherwise the active style's music bed and Ocular SFX rules apply. Never download the sound pack without his yes.
- **Credit:** in `project.md`, note "Drawings made with anidoodle by Alex Greenshpun (Apache-2.0)" plus the style name, and list what changed from the repo's demos, per the "never look copied" rule.
- **Delivery:** the usual: alpha clips plus the FCPXML, LUT, SRT and preview, in the project's `renders/` and `~/Movies/FCP/<name>-graphics/`.
