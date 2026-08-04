# What other icon systems do — and what it means for adoption

Research pass over seven shipping icon systems, read against the five questions
that decide whether anyone can actually *use* this library: what belongs in it,
what things are called, how they change, how consumers migrate, and what it
costs a team to adopt.

**Surveyed:** Material Symbols (Google) · Polaris (Shopify) · Octicons (GitHub
Primer) · Atlassian Design System · Fluent UI System Icons (Microsoft) ·
SF Symbols (Apple) · Carbon (IBM). Sources at the foot.

**The short version.** Open Icons is ahead of all of them on one axis and behind
all of them on another. The construction rules and the machine-readable
*selection* context are genuinely unusual — none of the seven ships anything
like `icon-rules.json`. But every one of them solves distribution, metadata,
deprecation and migration, and Open Icons currently solves none of those. An
outside team adopting this library today would have to build all four themselves.

---

## 1. What belongs in the library

The published criteria converge hard, and two of them are already principles
here.

**Polaris** states three: clear, consistent, universal. Its *forbidden* list is
the interesting half — excessive ornamentation, reinterpreting well-established
icons, and relying on **"cultural-specific, niche, or outdated metaphors."**
That last one is the culture principle, published by a major system, and it
supports treating locale semantics as a gate rather than a nice-to-have.

**Octicons** frames acceptance as four review questions, and they read almost
exactly like our contribution model:

- Where will this icon be used in the context of the UI?
- **Is an icon necessary in that context?**
- Could we use an existing icon?
- Is the icon trying to represent too many ideas?

Question two is principle 1 ("sometimes the answer is a word") asked at intake
rather than left to the requester's judgement. Worth stealing: make it a
required field on the request, not a norm.

**Atlassian** is the cautionary tale. Their legacy set reached 350+ icons with
**over 1,000 more custom icons scattered across product teams** — duplication
that happened precisely because there was no sanctioned way to contribute. Their
answer was not a stricter gate but **Icon Lab**: a contribution repo with a Figma
plugin that automates layout and export, which has since absorbed 275+
community icons. The lesson is that a library with no contribution valve does
not stay small; it just stops being the place the icons live.

> **For us:** the intake questions belong in the request template. And the
> "nineteen in twenty requests end at step 3" claim in our contribution model
> should be measured rather than asserted, because Atlassian's numbers suggest
> the failure mode is people routing *around* the library, which never shows up
> in request stats.

---

## 2. Naming

Four distinct conventions, and they answer different problems.

| System | Convention | What it buys |
|---|---|---|
| **Polaris** | `{Name}Icon.svg`, PascalCase, mandatory `Icon` suffix | No collision with component names in code |
| **Octicons** | Same — v10 renamed every component `Alert` → `AlertIcon` | Same, and they took the breaking change to get it |
| **Carbon** | kebab-case, single hyphen | URL- and filename-clean |
| **Atlassian** | **Two categories** — see below | Tells you *how much meaning* the name carries |
| **SF Symbols** | Direction words encode behaviour — see below | Makes RTL correctness a naming decision |

### The two best ideas

**Atlassian splits names by purpose.** Single-purpose icons get **semantic**
names describing the job — "Share", "Work item". Multi-purpose icons get
**literal** names describing the drawing — "arrow right", "globe". A name tells
you whether it is bound to one meaning or open to many.

That is the same distinction as our principle 6 (the library holds the drawing;
the product binds the meaning) — arrived at independently, and expressed in the
place a developer actually looks. Our set already does this by accident:
`chevron-right` and `circle` are literal, `campsite` and `restroom-figures` are
semantic. It has never been written down, so nothing stops the next icon
breaking the pattern.

**Apple encodes mirroring in the name.** SF Symbols uses `left`/`right` for
symbols that must **not** flip in right-to-left locales, and
`leading`/`trailing`/`forward`/`backward` for those that **must**. The
convention is the documentation: you cannot pick the wrong one without noticing.

This is a direct answer to the open RTL question across our 53 directional
icons — with one problem. Our names already shipped as `arrow-left`,
`chevron-right`, `skip-forward`. Renaming them is a breaking change for a set
that has no deprecation machinery yet, which is a good argument for building
that machinery before it is needed rather than after.

### Metadata is where the real gap is

**Polaris requires a YAML sidecar per icon**: name, description, keywords,
authors, `date_added`, `date_modified`. **Fluent ships a `directionType` field**
with values `unique` (separate LTR and RTL drawings) or `mirror` (flip it).

Open Icons has **no per-icon metadata at all** — just `names.json`, a flat list.
Everything downstream that teams expect is blocked on it: search by keyword, a
Figma library with descriptions, "what changed since v2", deprecation pointers,
and RTL correctness.

---

## 3. Updating and deprecating

**Polaris is the most complete published process**, and it is small enough to
copy:

1. Announce the deprecation and publish the migration **a month before** the
   next major release.
2. Warn in three places: docs (with the reason, the alternative, and the
   migration), a `console.warn` in development builds, and a `@deprecated`
   JSDoc tag with the replacement named.
3. Remove in the **next major version** — never in a minor.
4. Ship a **codemod** (`polaris-migrator`) so the migration is a command, not a
   chore.

**Atlassian** ran the same shape over a longer arc: deprecation notice in 2024,
legacy entry points **permanently removed** later, with the removed paths listed
explicitly so a failing build tells you exactly what to change.

**Octicons** used a major version (v10) to absorb several breaking changes at
once — the `Icon` suffix rename, dropping `width`/`height` props for a `size`
prop, and removing lookup exports to enable tree-shaking. Batching breaking
changes into one major is cheaper for consumers than dribbling them out.

> **For us:** Open Icons has **no version number, no deprecation policy, and no
> alias mechanism** — the last one is already a recorded open question, since
> `zoom-in`/`zoom-out` should be aliases of `search-add`/`search-minus` and
> `export.py` has nowhere to put them. All three are the same missing feature:
> a name can currently only ever mean one thing forever.

---

## 4. Migration — the strongest evidence in the survey

**Atlassian's icon migration is the best-documented example anywhere**, and the
numbers are the useful part:

- A **manual mapping** of the 350 legacy icons to their replacements.
- An **ESLint rule with an auto-fixer** built on that mapping, which migrated
  **roughly 75% safely** — the rest needed a human.
- An **"icon facade"** that allowed runtime swapping with no code change at all,
  so the visual change could ship independently of the code migration.
- **Feature flags** for gradual rollout.
- A custom **SVG extractor** to audit what legacy icons were actually in use.
- Applied across **16,000+ call sites**.

Three things to take from that:

1. **The mapping table is the deliverable.** The tooling is mechanical once the
   old→new mapping exists; the mapping is the part only a human can do.
2. **75% is the realistic ceiling for automation**, and the missing 25% is
   exactly our principle 6 — meaning does not map one-to-one, so a machine
   cannot decide whether an old "remove" becomes an X, a minus or a trash can.
   That is a product decision, and it is what the product manifest is for.
3. **A facade decouples the visual change from the code change.** For a team
   adopting Open Icons over an existing set, this is the difference between a
   quarter-long project and an afternoon.

---

## 5. Adoption effort — the question that matters

What a team must do to start using each library.

| System | Web | iOS | Android | Figma | Other |
|---|---|---|---|---|---|
| **Material Symbols** | Variable font (Google Fonts API or self-hosted WOFF2), SVG | TTF into Xcode, `UIFont`/`UIFontDescriptor` for axes | VectorDrawable XML, per-density | Official plugin | Flutter, PNG |
| **Fluent** | SVG, fonts | CocoaPods, Carthage | Maven Central | — | Flutter via pub |
| **Octicons** | npm, React, Styled System | — | — | — | Ruby, Jekyll |
| **Carbon** | `@carbon/icons-react`; community Angular, Svelte, Vue | — | — | Community file | — |
| **Polaris** | `@shopify/polaris-icons` (SVG + React) | — | — | Library | — |
| **SF Symbols** | ✗ | System font, app | ✗ | — | Apple platforms only |
| **Open Icons** | **SVG files + `icons.json`** | ✗ | ✗ | ✗ | ✗ |

### The variable-font lesson

Material's headline trick is that **one ~300 kB variable font file replaces
thousands of SVG variants**, with fill, weight, grade and optical size as live
CSS axes. It is the single biggest reduction in adoption cost in the survey: one
asset, four dials, every platform that can load a font.

**Open Icons is unusually well-placed to do this and nobody has noticed.** The
set is not a folder of drawings — it is a *function of stroke width*, which is
precisely what a variable font's weight axis is. Everything needed to emit one
already exists in `generate.py`; the axis is already carried from 1.0 to 2.5.
The generator is the asset, and the distribution layer is the missing half.

### What an adopting team faces today

Honestly assessed:

| Consumer | Effort now | Blocker |
|---|---|---|
| **Web, hand-rolled** | Low | None — `icons.json` is usable today |
| **Web, framework** | Medium | No npm package, no components, no tree-shaking |
| **Figma** | **High** | 216 SVGs imported and named by hand, no descriptions, no library |
| **iOS** | **High** | Nothing exists. Manual conversion per icon |
| **Android** | **High** | No VectorDrawable output |
| **Migrating from another set** | **Very high** | No mapping table, no codemod, no facade |
| **An AI choosing icons** | **Low — and best in class** | `icon-rules.json` has no equivalent anywhere in the survey |

That last row is worth stating plainly. Polaris ships keywords. Fluent ships
`directionType`. Nobody ships *when to reach for this one instead of that one* —
the cluster tiebreakers, the fill rule, the cultural hazards, the product
bindings. If the pitch for this library is "an icon system an AI can use
correctly", that is already true and already differentiated. What is not true
yet is "an icon system a team can install."

---

## Recommendations, ordered by adoption impact

1. **Per-icon metadata.** One sidecar (or one JSON) carrying: description,
   keywords/aliases, `directionType` (Fluent's `mirror` | `unique` | `none`),
   `status` (`stable` | `deprecated`), `deprecated_by`, `since`. This one file
   unblocks search, Figma, deprecation, aliases and RTL simultaneously. It is
   the highest-leverage thing on this list by a wide margin.
2. **A version number and a deprecation policy**, copied from Polaris: announce
   a major ahead, warn in docs and in code, remove only in a major, ship a
   codemod. Build it before the first rename, not after.
3. **Write down the naming convention that already exists** — literal names for
   multi-purpose icons, semantic names for single-purpose ones (Atlassian's
   split). Then decide whether directional icons adopt Apple's
   `leading`/`trailing`, knowing it is a breaking change.
4. **Emit more formats from the generator.** Ordered by cost-to-value: an npm
   package with tree-shakeable components, an SVG sprite, a Figma-importable
   file, then Android VectorDrawable and an iOS asset catalog. A variable font
   is the ambitious one and the one this architecture is uniquely suited to.
5. **A migration kit**, when there is a first external adopter: the mapping
   table first, then the codemod, then the facade. Expect 75% automation and
   plan for the 25%.

None of this changes a single icon. All of it changes whether anyone else can
use them.

---

## Sources

- [Polaris icons — contributing](https://github.com/Shopify/polaris-react/blob/main/polaris-icons/CONTRIBUTING.md)
- [Polaris — icon design guidelines](https://polaris-react.shopify.com/design/icons)
- [Polaris — deprecation guidelines](https://github.com/Shopify/polaris-react/blob/main/documentation/Deprecation%20guidelines.md)
- [Material Design Icons / Symbols](https://github.com/google/material-design-icons)
- [Material Icons & Symbols guide](https://developers.google.com/fonts/docs/material_icons)
- [Octicons — design guidelines](https://primer.github.io/octicons/guidelines/design/)
- [Octicons v10 release notes](https://github.com/primer/octicons/releases/tag/v10.0.0)
- [Atlassian — building the new icon system](https://www.atlassian.com/blog/design/behind-the-screens-building-atlassians-new-icon-system)
- [Atlassian — legacy icon deprecation and migration timeline](https://community.developer.atlassian.com/t/questions-regarding-legacy-icon-deprecation-and-migration-timeline/95618)
- [Fluent UI System Icons](https://github.com/microsoft/fluentui-system-icons)
- [Apple HIG — SF Symbols](https://developers.apple.com/design/human-interface-guidelines/foundations/sf-symbols)
- [Apple HIG — Icons](https://developers.apple.com/design/human-interface-guidelines/foundations/icons)
- [Carbon Design System — icons usage](https://carbondesignsystem.com/elements/icons/usage/)
- [Carbon monorepo](https://github.com/carbon-design-system/carbon)
