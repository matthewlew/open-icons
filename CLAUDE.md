# open-icons

A weight-aware, parametric icon system. Icons are **generated** from
`tools/generate.py` as functions of stroke width `W` — they are not drawings
that happen to be SVGs.

The principles, in plain language — the part that does not change:

@docs/principles.md

The target and the rules for getting something into the set:

@docs/north-star.md

Everything below is the short list of things that fail **quietly**. The
reasoning for all of it is in [`docs/decisions.md`](docs/decisions.md).

## The one rule that is easy to break

**A change needs an entry in [`docs/decisions.md`](docs/decisions.md), in the
same commit,** when it:

- adds, removes or reshapes an icon or a primitive
- changes what a construction rule means
- reverses a prior call
- sets a constraint a consumer has to respect

Exempt: typos, regenerated output, new example pages, and additions that follow
an existing pattern without changing it.

**The test for whether it is a decision at all: name what it ruled out.** If
nothing was ruled out it is a fact about the system and belongs in the README or
the North Star. Write the entry while the reasoning is still in hand — the diff
shows what changed; only you know what you rejected on the way.

**Reversals matter most.** Mark them `reversal` and amend the entry being
overturned rather than deleting it. This repo has already had one: a correct
sharp-corner fix was reverted because a lint score got worse, and the score was
the symptom, not a false positive.

## Traps

- **`icons/` is generated. Never hand-edit it.** The source of truth is
  `tools/generate.py`. You cannot fix an icon by nudging a path — fix the
  function and regenerate.
- **`tools/icon-lint.py` cannot score anything this generator produces.** It
  expects *flattened* SVGs and reads a stroke-attributed path as a solid: `add`
  and `close` come back "unmeasurable", `bolt` scores identically to
  `bolt-fill`. Do not chase its numbers. It also writes `tools/lint.json` into
  the repo and defaults `ICON_ROOT` to `icons-inspiration/`.
- **Verify by measurement, not by eye — then by eye.** Bounding box against its
  keyline, clearance between every pair of forms, largest-inscribed-disc for
  every counter, fill/line footprint and ink ratio, and a diff of
  `icons/icons.json` against `HEAD` for regressions. Screenshot capture has been
  unavailable in every session so far, so **nothing in the travel pack has been
  looked at.** Measured-correct and looks-right are not the same claim.
- **A fill variant identical to its line variant is a bug, not a variant.** An
  icon made of open strokes has no interior to flood. If `solidify()` gives you
  back what you passed it, the icon is line-only — say so and move on.
- **Line is the default; fill is emphasis.** Assume line. Reach for fill when an
  icon must carry more weight than the words around it — status and severity
  first (`warning-fill`, `close-circle-fill`, `check-circle-fill`, `info-fill`
  are the alerting forms), then the selected item. An icon nothing ever needs to
  emphasise gets no fill. This reversed an earlier call; see `decisions.md`.
- **16px is not a scaled 24px.** Stroke does not scale, so scaling a master
  gives the wrong weight. No 16px masters exist yet; the files in
  `icons-inspiration/16` are reference corpus, not output.
- **`data/icon-rules.json` is generated** by `tools/build-icon-rules.py`, which
  validates every icon name and cross-reference against `icons/names.json`.
  Hand-edits are overwritten and unchecked.
- **The `${u}` placeholder in `icons.json` must be unique per rendered
  instance.** Two copies of a masked icon on one page with the same id fight
  over it. The standalone files in `icons/24/` already have it stripped.
- **Ask whether it should be an icon at all.** A label is often clearer, and
  icons added for their own sake are noise. Principle 1.
- **An icon may carry several meanings, and that is fine.** The library holds one
  drawing per thing; which icon a given product uses for a given action is bound
  in a product manifest (`product_binding` in `data/icon-rules.json`), and that
  binding outranks any general recommendation.
- **Never let a feature adopt an icon as its badge.** Icons name actions.
  A sparkle drafted to mean "AI" stops being usable for the literal thing.
- **Cultural semantics are UNVERIFIED.** `cultural_semantics` in the rules file
  is a hazard list, not an audit. A circle means *correct* in Japan; 53 icons in
  this set point somewhere and RTL reverses them. No locale review has been done.
- **Clearances are solved, not chosen.** They are `gap ≥ 1 × stroke` solved
  exactly at `W = 2`. A number that looks arbitrary usually is not — check
  `generate.py` before changing it.

## Two audiences, two files

Keep these apart; blurring them is how both stop being trusted.

| | |
|---|---|
| How an icon is **built** | [`docs/icon-construction-spec.md`](docs/icon-construction-spec.md) · [`data/construction-tokens.json`](data/construction-tokens.json) |
| Which icon to **reach for** | [`data/icon-rules.json`](data/icon-rules.json) |

Selection context is structured because an AI queries it at use time. It answers
*kebab or hamburger*, *X or circled-X*, *line or fill* — never corner radii.

## Build

```bash
python3 tools/generate.py                 # sanity check: count + malformed paths
python3 tools/export.py icons 2.0         # regenerate icons/ at stroke 2.0
python3 tools/build-icon-rules.py         # regenerate + validate data/icon-rules.json
```

The second argument to `export.py` is the stroke on the weight axis, which the
axis carries from 1.0 to 2.5.

## Current state

216 icons at 24px. The travel & outdoors pack (the Roadtrip forcing function) is
built apart from `restroom` and `restroom-vault` — see the open-questions table
at the foot of [`docs/decisions.md`](docs/decisions.md) before starting
anything there.
