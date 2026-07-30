# Open Icons — Construction Spec

> **Status:** Derived, not declared. Every number below was measured from the 1,185 flattened
> SVGs in [`icons-inspiration/`](../icons-inspiration) (583 at 16px, 602 at 24px), not copied
> from another system. Where the set is internally inconsistent, this document says so and
> names the dominant behaviour as the rule.
>
> **Purpose:** make a new icon derivable rather than invented. If you know the concept and pick
> a keyline, everything else — stroke, terminals, clearances, how the fill variant differs —
> should already be decided for you.

---

## 0. How to read this document

The exported icons are **flattened**: strokes have been expanded to filled outlines, so the
original skeleton is gone. But the skeleton is recoverable, because a flattened 2px stroke is
just its centerline offset ±1 in every direction. Almost every rule below is stated in terms of
the **skeleton** (the centerline you actually draw) rather than the outline (what gets exported).

Three terms, used precisely throughout:

| Term | Meaning |
|---|---|
| **Skeleton** | The centerline path you draw. The source of truth. |
| **Outline / line variant** | Skeleton stroked at 2px. What ships as `*-line.svg`. |
| **Silhouette / fill variant** | The solid mass. What ships as `*-fill.svg`. |

And two for polarity:

| Term | Meaning |
|---|---|
| **Positive counter** | A detail drawn as ink (a solid dot on a white field). |
| **Knockout counter** | A detail cut out of a solid mass (a hole in a black field). |

---

## 1. The one non-negotiable: stroke = 2

**Stroke width is 2 units. At 16px and at 24px. For every stroke, every curve, every angle.**

This is the single strongest signal in the data, and it is what makes everything else fall out.

| Evidence | 16px | 24px |
|---|---|---|
| Icons whose modal local thickness is exactly 2.0 | 326 / 583 (56%) | 348 / 601 (58%) |
| Contour samples landing in the 1.9–2.1 band | dominant mode | 145,466 of ~200k |
| Icons at any other modal thickness | no second mode above 3% | no second mode above 2% |

The remainder are not exceptions to the rule — they're solid forms (blobs, logos, filled
masses) that have no stroke to measure.

**Corroborating signature.** Across both sizes, the most common non-integer coordinate
fractions are `.2929` and `.7071`. Those are `1 ∓ √2/2` — the exact horizontal offset produced
when a **2px** stroke is expanded at 45°. Diagonals in this set are 2px by construction, not by
eye.

**Consequence — and this is the important one:** because the stroke does *not* scale between
sizes, the 16px icon is not a scaled-down 24px icon. See §3.

---

## 2. Grid, live area, keylines

### 2.1 The frame

|  | 16px | 24px |
|---|---|---|
| Canvas | 16 × 16 | 24 × 24 |
| Trim / padding | **0** | **2** |
| Live area | **16 × 16** | **20 × 20** |
| Stroke | 2 | 2 |
| Stroke ÷ live area | 12.5% | 10% |

The 24px grid is Material's classic 20dp live area inside a 24dp box. **The 16px grid has no
padding at all** — 398 of 583 icons touch `x=0` or `y=0`, and 380 touch `16`. At 16px there is
no room to spend on trim: the 2px stroke already costs 12.5% of the box, so the live area is
pushed out to the full canvas.

### 2.2 Keyline shapes

Same family as Material, scaled to each live area:

| Keyline | 16px | 24px | Conformance (16 / 24) |
|---|---|---|---|
| **Circle** | Ø16 | Ø20 | 27.0% / 16.0% |
| **Square** | 14 × 14 | 18 × 18 | 11.9% / 11.3% |
| **Vertical rect** | 12 × 16 | 16 × 20 | 3.3% / 5.8% |
| **Horizontal rect** | 16 × 12 | 20 × 16 | 2.4% / 1.7% |
| **Diagonal** | 10 × 10 | 14 × 14 | (see §7.1) |

The relationships that generate the table:

- **Circle** = the full live area.
- **Square** = live area − 2 (one stroke) on each dimension.
- **Rectangles** = live area − 4 on the short axis.
- **Diagonal** = live area − 6, for glyphs built from 45° strokes (`add`, `close`).

⚠️ **Honest caveat:** measured strictly on ink bounding box, 53% (16px) and 61% (24px) of icons
land on none of these. Most are objects that legitimately fill one axis and not the other
(a receipt, a chevron, a bolt). The keylines are a strong *default*, not a universal fact of the
current set. Treat §2.2 as the rule for new work; don't retrofit it onto every existing icon.

---

## 3. Optical size — why 16 is not a shrunken 24

This is the most consequential structural finding, and it maps directly onto Material's
**optical size** axis. Material implements optical size as a continuous variable-font axis
(20–48dp) whose job is to *hold stroke weight constant as the glyph grows*, instead of scaling
a 24dp master and getting something too heavy. Open Icons does the same thing with **two
discrete optical masters**.

Measured across the 572 names that exist at both sizes, best-fit uniform scale mapping the
16px silhouette onto the 24px silhouette:

```
median 1.250      p25 1.219      p75 1.286      (a pure rescale would be 1.500)
median residual after best-fit scale: 0.069
```

Three different things scale by three different factors:

| What | 16 → 24 | Factor |
|---|---|---|
| Canvas | 16 → 24 | **× 1.5** |
| Live area / glyph | 16 → 20 | **× 1.25** |
| Stroke | 2 → 2 | **× 1.0** |

The measured p25–p75 band (1.219–1.286) brackets the two keyline ratios exactly: **1.25** for
circle-keyline icons (16→20) and **1.286** for square-keyline icons (14→18). The glyph tracks
its keyline; nothing tracks the canvas.

**Rule for drawing at a new size:** never scale an existing master. Re-place the skeleton on the
new keyline, then re-stroke at 2. Anything you scale will come out the wrong weight.

Material states the same principle from the failure side: resizing a 24dp source vector gives
"a large scaled icon that's too heavy compared to the original." Open Icons has the inverse
risk — scaling *down* from 24 to 16 would give a 1.33px stroke that disintegrates on a 1× display.

**Where the ranges sit.** Material's optical size axis runs **20–48dp**. Open Icons runs **16 and
24** — its small master is *below* Material's floor. Two things follow: the 16px master carries
more of the system's legibility burden than any Material optical size does, and if a large size
is ever added (32 / 40 / 48), it needs a **new master**, not an export at another scale. On the
evidence of §3 the glyph should track its keyline (≈ live area) while the stroke moves in whole
units at most.

**What this buys you optically:** at 24px the stroke is 10% of the live area; at 16px it's
12.5%. The small icon is *relatively bolder*, which is exactly what it needs to survive
rasterisation at half the pixel count. That relative bolding is the optical-size effect, and it
is produced automatically by holding stroke at 2 — you don't have to design it.

### 3.1 Why the stroke can't carry optical size once weights exist

Under the agreed weight model (§3.2), `400` resolves to **1.5 at 24px** and **1.0 at 16px**.
Both are exactly **6.25% of canvas** — the 0.5px quantization has flattened the optical exponent
to 1.0 across the two most important sizes. The only other value the grid allows at 16px is 1.5,
which is 9.4% — a 50% overbold.

> **So there is no stroke-based optical compensation available at 16px.**
> It has to come from somewhere else.

It comes from **aperture**. Measured modal clearance is **2.0 at both 16 and 24** (§7) — clearance
does not scale. The glyph shrinks ×0.8 while the gaps hold absolute, so the 16px icon is
*relatively looser*. That is the anti-clogging compensation, and it is already the house style.

**Clearance rule: ≥ 1 × stroke, never below 1.0 absolute.** This reproduces the measured library
exactly (2px stroke → 2.0 clearance) and extends cleanly: 1.5 at 24px, 1.0 at 16px, 2.5 at 48px,
3.5 at 72px.

**23% of 24px icons would clog if simply scaled to 16px** — their tightest aperture drops below
0.8. Worst offenders: `cart` (0.06), `card-id` (0.08), `promo` (0.11), `gift` (0.12). Those need
reshaping, not resizing.

### 3.2 The reshaping ladder

When redrawing a 24px master at a smaller size, apply in order. Stop when clearance is satisfied.

1. **Scale the glyph to the target keyline** (×0.8 for 24 → 16).
2. **Re-stroke at the target size's value** — never scale the stroke. `400`: 1.5 at 24, 1.0 at 16.
3. **Hold clearance ≥ 1 × stroke, absolute.** This is the compensation. Do not let it scale.
4. **Reduce counts until (3) is satisfied.** Three dots become two; eight gear teeth become six.
   Reduce *within* an element rather than deleting the element — the icon keeps its full
   vocabulary at every size.
5. **Marks scale, with a floor.** Dots, wheels and pips scale with the keyline down to a floor of
   **Ø2.5 at 16px**. Hold a mark absolute only when scaling it would drop its clearance below one
   stroke width.
6. **Corners stay squircle.** The corner family does not change between sizes. Ease the `tension`
   axis toward circular as size drops — a lever, not a switch.

**Decisions on record.** Steps 4–6 were forked and settled:

| Question | Chosen | Rejected | Consequence |
|---|---|---|---|
| Marks: scale or hold? | **Scale**, floor Ø2.5 | Hold absolute | `16/calendar-line` dot Ø3 → Ø2.5 |
| Overflow: drop or reduce? | **Reduce count** | Drop the element | `16/card-line` must restore the chip bar |
| Corners across sizes | **Squircle always** | Switch to circular at 16 | `16/calendar-line` corner is off-system |

Rationale for the marks call: holding breaks on `cart`. Its wheels already sit on the bottom edge
at Ø2.5; keeping them Ø3 pushes them out of the box and crowds the basket. A rule that fails on
contact is a preference, not a rule.

⚠️ All three decisions make the existing 16px masters non-conforming. That is expected — **24px is
the reference and 16px is being redrawn to match.**

---

## 4. Terminals, joins, corners

### 4.1 Terminals and joins

**Round is the default.** Arcs of radius exactly 1.0 — i.e. `stroke ÷ 2`, the signature of a
round cap or round join on a 2px stroke — are 20.9% of all arcs in the 24px set and 46.1% of all
quarter-turns. No other radius comes close.

```
add.svg (24)    →  arms 5..19, width 2, four round caps at r=1
close.svg (24)  →  bars 5..19, width 2, round caps + round join at centre
```

**Square terminals are used deliberately, not accidentally.** Where a stroke is cut off by
another form or sits on a shared baseline, it gets a butt end:

```
info-circle-line (24) stem  →  M11 10H13V17H11V10Z      ← flat top and bottom
```

**Rule:** round cap on a free end. Butt cap where the stroke terminates against, or aligns
with, something else. Round join everywhere.

*(Note: this is where Open Icons diverges from Material 1, which specifies squared terminals
throughout. The data here is unambiguously round-dominant; the divergence is intentional and
should stay.)*

### 4.2 Corners

| Corner | Value |
|---|---|
| Exterior, default | **2** |
| Exterior, large containers | 3 |
| Interior | exterior − 2 (one stroke) |

Measured quarter-turn radii at 24px, after excluding r=1 (caps/joins): **r=2 at 9.0%**,
r=3 at 5.1%, r=1.5 at 4.7%.

**Square containers use a smoothed (squircle) corner, not a plain radius.** From
`add-square-line` (24), the outer corner runs from `x=15.86` to `x=21` — a ~5.1-unit reach with
heavy smoothing, iOS-style. Its inner corner reaches ~3.2. The difference is 1.94 ≈ 2, i.e. the
smoothing survives the offset and the 2px stroke stays 2px around the whole corner.

---

## 5. Line → Fill

### 5.1 The invariant

> **A fill variant never extends beyond its line variant's outer edge.**

Measured on 191 pairs at 24px and 187 at 16px, comparing the outer silhouette radially at 720
angles:

| Relationship | 16px | 24px |
|---|---|---|
| **Identical footprint** (p90 ≤ 0.08) | **61.5%** | **61.3%** |
| Same within 0.3 | 4.8% | 4.7% |
| Fill inset ~0.5 | 13.9% | 9.4% |
| Fill inset ~1.0 | 4.8% | 11.0% |
| Fill inset > 1.25 | 1.6% | 0% |
| **Fill larger than line** | **0%** | **0%** |

Median radial delta across every pair: **+0.000**.

### 5.2 The two constructions

**(a) Container icons — footprint identical, glyph knocked out.**

This is the dominant pattern and it is mechanical. The container goes solid at exactly its line
radius; the glyph path is reused **byte-for-byte** as a knockout via `fill-rule="evenodd"`:

```
add-circle-line    →  ring r10/r8  +  path "M12 7C12.5523 7 13 7.44772 13 8V11H16…"
add-circle-fill    →  disc r10     ⊖  path "M12 7C12.5523 7 13 7.44772 13 8V11H16…"
                                       ^^^^ character-for-character the same string
```

Verified identical-glyph pairs include `add-circle`, `close-circle`, `check-circle`,
`add-square`. Circle containers: **r=10 → r=10** (10 pairs at 24px), **r=8 → r=8** (7 pairs at
16px). The container does not move.

**Producing the fill variant of a container icon is a boolean operation, not a redraw.**

**(b) Figure icons — solid mass inset 0.5 from the line's outer edge.**

Where a stroked ring becomes a solid disc with nothing inside it, the mass would read too heavy
at the line's outer radius, so it insets:

| | line ring outer | skeleton | fill solid | Δ vs outer |
|---|---|---|---|---|
| head, 24px | 5.0 | 4.0 | **4.5** | −0.5 |
| head, 16px | 4.0 | 3.0 | **3.5** | −0.5 |
| 24px (4 pairs) | 4.125 | 3.125 | 3.625 | −0.5 |
| 16px (4 pairs) | 3.625 | 2.625 | 3.125 | −0.5 |

So: **fill radius = skeleton + 0.5 = outer − 0.5.** Halfway between the skeleton and the outline.
Median Δ(fill − skeleton) across all 36 ring→solid transitions at 24px is +1.00, pulled up by
the containers in (a); the figure cases cluster tightly at +0.5.

### 5.3 Why the footprint doesn't grow: equal ink

Total ink area, fill ÷ line:

| | median | p25 | p75 |
|---|---|---|---|
| 16px | **0.90** | 0.66 | 1.20 |
| 24px | **0.91** | 0.62 | 1.30 |

A fill icon carries roughly the *same* amount of ink as its line counterpart — not 2–3× more.
That is the whole point of the knockouts. Line and fill balance because the fill variant spends
its extra mass on counters instead of on area.

**Rule of thumb:** if your fill variant has visibly more ink than your line variant, you have
not cut enough counter out of it.

---

## 6. Counters — and why they grow in the fill variant

This is the "dots look bigger on fill" question, and the data confirms it precisely.

**Why they grow — and it isn't the reason you'd first reach for.** Two opposing optical effects
act on a counter cut out of a solid mass:

| Effect | What it says | Direction |
|---|---|---|
| **Visual bleed / irradiation** | A light shape on a dark field blooms and reads *larger* than the same shape dark-on-light. This is exactly the effect Material's **grade** axis exists to cancel — hence grade `−25` for a light icon on a dark background. | argues for **shrinking** knockout counters |
| **Aperture closure** | A small hole inside a large mass loses definition. At 16–24px the surrounding ink, antialiasing, and any rasterisation error all eat into it, and the counter clogs shut. Type designers hit the same wall in bold weights and answer it by opening counters. | argues for **growing** knockout counters |

**Open Icons empirically chose aperture closure.** At 24px, 62% of counters grow on the flip to
knockout and **0% shrink** — not one, in either size set. At the scale this system operates,
keeping the counter *open* beats keeping it *optically equal*.

This is worth stating plainly because it means **Material's grade guidance does not transfer
directly.** Material's `−25` thins a light-on-dark symbol globally. Open Icons goes the other
way, locally, on apertures only. Both are right for their scale — Material's optical size range
starts at 20dp, and Open Icons runs down to 16.

### 6.1 Measured compensation

Circles that are **ink in the line variant** and **knockout in the fill variant**:

| | 24px | 16px |
|---|---|---|
| n | 24 | 17 |
| **median Δr** | **+0.25** | +0.00 (mean **+0.088**) |
| grew | **62%** | 47% |
| unchanged | 38% | 53% |
| **shrank** | **0%** | **0%** |

Most common transitions:

| 24px | 16px |
|---|---|
| r 1.5 → 1.75 (**+17%**) ×6 | r 1.25 → 1.375 (**+10%**) ×6 |
| r 1.5 → 2.0 (**+33%**) ×4 | r 1.25 → 1.5 (**+20%**) ×1 |
| r 1.25 → 1.5 (**+20%**) ×4 | r 2.0 → 2.5 (**+25%**) ×1 |

**No counter anywhere in the set gets smaller when it becomes a knockout.**

### 6.2 The rule

> **Knockout counters grow. Positive counters don't.**
> Radius +0.25 at 24px, +0.125 at 16px — one step on that size's sub-grid — or ~+15–20%,
> whichever is cleaner. Clearance between counters grows by +0.5.

### 6.3 Worked example — `info-circle`

The cleanest specimen in the set. Same icon, both variants, 24px:

| | line (positive) | fill (knockout) | Δ |
|---|---|---|---|
| Dot radius | 1.25 | **1.5** | **+0.25 (+20%)** |
| Dot centre y | 7.75 | 7.25 | −0.5 |
| Stem width | 2 | 2 | **0** |
| Stem span y | 10 → 17 (h 7) | 10.25 → 17.75 (h **7.5**) | **+0.5** |
| Dot-to-stem gap | 1.0 | **1.5** | **+0.5** |
| Glyph total height | 10.5 | 12.0 | +1.5 |

Note what *doesn't* change: **stem width stays 2.** The compensation is applied to round
counters and to gaps, never to stroke weight. Stroke is still the invariant from §1.

### 6.4 Second specimen — `warning-triangle`

Confirms the same direction on an organic form:

| | line | fill | Δ |
|---|---|---|---|
| Stem height | 6.72 | 8.00 | +1.28 |
| Stem-to-dot gap | 0.70 | 0.96 | **+0.26** |
| Glyph total height | 9.94 | 11.36 | **+14%** |

The glyph grows into the solid triangle and its internal gap opens up. Note the dot here goes
1.33 → 1.28, marginally *down* — a tapered-wedge glyph behaves slightly differently from a
geometric one. Don't over-fit: the reliable invariants are **glyph grows** and **gap opens**.

### 6.5 Relation to Material's *grade* axis

Material separates two thickness controls:

- **Weight** (100–700) — the symbol's stroke weight. Also affects overall size. Material's floor
  for a 24dp icon is weight 200.
- **Grade** (−25 / 0 / 200) — a finer adjustment with *smaller* impact on size. Grade 0 is the
  default for dark-on-light; **−25 for light-on-dark**, to cancel visual bleed; positive values
  (up to 200) to emphasise, e.g. an active state.

**Open Icons has neither axis.** Stroke is fixed at 2 (§1) — a single weight, single grade
system. Where Material would turn a dial, Open Icons redraws.

Two consequences worth being deliberate about:

1. **There is no "active state" emphasis mechanism.** Material reaches for positive grade;
   Open Icons has only the line → fill flip. That flip is a much larger visual jump than
   grade 200. If a denser emphasis step is ever needed, grade is the axis to add.
2. **There is no dark-mode compensation.** Material ships `−25` for light-on-dark. Open Icons
   renders the same geometry in both themes. At 2px on a 16–24px grid this is defensible —
   there's no sub-pixel headroom to spend — but it is an unhandled case, not a solved one.

If Open Icons ever ships a real grade axis, §6.1 is partial calibration data for it:
**one perceptible step ≈ 0.25 units at 24px, 0.125 at 16px.** Note the sign — §6's compensation
runs *opposite* to Material's grade, for the reason given above.

---

## 7. Clearance

**Minimum clearance between two forms = 2 (one stroke width).**

Modal clearance per icon:

| | 2.0 | 1.5 | 1.0 |
|---|---|---|---|
| 24px line | 26% | 8% | 7% |
| 24px **fill** | **39%** | 18% | 6% |
| 16px line | 18% | 19% | 16% |
| 16px **fill** | **38%** | 25% | 12% |

Both variants centre on 2.0, but **fill concentrates harder on it** — consistent with §6: negative
space needs more room than positive space to read as the same aperture. Line variants tolerate
1.0–1.5 far more often.

**Rule:** 2 is the default gap. 1.0 is the tight limit, and only in line variants. If a fill
variant needs a gap below 2, open it to 2 and shrink the form instead.

### 7.1 Special case — the head-to-shoulder gap = 1

There is one clearance that is deliberately tighter than 2, and it is **perfectly consistent
across the whole figure family**:

| Icon | 16 line | 16 fill | 24 line | 24 fill |
|---|---|---|---|---|
| `person-user` | 1.00 | 1.00 | 1.00 | 1.00 |
| `person-find` | 1.00 | 1.00 | 1.00 | 1.00 |
| `person-profile` | 1.00 | 1.00 | 1.00 | 1.00 |
| `people-add` | 1.00 | 1.00 | 1.00 | 1.00 |
| `people-group` | 1.00 | 1.00 | 1.00 | 1.00 |

Twenty independent measurements, all exactly 1.00. This is a **half-stroke** gap — a joint, not
a separation. It reads as "these two forms are one body," which is precisely the semantic. Use
2 to say *two things*; use 1 to say *one thing with a seam*.

---

## 8. Archetype recipes

### 8.1 The person / figure system

The most rigorously specified family in the set. Every figure icon uses it.

|  | 16 line | 16 fill | 24 line | 24 fill |
|---|---|---|---|---|
| Head skeleton radius | 3.0 | — | 4.0 | — |
| Head as drawn | ring, outer **4.0** | solid **3.5** | ring, outer **5.0** | solid **4.5** |
| Head centre y | 4.0 | **4.5** | 7.0 | **7.5** |
| **Head bottom (datum)** | **8.0** | **8.0** | **12.0** | **12.0** |
| **Shoulder top** | **9.0** | **9.0** | **13.0** | **13.0** |
| **Gap** | **1.0** | **1.0** | **1.0** | **1.0** |
| Shoulder outer | 1.5 → 14.5 | 2.0 → 14.0 | 4 → 20 | 4.5 → 19.5 |
| Shoulder bottom | 16.0 | 15.0 | 21.0 | 20.0 |

**How to construct it:**

1. Draw the head **skeleton** circle: r=4 at (12, 7) for 24px; r=3 at (8, 4) for 16px.
2. Line variant: stroke it at 2 → outer r=5. Head bottom lands at 12.
3. Fill variant: replace with a solid disc at **outer − 0.5** (r=4.5), then **move the centre
   down 0.5** so the head's bottom tangent stays pinned at 12.
4. Shoulder top sits at head bottom **+ 1**, in both variants.

Step 3 is the elegant part and worth internalising: the head shrinks by 0.5, but it shrinks
*from the top*. The bottom tangent is the datum and it never moves — which is exactly why the
gap can be 1.00 in all twenty measurements without anyone having to maintain it by hand.

**Exception:** `group-circles-4` uses gap 1.5 (line) / 2.5 (fill). It's a diagram of four
abstract circles, not a figure. Correct to exclude it.

### 8.2 The crossout (X)

|  | 16 | 24 |
|---|---|---|
| `close` — ink bbox | 3 → 13 (**10 × 10**) | 5 → 19 (**14 × 14**) |
| `close` — skeleton | 4 → 12 (8 × 8) | 6 → 18 (12 × 12) |
| **Bar width** | **2.000** | **2.000** |
| Caps | round, r=1 | round, r=1 |
| Centre join | round | round |

**Construction:** two 45° skeleton strokes crossing at the centre of the live area, extent
= live area − 6 (the diagonal keyline, §2.2), stroked at 2 with round caps and a round join.

**Measured bar width is exactly 2.000** in every crossout variant at both sizes — standalone,
in-circle, in-square, and `prohibited`. There is no diagonal weight compensation. The `.2929` /
`.7071` coordinate signature (§1) is the fingerprint of that expansion.

**Inside a container**, the X shrinks and clears the container's inner edge by ~1:

```
close-circle-line (24)  container ring r10/r8   glyph skeleton 7.79 → 16.21
                        glyph corner + cap reaches r≈6.95 from centre
                        clearance to container inner edge (r=8) ≈ 1.05
```

The contained glyph's skeleton spans 8.42 vs the standalone's 12 — **~70%**. Same for
`check-circle`, `add-circle`.

**The slash crossout (`prohibited`)** is the other crossout form, and it's fully regular:

| | 16 | 24 |
|---|---|---|
| Ring outer / inner | 8 / 6 | 10 / 8 |
| Ring stroke | 2 | 2 |
| Slash width | 2 | 2 |
| Fill: inner disc radius | 6 | 6 → *see note* |
| Fill: gap ring-inner-edge → disc | 2 | 2 |
| Fill: slash gap through disc | 2 | 2 |

`prohibited-fill` is the one place a fill variant is **not** a solid disc: it keeps the ring and
adds an inner disc split by a 2-unit diagonal gap, with 2 units of clearance from the ring.
Everything in it is 2. It's a legitimate three-layer construction, but note it diverges from the
§5.2(a) container pattern — flag it if you're aiming for consistency.

### 8.3 Glyph-in-container

The highest-leverage recipe, because it's fully mechanical.

1. **Container**: circle keyline — Ø20 at 24px (r=10), Ø16 at 16px (r=8).
2. **Line variant**: container as a 2px ring (r=10 / r=8 inner). Glyph drawn as positive ink,
   sized to clear the ring's inner edge by ~1.
3. **Fill variant**: container becomes a solid disc at the **same** outer radius. **Reuse the
   glyph path unchanged** as an even-odd knockout.
4. Only apply §6 counter compensation if the glyph contains small round counters or internal
   gaps (`info`, `warning`); a chunky glyph (`add`, `close`, `check`) transfers verbatim.

Square containers work identically with the 18×18 / 14×14 keyline and the smoothed corner
from §4.2.

### 8.4 Dots and dot rows

| | 16 | 24 |
|---|---|---|
| `more-horizontal` dot radius | 1.5 (Ø3) | 2.0 (Ø4) |
| Centre-to-centre spacing | 4.5 | 6.0 |
| Edge-to-edge gap | 1.5 | 2.0 |
| Positions | 3.5 / 8 / 12.5 | 6 / 12 / 18 |

**Rule:** dot Ø = stroke × 2 at 24px (4), stroke × 1.5 at 16px (3). Gap = the dot's own radius
+ 0.5, which reduces to the §7 default of 2 at 24px.

Standalone small-dot radii cluster at **1.5** (24px, 18 icons) and **1.25** (16px, 19 icons) —
use those as the default accent-dot size, then apply §6 if the dot becomes a knockout.

---

## 9. Where Open Icons sits in Material's taxonomy

Material Symbols ship three styles. Open Icons is unambiguously **rounded**:

| Style | Material's definition | Open Icons |
|---|---|---|
| Outlined | stroke + fill attributes, light and clean, for dense UIs | — |
| **Rounded** | "a corner radius that pairs well with brands that use heavier typography, curved logos, or circular elements" | ✅ round caps, round joins, r=2 exterior corners, smoothed square containers (§4) |
| Sharp | 0dp corner radius, straight edges | — |

Naming this matters for governance: it means "should this new icon have a sharp corner?" has a
standing answer (no), and it means a contributor porting an icon in from a sharp or outlined set
has a defined conversion to make rather than a judgement call.

**The line/fill pair is Material's `FILL` axis at its two endpoints** — `0` and `1`, with nothing
in between. Material's stated semantic for that axis is the one to honour: fill "can be used to
convey a state of transition, such as unfilled and filled states" — selected vs unselected nav,
active vs inactive. It is a **state** signal, not a decorative choice. Open Icons has no
intermediate values, so the transition is a swap, not an animation.

---

## 10. Usage rules that constrain construction

Three Material rules that have direct consequences for what you draw:

**Some icons should stay filled at all sizes.** Material: for legibility and recognition, "some
symbols should remain filled, such as full body human icons or proprietary icons." This is worth
auditing against §8.1 — Open Icons ships the whole person family in both variants, and the line
variant of a small figure is exactly the case Material calls out. It is not automatically wrong,
but at 16px a `-line` figure is the riskiest thing in the set.

**Target size.** 24px symbol → **48px** target. Dense/pointer contexts: a 20px symbol → 40px
target. The icon's live area is not the hit area; don't pad the SVG to reach it.

**Baseline alignment with text.** Shift the symbol's baseline **down ≈11.5% of the text size**
when setting icons inline with type. Match symbol size to text size — don't mix.

**Small sizes need labels.** Below 20dp, complex or multi-part icons and any icon carrying a key
action need an accompanying text label. This is a real constraint on the 16px set: if an icon
can't survive §3 without a label, that's a signal to simplify the skeleton, not to add detail.

---

## 11. Checklist for a new icon

Draw the **skeleton** only. Everything else is derived.

**Geometry**
- [ ] Pick a keyline (§2.2). Circle if the form is round, square if boxy, rectangle if the
      subject has a dominant axis, diagonal if it's built from 45° strokes.
- [ ] Skeleton anchors on integers; half-units only where the form genuinely needs them.
- [ ] Draw both sizes from the skeleton. **Do not scale one into the other** (§3).

**Stroke**
- [ ] Stroke = 2. Everywhere, both sizes, including diagonals and curves.
- [ ] Round caps on free ends; butt caps where a stroke terminates against another form.
- [ ] Round joins.
- [ ] Exterior corners r=2 (r=3 on large containers). Interior corners = exterior − 2.

**Clearance**
- [ ] Default gap 2. Never below 1.
- [ ] Gap 1 *only* to signal that two forms are one body (head-to-shoulder, §7.1).
- [ ] Fill variants: no gap below 2.

**Fill variant**
- [ ] Container icon → solid container at the same outer radius, glyph reused verbatim as an
      even-odd knockout (§5.2a).
- [ ] Figure icon → solid mass at outer − 0.5, anchored so the contact datum doesn't move
      (§5.2b, §8.1).
- [ ] Fill silhouette must not exceed the line silhouette anywhere (§5.1).
- [ ] Ink area within roughly ±30% of the line variant (§5.3). More ink than that means not
      enough counter.

**Counters**
- [ ] Round counters that flip positive → knockout: **+0.25 radius at 24px, +0.125 at 16px**
      (§6.2).
- [ ] Internal gaps in a knockout glyph: **+0.5**.
- [ ] Stroke width does **not** change. Ever.

---

## 12. Machine-readable

All of the above is encoded in [`data/construction-tokens.json`](../data/construction-tokens.json)
for linting, generation, and AI-assisted authoring.

---

## Appendix A — Governance findings surfaced by the measurement

Not construction rules, but they fell out of the analysis and are actionable under the
README's consolidation goals.

**Byte-identical duplicates** — 18 groups at 24px (36 files), 15 at 16px (30 files). Same
geometry shipped under two names:

| Keep | Deprecate |
|---|---|
| `info-circle-line` / `info-circle-fill` | `info-line` / `info-fill` |
| `money-circle-line` / `money-circle-fill` | `money-circle-enabled-line` / `-enabled-fill` |
| `tipping-line` / `tipping-fill` | `tips-staff-line` / `tips-staff-fill` |
| `bookmark-fill` | `bookmark-fill-light` |
| `favorite-fill` | `favorite-fill-light` |
| `send` | `send-line` (16px) |
| `call-dasher` | `call-dasher-line` (24px) |
| `call-office` | `call-office-line` (24px) |
| `order-medium-fill` | `order-medium-fill-fr-ca` |
| `card-doordash-monocolor` | `card-doordash-rewards-monocolor` |

**`dock-right-fill` is identical to `dock-right-line`** at both sizes — a fill variant that was
never actually drawn. This is a bug, not a duplicate.

**Coverage gap** — 19 names exist at 24px with no 16px counterpart; none the other way.

**Variant coverage** — 208 `-line` vs 193 `-fill` at 24px: 15 line icons have no fill partner.

---

## Appendix B — Method

Measurements were taken by parsing every SVG path into polygons and:

- **Stroke width**: ray-casting inward along the surface normal from ~900 sample points per
  contour, taking the modal first-crossing distance. This measures the actual local thickness of
  a flattened outline without needing the original stroke.
- **Silhouette comparison**: casting 720 rays inward from outside the canvas toward the centre
  and comparing the resulting radial profiles between line and fill variants.
- **Circle detection**: fitting circular arcs to cubic Béziers via normal intersection, then
  verifying every sampled point lies on the fitted circle.
- **Counter polarity**: point-in-shape test at each detected circle's centre, using the correct
  per-path `fill-rule`, to distinguish positive ink from knockout.
- **Cross-size scaling**: best-fit uniform scale between each name's 16px and 24px radial
  profile, with residual reported.

Scripts and raw output are reproducible from the session scratchpad; nothing in this document is
asserted without a count behind it.

---

## Sources for the cross-referenced Material concepts

Material is cited here as a **reference point, not an authority**. Where the measured Open Icons
behaviour diverges (round vs squared terminals in §4.1, counter compensation sign in §6.5), the
measurement wins and the divergence is called out.

- [Icons — Material Design 3](https://m3.material.io/styles/icons/applying-icons) and
  [Designing icons](https://m3.material.io/styles/icons/designing-icons) — the four axes
  (weight 100–700, fill 0–1, grade −25/0/200, optical size 20–48dp); the three styles
  (outlined / rounded / sharp); visual-bleed rationale for grade; target sizes; 11.5% baseline
  shift; guidance to keep full-body human icons filled
- [Icons — Style, Material Design 1](https://m1.material.io/style/icons.html) — 20dp live area
  in a 24dp box, keyline shapes, 2dp stroke and 2dp exterior corner radius
- [Material Symbols — Google Fonts Knowledge](https://fonts.google.com/knowledge/glossary/material_symbols)
- [Material Symbols guide — Google Developers](https://developers.google.com/fonts/docs/material_symbols)
