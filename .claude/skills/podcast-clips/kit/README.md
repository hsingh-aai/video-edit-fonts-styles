# podcast-clips kit

These are reference scripts copied from the Union Square podcast build (Nov 14, 2026). They show the method, but they aren't a drop-in library: adjust `ROOT`, the `spec.REELS` import (word ranges per reel) and the speaker sides for each new podcast.

| File | What it does |
| --- | --- |
| `pieces.py` | Turns word ranges into frame-exact pieces that never clip a word: ends ≥120 ms after the word and runs on to a 100 ms quiet point; starts at the last quiet point before the onset. Its `check()` reports each cut's envelope against the noise floor. |
| `cutsheet.py` | Draws a waveform sheet of every risky end cut (t/s/d/k/ch, numbers, "percent", anything not at the floor). Needs PIL from a venv, since system python has none. |
| `faces_all.swift` | Runs Apple Vision face rectangles on 1 fps stills. Usage: `swift faces_all.swift frames/*.jpg > faces_1fps.txt`. |
| `framing.py` | Builds one static 9:16 crop per speaker run from the median face, with a punch-in option and a stacked two-shot. |
