#!/usr/bin/env python3
# gen20.py — the weight-aware core. Geometry only, no HTML.
#
# Everything studies 15-19 measured is here re-expressed as a function of the
# stroke W. The point of the exercise: the reference set's clearances are not
# round numbers that happen to work, they are the floor `gap >= 1 x stroke`
# solved EXACTLY at stroke 2. Which means a weight axis is a geometry axis.
# Change stroke-width alone and the clearances collapse; every one of them.
#
# build(W) -> {name: svg-inner-string}, with ${u} left in place of unique ids.

import math

C = 12.0
W = 2.0                      # the axis

# ---- the constants, as functions of W --------------------------------------
def e_tip():  return 0.1875 * W          # arrow-tip corner extent   (0.75 @ 2)
def e_out():  return 5.14                # container corner, OUTER — a constant
def e_cl():   return 5.14 - 0.645 * W    # ... and on the centreline (3.85 @ 2)
                                         # linear fit to the solved value; it is
                                         # NOT e_out - W/2, see study 17
def gap():    return 1.00 * W            # stroke <-> stroke floor      (2.0 @ 2)
def gapm():   return 0.75 * W            # stroke <-> mark floor        (1.5 @ 2)
def moat():   return 0.75 * W            # crossing moat               (1.5 @ 2)
def badge():  return 0.875 * W           # badge moat                  (1.75 @ 2)
def gapi():   return 0.40 * W            # INTRA-glyph: the two pieces of one
                                         # mark (bang, i-dot, ?-dot). Measured off
                                         # warning-circle-line, which runs 0.35 W.
def gaps():   return 0.50 * W            # silhouette gap: two large masses, not
                                         # two strokes. person head <-> shoulders
                                         # measures exactly 1.0 at W = 2.
def crease(): return W                   # a negative LINE inside a solid is the
                                         # same width as the stroke it replaces.
                                         # Not a moat — a moat is for a mark that
                                         # CROSSES a wall.

# Head arm runs. `run` is the AXIAL setback of the arm ends, so an arm at 45 has
# length run*sqrt(2) and its end sits `run` off the axis. The notch between the
# arm and the shaft is then run - W/sqrt2 - W/2 = run - 1.207 W, and the two runs
# the reference actually uses are exactly 3W and 2W:
#     run = 3W  ->  notch 1.79 W   (a solo arrow: all the air it wants)
#     run = 2W  ->  notch 0.79 W   (paired heads: the intra-glyph floor, 0.75 W)
# Below 2W the notch closes, which is why arrow-all at run 2.5 was already solid
# at W = 2 and why every head clogged on the way up.
def run1(): return 3.00 * W              # solo               (6.0 @ 2)
def run2(): return 2.00 * W              # paired/constrained (4.0 @ 2)

SHIFT = 0.5                  # optical shift toward the point, tailless marks
REACH = 7.0
DIAG  = 5.0 * math.sqrt(2)

# Enclosed-mark half-extent. The container wall and the mark are NOT peers — one
# encloses the other — so the clearance is the stroke<->mark floor (0.75 W), the
# same one radio-on's pip already uses, not the stroke<->stroke floor. That reads
# a full step bigger than the reference and is what the naive set was winning on.
def R_circ(): return 9.0 - W / 2 - gapm()             # mark INK extent 6.5 @ 2
def m_circ(): return min(5.5, R_circ() - W / 2)       # ... centreline  5.5 @ 2
def m_sq():   return min(4.5, 8.0 - W / 2 - gapm() - W / 2)   # 4.5 @ 2

# repeat pitch. Three bars 5 apart clear by 5 - W; three dots of radius W at
# pitch p clear by p - 3W. Both bind at W = 2.5 on the 24 grid.
def pitch_bar(): return max(5.0, 2.0 * W)
def r_more():    return W                # the dot IS the ink for more-*
def r_mark():    return 0.75 * W         # a dot used as a list marker

CP_TIP = [((0, 0.8479), (0, 0.7269), (0.00798, 0.6292)),
          ((0.01614, 0.5292), (0.03323, 0.4439), (0.07301, 0.3658)),
          ((0.13724, 0.2397), (0.23974, 0.1372), (0.36577, 0.07301)),
          ((0.44384, 0.03323), (0.52911, 0.01614), (0.62915, 0.00798)),
          ((0.72680, 0), (0.84783, 0), (1, 0))]
CP_BOX = [((0, 0.9017), (0, 0.8060), (0.0066, 0.7250)),
          ((0.0139, 0.6360), (0.0310, 0.5310), (0.0849, 0.4253)),
          ((0.1596, 0.2788), (0.2788, 0.1596), (0.4253, 0.0849)),
          ((0.5310, 0.0310), (0.6360, 0.0139), (0.7250, 0.0066)),
          ((0.8060, 0), (0.9017, 0), (1, 0))]

# ============================================================================
# PRIMITIVES
# ============================================================================
def f2(p): return '%g %g' % (round(p[0], 4), round(p[1], 4))
def unit(d):
    m = math.hypot(d[0], d[1]); return (d[0] / m, d[1] / m)

def corner(V, din, dout, e, cp=CP_TIP):
    def M(s, t): return (V[0] + e * (s * dout[0] - t * din[0]),
                         V[1] + e * (s * dout[1] - t * din[1]))
    out = 'L' + f2(M(0, 1))
    for c1, c2, p in cp:
        out += 'C%s %s %s' % (f2(M(*c1)), f2(M(*c2)), f2(M(*p)))
    return out

def rrect(x, y, w, h, e=None):
    e = e_cl() if e is None else e
    e = min(e, w / 2, h / 2)
    TL, TR, BR, BL = (x, y), (x + w, y), (x + w, y + h), (x, y + h)
    p = 'M' + f2((x + e, y))
    p += corner(TR, (1, 0), (0, 1), e, CP_BOX)
    p += corner(BR, (0, 1), (-1, 0), e, CP_BOX)
    p += corner(BL, (-1, 0), (0, -1), e, CP_BOX)
    p += corner(TL, (0, -1), (1, 0), e, CP_BOX)
    return p + 'Z'

def rrect_out(x, y, w, h):
    """The same container as a solid: grown W/2 on every side, and drawn at the
       measured OUTER extent rather than offset — offsetting a superellipse
       outward makes it rounder than one drawn at the bigger extent."""
    k = W / 2
    return rrect(x - k, y - k, w + 2 * k, h + 2 * k, e_out())

def head(V, d, run=None, e=None):
    run = run1() if run is None else run
    e = e_tip() if e is None else e
    d = unit(d); p = (-d[1], d[0])
    A1 = (V[0] - run * d[0] + run * p[0], V[1] - run * d[1] + run * p[1])
    A2 = (V[0] - run * d[0] - run * p[0], V[1] - run * d[1] - run * p[1])
    din  = unit((d[0] - p[0], d[1] - p[1]))
    dout = unit((-d[0] - p[0], -d[1] - p[1]))
    if e <= 0:
        return 'M%sL%sL%s' % (f2(A1), f2(V), f2(A2))
    return 'M%s%sL%s' % (f2(A1), corner(V, din, dout, e), f2(A2))

def bar(P, Q): return 'M%sL%s' % (f2(P), f2(Q))
def arc(cx, cy, r, a0, a1, sweep=1):
    p0 = (cx + r * math.cos(a0), cy + r * math.sin(a0))
    p1 = (cx + r * math.cos(a1), cy + r * math.sin(a1))
    big = 1 if abs(a1 - a0) > math.pi else 0
    return 'M%sA%g %g 0 %d %d %s' % (f2(p0), r, r, big, sweep, f2(p1))

def ink(*ds, **kw):
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%g" '
            'stroke-linecap="%s" stroke-linejoin="round"/>'
            % (''.join(ds), kw.get('c', 'currentColor'), kw.get('w', W),
               kw.get('cap', 'round')))

def solid(*ds, **kw):
    return '<path d="%s" fill="%s"/>' % (''.join(ds), kw.get('c', 'currentColor'))

def solidify(*ds, **kw):
    """Fill = the line silhouette flooded. Same path, filled AND stroked at W,
       which is exactly the outer offset. Used for organic shapes, where there
       is no measured outer target to draw against."""
    return ('<path d="%s" fill="%s" stroke="%s" stroke-width="%g" '
            'stroke-linejoin="round" stroke-linecap="round"/>'
            % (''.join(ds), kw.get('c', 'currentColor'),
               kw.get('c', 'currentColor'), W))

def dot(cx, cy, r, c='currentColor'):
    return '<circle cx="%g" cy="%g" r="%g" fill="%s"/>' % (cx, cy, r, c)
def ring(cx, cy, r):
    return ('<circle cx="%g" cy="%g" r="%g" fill="none" stroke="currentColor" '
            'stroke-width="%g"/>' % (cx, cy, r, W))

def knockout(u, body, cut, dilate=None, cap='round'):
    """Cut `cut` out of `body` with a moat. Masks, never paint."""
    d = moat() * 2 + W if dilate is None else dilate
    return ('<mask id="k%s" maskUnits="userSpaceOnUse"><rect width="24" '
            'height="24" fill="#fff"/><path d="%s" fill="none" stroke="#000" '
            'stroke-width="%g" stroke-linecap="%s" stroke-linejoin="round"/>'
            '</mask><g mask="url(#k%s)">%s</g>' % (u, cut, d, cap, u, body))

def scale_path_pts(pts, s, cx=C, cy=C):
    return [(cx + (x - cx) * s, cy + (y - cy) * s) for x, y in pts]

# ============================================================================
# DIRECTIONAL — ported from study 16, now on the axis
# ============================================================================
D8 = {'right': (1, 0), 'left': (-1, 0), 'up': (0, -1), 'down': (0, 1),
      'up-right': (1, -1), 'up-left': (-1, -1),
      'down-right': (1, 1), 'down-left': (-1, 1)}

def arrow(d, run=None, e=None):
    d = unit(d)
    reach = DIAG if abs(d[0] * d[1]) > 0.01 else REACH
    def f(u):
        r = run1() if run is None else run
        V = (C + reach * d[0], C + reach * d[1])
        T = (C - reach * d[0], C - reach * d[1])
        S = (V[0] - d[0], V[1] - d[1])
        return ink(bar(T, S), head(V, d, r, e))
    return f

def arrow_double(d):
    d = unit(d)
    reach = DIAG if abs(d[0] * d[1]) > 0.01 else REACH
    def f(u):
        r = run1()
        V1 = (C + reach * d[0], C + reach * d[1])
        V2 = (C + (reach - r) * d[0], C + (reach - r) * d[1])
        T  = (C - reach * d[0], C - reach * d[1])
        S  = (V2[0] - d[0], V2[1] - d[1])
        return ink(bar(T, S), head(V2, d, r), head(V1, d, r))
    return f

def arrow_bi(d):
    """Two heads facing out. The arm ends must clear each other by the
       stroke<->stroke floor, so reach >= run + W — which is why the old
       reach of 7 with a run of 4 was jammed."""
    d = unit(d)
    def f(u):
        r = run2()
        reach = min(9.5, max(8.5, r + W))
        V1 = (C + reach * d[0], C + reach * d[1])
        V2 = (C - reach * d[0], C - reach * d[1])
        P1 = (C + (reach - 1) * d[0], C + (reach - 1) * d[1])
        P2 = (C - (reach - 1) * d[0], C - (reach - 1) * d[1])
        return ink(bar(P2, P1), head(V1, d, r), head(V2, (-d[0], -d[1]), r))
    return f

def arrow_all():
    """Four open heads on one grid, which takes some arranging: adjacent heads
       approach on the diagonal long before either of them clogs. This used to
       duck the problem with a closed triangle, and the result was a second
       arrowhead family living inside an otherwise open-headed set."""
    def f(u):
        run = run_open()
        # Adjacent heads approach on the diagonal: the right head's upper arm
        # ends at (reach - run, -run) and the top head's right arm at
        # (run, -reach + run), so the clear distance between them is
        # (reach - 2 run) * sqrt2 - W. Solving that against the stroke floor
        # gives the reach the four heads need; the box then caps it, and 9.4 is
        # the floor so the figure does not collapse at the light end.
        reach = min(12.0 - W / 2,
                    max(9.4, 2 * run + (gap() + W) / math.sqrt(2)))
        L = reach                               # the shaft runs to the vertex
        parts = [bar((C - L, C), (C + L, C)), bar((C, C - L), (C, C + L))]
        heads = ''
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            heads += ink(head((C + reach * d[0], C + reach * d[1]), d, run))
        return ink(*parts) + heads
    return f

def arrow_turn(sign):
    def f(u):
        V  = (C + 7 * sign, 9.0)
        K  = (C - 6 * sign, 9.0)
        st = (V[0] - sign, 9.0)
        sh = 'M%s%sL%s' % (f2(st), corner(K, (-sign, 0), (0, 1), 8.0),
                           f2((K[0], 19.0)))
        return ink(sh, head(V, (sign, 0), run2()))
    return f

def chevron(d, n=1, run=None, e=None, shift=SHIFT):
    d = unit(d)
    def f(u):
        r = run1() if run is None else run
        tip = r * n / 2 + shift
        return ink(*[head((C + (tip - i * r) * d[0], C + (tip - i * r) * d[1]),
                          d, r, e) for i in range(n)])
    return f

def caret(d, run=5.0):
    d = unit(d); p = (-d[1], d[0])
    def f(u):
        V = (C + (run / 2 + SHIFT) * d[0], C + (run / 2 + SHIFT) * d[1])
        A1 = (V[0] - run * d[0] + run * p[0], V[1] - run * d[1] + run * p[1])
        A2 = (V[0] - run * d[0] - run * p[0], V[1] - run * d[1] - run * p[1])
        return solid('M%sL%sL%sZ' % (f2(A1), f2(V), f2(A2)))
    return f

def menu():
    def f(u):
        p = pitch_bar()
        return ink(*[bar((4, C + k * p), (20, C + k * p)) for k in (-1, 0, 1)])
    return f

def listicon():
    def f(u):
        p = pitch_bar(); r = r_mark()
        ys = [C - p, C, C + p]
        bars = [bar((9, ys[0]), (20, ys[0])), bar((9, ys[1]), (20, ys[1])),
                bar((9, ys[2]), (16, ys[2]))]
        return ink(*bars) + ''.join(dot(4.5, y, r) for y in ys)
    return f

def more(vertical=False):
    def f(u):
        p = 3.0 * W; r = r_more()
        return ''.join(dot(C if vertical else C + k * p, C + k * p if vertical else C, r)
                       for k in (-1, 0, 1))
    return f

def sort_icon():
    """Two shafts side by side. Their heads' arms have to clear each other, so
       the shaft separation is 2.5 W — exactly the 5 the reference sits at."""
    def f(u):
        r = run2(); dx = min(6.0, 2.5 * W)
        return ink(bar((C - dx, 6), (C - dx, 18)) + head((C - dx, 19), (0, 1), r),
                   bar((C + dx, 18), (C + dx, 6)) + head((C + dx, 5), (0, -1), r))
    return f

def sort_order():
    return lambda u: ink(head((C, 6), (0, -1), run2()), head((C, 18), (0, 1), run2()))

def swap_icon():
    def f(u):
        r = run2(); dy = min(6.0, 2.5 * W)
        return ink(bar((18, C - dy), (6, C - dy)) + head((5, C - dy), (-1, 0), r),
                   bar((6, C + dy), (18, C + dy)) + head((19, C + dy), (1, 0), r))
    return f

# ============================================================================
# ENCLOSURES AND TOGGLES — ported from study 17, now on the axis
# ============================================================================
CHECK_R = 1.2266        # the tick's bounding RADIUS, in units of its half-extent

def _enc_marks(m, radial=False):
    """The four marks sized to a half-extent m. `close` is measured on its
       diagonal, so its orthogonal half-side is m/sqrt2; `check` is a 3:5 tick
       whose bounding half-extent is m.

       `radial` sizes the tick by its bounding RADIUS rather than its bounding
       box. A square wall is a box and a box is what m measures, so a square
       container wants the plain figure. A circular wall is equidistant from the
       centre, and the tick's far corner sits CHECK_R x its half-extent out - so
       a tick sized to the box hangs 23% past the clearance the ring actually
       allows, and lands on it. That is the check-circle pair touching its wall,
       and it is why every other mark in here looked fine: add, subtract and
       close all top out at a radius of exactly m."""
    k = m / math.sqrt(2)
    if radial:
        m = m / CHECK_R
    # the tick's own proportions, normalised off the solo check: the long arm is
    # 1.745 x the short one and both run at 45
    def P(a, b): return (C + a * m, C + b * m)
    return {
      'add':      bar((C, C - m), (C, C + m)) + bar((C - m, C), (C + m, C)),
      'subtract': bar((C - m, C), (C + m, C)),
      'close':    bar((C - k, C - k), (C + k, C + k))
                  + bar((C + k, C - k), (C - k, C + k)),
      'check':    bar(P(-1.0, 0.0348), P(-0.3725, 0.6623))
                  + 'L' + f2(P(1.0, -0.7103)),
    }

def _solo_marks():
    return {
      'add':      bar((12, 6), (12, 18)) + bar((6, 12), (18, 12)),
      'subtract': bar((6, 12), (18, 12)),
      'close':    bar((6, 6), (18, 18)) + bar((18, 6), (6, 18)),
      'check':    bar((5.9571, 12.2071), (9.75, 16)) + 'L' + f2((18.0429, 7.7071)),
    }

def solo(name):
    return lambda u: ink(_solo_marks()[name])

def enclosed(mark, shape, fill=False):
    def f(u):
        m = _enc_marks(m_circ() if shape == 'circle' else m_sq(),
                       shape == 'circle')[mark]
        if shape == 'circle':
            line, sol = ring(C, C, 9.0), '<circle cx="12" cy="12" r="%g" fill="%%s"/>' % (9 + W / 2)
        else:
            line = ink(rrect(4, 4, 16, 16))
            sol  = '<path d="' + rrect_out(4, 4, 16, 16) + '" fill="%s"/>'
        if fill:
            return ('<mask id="k%s" maskUnits="userSpaceOnUse">%s%s</mask>'
                    '<g mask="url(#k%s)">%s</g>'
                    % (u, sol % '#fff', ink(m, c='#000'), u, sol % 'currentColor'))
        return line + ink(m)
    return f

def radio(on):
    def f(u):
        r = ring(C, C, 9.0)
        # the pip is a mark inside a container: (9 - W/2) - r_pip >= gapm
        return r + (dot(C, C, 9 - W / 2 - gapm()) if on else '')
    return f

def checkbox_off():
    return lambda u: ink(rrect(4, 4, 16, 16))

TRANSFER = {
  'share':    dict(box=(4, 10, 16, 10), tip=(12, 3),  d=(0, -1), tail=(12, 14.5)),
  'upload':   dict(box=(4, 4, 16, 12),  tip=(12, 9),  d=(0, -1), tail=(12, 21)),
  'download': dict(box=(4, 8, 16, 12),  tip=(12, 15), d=(0, 1),  tail=(12, 3)),
  'log-out':  dict(box=(4, 4, 10, 16),  tip=(21, 12), d=(1, 0),  tail=(9.5, 12)),
}

def transfer(name, fill=False):
    s = TRANSFER[name]
    x, y, w, h = s['box']
    d, tip, tail = unit(s['d']), s['tip'], s['tail']
    def f(u):
        stem  = bar(tail, (tip[0] - d[0], tip[1] - d[1]))
        arrow_ = stem + head(tip, d, run2())
        # A crossing moat is figure-ground separation, not stroke clearance -
        # and figure-ground is judged at the RENDERED size, which does not shrink
        # when the stroke does. So the arrow keeps a floor of 1.5 grid units of
        # air whatever the wall weighs. The arrow is the meaning in these four;
        # the container is context, and context can give way.
        dil = W + 2 * max(moat(), 1.5)
        if fill:
            out = rrect_out(x, y, w, h)
            mask = ('<mask id="t%s" maskUnits="userSpaceOnUse">'
                    '<path d="%s" fill="#fff"/><path d="%s" fill="none" '
                    'stroke="#000" stroke-width="%g" stroke-linecap="round" '
                    'stroke-linejoin="round"/></mask>' % (u, out, arrow_, dil))
            body = '<path d="%s" fill="currentColor" mask="url(#t%s)"/>' % (out, u)
        else:
            mask = ('<mask id="t%s" maskUnits="userSpaceOnUse"><rect width="24" '
                    'height="24" fill="#fff"/><path d="%s" fill="none" '
                    'stroke="#000" stroke-width="%g" stroke-linecap="butt"/>'
                    '</mask>' % (u, stem, dil))
            body = ('<path d="%s" fill="none" stroke="currentColor" '
                    'stroke-width="%g" stroke-linejoin="round" '
                    'mask="url(#t%s)"/>' % (rrect(x, y, w, h), W, u))
        return mask + body + ink(arrow_)
    return f

# ============================================================================
# NEW — search, edit, person, time, comms, status, media, files, system
# ============================================================================
SC, SR = (10.25, 10.25), 6.5            # search lens centre / centreline radius

def _lens_handle():
    k = SR / math.sqrt(2)
    return bar((SC[0] + k, SC[1] + k), (19.5, 19.5))

def search(mark=None):
    def f(u):
        parts = ring(SC[0], SC[1], SR) + ink(_lens_handle())
        if mark:
            m = SR - W / 2 - gap()          # half-extent inside the lens
            if mark == 'add':
                parts += ink(bar((SC[0], SC[1] - m), (SC[0], SC[1] + m)),
                             bar((SC[0] - m, SC[1]), (SC[0] + m, SC[1])))
            else:
                parts += ink(bar((SC[0] - m, SC[1]), (SC[0] + m, SC[1])))
        return parts
    return f

def filter_icon():
    def f(u):
        p = pitch_bar()
        return ink(bar((4, C - p), (20, C - p)),
                   bar((6.5, C), (17.5, C)),
                   bar((9, C + p), (15, C + p)))
    return f

# ---- pencil ---------------------------------------------------------------
def _pencil():
    u_ = unit((1, -1)); p = unit((1, 1)); h = 2.4
    P0, P1 = (5.5, 18.5), (17.0, 7.0)
    A = (P0[0] + h * p[0], P0[1] + h * p[1])
    B = (P1[0] + h * p[0], P1[1] + h * p[1])
    Cc = (P1[0] - h * p[0], P1[1] - h * p[1])
    Dd = (P0[0] - h * p[0], P0[1] - h * p[1])
    body = 'M%sL%sL%sL%sZ' % (f2(A), f2(B), f2(Cc), f2(Dd))
    Mi = (P1[0] - 4 * u_[0], P1[1] - 4 * u_[1])
    ferrule = bar((Mi[0] - h * p[0], Mi[1] - h * p[1]),
                  (Mi[0] + h * p[0], Mi[1] + h * p[1]))
    return body, ferrule

def edit(fill=False):
    def f(u):
        body, ferrule = _pencil()
        if fill:
            return knockout(u, solidify(body), ferrule, crease(), cap='butt')
        return ink(body) + ink(ferrule)
    return f

def trash(fill=False):
    def f(u):
        lid  = bar((4, 6.5), (20, 6.5))
        hand = 'M%s%s%sL%s' % (f2((9.5, 6.5)),
                 corner((9.5, 4.0), (0, -1), (1, 0), 1.5, CP_BOX),
                 corner((14.5, 4.0), (1, 0), (0, 1), 1.5, CP_BOX), f2((14.5, 6.5)))
        can  = 'M%s%s%sL%s' % (f2((6.0, 6.5)),
                 corner((6.6, 19.0), (0.048, 1), (1, 0), 2.2, CP_BOX),
                 corner((17.4, 19.0), (1, 0), (-0.048, -1), 2.2, CP_BOX),
                 f2((18.0, 6.5)))
        ribs = ink(bar((10.1, 10.0), (10.4, 16.0)), bar((13.9, 10.0), (13.6, 16.0)))
        if fill:
            return ink(lid) + ink(hand) + solidify(can + 'Z')
        return ink(lid) + ink(hand) + ink(can) + ribs
    return f

def bookmark(fill=False):
    def f(u):
        e = 2.4
        p = ('M' + f2((6.0, 20.5)) + 'L' + f2((6.0, 4.0 + e)))
        p += corner((6.0, 4.0), (0, -1), (1, 0), e, CP_BOX)
        p += corner((18.0, 4.0), (1, 0), (0, 1), e, CP_BOX)
        p += 'L' + f2((18.0, 20.5)) + 'L' + f2((12.0, 15.2)) + 'Z'
        return solidify(p) if fill else ink(p)
    return f

def _star_pts(ro=8.6, ri=3.7, cy=12.6):
    pts = []
    for i in range(5):
        a  = -math.pi / 2 + i * 2 * math.pi / 5
        b  = a + math.pi / 5
        pts.append((C + ro * math.cos(a), cy + ro * math.sin(a)))
        pts.append((C + ri * math.cos(b), cy + ri * math.sin(b)))
    return pts

def star(fill=False):
    def f(u):
        d = 'M' + 'L'.join(f2(q) for q in _star_pts()) + 'Z'
        return solidify(d) if fill else ink(d)
    return f

def heart(fill=False):
    def f(u):
        d = ('M12 20.1C6.6 16.2 3.2 13.3 3.2 9.7C3.2 7.1 5.2 5.1 7.8 5.1'
             'C9.6 5.1 11.1 6 12 7.4C12.9 6 14.4 5.1 16.2 5.1'
             'C18.8 5.1 20.8 7.1 20.8 9.7C20.8 13.3 17.4 16.2 12 20.1Z')
        return solidify(d) if fill else ink(d)
    return f

def flag(fill=False):
    def f(u):
        pole = bar((5.5, 3.5), (5.5, 20.5))
        e = 2.2
        ban = ('M' + f2((5.5, 4.5)) + 'L' + f2((18.5 - e, 4.5))
               + corner((18.5, 4.5), (1, 0), (0, 1), e, CP_BOX)
               + 'L' + f2((18.5, 13.5 - e))
               + corner((18.5, 13.5), (0, 1), (-1, 0), e, CP_BOX)
               + 'L' + f2((5.5, 13.5)))
        return ink(pole) + (solidify(ban + 'Z') if fill else ink(ban))
    return f

def link():
    def f(u):
        # two hooks on the 45 diagonal, each an arc, clearing by gap()
        a = ('M9.2 14.8L14.8 9.2M10.6 7.8L12.4 6C14 4.4 16.6 4.4 18.2 6'
             'C19.8 7.6 19.8 10.2 18.2 11.8L16.4 13.6')
        b = ('M13.4 16.2L11.6 18C10 19.6 7.4 19.6 5.8 18'
             'C4.2 16.4 4.2 13.8 5.8 12.2L7.6 10.4')
        return ink(a) + ink(b)
    return f

def external():
    def f(u):
        box = ('M' + f2((19.0, 13.5)) + 'L' + f2((19.0, 20.0 - e_cl()))
               + corner((19.0, 20.0), (0, 1), (-1, 0), e_cl(), CP_BOX)
               + 'L' + f2((5.0 + e_cl(), 20.0))
               + corner((5.0, 20.0), (-1, 0), (0, -1), e_cl(), CP_BOX)
               + 'L' + f2((5.0, 5.0 + e_cl()))
               + corner((5.0, 5.0), (0, -1), (1, 0), e_cl(), CP_BOX)
               + 'L' + f2((10.5, 5.0)))
        d = unit((1, -1))
        V = (20.0, 4.0)
        return ink(box) + ink(bar((13.0, 11.0), (V[0] - d[0], V[1] - d[1])),
                              head(V, d, run2()))
    return f

# ---- person ---------------------------------------------------------------
# Measured off person-user-line, not invented: head centreline radius 4 at
# (12, 7); shoulders half-width 7, arch top y 14, base y 20. Head ink bottom 12,
# shoulder ink top 13 - a gap of 1, i.e. 0.5 W. Two big masses read across a
# smaller gap than two thin strokes do, which is what gaps() is for.
PERSON = dict(cx=12.0, hy=7.0, rh=4.0, half=7.0, base=20.0)

def _person(s=1.0, cx=None, hy=None, top=None, base=20.0):
    """One person at scale s. Head radius 4 at (12, 7), shoulders 7 wide, arch
       top 14, base 20 - every number off person-user-line, and at s = 1 this
       reproduces it exactly.

       `top` may be given instead of derived, and then `hy` follows from it. That
       is what people uses: both figures share ONE shoulder line, so the smaller
       one has nothing standing above the larger one's silhouette."""
    P = PERSON
    cx = P['cx'] if cx is None else cx
    rh, half = P['rh'] * s, P['half'] * s
    if top is None:
        hy = (12.0 - 5.0 * s) if hy is None else hy
        top = hy + rh + W + gaps()
    elif hy is None:
        hy = top - rh - W - gaps()
    kx = half * 0.60
    body = ('M%s C%s %s %s C%s %s %s'
            % (f2((cx - half, base)),
               f2((cx - half, top + (base - top) * 0.38)), f2((cx - kx, top)), f2((cx, top)),
               f2((cx + kx, top)), f2((cx + half, top + (base - top) * 0.38)),
               f2((cx + half, base))))
    return (cx, hy, rh), body, top

def _head_ring(cx, hy, rh, fill):
    return dot(cx, hy, rh + W / 2) if fill else ring(cx, hy, rh)

def _body_paint(body, fill):
    if not fill:
        return ink(body)
    return ('<path d="%s" fill="currentColor" stroke="currentColor" '
            'stroke-width="%g" stroke-linejoin="round" stroke-linecap="round"/>'
            % (body + 'Z', W))

def person(fill=False):
    def f(u):
        (cx, hy, rh), body, _ = _person()
        return _head_ring(cx, hy, rh, fill) + _body_paint(body, fill)
    return f

def _occlude(u, behind, head, body):
    """What one person takes out of the person behind: the FILLED silhouette
       plus a moat, not the stroked outline. Cutting only the outline is why the
       back figure's far leg used to show through under the front one's arch."""
    cx, cy, r = head
    return ('<mask id="k%s" maskUnits="userSpaceOnUse"><rect width="24" '
            'height="24" fill="#fff"/>'
            '<circle cx="%g" cy="%g" r="%g" fill="#000"/>'
            '<path d="%sZ" fill="#000" stroke="#000" stroke-width="%g" '
            'stroke-linejoin="round" stroke-linecap="round"/>'
            '</mask><g mask="url(#k%s)">%s</g>'
            % (u, cx, cy, r + W / 2 + gapm(), body, W + 2 * gapm(), u, behind))

def people(fill=False):
    """Two of the same person, the back one smaller and to the right. Both share
       the FRONT figure's shoulder line, so the smaller figure has nothing
       standing above the larger one - it emerges from behind its flank, which is
       what the reference does. Widest ink lands at 21.9, inside the box."""
    def f(u):
        (fx, fhy, frh), fbody, ftop = _person(s=0.92, cx=9.4)
        (bx, bhy, brh), bbody, _    = _person(s=0.76, cx=15.6, top=ftop)
        front  = _head_ring(fx, fhy, frh, fill) + _body_paint(fbody, fill)
        behind = _head_ring(bx, bhy, brh, False) + ink(bbody)
        return _occlude(u, behind, (fx, fhy, frh), fbody) + front
    return f

def person_badge(mark):
    """The badge takes the REGULAR moat out of the figure: its own path stroked
       at W + 2 x badge(), so the counter follows the plus or the tick instead of
       being a disc big enough to contain it."""
    def f(u):
        (cx, hy, rh), body, _ = _person(s=0.88, cx=10.4)
        base = ring(cx, hy, rh) + ink(body)
        bx, by, m = 18.2, 17.8, 2.4
        if mark == 'add':
            d = bar((bx, by - m), (bx, by + m)) + bar((bx - m, by), (bx + m, by))
        else:
            d = (bar((bx - m, by + 0.035 * m), (bx - 0.3725 * m, by + 0.6623 * m))
                 + 'L' + f2((bx + m, by - 0.7103 * m)))
        return knockout(u, base, d, W + 2 * badge()) + ink(d)
    return f

# ---- time -----------------------------------------------------------------
def clock(fill=False):
    def f(u):
        # hand tips must clear the ring's inner ink by gap()
        reach = 9 - W / 2 - W / 2 - gap()          # 6.0 @ W=2
        hands = bar((C, C - reach), (C, C)) + 'L' + f2((C + reach - 2, C))
        if fill:
            return ('<mask id="k%s" maskUnits="userSpaceOnUse">'
                    '<circle cx="12" cy="12" r="%g" fill="#fff"/>'
                    '<path d="%s" fill="none" stroke="#000" stroke-width="%g" '
                    'stroke-linecap="round" stroke-linejoin="round"/></mask>'
                    '<circle cx="12" cy="12" r="%g" fill="currentColor" '
                    'mask="url(#k%s)"/>'
                    % (u, 9 + W / 2, hands, W, 9 + W / 2, u))
        return ring(C, C, 9.0) + ink(hands)
    return f

def timer():
    """A stopwatch: ring, crown, and a hand that starts at the centre. The old
       one drew a bar floating in the middle with no pivot, so it read as a
       stem rather than a hand."""
    def f(u):
        r, cy = 7.6, 13.6
        reach = r - W / 2 - gap() - W / 2                  # 4.6 @ 2
        d = unit((0.55, -1.0))
        hand = bar((C, cy), (C + reach * d[0], cy + reach * d[1]))
        neck = bar((C, cy - r - W / 2 - 0.4), (C, 4.4))     # sits ON the ring
        crown = bar((C - 2.6, 3.2), (C + 2.6, 3.2))
        return ring(C, cy, r) + ink(hand) + ink(neck) + ink(crown) + dot(C, cy, W / 2)
    return f

def history():
    """A clock ring turned back on itself, counter-clockwise. An OPEN head cannot
       go on a ring this size — its outer arm sits at sqrt((r+run)^2 + run^2) from
       the centre, 13.2 at r 8.4 and run 4 — so the head closes and is inscribed
       on the ring. Same primitive, same optical skew, as refresh."""
    def f(u):
        run = run_open()
        r = ring_r(8.4, run)             # the head decides how big the ring can be
        a_t = math.radians(214)                          # tip, upper left
        brk = (gap() + W / 2) / r                        # clear air ahead of it
        reach = r - W / 2 - gap() - W / 2
        hands = (bar((C, C - reach), (C, C)) + 'L'
                 + f2((C + reach * 0.64, C + reach * 0.64)))
        # the arc runs all the way INTO the head, the way a shaft does on a
        # straight arrow — an open head has a vertex to arrive at
        return (ink(arc(C, C, r, a_t, a_t + 2 * math.pi - brk))
                + ring_head(r, a_t, run, ccw=True)
                + ink(hands))
    return f

def calendar(fill=False):
    """Body 4..20 both ways, header rule at y 8, posts from y 2 down to the wall.
       All four numbers are the reference's. The posts used to run 2 units PAST
       the wall, which is what made the frame look welded shut."""
    x, y, w, h = 4.0, 4.0, 16.0, 16.0
    def f(u):
        # The rule has to land on STRAIGHT wall. At y 8 it meets the corner arc
        # at W 2 and sits inside it at every lighter weight, which is what made
        # the band look like it stopped short of the frame instead of crossing
        # it. Clear the corner's tangent by the intra-glyph floor instead.
        hy = y + e_cl() + gapi()
        hdr = bar((x, hy), (x + w, hy))
        posts = ink(bar((7.0, 2.0), (7.0, y)), bar((17.0, 2.0), (17.0, y)))
        if fill:
            body = '<path d="%s" fill="currentColor"/>' % rrect_out(x, y, w, h)
            return knockout(u, body, hdr, crease(), cap='butt') + posts
        return ink(rrect(x, y, w, h)) + ink(hdr) + posts
    return f

# ---- comms ----------------------------------------------------------------
def chat(fill=False):
    x, y, w, h = 4.0, 4.5, 16.0, 12.0
    def f(u):
        e = e_cl(); tw, tx = 4.0, 8.0
        p = 'M' + f2((x + e, y))
        p += corner((x + w, y), (1, 0), (0, 1), e, CP_BOX)
        p += corner((x + w, y + h), (0, 1), (-1, 0), e, CP_BOX)
        p += 'L' + f2((tx + tw, y + h))
        p += 'L' + f2((tx, 20.5))
        p += 'L' + f2((tx, y + h))
        p += corner((x, y + h), (-1, 0), (0, -1), e, CP_BOX)
        p += corner((x, y), (0, -1), (1, 0), e, CP_BOX) + 'Z'
        return solidify(p) if fill else ink(p)
    return f

def mail(fill=False):
    x, y, w, h = 3.5, 5.5, 17.0, 13.0
    def f(u):
        flap = bar((x + 0.6, y + 1.6), (C, y + 7.0)) + 'L' + f2((x + w - 0.6, y + 1.6))
        if fill:
            body = '<path d="%s" fill="currentColor"/>' % rrect_out(x, y, w, h)
            return knockout(u, body, flap, crease(), cap='butt')
        return ink(rrect(x, y, w, h)) + ink(flap)
    return f

def bell(fill=False, off=False):
    def f(u):
        base_y = 15.5
        dome = ('M%s L%s C%s %s %s C%s %s %s L%s'
                % (f2((18.0, base_y)), f2((18.0, 10.5)),
                   f2((18.0, 7.2)), f2((15.3, 4.5)), f2((C, 4.5)),
                   f2((8.7, 4.5)), f2((6.0, 7.2)), f2((6.0, 10.5)),
                   f2((6.0, base_y))))
        rail = bar((3.5, base_y), (20.5, base_y))
        clap = ('M%s C%s %s %s C%s %s %s'
                % (f2((9.8, base_y + gap() + W)),
                   f2((10.4, 20.9)), f2((11.1, 21.2)), f2((C, 21.2)),
                   f2((12.9, 21.2)), f2((13.6, 20.9)), f2((14.2, base_y + gap() + W))))
        body = (solidify(dome + 'Z') + ink(rail)) if fill else (ink(dome) + ink(rail))
        out = body + ink(clap)
        if off:
            # A 45 slash enters the dome ~3.5 along the arc from its end, so a
            # full moat leaves a floating stub. The off-slash therefore takes a
            # half moat: enough to read as a break, not enough to orphan.
            slash = bar((4.4, 19.6), (19.6, 4.4))
            return knockout(u, out, slash, W + moat()) + ink(slash)
        return out
    return f

def call(fill=False):
    def f(u):
        d = ('M8.6 4.2L11.2 8.6L9.0 10.8C9.9 13.2 10.8 14.1 13.2 15.0L15.4 12.8'
             'L19.8 15.4L19.8 18.4C19.8 19.6 19.0 20.3 17.8 20.2'
             'C10.6 19.5 4.5 13.4 3.8 6.2C3.7 5.0 4.4 4.2 5.6 4.2Z')
        return solidify(d) if fill else ink(d)
    return f

# ---- status ---------------------------------------------------------------
def e_for_r(r, din, dout):
    """Corner extent that lands a given corner RADIUS at a given vertex angle.

       `e` is a tangent length, not a radius: corner() puts the curve's ends e
       back along each edge. For a corner of interior angle th the inscribed
       radius is e*tan(th/2), so going the other way is e = r/tan(th/2). Which
       matters the moment one polygon has vertices of different sharpness — a
       triangle's apex needs a much longer reach than its base corners to read
       at the same r, and a single flat extent gives the two corners visibly
       different roundness. §4.2 specifies a radius, so solve for it."""
    cos_th = -(din[0] * dout[0] + din[1] * dout[1])       # interior angle
    th = math.acos(max(-1.0, min(1.0, cos_th)))
    return r / math.tan(th / 2.0)

def ngon(pts, e, cp=CP_BOX):
    """Closed polygon with every vertex rounded to extent e on the given profile.
       Arrival and departure directions come from the neighbours, so the same
       call handles a triangle, a play button or a gear tooth.

       `e` may be a per-vertex sequence, for a polygon whose corners are not all
       the same angle — see e_for_r()."""
    n = len(pts)
    es = list(e) if isinstance(e, (list, tuple)) else [e] * n
    segs = []
    for i in range(n):
        P, Q, R = pts[(i - 1) % n], pts[i], pts[(i + 1) % n]
        din  = unit((Q[0] - P[0], Q[1] - P[1]))
        dout = unit((R[0] - Q[0], R[1] - Q[1]))
        ei = min(es[i], math.hypot(Q[0] - P[0], Q[1] - P[1]) / 2,
                        math.hypot(R[0] - Q[0], R[1] - Q[1]) / 2)
        segs.append((Q, din, dout, ei))
    Q, din, dout, ei = segs[0]
    out = 'M' + f2((Q[0] - ei * din[0], Q[1] - ei * din[1]))
    for Q, din, dout, ei in segs:
        out += corner(Q, din, dout, ei, cp)
    return out + 'Z'

def ring_barb(r, a_tip, dep, half, ccw=True, cx=C, cy=C):
    """A closed arrowhead inscribed ON a ring.

       Tip on the circle; base a chord `dep` back along travel; base corners
       +/- half across that chord. Then the whole barb is rotated about its tip
       by a QUARTER of the subtended angle, toward the tangent.

       That last step is the optical correction. A head whose axis is the chord
       lags the tangent at the tip by half the subtended angle, so it reads as
       leaning into the circle even though it is geometrically exact. Splitting
       the difference makes it look placed. The resulting angle is not a round
       number and does not need to be — nothing downstream depends on it."""
    sgn = 1.0 if ccw else -1.0            # ccw on screen = decreasing theta
    dth = dep / r
    a_b = a_tip + sgn * dth
    T = (cx + r * math.cos(a_tip), cy + r * math.sin(a_tip))
    B = (cx + r * math.cos(a_b),   cy + r * math.sin(a_b))
    L = math.hypot(T[0] - B[0], T[1] - B[1])
    e = ((T[0] - B[0]) / L, (T[1] - B[1]) / L)
    phi = -sgn * dth / 4.0
    ca, sa = math.cos(phi), math.sin(phi)
    e = (e[0] * ca - e[1] * sa, e[0] * sa + e[1] * ca)
    Bc = (T[0] - L * e[0], T[1] - L * e[1])
    p = (-e[1], e[0])
    return solid(ngon([T, (Bc[0] + half * p[0], Bc[1] + half * p[1]),
                          (Bc[0] - half * p[0], Bc[1] - half * p[1])], e_tip()))

RING_OFF = 15.0          # degrees the head's axis leans OUT of the tangent

def run_open(): return 1.607 * W
    # ^ the smallest 45 arm that still clears the notch: notch = run - 1.207 W,
    #   and the intra-glyph floor is 0.40 W, so run >= 1.607 W. Everything below
    #   spends its remaining room on the arm rather than on the shaft.

def ring_r(r_want, run, off=RING_OFF):
    """The largest ring that still holds an OPEN head inside the box.

       A 45 head throws its arms run*sqrt2 back from the tip. Laid on the raw
       tangent the outer arm lands at sqrt((r + run)^2 + run^2) - 13.2 at r 8.4,
       which is off the canvas, and that is why these two used to carry a closed
       triangle while every other arrow in the set carried an open head. Two
       arrowhead families in one set is exactly the drift worth removing.

       Leaning the axis OUT of the tangent by RING_OFF swings that arm back
       along the ring instead of past it. What is left is a straight solve: put
       the arm's own corner on the box and read off the radius."""
    o = math.radians(off)
    ct, st = math.cos(o), math.sin(o)
    at = (ct + st) * run                 # arm reach along the tangent
    ar = (ct - st) * run                 # ... and outward, radially
    lim = 12.0 - W / 2
    inner = lim * lim - at * at
    if inner <= 0:
        return r_want
    return min(r_want, math.sqrt(inner) - ar)

def ring_head(r, a_tip, run, off=RING_OFF, ccw=True, cx=C, cy=C):
    """An open head at a point on a ring, its axis leaned out of the tangent."""
    sgn = 1.0 if ccw else -1.0           # ccw on screen = decreasing theta
    ca, sa = math.cos(a_tip), math.sin(a_tip)
    t = (sgn * sa, -sgn * ca)            # direction of travel at the tip
    o = math.radians(off)
    ct, st = math.cos(o), math.sin(o)
    d = (ct * t[0] + st * ca, ct * t[1] + st * sa)
    return ink(head((cx + r * ca, cy + r * sa), d, run))

def barb_dep():  return (W + gapm()) * 1.25    # 4.375 @ 2
def barb_half(): return W + gapm() / 2         # 2.75  @ 2

TRI = ((12.0, 3.2), (20.9, 19.7), (3.1, 19.7))
TRI_E = 2.9

def _tri_top():
    """Where a mark on the axis may start. Two things push it down from the
       apex: the rounded corner only comes within 0.3228 e of the vertex, and a
       wedge of half-angle a offsets its own apex inward by (W/2)/sin a."""
    A, R, L = TRI
    alpha = math.atan2((R[0] - A[0]), (R[1] - A[1]))
    return A[1] + 0.3228 * TRI_E + (W / 2) / math.sin(alpha) + gapm()

def warning(fill=False):
    """Bang inside a triangle. Placed from BOTH ends inward: the stem starts where
       the apex wedge lets it, the dot's ink stops exactly gapm() short of the
       base, and whatever is left is the stem. When that leaves the stem shorter
       than 1.5 W the DOT gives way instead - a short stem reads as a second dot,
       which is worse than a small one."""
    def f(u):
        t = ngon(list(TRI), TRI_E)
        top = _tri_top()
        L = TRI[1][1] - W / 2 - gapm()                   # lowest ink allowed
        A = L - top                                      # all the room there is
        r = (A - W / 2 - gapi() - 1.5 * W) / 2
        r = min(r_mark(), max(0.40 * W, r))
        bottom = max(top + W, A + top - W / 2 - gapi() - 2 * r)
        dy = bottom + W / 2 + gapi() + r
        stem = bar((C, top), (C, bottom))
        if fill:
            return ('<mask id="k%s" maskUnits="userSpaceOnUse">'
                    '<path d="%s" fill="#fff" stroke="#fff" stroke-width="%g" '
                    'stroke-linejoin="round"/>'
                    '<path d="%s" fill="none" stroke="#000" stroke-width="%g" '
                    'stroke-linecap="round"/>'
                    '<circle cx="12" cy="%g" r="%g" fill="#000"/></mask>'
                    '<g mask="url(#k%s)">%s</g>'
                    % (u, t, W, stem, W, dy, r, u, solidify(t)))
        return ink(t) + ink(stem) + dot(C, dy, r)
    return f

# The ? loop, in units of its own height, measured off the drawing that read
# best and then normalised so it can be scaled into whatever box it lands in.
# Origin is the hook's lower END; y negative going up; height 1.
QMARK = [(-0.3827, -0.6049),
         (-0.3580, -0.8519), (-0.1975, -1.0000), ( 0.0247, -1.0000),
         ( 0.2593, -1.0000), ( 0.4198, -0.8519), ( 0.4198, -0.6420),
         ( 0.4198, -0.4568), ( 0.3210, -0.3704), ( 0.1481, -0.2593),
         ( 0.0370, -0.1852), ( 0.0000, -0.1111), ( 0.0000,  0.0000)]
QMARK_H = 8.1          # the height it was drawn at - never scale UP past this

def info(fill=False, question=False):
    """i and ? in a ring. Both are laid out from the ring's mark box inward: the
       dot goes hard against one end of the box, the other glyph takes what is
       left, and the two are spaced by gapi() because they are one mark. So
       neither can grow into the wall at any weight."""
    def f(u):
        R, r = R_circ(), r_mark()
        if question:
            # cap the loop at the height it was drawn, then CENTRE the whole
            # glyph in the box rather than hanging it from the top
            H = min(QMARK_H, 2 * R - W - gapi() - 2 * r)
            Ht = W + gapi() + 2 * r + H                  # total ink height
            E = (C, C - Ht / 2 + W / 2 + H)              # the hook's lower end
            d = 'M' + f2((E[0] + QMARK[0][0] * H, E[1] + QMARK[0][1] * H))
            for i in range(1, len(QMARK), 3):
                d += 'C' + ' '.join(f2((E[0] + px * H, E[1] + py * H))
                                    for px, py in QMARK[i:i + 3])
            marks = [(d, None), (None, (C, E[1] + W / 2 + gapi() + r))]
        else:
            SH = min(7.2, 2 * R - W - gapi() - 2 * r)    # stem, same cap habit
            Ht = W + gapi() + 2 * r + SH
            dy = C - Ht / 2 + r
            marks = [(bar((C, dy + r + gapi() + W / 2),
                          (C, dy + r + gapi() + W / 2 + SH)), None),
                     (None, (C, dy))]
        def paint(colour):
            out = ''
            for dd, pt in marks:
                out += ink(dd, c=colour) if dd else dot(pt[0], pt[1], r, colour)
            return out
        if fill:
            sol = '<circle cx="12" cy="12" r="%g" fill="%%s"/>' % (9 + W / 2)
            return ('<mask id="k%s" maskUnits="userSpaceOnUse">%s%s</mask>'
                    '<g mask="url(#k%s)">%s</g>'
                    % (u, sol % '#fff', paint('#000'), u, sol % 'currentColor'))
        return ring(C, C, 9.0) + paint('currentColor')
    return f

# ---- media ---------------------------------------------------------------
# Measured off play-line / play-fill, not invented. The reference ships
# expanded outlines, so the drawing IS the silhouette and the nominal triangle
# has to be recovered: take the straight run either side of each corner, extend
# both, intersect. Doing that to the inner contour gives round numbers -
# (7,4), (20,12), (7,20) - with a wall of exactly 2 and a corner radius of 2.5
# on all three vertices. So the centreline triangle is that inner one offset
# outward by W/2, which at W = 2 is:
PLAY_TRI = ((6.0, 2.212), (21.908, 12.0), (6.0, 21.788))

def e_play():
    """Corner extent for the play triangle.

       The reference rounds all three vertices to the same RADIUS (2.5 outer,
       so 1.5 on the centreline), but ngon rounds to a constant EXTENT, and
       extent = r / tan(half the interior angle). The three angles here are
       58.4, 63.2 and 58.4 degrees, so one extent of 0.65 W puts the radii at
       1.45 / 1.60 / 1.45 against a target of 1.5 - under a tenth of a unit
       out, which is nothing at 24px."""
    return 0.65 * W

def play(fill=False):
    def f(u):
        p = ngon(list(PLAY_TRI), e_play())
        return solidify(p) if fill else ink(p)
    return f

# pause is NOT two bars. The reference draws two CONTAINERS: outer 7 x 18 at
# 3.5..10.5 and 13.5..20.5, y 3..21, corner radius 2.5, wall exactly 2. On the
# centreline that is 5 x 16 boxes at 4.5 and 14.5, y 4..20.
PAUSE_BOX = ((4.5, 4.0, 5.0, 16.0), (14.5, 4.0, 5.0, 16.0))

def pause(fill=False):
    """Two containers, the reference's own, at 1.5 W apart.

       The old drawing was two round-capped bars on a 9..15 ink box - a third
       the mass of play-fill, so in a single play/pause button the paused state
       read as the disabled one. These two boxes span 3.5..20.5 against play's
       5..21.6, which is what makes the pair swap without the button changing
       weight.

       The gap between them is 3, i.e. 1.5 W. That is above the stroke<->stroke
       floor rather than on it, and deliberately: at the floor the two bars fuse
       into one slab at 16px."""
    def f(u):
        e = 0.75 * W                                  # centreline r; outer 2.5 @ 2
        if fill:
            k = W / 2
            return solid(*[rrect(x - k, y - k, w + 2 * k, h + 2 * k, e + k)
                           for x, y, w, h in PAUSE_BOX])
        return ink(*[rrect(x, y, w, h, e) for x, y, w, h in PAUSE_BOX])
    return f

def skip(sign):
    """Caret-shaped triangle plus a stop bar; the gap between them is the floor."""
    def f(u):
        bx = C + 5.6 * sign
        vx = bx - sign * (W + gap())          # apex stops one floor short of the bar
        return (solidify(ngon([(vx, 12.0), (C - 7.4 * sign, 6.2),
                               (C - 7.4 * sign, 17.8)], 1.4))
                + ink(bar((bx, 5.6), (bx, 18.4))))
    return f

def volume(level=2):
    """Cone plus `level` arcs. The arcs are struck from the cone's MOUTH, and an
       arc's nearest point to that mouth is r*cos(span) - so the first radius is
       whatever puts gap() of air there, not a number picked by eye. The old cone
       ran to x 12.4 and left the first arc no room at all."""
    MOUTH, SPAN = 10.6, math.radians(45)
    def f(u):
        cone = ('M%sL%sL%sL%sL%sL%sZ' % (f2((3.6, 9.5)), f2((7.0, 9.5)),
                f2((MOUTH, 5.2)), f2((MOUTH, 18.8)), f2((7.0, 14.5)), f2((3.6, 14.5))))
        out = solidify(cone)
        if level == 0:
            m = W + gapm()
            cx = MOUTH + W / 2 + gap() + m
            return (out + ink(bar((cx - m, 12 - m), (cx + m, 12 + m)))
                        + ink(bar((cx + m, 12 - m), (cx - m, 12 + m))))
        r0 = (W / 2 + gap() + W / 2) / math.cos(SPAN)      # 5.23 @ W=2
        waves = ''
        for i in range(level):
            r = r0 + i * (W + gap())
            waves += arc(MOUTH, 12.0, r, -SPAN, SPAN)
        return out + ink(waves)
    return f

# ---- files ---------------------------------------------------------------
def file_icon(fill=False):
    """A page with a dog-ear. In the fill the fold is an L-shaped CREASE, so the
       corner tab survives as solid ink - dilating it by a full moat is what was
       erasing the tab entirely."""
    def f(u):
        e = e_cl(); k = 6.0
        x0, x1, y0, y1 = 5.0, 19.0, 3.5, 20.5
        page = ('M' + f2((x1 - k, y0))
                + 'L' + f2((x1, y0 + k))
                + 'L' + f2((x1, y1 - e))
                + corner((x1, y1), (0, 1), (-1, 0), e, CP_BOX)
                + 'L' + f2((x0 + e, y1))
                + corner((x0, y1), (-1, 0), (0, -1), e, CP_BOX)
                + 'L' + f2((x0, y0 + e))
                + corner((x0, y0), (0, -1), (1, 0), e, CP_BOX) + 'Z')
        crs = ('M' + f2((x1 - k, y0)) + 'L' + f2((x1 - k, y0 + k))
               + 'L' + f2((x1, y0 + k)))
        if fill:
            return knockout(u, solidify(page), crs, crease(), cap='butt')
        return ink(page) + ink(crs)
    return f

def folder(fill=False, open_=False):
    def f(u):
        e = e_cl(); y0, y1 = 5.5, 19.5
        x0, x1 = 3.5, 20.5
        tab = 10.5
        p = ('M' + f2((x0 + e, y0))
             + 'L' + f2((tab - 1.4, y0)) + 'L' + f2((tab + 1.2, y0 + 2.4))
             + 'L' + f2((x1 - e, y0 + 2.4))
             + corner((x1, y0 + 2.4), (1, 0), (0, 1), e, CP_BOX)
             + 'L' + f2((x1, y1 - e))
             + corner((x1, y1), (0, 1), (-1, 0), e, CP_BOX)
             + 'L' + f2((x0 + e, y1))
             + corner((x0, y1), (-1, 0), (0, -1), e, CP_BOX)
             + 'L' + f2((x0, y0 + e))
             + corner((x0, y0), (0, -1), (1, 0), e, CP_BOX) + 'Z')
        if open_:
            # FLAT, not axonometric: the front pocket is the same rounded box,
            # dropped so the back plate shows above it. A lifted parallelogram
            # is a 3D shape and this set does not have one.
            fy = 11.6
            front = rrect(x0, fy, x1 - x0, y1 - fy, min(e_cl(), (y1 - fy) / 2))
            return ('<mask id="k%s" maskUnits="userSpaceOnUse"><rect width="24" '
                    'height="24" fill="#fff"/><path d="%s" fill="#000" '
                    'stroke="#000" stroke-width="%g" stroke-linejoin="round"/>'
                    '</mask><g mask="url(#k%s)">%s</g>%s'
                    % (u, front, W + 2 * gapm(), u, ink(p), ink(front)))
        return solidify(p) if fill else ink(p)
    return f

# ---- system --------------------------------------------------------------
def home(fill=False):
    """One pentagon and one arched door. The old one drew the roof and the walls
       as separate strokes whose ends did not meet, which is where the hanging
       eave came from. A simplified home has no eave at all."""
    def f(u):
        apex, sh, base, hx = (12.0, 3.4), 11.0, 20.4, 8.7
        house = ngon([apex, (C + hx, sh), (C + hx, base),
                      (C - hx, base), (C - hx, sh)], 2.2)
        dw, dh = 2.5, 6.4                      # door half-width, height
        arch = 'A%g %g 0 0 1 %s' % (dw, dw, f2((C + dw, base - dh + dw)))
        door = ('M' + f2((C - dw, base)) + 'L' + f2((C - dw, base - dh + dw))
                + arch + 'L' + f2((C + dw, base)))
        if fill:
            hole = ('M' + f2((C - dw, base + 1)) + 'L' + f2((C - dw, base - dh + dw))
                    + arch + 'L' + f2((C + dw, base + 1)) + 'Z')
            # an interior hole is NOT dilated: a moat applies only where a mark
            # crosses a wall, and this one does not
            return ('<mask id="k%s" maskUnits="userSpaceOnUse"><rect width="24" '
                    'height="24" fill="#fff"/><path d="%s" fill="#000"/></mask>'
                    '<g mask="url(#k%s)">%s</g>'
                    % (u, hole, u, solidify(house)))
        return ink(house) + ink(door)
    return f

def gear_pts(n=6, r_out=9.0, r_in=6.4, tooth=0.42, shoulder=0.13):
    """Cog polygon: n teeth, each a flat top at r_out and a valley at r_in.
       Six wide teeth read as a gear; eight narrow ones read as a flower, which
       is what the last one was."""
    p = 2 * math.pi / n
    pts = []
    for i in range(n):
        a = i * p - math.pi / 2
        for frac, r in ((-tooth / 2, r_out), (tooth / 2, r_out),
                        (tooth / 2 + shoulder, r_in),
                        (1 - tooth / 2 - shoulder, r_in)):
            t = a + frac * p
            pts.append((C + r * math.cos(t), C + r * math.sin(t)))
    return pts

def settings():
    """Cog plus a solid hub. The hub is the biggest dot that still clears the
       valley floor by the mark floor - 2.9 at W 2, which is the 3 the reference
       draws."""
    def f(u):
        r_in, n, tooth, shoulder = 6.4, 6, 0.42, 0.13
        # the valley is a CHORD between two points at r_in, so the wall actually
        # dips inside it — measure the chord, not the radius
        span = (1 - tooth - 2 * shoulder) * (2 * math.pi / n)
        r_wall = r_in * math.cos(span / 2)
        # The hub is a RING, not a disc. A solid hub is the only filled mass in
        # an otherwise stroked glyph, so it reads as a fill variant that wandered
        # into the line set. Same outer extent, so the clearance is unchanged.
        hub = r_wall - W / 2 - gapm() - W / 2
        return (ink(ngon(gear_pts(n=n, r_in=r_in, tooth=tooth, shoulder=shoulder), 0.8))
                + ring(C, C, hub))
    return f

def grid():
    def f(u):
        s = (14.0 - gap() - W) / 2          # cell centreline side
        g = gap() + W
        for_ = []
        for cx in (12 - g / 2 - s / 2, 12 + g / 2 + s / 2):
            for cy in (12 - g / 2 - s / 2, 12 + g / 2 + s / 2):
                for_.append(rrect(cx - s / 2, cy - s / 2, s, s, min(1.6, s / 2)))
        return ink(*for_)
    return f

def lock(open_=False):
    """Body and shackle, both the reference's: body 6..18 x 11..20, shackle
       centreline radius 3.5. Open is the SAME shackle with its right leg cut
       short and the whole thing lifted - a structural difference, not a 2-unit
       nudge. Neither carries a keyhole; the shackle is the message."""
    def f(u):
        x, y, w, h = 6.0, 11.0, 12.0, 9.0
        body = rrect(x, y, w, h, min(e_cl(), 3.0))
        r, cy = 3.5, (7.0 if not open_ else 5.8)
        foot = y + W / 2                       # legs tuck under the body wall
        sh = ('M%s L%s A%g %g 0 0 1 %s L%s'
              % (f2((C - r, foot)), f2((C - r, cy)), r, r, f2((C + r, cy)),
                 f2((C + r, cy + 2.4 if open_ else foot))))
        return ink(sh) + ink(body)
    return f

def eye(off=False):
    def f(u):
        lid = ('M2.6 12C5.0 8.0 8.2 6.0 12 6.0C15.8 6.0 19.0 8.0 21.4 12'
               'C19.0 16.0 15.8 18.0 12 18.0C8.2 18.0 5.0 16.0 2.6 12Z')
        pupil = ring(12, 12, 3.2)
        out = ink(lid) + pupil
        if off:
            # A 45 slash enters the dome ~3.5 along the arc from its end, so a
            # full moat leaves a floating stub. The off-slash therefore takes a
            # half moat: enough to read as a break, not enough to orphan.
            slash = bar((4.4, 19.6), (19.6, 4.4))
            return knockout(u, out, slash, W + moat()) + ink(slash)
        return out
    return f

def refresh():
    """Two half-turns, rotationally symmetric, each ending in the same inscribed
       barb history uses. Because both barbs come out of one primitive they sit
       at identical angles to their own arcs, which is what makes the pair read
       as even — the old version laid a tiny open head on the raw tangent and
       the two ends looked mismatched."""
    def f(u):
        run = run_open()
        r = ring_r(7.4, run)
        brk = (gap() + W / 2) / r
        out = ''
        for base in (0.0, math.pi):
            a_t = base + math.pi                         # travel: increasing th
            out += ink(arc(C, C, r, base + brk, a_t))
            out += ring_head(r, a_t, run, ccw=False)
        return out
    return f

# ---- location / money ----------------------------------------------------
def location(fill=False):
    """The map marker: a circle and an apex joined by their common tangents, so
       the shoulder is tangent-continuous at any radius rather than a drawn
       curve.

       Named `location`, not `pin`. It answers "where", and the reference set
       calls its own version location-pin-enabled-line. `pin` is the verb - see
       below - and one name cannot carry both."""
    def f(u):
        r, cy, ay = 6.2, 10.2, 20.6
        dy = ay - cy
        tx = r * r / dy
        ty = r * math.sqrt(dy * dy - r * r) / dy
        d = 'M%sA%g %g 0 1 1 %sL%sZ' % (f2((C - ty, cy + tx)), r, r,
                                        f2((C + ty, cy + tx)), f2((C, ay)))
        if fill:
            return solidify(d)
        return ink(d) + dot(C, cy, r - W - gapm())
    return f

# A push pin, and everything about it is chosen to not be the map marker.
#
#   location  balloon head, hole in the middle, tapering to a point  -> a place
#   pin       flat wide cap, no hole, a solid needle below it        -> an act
#
# The two silhouettes share nothing: one is a teardrop, the other a T. That is
# the whole design brief, because they sit next to each other in a set and a
# reader has to tell them apart at 16px without reading a label.
PIN_TILT  = 34.0        # degrees the whole tack leans, clockwise
PIN_CAP_R = 1.5 * W     # cap radius. Interior on the flip to fill is R - W/2
                        # = W, clear of the gapm floor (0.75 W) with room to
                        # spare, which is what makes the cap read as hollow
                        # rather than as a filled disc wearing a thin ring.
PIN_SHAFT = 5.0 * W     # cap wall to tip, along the axis
PIN_POINT = 2.0 * W     # ... of which the last stretch is the taper


def pin(fill=False):
    """A tack, leaning.

       Upright, this read as a lollipop and its needle came to a 7-degree spike -
       a printing fault rather than a point. Both problems are the same problem:
       a pin is a thing at an angle, stuck into something, and drawing it square
       to the grid makes it look like a diagram of a pin.

       So it leans, and the needle is a shaft with a point on the end rather than
       one long triangle: the taper runs only the last third of it, which puts
       the tip at a real angle instead of a printing-fault spike.

       Three failed passes on the way here. Upright and square to the grid it
       read as a diagram of a pin rather than a pin. Tilted, with a capsule for
       the cap, the capsule's own arc math bulged inward at this length-to-
       radius ratio and crossed itself into a bowtie. And the shaft, rounded on
       CP_BOX - the superellipse profile `rrect` uses, built for a box's four
       right angles - over-rounded the shoulders of a wedge this acute until
       they ballooned past the outline. The cap is a plain ring now: a round
       head reads as a tack just as well as a capsule does, without carrying
       capsule's orientation math, and CP_TIP is the arrowhead profile for a
       reason - it is built for exactly this, a point flanked by two shoulders.

       The two pieces are emitted as SEPARATE paths on purpose. Combined into one
       filled path they wind against each other, and the overlap where the shaft
       enters the pad knocks itself out - a stray counter with no clearance
       reason to exist. Separate paths cannot interact, whatever their winding."""
    th = math.radians(PIN_TILT)
    d = (math.sin(th), math.cos(th))                 # axis: down and to the right
    p = (-d[1], d[0])
    def f(u):
        hw = 0.5 * W                                 # shaft half-width, 1.0 @ 2
        back = PIN_CAP_R + W / 2                     # ink behind the cap centre
        span = back + PIN_CAP_R + PIN_SHAFT
        # sit the whole figure on the canvas centre, along its own axis
        k = span / 2 - back
        H = (C - k * d[0], C - k * d[1])             # cap centre
        B = (H[0] + PIN_CAP_R * d[0], H[1] + PIN_CAP_R * d[1])   # far cap wall
        def at(s, t): return (B[0] + s * d[0] + t * p[0],
                              B[1] + s * d[1] + t * p[1])
        shaft = ngon([at(0, hw), at(PIN_SHAFT - PIN_POINT, hw),
                      at(PIN_SHAFT, 0),
                      at(PIN_SHAFT - PIN_POINT, -hw), at(0, -hw)],
                     e_tip(), CP_TIP)
        # the shaft is solid in BOTH variants, so the pair differ only in
        # whether the cap is hollow - and the fill lands on exactly the line's
        # outer edge, same as every other pair in the set
        head = dot(H[0], H[1], PIN_CAP_R) if fill else ring(H[0], H[1], PIN_CAP_R)
        return head + solid(shaft)
    return f


def navigation():
    return lambda u: ink(ngon([(20.0, 4.0), (4.4, 10.4), (11.2, 12.8),
                               (13.6, 19.6)], 1.3))

def money(fill=False):
    x, y, w, h = 3.0, 6.5, 18.0, 11.0
    def f(u):
        r = 2.6
        if fill:
            out = rrect_out(x, y, w, h)
            return ('<mask id="k%s" maskUnits="userSpaceOnUse">'
                    '<path d="%s" fill="#fff"/><circle cx="12" cy="12" r="%g" '
                    'fill="#000"/></mask><path d="%s" fill="currentColor" '
                    'mask="url(#k%s)"/>' % (u, out, r + moat(), out, u))
        return ink(rrect(x, y, w, h, min(e_cl(), 3.0))) + ring(C, C, r)
    return f

def price(fill=False):
    def f(u):
        e = 2.4
        p = ('M' + f2((11.4, 3.4)) + 'L' + f2((20.6 - e, 3.4))
             + corner((20.6, 3.4), (1, 0), (0, 1), e, CP_BOX)
             + 'L' + f2((20.6, 12.6)) + 'L' + f2((12.2, 21.0))
             + 'L' + f2((3.0, 11.8)) + 'Z')
        hx, hy, hr = 16.9, 7.1, r_mark() + 0.3
        if fill:
            return ('<mask id="k%s" maskUnits="userSpaceOnUse">'
                    '<path d="%s" fill="#fff" stroke="#fff" stroke-width="%g" '
                    'stroke-linejoin="round"/><circle cx="%g" cy="%g" r="%g" '
                    'fill="#000"/></mask><g mask="url(#k%s)">%s</g>'
                    % (u, p, W, hx, hy, hr + moat() * 0.6, u, solidify(p)))
        return ink(p) + dot(hx, hy, hr)
    return f

# ============================================================================
# STUDY 15, PORTED ONTO THE AXIS
# ----------------------------------------------------------------------------
# cart, copy and photo were literal path data pinned at stroke 2. Everything
# that has to move with the weight here is a clearance, a moat or a repeat, and
# every one of them is now written as a multiple of W. The corner also changes:
# these were drawn on study 15's own superellipse (apex 0.2298) and are now on
# the library's CP_BOX (0.3228), so the whole set finally has ONE corner.
# ============================================================================
CART_CX, CART_CY = 19.5, 4.5             # badge centre

def bscale(): return W / 2.0             # the badge is a small icon on its own
                                         # grid, and that grid rides the stroke

def _badge_sym(sym):
    """The six badge marks, scaled about the badge centre by bscale()."""
    k = bscale(); X, Y = CART_CX, CART_CY
    def P(dx, dy): return (X + dx * k, Y + dy * k)
    if sym == 'add':
        return bar(P(-3.5, 0), P(3.5, 0)) + bar(P(0, -3.5), P(0, 3.5))
    if sym == 'check':
        return bar(P(-3.5, 0.35), P(-1.4, 2.47)) + 'L' + f2(P(3.5, -2.47))
    if sym == 'close':
        return bar(P(-2.6, -2.6), P(2.6, 2.6)) + bar(P(2.6, -2.6), P(-2.6, 2.6))
    if sym == 'alert':
        return bar(P(0, -2.9), P(0, -0.4))
    if sym == 'upload':
        return (bar(P(0, 2.3), P(0, -2.3))
                + 'M%sL%sL%s' % (f2(P(-2.9, -0.6)), f2(P(0, -3.5)), f2(P(2.9, -0.6))))
    return bar(P(-2.3, 0), P(2.3, 0))

def _badge(sym, u):
    """`remove` is a filled disc with the bar knocked out; the rest are ink."""
    k = bscale(); bw = 0.875 * W
    if sym == 'remove':
        ext = 1.75 * W + bw / 2
        return ('<mask id="b%s" maskUnits="userSpaceOnUse">'
                '<circle cx="%g" cy="%g" r="%g" fill="#fff"/>'
                '<path d="%s" fill="none" stroke="#000" stroke-width="%g" '
                'stroke-linecap="round"/></mask>'
                '<circle cx="%g" cy="%g" r="%g" fill="currentColor" '
                'mask="url(#b%s)"/>'
                % (u, CART_CX, CART_CY, ext, _badge_sym('remove'), bw,
                   CART_CX, CART_CY, ext, u))
    out = ink(_badge_sym(sym), w=bw)
    if sym == 'alert':
        out += dot(CART_CX, CART_CY + 2.8 * k, 0.5 * W)
    return out

def _badge_moat(sym):
    """What the badge takes out of what it sits on: its own ink plus badge()."""
    k = bscale(); bw = 0.875 * W
    if sym == 'remove':
        return '<circle cx="%g" cy="%g" r="%g" fill="#000"/>' % (
               CART_CX, CART_CY, 1.75 * W + bw / 2 + badge())
    out = ('<path d="%s" fill="none" stroke="#000" stroke-width="%g" '
           'stroke-linecap="round" stroke-linejoin="round"/>'
           % (_badge_sym(sym), bw + 2 * badge()))
    if sym == 'alert':
        out += '<circle cx="%g" cy="%g" r="%g" fill="#000"/>' % (
               CART_CX, CART_CY + 2.8 * k, 0.5 * W + badge())
    return out

def cart(sym=None, fill=False):
    """Handle, basket, two wheels. The wheels sit exactly gapm() under the
       handle's ink, which is what puts them at y 20.5 when W is 2."""
    def f(u):
        handle = 'M3 3.5H4.5L7.9 16.5H17.5'
        basket = 'M5.02 5.5H18.98L17.15 12.5H6.85'
        wy = 16.5 + W / 2 + gapm() + r_mark()
        wheels = dot(7.2, wy, r_mark()) + dot(16.8, wy, r_mark())
        body = ink(handle) + (solidify(basket + 'Z') if fill else ink(basket)) + wheels
        if sym is None:
            return body
        return ('<mask id="m%s" maskUnits="userSpaceOnUse"><rect width="24" '
                'height="24" fill="#fff"/>%s</mask><g mask="url(#m%s)">%s</g>%s'
                % (u, _badge_moat(sym), u, body, _badge(sym, u)))
    return f

# ---- twin cards ------------------------------------------------------------
def e_card(h): return round(0.29 * h, 2)   # extent is a fraction of the SHORT side

def _twin(front, back, fill, front_ink='', ko=''):
    """Back plate, front plate, and the moat the front takes out of the back:
       its own ink (W/2) plus the stroke<->stroke floor."""
    def f(u):
        if fill and ko:
            fr = ('<mask id="k%s" maskUnits="userSpaceOnUse"><path d="%s" '
                  'fill="#fff" stroke="#fff" stroke-width="%g" '
                  'stroke-linejoin="round"/>%s</mask>'
                  '<path d="%s" fill="currentColor" stroke="currentColor" '
                  'stroke-width="%g" stroke-linejoin="round" mask="url(#k%s)"/>'
                  % (u, front, W, ko, front, W, u))
        else:
            fr = ('<path d="%s" fill="%s" stroke="currentColor" stroke-width="%g" '
                  'stroke-linejoin="round"/>'
                  % (front, 'currentColor' if fill else 'none', W))
        return ('<mask id="m%s" maskUnits="userSpaceOnUse"><rect width="24" '
                'height="24" fill="#fff"/><path d="%s" fill="#000" stroke="#000" '
                'stroke-width="%g" stroke-linejoin="round"/></mask>'
                '<path d="%s" mask="url(#m%s)" fill="none" stroke="currentColor" '
                'stroke-width="%g" stroke-linejoin="round"/>%s%s'
                % (u, front, W + 2 * gap(), back, u, W, fr, front_ink))
    return f

def copy_icon(fill=False):
    e = e_card(14)
    return _twin(rrect(7, 3, 14, 14, e), rrect(3, 7, 14, 14, e), fill)

# ---- photo -----------------------------------------------------------------
def _interior(u, clip_path, rng, sun, colour, clip=True, w=None):
    w = W if w is None else w
    g = (('<clipPath id="cp%s"><path d="%s"/></clipPath>'
          '<g clip-path="url(#cp%s)">%s</g>'
          % (u, clip_path, u, ink(rng, c=colour, w=w))) if clip
         else ink(rng, c=colour, w=w))
    return g + '<circle cx="%g" cy="%g" r="%g" fill="%s"/>' % (
           sun[0], sun[1], sun[2], colour)

def photo(fill=False):
    e = e_card(14)
    box = rrect(3, 5, 18, 14, e)
    def f(u):
        inner = rrect(3 + W / 4, 5 + W / 4, 18 - W / 2, 14 - W / 2, e - W / 4)
        rng  = 'M2.26 13.09L7 9L12.5 14.09L14.5 12.5L20.7 18.19'
        rngf = 'M0.5 14.61L7 9L12.5 14.09L14.5 12.5L23 20.31'
        sun  = (16.5, 9.5, r_mark())
        sunf = (17.0, 9.0, r_mark() + W / 4)
        if not fill:
            return ('<path d="%s" fill="none" stroke="currentColor" '
                    'stroke-width="%g" stroke-linejoin="round"/>%s'
                    % (box, W, _interior(u, inner, rng, sun, 'currentColor')))
        return ('<mask id="k%s" maskUnits="userSpaceOnUse"><path d="%s" fill="#fff" '
                'stroke="#fff" stroke-width="%g" stroke-linejoin="round"/>%s</mask>'
                '<path d="%s" fill="currentColor" stroke="currentColor" '
                'stroke-width="%g" stroke-linejoin="round" mask="url(#k%s)"/>'
                % (u, box, W, _interior(u, inner, rngf, sunf, '#000', clip=False),
                   box, W, u))
    return f

def photo_stack(fill=False):
    e = e_card(10)
    front, back = rrect(7, 5, 14, 10, e), rrect(3, 9, 14, 10, e)
    dw = 0.875 * W          # interior detail steps one rung DOWN in a twin
    def f(u):
        inner = rrect(7 + W / 4, 5 + W / 4, 14 - W / 2, 10 - W / 2, e - W / 4)
        rng  = 'M5.6 11.6L10.25 8.2L14.35 11.3L15.6 10.5L21.6 15.15'
        rngf = 'M4.5 12.41L10.25 8.2L14.35 11.3L15.6 10.5L23 16.23'
        sun  = (17.75, 8.25, 0.525 * W)
        sunf = (18.20, 7.75, 0.55 * W)
        if fill:
            return _twin(front, back, True,
                         ko=_interior(u, inner, rngf, sunf, '#000', clip=False, w=dw))(u)
        return _twin(front, back, False,
                     front_ink=_interior(u, inner, rng, sun, 'currentColor', w=dw))(u)
    return f

def grid_masonry():
    """Masonry: one column merged, the other still in cells.

       The first attempt was two columns of two, the split in a different place
       on each side. That is geometrically masonry and optically useless - the
       box is 14 tall, the gap is at its floor, so the two cells can only be 6
       and 4, and 2 units of difference is invisible at 16px next to `grid`.
       The two sit in the same toggle group, so that is a failure.

       Cell COUNT carries what cell height cannot. The right column keeps grid's
       own cell - same 5-unit height - and the left column is one cell spanning
       the whole box. Same cells, one column merged, which is what a masonry
       column actually is."""
    def f(u):
        g = gap() + W                        # 4 @ 2 - grid's pitch, unchanged
        s = (14.0 - g) / 2                   # column width, 5 @ 2
        lo, hi = 5.0, 19.0
        cell = (hi - lo - g) / 2             # 5 @ 2 - grid's cell height exactly
        e = min(1.6, cell / 2)
        return ink(rrect(lo, lo, s, hi - lo, e),
                   rrect(hi - s, lo, s, cell, e),
                   rrect(hi - s, lo + cell + g, s, cell, e))
    return f

def grid_dense():
    """Nine cells where grid has four. At W = 2 a 3x3 of OUTLINED cells leaves a
       0-unit counter - the cell closes - so the dense grid is made of solid
       marks instead, the same move more-horizontal makes. Side 2W with a gap()
       between, which lands the outer ink on 4..20: grid's silhouette exactly."""
    def f(u):
        a = 2.0 * W                          # 4 @ 2
        p = a + gap()                        # pitch, 6 @ 2
        e = e_card(a)
        out = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                out.append(rrect(C + i * p - a / 2, C + j * p - a / 2, a, a, e))
        return solid(*out)
    return f

# ============================================================================
# REGISTRY
# ============================================================================
# ---- facilities pack ------------------------------------------------------
# A tent is a gable: an isosceles triangle standing on a ground datum, with a
# flap that is the same triangle scaled about the base midpoint. Everything
# here is derived from four numbers per tent (centre, ground, half-width,
# height) so the family stays one drawing at two scales.
#
# Corners go through ngon(), NOT as raw M-L-L-Z spikes — §4.2 puts every
# exterior corner on a radius and the set has no sharp-vertex allowance.
#
# The extent is warning's, scaled to the form. Solving e_for_r() for a literal
# r=2 was tried first and over-rounds: e = r/tan(th/2) blows up as the apex
# sharpens, and on a tent (half-angle 26deg vs warning's 28) it pulled the peak
# ~3 units below its own vertex — a decapitated tent, measurably rounder than
# the set's only shipped triangle. warning reads correctly at TRI_E over a
# 14-tall triangle, so that ratio is the family constant and every tent takes
# its extent from its own height. §3.2 step 6: ease the corner as the form
# shrinks, don't switch corner families.
TENT_EK = TRI_E / 14.0     # extent per unit of tent height (TRI_E = 2.9)
TENT_AR = 0.51585          # half-width : height, one aspect for the family.
                           # Solved, not styled: at this ratio the rounded
                           # silhouette's own bbox comes out square, which is
                           # what puts campsite on the 18x18 keyline (§2.2) with
                           # its ink filling the 20x20 live area exactly.

def ct_grow(): return 0.125 * W   # §6.2: a counter that flips positive ->
                                  # knockout grows +0.25 at 24 (= 0.125 W)

def _tent_pts(cx, by, hw, h):
    """Apex, base-right, base-left. Wound so ngon() sees a consistent turn."""
    return [(cx, by - h), (cx + hw, by), (cx - hw, by)]

def _tent(cx, by, hw, h):
    return ngon(_tent_pts(cx, by, hw, h), TENT_EK * h)

def flap_k(hw, h):
    """How far up the tent the door reaches, SOLVED from clearance rather than
       eyeballed off the draft.

       Scaling the door about the base midpoint keeps its legs parallel to the
       walls, so the wall-to-door gap is one constant for the whole run: the
       horizontal offset hw(1-k) laid perpendicular, less one stroke. Setting
       that to gap() and solving is what fixes the draft's 1.24 — legal under
       §7's absolute floor of 1, but under its default of 2, and the draft also
       closed the door's base straight along the tent's own base so the two
       strokes were drawn on top of each other (measured clearance: 0.00)."""
    return 1.0 - 2.0 * W * math.hypot(hw, h) / (hw * h)

def _flap(cx, by, hw, h):
    """The door as an open run, not a closed triangle: up one leg, over the
       apex, down the other. §4.1 — butt where a stroke terminates against
       another form, which is what both feet do on the tent's own base."""
    k = flap_k(hw, h)
    return 'M%sL%sL%s' % (f2((cx - hw * k, by)), f2((cx, by - h * k)),
                          f2((cx + hw * k, by)))

def _flap_hole(cx, by, hw, h):
    """The same door as an area, for the knockout. Its base runs W/2 PAST the
       ground so the opening punches through the solidified tent's bottom edge
       instead of leaving a sliver of ink under the door — home's fill does the
       same thing with its own doorway."""
    k = flap_k(hw, h)
    foot = by + W / 2
    return ngon([(cx, by - h * k), (cx + hw * k, foot), (cx - hw * k, foot)],
                TENT_EK * h * k)

def hole_mask(u, hole, grow, key='h'):
    """Cut `hole` out of the wrapped body as an AREA, grown `grow` on every side.

       This is §5.2a — solid body, glyph reused verbatim as a knockout — plus
       §6.2's counter compensation, applied by stroking the mask path rather
       than redrawing it at a second size. Distinct from knockout(), which
       strokes a path it does NOT fill and so cuts a groove; a groove is right
       for eye's off-slash and wrong for a doorway."""
    return ('<mask id="%s%s" maskUnits="userSpaceOnUse"><rect width="24" '
            'height="24" fill="#fff"/><path d="%s" fill="#000" stroke="#000" '
            'stroke-width="%g" stroke-linejoin="round"/></mask>'
            % (key, u, hole, grow * 2))

def _masked(u, body, key='h'):
    return '<g mask="url(#%s%s)">%s</g>' % (key, u, body)

CAMPSITE = (12.0, 21.0, 10.1369, 19.6508)   # cx, ground y, half-width, height
                                            # -> path bbox 18x18 at 3..21, ink
                                            # 2..22 on both axes

def campsite(fill=False):
    """One tent, alone, on a ground line: a specific, reservable site.

       Fill is the §5.2a boolean, not a redraw: solidify() puts the mass at the
       line variant's own outer edge (fill + stroke at W is exactly that offset,
       so the footprint is identical per §5.1), and the door is knocked out as
       the same geometry, grown by ct_grow()."""
    def f(u):
        cx, by, hw, h = CAMPSITE
        tent = _tent(cx, by, hw, h)
        if fill:
            return (hole_mask(u, _flap_hole(cx, by, hw, h), ct_grow())
                    + _masked(u, solidify(tent)))
        return ink(tent) + ink(_flap(cx, by, hw, h), cap='butt')
    return f

# The whole facility rather than one site. The draft carried a single bare
# diagonal here, which is the one thing the review explicitly ruled out: a bare
# stroke has no peak of its own, so it reads as a stray line rather than as
# another tent — and its free upper end could not take a round cap without
# looking like a dropped match, while its lower end had to be butt to sit on
# the ground. Two ends, two rules, one path: that is the tell that it was the
# wrong primitive.
#
# The second tent stands BEHIND the first rather than beside it. Side by side,
# the live area only leaves room for a nub: holding gap() at the ground between
# two full tents caps the far one at ~4 units wide, and the near one has to
# narrow so far that its own door falls under the clearance floor. Overlapping
# with a moat is the set's existing answer to exactly this (photo-stack's
# plates, people's heads), so the far tent is occluded by the near one's
# silhouette dilated by moat().
#
# The pair is fitted as one object: two tents plus a moat cannot also be 18
# tall inside a 20-unit live area, so campground lands the 18 on width and
# takes the shorter axis — the same one-axis conformance warning ships with.
# The tents keep TENT_AR, so they read as campsite redrawn smaller rather than
# campsite scaled (§3).
CAMPGROUND = ((9.1910, 21.0, 6.9733, 13.5180),    # near
              (16.5299, 21.0, 5.0305, 9.7519))    # far, peak clear of the wall

def campground(fill=False):
    """Near tent with its door, far tent behind it, no door.

       The far tent drops the door rather than shrinking it: §3.2 step 4 says
       reduce detail within the vocabulary when clearance runs out, and at that
       scale flap_k() solves negative — there is no door that clears."""
    def f(u):
        (nx, ny, nhw, nh), (fx, fy, fhw, fh) = CAMPGROUND
        near = _tent(nx, ny, nhw, nh)
        far  = _tent(fx, fy, fhw, fh)
        # the near tent's own silhouette, plus a crossing moat, cut out of the
        # far one — so the far tent reads as passing behind, not through
        occl = (hole_mask(u, near, W / 2 + moat(), key='o')
                + _masked(u, ink(far), key='o'))
        if fill:
            return (occl + hole_mask(u, _flap_hole(nx, ny, nhw, nh), ct_grow())
                    + _masked(u, solidify(near)))
        return occl + ink(near) + ink(_flap(nx, ny, nhw, nh), cap='butt')
    return f

# ev-charger — recommendation A from the facilities-pack review. The body is
# fuel's own tank silhouette verbatim (so "is this a pump" is true by
# construction, not by eye), the bolt is the standalone bolt path at half
# scale centred on the tank, and the cable ends in a straight two-prong plug —
# the NPS electrical-hookup symbol's prong pair, not a bent gas nozzle.
_TANK      = 'M4.6 20.5V6.6C4.6 5.5 5.5 4.6 6.6 4.6H11.6C12.7 4.6 13.6 5.5 13.6 6.6V20.5'
_TANK_BASE = ((2.9, 20.5), (15.3, 20.5))
_BOLT      = 'M10.1 7.85L5.9 13.35H8.8L8.1 17.25L12.3 11.75H9.4Z'
_CABLE     = 'M13.6 15.4H18.4C19.17 15.4 19.8 14.77 19.8 14V9.8'
_PLUG      = (17.8, 6.4, 3.8, 3.4)                        # housing x, y, w, h
_PRONGS    = (((18.2, 4.0), (1.0, 2.4)), ((20.2, 4.0), (1.0, 2.4)))

def _rect_path(x, y, w, h):
    return 'M%sH%gV%gH%gZ' % (f2((x, y)), x + w, y + h, x)

# fuel and ev-charger are the same machine — same tank, same plinth, same arm
# geometry. What differs is the mark on the face and what the arm ends in, which
# is exactly the difference between the two things in the world. Sharing the
# body makes "is this the same kind of object" true by construction.
_TANK_CLOSED = _TANK + 'Z'
_HOSE  = 'M13.6 15.4H18.4C19.17 15.4 19.8 14.77 19.8 14V8.6H17.6'
_DROP  = (9.1, 14.2, 2.0, 8.8)     # cx, circle cy, r, apex y — sized so its ink
                                   # clears the tank wall by gapm() on both sides

def _pump(u, mark, arm, fill):
    """Pump body, a mark on its face, an arm. On the flip the mark goes from ink
       to knockout and grows by ct_grow() (§6.2); the plinth stays ink in both,
       since it is a separate form the mark never touches."""
    if fill:
        return (ink(bar(*_TANK_BASE), cap='butt')
                + hole_mask(u, mark, ct_grow())
                + _masked(u, solidify(_TANK_CLOSED)) + arm)
    return ink(_TANK, bar(*_TANK_BASE), cap='butt') + solid(mark) + arm

def _plug_arm():
    x, y, w, h = _PLUG
    out = ink(_CABLE, cap='butt') + ink(rrect(x, y, w, h, 1.0))
    for (px, py), (pw, ph) in _PRONGS:
        out += solid(_rect_path(px, py, pw, ph))
    return out

def ev_charger(fill=False):
    return lambda u: _pump(u, _BOLT, _plug_arm(), fill)

def fuel(fill=False):
    """The same pump, dispensing a liquid. The droplet is water's own primitive
       at mark scale, so `water`, `fuel` and `location` all come off one curve."""
    cx, cy, r, ay = _DROP
    return lambda u: _pump(u, droplet(cx, cy, r, ay), ink(_HOSE), fill)

# ---- facilities -----------------------------------------------------------
# restroom-figures. Two figures, equal, apart — NOT people's overlapping pair.
# The scale is forced rather than chosen: two figures plus gap() inside the live
# area is 4*half + 6 = 20, so half is 3.5 and s is 0.5 exactly. That puts the
# head ring's counter at Ø2 — on the §7 floor, not under it, but it is the first
# thing that will need reworking when the 16px master is drawn.
RESTROOM_S  = 0.5
RESTROOM_DX = 5.5
RESTROOM_HY = 7.0
RESTROOM_BASE = 20.5

def restroom_figures(fill=False):
    def f(u):
        out = ''
        for cx in (C - RESTROOM_DX, C + RESTROOM_DX):
            (x, hy, rh), body, _ = _person(s=RESTROOM_S, cx=cx, hy=RESTROOM_HY,
                                           base=RESTROOM_BASE)
            out += _head_ring(x, hy, rh, fill) + _body_paint(body, fill)
        return out
    return f

# ---- map chrome -----------------------------------------------------------
# None of these takes a fill. Map chrome is always a button, never a marker, so
# there is no selected state for the line/fill flip to carry (§9: the flip is a
# STATE signal, not decoration).

def e_apex(h):
    """The set's apex extent for a form h tall. warning's triangle is the only
       shipped precedent for a sharp vertex and TENT_EK is its ratio; anything
       else with a point takes the same reach scaled to its own size."""
    return TENT_EK * h

def ngon_r(pts, r, cp=CP_BOX):
    """ngon() driven by the §4.2 corner RADIUS rather than by a tangent length.
       A polygon whose vertices are not all the same angle needs a different
       extent at each one to land on a single radius — see e_for_r()."""
    es = []
    n = len(pts)
    for i in range(n):
        A, V, B = pts[(i - 1) % n], pts[i], pts[(i + 1) % n]
        din  = unit((V[0] - A[0], V[1] - A[1]))
        dout = unit((B[0] - V[0], B[1] - V[1]))
        es.append(e_for_r(r, din, dout))
    return ngon(pts, es, cp)

def _vee(cx, by, hw, hh, r=2.0):
    """The lower half of a plate: down one edge, round the bottom on the same
       radius a closed plate would use, up the other. Open run, so the two outer
       ends are free and take round caps."""
    A, V, B = (cx - hw, by - hh), (cx, by), (cx + hw, by - hh)
    din  = unit((V[0] - A[0], V[1] - A[1]))
    dout = unit((B[0] - V[0], B[1] - V[1]))
    return ('M%s%sL%s'
            % (f2(A), corner(V, din, dout, e_for_r(r, din, dout), CP_BOX), f2(B)))

MAP_X  = (3.0, 9.0, 15.0, 21.0)     # three panels, 6 wide, on the 18 keyline
MAP_Y  = (7.0, 3.0, 7.0, 3.0)       # the fold heights along the top edge
MAP_H  = 14.0                       # panel height; 3..21 on both axes

def map_icon():
    """Three folded panels.

       The zigzag runs IN PHASE top and bottom, which makes every panel a
       parallelogram of one size. Out of phase they become trapezoids of
       different areas, i.e. a map drawn in perspective — and this set has no
       axonometric forms (see folder-open, which was flattened for exactly this
       reason).

       The two creases are butt-capped: each terminates against the outline
       (§4.1), and a crease is a fold, not a second object, so it takes no moat."""
    def f(u):
        top = list(zip(MAP_X, MAP_Y))
        bot = [(x, y + MAP_H) for x, y in reversed(top)]
        creases = [bar((x, y), (x, y + MAP_H)) for x, y in top[1:3]]
        return ink(ngon_r(top + bot, 2.0)) + ink(*creases, cap='butt')
    return f

LAYER_HW, LAYER_HH = 9.0, 3.5       # plate half-width, half-height
LAYER_PITCH = 5.0                   # plate pitch, NOT gap(): these edges are
                                    # raked, so a vertical pitch p only buys
                                    # p*cos(th) of perpendicular air. At this
                                    # rake that is 4.66, i.e. gap() + W with
                                    # 0.66 to spare, and a vertical pitch of 4
                                    # would land at 1.66 — under the floor.

def layers():
    """One whole plate and two more seen edge-on beneath it. Only the top plate
       closes: the ones below are occluded by definition, so drawing them closed
       would be drawing what the stack hides."""
    def f(u):
        top, cy = 3.5, 3.5 + LAYER_HH
        plate = ngon_r([(C, top), (C + LAYER_HW, cy),
                        (C, top + 2 * LAYER_HH), (C - LAYER_HW, cy)], 2.0)
        out = ink(plate)
        for i in (1, 2):
            by = top + 2 * LAYER_HH + i * LAYER_PITCH
            out += ink(_vee(C, by, LAYER_HW, LAYER_HH))
        return out
    return f

ROUTE_R  = 3.5      # U-turn radius. Sets the run pitch at 2R = 7, so two runs
                    # clear by 5, and it is the largest radius that still leaves
                    # the terminal marks inside the live area.
ROUTE_M  = 2.0      # terminal mark radius (a mark, so r_mark()-class, not a ring:
                    # a ring this small has a 2-unit counter, exactly on the §7
                    # floor, and it is the first thing to clog at 16px)

def route():
    """Origin, destination, and a switchback between them.

       Two U-turns rather than one S-bend: one bend reads as a river, two read as
       a route that had to go around something. The marks are solid dots held off
       the path by gapm() — they are marks on a line, not junctions in it."""
    def f(u):
        r = ROUTE_R
        y0, y1, y2 = C + 2 * r, C, C - 2 * r           # 19, 12, 5
        ax, bx = 15.0, 9.0                             # the two U-turn axes
        a, b = (5.0, y0), (19.0, y2)                   # the two marks
        off = ROUTE_M + gapm()                         # mark ink -> path ink; the
                                                       # run's end is butt, so it
                                                       # adds nothing of its own
        p = ('M%sL%s' % (f2((a[0] + off, y0)), f2((ax, y0)))
             + 'A%g %g 0 0 0 %s' % (r, r, f2((ax, y1)))
             + 'L%s' % f2((bx, y1))
             + 'A%g %g 0 0 1 %s' % (r, r, f2((bx, y2)))
             + 'L%s' % f2((b[0] - off, y2)))
        return (ink(p, cap='butt')
                + dot(a[0], a[1], ROUTE_M) + dot(b[0], b[1], ROUTE_M))
    return f

NEEDLE = (6.8, 3.0)     # needle half-length, waist half-width. The apex extent
                        # eats ~0.85 off each point, so the drawn tip lands at
                        # ~6.0 and its ink clears the ring's inner edge by ~1 —
                        # §8.3's contained-glyph clearance.

def compass():
    """A ring and a needle. The needle's long points take the apex extent (they
       are the same 53-degree vertex a tent's peak is), the waist takes the plain
       exterior r=2 — one flat extent on a rhombus this elongated rounds the
       waist to r=5 and the thing stops being a needle."""
    def f(u):
        rn, rw = NEEDLE
        k = math.sqrt(0.5)
        pts = [(C + rn * k, C - rn * k), (C + rw * k, C + rw * k),
               (C - rn * k, C + rn * k), (C - rw * k, C - rw * k)]
        ea = e_apex(2 * rn)
        din, dout = unit((-1, 1)), unit((-1, -1))      # at the SE waist vertex
        ew = e_for_r(2.0, din, dout)
        return ring(C, C, 9.0) + ink(ngon(pts, [ea, ew, ea, ew]))
    return f

# ---- data & status --------------------------------------------------------
def circle_icon(fill=False):
    """The bare status dot the set never had. Ring on the Ø20 circle keyline;
       the fill is the §5.2b figure rule — a solid mass at outer - 0.5 — because
       there is nothing inside it to knock out."""
    r = 9.0
    def f(u):
        return dot(C, C, r + W / 2 - 0.5) if fill else ring(C, C, r)
    return f

BAR_BASE = 20.0                     # shared baseline, skeleton
BAR_MAX  = 16.0                     # tallest bar: ink 3..21
BAR_N    = 5                        # five columns at pitch W+gap() lands the ink
                                    # on 3..21 too, so the block is the 18x18
                                    # square keyline with integer anchors and a
                                    # gap of exactly gap(). pitch_bar()'s 5.0 is
                                    # the DOT row's pitch (more-*) and gives 17.

def bars(heights, base=BAR_BASE, pitch=None):
    """n bars on a shared baseline. Round caps at both ends: there is no drawn
       axis for the feet to terminate against, so both ends are free (§4.1)."""
    pitch = W + gap() if pitch is None else pitch
    x0 = C - (len(heights) - 1) * pitch / 2.0
    return [bar((x0 + i * pitch, base), (x0 + i * pitch, base - h))
            for i, h in enumerate(heights)]

CHART_H = (7.0, 13.0, BAR_MAX, 8.0, 11.0)      # busy-times: rises, peaks, falls

def chart():
    """Five columns, non-monotonic. The profile is the only thing separating this
       from `signal` — same block, same pitch, same footprint — so it has to fall
       at least once or the two icons are one icon."""
    return lambda u: ink(*bars(list(CHART_H)))

def signal():
    """Five bars, even steps: BAR_MAX * i/n, so the ramp is linear rather than
       eyeballed and the shortest bar is a fifth of the tallest."""
    hs = [BAR_MAX * (i + 1) / float(BAR_N) for i in range(BAR_N)]
    return lambda u: ink(*bars(hs))

def activity():
    """The route polyline flattened onto a baseline: a level run, one spike, a
       level run. Occupancy over time, not a value per category — which is why
       it is a continuous line and `chart` is discrete columns.

       Ink lands on 20 x 16: the horizontal-rect keyline, which is the one that
       fits a form with a dominant axis (§2.2)."""
    def f(u):
        y, lo, hi = C, 19.0, 5.0
        return ink('M%sL%sL%sL%sL%sL%s'
                   % (f2((3.0, y)), f2((7.5, y)), f2((10.5, hi)),
                      f2((13.5, lo)), f2((16.5, y)), f2((21.0, y))))
    return f

# ---- POI primitives -------------------------------------------------------
# bolt. Point-symmetric about the canvas centre, six vertices: two tips, two
# extremes, two shelf returns. Every published bolt is this figure; what is
# NOT published is a waist wide enough to survive being outlined at W, which is
# why the shelf returns sit further out here than the usual drawing puts them.
BOLT_A = (3.0, 9.5)     # tip, offset from centre (dx, -dy)
BOLT_E = (7.5, 2.0)     # extreme. Both sit half a unit proud of the keyline:
                        # the corner profile eats ~0.5 off every vertex, so the
                        # DRAWN figure lands on 16 x 20 — the vertical rect.
BOLT_W = 4.0            # waist: the perpendicular distance from the shelf
                        # return to the opposite long edge. Outlined at W that
                        # leaves gap() of counter, which is the whole reason it
                        # is solved rather than drawn.
BOLT_E_K = 1.3          # flat extent, navigation's — the tips are 35 degrees,
                        # far sharper than warning's 54, so e_apex() over-reaches
                        # and a uniform RADIUS would take 2.4 off each point.

def _bolt_pts():
    ax, ay = BOLT_A
    ex, ey = BOLT_E
    A  = (C + ax, C - ay)
    E  = (C + ex, C - ey)
    Ep = (C - ex, C + ey)
    # solve the shelf return's x so the waist lands on BOLT_W
    d  = unit((Ep[0] - A[0], Ep[1] - A[1]))
    n  = (-d[1], d[0])
    # S sits on the shelf, i.e. at E's height; its distance from the A->E' edge
    # is (S - A).n, so sx follows directly — on whichever side of that edge the
    # body actually lies, which is the side E is on
    side = math.copysign(1.0, (E[0] - A[0]) * n[0] + (E[1] - A[1]) * n[1])
    sy = C - ey
    sx = A[0] + (side * BOLT_W - (sy - A[1]) * n[1]) / n[0]
    S  = (sx, sy)
    Sp = (2 * C - sx, 2 * C - sy)
    Ap = (2 * C - A[0], 2 * C - A[1])
    return [Ep, Sp, Ap, E, S, A]

def bolt(fill=False):
    """Charging speed, bare. Fill is the line silhouette flooded — identical
       footprint (§5.1), and what it spends its extra mass on is closing the
       waist counter, which is the only counter the figure has."""
    def f(u):
        p = ngon(_bolt_pts(), BOLT_E_K)
        return solidify(p) if fill else ink(p)
    return f

def droplet(cx, cy, r, ay):
    """A circle and an apex joined by their common tangents, so the shoulder is
       tangent-continuous at any radius rather than a drawn curve. location()'s
       construction, lifted — three copies of it existed inline.

       The apex may sit either side of the centre; the arc always wraps the far
       side, so the start point swaps with the sign."""
    dy = ay - cy
    tx = r * r / dy
    ty = r * math.sqrt(dy * dy - r * r) / abs(dy)
    L, R = (cx - ty, cy + tx), (cx + ty, cy + tx)
    P, Q = (L, R) if dy > 0 else (R, L)
    return 'M%sA%g %g 0 1 1 %sL%sZ' % (f2(P), r, r, f2(Q), f2((cx, ay)))

WATER = (6.2, 13.8, 3.4)     # r, circle centre y, apex y — location's droplet
                             # inverted: apex up, and no counter, so the two
                             # never share a silhouette

def water(fill=False):
    def f(u):
        r, cy, ay = WATER
        d = droplet(C, cy, r, ay)
        return solidify(d) if fill else ink(d)
    return f

def arcs(n, cx, cy, span, r0, pitch=None):
    """n concentric arcs struck from one origin, opening upward. Radial pitch is
       volume's wave pitch: W + gap(), i.e. the arcs clear each other by exactly
       the stroke floor."""
    pitch = W + gap() if pitch is None else pitch
    a = -math.pi / 2
    return ''.join(arc(cx, cy, r0 + i * pitch, a - span, a + span)
                   for i in range(n))

WIFI_O    = (12.0, 18.0)
WIFI_N    = 3
WIFI_SPAN = math.radians(44.0)

def wifi():
    """A device and three waves. The first radius is not chosen: it is the dot's
       own ink plus gap() plus a half stroke, the same solve volume makes for the
       air between its cone mouth and its first wave."""
    def f(u):
        cx, cy = WIFI_O
        rd = r_mark()
        return (dot(cx, cy, rd)
                + ink(arcs(WIFI_N, cx, cy, WIFI_SPAN, rd + gap() + W / 2)))
    return f

# parking. Square container, not circle: the NPS symbol has no container at all,
# a bare P, so the container here is doing typographic work — holding the letter
# off the label beside it — and a box is what a letter sits in.
PARK_STEM  = 9.5        # stem x. The bowl hangs right of it, so the figure is
                        # left-heavy and the whole letter shifts +0.5 to centre
                        # optically rather than metrically.
PARK_BOWL  = (7.5, 12.5, 2.5)    # arm y top, arm y bottom, bowl radius
PARK_FOOT  = 16.5

def _p_glyph(grow=0.0):
    """A capital P as a skeleton: stem, top arm, bowl, return.

       `grow` is §6.2/§6.3's knockout compensation. The bowl radius takes +0.25
       and the two arms move 0.25 apart each, which opens the counter by the
       +0.5 §6.3 measures on info-circle — applied to the glyph, never to W."""
    x = PARK_STEM
    y0, y1, r = PARK_BOWL
    y0 -= grow; y1 += grow; r += grow
    return ('M%sL%sL%sA%g %g 0 0 1 %sL%s'
            % (f2((x, PARK_FOOT)), f2((x, y0)), f2((C, y0)), r, r,
               f2((C, y1)), f2((x, y1))))

def parking(fill=False):
    def f(u):
        box, sol = rrect(4, 4, 16, 16), rrect_out(4, 4, 16, 16)
        if fill:
            return ('<mask id="k%s" maskUnits="userSpaceOnUse"><path d="%s" '
                    'fill="#fff"/>%s</mask><path d="%s" fill="currentColor" '
                    'mask="url(#k%s)"/>'
                    % (u, sol, ink(_p_glyph(ct_grow()), c='#000'), sol, u))
        return ink(box) + ink(_p_glyph())
    return f

# ---- landform -------------------------------------------------------------
# The live collision in this pack is `mountain` against `campground`: both are
# two triangles on a ground datum, and at 16px that is one icon. Three things
# separate them here, and all three are structural rather than stylistic:
#
#   1. ONE silhouette. campground is two tents with a moat cut between them, so
#      it reads as two objects; a range is a single closed outline with a saddle,
#      so it reads as one landform.
#   2. The horizontal-rect keyline (20 x 16) against campsite's square 18 x 18 —
#      a mountain is wider than it is tall, a tent is not.
#   3. A snow line. campsite's counter is a doorway at the BASE; mountain's is a
#      chevron near the PEAK. Different counter, different place, and it is the
#      first thing that survives at small size.

def _on_seg(P, Q, y):
    t = (y - P[1]) / float(Q[1] - P[1])
    return (P[0] + t * (Q[0] - P[0]), y)

def _extents(pts, apexes, base_y, r=2.0):
    """Per-vertex extents for a landform outline: a peak takes the apex reach
       scaled to its own height (warning's ratio), everything else takes the
       plain §4.2 exterior radius. One flat extent cannot serve both — at a
       55-degree peak r=2 needs a 3-unit tangent, and at a 67-degree foot it
       needs 3.03, but at the 108-degree saddle it needs 1.46."""
    es, n = [], len(pts)
    for i, V in enumerate(pts):
        A, B = pts[(i - 1) % n], pts[(i + 1) % n]
        din  = unit((V[0] - A[0], V[1] - A[1]))
        dout = unit((B[0] - V[0], B[1] - V[1]))
        es.append(e_apex(base_y - V[1]) if i in apexes else e_for_r(r, din, dout))
    return es

# Anchors sit proud of the target on every side, because the corner profile eats
# a different amount at each vertex — 0.75 at the west foot, 0.54 at the east
# (the slopes differ), 1.29 at the peak. Solved against the drawn result, which
# is the only thing a keyline can be measured on.
MOUNT_PTS = [(2.25, 21.0), (9.32, 5.7), (15.5, 15.5), (18.5, 11.0), (21.54, 21.0)]
MOUNT_BASE = 21.0            # the ground datum campsite also sits on
MOUNT_SNOW = (12.0, 1.0)     # snow-line height, and how far its middle dips
# The saddle sits deep — 9.8 below the main peak — and that is what makes the
# snow line possible at all. A shallow saddle crowds the main peak from below,
# and the snow line then has to ride so high that the counter left above it is a
# 2 x 1.9 sliver with an inradius of 0.55: a clogged aperture, and the §7 floor
# is 1.0. Dropping the saddle lengthens the main peak's right slope, which lets
# the snow line sit at 12 with 1.12 of inradius above it and 4.18 of clearance
# from its dip to the saddle. A deep saddle also reads less like two tents on a
# shared ground line, which is the collision this icon has to win.

def mountain(fill=False):
    """A range: two peaks, one outline, a snow line on the main peak.

       The snow line terminates ON the two slopes with butt caps — it is a
       boundary drawn across a mass, not a second object, so it takes no
       clearance from the walls it meets (§4.1). In the fill it becomes a crease
       of exactly W: a negative line inside a solid is the same width as the
       stroke it replaces, and it is the only counter the figure has to spend
       its extra mass on (§5.3)."""
    def f(u):
        pts = MOUNT_PTS
        y, dip = MOUNT_SNOW
        L = _on_seg(pts[0], pts[1], y)          # up the left slope
        R = _on_seg(pts[1], pts[2], y)          # down into the saddle
        snow = 'M%sL%sL%s' % (f2(L), f2(((L[0] + R[0]) / 2, y + dip)), f2(R))
        body = ngon(pts, _extents(pts, {1, 3}, MOUNT_BASE))
        if fill:
            return knockout(u, solidify(body), snow, crease(), cap='butt')
        return ink(body) + ink(snow, cap='butt')
    return f

# park. The proposal drew this as a notched gable + trunk, i.e. a conifer, and
# that does not survive being outlined: two tiers put the underside of the upper
# slope 2.29 from the lower one, so the step closes at W (§3.2 step 4 — reduce
# the count, and one tier of a conifer is just campsite wearing a trunk). A
# broadleaf canopy is one arc, has no step to close, and settles the proposal's
# own open question 3 — park against mountain at 16px — by not being a triangle.
PARK_TREE = (10.0, 7.0, 2.0, 21.0)      # canopy centre y, canopy r, trunk half-width, foot y

def park(fill=False):
    """Canopy and trunk as ONE silhouette: the trunk's sides are chords of the
       canopy, so the two meet tangentially rather than crossing."""
    def f(u):
        cy, r, tw, fy = PARK_TREE
        ty = cy + math.sqrt(r * r - tw * tw)     # where the trunk leaves the arc
        Rt, Lt = (C + tw, ty), (C - tw, ty)
        d = ('M%sA%g %g 0 1 0 %sL%sL%sZ'
             % (f2(Rt), r, r, f2(Lt), f2((C - tw, fy)), f2((C + tw, fy))))
        return solidify(d) if fill else ink(d)
    return f

# picnic-table. Line only, and that is a construction fact rather than an
# omission: the figure is four bars, so it has no interior to flood. solidify()
# on an open run returns the run, which would ship a fill variant identical to
# its line variant — the exact bug Appendix A flags on dock-right-fill. If the
# app needs a selected state here it belongs on the chip, not the glyph.
PICNIC_TOP  = 6.5
PICNIC_FOOT = 20.5
PICNIC_BENCH = 14.0
PICNIC_LEG = ((7.5, 4.0), (16.5, 20.0))   # (top x, foot x) per leg

def picnic_table():
    def f(u):
        (ltx, lfx), (rtx, rfx) = PICNIC_LEG
        legs = [bar((ltx, PICNIC_TOP), (lfx, PICNIC_FOOT)),
                bar((rtx, PICNIC_TOP), (rfx, PICNIC_FOOT))]
        return ink(bar((3.0, PICNIC_TOP), (21.0, PICNIC_TOP)),
                   bar((5.0, PICNIC_BENCH), (19.0, PICNIC_BENCH)), *legs)
    return f

# ---- vehicles -------------------------------------------------------------
# One chassis for the three of them, so they read as a family and differ only
# where the vehicles actually differ. Wheels are cart's, not new: solid marks of
# r_mark() sitting gapm() under the body's ink, which is the datum that already
# puts cart's wheels at 20.5 when W is 2.
#
# Every one of them takes the same fill counter — a belt line, drawn as ink in
# the line variant and cut as a crease() groove in the fill. That is file's
# dog-ear treatment, and it is the only counter a vehicle silhouette has that is
# not a window; a window does not fit. The coach interior is 9 units tall, a
# window needs gap() above and below, and what is left is 5 of ink for a 3-unit
# opening — under the floor before it is drawn.
CHASSIS_FLOOR = 16.5

def wheel_y(): return CHASSIS_FLOOR + W / 2 + gapm() + r_mark()   # 20.5 @ 2

def wheels(*xs):
    return ''.join(dot(x, wheel_y(), r_mark()) for x in xs)

def _vehicle(u, pts, belt, axles, fill):
    body = ngon_r(pts, 2.0)
    if fill:
        return (knockout(u, solidify(body), belt, crease(), cap='butt')
                + wheels(*axles))
    return ink(body) + ink(belt, cap='butt') + wheels(*axles)

CAR_PTS = [(3.0, 16.5), (3.0, 12.5), (7.5, 12.5), (10.0, 8.0),
           (15.0, 8.0), (17.5, 12.5), (21.0, 12.5), (21.0, 16.5)]
CAR_BELT = ((7.5, 12.5), (17.5, 12.5))
CAR_AXLES = (7.5, 16.5)

def car(fill=False):
    """Body and cabin as one silhouette, split by the belt line. Two counters,
       both at gap() + 0.5: the cabin 8..12.5 and the body 12.5..16.5."""
    def f(u):
        return _vehicle(u, CAR_PTS, bar(*CAR_BELT), CAR_AXLES, fill)
    return f

# The step over the cab is the whole icon: without it this is a bus. The recess
# it leaves — bunk underside to hood — is held at 4 so the outline clears itself
# by gap() through the notch; at NPS's proportions it comes out 2.5 and closes.
RV_PTS = [(3.0, 16.5), (3.0, 5.5), (20.0, 5.5), (20.0, 8.5),
          (17.0, 8.5), (17.0, 12.5), (21.0, 12.5), (21.0, 16.5)]
RV_BELT = ((3.0, 12.5), (17.0, 12.5))
RV_AXLES = (7.0, 18.0)

def rv(fill=False):
    def f(u):
        return _vehicle(u, RV_PTS, bar(*RV_BELT), RV_AXLES, fill)
    return f

# trailer. The proposal wanted the tow vehicle drawn too, on the grounds that a
# trailer without one is just a box. It is the TONGUE that says trailer, not the
# tow vehicle — and two vehicles inside 20 units gives each about 8, at which
# point neither is legible. The tongue leaves the bottom-front corner rather
# than the wall above it, so there is no closing wedge between the two.
TRAILER_PTS = [(6.5, 16.5), (6.5, 9.0), (8.5, 7.0), (21.0, 7.0), (21.0, 16.5)]
TRAILER_BELT = ((6.5, 12.0), (21.0, 12.0))
TRAILER_TONGUE = ((6.5, 16.5), (3.0, 14.5))
TRAILER_AXLES = (14.0,)

def trailer(fill=False):
    def f(u):
        return (_vehicle(u, TRAILER_PTS, bar(*TRAILER_BELT), TRAILER_AXLES, fill)
                + ink(bar(*TRAILER_TONGUE)))
    return f

def registry():
    R = {}
    for k in D8:
        R['arrow-' + k] = arrow(D8[k])
        R['arrow-double-' + k] = arrow_double(D8[k])
    for k in ('right', 'left', 'up', 'down'):
        R['chevron-' + k] = chevron(D8[k], 1)
        R['chevron-double-' + k] = chevron(D8[k], 2)
        R['caret-' + k] = caret(D8[k])
    R['arrow-horizontal'] = arrow_bi((1, 0))
    R['arrow-vertical']   = arrow_bi((0, 1))
    R['arrow-all']        = arrow_all()
    R['arrow-turn-right'] = arrow_turn(1)
    R['arrow-turn-left']  = arrow_turn(-1)
    R['menu'] = menu(); R['list'] = listicon()
    R['more-horizontal'] = more(False); R['more-vertical'] = more(True)
    R['sort'] = sort_icon(); R['sort-order'] = sort_order(); R['swap'] = swap_icon()

    for m in ('add', 'minus', 'check', 'close'):
        key = 'subtract' if m == 'minus' else m
        R[m] = solo(key)
        for sh in ('circle', 'square'):
            R['%s-%s' % (m, sh)] = enclosed(key, sh, False)
            R['%s-%s-fill' % (m, sh)] = enclosed(key, sh, True)
    R['radio-off'] = radio(False); R['radio-on'] = radio(True)
    R['checkbox-off'] = checkbox_off()
    R['checkbox-on'] = enclosed('check', 'square', False)
    R['checkbox-on-fill'] = enclosed('check', 'square', True)
    R['checkbox-mixed'] = enclosed('subtract', 'square', False)
    R['checkbox-mixed-fill'] = enclosed('subtract', 'square', True)
    for t in TRANSFER:
        R[t] = transfer(t, False); R[t + '-fill'] = transfer(t, True)

    R['search'] = search(); R['search-add'] = search('add')
    R['search-minus'] = search('minus'); R['filter'] = filter_icon()
    R['edit'] = edit(); R['edit-fill'] = edit(True)
    R['trash'] = trash(); R['trash-fill'] = trash(True)
    R['bookmark'] = bookmark(); R['bookmark-fill'] = bookmark(True)
    R['star'] = star(); R['star-fill'] = star(True)
    R['heart'] = heart(); R['heart-fill'] = heart(True)
    R['flag'] = flag(); R['flag-fill'] = flag(True)
    R['link'] = link(); R['external'] = external()
    R['person'] = person(); R['person-fill'] = person(True)
    R['people'] = people(); R['people-fill'] = people(True)
    R['person-add'] = person_badge('add'); R['person-check'] = person_badge('check')
    R['clock'] = clock(); R['clock-fill'] = clock(True)
    R['timer'] = timer(); R['history'] = history()
    R['calendar'] = calendar(); R['calendar-fill'] = calendar(True)
    R['chat'] = chat(); R['chat-fill'] = chat(True)
    R['mail'] = mail(); R['mail-fill'] = mail(True)
    R['bell'] = bell(); R['bell-fill'] = bell(True)
    R['bell-off'] = bell(False, True)
    R['call'] = call(); R['call-fill'] = call(True)
    R['info'] = info(); R['info-fill'] = info(True)
    R['help'] = info(False, True); R['help-fill'] = info(True, True)
    R['warning'] = warning(); R['warning-fill'] = warning(True)
    R['play'] = play(); R['play-fill'] = play(True)
    R['pause'] = pause(); R['pause-fill'] = pause(True)
    R['skip-forward'] = skip(1); R['skip-back'] = skip(-1)
    R['volume'] = volume(2); R['volume-low'] = volume(1); R['volume-off'] = volume(0)
    R['file'] = file_icon(); R['file-fill'] = file_icon(True)
    R['folder'] = folder(); R['folder-fill'] = folder(True)
    R['folder-open'] = folder(False, True)
    R['home'] = home(); R['home-fill'] = home(True)
    R['settings'] = settings(); R['grid'] = grid()
    R['grid-masonry'] = grid_masonry(); R['grid-dense'] = grid_dense()
    R['lock'] = lock(); R['lock-open'] = lock(True)
    R['eye'] = eye(); R['eye-off'] = eye(True)
    R['refresh'] = refresh()
    R['pin'] = pin(); R['pin-fill'] = pin(True)
    R['location'] = location(); R['location-fill'] = location(True)
    R['navigation'] = navigation()
    R['money'] = money(); R['money-fill'] = money(True)
    R['price'] = price(); R['price-fill'] = price(True)

    R['cart'] = cart(); R['cart-fill'] = cart(fill=True)
    for sym in ('add', 'check', 'close', 'alert', 'upload', 'remove'):
        R['cart-' + sym] = cart(sym)
        R['cart-' + sym + '-fill'] = cart(sym, True)
    R['copy'] = copy_icon(); R['copy-fill'] = copy_icon(True)
    R['photo'] = photo(); R['photo-fill'] = photo(True)
    R['photo-stack'] = photo_stack(); R['photo-stack-fill'] = photo_stack(True)

    R['campsite'] = campsite(); R['campsite-fill'] = campsite(True)
    R['campground'] = campground(); R['campground-fill'] = campground(True)
    R['ev-charger'] = ev_charger(); R['ev-charger-fill'] = ev_charger(True)
    R['fuel'] = fuel(); R['fuel-fill'] = fuel(True)
    R['restroom-figures'] = restroom_figures()
    R['restroom-figures-fill'] = restroom_figures(True)

    R['map'] = map_icon(); R['layers'] = layers()
    R['route'] = route(); R['compass'] = compass()
    R['circle'] = circle_icon(); R['circle-fill'] = circle_icon(True)
    R['chart'] = chart(); R['signal'] = signal(); R['activity'] = activity()
    R['bolt'] = bolt(); R['bolt-fill'] = bolt(True)
    R['water'] = water(); R['water-fill'] = water(True)
    R['parking'] = parking(); R['parking-fill'] = parking(True)
    R['wifi'] = wifi()
    R['mountain'] = mountain(); R['mountain-fill'] = mountain(True)
    R['park'] = park(); R['park-fill'] = park(True)
    R['picnic-table'] = picnic_table()
    R['car'] = car(); R['car-fill'] = car(True)
    R['rv'] = rv(); R['rv-fill'] = rv(True)
    R['trailer'] = trailer(); R['trailer-fill'] = trailer(True)
    return R

def build(w=2.0):
    global W
    prev, W = W, float(w)
    try:
        out = {}
        for k, fn in registry().items():
            out[k] = fn('${u}')
        return out
    finally:
        W = prev

if __name__ == '__main__':
    d = build(2.0)
    print(len(d), 'icons')
    bad = [k for k, v in d.items() if 'None' in v or 'nan' in v]
    print('bad:', bad)
