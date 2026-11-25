"""Word-level transcript of the source via AssemblyAI (key from ~/.config/assemblyai/config.json).
Usage: python3 transcribe.py AUDIO OUT_JSON"""
import json, os, sys, time, urllib.request

KEY = json.load(open(os.path.expanduser('~/.config/assemblyai/config.json')))['api_key']
BASE = 'https://api.assemblyai.com/v2'


def req(path, data=None, ctype='application/json'):
    r = urllib.request.Request(BASE + path, data=data, headers={'authorization': KEY, 'content-type': ctype})
    return json.load(urllib.request.urlopen(r))


audio, out = sys.argv[1], sys.argv[2]
up = req('/upload', open(audio, 'rb').read(), 'application/octet-stream')['upload_url']
tid = req('/transcript', json.dumps({'audio_url': up, 'speech_models': os.environ.get('AAI_MODELS', 'universal-3-6-pro-preview,universal-2').split(','),
                                     }).encode())['id']
while True:
    t = req('/transcript/' + tid)
    if t['status'] in ('completed', 'error'):
        break
    time.sleep(3)
if t['status'] == 'error':
    sys.exit(t['error'])
json.dump({'model': t.get('speech_model_used') or t.get('speech_model'), 'text': t['text'], 'words': [{'w': w['text'], 's': w['start'] / 1000, 'e': w['end'] / 1000} for w in t['words']]},
          open(out, 'w'), indent=1)
print(t['text'])
