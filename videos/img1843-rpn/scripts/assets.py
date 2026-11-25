"""Card images + marker rects -> assets/cards/<name>.png and cards.json {name: {marks: [[[x0,y0,x1,y1], ...], ...], dark: bool}}
(one list of line rects per marked phrase).
- info_bars / info_rest: The Information, "How Much Companies Allow Their Engineers to Spend on Tokens a Month" (the chart
  Harnoor attached, 926x1550). Marks measured on a 100 px grid (raw px); dark page, so marks are tint + underline.
Usage: <venv>/python scripts/assets.py"""
import json, os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(f'{HERE}/..'); CD = f'{R}/assets/cards'
PNG = {   # name: (raw capture, crop box in raw px, marks in raw px, dark page)
    'info_bars': ('../dl/info_raw.png', (62, 40, 862, 640),
                  [[[664, 495, 760, 628]],      # Tesla $800
                   [[564, 458, 660, 628]],      # Uber $2,000
                   [[364, 458, 460, 634]],      # Atlassian $2,000
                   [[464, 458, 560, 628]],      # Rippling $2,000
                   [[164, 395, 260, 628]],      # Apple $4,000
                   [[64, 202, 160, 628]]], True),   # Microsoft $10,000
    'info_rest': ('../dl/info_raw.png', (62, 1002, 862, 1422),
                  [[[332, 1214, 592, 1261]],    # Anthropic
                   [[64, 1319, 324, 1365]],     # OpenAI
                   [[332, 1371, 592, 1417]],    # Snowflake
                   [[332, 1319, 592, 1365]],    # Oracle
                   [[64, 1371, 324, 1417]],     # Replit
                   [[64, 1267, 324, 1313]],     # Cognition
                   [[222, 1012, 402, 1106]]], True),   # NVIDIA $35,000-$50,000
}


def main():
    os.makedirs(CD, exist_ok=True); meta = {}
    for name, (raw, box, marks, dark) in PNG.items():
        Image.open(f'{CD}/{raw}').convert('RGB').crop(box).save(f'{CD}/{name}.png')
        meta[name] = dict(marks=[[[r[0] - box[0], r[1] - box[1], r[2] - box[0], r[3] - box[1]] for r in ph] for ph in marks], dark=dark)
    json.dump(meta, open(f'{CD}/cards.json', 'w'), indent=1)
    for k, v in meta.items(): print(k, Image.open(f'{CD}/{k}.png').size, len(v['marks']))


if __name__ == '__main__':
    main()
