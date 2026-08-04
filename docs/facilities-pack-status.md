# Facilities / travel pack — status

Handoff note for picking this up in a fresh session. Companion to
[`proposal-travel-outdoors-pack.md`](proposal-travel-outdoors-pack.md), which is
the brief; this is what actually got built against it.

**Branch:** `proposal/facilities-pack-review` — 3 commits ahead of `origin`,
unpushed. **Set size:** 174 → **216** icons at 24px.

---

## What shipped

| Commit | Icons |
|---|---|
| `afbd8d7` | `campsite`＋fill, `campground`＋fill, `ev-charger` |
| `446038a` | `map` `layers` `route` `compass` · `circle`＋fill `chart` `signal` `activity` · `bolt`＋fill `water`＋fill `parking`＋fill `wifi` · `mountain`＋fill `park`＋fill `picnic-table` |
| `2f6d567` | `car` `rv` `trailer` (＋fills) · `fuel`＋fill · `ev-charger-fill` · `restroom-figures`＋fill |
| `f06c007` | `shower` `campfire` `pets` `food` `store` |

Everything is generated from [`tools/generate.py`](../tools/generate.py) against
[`icon-construction-spec.md`](icon-construction-spec.md). Nothing is traced, and
nothing is a one-off master — the whole pack is geometry as a function of `W`.

### Primitives added

| Primitive | What it does |
|---|---|
| `ngon_r(pts, r)` | `ngon` driven by the §4.2 corner **radius** rather than a tangent length. A polygon whose vertices differ in angle needs a different extent at each one to land on one radius. |
| `e_apex(h)` | The set's apex reach per unit of height, lifted out of the tent block. `warning`'s triangle is the only shipped sharp vertex, so its ratio is the family constant. |
| `_vee(...)` | Lower half of a plate, rounded on the radius a closed plate would use. |
| `bars(heights)` | n bars on a shared baseline, pitch `W + gap()`. |
| `droplet(cx, cy, r, ay)` | Circle and apex joined by their common tangents — `location()`'s construction, lifted. It existed inline in three places. Now `location`, `water` and `fuel` all come off one curve. |
| `arcs(n, ...)` | n concentric arcs, radial pitch = `volume`'s wave pitch. |
| `_pump(u, mark, arm, fill)` | `fuel` and `ev-charger` are one machine — same tank, plinth and arm geometry; the mark on the face and what the arm ends in are the only difference. |
| `_vehicle(u, pts, belt, axles, fill)` | One chassis for `car` / `rv` / `trailer`. Wheels are `cart`'s, not new. |

---

## Where the build departed from the proposal

Each of these is a construction fact, not a preference. Worth reading before
anyone "fixes" them back.

- **`park` is a broadleaf canopy, not a notched gable.** Two conifer tiers put
  the upper slope's underside 2.29 from the lower one, so the step closes at
  `W`; one tier is just `campsite` wearing a trunk. A canopy also settles the
  proposal's open question 3 (`park` vs `mountain` at 16px) by not being a
  triangle at all.
- **`trailer` drops the tow vehicle** the proposal asked for. The tongue is what
  says trailer; two vehicles inside 20 units gives each about 8.
- **`food` is fork + spoon, not fork + knife.** A knife at this size is a bar
  with a taper, and beside a fork's handle it reads as two bars.
- **`campfire`'s flame has no inner counter.** An inner shape needs `gap()` from
  the outer wall on both sides — 2 + 2 + 2 before it has any width of its own —
  and this flame's interior is 7. §3.2 step 4: reduce within the vocabulary. The
  notch at the flame's base is what separates it from `water`'s droplet.
- **`picnic-table` ships line-only.** Four bars have no interior to flood, and
  `solidify()` on an open run returns the run — shipping a fill would reproduce
  the `dock-right-fill` bug Appendix A flags. Same reason `menu` and `chart` have
  no fills. If the app needs a selected state there, it belongs on the chip.

## `mountain` vs `campground` — the collision, and how it was resolved

Both are triangles on a ground datum, which at 16px is one icon. Three
separators, all structural:

1. **One silhouette with a saddle.** `campground` is two tents with a moat cut
   between them, so it reads as two objects; a range reads as one landform.
2. **The horizontal-rect keyline (20×16)** against `campsite`'s square 18×18.
3. **The counter is at the peak, not the base.** `campsite`'s counter is a
   doorway on the ground; `mountain`'s is a snow line near the summit.

The saddle sits 9.8 below the main peak *because* of (3): a shallow saddle
crowds the snow line upward until the counter above it is a 2 × 1.9 sliver with
0.55 of inradius, under the §7 floor of 1.0. As shipped it measures **1.275**.

---

## Open — decisions, not drawing

1. **`restroom` and `restroom-vault` are unbuilt.** `restroom` is straightforward
   (rrect + bowl). `restroom-vault` is blocked: the proposal itself flags its
   silhouette collision with `home` as must-resolve-before-shipping, and
   resolving it means deciding how far the vault may diverge from the home
   pentagon.
2. **`restroom-figures` sits close to `people`.** As shipped it is two plain
   equal figures, separated and symmetric, against `people`'s overlapping unequal
   pair. The conventional fix is the skirted pictogram — a product call about a
   gendered convention, not a construction one, so it was left open. Its head
   ring's counter is also at Ø2.0, exactly on the §7 floor, and will be the first
   thing to need rework for a 16px master.
3. **`zoom-in` / `zoom-out` aliases.** The proposal wants these aliased to
   `search-add` / `search-minus` rather than redrawn. There is **no alias
   mechanism** in `tools/export.py` at all — this is a tooling task, not an icon.
4. **The `travel` scope question** (proposal open question 1) is untouched.
5. **No 16px masters exist** for any of this. §3 forbids scaling the 24px ones.

---

## How this was verified — and the two things it does NOT cover

Verification is a headless-puppeteer geometry probe: path box, ink box, ink
area, per-element clearance, the §5.1 radial silhouette check, the §5.3 ink
ratio, and largest-inscribed-disc for every counter. A regression diff of
`icons/icons.json` against `HEAD` ran at every step — **all previously shipped
icons stayed byte-identical throughout**, including `ev-charger` across the
`_pump` refactor.

⚠️ **`tools/icon-lint.py` cannot evaluate this generator's output.** It expects
*flattened* SVGs and ray-casts filled contours, so it reads a stroke-attributed
path as a solid. `add` and `close` — the spec's own canonical examples — score
100 "unmeasurable"; `warning` scores 67; `bolt` scores identically to
`bolt-fill`. Its numbers are not evidence here in either direction. Do not chase
them. (It also writes `tools/lint.json` into the repo as a side effect, and it
defaults `ICON_ROOT` to `icons-inspiration/`, not `icons/`.)

⚠️ **None of these 42 files has been reviewed by eye.** Screenshot capture is
blocked in the environment they were built in — `file://` renders as a static
snapshot in the browser pane and `localhost` is policy-blocked — so every number
above is geometric measurement. Measured-correct and looks-right are not the
same claim, and this project has already had one round where the numbers passed
and the drawing did not. **A visual pass over the whole pack is the single
highest-value next action.**

### Ink ratios above the §11 checklist's ±30%

`circle-fill` 2.50 · `water-fill` 2.16 · `park-fill` 2.16 · `parking-fill` 1.90 ·
`mountain-fill` 1.62 · `restroom-figures-fill` 1.55.

All are solid figures with no counter to cut — a pattern the shipped set already
carries (`heart-fill` 2.30, `play-fill` 1.94, `location-fill` 1.70). §5.3's band
is calibrated on a reference library of container knockouts and does not
describe this case.

### One metric artifact worth knowing

The §5.1 radial check reads 7.54 on `restroom-figures-fill`. That is the metric
failing, not the icon: `person-fill` reads 7.13 and `people-fill` 8.21 on the
same measure, because the figure family's line variant is an open arch and the
fill closes it, so ink appears in the arch's mouth. The mouth is interior
negative space, not outside the outline, and a max-radius-per-angle profile
struck from the canvas centre cannot tell the difference. For that family the
real check is the ink box, and line and fill share one exactly.
