"""Ray-cast local thickness + local gap measurement for flattened icon outlines."""
import sys, os, re, math, glob, json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from svgparse import parse_path, seg_points

PATH_RE = re.compile(r'<path\b([^>]*)>')

def flatten(sp, tol=0.06):
    """Adaptive-ish flatten: fixed subdivision scaled by segment size."""
    pts = []
    for s in sp:
        if s[0] == 'L':
            n = 1
        else:
            # chord length heuristic
            L = math.hypot(s[-1][0]-s[1][0], s[-1][1]-s[1][1])
            n = max(4, min(48, int(L*12)+4))
        p = seg_points(s, n)
        if pts and math.hypot(p[0][0]-pts[-1][0], p[0][1]-pts[-1][1]) < 1e-9:
            pts += p[1:]
        else:
            pts += p
    return pts

def load_shape(fname):
    """Return (polys, groups) where groups=[(fillrule, [poly_idx,...]), ...]"""
    src = open(fname, encoding='utf-8').read()
    polys = []
    groups = []
    for m in PATH_RE.finditer(src):
        attrs = m.group(1)
        dm = re.search(r'\sd="([^"]+)"', attrs)
        if not dm: continue
        rule = 'evenodd' if 'evenodd' in attrs else 'nonzero'
        idxs = []
        for sp in parse_path(dm.group(1)):
            pts = flatten(sp)
            if len(pts) < 3: continue
            idxs.append(len(polys))
            polys.append(np.array(pts, dtype=float))
        if idxs: groups.append((rule, idxs))
    # <circle> elements
    for m in re.finditer(r'<circle[^>]*>', src):
        tag = m.group(0)
        def g(a, d=0.0):
            mm = re.search(a + r'="([-\d.]+)"', tag)
            return float(mm.group(1)) if mm else d
        cx, cy, r = g('cx'), g('cy'), g('r')
        if r <= 0: continue
        th = np.linspace(0, 2*math.pi, 64)
        polys.append(np.stack([cx+r*np.cos(th), cy+r*np.sin(th)], 1))
        groups.append(('nonzero', [len(polys)-1]))
    return polys, groups

def edges_of(polys, idxs):
    A, B = [], []
    for i in idxs:
        p = polys[i]
        A.append(p); B.append(np.roll(p, -1, axis=0))
    return np.concatenate(A), np.concatenate(B)

class Shape:
    def __init__(self, fname):
        self.polys, self.groups = load_shape(fname)
        self.gedges = [(rule,) + edges_of(self.polys, idxs) for rule, idxs in self.groups]
        if self.polys:
            allp = np.concatenate(self.polys)
            self.bbox = (allp[:,0].min(), allp[:,1].min(), allp[:,0].max(), allp[:,1].max())
        else:
            self.bbox = None
        A, B = ([], [])
        for _, a, b in self.gedges:
            A.append(a); B.append(b)
        self.EA = np.concatenate(A) if A else np.zeros((0,2))
        self.EB = np.concatenate(B) if B else np.zeros((0,2))

    def inside(self, Q):
        """Q: (N,2) -> bool (N,). Union over path groups."""
        res = np.zeros(len(Q), dtype=bool)
        for rule, A, B in self.gedges:
            ax, ay = A[:,0][None,:], A[:,1][None,:]
            bx, by = B[:,0][None,:], B[:,1][None,:]
            qx, qy = Q[:,0][:,None], Q[:,1][:,None]
            cond = (ay > qy) != (by > qy)
            with np.errstate(divide='ignore', invalid='ignore'):
                t = (qy - ay) / (by - ay)
                xint = ax + t*(bx - ax)
            crosses = cond & (qx < xint)
            if rule == 'evenodd':
                r = (crosses.sum(1) % 2) == 1
            else:
                sign = np.where(by > ay, 1, -1)
                r = (crosses*sign).sum(1) != 0
            res |= r
        return res

    def ray_hits(self, P, D, maxt=40.0):
        """First intersection distance along ray P+tD (t>eps) with any edge. (N,)"""
        ax, ay = self.EA[:,0][None,:], self.EA[:,1][None,:]
        ex = (self.EB[:,0]-self.EA[:,0])[None,:]
        ey = (self.EB[:,1]-self.EA[:,1])[None,:]
        px, py = P[:,0][:,None], P[:,1][:,None]
        dx, dy = D[:,0][:,None], D[:,1][:,None]
        den = dx*ey - dy*ex
        with np.errstate(divide='ignore', invalid='ignore'):
            rx, ry = ax-px, ay-py
            t = (rx*ey - ry*ex) / den      # along ray
            u = (rx*dy - ry*dx) / den      # along edge
        ok = np.isfinite(t) & (t > 1e-3) & (u >= -1e-9) & (u <= 1+1e-9)
        t = np.where(ok, t, np.inf)
        return t.min(1)

    def samples(self, spacing=0.12):
        """Contour sample points + unit normals."""
        P, N = [], []
        for p in self.polys:
            d = np.roll(p, -1, axis=0) - p
            L = np.hypot(d[:,0], d[:,1])
            keep = L > 1e-9
            mid = p + d*0.5
            nrm = np.stack([-d[:,1], d[:,0]], 1)
            nl = np.hypot(nrm[:,0], nrm[:,1])
            nrm = nrm / np.where(nl == 0, 1, nl)[:,None]
            P.append(mid[keep]); N.append(nrm[keep])
        if not P: return np.zeros((0,2)), np.zeros((0,2))
        return np.concatenate(P), np.concatenate(N)

def measure(fname, eps=0.012):
    sh = Shape(fname)
    P, N = sh.samples()
    if len(P) == 0: return None
    # subsample for speed
    if len(P) > 900:
        idx = np.linspace(0, len(P)-1, 900).astype(int)
        P, N = P[idx], N[idx]
    inN = sh.inside(P + N*eps)
    D_in = np.where(inN[:,None], N, -N)
    D_out = -D_in
    th = sh.ray_hits(P + D_in*eps, D_in) + eps
    gp = sh.ray_hits(P + D_out*eps, D_out) + eps
    th = th[np.isfinite(th)]
    gp = gp[np.isfinite(gp)]
    return dict(thickness=th, gap=gp, bbox=sh.bbox)

def mode_of(vals, binw=0.05, lo=0.0, hi=12.0):
    v = vals[(vals > lo) & (vals < hi)]
    if len(v) == 0: return None, 0
    bins = np.floor(v/binw).astype(int)
    u, c = np.unique(bins, return_counts=True)
    i = c.argmax()
    return round((u[i]+0.5)*binw, 3), int(c[i])
