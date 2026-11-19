---
name: avatar-video
description: How to make a talking AI avatar of Harnoor (a face plus a cloned voice saying a script) in 9:16 1080×1920. HeyGen is the default route, using his saved avatar and saved voice clone in the web app. Artlist (OmniHuman 1.5 / HeyGen Avatar 4) is a fallback that needs a paid plan to download. Covers access, best settings, picking a new look from a video frame, clean voice samples, costs and limits, downloads and deliverable paths. Use when Harnoor asks for an avatar, a digital twin, "make me say X", or an AI talking-head clip.
---

# Avatar video (talking AI avatar)

Learned Nov 19, 2026 on a first test: the line "Hello, I'm Harnoor." at 9:16. HeyGen gave the best result. Artlist made a video but wouldn't let us download it on the free tier.

## Ground rules

- **Ask Harnoor in chat first** before anything that creates an account, accepts terms or consent for voice or likeness cloning, spends credits or paid generations, or uploads a file (his face, his voice, a frame from his footage). Each one needs his yes.
- **He signs in himself.** Never type passwords. Drive the web app in Claude in Chrome with his signed-in session.
- **Don't swap in another service without asking.**
- **Never commit** his face photos, voice audio, avatar renders, avatar or voice IDs, or account details. They stay under `videos/<project>/`, which is never pushed.

## Route 1: HeyGen (default)

**Access.** Use the HeyGen web app (app.heygen.com) in Claude in Chrome, where Harnoor is signed in. There's no MCP or API here. He already has a saved avatar called "Harnoor" with several looks, and a saved voice clone called "Harnoor", so most jobs need no new uploads.

**Best settings (9:16, 1080×1920):**
- **Avatar:** "Harnoor". Pick the sharpest, best-lit look. A crisp photo look beat an older, softer one.
- **Voice:** his saved clone "Harnoor". Type the script; don't upload audio unless he records the line himself.
- **Model:** Avatar 6 Pro is the best, but it needs the $49/mo plan. Without it, use **Turbo (Avatar 6)**, which is the best on the current plan and is fine for 1080p.
- **Format:** portrait 9:16 at 1080p. The render comes out at 1080×1920 and 25 fps, so conform it to the 30p timeline in FCP.
- **Result:** "Hello, I'm Harnoor." rendered at 3.64 s. It opens with a natural wave and smile, the lip sync is clean, and there was no corner watermark on the download. HeyGen showed no credit cost for the Turbo renders.

**New look from a video.** HeyGen makes new looks from a **photo**, not a video. To use a fresh clip (a new outfit, say), pull one frame from it and upload that as a new "Photo Avatar" look on the existing avatar. A good frame is:
- full resolution, 1080×1920 straight from the source;
- sharp, with no motion blur;
- eyes open, mouth closed or a slight smile;
- no hands in front of the body;
- even light on the face.

To find it, extract frames at about 4 fps into PNGs rather than seeking single frames, because seeking lands on blurred or blinking frames. Score each frame's sharpness (Laplacian variance) and pick the best by eye from a contact sheet.

**Download.** Open the finished video in HeyGen, choose Download at 1080p, then move the file out of `~/Downloads` into the project.

## Route 2: Artlist (fallback, paid to download)

- Tool: toolkit.artlist.io → Video → avatar models **OmniHuman 1.5 Avatar** (ByteDance, the more realistic one; there's no aspect setting, so it follows the input image) and **HeyGen Avatar 4** (has a 9:16 setting). Both go up to 1080p. Inputs are an image reference plus an audio file.
- For OmniHuman, feed it a 1080×1920 crop of the photo so the output is 9:16. It rendered at 1088×1920.
- **Audio must be at least 4 s.** Pad a short line with silence (`adelay` plus `apad`).
- **Free tier:** 1 video and 3 voiceovers. **Custom voices (cloning) are paid only.** **Download is paywalled**: the Download button opens the plan picker ($11.99/mo billed yearly). Never try to get around that. On the free tier the render can only be previewed.
- Chrome's file upload breaks above about 5–10 MB, so upload voice as MP3 rather than WAV.

## Clean voice samples (for cloning or a recorded line)

- Use solo speech only: no music, no second voice, no room echo. A phone voice memo in a quiet room works.
- For a clone, give 30–60 s of natural speech with short pauses (Artlist takes 10 s to 5 min, MP3, WAV or M4A, up to 20 MB). If the source is a YouTube video, transcribe it (AssemblyAI) and cut a continuous stretch where only he talks.
- For a single recorded line, trim to the words using the transcript word times, leave about 0.3–0.4 s of lead-in, and pad to the tool's minimum length.

## Making it more accurate

- Use a sharp, front-on, evenly lit photo at full 9:16 resolution. That matters more than the model.
- Use his own voice clone, trained on clean audio, rather than a stock voice.
- Use the Pro model when the plan allows it.
- Give it a longer line. A 2-second line leaves little room for natural motion.

## Deliverables

- `videos/<project>/renders/<service>-<model>-<look>-<slug>.mp4`, for example `heygen-turbo-tanjacket-hello-im-harnoor.mp4`.
- Copy each one to `~/Movies/FCP/<project>-graphics/`.
- Check each render before reporting: `ffprobe` for size, fps and duration, a frame sheet for lip sync and motion, and a crop of the corners for watermarks.
- Report the file path, the avatar look, the voice, the model and the credits used.
