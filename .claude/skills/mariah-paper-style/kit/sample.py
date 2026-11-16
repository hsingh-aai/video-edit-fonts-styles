"""Mariah Paper sample stills (styles/samples/mariah-paper/) and the gallery screenshot.
Usage: ~/Developer/video-use/.venv/bin/python sample.py <repo> <frames_dir> <out_dir>
frames_dir holds stills from Harnoor's own img1092 build (videos/img1092-reel, not committed):
cam_2/12/30.jpg from edit/base.mp4 (ffmpeg -ss 2 etc.).
Every post, table, tile and agent card here is drawn placeholder art with made-up words and
numbers ("sample"). In a real build each one is the real screenshot."""
import sys; sys.path.insert(0, sys.argv[1] + '/.claude/skills/mariah-paper-style/kit')
import mariahpaper as mp
from PIL import Image
D, OUT = sys.argv[2], sys.argv[3]
cam, cam2, cam3 = (Image.open(f'{D}/cam_{t}.jpg') for t in (2, 12, 30))
FACE = (0.5, 0.38)
POST = ['Every time a new model ships, I run', 'the same simple prompt on my projects:', '',
        '"Read this entire project and find', 'everything that\'s broken or unused."', '', 'sample post']


def save(im, name):
    im.save(f'{OUT}/{name}.jpg', quality=90)
    return im


# 1. hook: two-line title with the red spark, a launch card over the chest, caption under it
a = mp.face(cam, FACE)
mp.hook(a, 'The 1st thing to do with', 'a new AI model')
mp.card(a, mp.art((900, 520), 'New model', (16, 14, 20), (70, 40, 110)), (120, 900, 960, 1370))
save(mp.caption(a, 'and here'), '1_hook')

# 2. a post takes the top of the frame, the face stays below, serif + red accent beat
b = mp.face(cam2, (0.5, 0.2))
mp.top_split(b, mp.crumpled().crop((0, 0, 1080, 760)), h=760)
mp.card(b, mp.post((980, 520), 'Sample Researcher', '@sample', POST), (50, 170, 1030, 690), r=30)
save(mp.accent(b, 'he runs the', 'same prompt', cy=1400), '2_top_post')

# 3. the same post on the crumpled cream board, red marker bar on the phrase being read
c = mp.crumpled()
mp.card(c, mp.post((980, 520), 'Sample Researcher', '@sample', POST, mark=(3, 0, 25)), (50, 700, 1030, 1220), r=30)
save(mp.caption(c, 'entire project', on='paper', cy=1300), '3_paper_post')

# 4. plain face beat on the tight framing, caption only
d = mp.face(cam3, FACE, tight=True)
save(mp.caption(d, 'now which'), '4_face')

# 5. red board with a white table card
e = mp.red_board()
rows = [(n, [f'{v - 3 * i}%' for i in range(4)]) for n, v in
        (('Coding', 88), ('Research', 81), ('Design', 79), ('Search', 84), ('Vision', 73), ('Reasoning', 77), ('Tools', 69))]
mp.card(e, mp.table((860, 1040), 'Model A vs the rest', ['Model A', 'Model B', 'Model C', 'Model D'], rows, lit=0),
        (110, 360, 970, 1400), r=40)
save(mp.caption(e, 'sample data', on='red', cy=1500), '5_red_table')

# 6. cream board diagram: one lead card, a dotted bracket, four sub cards
f = mp.crumpled(seed=9)
mp.agent_card(f, (270, 200, 810, 780), 'Lead model', 'Orchestrator', 'Plans, delegates, checks', tag='LEAD')
mp.dotted(f, [(270, 860), (90, 880), (70, 1560)]); mp.dotted(f, [(810, 860), (990, 880), (1010, 1560)])
for i, job in enumerate(['Research', 'Write code', 'Run tests', 'Draft report']):
    x, y = 110 + (i % 2) * 440, 960 + (i // 2) * 330
    mp.agent_card(f, (x, y, x + 420, y + 290), 'Worker model', f'Subagent {i + 1}', job,
                  top=(40, 44, 70), bottom=(200, 110, 50), progress=(.5, .7, .4, .6)[i])
save(mp.caption(f, 'orchestrator', on='paper', cy=880), '6_paper_tree')

# 7. red board stack: one tile per named thing
g = mp.red_board()
mp.stack(g, [mp.art((580, 440), 'Release 3', (230, 222, 170), (190, 60, 40)),
             mp.art((580, 440), 'Release 2', (120, 170, 220), (230, 225, 205)),
             mp.art((580, 440), 'Release 1', (240, 228, 200), (120, 140, 90))], y1=1660)
save(mp.caption(g, 'this year', on='red', cy=1760), '7_red_stack')

# 8. close: the comment call over the head
h = mp.face(cam, FACE)
mp.cta(h, 'comment', 'recheck')
save(mp.caption(h, 'down below'), '8_cta')

b.resize((540, 960), Image.LANCZOS).save(OUT + '/mariah-paper.jpg', quality=88)   # move to styles/screenshots/
