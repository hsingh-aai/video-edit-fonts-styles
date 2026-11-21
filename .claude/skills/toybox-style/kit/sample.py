"""Toybox sample stills (styles/samples/toybox/) and the gallery screenshot (styles/screenshots/toybox.jpg).
Usage: ~/Developer/video-use/.venv/bin/python sample.py <repo> <out_dir> <screenshot_path>
Every card here is drawn placeholder art ("sample lesson", made-up numbers) and the face is a drawn
silhouette. In a real build the cards are the real product screenshots and the lower half is Harnoor."""
import sys; sys.path.insert(0, sys.argv[1] + '/.claude/skills/toybox-style/kit')
import toybox as tb
from PIL import Image, ImageDraw, ImageFont

OUT, SHOT = sys.argv[2], sys.argv[3]
MONO = tb.font(tb.CHIP_FONT, 30)
HEX = [(130, 170, 240), (240, 150, 150), (150, 210, 160), (250, 200, 110), (190, 160, 240)]


def hexagon(d, cx, cy, r, col, label):
    pts = [(cx + r * x, cy + r * y) for x, y in [(0, -1), (0.87, -0.5), (0.87, 0.5), (0, 1), (-0.87, 0.5), (-0.87, -0.5)]]
    d.polygon([(x + 6, y + 10) for x, y in pts], fill=(60, 60, 90))
    d.polygon(pts, fill=col, outline=(40, 40, 70), width=4)
    d.text((cx, cy), label, font=tb.font(tb.CHIP_FONT, 24), fill=(30, 30, 50), anchor='mm')


def lesson(w=860, h=1100, title='Sample lesson', nodes=3, steps=True):
    """drawn placeholder of an interactive-lesson screen: title, stat chips, a node diagram, a step tracker."""
    im = Image.new('RGB', (w, h), tb.SITE_CREAM); d = ImageDraw.Draw(im)
    d.text((44, 60), title, font=tb.font(tb.ART_FONT, 54), fill=(30, 30, 40))
    for i, (k, v) in enumerate([('USERS', '120,000'), ('REQ / S', '4,000'), ('LATENCY', '90 ms')]):
        x = 44 + i * 260
        d.rounded_rectangle((x, 160, x + 240, 250), 14, fill=(252, 248, 240), outline=(200, 190, 175), width=2)
        d.text((x + 18, 178), k, font=tb.font(tb.CHIP_FONT, 20), fill=(120, 110, 100))
        d.text((x + 18, 205), v, font=tb.font(tb.ART_FONT, 30), fill=(30, 30, 40))
    pos = [(w * 0.3, h * 0.52), (w * 0.62, h * 0.4), (w * 0.72, h * 0.62), (w * 0.45, h * 0.7), (w * 0.2, h * 0.75)][:nodes]
    for a, b in zip(pos, pos[1:]):
        d.line((a, b), fill=(60, 60, 90), width=5)
        for k in range(1, 4):
            d.ellipse((a[0] + (b[0] - a[0]) * k / 4 - 8, a[1] + (b[1] - a[1]) * k / 4 - 8,
                       a[0] + (b[0] - a[0]) * k / 4 + 8, a[1] + (b[1] - a[1]) * k / 4 + 8), fill=(240, 150, 60))
    for i, (x, y) in enumerate(pos):
        hexagon(d, x, y, 78, HEX[i % len(HEX)], ['App', 'Cache', 'DB', 'Queue', 'CDN'][i])
    if steps:
        d.text((44, h - 130), 'IN THIS LESSON', font=tb.font(tb.CHIP_FONT, 22), fill=(80, 80, 90))
        for i in range(10):
            x = 70 + i * 74
            d.ellipse((x - 22, h - 80, x + 22, h - 36), fill=(200, 230, 180) if i < 3 else (252, 248, 240), outline=(80, 80, 90), width=2)
            d.text((x, h - 58), str(i + 1), font=tb.font(tb.CHIP_FONT, 20), fill=(40, 40, 50), anchor='mm')
    return im


def checklist(w=860, h=1000):
    im = Image.new('RGB', (w, h), tb.SITE_CREAM); d = ImageDraw.Draw(im)
    d.text((44, 50), 'Recap', font=tb.font(tb.ART_FONT, 56), fill=(30, 30, 40))
    for i, line in enumerate(['One front door for many servers', 'Health checks drop dead nodes', 'Spread load, not just traffic',
                              'Plan for the node that fails', 'Measure before you scale']):
        y = 170 + i * 140
        d.rounded_rectangle((44, y, 92, y + 48), 10, fill=(120, 190, 110))
        d.line((56, y + 24, 66, y + 36, 82, y + 12), fill='white', width=6)
        d.text((120, y + 24), line, font=MONO, fill=(40, 40, 50), anchor='lm')
    return im


def face_placeholder():
    """drawn stand-in for the lower half (in a build: the avatar or camera, face centred)."""
    im = Image.new('RGB', (tb.W, tb.HALF), (150, 185, 210)); d = ImageDraw.Draw(im)
    for y in range(tb.HALF):
        d.line((0, y, tb.W, y), fill=(int(150 + 60 * y / tb.HALF), int(185 + 30 * y / tb.HALF), 210))
    d.ellipse((380, 150, 700, 530), fill=(70, 80, 100))          # head
    d.rounded_rectangle((200, 560, 880, 1200), 240, fill=(55, 65, 85))  # shoulders
    d.text((540, 900), 'face here (centred)', font=tb.font(tb.CHIP_FONT, 30), fill=(220, 225, 235), anchor='mm')
    return im


def save(fr, name):
    fr.convert('RGB').save(f'{OUT}/{name}.jpg', quality=90); return fr


bg = tb.paper_bg()
# 1. the open: hard 50/50 split, lesson on top, face below, caption on the seam
top = lesson(1080, 960, 'Sample lesson', nodes=3)
save(tb.caption(tb.split(top, face_placeholder()), 'someone just built', tb.HALF), '1_split_open')

# 2. blue paper card with bubble-letter title art (also the gallery screenshot)
fr = bg.copy()
im, xy = tb.zoom_in(tb.card(lesson()), 0, 2, tb.W / 2, 1120); fr.alpha_composite(im, xy)
fr.alpha_composite(tb.word_art('free', 120), (tb.W // 2 - tb.word_art('free', 120).width // 2, 90))
a2 = tb.word_art('system design', 92); fr.alpha_composite(a2, (tb.W // 2 - a2.width // 2, 225))
tb.caption(fr, 'every diagram is', 1840)
save(fr, '2_title_card').convert('RGB').resize((540, 960)).save(SHOT, quality=88)

# 3. three-card stack, one card per named example
fr = bg.copy()
for j, title in enumerate(['URL shortener', 'News feed', 'Chat system']):
    im, xy = tb.zoom_in(tb.card(lesson(1000, 900, title, nodes=4, steps=False), width=640, aspect=1.62), 0, 2, tb.W / 2, 640 + j * 430, push=0.02)
    fr.alpha_composite(im, xy)
save(tb.caption(fr, 'a chat system', 330), '3_stack')

# 4. checklist card on blue
fr = bg.copy()
im, xy = tb.zoom_in(tb.card(checklist()), 0, 2, tb.W / 2, 1050); fr.alpha_composite(im, xy)
save(tb.caption(fr, 'with a checklist', 330), '4_checklist')

# 5. CTA on the split: keyword pill over the visual, caption on the seam
fr = tb.split(lesson(1080, 960, 'Sample lesson', nodes=5), face_placeholder())
p = tb.cta_pill('scale'); fr.alpha_composite(p, (tb.W // 2 - p.width // 2, 770 - p.height // 2))
save(tb.caption(fr, 'comment scale and', tb.HALF), '5_cta')
print('ok')
