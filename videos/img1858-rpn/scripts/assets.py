"""Card images + marker rects -> assets/cards/<name>.png and cards.json {name: {marks: [[[x0,y0,x1,y1], ...], ...], dark: bool}}
(one list of line rects per marked phrase).
Posts from Harnoor's "applied board.excalidraw" (images extracted to assets/board/, 1096 px wide X screenshots). Header and
full text kept; footer (likes, replies) and attached media cut. The board's deal and Linden shots were cut at "Show more",
so those two are rebuilt by postcard.py with the full text from x.com (header still the real screenshot crop).
- deal: Yash Patil, Nov 18, 2026 (x.com/ypatil125/status/2123175975093784902), board b00
- linden: Linden Li, Oct 29, 2025 (x.com/lindensli/status/1983574681916731476), board b04
- tbpn: TBPN, Nov 18, 2026 (x.com/tbpn/status/2123193914362396820), board b06
Marks measured on a 100 px grid shown at half size (displayed coords doubled).
Usage: <venv>/python scripts/assets.py"""
import json, os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(f'{HERE}/..'); CD = f'{R}/assets/cards'
PNG = {   # name: (raw capture, crop box in raw px, marks in raw px, dark page)
    # deal + linden: the board screenshots (and X's embed) stop at "Show more", so postcard.py rebuilds them with the full text
    'tbpn': ('../board/b06.png', (0, 0, 1096, 1310),
             [[[240, 144, 1046, 194], [30, 194, 372, 242]]], False),   # Palo Alto Networks agrees to acquire Applied Compute for $4.5B
}


def main():
    os.makedirs(CD, exist_ok=True); meta = {}
    import postcard
    for n in postcard.POSTS:
        p, mk = postcard.build(n); im = Image.open(p); PNG[n] = (os.path.relpath(p, CD), (0, 0) + im.size, mk, False)
    for name, (raw, box, marks, dark) in PNG.items():
        Image.open(f'{CD}/{raw}').convert('RGB').crop(box).save(f'{CD}/{name}.png')
        meta[name] = dict(marks=[[[r[0] - box[0], r[1] - box[1], r[2] - box[0], r[3] - box[1]] for r in ph] for ph in marks], dark=dark)
    json.dump(meta, open(f'{CD}/cards.json', 'w'), indent=1)
    for k, v in meta.items(): print(k, Image.open(f'{CD}/{k}.png').size, len(v['marks']))


if __name__ == '__main__':
    main()
