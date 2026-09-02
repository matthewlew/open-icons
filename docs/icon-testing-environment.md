# Icon Testing & Visual QA Environment Specification

This specification defines the automated and interactive visual QA testing suite required when creating, editing, or validating icons. It ensures that every icon is legible, optically balanced, system-aligned, and resilient under adverse display conditions.

---

## 1. Overview & Architecture

When building the icon editing environment and preview toolchain, the system must provide an **Icon Testing Environment** with dedicated testing modules:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ICON TESTING ENVIRONMENT                        │
├───────────────────┬────────────────────┬───────────────────────────────┤
│ 1. Resemblance    │ 2. Optical Balance │ 3. Affordance & Obstruction   │
│    - 5×5 Matrix   │    - ±90° Rotation │    - 45° Slash Knockout       │
│    - Line & Fill  │    - H / V Flips   │    - 4-Corner Badges          │
│    - Light & Dark │    - Center Check  │    - Low Vision (Blur)        │
├───────────────────┴────────────────────┴───────────────────────────────┤
│ 4. Colorization & Contrast             │ 5. Multi-Scale Ladder         │
│    - Default (Light)                   │    - 24px: 200%, 150%, 100%   │
│    - Inverted (Dark)                   │    - 16px: 100%, 75%, 62%, 50%│
└────────────────────────────────────────┴───────────────────────────────┘
```

---

## 2. Test Suites Specification

### Suite 1: Resemblance (System Cohesion)
**Goal:** Verify that the candidate icon looks harmonious and shares identical optical weight with existing system icons.

* **Test Matrices (5×5 Grids)**:
  1. **Large Line Icons (24px)**: Candidate placed in a 5×5 grid alongside 24 peer icons on default (light) background.
  2. **Small Line Icons (16px)**: Candidate placed in a 5×5 grid alongside 24 peer icons on default (light) background.
  3. **Large Fill Icons (24px)**: Candidate placed in a 5×5 grid alongside 24 peer icons on inverted (dark) background.
  4. **Small Fill Icons (16px)**: Candidate placed in a 5×5 grid alongside 24 peer icons on inverted (dark) background.

* **Standard Benchmark Archetype Set (24 Keyline Peers)**:
  To provide consistent and reproducible baseline QA, the 5×5 matrix uses a curated benchmark set representing all primary keylines and visual densities:
  - **Circle / Round**: `info`, `check-circle`, `settings/gear`, `user`, `clock`
  - **Square / Bounding Box**: `image`, `apps/grid`, `store/shop`, `briefcase`, `camera`
  - **Horizontal Rectangle**: `credit-card`, `mail/envelope`, `desktop/screen`
  - **Vertical Rectangle**: `bookmark`, `mobile/phone`, `document`
  - **45° Diagonal / Cross / Dynamic**: `arrow-left`, `send/paper-plane`, `share/export`, `plus`, `close`, `tag`, `sparkle/ai`, `slash/eye-off`, `utensils`, `home`

* **Sampling Modes in Testing Environment**:
  1. **Canonical Benchmark (Default)**: Fixed 24 archetype icons for standardized QA comparisons.
  2. **Random System Sample**: Shuffled 24 random icons drawn live from the `icons/` repository to test against arbitrary neighbours.
  3. **Category-Specific**: Filtered peer set (e.g. Navigation, Commerce, Actions, Communication) for domain-focused checks.

* **Pass Criteria**: Candidate does not pop out as excessively bold, faint, overly dense, or sparse compared to neighboring glyphs.


---

### Suite 2: Optical Alignment & Balance (Rotations & Flips)
**Goal:** Eliminate semantic bias to expose true visual mass and optical centering.

* **Transformations**:
  1. **Rotated -90°** (Counter-Clockwise)
  2. **Rotated +90°** (Clockwise)
  3. **Horizontally Flipped** (Mirror X-axis)
  4. **Vertically Flipped** (Mirror Y-axis)
* **Pass Criteria**: The icon does not feel like it is tipping over, leaning awkwardly, or weighted heavily toward one side when viewed in inverted orientations.

---

### Suite 3: Affordance & Obstruction Testing
**Goal:** Guarantee that the icon’s essential silhouette remains recognizable even when obstructed, masked, or viewed with impaired vision.

1. **Slash Obstruction**:
   - Apply a standard **45° diagonal slash** with a **2px knockout gap**.
   - Test both Line and Fill variants.
   - *Pass Criteria*: Core metaphor remains identifiable beneath the negation slash.
2. **Corner Obstruction (4-Quadrant Badge Check)**:
   - Place a circular modifier badge with a 2px knockout mask in each of the 4 quadrants:
     - Top-Left
     - Top-Right
     - Bottom-Left
     - Bottom-Right
   - *Pass Criteria*: The primary shape remains distinct regardless of which corner is obscured.
3. **Low Vision / Blur Simulation**:
   - Apply progressive Gaussian blur filters (e.g. `1px`, `2px`, `3px`, `4px`).
   - *Pass Criteria*: The gross silhouette and primary geometric mass remain distinguishable even at high blur levels.

---

### Suite 4: Colorization & Contrast Parity
**Goal:** Ensure legibility across theme surfaces and polarities.

* **Surface Variants**:
  1. **Default Mode (Light)**: Dark icon (`#111111`) on pure white background (`#FFFFFF`).
  2. **Inverted Mode (Dark)**: Light icon (`#FFFFFF`) on dark background (`#111111`).
* **Variant Parity**:
  - Test both `*-line.svg` and `*-fill.svg`.
  - Check that knockout counters do not optically bleed or disappear in dark mode.

---

### Suite 5: Multi-Scale & Down-Sampling Ladder
**Goal:** Test subpixel rendering and rasterization fidelity across display scales.

* **24px Icon Ladder**:
  - `48px` (200% zoom / high DPI display)
  - `36px` (150% zoom)
  - `24px` (100% native scale)
* **16px Icon Ladder (Degradation & Down-sampling)**:
  - `16px` (100% native scale)
  - `12px` (75% scaling)
  - `10px` (62.5% scaling)
  - `8px` (50% scaling)
* **Pass Criteria**: Lines do not blur into fuzzy grey anti-aliasing artifacts; counters remain open and clear.
