"""Cuts for the IMG_1858 reel (RPN pixel variant, Applied Compute $4.5B deal). Ranges are word indices (inclusive) into
edit/transcript.json (AssemblyAI).
Words always finish (repo rule): end >= word end + 120 ms, then on to the next 100 ms quiet point; start = last quiet
point before the onset. Pauses > 0.30 s inside a range are cut where the audio really has one. Frames: start DOWN, end UP
on the 1/30 s grid. Writes edit/<reel>/pieces.json + out_words.json. Usage: python3 cut.py [reel ...]"""
import json, math, os, re, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(f'{HERE}/..')
FPS, HOP, GAP = 30, 0.01, 0.30
SRC = {'cam': '/Users/harnoor/Movies/FCP/img1858-rpn-graphics/IMG_1858_clean.MOV'}   # lossless remux of ~/Desktop/IMG_1858.MOV: video + audio only (the 5 mebx metadata tracks dropped), FCP showed Missing Plug-in
WAV = {'cam': (f'{R}/audio/src16k.wav', 0.0)}
W = {'cam': json.load(open(f'{R}/edit/transcript.json'))['words']}

# mode: split = graphic on top, face below; full = full-screen graphic (camera hidden); face = full face
REELS = {
    'main': [
        ('cam', 62, 84, 'face'),      # "This 23-year-old Stanford dropout just closed the acquisition deal worth $4.5 billion for a company he started 18 months ago. How that happened?"  (phone in hand -> face; title on top, burst on "acquisition")  -- "closed" is wrong: signed, not closed (flag)
        ('cam', 123, 136, 'split'),   # "Yash, Rhythm, and Linden, all three went to Stanford, all three worked at OpenAI"  (Linden's launch tweet: "since @ypatil125, @rhythmrg, and I left OpenAI")
        ('cam', 157, 176, 'split'),   # "All of these three students had expertise in reasoning models, RL or infrastructure. All three are deadly combination."
        ('cam', 182, 202, 'face'),    # "(Now think about this way,) most engineers ... dependent on third-party models, closed source or open source. They were like, why not we combine"
        ('cam', 203, 210, 'split'),   # "infrastructure, data, compute, all together and sell it."  (real photos, hard cut on each word: server racks / rack cabling / H100 GPUs, then all three)
        ('cam', 263, 269, 'split'),    # "They went to customers like Cognition, Microsoft."  (Yash's Nov 2 update, full text: marks on Cognition, Microsoft)
        ('cam', 284, 300, 'split'),    # "why should you be using third-party models, why not we optimize for you with your own data?"  (same post: mark on "custom model training + production inference")
        ('cam', 339, 353, 'full'),    # "And now Palo Alto Networks is trying to make infrastructure more secure by purchasing it."  (Yash's Nov 18 deal post, full text: 4 paragraphs, too long for the top half -> full screen)
        ('cam', 354, 388, 'face'),    # "Fireworks was just hacked ... why not we acquire and package it with more security?"  (his read of the motive: no graphic)
        ('cam', 389, 399, 'split'),   # "And that's how they got one of the biggest exit offers."  (TBPN "ACQUIRED" post)
        ('cam', 400, 403, 'face'),    # "Another cool Stanford story."
        ('cam', 408, 419, 'face'),    # "What do you all think? Let me know in the comments below."
    ],
}
END_AT = {('cam', 403): 184.62}   # "story." runs straight into the dropped "What are you all-": cut just before that onset (energy rises at 184.63)
START_AT = {}
SKIP = set()


def env(src):
    path, off = WAV[src]; w = wave.open(path); sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    n = int(sr * HOP); x = x[:len(x) // n * n].reshape(-1, n)
    e = 20 * np.log10(np.sqrt((x ** 2).mean(1)) + 1e-6)
    return e[int(round(off / HOP)):]


ENV = {k: env(k) for k in WAV}
floor_at = lambda s, t: np.percentile(ENV[s][max(0, int(t / HOP) - 300):int(t / HOP) + 300], 8)
quiet = lambda s, t, thr: ENV[s][int(round(t / HOP)):int(round(t / HOP)) + 10].max() <= thr + 4


def end_of(s, i1):
    """>= 120 ms past the word, then on to a 100 ms quiet point. ASR onsets of the next word are often early, so the scan
    runs up to 0.5 s and stops only at a real onset (energy back above floor + 20 dB after a dip). If no quiet point
    comes first (run-on speech), cut in the energy valley between the two words."""
    ws = W[s]; e = ws[i1]['e']; fl = floor_at(s, e); thr = fl + 4; t = e + 0.12
    k = int(e / HOP); seen_dip = False
    for j in range(k, k + 50):
        v = ENV[s][j] - fl
        if v < 12: seen_dip = True
        if seen_dip and v > 20: onset = j * HOP; break
    else: onset = e + 0.5
    lim = max(onset - 0.03, e + 0.12)
    while t < lim and not quiet(s, t, thr): t += HOP
    if t < lim: return min(t + 0.02, lim), ''
    a, b = int((e - 0.05) / HOP), int(max(onset, e + 0.08) / HOP)
    return (a + int(np.argmin(ENV[s][a:b]))) * HOP, 'valley'


def start_of(s, i0):
    ws = W[s]; st = ws[i0]['s']; prv = ws[i0 - 1]['e'] if i0 > 0 else 0
    thr = floor_at(s, st) + 4; lo = max(st - 0.20, prv + 0.03); t = st - 0.04
    while t > lo and not quiet(s, t - 0.10, thr): t -= HOP
    return max(t, lo) if lo < st - 0.04 else st - 0.03


def build(name):
    pieces = []
    for k, (s, a, b, mode) in enumerate(REELS[name]):
        ws = W[s]; groups, cur = [], [a]
        for i in range(a + 1, b + 1):
            if i in SKIP: continue
            if ws[i]['s'] - ws[cur[-1] if cur else i - 1]['e'] > GAP or (cur and cur[-1] != i - 1): groups.append(cur); cur = []
            cur.append(i)
        groups.append(cur)
        merged = [groups[0]]
        for g in groups[1:]:
            e, note = end_of(s, merged[-1][-1]); st = start_of(s, g[0])
            if g[0] == merged[-1][-1] + 1 and (note == 'no-quiet' or st - e < 0.15): merged[-1] = merged[-1] + g
            else: merged.append(g)
        for g in merged:
            i0, i1 = g[0], g[-1]
            st = START_AT.get((s, i0), start_of(s, i0)); e, note = end_of(s, i1)
            if (s, i1) in END_AT: e, note = END_AT[(s, i1)], 'wave-fixed'
            pieces.append(dict(src=s, w0=i0, w1=i1, s=st, e=e, note=note, mode=mode, rng=k))
    for a_, b_ in zip(pieces, pieces[1:]):     # contiguous source across a layout change: one shared boundary, no overlap
        if a_['src'] == b_['src'] and b_['w0'] == a_['w1'] + 1 and a_['rng'] != b_['rng']:
            ws = W[a_['src']]; bd = max(ws[a_['w1']]['e'] + 0.02, min(b_['s'], (ws[a_['w1']]['e'] + ws[b_['w0']]['s']) / 2))
            a_['e'] = b_['s'] = bd; a_['note'] = 'contig'; a_['contig'] = True; b_['after_contig'] = True
    tl = 0
    for p in pieces:
        ws = W[p['src']]; nxt = ws[p['w1'] + 1]['s'] if p['w1'] + 1 < len(ws) else 1e9
        f0, f1 = (round(p['s'] * FPS) if p.get('after_contig') else math.floor(p['s'] * FPS)), math.ceil(p['e'] * FPS)
        if p.get('contig'): f1 = round(p['e'] * FPS)
        elif f1 / FPS > nxt - 0.02 and p['note'] != 'wave-fixed': f1 = math.floor(p['e'] * FPS)
        p.update(f0=f0, f1=f1, frames=f1 - f0, out0=tl / FPS, **{'in': f0 / FPS, 'out': f1 / FPS}); tl += f1 - f0
    for a_, b_ in zip(pieces, pieces[1:]):
        if a_['src'] == b_['src']: assert not (b_['f0'] < a_['f1'] and b_['f1'] > a_['f0']), ('replays source', a_, b_)
    out_words = []
    for p in pieces:
        for i in range(p['w0'], p['w1'] + 1):
            if i in SKIP: continue
            w = W[p['src']][i]; d = p['out0'] - p['in']
            out_words.append(dict(w=w['w'], s=round(w['s'] + d, 3), e=round(min(w['e'], p['out']) + d, 3), src=p['src'], i=i))
    os.makedirs(f'{R}/edit/{name}', exist_ok=True)
    json.dump(pieces, open(f'{R}/edit/{name}/pieces.json', 'w'), indent=1)
    json.dump(out_words, open(f'{R}/edit/{name}/out_words.json', 'w'), indent=1)
    print(f'\n{name}: {len(pieces)} pieces, {tl / FPS:.2f} s')
    for p in pieces:
        w = W[p['src']][p['w1']]; tail = p['out'] - w['e']; s = p['src']
        lvl = ENV[s][int(p['out'] / HOP) - 3:int(p['out'] / HOP)].mean() - floor_at(s, w['e'])
        word = re.sub(r'[^a-z0-9]', '', w['w'].lower())
        risky = word.endswith(('t', 's', 'd', 'k', 'ch')) or any(c.isdigit() for c in word)
        flag = ' <-- CHECK' if (tail < 0.12 and p['note'] not in ('contig', 'valley')) or p['note'] == 'no-quiet' else ''
        txt = ' '.join(W[s][i]['w'] for i in range(p['w0'], p['w1'] + 1))
        print(f"  {p['mode']:5} out {p['out0']:6.2f} {s:4} {p['in']:7.3f}-{p['out']:7.3f} tail {tail * 1000:4.0f}ms env +{lvl:4.1f}dB {'risky' if risky else '     '} {p['note']}{flag} | {txt[:70]}")


if __name__ == '__main__':
    for n in (sys.argv[1:] or REELS): build(n)
