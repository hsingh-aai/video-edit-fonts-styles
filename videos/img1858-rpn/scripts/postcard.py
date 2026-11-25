"""Clean full-text X post cards for posts whose board screenshot (and X's own embed) cut the text at "Show more".
Header (avatar, name, badges, handle, X logo) is the real header cropped from Harnoor's board screenshot; the text is the
exact full post text as read from the post page on x.com (Nov 24, 2026), set in SF Pro on the X light theme; then the
date line. The attached media is left off (as on the old cards). Returns marks (line rects per phrase) for assets.py.
Usage: imported by assets.py (POSTS); run alone to write assets/dl/<name>_full.png for a look."""
import os, re
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(f'{HERE}/..')
SF = '/System/Library/Fonts/SFNS.ttf'
W, PAD, FS, LH, PG = 1096, 32, 40, 50, 26
TXT, BLUE, GREY, RULE = (15, 20, 25), (29, 155, 240), (83, 100, 113), (207, 217, 222)

POSTS = {
    'linden': dict(board='b04.png', head=128, date='9:40 AM · Oct 29, 2025',
                   text="Introducing @appliedcompute. We build Specific Intelligence, to create the first generation of agent workforces.\n\n"
                        "It’s been an incredible six months since @ypatil125, @rhythmrg, and I left OpenAI to work on this problem together. "
                        "We’ve brought together an insanely talent-dense team and are growing quickly to meet customer demand.",
                   marks=['@ypatil125, @rhythmrg,', 'left OpenAI', 'insanely talent-dense']),
    'deal': dict(board='b00.png', head=128, date='2:06 PM · Nov 18, 2026',
                 text="Applied Compute has signed a definitive agreement to be acquired by Palo Alto Networks for $4.5B!\n\n"
                      "Rhythm, Linden, and I founded Applied Compute with a belief that was unusual at the time: that every company should own its "
                      "intelligence. We think training, serving, and improving proprietary models will become a normal part of running a company.\n\n"
                      "To do useful work, a model needs to access sensitive data and systems, comply with policies, and remain explainable, verifiable, "
                      "and auditable. This is the reason we've always prioritized security, and why joining Palo Alto Networks will help us go further "
                      "faster. Customers will still own and control their models, and I'm excited for all the ways our combined capabilities can serve "
                      "them even better.\n\n"
                      "Above all, I'm incredibly grateful for the AC team. A few dozen people in just over 18 months grew this company from zero revenue "
                      "to over $100M in annualized revenue run-rate, working with many of the world's most innovative companies. More to come soon.",
                 marks=['signed a definitive agreement', 'acquired by Palo Alto Networks for $4.5B!']),
    'update': dict(board='b09.png', head=128, date='9:17 AM · Nov 2, 2026',
                   text="Applied Compute update:\n\n"
                        "- crossed $100M annualized revenue run rate up from zero 18 months ago\n"
                        "- raised $350M at $3.25B led by Elad Gil\n"
                        "- 40% of customers use AC for both custom model training + production inference\n"
                        "- inference serving 1T tokens a day after launching 12 weeks ago\n"
                        "- 2X enterprise customers since last raise\n"
                        "- 3X team since January, 85% are researchers and engineers\n"
                        "- Working with customers like Microsoft, Shopify, Harvey, DoorDash, Cognition, Clay, Decagon and others\n\n"
                        "To move even faster we need people who are extremely technical AND extremely practical. If this is you, please reach out.",
                   marks=['Cognition,', 'Microsoft,', 'custom model training + production inference']),
}


def font(size):
    f = ImageFont.truetype(SF, size); f.set_variation_by_name('Regular'); return f


def build(name):
    P = POSTS[name]; f = font(FS); fd = font(30); sp = f.getlength(' ')
    lines, y = [], 0                                  # layout: (word, x, y) per word, paragraphs split on \n\n
    for k, para in enumerate(P['text'].split('\n\n')):
        for ln in para.split('\n'):                   # single newlines (bullet lists) start a new line, hanging indent after "- "
            x = 0; ind = f.getlength('- ') if ln.startswith('- ') else 0
            for wd in ln.split(' '):
                w = f.getlength(wd)
                if x and x + w > W - 2 * PAD: x = ind; y += LH
                lines.append((wd, x, y)); x += w + sp
            y += LH
        y += (PG if k < len(P['text'].split('\n\n')) - 1 else 0)
    head = Image.open(f'{R}/assets/board/{P["board"]}').convert('RGB').crop((0, 0, W, P['head']))
    ty = P['head'] + 6; dy = ty + y + 22; Ht = dy + 30 + 34
    im = Image.new('RGB', (W, Ht), head.getpixel((W - 60, P['head'] - 6))); im.paste(head, (0, 0)); d = ImageDraw.Draw(im)   # card bg = the screenshot's own bg
    for wd, x, yy in lines:
        col = BLUE if wd.startswith('@') else TXT
        if wd.startswith('@') and wd[-1] in ',.': d.text((PAD + x, ty + yy), wd[:-1], font=f, fill=BLUE); d.text((PAD + x + f.getlength(wd[:-1]), ty + yy), wd[-1], font=f, fill=TXT)
        else: d.text((PAD + x, ty + yy), wd, font=f, fill=col)
    d.text((PAD, dy), P['date'], font=fd, fill=GREY)
    marks = []
    for ph in P['marks']:                             # find the phrase as a run of words; one rect per line it spans
        toks = ph.split(' ')
        for i in range(len(lines) - len(toks) + 1):
            if [w for w, _, _ in lines[i:i + len(toks)]] == toks:
                rects = {}
                for wd, x, yy in lines[i:i + len(toks)]:
                    r = rects.setdefault(yy, [PAD + x, ty + yy - 4, 0, ty + yy + LH - 6]); r[2] = PAD + x + f.getlength(wd)
                marks.append([[round(v) for v in r] for r in rects.values()]); break
        else: raise SystemExit(f'mark not found: {ph}')
    out = f'{R}/assets/dl/{name}_full.png'; im.save(out)
    return out, marks


if __name__ == '__main__':
    for n in POSTS: print(build(n))
