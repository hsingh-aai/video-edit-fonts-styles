---
name: match-cut-intro
description: Harnoor's match-cut move for shorts. A fast burst of 4–8 public-domain images, each pinned to the same spot and size as a shape in the reel (his head, a laptop card, a logo), cut so one object seems to keep changing, then cut back into the reel on the same shape. The default is a mid-reel burst at about 2.5 s with 4 frames per image; an opening sequence is the alternative. Covers shape chains, measuring the landing spot, SFX, the cut contact sheet check and image sourcing. Use when Harnoor asks for a match cut, a "match intro", an image burst or a "more intense" opener on a reel.
---

# Match-cut burst / intro

Learned Nov 19–20, 2026, on the two ElevenLabs avatar reels (Anthropic IPO and Protocol Explorer). Harnoor went through three rounds of feedback:
1. "Make it a match cut with multiple images, not a 1-second card."
2. "Even faster, after 2.5 s in the video, then show it."
3. "Add 3–4 more images, it becomes more intense, keep it fast."

## What he wants (default)

- **The reel opens untouched.** His face and the hook line carry the first ~2.5 s. Start the burst on a caption boundary near 2.5 s.
- **A fast burst:** 8 images at **4 frames each** (0.13 s), about 1.1 s in all. Five frames each with 4 images is the calmer version.
- **It cuts out of the reel's own shape and back into it.** The first image echoes the shape on screen (his head becomes a coin with a profile head; the site's laptop becomes a real laptop), and the last image cuts back to the reel on that same shape.
- **Exact size and spot.** Every image's key shape is pinned to the same landing centre and size, measured on the reel frame. Nothing drifts between cuts.
- **The narration is unchanged.** The burst replaces only the picture, so the burned-in captions vanish for about 1 s. That's fine.

**The alternative, an opening sequence** (`mode: intro`): 3–5 images at about 0.65 s each over the first ~2.5 s, with one push-in from 78% to 100% of the landing size that runs through every cut, then a match cut into the reel's frame at that point. Put a short label plus a two-line hook (key word in the sky-blue pill) low on a soft dark band, away from the subject. Harnoor found this too slow on its own, so use it only when he asks for an opener.

## Shape chains that worked

- **Money / IPO (discs on black, landing on his head):** $10 Liberty-head coin → 1849 Liberty Head $20 → Buffalo nickel → 1907 $20 → SEC seal → Apollo 17 Earth → Earth by day → Earth at night → his head. A profile head on a coin into his head is the strongest match. A black background makes the cut-out avatar match too.
- **Internet / tech (landing on a site's laptop card):** a laptop photo → the site's own router, DNS and web-server icons → Earth by day → Apollo 17 → Earth at night → the site's cloud-globe icon → the laptop. You can use a site's own icons (grabbed from the screen recording) as "source images".
- Other ideas: a ticker line into a skyline line, a round logo into a coin into a globe, or a centred subject at the same scale and spot.

## Recipe

1. **Measure the landing shape.** Grab the reel frame at the burst start and the frame at the end, draw a 100 px grid on them, and note the shape's centre and size (for example, head at (522, 1170) and 300 px; laptop at (685, 860) and 350 px). The shape must sit in the same place on both frames.
2. **Gather images.** Use public-domain ones from the README's **Public-domain image sources** (NASA, Library of Congress, Smithsonian NNC coin photos and SEC seals on Wikimedia Commons, and so on), or the topic's own source images (screenshots, icons). Check the licence on every file: CC BY-SA is **not** public domain, so skip it. No private people. Fetch the Commons `thumburl` at 1600–3000 px through the API, with a generic User-Agent.
3. **Describe each image** in the kit config. Discs are found automatically: `disc-dark` for globes on black, `disc-light` for coins on white (cut out to a circle on black), `disc-alpha` for transparent PNGs. Anything else is `anchor` (key-shape centre and size in source pixels, measured by bounding the shape's pixels), with a `fill` colour around it. Small icons scaled up about 3× still look clean.
4. **Run the kit:** `python .claude/skills/match-cut-intro/kit/matchcut.py config.json` (see `kit/example-config.json`). It writes the MP4 and the contact sheet.
5. **SFX.** Put a soft Ocular Utility touchscreen single (`Utility - Designed/Phone or Touchscreen Typing/...Singles 01/09/02`) at about 0.4 on each cut, and the Foundation whoosh "Be Gentle" with its peak on the cut out of the reel (burst) or into the reel (intro).
6. **Check the contact sheet.** Each row shows the last frame before the cut, the first frame after it, and a 50% overlay with the landing point marked. In the overlay, the two shapes should sit on top of each other.
7. **Credit and deliver.** Put one small chip listing every source ("Images: NASA · U.S. SEC · Smithsonian NNC (public domain)"). Save new files next to the old ones with a suffix such as `_matchcut_fast8`, never overwriting, copy them to `~/Movies/FCP/<project>-graphics/` with the cut sheet, and open them for Harnoor. Say whether you watched them all the way through or only checked frames.
