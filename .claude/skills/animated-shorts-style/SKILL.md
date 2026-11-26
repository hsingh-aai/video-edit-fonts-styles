---
name: animated-shorts-style
description: Pointer and house rules for the outside style "Claude Animated Shorts" (mromidev/claude-animated-shorts, MIT). 55–70 s vertical animated story shorts with 2D ink-outlined characters in a colourful 3D town, lens blur, gliding cameras, a march score and SFX, rendered with three.js inside Remotion. Use only when Harnoor says "animated shorts", "cartoon short" or names the repo. Never a default. "The cartoon style" is Toybox, not this.
---

# Claude Animated Shorts (outside style)

**Source:** [mromidev/claude-animated-shorts](https://github.com/mromidev/claude-animated-shorts) by Mr omi. Checked on Nov 25, 2026. MIT for code and docs (© 2026 Mr omi); keep the notice if its code ships in a build. Its `references/frames/` and `references/sheets/` are frames from someone else's channel, included "for style study only". **Never put them in a video, a README or a storyboard.**

**How it differs from Toybox:** Toybox ("the cartoon style") is Harnoor on camera with blue-paper cards and handwritten captions. Animated Shorts has no camera at all: it's a fully animated story film with characters, a world and a score.

**What it looks like:** flat 2D characters with thick ink outlines walk through a painted 3D town. Lens blur separates the depth planes, the camera glides and holds (about 80% of frames hold, then an ease-out burst), and a march-style score with SFX carries a 55–70 s story.

**Storyboard:** [styles/storyboards/animated-shorts.jpg](../../../styles/storyboards/animated-shorts.jpg). It is a **mock**: hand-drawn panels showing the shot plan for the sample chip script. The tool wasn't run, because the repo's `templates/bridge/` source is listed in its README but isn't published, and it needs Remotion with `@remotion/three`.

## When to use it

- **By name only:** "animated shorts", "cartoon short", or the repo name.
- **Good fits:** a faceless history or story short ("the bridge that fell for a song"), or a fable-style explainer with a character.
- **Bad fits:** anything that needs proof. Real pages and posts still get real captures, as a cut-in or not at all.

## Install

```bash
git clone https://github.com/mromidev/claude-animated-shorts.git ~/.claude/skills/cartoon-3d-short
```

- It needs [Remotion](https://www.remotion.dev/) with `@remotion/three`, Node, Python 3 and ffmpeg.
- Set `REMOTION_TMP` on a big drive. Each bundle copies about 1.3 GB of `public/`.
- Check that its templates are present before planning a render. If they are missing, build the world from its `STYLE_BIBLE.md` rules in our own Remotion or HyperFrames project.
- Install only once Harnoor picks it.

## Harnoor's rules on top

- **The story and characters are his own.** Use the references for the look only, and never copy a reference short's plot, lines or characters.
- **Captions** are lowercase Poppins in the chosen house style, on their own lane, kept clear of the characters' faces.
- **Title:** a hook title by 2 s, 4–5 words, on its own "Title" lane.
- **Layering:** render the world, the characters and the captions as separate alpha ProRes 4444 clips on named FCPXML lanes. Snap them to the 1/30 s grid.
- **Sound:** keep its synthesized score and SFX only if he wants them. Otherwise use one music bed at 15–20 LU under the voice and the Ocular SFX rules.
- **Credit:** in `project.md`, note "Made with claude-animated-shorts by Mr omi (MIT)" and list what changed from its defaults.
- **Delivery:** the usual: FCPXML, SRT, preview and alpha clips, in `renders/` and `~/Movies/FCP/<name>-graphics/`.
