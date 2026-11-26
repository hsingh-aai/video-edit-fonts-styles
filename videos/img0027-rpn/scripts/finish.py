"""Camera layout, preview and FCPXML 1.14 for the IMG_0027 reel (camera: portrait 1080x1920 30p HEVC via a -90 rotation tag).
One spine clip per cut piece, each with one static transform from layout.py (face centred to 0 px, never mirrored):
  split : lower half, hair top 50 px under the seam; the top half sits under the opaque top-half run on lane 1
  face  : whole frame, 1.8x
  full  : hidden under the full-screen run (kept on the spine at real source in/out so the audio and the cut stay his)
  ext   : the Lauren Tan excerpt (30p transcode of 40-52 s of her talk), fit to width, under the ext run's clear window
Lanes: 1 graphics runs (ProRes 4444), 2 captions, 3 "Title" (opening title, own role so it can be disabled/deleted alone), -1 bed, -2 SFX. Custom LUT on every camera clip (img1769-rpn.cube).
Usage: <venv>/python finish.py <reel> [preview|fcpxml|all]"""
import json, os, re, shutil, subprocess, sys, urllib.parse
from fractions import Fraction as Fr
from xml.sax.saxutils import quoteattr as q
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(f'{HERE}/..')
sys.path.insert(0, HERE)
from cut import SRC
from layout import xform, FULL_HEAD
W, H, FPS, SEAM = 1080, 1920, 30, 960
REEL = sys.argv[1] if len(sys.argv) > 1 else 'main'
TITLES = {'main': 'Software Factories, ep. 1'}
ED = f'{R}/edit/{REEL}'; OUT = f'{R}/renders/{REEL}'; G = os.path.expanduser('~/Movies/FCP/img0027-rpn-graphics')
# A bare Custom LUT (no LUT file inside) shows as "Missing Plug-in" in FCP 13 (IMG_0027), so it's off by default:
# the grade is baked into the MP4 only; in FCP add Custom LUT by hand and pick the .cube. FCP_LUT=1 puts the bare effect back.
FCP_LUT = os.environ.get('FCP_LUT') == '1'
LUT_TAG = '\n            <filter-video ref="r1" name="Custom LUT"/>' if FCP_LUT else ''
LUT = os.path.expanduser('~/Movies/FCP/img0027-rpn-graphics/img0027-rpn.cube')   # the img1769 grade (same office, same painting), copied
SCR = os.path.expanduser('~/.cache/fast-rpn')
pieces = json.load(open(f'{ED}/pieces.json')); faces = json.load(open(f'{ED}/faces.json')); RJ = json.load(open(f'{OUT}/runs.json'))


def segments():
    segs, off = [], 0
    for k, p in enumerate(pieces):
        L = xform(p['mode'], faces[k]); assert not L['fill'] or p['mode'] == 'split', ('needs a blurred backdrop', k, L)   # split: blurred fill under the open strip (lane -3)
        segs.append(dict(piece=k, src=p['src'], offset=off, start=p['f0'], dur=p['frames'], run=p['mode'], L=L)); off += p['frames']
    fh = FULL_HEAD.get(REEL, 0)
    if fh:                                   # the opening frames play under a full-screen graphic: one clip cut in two, same source, no gap
        s0 = segs[0]; head = dict(s0, dur=fh, run='full', L=xform('full', None))
        segs[0] = dict(s0, offset=fh, start=s0['start'] + fh, dur=s0['dur'] - fh); segs.insert(0, head)
    return segs


def fill_mov(s):
    """blurred, darker copy of the piece that covers the lower half (top half clear), ProRes 4444 alpha: lane -3 in FCP,
    under the camera, so the strip the centred crop leaves open shows the room, never black (rpn-style rule)"""
    p = f'{OUT}/blurfill_{s["piece"]:02d}.mov'
    if os.path.exists(p): return p
    fy = faces[s['piece']]['y'] + faces[s['piece']]['h'] / 2; y0 = int(min(max(0, fy - 480), 960))
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', f"{s['start'] / FPS:.4f}", '-i', SRC['cam'], '-filter_complex',
                    f"[0:v]fps=30,setpts=PTS-STARTPTS,lut3d='{LUT}',crop=1080:960:0:{y0},gblur=sigma=40,eq=brightness=-0.10:saturation=0.8,format=rgba[f];"
                    f"color=black@0.0:s={W}x{H}:r=30,format=rgba[bg];[bg][f]overlay=0:{SEAM}:shortest=1",
                    '-frames:v', str(s['dur']), '-an', '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', '-vendor', 'apl0', p], check=True)
    return p


def preview():
    segs = segments(); d = f'{SCR}/base_{REEL}'; os.makedirs(d, exist_ok=True); parts = []
    for i, s in enumerate(segs):
        L = s['L']; out = f'{d}/s{i:02d}.mp4'; parts.append(out); n = s['dur']
        if s['run'] == 'full':
            cmd = ['-f', 'lavfi', '-i', f'color=black:s={W}x{H}:r=30']
        elif s['run'] == 'ext':
            cmd = ['-ss', f"{s['start'] / FPS:.4f}", '-i', SRC['pot'], '-filter_complex',
                   f"[0:v]fps=30,setpts=PTS-STARTPTS,scale=1080:608,setsar=1[c];color=black:s={W}x{H}:r=30[bg];[bg][c]overlay=0:656:shortest=1,format=yuv420p"]
        else:
            sw, sh = round(1080 * L['s'] / 2) * 2, round(1920 * L['s'] / 2) * 2
            if L['fill']:
                fill_mov(s)
                cmd = ['-ss', f"{s['start'] / FPS:.4f}", '-i', SRC['cam'], '-i', f'{OUT}/blurfill_{s["piece"]:02d}.mov', '-filter_complex',
                       f"[0:v]fps=30,setpts=PTS-STARTPTS,lut3d='{LUT}',scale={sw}:{sh}:flags=lanczos,setsar=1[c];color=black:s={W}x{H}:r=30[bg];"
                       f"[bg][1:v]overlay=0:0:shortest=1[bb];[bb][c]overlay={round(L['ox'])}:{round(L['oy'])}:shortest=1,format=yuv420p"]
            else:
                cmd = ['-ss', f"{s['start'] / FPS:.4f}", '-i', SRC['cam'], '-filter_complex',
                       f"[0:v]fps=30,setpts=PTS-STARTPTS,lut3d='{LUT}',scale={sw}:{sh}:flags=lanczos,setsar=1[c];color=black:s={W}x{H}:r=30[bg];"
                       f"[bg][c]overlay={round(L['ox'])}:{round(L['oy'])}:shortest=1,format=yuv420p"]
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', *cmd, '-frames:v', str(n), '-an', '-pix_fmt', 'yuv420p', '-c:v', 'libx264', '-bf', '0', '-crf', '16', '-preset', 'veryfast', out], check=True)
    blk = f'{d}/end.mp4'; parts.append(blk)
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=black:s={W}x{H}:r=30', '-frames:v', str(RJ['total_frames'] - RJ['speech_frames']),
                    '-pix_fmt', 'yuv420p', '-c:v', 'libx264', '-bf', '0', '-crf', '16', '-preset', 'veryfast', blk], check=True)
    open(f'{d}/list.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{d}/list.txt', '-c', 'copy', f'{d}/base.mp4'], check=True)
    ins = ['-i', f'{d}/base.mp4']; fc = []; last = '0:v'
    for k, (m, a, b, fn) in enumerate(RJ['gfx']):
        ins += ['-i', f'{OUT}/{fn}']; fc.append(f'[{k + 1}:v]format=yuva444p,tpad=stop=4:color=0x00000000,setpts=PTS-STARTPTS+{a}/(30*TB)[g{k}];[{last}][g{k}]overlay=eof_action=pass:repeatlast=0[v{k}]'); last = f'v{k}'
    n = len(RJ['gfx']) + 1; ins += ['-i', f'{OUT}/captions.mov', '-i', f'{OUT}/mix.wav', '-i', f'{OUT}/title.mov']
    fc.append(f'[{last}][{n}:v]overlay=eof_action=pass[vc];[{n + 2}:v]format=yuva444p,setpts=PTS-STARTPTS[tt];[vc][tt]overlay=eof_action=pass,format=yuv420p[vout]')
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(fc), '-map', '[vout]', '-map', f'{n + 1}:a',
                    '-frames:v', str(RJ['total_frames']), '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-c:a', 'aac', '-b:a', '256k',
                    '-movflags', '+faststart', f'{OUT}/img0027_rpn_preview.mp4'], check=True)


def probe(p):
    j = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type,sample_rate,channels', '-of', 'json', p],
                                  capture_output=True, text=True).stdout)
    return float(j['format']['duration']), next((s for s in j['streams'] if s['codec_type'] == 'audio'), None)


def fcpxml():
    os.makedirs(G, exist_ok=True); AU = json.load(open(f'{OUT}/audio.json'))
    gfx = [g[3] for g in RJ['gfx']]
    for f in gfx + ['captions.mov', 'title.mov', f'img0027_rpn_preview.mp4']: shutil.copy2(f'{OUT}/{f}', G)
    shutil.copy2(f'{OUT}/{REEL}.srt', f'{G}/img0027_rpn.srt')
    T = lambda f: f'{f}/{FPS}s' if f else '0s'; fr = lambda s: round(s * FPS)
    assets, ids = [], {}

    def asset(key, path, video, name=None, fmt='r3'):
        if key in ids: return ids[key]
        rid = f'r{len(ids) + 4}'; d, a = probe(path); ids[key] = rid
        at = f'id="{rid}" name={q(name or key)} start="0s" duration="{round(d * 48000)}/48000s"'
        if video: at += f' hasVideo="1" format="{fmt}"'
        if a: at += f' hasAudio="1" audioSources="1" audioChannels="{a["channels"]}" audioRate="{a["sample_rate"]}"'
        assets.append(f'    <asset {at}>\n      <media-rep kind="original-media" src={q("file://" + urllib.parse.quote(path))}/>\n    </asset>')
        return rid

    if FCP_LUT: assets.append('    <effect id="r1" name="Custom LUT" uid="FxPlug:14B39AEF-607D-42DF-98DD-DB3DD345E925"/>')
    cam = asset('IMG_0027', SRC['cam'], True, fmt='rcam')   # iPhone portrait: 1920x1080 HEVC stored with a -90 rotation, 120 fps
    segs = segments(); spine = [dict(s, kind='clip', children=[]) for s in segs]
    total = RJ['total_frames']; sp = sum(s['dur'] for s in segs); assert sp == RJ['speech_frames']
    spine.append(dict(kind='gap', offset=sp, start=0, dur=total - sp, children=[]))

    def attach(t, fn):
        for p in spine:
            if p['offset'] <= t < p['offset'] + p['dur'] or p is spine[-1]:
                p['children'].append(fn(p['start'] + (t - p['offset']))); return

    for k, (m, a, b, fn) in enumerate(RJ['gfx']):
        nm = gfx[k][:-4]; rid = asset(f'{REEL} {nm}', f'{G}/{gfx[k]}', True)
        attach(a, lambda l, rid=rid, nm=nm, n=b - a: f'<video ref="{rid}" lane="1" name="{nm}" offset="{T(l)}" start="0s" duration="{T(n)}"/>')
    ti = RJ['title']; tid = asset(f'{REEL} title', f'{G}/title.mov', True, 'Title')
    attach(ti['start'], lambda l, n=ti['frames']: f'<video ref="{tid}" lane="3" name="Title: {ti["text"]}" role="Title" offset="{T(l)}" start="0s" duration="{T(n)}"/>')
    cap = asset(f'{REEL} captions', f'{G}/captions.mov', True)
    for p in spine:
        p['children'].append(f'<video ref="{cap}" lane="2" name="captions" offset="{T(p["start"])}" start="{T(p["offset"])}" duration="{T(p["dur"])}"/>')
    bed = AU['bed']; mus = asset('music', bed['file'], False, os.path.basename(bed['file']).rsplit('.', 1)[0])
    attach(0, lambda l: (f'<asset-clip ref="{mus}" lane="-1" name="music bed" offset="{T(l)}" start="{T(fr(bed["src"]))}" duration="{T(total)}" audioRole="music">'
                         f'<adjust-volume amount="{bed["gain"]}dB"><param name="amount"><fadeIn type="easeIn" duration="{T(2)}"/>'
                         f'<fadeOut type="easeOut" duration="{T(24)}"/></param></adjust-volume></asset-clip>'))
    for s in AU['sfx']:
        rid = asset('sfx ' + os.path.basename(s['file']), s['file'], False, 'sfx ' + s['name'])
        attach(fr(s['start']), lambda l, rid=rid, s=s: f'<asset-clip ref="{rid}" lane="-2" name="sfx {s["name"]}" offset="{T(l)}" start="0s" '
               f'duration="{T(max(2, round(s["len"] * FPS)))}" audioRole="effects"><adjust-volume amount="{s["gain"]}dB"/></asset-clip>')
    for p in spine:
        if p.get('kind') == 'clip' and p['L']['fill']:
            fp = fill_mov(p); shutil.copy2(fp, G); rid = asset(f'blurfill_{p["piece"]:02d}', f'{G}/{os.path.basename(fp)}', True)
            p['children'].insert(0, f'<video ref="{rid}" lane="-3" name="blur fill (open strip)" offset="{T(p["start"])}" start="0s" duration="{T(p["dur"])}"/>')
    clips = []
    for i, p in enumerate(spine):
        inner = ''.join('\n            ' + c for c in p['children'])
        if p['kind'] == 'gap':
            clips.append(f'          <gap name="end card (cheat sheet)" offset="{T(p["offset"])}" start="0s" duration="{T(p["dur"])}">{inner}\n          </gap>'); continue
        L = p['L']; g = AU['source_gain_db'][p['src']]
        if p['src'] == 'pot':
            g = min(g, 10.7)                 # the upload is quiet (-28 LUFS); a full lift to -14 would clip, so cap at its -1.5 dBTP peak (as in the long form)
            clips.append(f'          <asset-clip ref="{pot}" name="Lauren Tan, AIE (credited excerpt)" offset="{T(p["offset"])}" start="{T(p["start"])}" duration="{T(p["dur"])}" '
                         f'tcFormat="NDF" audioRole="dialogue">\n            <adjust-conform type="fit"/>\n            <adjust-volume amount="{g}dB"/>{inner}\n          </asset-clip>')
            continue
        clips.append(f'          <asset-clip ref="{cam}" name="IMG_0027 {i + 1:02d} ({p["run"]})" offset="{T(p["offset"])}" start="{T(p["start"])}" duration="{T(p["dur"])}" '
                     f'tcFormat="NDF" audioRole="dialogue">\n            <adjust-conform type="fit"/>\n            <adjust-transform position="{L["fcp_pos"][0]} {L["fcp_pos"][1]}" scale="{L["fcp_scale"]} {L["fcp_scale"]}"/>'
                     f'\n            <adjust-volume amount="{g}dB"/>{inner}{LUT_TAG}\n          </asset-clip>')
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.14">
  <resources>
    <format id="r2" name="FFVideoFormat1080p30" frameDuration="1/{FPS}s" width="1920" height="1080" colorSpace="1-1-1 (Rec. 709)"/>
    <format id="r3" name="FFVideoFormat1080x1920p30" frameDuration="1/{FPS}s" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>
    <format id="rcam" name="FFVideoFormatRateUndefined" frameDuration="1/120s" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>
{chr(10).join(assets)}
  </resources>
  <library>
    <event name="IMG_0027 RPN (software factories)">
      <project name={q(f"IMG_0027 reel: {TITLES[REEL]} (RPN pixel)")}>
        <sequence format="r3" duration="{T(total)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k">
          <spine>
{chr(10).join(clips)}
          </spine>
        </sequence>
      </project>
    </event>
  </library>
</fcpxml>
'''
    bad = [v for v in re.findall(r' (?:offset|start|duration)="([^"]+)"', xml) if v.endswith('/30s') and (Fr(v.rstrip('s')) * FPS).denominator != 1]
    bad += [v for v in re.findall(r' (?:offset|start)="([^"]+)"', xml) if (Fr(v.rstrip('s')) * FPS).denominator != 1]
    if bad: sys.exit(f'off-grid: {bad[:8]}')
    os.makedirs(f'{R}/fcp', exist_ok=True)
    for o in (f'{R}/fcp/img0027_rpn.fcpxml', f'{G}/img0027_rpn.fcpxml'): open(o, 'w').write(xml)
    json.dump(segs, open(f'{ED}/segments.json', 'w'), indent=1)
    print(REEL, 'fcpxml', total / FPS, 's,', len(spine), 'spine items')


if __name__ == '__main__':
    w = sys.argv[2] if len(sys.argv) > 2 else 'all'
    if w in ('preview', 'all'): preview()
    if w in ('fcpxml', 'all'): fcpxml()
