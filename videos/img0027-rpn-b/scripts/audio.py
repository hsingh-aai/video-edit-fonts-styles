"""IMG_0027 reel audio (software factories ep. 1): voice (each source levelled on its own, then -14 LUFS; the Lauren Tan excerpt only plays where
Harnoor is silent), one bed for the whole series 15 LU under the voice, sparse Ocular SFX (picked by Metadata CSV tag) plus
the match-cut-intro burst SFX (a touchscreen single on each cut, "Be Gentle" peaking on the cut out of the reel).
Reads edit/<reel>/pieces.json + renders/<reel>/runs.json. Writes renders/<reel>/mix.wav + audio.json.
Usage: python3 audio.py <reel>"""
import glob, json, os, re, subprocess, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(f'{HERE}/..')
sys.path.insert(0, HERE)
from cut import SRC
OC = os.path.expanduser('~/Music/Ocular_Sounds'); ES = os.path.expanduser('~/Music/documentary es')
of = lambda name: glob.glob(f'{OC}/**/{name}', recursive=True)[0]
SFX = {  # name: (file, peak target dBFS, max length s). Picked by Ocular CSV tag: tick = "Designed, Gear, Mechanical" (a small gear
         # single when a named thing cuts in: the reel is about a mechanism in the primes), swell = "Powerful, Whoosh, Fast" (section change), burst sounds from the match-cut skill
    'tick': (of('MECHGear_SINGULAR-Small Gears 10_Ocular_Mechanica.wav'), -15, 0.3),
    'swell': (of('DSGNWhsh_WHOOSH-Weight_Ocular_Foundation.wav'), -10, 1.2),
    'gentle': (of('DSGNWhsh_WHOOSH-Be Gentle_Ocular_Foundation.wav'), -12, 1.6),
    'touch1': (of('COMCell_TOUCH SCREEN-Typing On Cell Phone Screen Singles 01_Ocular_Utility.wav'), -22, 0.25),
    'touch9': (of('COMCell_TOUCH SCREEN-Typing On Cell Phone Screen Singles 09_Ocular_Utility.wav'), -22, 0.25),
    'touch2': (of('COMCell_TOUCH SCREEN-Typing On Cell Phone Screen Singles 02_Ocular_Utility.wav'), -22, 0.25),
}
BED = (f'{ES}/ES Problem Solver - Auxjack.mp3', 15, None, None)   # "Problem Solver": an engineering explainer, episode 1 of a series; 15 LU under the voice


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr[-2500:])
    return r


def loud(path, extra=()):
    s = subprocess.run(['ffmpeg', '-nostats', *extra, '-i', path, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    s = s[s.rfind('Summary:'):]; g = lambda k: float(re.search(k + r':\s+(-?[\d.]+|-inf)', s).group(1).replace('-inf', '-99'))
    return {'I': g('I'), 'LRA': g('LRA'), 'TP': g('Peak')}


def mono(path, sr, ss=0.0, t=None):
    tmp = f'{R}/audio/_m_{os.getpid()}.wav'
    sh(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), *(['-t', str(t)] if t else []), '-i', path, '-ac', '1', '-ar', str(sr), tmp])
    w = wave.open(tmp); return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768


def peak_t(path, ln):
    x = mono(path, 48000, 0, ln); n = 480; e = np.sqrt((x[:len(x) // n * n].reshape(-1, n) ** 2).mean(1))
    return float(np.argmax(e) * 0.01), float(20 * np.log10(np.abs(x).max() + 1e-9))


def onsets(path, ss, dur):
    """strong low-end onsets (s from ss): 10 ms energy under ~150 Hz, positive flux peaks"""
    x = mono(path, 4000, ss, dur); k = np.ones(13) / 13; lo = np.convolve(x, k, 'same')
    n = 40; e = np.sqrt((lo[:len(lo) // n * n].reshape(-1, n) ** 2).mean(1)); e = 20 * np.log10(e + 1e-6)
    fl = np.maximum(np.diff(e, prepend=e[0]), 0); th = np.percentile(fl, 99)
    return [i * 0.01 for i in range(2, len(fl) - 2) if fl[i] >= th and fl[i] == fl[i - 2:i + 3].max()]


def run(name):
    out = f'{R}/renders/{name}'; os.makedirs(f'{R}/audio', exist_ok=True)
    pieces = json.load(open(f"{R}/edit/{name}/pieces.json")); rj = json.load(open(f'{out}/runs.json'))
    bu = rj['burst']; cuts = [(bu['b0'] + k * bu['fpi']) / 30 for k in range(1, len(bu['items']) + 1)]
    rj['sfx'] = [s for s in rj['sfx'] if s[0] != 'swell' or abs(s[1] - bu['b0'] / 30) > 0.05] + [('gentle', bu['b0'] / 30)] + [(['touch1', 'touch9', 'touch2'][k % 3], t) for k, t in enumerate(cuts)]
    END = rj['total_frames'] / 30
    # 1. voice: each source measured alone and matched, 8 ms fades at joins
    gains = {}
    for src in {p['src'] for p in pieces}:
        ins, fc = [], []
        ps = [p for p in pieces if p['src'] == src]
        for i, p in enumerate(ps):
            ins += ['-ss', f"{p['in']:.4f}", '-t', f"{p['out'] - p['in']:.4f}", '-i', SRC[src]]; fc.append(f'[{i}:a:0]aformat=sample_rates=48000:channel_layouts=stereo[a{i}]')
        fc.append(''.join(f'[a{i}]' for i in range(len(ps))) + f'concat=n={len(ps)}:v=0:a=1[v]')
        sh(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(fc), '-map', '[v]', f'{R}/audio/_src_{name}_{src}.wav'])
        gains[src] = loud(f'{R}/audio/_src_{name}_{src}.wav')
    ins, fc = [], []
    for i, p in enumerate(pieces):
        d = p['out'] - p['in']; g = -19.4 - gains[p['src']]['I']
        ins += ['-ss', f"{p['in']:.4f}", '-t', f'{d:.4f}', '-i', SRC[p['src']]]
        fc.append(f'[{i}:a:0]aformat=sample_rates=48000:channel_layouts=stereo,volume={g:.2f}dB,afade=t=in:d=0.008,afade=t=out:st={d - 0.008:.4f}:d=0.008[a{i}]')
    hold = END - sum(p['out'] - p['in'] for p in pieces)
    fc.append(''.join(f'[a{i}]' for i in range(len(pieces))) + f'concat=n={len(pieces)}:v=0:a=1,apad=pad_dur={hold + 0.1:.3f}[v]')
    sh(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(fc), '-map', '[v]', '-t', f'{END:.3f}', f'{R}/audio/{name}_voice_raw.wav'])
    COMP = 'highpass=f=85,acompressor=threshold=-30dB:ratio=3.5:attack=10:release=200:makeup=1'
    sh(['ffmpeg', '-v', 'error', '-y', '-i', f'{R}/audio/{name}_voice_raw.wav', '-af', COMP, f'{R}/audio/_vc_{name}.wav'])
    cg = round(-14.0 - loud(f'{R}/audio/_vc_{name}.wav')['I'], 2)
    sh(['ffmpeg', '-v', 'error', '-y', '-i', f'{R}/audio/_vc_{name}.wav', '-af', f'volume={cg}dB,alimiter=limit=0.84:level=false', f'{R}/audio/{name}_voice.wav'])
    vo = loud(f'{R}/audio/{name}_voice.wav', ['-t', f'{END - hold:.2f}'])
    # 2. bed: one level, in on its start frame, out over 1.5 s at the end; slide so a strong low-end onset lands on the cue
    file, under, start_mode, cue_mode = BED
    runs = rj['runs']; first = lambda m: next(a for mm, a, b in runs if mm == m) / 30
    tl = 0.0 if start_mode is None else first(start_mode)
    cue = tl
    ons = onsets(file, 0, 60)
    cand = [o for o in ons if o >= 0.3]
    src0 = round(min(cand, key=lambda o: o) - (cue - tl), 3) if cand else 0.0
    dur = END - tl
    ml = loud(file, ['-ss', str(src0), '-t', f'{dur:.2f}'])
    bed = {'file': file, 'tl': round(tl, 4), 'src': src0, 'dur': round(dur, 4), 'cue': round(cue, 3), 'gain': round(vo['I'] - under - ml['I'], 1), 'measured': ml}
    # 3. SFX: peak on the cue frame, gain to the target peak, cap per minute
    sfx = []
    for nm, t in rj['sfx']:
        f, tgt, ln = SFX[nm]; pt, pk = peak_t(f, ln)
        if nm in ('whoosh', 'swell', 'gentle'): pt = min(pt, 0.9)
        if nm == 'keys': pt = 0.0
        sfx.append({'name': nm, 'file': f, 'at': round(t, 4), 'len': ln, 'peak_t': pt, 'gain': round(tgt - pk, 1), 'start': round(max(0, t - pt), 4)})
    ins = ['-i', f'{R}/audio/{name}_voice.wav', '-ss', str(bed['src']), '-t', f'{dur:.3f}', '-i', file]
    fc = [f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={bed['gain']}dB,afade=t=in:d={0.05 if tl == 0 else 0.4},"
          f"afade=t=out:st={dur - 0.8:.3f}:d=0.8,adelay={int(tl * 1000)}:all=1[b]"]; tags = ['[0:a]', '[b]']
    for j, s in enumerate(sfx):
        k = j + 2; ins += ['-t', str(s['len']), '-i', s['file']]
        fo = max(s['len'] * 0.6, min(s['len'], s['peak_t'] + 0.12))
        fc.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={s['gain']}dB,afade=t=out:st={fo:.3f}:d={max(0.02, s['len'] - fo):.3f},adelay={int(s['start'] * 1000)}:all=1[s{k}]")
        tags.append(f'[s{k}]')
    fc.append(''.join(tags) + f'amix=inputs={len(tags)}:normalize=0:duration=first,alimiter=limit=0.83:level=false[mix]')
    sh(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(fc), '-map', '[mix]', '-t', f'{END:.3f}', '-ar', '48000', f'{out}/mix.wav'])
    mx = loud(f'{out}/mix.wav')
    json.dump({'source_loudness': gains, 'source_gain_db': {s: round(-14.0 - g['I'], 1) for s, g in gains.items()}, 'voice': vo,
               'bed': bed, 'sfx': sfx, 'mix': mx}, open(f'{out}/audio.json', 'w'), indent=1)
    print(name, 'voice', vo, 'bed', os.path.basename(file), bed['gain'], 'src', bed['src'], '| sfx', len(sfx), f'({len(sfx) / END * 60:.1f}/min)', '| mix', mx)


if __name__ == '__main__':
    run(sys.argv[1])
