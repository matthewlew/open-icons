# Open Icons — built set

Generated. Do not hand-edit anything in this directory.

```bash
python3 tools/export.py icons 2.0
```

`tools/generate.py` holds the geometry; `tools/export.py` writes it out. The
second argument is the stroke on the weight axis, which the axis carries from
1.0 to 2.5.

## What's here

| path | what it is |
| --- | --- |
| `24/<name>.svg` | 174 standalone SVGs on the 24 grid, ready to drop in a sprite or an `<img>` |
| `icons.json` | `{grid, stroke, icons: {name: innerMarkup}}` — for anything that renders at runtime |
| `names.json` | just the names, for a manifest or a lint rule |

## The `${u}` placeholder

54 of the 174 icons carry a mask, because a mark that crosses a wall needs a
moat cut out of that wall, and a moat is a mask. A mask needs an id.

`icons.json` leaves the id as `m${u}` / `t${u}` / `k${u}`. Substitute `${u}` with
something unique **per rendered instance** — two copies of `copy` on one page
with the same mask id will fight over it. The standalone files in `24/` have the
placeholder already removed, since a file is its own document and cannot collide.

## The stroke is not a CSS knob

The geometry is weight-aware: every clearance in the set is a ratio of the
stroke, not a constant, so a different weight is a different drawing rather than
the same paths at a different `stroke-width`. Re-run the exporter for another
weight; do not restyle `stroke-width` downstream.

Concretely, that means **never apply a rule that sets `stroke-width` across the
whole SVG** — including LDS's own `.lds-icon`. The mask strokes are 5–6 units
wide on purpose. Overriding them to the nominal weight closes every moat in the
set.
