"""Render sponsor-free sample stills of the premium paper cards to styles/samples/premium-paper-cards/.
Generic content only (no brands, no faces). Run: python sample.py"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from papercard import PaperCard, Mark, motion, INK, MUTED, GREEN_INK, RED_PEN

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')) + '/'
OUT = ROOT + 'styles/samples/premium-paper-cards/'
POP_XB, POP_B = ROOT + 'fonts/poppins/Poppins-ExtraBold.ttf', ROOT + 'fonts/poppins/Poppins-Bold.ttf'
SERIF = '/System/Library/Fonts/Supplemental/Georgia.ttf'
SANS = '/System/Library/Fonts/Helvetica.ttc'
ft = lambda p, s: ImageFont.truetype(p, s)


def backdrop():
    """A soft, out-of-focus stand-in for the talking head (warm room, dark sweater), so cards read in context."""
    bg = Image.new('RGB', (1080, 1920), (196, 170, 132)); d = ImageDraw.Draw(bg)
    d.ellipse([290, 380, 790, 1000], fill=(205, 160, 128))           # head-ish blob in the face zone
    d.rounded_rectangle([90, 1000, 990, 2100], radius=260, fill=(58, 52, 60))   # shoulders
    return bg.filter(ImageFilter.GaussianBlur(40))


def place(frame, rgba, cx, cy, rot):
    im = rgba.rotate(rot, resample=Image.BICUBIC, expand=True)
    frame.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)), im)


def article():
    """Encyclopedia-style lead, marker on the phrase being said."""
    w, h = 900, 420; card = PaperCard(w, h, seed=4, tape_at=0.0)
    lines = ['The printing press', 'From the encyclopedia',
             'A printing press is a mechanical device for applying',
             'pressure to an inked surface resting upon a print medium,',
             'transferring the ink and spreading information quickly.']
    def draw(sheet, u):
        d = ImageDraw.Draw(sheet)
        d.text((48, 40), lines[0], font=ft(SERIF, 56), fill=INK)
        d.line([48, 118, w - 48, 118], fill=(180, 176, 170), width=2)
        d.text((48, 132), lines[1], font=ft(SANS, 26), fill=MUTED)
        for i, l in enumerate(lines[2:]):
            d.text((48, 196 + i * 52), l, font=ft(SANS, 32), fill=INK)
    tw = ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength('spreading information quickly', font=ft(SANS, 32))
    x0 = 48 + ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength('transferring the ink and ', font=ft(SANS, 32))
    return card.render(None, [Mark((x0, 196 + 2 * 52 + 4, x0 + tw, 196 + 2 * 52 + 40), 0.0)], 1.0, draw)


def fare():
    w, h = 860, 440; card = PaperCard(w, h, seed=9, tape_at=0.0)
    def draw(sheet, u):
        d = ImageDraw.Draw(sheet)
        d.text((50, 32), 'same flight, two ways', font=ft(POP_B, 34), fill=MUTED)
        d.text((50, 76), '$1,240', font=ft(POP_XB, 84), fill=(150, 146, 140))
        d.line([44, 150, 380, 124], fill=RED_PEN, width=11)
        d.text((50, 190), '$1,090', font=ft(POP_XB, 150), fill=GREEN_INK)
    tw = ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength('$1,090', font=ft(POP_XB, 150))
    return card.render(None, [Mark((50, 250, 50 + tw, 360), 0.0)], 1.0, draw)


def darktable():
    """Dark-mode screenshot: the swipe inverts so light text turns to ink on yellow."""
    w, h = 900, 300
    ui = Image.new('RGB', (w - 52, h - 52), (32, 33, 36)); d = ImageDraw.Draw(ui)
    rows = [('Route A', '2 stops', '$612'), ('Route B', '1 stop', '$684'), ('Route C', 'nonstop', '$798')]
    for i, (a, b, c) in enumerate(rows):
        y = 26 + i * 80
        d.text((30, y), a, font=ft(SANS, 34), fill=(232, 234, 237)); d.text((330, y), b, font=ft(SANS, 34), fill=(154, 160, 166))
        d.text((w - 52 - 150, y), c, font=ft(SANS, 36), fill=(232, 234, 237))
        if i < 2:
            d.line([20, y + 64, w - 72, y + 64], fill=(60, 64, 67), width=2)
    card = PaperCard(w, h, seed=12, tape_at=0.0)
    return card.render(ui, [Mark((w - 52 - 150, 26 + 80 + 4, w - 52 - 60, 26 + 80 + 44), 0.0)], 1.0)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, fn, rot in [('01_article_marker', article, -2), ('02_price_drop', fare, 1.5), ('03_darkmode_marker', darktable, -1.5)]:
        fr = backdrop(); place(fr, fn(), 540, 1500, rot)
        fr.save(OUT + name + '.jpg', quality=90)
        print(OUT + name + '.jpg')
