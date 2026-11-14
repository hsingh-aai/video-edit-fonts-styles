"""Spec word ranges -> frame-exact spine pieces that never clip a word.

Rules (Harnoor, Nov 14 2026: "let that word finish"):
- a piece ends at least END_MIN (120 ms) after the ASR word end, then runs on to the next quiet point: the first
  30 ms where the 10 ms RMS envelope is back at the local noise floor (+4 dB). Never inside the word's decay.
- a piece starts a little before the word onset: back to the last quiet point within START_MAX, at least 40 ms early.
- the end frame is rounded UP and the start frame DOWN (30 fps grid), unless that would reach into a word we drop.
- pacing comes only from removing pauses between phrases (gaps > 0.3 s inside a range are cut out).
Every cut is checked (check()): envelope at the cut vs the floor, plus a list of the risky word endings.
Usage: python3 pieces.py   (prints the pieces and the cut check for every reel)"""
import json, math, os, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spec import REELS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS, GAP, END_MIN, END_MAX, START_MIN, START_MAX = 30, 0.35, 0.12, 0.60, 0.04, 0.20
QWIN, QDB = 0.10, 8   # quiet = 100 ms with the envelope never above floor + 8 dB (a stop closure inside 'per-cent' is shorter)
HOP = 0.01
W = json.load(open(f'{ROOT}/edit/transcript.json'))['words']


def _env():
    p = f'{ROOT}/edit/env.npy'
    if os.path.exists(p):
        return np.load(p)
    with wave.open(f'{ROOT}/audio/source.wav') as w:
        sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    n = int(sr * HOP); x = x[:len(x) // n * n].reshape(-1, n)
    e = 20 * np.log10(np.sqrt((x ** 2).mean(1)) + 1e-6)
    np.save(p, e)
    return e


ENV = _env()


def floor_at(t):
    i = int(t / HOP)
    return np.percentile(ENV[max(0, i - 300):i + 300], 8)


def quiet(t, thr):
    """True if the QWIN from t is at the floor (thr = floor + 4; noisy outdoor floor, so allow QDB - 4 more on peaks)."""
    i = int(round(t / HOP))
    return ENV[i:i + int(QWIN / HOP)].max() <= thr - 4 + QDB


def end_of(i1, keep_next):
    e = W[i1]['e']
    nxt = W[i1 + 1]['s'] if i1 + 1 < len(W) else e + 2
    thr = floor_at(e) + 4
    lim = min(max(e + END_MAX, nxt - 0.03), e + 1.2, nxt - 0.03) if not keep_next else e + END_MAX
    t = e + END_MIN
    while t < lim and not quiet(t, thr):
        t += HOP
    note = '' if t < lim else 'no-quiet'
    t = min(max(t + 0.02, e + END_MIN), lim if not keep_next else t + 0.02)
    if t < e + END_MIN:
        note = 'next-word-close'
    return t, note


def start_of(i0):
    s = W[i0]['s']
    prv = W[i0 - 1]['e'] if i0 > 0 else 0
    thr = floor_at(s) + 4
    lo = max(s - START_MAX, prv + 0.03)
    t = s - START_MIN
    while t > lo and not quiet(t - QWIN, thr):
        t -= HOP
    return max(min(t, s - START_MIN), lo if lo < s - START_MIN else s - 0.02)


def build(name):
    spec = REELS[name]
    rs = [(r[0], r[1], r[2] if len(r) > 2 else {}) for r in spec['ranges']]
    pieces = []
    for k, (a, b, prm) in enumerate(rs):
        groups, cur = [], [a]
        for i in range(a + 1, b + 1):
            if W[i]['s'] - W[i - 1]['e'] > GAP:
                groups.append(cur); cur = []
            cur.append(i)
        groups.append(cur)
        # a pause the ASR sees but the audio doesn't (the word's tail runs into it, e.g. 'per-cent'): don't cut there
        merged = [groups[0]]
        for g in groups[1:]:
            if end_of(merged[-1][-1], False)[1] == 'no-quiet':
                merged[-1] = merged[-1] + g
            else:
                merged.append(g)
        groups = merged
        for g in groups:
            i0, i1 = g[0], g[-1]
            s = start_of(i0)
            e, note = end_of(i1, False)
            spk = max('AB', key=lambda c: sum(W[i]['e'] - W[i]['s'] for i in range(i0, i1 + 1) if W[i]['spk'] == c))
            pieces.append(dict(w0=i0, w1=i1, s=s, e=e, note=note, spk=spk, layout=prm.get('layout', 'face'),
                               punch=prm.get('punch', False), rng=k))
    # source-contiguous neighbours (next piece starts at the next word, tiny gap): cut at the gap midpoint
    for p, q in zip(pieces, pieces[1:]):
        if q['w0'] == p['w1'] + 1 and W[q['w0']]['s'] - W[p['w1']]['e'] <= GAP:
            m = (W[p['w1']]['e'] + W[q['w0']]['s']) / 2
            p['e'] = q['s'] = m; p['note'] = 'contiguous'
    t = 0
    for p in pieces:
        nxt_s = W[p['w1'] + 1]['s'] if p['w1'] + 1 < len(W) else 1e9
        prv_e = W[p['w0'] - 1]['e'] if p['w0'] > 0 else -1
        p['f0'] = math.floor(p['s'] * FPS)      # always round the start DOWN: never clip an onset
        p['f1'] = math.ceil(p['e'] * FPS)
        if p['f1'] / FPS > nxt_s and p['note'] != 'contiguous': p['f1'] = math.floor(p['e'] * FPS)
        p['frames'] = p['f1'] - p['f0']
        p['tl'] = t; t += p['frames']
    return pieces, t


RISKY = ('t', 's', 'd', 'k', 'ch', 'ts', 'nt', 'st')


def check(name, pieces):
    """every cut boundary: envelope at the cut vs floor; risky endings listed."""
    rows = []
    for p in pieces:
        w = W[p['w1']]
        word = w['w'].strip('.,?!-').lower()
        tail = p['f1'] / FPS - w['e']
        lvl = ENV[int(p['f1'] / FPS / HOP) - 3:int(p['f1'] / FPS / HOP)].mean() - floor_at(w['e'])
        risky = word.endswith(RISKY) or any(c.isdigit() for c in word) or 'percent' in word or '%' in word
        head = W[p['w0']]['s'] - p['f0'] / FPS
        rows.append((p['w1'], w['w'], round(tail * 1000), round(lvl, 1), round(head * 1000), risky, p['note']))
    return rows


if __name__ == '__main__':
    for n in REELS:
        ps, tot = build(n)
        print(f'== {n}: {len(ps)} pieces, {tot / FPS:.2f} s')
        for r in check(n, ps):
            flag = ' <-- CHECK' if r[6] != 'contiguous' and (r[2] < 120 or r[3] > 8) else ''
            print(f'   end w{r[0]:<5} {r[1]:<16} tail {r[2]:>4} ms  env@cut +{r[3]:>5} dB  head {r[4]:>4} ms  {"risky" if r[5] else ""} {r[6]}{flag}')
