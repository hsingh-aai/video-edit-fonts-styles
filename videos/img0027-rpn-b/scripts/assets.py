"""Card images + marker rects -> assets/cards/<name>.png and cards.json {name: {marks: [[[x0,y0,x1,y1], ...], ...], dark: bool}}
(one list of line rects per marked phrase).
- aie: AI Engineer's write-up of Zach Lloyd's (Warp) Code Summit talk "Software Engineering Is Becoming Factory Engineering"
  (ai.engineer/code/2026/talks/zach-lloyd, Nov 12, 2026), captured with headless Chrome at 540 px x2 (assets/dl/aie_m_raw.png).
  The card stacks three real crops of that page: date + title, the byline (Zach Lloyd / Warp / Founder & CEO), and the
  "Put the factory under version control" section through "...cloud coding agents." (the rest of that paragraph is cut).
Marks measured on a 50 px grid at full size.
Usage: <venv>/python scripts/assets.py"""
import json, os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(f'{HERE}/..'); CD = f'{R}/assets/cards'
BG = (10, 10, 10)


def aie():
    raw = Image.open(f'{R}/assets/dl/aie_m_raw.png').convert('RGB')
    parts = [(0, 420, 1080, 660), (0, 860, 1080, 1035), (0, 3680, 1080, 3978)]   # title, byline, definition
    gap = 30; h = sum(b[3] - b[1] for b in parts) + gap
    out = Image.new('RGB', (1080, h), BG); y = 0; offs = []
    for k, b in enumerate(parts):
        if k == 2: y += gap
        offs.append(y - b[1]); out.paste(raw.crop(b), (0, y)); y += b[3] - b[1]
    o = offs[2]   # raw y -> card y for the definition section
    marks = [[[683, 3860 + o, 1025, 3905 + o], [40, 3922 + o, 222, 3970 + o]],    # "code-defined, closed-loop system"
             [[284, 3922 + o, 995, 3970 + o]]]                                     # "measuring and improving cloud coding agents."
    out.save(f'{CD}/aie.png'); return marks


def main():
    os.makedirs(CD, exist_ok=True)
    meta = {'aie': dict(marks=aie(), dark=True)}
    json.dump(meta, open(f'{CD}/cards.json', 'w'), indent=1)
    for k, v in meta.items(): print(k, Image.open(f'{CD}/{k}.png').size, len(v['marks']))


if __name__ == '__main__':
    main()
