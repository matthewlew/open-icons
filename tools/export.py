"""Emit the icon set as files: standalone SVGs plus one JSON of inner markup.

The generator keeps a ${u} placeholder wherever a mask or clip id appears, so
that many copies of one icon can sit on the same page without their ids
colliding. A standalone file has no such problem, so there the placeholder
becomes the empty string; the JSON keeps it, because whoever renders from the
JSON is the one putting several on a page."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate as gen20

OUT = sys.argv[1] if len(sys.argv) > 1 else 'icons'
W = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0

d = gen20.build(W)
os.makedirs(os.path.join(OUT, '24'), exist_ok=True)

HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" '
        'viewBox="0 0 24 24" fill="none">')
for name, inner in sorted(d.items()):
    body = inner.replace('${u}', '')
    with open(os.path.join(OUT, '24', name + '.svg'), 'w') as f:
        f.write(HEAD + body + '</svg>\n')

with open(os.path.join(OUT, 'icons.json'), 'w') as f:
    json.dump({'grid': 24, 'stroke': W, 'icons': dict(sorted(d.items()))}, f, indent=1)

with open(os.path.join(OUT, 'names.json'), 'w') as f:
    json.dump(sorted(d), f, indent=1)

print('%d icons -> %s' % (len(d), OUT))
