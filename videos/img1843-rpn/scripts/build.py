"""IMG_1843 reel, RPN pixel variant, "token budget" look (copied from img1827-rpn; beats, burst, title and end card changed).
The opening title ("$250K IN / TOKENS", NVIDIA logo) is its own layer: title.mov (ProRes 4444 alpha, frame 0 -> burst), lane 3 "Title" in the FCPXML. Renders every non-face run (split: top half opaque, lower half clear;
full: whole frame; ext: whole frame with a clear window for the talk clip) and the end card as ProRes 4444 alpha, the
match-cut burst inside its split run, plus captions.mov, the SRT and runs.json for audio/finish.
Usage: <venv>/python build.py <reel> [all|runs|captions|stills t ...]"""
import json, os, subprocess, sys
from multiprocessing import get_context
from kit import *
from PIL import ImageFilter
from layout import xform

REEL = sys.argv[1] if len(sys.argv) > 1 else 'main'
ED = f'{R}/edit/{REEL}'; OUT = f'{R}/renders/{REEL}'; os.makedirs(OUT, exist_ok=True)
SCR = os.path.expanduser('~/.cache/fast-rpn')
CD = f'{R}/assets/cards'; CM = json.load(open(f'{CD}/cards.json'))
END_CARD = 75
PIECES = json.load(open(f'{ED}/pieces.json')); OW = json.load(open(f'{ED}/out_words.json')); FACES = json.load(open(f'{ED}/faces.json'))
WI = {(w['src'], w['i']): w for w in OW}
t_ = lambda i, src='cam': WI[(src, i)]['s']
e_ = lambda i, src='cam': WI[(src, i)]['e']
SPEECH = sum(p['frames'] for p in PIECES); TOTAL = SPEECH + END_CARD
RUNS = []
for p in PIECES:
    a = round(p['out0'] * FPS); b = a + p['frames']
    if RUNS and RUNS[-1][0] == p['mode'] and RUNS[-1][2] == a: RUNS[-1][2] = b
    else: RUNS.append([p['mode'], a, b])
from layout import FULL_HEAD
FH = FULL_HEAD.get(REEL, 0)
if FH: RUNS[0][1] = FH; RUNS.insert(0, ['full', 0, FH])
RUNS.append(['end', SPEECH, TOTAL])
mode_at = lambda t: next((m for m, a, b in RUNS if a <= round(t * FPS) < b), 'end')
runs_of = lambda m: [(a / FPS, b / FPS) for mm, a, b in RUNS if mm == m]
pin = lambda i, src='cam': next(p['out0'] for p in PIECES if p['w0'] == i and p['src'] == src)
piece_at = lambda t: next(k for k, p in enumerate(PIECES) if p['out0'] - 1e-6 <= t < p['out0'] + p['frames'] / FPS + 1e-6)


# ---------------- cards ----------------
_cards = {}


def card(name, maxw, maxh):
    k = (name, maxw, maxh)
    if k not in _cards:
        im = Image.open(f'{CD}/{name}.png').convert('RGBA'); c, s = page_card(im, maxw, maxh, r=26 if name == 'x_post' else 0)
        _cards[k] = (c, [[[v * s for v in r] for r in ph] for ph in CM.get(name, {}).get('marks', [])])
    return _cards[k]


_full = {}


def full_im(name):
    if name not in _full: _full[name] = Image.open(f'{CD}/{name}.png').convert('RGBA')
    return _full[name]


def page(name, t, marks_at=(), h=SEAM, maxw=960, maxh=780, src=None, cy=None, push=0.035, mdur=0.33, co=False, logo_top=None):
    """card centred in a canvas of height h; hard cut in (reference treatment), slow push, marker wipes at marks_at[i]
    (beat-relative; a (start, end) pair wipes over that span)"""
    fr = base(h); c, mk = card(name, maxw, maxh); c = c.copy()
    for i, m in enumerate(marks_at):
        if m is None or i >= len(mk): continue
        a, b = m if isinstance(m, tuple) else (m, m + mdur)
        marker(c, mk[i], (t - a) / max(0.1, b - a), dark=CM.get(name, {}).get('dark', False))
    z = 1 + push * clamp(t / 4.0); c = c.resize((round(c.width * z), round(c.height * z)), Image.LANCZOS)
    cy = cy if cy is not None else (h / 2 - (24 if src else 0))
    if co: cy = 70 + c.height / 2
    paste_c(fr, shadow(c), 540, cy)
    if src: tag(fr, src, cx=540, y=cy + c.height / 2 + 22, size=28)
    if logo_top:
        lg = logo(logo_top, 70); paste_c(fr, lg, 540, cy - c.height / 2 - 70)
    if co:                                   # magnified callout of the phrase being read (the latest mark that has started)
        live = [(i, m) for i, m in enumerate(marks_at) if m is not None and t >= (m[0] if isinstance(m, tuple) else m)]
        if live:
            i, m = live[-1]; a, b = m if isinstance(m, tuple) else (m, m + mdur)
            ci = callout(full_im(name), CM[name]['marks'][i], (t - a) / max(0.1, b - a), pad=3)
            paste_c(fr, shadow(ci), 540, (cy + c.height / 2 + 70 + h - 40) / 2 + 10)
    return fr


# ---------------- the match-cut burst (match-cut-intro skill: 4 frames an image, pinned to his head) ----------------
# Jensen Huang photos (Anders Eidesvik, Stanford, Apr 2026, CC BY 4.0 on Wikimedia Commons), each face (Apple Vision box,
# 1280 px thumbs) pinned to his face's centre and width: his head -> Jensen x7 -> his head. "He's back" as a match cut.
PORTRAITS = [('Jensen_huang_stanford_2026-04-30_009.jpg', (543, 555, 388, 388)), ('Jensen_huang_stanford_2026-04-09_030.jpg', (547, 616, 194, 194)),
             ('Jensen_huang_stanford_2026-04-30_011.jpg', (455, 490, 303, 303)), ('Jensen_huang_stanford_2026-04-09_033.jpg', (461, 432, 161, 161)),
             ('Jensen_huang_stanford_2026-04-30_005.jpg', (483, 338, 278, 278)),
             ('Jensen_huang_stanford_2026-04-30_036.jpg', (539, 532, 218, 218))]   # same six as img1805 (face boxes from there)
BU = dict(at=('cam', 91), items=[p for p, _ in PORTRAITS], credit='JENSEN HUANG PHOTOS: ANDERS EIDESVIK, WIKIMEDIA COMMONS, CC BY 4.0')
FPI = 4
B0 = round(t_(91) * FPS)                   # onset of "Jensen" (~3.5 s): later than the usual ~2 s so the title owns the opening; lands on the name
assert B0 + FPI * len(PORTRAITS) <= PIECES[0]['frames'], 'burst must stay inside the opening face piece'
_bp = PIECES[piece_at(B0 / FPS + 0.01)]; LAND = xform(_bp['mode'], FACES[piece_at(B0 / FPS + 0.01)])
TARGET = LAND['face_c']; SIZE = round(LAND['face_w'])
B1 = B0 + FPI * len(PORTRAITS)
for _k, (_m, _a, _b) in enumerate(RUNS):     # the burst gets its own graphics run, cut out of the face run around it
    if _m == 'face' and _a <= B0 and B1 <= _b:
        RUNS[_k:_k + 1] = [r for r in (['face', _a, B0], ['full', B0, B1], ['face', B1, _b]) if r[2] > r[1]]; break
_bimgs = {}


def burst_frame(k):
    if k not in _bimgs:
        fn, (x, y, w, h) = PORTRAITS[k]; im = Image.open(f'{R}/assets/burst/{fn}').convert('RGBA')
        kk = SIZE / w; lg = im.resize((max(1, round(im.width * kk)), max(1, round(im.height * kk))), Image.LANCZOS)
        cv = max(W / im.width, H / im.height); fr = im.resize((round(im.width * cv), round(im.height * cv)), Image.LANCZOS)   # blurred cover fill: no dark strip when the pinned photo doesn't reach an edge
        fr = fr.crop(((fr.width - W) // 2, (fr.height - H) // 2, (fr.width - W) // 2 + W, (fr.height - H) // 2 + H)).filter(ImageFilter.GaussianBlur(40)); fr.alpha_composite(lg, (round(TARGET[0] - (x + w / 2) * kk), round(TARGET[1] - (y + h / 2) * kk)))
        cr = text_im(BU['credit'], 24, INK, vt=True, track=1)
        ImageDraw.Draw(fr).rectangle([40, 1800, 40 + cr.width + 28, 1840], fill=(0, 0, 0, 190)); fr.alpha_composite(cr, (54, 1820 - cr.height // 2))
        _bimgs[k] = fr
    return _bimgs[k]


# ---------------- beats ----------------
SFX = []
CAP_X = {}
CAP_Y = {}
INFO = 'THE INFORMATION · TOKEN BUDGET PER ENGINEER, MONTHLY'


def beats_main():
    S = runs_of('split')
    top = [
        (pin(113), S[0][1], lambda r, a=pin(113): page('info_bars', r, marks_at=[t_(i) - a for i in (113, 117, 121, 122, 132, 136)], src=INFO, maxw=960, maxh=760)),   # Tesla .. Microsoft
        (pin(157), S[1][1], lambda r, a=pin(157): page('info_rest', r, marks_at=[t_(i) - a for i in (160, 161, 162, 163, 164, 165, 169)], src=INFO, maxw=960, maxh=760)),  # no-limit list, then NVIDIA
    ]
    SFX[:] = [('swell', pin(113)), ('tick', t_(113)), ('tick', t_(132)), ('tick', t_(136)), ('swell', pin(157)), ('tick', t_(169)), ('swell', SPEECH / FPS)]
    return top


TOP = beats_main()


# ---------------- opening title (own layer) ----------------
# Structure from the reference (small logo + a word on line 1, one huge heavy word on line 2, white, high in frame), drawn in
# the series' pixel type. Max 5 words; on screen from frame 0 (settled by frame 12), until the burst cuts in.
TITLE = dict(logo='nvidia_white', l1='$250K IN', l2='TOKENS', end=B0)
TITLE_Y = (215, 365)


def title_frame(t):
    fr = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if t * FPS >= TITLE['end'] - 1e-6: return fr
    g = Image.new('L', (1, 560)); g.putdata([int(150 * (1 - y / 560) ** 1.6) for y in range(560)])
    sh = Image.new('RGBA', (W, 560), (0, 0, 0, 255)); sh.putalpha(g.resize((W, 560)))
    fr.alpha_composite(fade(sh, ease(t / 0.2)))
    lg = logo(TITLE['logo'], 64, maxw=220); num, word = TITLE['l1'].split(' ', 1)
    n_im = text_im(num, 118, ACC, vt=True, track=2); w_im = text_im(word, 74, INK, track=4)
    l1 = Image.new('RGBA', (lg.width + 28 + n_im.width + 24 + w_im.width, max(lg.height, n_im.height, w_im.height)), (0, 0, 0, 0))
    l1.alpha_composite(lg, (0, (l1.height - lg.height) // 2)); l1.alpha_composite(n_im, (lg.width + 28, (l1.height - n_im.height) // 2))
    l1.alpha_composite(w_im, (lg.width + 52 + n_im.width, (l1.height - w_im.height) // 2 + 4))
    l2 = text_im(TITLE['l2'], 206, INK, track=10, wt='Bold')
    slide_in(fr, l1, 540 - l1.width / 2, TITLE_Y[0] - l1.height / 2, t + 0.05)
    slide_in(fr, l2, 540 - l2.width / 2, TITLE_Y[1] - l2.height / 2 + 30, t - 0.06)
    return fr


# ---------------- end card ----------------
CHEAT = ('TOKEN BUDGETS // MONTH', [
    ('THE BAR', '$250K A YEAR', "JENSEN HUANG, GTC 2026: HALF A $500K ENGINEER'S PAY", ['nvidia_white']),
    ('THE TOP', 'NVIDIA $35-50K', 'PER MONTH, SO $420-600K A YEAR', []),
    ('BIG TECH', 'MSFT $10K · APPLE $4K', 'UBER · ATLASSIAN · RIPPLING $2K · TESLA $800', []),
    ('NO LIMIT', 'UNLIMITED', 'ANTHROPIC · OPENAI · ORACLE · SNOWFLAKE · REPLIT + 6', []),
    ('THE RANGE', 'DISNEY $50-$25K', 'WORKDAY $100-$300 · LOWEST CAP ON THE CHART', [])])


def cheat(t):
    fr = base(H); title, rows = CHEAT; y = 250
    paste_c(fr, mixed(title, 64, INK, track=5), 540, y)
    paste_c(fr, text_im('CHEAT SHEET // SCREENSHOT THIS', 34, DIM, vt=True, track=3), 540, y + 76)
    for k, (nm, chp, note, cos) in enumerate(rows):
        a = ease((t - 0.1 - k * 0.12) / 0.2)
        if a <= 0: continue
        yy = 420 + k * 236; row = Image.new('RGBA', (920, 210), (0, 0, 0, 0)); d = ImageDraw.Draw(row)
        row.alpha_composite(text_im(f'0{k + 1}', 44, ACC, vt=True), (0, 6))
        row.alpha_composite(mixed(nm, 46, INK, track=3), (80, 6))
        ci = text_im(chp, 44, GRAPH, vt=True, track=2); d.rectangle([80, 72, 80 + ci.width + 28, 72 + 58], fill=ACC)
        row.alpha_composite(ci, (94, 72 + (58 - ci.height) // 2))
        row.alpha_composite(text_im(note, 30, DIM, vt=True, track=2), (80, 148))
        lx = 920
        for co in reversed(cos):
            im = logo(co, 44, maxw=200); lx -= im.width; row.alpha_composite(im, (lx, 6 + (44 - im.height) // 2)); lx -= 24
        fr.alpha_composite(fade(row, a), (100, yy))
    if t > 0.8: paste_c(fr, text_im('SOURCES: THE INFORMATION · ALL-IN PODCAST, GTC 2026', 26, DIM, vt=True, track=2), 540, 1660)
    diff_seam(fr, 1790)
    return fr


def run_frame(f):
    t = f / FPS; m = mode_at(t)
    if m == 'end': return cheat(t - SPEECH / FPS)
    if B0 <= f < B1: return burst_frame((f - B0) // FPI)
    k = max(k for k, (a, b, fn) in enumerate(TOP) if a - 1e-6 <= t); a, b, fn = TOP[k]; im = fn(t - a)
    if m == 'full':
        assert im.size == (W, H), (f, m, k, im.size); return im
    assert im.size == (W, SEAM), (f, m, k, im.size)
    diff_seam(im); out = Image.new('RGBA', (W, H), (0, 0, 0, 0)); out.paste(im, (0, 0)); return out


# ---------------- captions ----------------
def cw(w): return w['w'].strip('.,?!:').upper()


SIGN = []
SIGN_I = set()


def chunks():
    out, cur = [], []
    for w in [w for w in OW if not (w['src'] == 'cam' and w['i'] in SIGN_I)]:
        txt = ' '.join(cw(x) for x in cur + [w])
        if cur and (len(cur) >= 3 or len(txt) > 14 or cur[-1]['w'][-1] in '.,?!:' or w['i'] != cur[-1]['i'] + 1 or w['src'] != cur[-1]['src']):
            out.append(cur); cur = []
        cur.append(w)
    out.append(cur)
    caps = [(' '.join(cw(x) for x in c), c[0]['s'], c[-1]['e']) for c in out]
    end = t_(SIGN[0][1]) if SIGN else SPEECH / FPS
    return [(s, a, min(caps[i + 1][1] if i + 1 < len(caps) and caps[i + 1][1] - e < 0.6 else e + 0.25, end)) for i, (s, a, e) in enumerate(caps)]


CAPS = chunks()


def cap_im(s):
    return [text_im(p, 60, ACC, vt=True, track=1) if any(ch.isdigit() for ch in p) else text_im(p, 46, INK, track=2) for p in s.split(' ')]


def caption_frame(t):
    fr = Image.new('RGBA', (W, H), (0, 0, 0, 0)); m = mode_at(t); f = round(t * FPS)
    if m == 'end' or B0 <= f < B1: return fr
    if SIGN and t >= t_(SIGN[0][1]):
        k = max(j for j, (s, i) in enumerate(SIGN) if t >= t_(i) or j == 0); s, i = SIGN[k]
        tt = t - t_(i); im = text_im(s, 96 if len(s) < 10 else 80, INK if k != len(SIGN) - 1 else ACC, track=4); a = ease(tt / 0.13)
        sm = smear(shadow(im), 1 - a); fr.alpha_composite(fade(sm, min(1, a * 2)), (round(540 - im.width / 2 - (1 - a) * 160 - (sm.width - im.width - 6)), 1440))
        return fr
    c = next((c for c in CAPS if c[1] - 1e-6 <= t < c[2]), None)
    if not c: return fr
    cy = next((y for (a, b), y in CAP_Y.items() if a - 1e-6 <= t < b), {'split': SEAM, 'full': 1352, 'face': 1500}[m])
    ims = cap_im(c[0]); cx = next((x for (a, b), x in CAP_X.items() if a - 1e-6 <= t < b), 540)
    if cx == 540: box_caption(ims, cy, fr)
    else:
        tmp = Image.new('RGBA', (W, 200), (0, 0, 0, 0)); box_caption(ims, 100, tmp); bb = tmp.getbbox()
        fr.alpha_composite(tmp.crop(bb), (round(cx - (bb[2] - bb[0]) / 2), round(cy - 36)))
    return fr


def srt():
    ts = lambda t: f'{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{int(round(t % 1 * 1000)) % 1000:03d}'
    allc = CAPS + [(s, t_(i), (t_(SIGN[j + 1][1]) if j + 1 < len(SIGN) else SPEECH / FPS)) for j, (s, i) in enumerate(SIGN)]
    return '\n'.join(f'{k + 1}\n{ts(a)} --> {ts(e)}\n{s}\n' for k, (s, a, e) in enumerate(allc))


# ---------------- writers ----------------
def prores(path):
    return subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                             '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', '-vendor', 'apl0', path], stdin=subprocess.PIPE)


GFX = [r for r in RUNS if r[0] != 'face']


def render_run(k):
    m, a, b = GFX[k]; path = f'{OUT}/run_{k:02d}_{m}.mov'; pr = prores(path)
    for f in range(a, b): pr.stdin.write(run_frame(f).tobytes())
    pr.stdin.close(); pr.wait(); return path


def render_caps(_=None):
    pr = prores(f'{OUT}/captions.mov')
    for f in range(TOTAL): pr.stdin.write(caption_frame(f / FPS).tobytes())
    pr.stdin.close(); pr.wait(); return 'captions'


def render_title(_=None):
    pr = prores(f'{OUT}/title.mov')
    for f in range(TITLE['end']): pr.stdin.write(title_frame(f / FPS).tobytes())
    pr.stdin.close(); pr.wait(); return 'title'


def job(x): return render_caps() if x == 'cap' else render_title() if x == 'title' else render_run(x)


if __name__ == '__main__':
    what = sys.argv[2] if len(sys.argv) > 2 else 'all'
    for (a, b, _), (a2, _, _) in zip(TOP, TOP[1:]): assert b <= a2 + 1e-6, (a, b, a2)
    json.dump({'runs': RUNS, 'gfx': [[m, a, b, f'run_{k:02d}_{m}.mov'] for k, (m, a, b) in enumerate(GFX)], 'sfx': SFX, 'total_frames': TOTAL,
               'speech_frames': SPEECH, 'captions': CAPS, 'title': dict(file='title.mov', start=0, frames=TITLE['end'], text=f"{TITLE['l1']} {TITLE['l2']}"), 'burst': dict(b0=B0, b1=B1, fpi=FPI, target=TARGET, size=SIZE, items=BU['items'])},
              open(f'{OUT}/runs.json', 'w'), indent=1)
    open(f'{OUT}/{REEL}.srt', 'w').write(srt())
    if what == 'stills':
        d = f'{SCR}/st_{REEL}'; os.makedirs(d, exist_ok=True)
        for t in map(float, sys.argv[3:]):
            fr = run_frame(round(t * FPS)) if mode_at(t) != 'face' else Image.new('RGBA', (W, H), (60, 60, 60, 255))
            bg = Image.new('RGBA', (W, H), (60, 60, 60, 255)); bg.alpha_composite(fr); bg.alpha_composite(caption_frame(t)); bg.alpha_composite(title_frame(t)); bg.convert('RGB').resize((540, 960)).save(f'{d}/g_{t:05.2f}.png')
        sys.exit()
    jobs = ([] if what == 'captions' else list(range(len(GFX)))) + ([] if what == 'runs' else ['cap', 'title'])
    with get_context('fork').Pool(6) as pool: print(pool.map(job, jobs))
