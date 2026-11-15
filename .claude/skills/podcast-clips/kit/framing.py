"""9:16 framing from Apple Vision faces (edit/faces_1fps.txt, scripts/faces_all.swift on 1 fps frames).
Speaker B (guest) sits on the left of the 1920x1080 frame, speaker A (host) on the right. Each run of pieces on the same
speaker gets one static crop (median face over the run), so the frame never drifts inside a run and only changes on a cut.
- face: crop height Hc so the face is ~FACE_OUT px wide in the 1080x1920 output, face centre at y = FACE_Y,
  clamped to the source; punch=True tightens it by PUNCH.
- stack: B in the top 1080x960, A in the bottom 1080x960, each its own crop (back-and-forth exchanges).
Returns crops as (x, y, w, h) in source px."""
import os, statistics as st

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACE_OUT, FACE_Y, PUNCH = 360, 760, 1.12
SW, SH = 1920, 1080


def _load():
    F = {}
    for r in open(f'{ROOT}/edit/faces_1fps.txt'):
        p, _, rest = r.partition('.jpg')
        k = int(p[-5:]) - 1                     # frame k (1-based) of fps=1 ~ t = k-1 .. k
        best = {}
        for x in rest.split(';'):
            if not x.strip(): continue
            x, y, w, h = map(int, x.split())
            if w < 100: continue                 # passers-by in the plaza are far smaller
            side = 'B' if x + w / 2 < SW / 2 else 'A'
            if side not in best or w > best[side][2]:
                best[side] = (x + w / 2, y + h / 2, w)
        F[k] = best
    return F


FACES = _load()


def face_over(spk, t0, t1):
    pts = [FACES[k][spk] for k in range(int(t0), int(t1) + 1) if k in FACES and spk in FACES[k]]
    if not pts:   # widen the window
        pts = [FACES[k][spk] for k in range(int(t0) - 10, int(t1) + 11) if k in FACES and spk in FACES[k]]
    return tuple(st.median(p[i] for p in pts) for i in range(3))


def crop_face(cx, cy, fw, punch=False, out_w=1080, out_h=1920, face_y=FACE_Y, face_out=FACE_OUT):
    h = out_h * fw / face_out
    if punch: h /= PUNCH
    a = face_y / out_h
    h = min(h, cy / a, (SH - cy) / (1 - a), SH)       # keep the face at face_y without leaving the source
    w = h * out_w / out_h
    x = min(max(cx - w / 2, 0), SW - w)
    y = min(max(cy - a * h, 0), SH - h)
    return (round(x, 1), round(y, 1), round(w, 1), round(h, 1))


def frame(pieces, src_time):
    """adds p['crop'] (face) or p['crops'] = {'B': top, 'A': bottom} (stack) to every piece."""
    runs, cur = [], [pieces[0]]
    for p in pieces[1:]:
        if p['spk'] == cur[-1]['spk'] and p['layout'] == cur[-1]['layout'] and p['punch'] == cur[-1]['punch']:
            cur.append(p)
        else:
            runs.append(cur); cur = [p]
    runs.append(cur)
    for run in runs:
        t0, t1 = src_time(run[0])[0], src_time(run[-1])[1]
        if run[0]['layout'] == 'stack':
            cs = {}
            for spk in 'BA':
                cx, cy, fw = face_over(spk, t0, t1)
                cs[spk] = crop_face(cx, cy, fw, out_w=1080, out_h=960, face_y=540, face_out=250)
            for p in run: p['crops'] = cs
        else:
            cx, cy, fw = face_over(run[0]['spk'], t0, t1)
            c = crop_face(cx, cy, fw, run[0]['punch'])
            for p in run: p['crop'] = c
    return pieces
