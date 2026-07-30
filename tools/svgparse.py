"""Minimal SVG path parser + geometry feature extractor for Open Icons analysis."""
import re, math, os, json, glob
from collections import defaultdict

NUM = re.compile(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?')
CMD = re.compile(r'([MmLlHhVvCcSsQqTtAaZz])')

def parse_path(d):
    """Return list of subpaths; each subpath = list of segments.
    Segment = ('L', p0, p1) or ('C', p0, c1, c2, p1)."""
    tokens = CMD.split(d)
    subpaths = []
    cur = []
    pos = (0.0, 0.0)
    start = (0.0, 0.0)
    prev_c2 = None
    i = 1
    last_cmd = None
    while i < len(tokens):
        cmd = tokens[i]
        args = [float(x) for x in NUM.findall(tokens[i+1])] if i+1 < len(tokens) else []
        i += 2
        rel = cmd.islower()
        c = cmd.upper()
        k = 0
        first = True
        while True:
            if c == 'M':
                if k+2 > len(args): break
                p = (args[k], args[k+1])
                if rel: p = (pos[0]+p[0], pos[1]+p[1])
                k += 2
                if first:
                    if cur: subpaths.append(cur)
                    cur = []
                    start = p
                    pos = p
                    first = False
                    c = 'L'  # subsequent pairs are implicit lineto
                    continue
            elif c == 'L':
                if k+2 > len(args): break
                p = (args[k], args[k+1])
                if rel: p = (pos[0]+p[0], pos[1]+p[1])
                k += 2
                cur.append(('L', pos, p)); pos = p
            elif c == 'H':
                if k+1 > len(args): break
                x = args[k]; k += 1
                p = (pos[0]+x if rel else x, pos[1])
                cur.append(('L', pos, p)); pos = p
            elif c == 'V':
                if k+1 > len(args): break
                y = args[k]; k += 1
                p = (pos[0], pos[1]+y if rel else y)
                cur.append(('L', pos, p)); pos = p
            elif c == 'C':
                if k+6 > len(args): break
                a = args[k:k+6]; k += 6
                if rel:
                    c1 = (pos[0]+a[0], pos[1]+a[1]); c2 = (pos[0]+a[2], pos[1]+a[3]); p = (pos[0]+a[4], pos[1]+a[5])
                else:
                    c1 = (a[0], a[1]); c2 = (a[2], a[3]); p = (a[4], a[5])
                cur.append(('C', pos, c1, c2, p)); prev_c2 = c2; pos = p
            elif c == 'S':
                if k+4 > len(args): break
                a = args[k:k+4]; k += 4
                if rel:
                    c2 = (pos[0]+a[0], pos[1]+a[1]); p = (pos[0]+a[2], pos[1]+a[3])
                else:
                    c2 = (a[0], a[1]); p = (a[2], a[3])
                c1 = (2*pos[0]-prev_c2[0], 2*pos[1]-prev_c2[1]) if prev_c2 else pos
                cur.append(('C', pos, c1, c2, p)); prev_c2 = c2; pos = p
            elif c == 'Z':
                if pos != start:
                    cur.append(('L', pos, start))
                pos = start
                if cur: subpaths.append(cur); cur = []
                break
            else:
                break
            first = False
            if k >= len(args): break
    if cur: subpaths.append(cur)
    return subpaths

def seg_points(seg, n=16):
    if seg[0] == 'L':
        p0, p1 = seg[1], seg[2]
        return [(p0[0]+(p1[0]-p0[0])*t/n, p0[1]+(p1[1]-p0[1])*t/n) for t in range(n+1)]
    _, p0, c1, c2, p1 = seg
    out = []
    for t in range(n+1):
        t = t/n
        mt = 1-t
        x = mt**3*p0[0] + 3*mt*mt*t*c1[0] + 3*mt*t*t*c2[0] + t**3*p1[0]
        y = mt**3*p0[1] + 3*mt*mt*t*c1[1] + 3*mt*t*t*c2[1] + t**3*p1[1]
        out.append((x, y))
    return out

KAPPA = 4*(math.sqrt(2)-1)  # 0.5522847

def arc_circle(seg, tol=0.02):
    """If cubic seg is a circular-arc approximation, return (cx, cy, r). Else None."""
    if seg[0] != 'C': return None
    _, p0, c1, c2, p1 = seg
    # tangent at p0 is p0->c1, at p1 is c2->p1. Normals intersect at center.
    t0 = (c1[0]-p0[0], c1[1]-p0[1])
    t1 = (p1[0]-c2[0], p1[1]-c2[1])
    if abs(t0[0])+abs(t0[1]) < 1e-9 or abs(t1[0])+abs(t1[1]) < 1e-9: return None
    n0 = (-t0[1], t0[0]); n1 = (-t1[1], t1[0])
    den = n0[0]*(-n1[1]) - n0[1]*(-n1[0])
    if abs(den) < 1e-9: return None
    dx = p1[0]-p0[0]; dy = p1[1]-p0[1]
    s = (dx*(-n1[1]) - dy*(-n1[0])) / den
    cx = p0[0] + s*n0[0]; cy = p0[1] + s*n0[1]
    r = math.hypot(p0[0]-cx, p0[1]-cy)
    if r < 0.05 or r > 200: return None
    for pt in seg_points(seg, 8):
        if abs(math.hypot(pt[0]-cx, pt[1]-cy) - r) > max(tol, r*tol): return None
    return (cx, cy, r)

def subpath_circle(sp, tol=0.02):
    """If the whole subpath is one circle, return (cx,cy,r)."""
    arcs = [arc_circle(s, tol) for s in sp]
    if not arcs or any(a is None for a in arcs): return None
    cx = sum(a[0] for a in arcs)/len(arcs); cy = sum(a[1] for a in arcs)/len(arcs)
    r = sum(a[2] for a in arcs)/len(arcs)
    if any(abs(a[0]-cx) > 0.05 or abs(a[1]-cy) > 0.05 or abs(a[2]-r) > 0.05 for a in arcs): return None
    # must be closed & span full turn: check total angle
    pts = []
    for s in sp: pts += seg_points(s, 8)
    if math.hypot(pts[0][0]-pts[-1][0], pts[0][1]-pts[-1][1]) > 0.05: return None
    total = 0.0
    for i in range(1, len(pts)):
        a0 = math.atan2(pts[i-1][1]-cy, pts[i-1][0]-cx)
        a1 = math.atan2(pts[i][1]-cy, pts[i][0]-cx)
        d = a1-a0
        while d > math.pi: d -= 2*math.pi
        while d < -math.pi: d += 2*math.pi
        total += d
    if abs(abs(total) - 2*math.pi) > 0.15: return None
    return (cx, cy, r)

def bbox(subpaths):
    xs, ys = [], []
    for sp in subpaths:
        for s in sp:
            for p in seg_points(s, 12):
                xs.append(p[0]); ys.append(p[1])
    if not xs: return None
    return (min(xs), min(ys), max(xs), max(ys))

def area(sp):
    pts = []
    for s in sp: pts += seg_points(s, 24)
    a = 0.0
    for i in range(len(pts)):
        x0, y0 = pts[i]; x1, y1 = pts[(i+1) % len(pts)]
        a += x0*y1 - x1*y0
    return a/2

def load_svg(path):
    src = open(path, encoding='utf-8').read()
    ds = re.findall(r'\sd="([^"]+)"', src)
    circles = []
    for m in re.finditer(r'<circle[^>]*>', src):
        tag = m.group(0)
        def g(a):
            mm = re.search(a + r'="([-\d.]+)"', tag)
            return float(mm.group(1)) if mm else 0.0
        circles.append((g('cx'), g('cy'), g('r')))
    rects = re.findall(r'<rect[^>]*>', src)
    vb = re.search(r'viewBox="([^"]+)"', src)
    return dict(src=src, ds=ds, circles=circles, rects=rects,
                viewBox=vb.group(1) if vb else None,
                evenodd=('evenodd' in src))

def all_subpaths(svg):
    out = []
    for d in svg['ds']:
        out += parse_path(d)
    return out
