---
name: huashu-art-motion-style
description: Pointer and house rules for the outside style "Huashu Art Motion" (alchaincyf/huashu-art-motion, MIT). Art-history styles drawn in code that actually move (Van Gogh flow-field strokes, Monet, Seurat, Matisse cut paper, ink wash, pop art, 8-bit, vaporwave and more), plus explainer grammars (whiteboard, Vox collage, 3Blue1Brown-style morphs, kinetic type, Keynote UI, finance charts) rendered from a JSON cue spec, in portrait or landscape, with optional alpha. Use only when Harnoor asks for Huashu, "huashu art motion", "the moving paintings style" or "make it look like a painting that moves", or picks it from an outside-styles suggestion. Never a default.
---

# Huashu Art Motion (outside style)

**Source:** [alchaincyf/huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion) by 花叔 / Huashu. Checked on Nov 25, 2026 at v1.3.1. Nothing from the repo is copied into this one. This file only says how to use it with Harnoor's rules.

**Licence:** MIT for code and docs (© 2026 alchaincyf). When code from it is shipped in a build, keep its copyright and licence notice. These parts are **not** under MIT and are never used in Harnoor's videos:
- Huashu's own cartoon likeness and character frames (`scripts/engine/demos/_shared/hero/`, `demos/long_scroll/frames/`, `assets/角色/`), including the overview images and demo films that show it.
- The *Clawd: Night at the Museum* demo, its GIFs and the film. Clawd belongs to Anthropic.
- Fonts in `scripts/engine/lib/fonts/` keep their own OFL licences, and the stroke-order data under `reference_films/spacex/` keeps the Arphic licence.

**What it looks like:** a painting that keeps moving. In the Van Gogh scene the brushstrokes follow a flow field, the stars swirl and the lamp glow breathes. Each era has its own renderer (impasto strokes, pointillist dots, cut-paper edges, ink bleed, Ben-Day dots, 8-bit pixels, neon glow) and its own signature transition into the next. A second half of the repo holds explainer grammars. These are parameterised clips drawn from a JSON list of cues (`draw`, `point`, `highlight`, ...) timed to the voice.

Gallery frames: [styles/screenshots/huashu-art-motion-9x16.jpg](../../../styles/screenshots/huashu-art-motion-9x16.jpg) (Van Gogh scene rendered at 1080×1920 with the repo's own `render.py`, Nov 25, 2026) and [huashu-art-motion.jpg](../../../styles/screenshots/huashu-art-motion.jpg) (the repo's showcase hero).

## When to use it

- **By name only.** Harnoor asks for Huashu, huashu art motion, "moving paintings" or "the art history style". Or the outside-styles step in CLAUDE.md suggests it and he picks it.
- **Good fits:** an art, history or "through the ages" beat; a 3–8 s full-screen board where one idea becomes a painting; a transition between sections that changes the era; a whiteboard or kinetic-type explainer clip when the house style has no drawn version.
- **Bad fits:** proof beats. Real pages, posts, apps and products always get the real capture, never a painting of them.
- Use one recipe per piece unless Harnoor asks to mix them. The exception is a deliberate "through the eras" sequence.

## Install and render

Needs [uv](https://docs.astral.sh/uv/), ffmpeg and Playwright Chromium (already installed on this Mac on Nov 25, 2026).

```bash
npx skills add alchaincyf/huashu-art-motion
uv run --with playwright playwright install chromium   # once
```

For a one-off, cloning into the project's `assets/` or the scratchpad is enough. Run its scripts from the clone with `uv run`.

```bash
# a still of one era (portrait), to approve the look first
uv run --with playwright python scripts/engine/render.py --solo 09_postimp --stills 0.3,1.5 --no-counter --width 1080 --height 1920 --out preview
# a clip from a cue spec, transparent, for an FCP lane
uv run --with playwright python scripts/engine/render.py --spec my_clip.json --alpha --fps 30 --out clip.mov
```

- The skill docs and recipe cards are mostly in Chinese. The English README only gives an overview. Start with `references/风格配方/INDEX.md`: the ★★★ cards are the ones it calls ready to use.
- A spec sets `grammar`, `duration`, `fps`, `width`, `height`, `theme` and `cues`. Set `fps: 30` and `1080×1920` for reels, or `1920×1080` for long form. The engine's default is 60 fps.
- `--alpha` writes ProRes 4444 with transparency, which drops straight onto a connected FCP lane.
- Before a clip ships, run `scripts/qa.py`. Its film gate blocks slideshow-like clips, and that matches this repo's rule that something should be moving.

## Harnoor's rules on top

- **No franchise look-alikes.** Skip the recipes and demos that imitate a specific show, studio or game (Ghibli, Pixar, Shinkai, Kirby, Rick & Morty, South Park, the Super Mario level). Art-history and medium recipes are fine (Van Gogh, Monet, Seurat, Matisse, Klimt, ink wash, pop art, 8-bit, vaporwave, Bauhaus, mosaic). Old masters' paintings are public domain. Don't reuse the girl-and-cat room from the speedrun demo either; compose a new scene for the subject.
- **Fonts:** replace the repo's Chinese fonts with this repo's pairings (`fonts/`, README pairings). Use the active style's caption font for any words inside the clip.
- **Safe zones (9:16):** keep anything to be read out of the face area (y 460–1060). Words go in the top band (y 80–430) or the chest band (y 1110–1580). On a full-screen board with no face, the whole frame is free, with platform UI margins.
- **No text over the face.** If a painting covers the camera, it has no words over where the eyes and mouth would be.
- **Captions** stay the active style's captions (warm & witty by default), above the head, on their own lane. Never bake captions into the painting.
- **Layering:** each Huashu clip is its own alpha `.mov` on a named FCPXML lane (for example "Huashu – era board" or "Huashu – whiteboard"), separate from Title, captions and other graphics. Snap every offset and start to the 1/30 s grid.
- **Motion and sound:** the house premium rules still apply. Entrances settle within 10 frames, one thing moves at a time, and anything to read holds 1.5 s. The repo can synthesise music in code. Use it only if Harnoor asks; otherwise the music bed and Ocular SFX rules of the active style apply.
- **Credit:** in `project.md`, note "Visuals made with huashu-art-motion by 花叔 (MIT)" and the recipe IDs used. List what changed from the repo's demos (subject, palette, composition), per the "never look copied" rule.
- **Delivery:** the usual: alpha clips plus the FCPXML, LUT, SRT and preview, in the project's `renders/` and `~/Movies/FCP/<name>-graphics/`.
