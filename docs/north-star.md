# Open Icons — North Star

The target every session on this repo pulls toward. Stable by design: this file
changes when the *goal* changes, not when an icon does.

For the short, non-technical version, read [`principles.md`](principles.md)
first — ten rules, no measurements. This file is the next layer down.

It deliberately does **not** restate the geometry. Construction rules live in
[`icon-construction-spec.md`](icon-construction-spec.md) and its machine-readable
mirror [`../data/construction-tokens.json`](../data/construction-tokens.json).
This document says what we are building and how a thing gets in; that one says
how it is drawn.

---

## 1. The target

**A comprehensive icon component set, line and fill, built parametrically from a
24-unit bounding box, whose visual lineage is measured from `icons-inspiration/`
rather than asserted.**

Four claims in that sentence, each load-bearing.

### Comprehensive, and line + fill

**Line is the default variant.** Almost every icon, in almost every surface, is
a line icon. Fill is the emphasis style you reach for when an icon has to carry
more weight than the words around it — most often status and severity. Not every
icon has one, and that absence is information rather than an omission. See
[§ Line is the default; fill is emphasis](#3-line-is-the-default-fill-is-emphasis).

### 24 is the master; other sizes are built, not scaled

The 24-unit box is the default and the reference. **A 16px icon is not a
shrunken 24px icon** — stroke does not scale, so scaling a master gives the
wrong weight. Other sizes are re-placed on their own keyline and re-stroked.
The spec's §3 carries the measurement behind that, and §3.2 the ladder for
doing it.

> **Current state:** 24 exists (216 icons). **16 does not.** The 583 files in
> `icons-inspiration/16` are the reference corpus, not our masters. Drawing the
> 16 masters is the largest single piece of unbuilt work in the repo.

### Lineage is measured, not copied

`icons-inspiration/` holds 1,185 flattened SVGs (583 at 16, 602 at 24). Every
number in the construction spec was derived from that corpus by measurement —
ray-cast thickness, radial silhouette comparison, arc fitting — and where the
corpus is internally inconsistent the spec says so and names the dominant
behaviour as the rule.

This is the difference between a house style and a copy. We are reproducing the
*system* the corpus implies, not its individual drawings.

### Parametric, not hand-drawn

Geometry is a function of stroke width `W` in [`../tools/generate.py`](../tools/generate.py).
Clearances are not round numbers that happen to work — they are the floor
`gap ≥ 1 × stroke` solved exactly at `W = 2`. Change the stroke alone and every
clearance collapses, which is why a weight axis is a geometry axis and why a
one-off drawing at `W = 2` is a dead end.

**A hand-drawn SVG is not an icon in this system.** It is a sketch of one.

---

## 2. Two audiences, two artifacts

This is the split that makes the system usable, and the one most likely to get
blurred.

| Audience | Wants | Artifact | Form |
|---|---|---|---|
| **Humans & future sessions** | the target and the build rules | this file · [`icon-construction-spec.md`](icon-construction-spec.md) · [`decisions.md`](decisions.md) | prose |
| **AI at use time** | *which icon do I reach for* | [`../data/icon-rules.json`](../data/icon-rules.json) | structured |
| **Either, mechanically** | the numbers | [`../data/construction-tokens.json`](../data/construction-tokens.json) | structured |

The second row is the one people skip. An AI choosing an icon does not need to
know the corner radius — it needs to know that **kebab is row-scoped and
hamburger is view-scoped**, that **circled-X dismisses while plain X closes**,
and that **a warning ships filled**. That is selection context, it is per-icon,
and prose cannot be queried. It goes in `icon-rules.json`.

Keep them apart. Construction facts drifting into the rules file, or selection
guidance drifting into the spec, is how both stop being trusted.

---

## 3. Line is the default; fill is emphasis

The most-misused axis, so it gets stated here rather than buried.

**Assume line.** Almost every icon in almost every surface is a line icon — a
toolbar, a nav at rest, a list of amenities, a form. Line is not the weak option;
it is the normal one.

**Reach for fill when the icon has to carry more weight than the words around
it.** Three cases, in order of how often they come up:

1. **Status and severity.** Warning, error, success, info in a banner or an
   alert. These are the one family where the icon has to be read *before* the
   sentence beside it, and a line glyph does not win that race. `warning-fill`,
   `close-circle-fill`, `check-circle-fill`, `info-fill`.
2. **The selected item.** The current tab, the active filter, the marker for
   *this* place. Fill is the strongest emphasis step the system has, so it is
   also what a selected state gets.
3. **Anything that is losing at a glance.** A dense surface where line is
   disappearing. This is a judgement call and should be rare — if it is not
   rare, the surface is too dense.

**Nothing sits in between.** No intermediate fill values, no weight axis, no
grade axis in the shipped set. Switching is a swap, not a dial.

**Not every icon has a fill, and that is not an oversight.** Two reasons an icon
is line-only:

- Nothing in any product ever needs to emphasise it. Map chrome is always a
  button — `map`, `layers`, `route`, `compass`.
- It has no interior to flood. An icon built entirely from open strokes returns
  itself when you try to fill it, and a fill identical to its line variant is a
  bug the spec already names. `picnic-table`, `chart`, `signal`, `activity`.

**Construction is unaffected by any of this.** How a fill is *drawn* — never
exceeding the line variant's outer edge, carrying roughly the same total ink,
spending its extra mass on counters rather than area — is measured and settled
in the spec. This section is only about *when to reach for one*.

---

## 4. Scope: who may use an icon

Three tiers. The README's original model was binary; the travel pack forced the
middle one.

| Scope | Meaning | Example |
|---|---|---|
| `generic` | universal — any product, any context | `close`, `search`, `chevron-right` |
| `travel` | generic **within a domain**, opt-in at import | `campsite`, `ev-charger`, `trailer` |
| `product` | one product, cannot be repurposed | *(none yet)* |

`travel` exists because `campground` is not universal — it would be noise in a
CRM — but it is not Roadtrip-specific either. Any travel, mapping or booking
product wants exactly that set. Scoping all of it to `roadtrip` would mean the
second travel product redraws it, which is the redundancy this repo exists to
prevent.

> **Open:** the `travel` scope is recommended and in use in the rules file, but
> has never been ratified, and nothing enforces it at import. See
> [`decisions.md`](decisions.md).

---

## 5. How a new icon enters the library

Product need is the forcing function. Roadtrip is the current one. The path:

1. **Name the gap against the existing set first.** Most "missing" icons are
   present under another name. The travel-pack audit found UI chrome ~95%
   already covered; the real gap was two clusters, not 34 drawings.
2. **Size the work as primitives, not drawings.** If three icons share a form,
   that form is a primitive in `generate.py` and the icons fall out of it. This
   is also the only way to keep new work on the weight axis.
3. **Pick a keyline, draw the skeleton.** Everything else is derived — stroke,
   terminals, clearances, how the fill differs. Spec §11 is the checklist.
4. **Verify by measurement.** Bounding box against its keyline, clearance
   between every pair of forms, largest-inscribed-disc for every counter, and
   the fill/line footprint and ink ratio. Numbers, not eyeballs.
5. **Then look at it.** Measured-correct and looks-right are not the same
   claim, and this repo has already had a round where the numbers passed and the
   drawing did not.
6. **Add a selection entry** if the new icon is confusable with an existing one.
   If it is not confusable with anything, it does not need an entry.
7. **Record the decision** if the work ruled something out.

### The tests something must pass to be a decision

Borrowed wholesale from LDS, because it works: **an entry is only a decision if
it names what it ruled out.** "The grid is 24" is a fact and belongs in the
README. "We chose a canopy over a conifer for `park`, because two tiers close at
`W`" is a decision. Facts go in READMEs; decisions go in
[`decisions.md`](decisions.md).

---

## 6. Where everything lives

```
CLAUDE.md                        always in context — the pointer and the traps
README.md                        what the project is; facts about the system
docs/
  principles.md                  the ten, in plain language — start here
  north-star.md                  ← you are here: the target
  icon-construction-spec.md      how icons are drawn (measured, 734 lines)
  decisions.md                   why the system is shaped this way
  proposal-travel-outdoors-pack.md   the Roadtrip forcing function
  facilities-pack-status.md      what shipped and what is blocked
data/
  construction-tokens.json       the spec, queryable
  icon-rules.json                selection context, queryable
  icon-metadata.json             per-icon: description, keywords, aliases, RTL
  measured-symmetry.json         derived input — which icons a mirror cannot change
tools/
  generate.py                    the geometry — the actual source of truth
  export.py                      writes icons/ from it
  icon-lint.py                   scores the INSPIRATION corpus (see CLAUDE.md)
icons/                           generated output — never hand-edit
icons-inspiration/               the 1,185-file reference corpus
```

---

## 7. What "done" looks like

Not a fixed icon count. Four conditions:

1. **Both sizes exist as masters.** 24 and 16, each drawn on its own keyline.
2. **Every state-carrying icon has its fill**, and no icon has a fill it cannot
   justify.
3. **Every confusable cluster has a selection entry**, so an AI picking an icon
   is choosing rather than guessing.
4. **The decision record explains the set to someone who wasn't here** — enough
   that a settled question doesn't get re-opened by accident.

The set is finished when a new product need is answered by *composing what
exists* more often than by drawing something new.
