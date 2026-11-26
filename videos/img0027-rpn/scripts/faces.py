"""Per-piece Apple Vision face boxes (rule: one static, face-centred crop per piece). ~3 samples a second (at least 5)
from the portrait 1080x1920 camera (auto-rotated) at 540 wide; largest face; median per piece, in source px. Camera pieces only.
Writes edit/<reel>/faces.json. Usage: python3 faces.py [reel ...]"""
import json, os, subprocess, sys
import numpy as np
from cut import R, SRC, REELS
SCR = os.path.expanduser('~/.cache/fast-rpn')


def run(name):
    pieces = json.load(open(f'{R}/edit/{name}/pieces.json')); d = f'{SCR}/faces_img0027'; os.makedirs(d, exist_ok=True); jobs = []
    for k, p in enumerate(pieces):
        if p['src'] != 'cam': continue
        dur = p['out'] - p['in']; n = max(5, int(round(dur * 3)))
        for j in range(n):
            t = p['in'] + dur * (j + 0.5) / n; f = f'{d}/c{t:09.3f}.jpg'
            if not os.path.exists(f):
                subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', SRC['cam'], '-frames:v', '1', '-vf', 'scale=540:-2', '-q:v', '3', f], check=True)
            jobs.append((k, f))
    B = {}
    files = sorted({f for _, f in jobs})
    for i in range(0, len(files), 200):
        for line in subprocess.run([f'{SCR}/faces_all'] + files[i:i + 200], capture_output=True, text=True).stdout.splitlines():
            path, _, rest = line.partition(' ')
            fs = [list(map(int, x.split())) for x in rest.split(';') if x.strip()]
            if fs: B[path] = max(fs, key=lambda b: b[2] * b[3])
    out = []
    for k, p in enumerate(pieces):
        bs = [B[f] for kk, f in jobs if kk == k and f in B]
        if not bs: out.append(None); continue
        a = np.array(bs) * 2; m = np.median(a, 0); sp = np.ptp(a[:, 0] + a[:, 2] / 2)
        out.append(dict(x=float(m[0]), y=float(m[1]), w=float(m[2]), h=float(m[3]), n=len(bs), spread=float(sp)))
        print(f"{name} p{k:02d} {p['mode']:5} faces {len(bs)} box {[round(v) for v in m]} x-spread {sp:.0f}")
    json.dump(out, open(f'{R}/edit/{name}/faces.json', 'w'), indent=1)


if __name__ == '__main__':
    for n in (sys.argv[1:] or REELS): run(n)
