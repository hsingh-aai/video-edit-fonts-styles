"""Camera framing for the IMG_0027 reel. The camera is a portrait phone selfie (1080x1920 after its -90 rotation tag), the
reel is 1080x1920. One static transform per piece from the Apple Vision median (never mirrored, uniform scale):
  split : face centred to 0 px in the lower half, hair top 15 px under the seam (y 975), head (hair to chin) 670 px tall,
          about 70% of the lower half, so the collar and shoulders stay in frame. Harnoor, Nov 25 2026: "you cropped too
          much on my face. That should not happen." His FCP fix went 1.0651 -> 0.925 scale on every split clip.
          s = min(centring need, 670 / head height), with NO floor at 1.0: never zoom in to cover the edges. Any open side
          strip is filled by the blurred copy (lane -3, finish.fill_mov).
  face  : whole frame, face centred, head top at y 420, zoom only as far as covering the frame and centring need
  full  : camera hidden (full-screen graphic)
Hair top / chin measured on this clip (frame at 30 s): hair 0.62 face-box heights above the Vision box, chin 0.03 below it.
Display px = s * source px; ox, oy = where the source's top-left lands. FCP: the portrait asset is conformed 'fit' into the
1080x1920 frame (scale 1 = 1 px/px), so FCP scale = s; position units are 1/100 of the frame height (19.2 px)."""
W, H, SEAM = 1080, 1920, 960
SW, SH = 1080, 1920
SEAM_HEAD, FACE_HEAD = 975, 420
HEAD_SPLIT = 670                     # hair-to-chin height on split shots (~70% of the 960 px lower half)
HAIR, CHIN = 0.62, 1.03
FIT = 1.0
S_MIN_SPLIT, S_MIN_FACE = 1.0, 1.08


def head_span(f):
    return f['y'] - HAIR * f['h'], f['y'] + CHIN * f['h']


def xform(mode, f):
    if mode == 'full' or f is None:
        return dict(mode=mode, s=1.0, ox=0.0, oy=0.0, fcp_scale=1.0, fcp_pos=[0.0, 0.0], fill=0)
    fx = f['x'] + f['w'] / 2; top, chin = head_span(f)
    need = 540 / max(1, min(fx, SW - fx))                             # zoom that keeps both edges covered with the face centred
    if mode == 'face':
        s = max(S_MIN_FACE, need, (H - FACE_HEAD) / (SH - top)); oy = min(0.0, FACE_HEAD - s * top); lo_y = 0   # head sits high in the source: lift it a few px rather than open a strip at the top
    else:
        s = min(need, HEAD_SPLIT / (chin - top)); oy = SEAM_HEAD - s * top; lo_y = SEAM   # no S_MIN_SPLIT floor: strips get the blur fill
    ox = 540 - s * fx
    uncovered = max(0, ox) + max(0, W - (ox + SW * s)) + max(0, oy - lo_y) + max(0, H - (oy + SH * s))
    xc, yc = ox + SW / 2 * s, oy + SH / 2 * s
    return dict(mode=mode, s=round(s, 4), ox=round(ox, 2), oy=round(oy, 2), face_x=round(ox + s * fx, 1), head_y=round(oy + s * top),
                chin_y=round(oy + s * chin), face_c=[round(ox + s * fx, 1), round(oy + s * (f['y'] + f['h'] / 2), 1)], face_w=round(s * f['w'], 1),
                fill=round(uncovered), fill_side=('left' if ox > 0 else 'right' if ox + SW * s < W else ''),
                fcp_scale=round(s / FIT, 4), fcp_pos=[round((xc - 540) / 19.2, 4), round((960 - yc) / 19.2, 4)])

# Frames at the very start that open full screen instead of split: for the first 15 frames of "This idiot" he is still
# turning round to the camera. The camera piece keeps playing underneath; FCP gets the first spine clip cut in two.
FULL_HEAD = {}
