# Open Icons Playground

> A React-based design tool for exploring, testing, and governing a scalable icon system.

**Live Demo:** [matthewlew.github.io/open-icons](https://matthewlew.github.io/open-icons/)

---

## 🧭 Start here

| If you want | Read |
|---|---|
| **The ten principles** — start here, no measurements, anyone can read it | **[`docs/principles.md`](./docs/principles.md)** |
| **The target** — what we are building and how something gets in | [`docs/north-star.md`](./docs/north-star.md) |
| **Why the system is shaped this way** | [`docs/decisions.md`](./docs/decisions.md) |
| **How an icon is drawn** | [`docs/icon-construction-spec.md`](./docs/icon-construction-spec.md) · [`data/construction-tokens.json`](./data/construction-tokens.json) |
| **Which icon to reach for, cultural hazards, product bindings** | [`data/icon-rules.json`](./data/icon-rules.json) |
| **Per-icon description, keywords, aliases, RTL behaviour, status** | [`data/icon-metadata.json`](./data/icon-metadata.json) |
| **The traps that fail quietly** | [`CLAUDE.md`](./CLAUDE.md) |
| **How other systems do this, and what adoption costs** | [`docs/research-icon-systems.md`](./docs/research-icon-systems.md) |

This README is the **facts** about the project. Anything that ruled an
alternative out is a decision and lives in `decisions.md` instead.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Goals of the Project](#goals-of-the-project)
- [Repository Structure](#repository-structure)
- [Icon System Philosophy](#icon-system-philosophy)
- [Icon Variant System](#icon-variant-system)
- [North Star](#-start-here)
- [Construction Spec](#-construction-spec)
- [Encoding Design Knowledge](#encoding-design-knowledge)
- [Playground UI](#playground-ui)
- [Changelog Philosophy](#changelog-philosophy)
- [Example Change Entry](#example-change-entry)
- [AI Contribution Guidelines](#ai-contribution-guidelines)
- [Future Goals](#future-goals)
- [Contribution Guide](#contribution-guide)
- [License](#license)

---

## 🎯 Project Overview

**Open Icons Playground** is an interactive design tool built to:

- **Explore** an internal icon set with real-time previews
- **Test** icon variants (weights, styles, fills) across different contexts
- **Establish** clear usage rules and governance principles
- **Simplify** the icon library by identifying redundancy and consolidation opportunities
- **Embed** design knowledge directly into the system for humans and AI tools

This project serves:
- **Designers** — visual exploration and testing of icon consistency
- **Developers** — structured data and variant APIs
- **AI Design Tools** — machine-readable rules for icon selection and governance

---

## 🚀 Goals of the Project

The Open Icons Playground was created to solve key challenges in icon system management:

### Core Motivations

1. **Reduce Icon Redundancy**  
   Consolidate duplicate or overly similar icons to maintain a lean, focused library.

2. **Standardize Icon Usage**  
   Prevent misuse by documenting when and where specific icons should be used.

3. **Prevent Product-Specific Icon Misuse**  
   Clearly distinguish between generic icons (usable anywhere) and product-scoped icons (restricted to specific contexts).

4. **Create a Testbed for Variants**  
   Enable rapid prototyping of icon weights, fills, and styles to validate design decisions.

5. **Make Icon Governance Easier**  
   Provide a centralized system for tracking changes, deprecations, and design rationale.

### Key Questions This Tool Helps Answer

- **How can we simplify the icon set?**  
  Identify redundant icons and consolidation opportunities.

- **When should a generic icon vs product icon be used?**  
  Enforce scoping rules to prevent cross-product contamination.

- **How should designers override icons?**  
  Allow context-specific customization while maintaining system integrity.

- **How can company design knowledge be encoded into the system?**  
  Transform tribal knowledge into machine-readable rules.

---

## 📂 Repository Structure

```
open-icons-playground/
├── tools/
│   ├── generate.py               # THE SOURCE OF TRUTH — geometry as a function of W
│   ├── export.py                 # writes the set at a given weight
│   ├── build-icon-rules.py       # writes + validates data/icon-rules.json
│   ├── build-icon-metadata.py    # writes + validates data/icon-metadata.json
│   ├── site.py                   # builds site/index.html (all four weights embedded)
│   └── icon-lint.py              # scores SVGs against the construction spec
├── icons/                        # generated — do not hand-edit
│   ├── 24/<name>.svg             # 216 standalone files
│   ├── icons.json                # {grid, stroke, icons: {name: innerMarkup}}
│   └── names.json
├── site/
│   ├── template.html             # the site, with one @@DATA@@ placeholder
│   └── index.html                # generated — the whole site in one file
├── docs/
│   ├── north-star.md             # THE TARGET — read first
│   ├── decisions.md              # why the system is shaped this way
│   └── icon-construction-spec.md # the derivation, with counts behind every claim
├── data/
│   ├── construction-tokens.json  # machine-readable form of the spec
│   ├── icon-metadata.json        # per-icon: description, keywords, aliases, RTL
│   └── icon-rules.json           # machine-readable selection context
└── icons-inspiration/            # the 1,185 reference SVGs the spec was measured from
```

### Folder Responsibilities

| Folder | Purpose |
|--------|--------|
| `tools/` | The generator, the exporters, and the conformance linter |
| `icons/` | The built set. Regenerate rather than edit. |
| `site/` | The library's own site — gallery, rationale, changelog, proposals |
| `data/` | Structured metadata and governance rules |
| `docs/` | The target, the decision record, and the derivations |

### Rebuilding

```bash
python3 tools/export.py icons 2.0    # the set, at stroke 2.0
python3 tools/site.py                # the site, at every weight on the axis
```

**The weight is an argument, not a build target.** There is no single built set;
there is a generator and an axis. See [§ Icon System Philosophy](#-icon-system-philosophy).

---

## 🌐 The site

**`site/index.html`** is the library's front door, and it is self-contained: no build
step, no CDN, no server. Open it in a browser.

| Page | What it holds |
|---|---|
| The set | All 216 icons, with the weight, size, style, ground and keylines all live |
| What's different | Five claims about this set, each with a count behind it |
| Anatomy | How one of these is actually built, in the order you would need it |
| Changelog | Problem → decision → **what was tried first and thrown away** |
| Roadmap | What is next, what is parked, and the proposal composer |
| Use it | Three ways in, and the one rule (the stroke is not a CSS knob) |

The gallery has an **A/B mode**: every icon rendered twice, once re-derived at the
chosen weight and once as the 2.0 drawing with `stroke-width` overridden. At weight
2.0 the two are identical, which is the point — the axis is anchored there.

---

## 📐 Construction Spec

**→ [`docs/icon-construction-spec.md`](./docs/icon-construction-spec.md)** — how the icons are
actually built, derived by measuring all 1,185 flattened SVGs in `icons-inspiration/`.
Machine-readable equivalent: [`data/construction-tokens.json`](./data/construction-tokens.json).

The short version:

| Rule | Value |
|---|---|
| Stroke width | **2** — at 16px *and* 24px, every curve, every angle |
| Live area | 20×20 in a 24px box; **16×16 in a 16px box (no padding)** |
| Keylines | circle = live area · square = −2 · rects = −4 · diagonal = −6 |
| 16 → 24 | canvas ×1.5, glyph ×**1.25**, stroke ×**1.0** — never scale a master |
| Terminals | round cap on free ends, butt where a stroke meets another form |
| Fill variant | **never** exceeds the line variant's outer edge (0 of 378 pairs do) |
| Container fills | solid at the same radius, line glyph reused **verbatim** as a knockout |
| Figure fills | solid at outer − 0.5, contact datum pinned |
| Counters | grow on the flip to knockout: +0.25 at 24px, +0.125 at 16px. Never shrink. |
| Clearance | 2 by default; 1 only to say "one body with a seam" |

---

## 🎨 Icon System Philosophy

The Open Icons system is built on clear, enforceable principles:

### Core Principles

1. **Icons Should Be Generic by Default**  
   Base icons represent universal concepts (e.g., `search`, `close`, `add`) and can be used across any product.

2. **Product Icons Must Be Scoped**  
   Icons tied to specific products (e.g., `analytics-dashboard-icon`) cannot be repurposed generically.

3. **Visual Consistency is Required**  
   Icons must align with stroke weight, corner radius, and endpoint styles defined in the system.

4. **Duplicate Icons Should Be Consolidated**  
   Multiple icons serving the same purpose create confusion and bloat.

### Icon Classification

| Type | Definition | Example |
|------|------------|--------|
| **Generic** | Universal, reusable across all contexts | `document`, `share`, `close` |
| **Product** | Scoped to a specific product or feature | `analytics-chart`, `crm-contact` |
| **Custom** | Context-specific overrides of generic icons | `search-advanced` (replaces `search` in specific UI) |
| **Deprecated** | Marked for removal, should not be used | `old-arrow-left` → use `arrow-left` |

---

## 🔀 Icon Variant System

The playground supports multiple visual variants per icon to enable flexible design:

### Supported Variants

| Variant | Description | Use Case |
|---------|-------------|----------|
| **Default** | Base icon, generic usage | Standard UI elements |
| **Outlined** | Stroke-only, no fill | Minimal, light themes |
| **Filled** | Solid fill, no stroke | Bold, emphasis states |
| **Brand** | Company-specific styling | Marketing, branded contexts |
| **Custom** | Context-specific override | Product-specific adaptations |

### Override Philosophy

The system allows **custom icons** to replace **default icons** in specific product contexts:

```json
{
  "search": {
    "default": "generic-search.svg",
    "custom": {
      "product-x": "advanced-search.svg"
    }
  }
}
```

This approach maintains **flexibility** (products can adapt icons when needed) while **preventing misuse** (custom icons don't leak into other products).

---

## 🧠 Encoding Design Knowledge

One of the project's core goals is to transform **tribal design knowledge** into **machine-readable rules** that AI tools can understand.

### Why Encode Rules?

Without structured rules:
- Designers repeat the same questions
- AI tools make incorrect icon suggestions
- Inconsistencies creep into products over time

### The rules file

**→ [`data/icon-rules.json`](./data/icon-rules.json)** — the selection layer, generated by
[`tools/build-icon-rules.py`](./tools/build-icon-rules.py) and validated against
`icons/names.json` at build time.

It answers *which icon do I reach for*, not *what does this icon look like*. Keyed by icon
name, with a per-cluster tiebreaker naming the single axis that separates the members:

```json
"more-vertical": {
  "cluster": "menu-affordance",
  "scope": "generic",
  "use_when": "Row-level or card-level overflow. The kebab: actions that apply to the one thing it sits beside.",
  "not_when": "Not for view-wide navigation, and not when there is horizontal room to show the actions outright.",
  "instead_use": { "menu": "the target is the whole view" },
  "confusable_with": ["list", "menu", "more-horizontal"],
  "has_fill": false
}
```

Coverage is **confusable clusters only** — 39 icons across 12 clusters. An entry earns its
place by naming what it rules out; absence means unambiguous, not undocumented. Global blocks
cover `fill_axis` (fill is a state, never a style), `container_shape` (bare vs circled vs
squared) and `scopes`.

### Benefits

✅ **AI tools** can avoid suggesting incorrect icons  
✅ **Designers** get instant feedback on icon usage  
✅ **Documentation** stays synchronized with the system

---

## 🖼️ Playground UI

The playground interface provides real-time visual testing:

### Key Features

- **Icon Browsing** — Grid view of all icons with search/filter
- **Variant Preview** — Live comparison of weights, fills, and styles
- **Override Testing** — Simulate product-specific icon replacements
- **Relationship Exploration** — Visualize which icons are related or redundant
- **Deprecation Review** — Highlight icons marked for removal

### How Designers Use It

1. **Evaluate simplification opportunities** — Are two icons too similar?
2. **Test variant consistency** — Do all icons look cohesive at different weights?
3. **Validate new icons** — Does a proposed icon fit the system?
4. **Document decisions** — Add rationale directly in the tool

---

## 📖 Changelog Philosophy

Traditional changelogs list technical changes. This project uses **Design Change Logs** to document **why** decisions were made.

### What's Different?

Each change entry includes:

| Field | Purpose |
|-------|--------|
| **Problem** | What design issue existed? |
| **Decision** | How was it solved? |
| **Before / After** | Visual comparison |
| **Impact** | How does this affect designers? |

### Why This Matters

- **Humans** understand the reasoning, not just the result
- **AI tools** can learn from past decisions
- **Design blog posts** can be generated automatically

---

## 📝 Example Change Entry

### ✅ Simplified Navigation Icons

**Problem:**  
Too many arrow variants existed (`arrow-left`, `chevron-left`, `caret-left`, `back-arrow`), causing confusion about which to use.

**Decision:**  
Consolidated into **three directional arrows**:
- `arrow-left` / `arrow-right` — Navigation actions
- `chevron-right` — Expanding/collapsing menus
- `arrow-up` / `arrow-down` — Vertical movement

**Before:**
- 12 arrow-like icons with unclear distinctions

**After:**
- 5 clear, purposeful arrows

**Impact:**  
Reduces ambiguity and simplifies design decisions. Designers no longer need to guess which arrow to use.

**Deprecations:**
- ~~`caret-left`~~ → use `chevron-right`
- ~~`back-arrow`~~ → use `arrow-left`

---

## 🤖 AI Contribution Guidelines

AI assistants (like Claude, GPT, or design copilots) are encouraged to contribute, following these guidelines:

### What AI Should Do

✅ **Propose icon simplifications** — Flag redundant or overly similar icons  
✅ **Identify duplicates** — Suggest consolidation opportunities  
✅ **Recommend clearer naming** — Improve icon discoverability  
✅ **Update rules** — Suggest new governance rules based on usage patterns  
✅ **Document rationale** — Explain why a change improves the system

### What AI Should NOT Do

❌ **Delete icons without deprecation steps** — Always mark for deprecation first  
❌ **Introduce product-specific icons as generic** — Respect scoping rules  
❌ **Bypass governance rules** — Changes must align with icon philosophy  
❌ **Make breaking changes without impact analysis** — Consider downstream effects

### How AI Should Treat This Repository

This is a **design knowledge base**, not just code:
- Rules should be learned and applied
- Past decisions inform future suggestions
- Governance principles take priority over personal preference

---

## 🔮 Future Goals

### Short-Term
- [ ] Add `data/icons.json` with full icon metadata
- [ ] Implement icon search and filtering in UI
- [x] Create `data/icon-rules.json` with initial governance rules

### Medium-Term
- [ ] **Automated icon linting** — Flag rule violations in CI/CD
- [ ] **Figma plugin integration** — Sync icons between Figma and code
- [ ] **AI-assisted icon selection** — Suggest the right icon based on context

### Long-Term
- [ ] **Design rule enforcement** — Prevent incorrect icon usage at compile time
- [ ] **Visual regression testing** — Ensure icons remain pixel-perfect across updates
- [ ] **Cross-platform icon generation** — Export to iOS, Android, Web

---

## 🤝 Contribution Guide

We welcome contributions that improve the icon system. Follow these steps:

### How to Contribute

1. **Identify a Problem**  
   What design issue exists? (e.g., "Too many similar search icons")

2. **Propose a Solution**  
   How should it be fixed? (e.g., "Consolidate into one search icon with variants")

3. **Document Reasoning**  
   Why is this better? What's the design rationale?

4. **Update Icon Rules** (if applicable)  
   Add or modify `data/icon-rules.json` to reflect the change.

5. **Add Changelog Entry**  
   Add an entry to the Changelog view in `site/template.html`, using the format
   above. Include what you tried first and rejected — that is the expensive part,
   and losing it means someone re-derives it in six months.

6. **Open a Pull Request**  
   Include before/after visuals and impact analysis.

### Review Criteria

Contributions are evaluated based on:
- Alignment with icon system philosophy
- Clarity of design rationale
- Impact on existing designs
- AI/human readability of documentation

---

## 📜 License

MIT License — Free to use, modify, and distribute.

See [LICENSE](./LICENSE) for full details.

---

## 🙌 Acknowledgments

Built with:
- [React](https://react.dev) — UI framework
- [Vite](https://vitejs.dev) — Build tool
- [GitHub Pages](https://pages.github.com) — Deployment platform

Inspired by design systems from Google Material, Apple SF Symbols, and Figma Icons.

---

**Questions?** Open an issue or start a discussion. This project thrives on thoughtful design contributions. 🎨
