"""Spec conformance linter: scores every icon against docs/icon-construction-spec.md."""
import sys, os, glob, math, json, re
import numpy as np
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from svgparse import parse_path, load_svg, all_subpaths, area
from thickness import Shape, measure, mode_of

ROOT = os.environ.get("ICON_ROOT", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icons-inspiration"))
KEY24 = [(20,20),(18,18),(16,20),(20,16),(14,20),(20,14),(24,24),(22,22)]
KEY16 = [(16,16),(14,14),(12,16),(16,12),(10,16),(16,10),(13,13)]

def node_count(f):
    svg = load_svg(f); n = 0
    for d in svg['ds']:
        n += len(re.findall(r'[MmLlHhVvCcSsQqTtAa]', d))
    return n

def lint(f, size):
    name = os.path.basename(f)[:-4]
    sh = Shape(f)
    m = measure(f)
    out = dict(name=name, size=size, flags=[], score=0)
    if not m or not sh.bbox:
        out['flags'].append(('unmeasurable','error')); out['score']=100; return out
    th, gp = m['thickness'], m['gap']

    # --- 1. stroke consistency ---
    at2 = float(((th > 1.94) & (th < 2.06)).mean()) if len(th) else 0.0
    out['strokeAt2'] = round(at2, 3)
    mode_th, _ = mode_of(th, 0.05, 0.05, 10)
    out['modeTh'] = mode_th
    is_solid = at2 < 0.12 and (mode_th or 0) > 3.5   # a solid mass, no stroke to judge
    out["solid"] = bool(is_solid)
    if not is_solid:
        if mode_th is None or abs(mode_th - 2.0) > 0.08:
            out['flags'].append((f'stroke mode {mode_th} != 2.0','error')); out['score'] += 30
        if at2 < 0.45:
            out['flags'].append((f'only {at2:.0%} of contour at 2.0','warn')); out['score'] += int((0.45-at2)*60)

    # --- 2. minimum feature / clearance ---
    thin = float((th < 0.9).mean()) if len(th) else 0
    tight = float((gp[np.isfinite(gp)] < 0.9).mean()) if len(gp) else 0
    out['thinShare'] = round(thin,3); out['tightShare'] = round(tight,3)
    if thin > 0.04:
        out['flags'].append((f'{thin:.0%} of form thinner than 0.9','error')); out['score'] += int(thin*180)
    if tight > 0.06:
        out['flags'].append((f'{tight:.0%} of gaps below 0.9','warn')); out['score'] += int(tight*90)

    # --- 3. keyline ---
    x0,y0,x1,y1 = sh.bbox
    w,h = x1-x0, y1-y0
    keys = KEY24 if size==24 else KEY16
    ok = any(abs(w-a)<0.26 and abs(h-b)<0.26 for a,b in keys)
    axis = any(abs(w-a)<0.26 or abs(h-b)<0.26 for a,b in keys)
    out['bbox'] = [round(v,2) for v in (w,h)]
    if not ok:
        if axis: out['flags'].append(('keyline on one axis only','info'))
        else: out['flags'].append((f'bbox {w:.2f}x{h:.2f} off-keyline','warn')); out['score'] += 8

    # --- 4. grid discipline (on-path anchors) ---
    frac = []
    for sp in all_subpaths(load_svg(f)):
        for s in sp:
            for p in (s[1], s[-1]):
                for v in p: frac.append(round(v % 1, 4))
    if frac:
        onq = sum(1 for v in frac if min(abs(v-t) for t in (0,0.25,0.5,0.75,1)) < 0.002)/len(frac)
        out['onGrid'] = round(onq,3)
        if onq < 0.30:
            out['flags'].append((f'only {onq:.0%} of anchors on the 0.25 grid','warn')); out['score'] += int((0.30-onq)*45)

    # --- 5. complexity ---
    nc = node_count(f); out['nodes'] = nc
    budget = 60 if size==24 else 55
    if nc > budget:
        out['flags'].append((f'{nc} path commands (budget {budget})','warn')); out['score'] += min(25,(nc-budget)//4)
    return out

results = {}
for size in (16,24):
    rows = []
    for f in sorted(glob.glob(f"{ROOT}/{size}/*.svg")):
        if 'color' in os.path.basename(f): continue
        try: rows.append(lint(f, size))
        except Exception as e: print("ERR", f, e)
    results[size] = rows
    clean = [r for r in rows if r['score']==0]
    minor = [r for r in rows if 0 < r['score'] <= 15]
    rework= [r for r in rows if r['score'] > 15]
    print(f"\n{'='*70}\nSIZE {size} — {len(rows)} icons linted\n{'='*70}")
    print(f"  CLEAN  (score 0)      {len(clean):>4}   {100*len(clean)/len(rows):5.1f}%   <- baseline-ready")
    print(f"  MINOR  (1-15)         {len(minor):>4}   {100*len(minor)/len(rows):5.1f}%   <- accept w/ note")
    print(f"  REWORK (>15)          {len(rework):>4}   {100*len(rework)/len(rows):5.1f}%   <- redraw queue")
    rework.sort(key=lambda r:-r['score'])
    print(f"\n  worst 22 at {size}px:")
    for r in rework[:22]:
        fl = '; '.join(f[0] for f in r['flags'][:3])
        print(f"    {r['score']:>4}  {r['name']:<30} {fl}")

json.dump(results, open(os.path.dirname(__file__)+"/lint.json","w"), indent=1)

# focused report on the photo family
print(f"\n{'='*70}\nPHOTO / IMAGE FAMILY — detail\n{'='*70}")
for size in (24,16):
    for r in results[size]:
        if re.match(r'^(photo|photos|camera|image)', r['name']):
            print(f"  [{size}] {r['name']:<24} score={r['score']:<4} at2={r.get('strokeAt2')} "
                  f"thin={r.get('thinShare')} nodes={r.get('nodes')} bbox={r.get('bbox')}")
            for fl,sev in r['flags']: print(f"           {sev:<6} {fl}")
