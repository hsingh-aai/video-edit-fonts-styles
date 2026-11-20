"""Match-cut sequence for a finished 1080x1920 reel (generic kit, no project paths).

Every image's key shape (a disc, a laptop, an icon) is pinned to the same landing point and size
as the shape in the reel, so each cut reads as one object changing. Two modes:

  burst  (default, Harnoor's pick): the reel plays untouched, then at `start_frame` it cuts OUT of
         the reel's own shape into N images (`frames_per_image` each, e.g. 8 x 4 frames) and back
         INTO the reel on the same shape. All shapes sit at exactly `size`.
  intro  replaces the reel's opening: N images over `cut_frame` frames with one push-in from
         push[0]*size to size that runs through every cut, then a match cut into the reel at
         `cut_frame`. Optional label + 2-line hook on a soft dark band.

Narration is untouched; each cut gets a soft tick, and a whoosh peaks on the first (burst) or
last (intro) cut. Also writes a contact sheet: one row per cut, before | after | 50% overlay,
with the landing point marked. That sheet is the check.

usage: python matchcut.py config.json      (paths inside are relative to the config file)

config keys:
  reel, out, sheet               input reel, output mp4, contact-sheet jpg
  mode                           "burst" | "intro"
  target [x, y], size            landing point and key-shape size in px (measure on the reel frame)
  start_frame, frames_per_image  burst timing
  cut_frame, push [0.78, 1.0]    intro timing
  items                          list of {file, kind, label, ...}
      kind "disc-dark"  round subject on black (globes)       optional thr (default 24)
      kind "disc-light" round subject on white (coins)        optional half: "left"|"right"
      kind "disc-alpha" round subject with transparency (seals, cut-out globes)
      kind "anchor"     full frame: anchor [x, y] and ref (key-shape px) in source pixels,
                        fill [r,g,b] around it, optional vignette: true for small photos
  credit                         one chip listing every source, e.g. "Images: NASA · Smithsonian NNC (public domain)"
  font, font_bold                TTF paths for the chip / hook
  ticks [wav...], whoosh wav     SFX (optional)
  label, hook [[text, null|"pill"], ...]   intro only, optional
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
SKY = (86, 182, 255)


def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


def prep(it, base):
    im = Image.open(base / it['file'])
    if it.get('half') in ('left', 'right'):
        im = im.crop((0, 0, im.width // 2, im.height) if it['half'] == 'left' else (im.width // 2, 0, im.width, im.height))
    rgba = im.convert('RGBA')
    kind = it['kind']
    if kind == 'anchor':
        return dict(it, img=rgba, fill=tuple(it.get('fill', (0, 0, 0))))
    if kind == 'disc-alpha':
        mask = np.array(rgba)[:, :, 3] > 10
    else:
        g = np.array(im.convert('L')).astype(int)
        mask = g > it.get('thr', 24) if kind == 'disc-dark' else g < 235
    ys, xs = np.where(mask)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    cx, cy, d = (x0 + x1) / 2, (y0 + y1) / 2, max(x1 - x0, y1 - y0)
    if kind != 'disc-dark':  # clean circular cut-out on black
        m = Image.new('L', rgba.size, 0)
        ImageDraw.Draw(m).ellipse((cx - d / 2 + 2, cy - d / 2 + 2, cx + d / 2 - 2, cy + d / 2 - 2), fill=255)
        m = m.filter(ImageFilter.GaussianBlur(2))
        if kind == 'disc-alpha':
            m = Image.fromarray(np.minimum(np.array(m), np.array(rgba)[:, :, 3]))
        rgba.putalpha(m)
    return dict(it, img=rgba, anchor=(cx, cy), ref=d, fill=(0, 0, 0))


def place(it, s, target):
    """Frame with the item's key shape scaled to s px and its anchor on target."""
    k = s / it['ref']; im = it['img']
    sw, sh = max(1, int(im.width * k)), max(1, int(im.height * k))
    ox, oy = int(round(target[0] - it['anchor'][0] * k)), int(round(target[1] - it['anchor'][1] * k))
    vx0, vy0, vx1, vy1 = max(0, -ox), max(0, -oy), min(sw, W - ox), min(sh, H - oy)
    fr = Image.new('RGBA', (W, H), tuple(it['fill']) + (255,))
    if vx1 > vx0 and vy1 > vy0:  # resize only the visible window
        part = im.resize((vx1 - vx0, vy1 - vy0), Image.LANCZOS, box=(vx0 / k, vy0 / k, vx1 / k, vy1 / k))
        if it.get('vignette'):
            m = Image.new('L', part.size, 0)
            ImageDraw.Draw(m).rounded_rectangle((0, 0, part.width - 1, part.height - 1), 40, fill=255)
            part.putalpha(m.filter(ImageFilter.GaussianBlur(30)))
        fr.alpha_composite(part, (ox + vx0, oy + vy0))
    return fr


class Overlay:
    def __init__(self, cfg, base):
        self.cfg = cfg
        self.f = ImageFont.truetype(str(base / cfg['font']), 24)
        self.fb = ImageFont.truetype(str(base / cfg.get('font_bold', cfg['font'])), 104)
        self.fl = ImageFont.truetype(str(base / cfg['font']), 34)
        g = np.clip((np.arange(H) - 1330) / 160, 0, 1) * 175
        self.band = Image.new('RGBA', (W, H), (0, 0, 0, 255))
        self.band.putalpha(Image.fromarray(np.repeat(g.astype(np.uint8)[:, None], W, 1)))

    def __call__(self, fr, t, hook):
        c = self.cfg
        if hook and c.get('hook'):
            fr.alpha_composite(self.band)
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            k = ease((t - 0.05) / 0.25)
            if c.get('label') and k > 0:
                lw = int(self.fl.getlength(c['label'])) + 44; x0, y0 = (W - lw) // 2, int(1420 + 20 * (1 - k))
                d.rounded_rectangle((x0, y0, x0 + lw, y0 + 58), 29, fill=(255, 255, 255, int(235 * k)))
                d.text((W // 2, y0 + 29), c['label'], font=self.fl, fill=(15, 15, 15, int(255 * k)), anchor='mm')
            for i, (txt, style) in enumerate(c['hook']):
                k = ease((t - 0.15 - 0.2 * i) / 0.3)
                if k <= 0:
                    continue
                y = int(1560 + 132 * i + 40 * (1 - k))
                if style == 'pill':
                    pw, ph = int(self.fb.getlength(txt) + 70), 140
                    d.rounded_rectangle((W // 2 - pw // 2, y - ph // 2, W // 2 + pw // 2, y + ph // 2), 32, fill=SKY + (int(255 * k),))
                    d.text((W // 2, y), txt, font=self.fb, fill=(255, 255, 255, int(255 * k)), anchor='mm')
                else:
                    d.text((W // 2, y), txt, font=self.fb, fill=(255, 255, 255, int(255 * k)), anchor='mm',
                           stroke_width=5, stroke_fill=(0, 0, 0, int(190 * k)))
            fr.alpha_composite(lay)
        if c.get('credit'):
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            cw = int(self.f.getlength(c['credit'])) + 32
            d.rounded_rectangle((40, 1790, 40 + cw, 1834), 22, fill=(0, 0, 0, 150))
            d.text((56, 1812), c['credit'], font=self.f, fill=(255, 255, 255, 225), anchor='lm')
            fr.alpha_composite(lay)
        return fr


def grab(src, i):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{i / FPS:.4f}', '-i', str(src), '-frames:v', '1',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return Image.frombytes('RGB', (W, H), b)


def peak(path):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-ac', '1', '-ar', '8000', '-f', 's16le', '-'],
                       capture_output=True).stdout
    a = np.convolve(np.abs(np.frombuffer(b, np.int16).astype(float)), np.ones(400) / 400, 'same')
    return float(np.argmax(a) / 8000), len(a) / 8000


def main(cfg_path):
    cfg_path = Path(cfg_path).resolve(); base = cfg_path.parent
    c = json.load(open(cfg_path))
    src, out = base / c['reel'], base / c['out']
    items = [prep(it, base) for it in c['items']]
    tgt, S, burst = c['target'], c['size'], c.get('mode', 'burst') == 'burst'
    ov = Overlay(c, base)
    if burst:
        fpi = c.get('frames_per_image', 4); s0 = c['start_frame']; n = fpi * len(items)
        bounds = [s0 + k * fpi for k in range(len(items) + 1)]
    else:
        s0 = 0; n = c['cut_frame']; p0, p1 = c.get('push', [0.78, 1.0])
        bounds = [round(k * n / len(items)) for k in range(len(items) + 1)]
    tmp = out.with_suffix('.frames.mp4')
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                            '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '15', '-pix_fmt', 'yuv420p', str(tmp)],
                           stdin=subprocess.PIPE)
    first, last = {}, {}
    for i in range(s0, s0 + n):
        j = max(k for k in range(len(items)) if bounds[k] <= i)
        s = S if burst else S * (p0 + (p1 - p0) * i / n)
        fr = place(items[j], s, tgt)
        if i == bounds[j]: first[j] = fr.convert('RGB')
        if i == bounds[j + 1] - 1: last[j] = fr.convert('RGB')
        enc.stdin.write(ov(fr, (i - s0) / FPS, hook=not burst).convert('RGB').tobytes())
    enc.stdin.close(); enc.wait()
    # audio: narration + ticks on cuts + whoosh
    cuts = [b / FPS for b in bounds]
    tick_at = cuts[1:] if burst else cuts[1:-1]
    whoosh_at = cuts[0] if burst else cuts[-1]
    ins, chains, labels = [], [], []
    ticks = [base / t for t in c.get('ticks', [])]
    for k, t in enumerate(tick_at if ticks else []):
        ins += ['-i', str(ticks[k % len(ticks)])]
        chains.append(f'[{len(ins) // 2 + 1}:a]atrim=0:0.3,volume=0.4,adelay={int(t * 1000)}:all=1,aresample=48000[t{k}]')
        labels.append(f'[t{k}]')
    if c.get('whoosh'):
        wp, wl = peak(base / c['whoosh']); ins += ['-i', str(base / c['whoosh'])]
        chains.append(f'[{len(ins) // 2 + 1}:a]atrim=0:{min(wl, wp + 0.8):.3f},afade=t=out:st={wp + 0.35:.3f}:d=0.45,'
                      f'volume=0.32,adelay={int(max(0, whoosh_at - wp) * 1000)}:all=1,aresample=48000[w]')
        labels.append('[w]')
    vf = (f"[1:v]split[a][b];[a]trim=end_frame={s0},setpts=PTS-STARTPTS[pre];"
          f"[b]trim=start_frame={s0 + n},setpts=PTS-STARTPTS[post];[pre][0:v][post]concat=n=3:v=1:a=0[v]")
    af = f"[1:a]aresample=48000[n];" + ''.join(x + ';' for x in chains) + \
         f"[n]{''.join(labels)}amix=inputs={len(labels) + 1}:duration=first:normalize=0[out]"
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(tmp), '-i', str(src), *ins,
                    '-filter_complex', vf + ';' + af, '-map', '[v]', '-map', '[out]', '-r', str(FPS),
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', str(out)], check=True)
    tmp.unlink()
    # contact sheet
    names = [it.get('label', it['file']) for it in c['items']]
    befores = ([grab(src, s0 - 1)] if burst else []) + [last[j] for j in range(len(items))]
    afters = [first[j] for j in range(len(items))] + [grab(src, s0 + n)]
    if not burst:
        afters = afters[1:]
    seq = (['reel'] + names + ['reel']) if burst else (names + ['reel'])
    tw, th = 270, 480
    sheet = Image.new('RGB', (3 * tw + 20, len(afters) * (th + 34) + 10), (24, 24, 24))
    sd = ImageDraw.Draw(sheet)
    for r, (b, a) in enumerate(zip(befores, afters)):
        y = 10 + r * (th + 34)
        t = cuts[r] if burst else cuts[r + 1]
        sd.text((10, y), f'cut {r + 1} @ {t:.2f}s: {seq[r]} -> {seq[r + 1]}', font=ov.f, fill=(255, 255, 255))
        for k, im in enumerate([b, a, Image.blend(b, a, 0.5)]):
            sheet.paste(im.resize((tw, th)), (5 + k * (tw + 5), y + 30))
        tx, ty = tgt[0] * tw / W + 5 + 2 * (tw + 5), tgt[1] * th / H + y + 30
        sd.ellipse((tx - 4, ty - 4, tx + 4, ty + 4), outline=(255, 60, 60), width=2)
    sheet.save(base / c['sheet'], quality=90)
    print(out, 'cuts at', [round(x, 2) for x in (cuts if burst else cuts[1:])])


if __name__ == '__main__':
    main(sys.argv[1])
