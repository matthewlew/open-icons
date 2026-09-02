# Open Icons — Design Standards & System Rules

This document defines the strict, actionable design standards and system rules for all icons in the design system.

---

## 1. Style & Color Standards

### 1.1 Monochrome First
- **Single-color rendering**: All core icons are monochromatic.
- **Dynamic theming**: Icons must use `currentColor` (or standard theme tokens) to seamlessly adapt across Light and Dark themes.
- **No embedded tints/gradiants**: Core UI icons do not contain hardcoded fills, shadows, or multi-tone opacity layers.

### 1.2 Paired Line (`*-line.svg`) & Fill (`*-fill.svg`) Variants
Every UI icon exists as a coordinated pair:
- **Line Variant (`*-line.svg`)**:
  - Outlined skeleton with uniform **2px stroke**.
  - Used for default, inactive, or neutral UI states.
- **Fill Variant (`*-fill.svg`)**:
  - Filled solid mass silhouette.
  - Used for selected, active, pinned, or emphasized states.
  - Interior details are rendered as **knockout counters** (transparent cutouts) to preserve silhouette readability.

---

## 2. Geometry & Keylines

All icon skeletons are built strictly upon standard geometric primitives:

| Keyline Primitive | 16px Live Area (16×16) | 24px Live Area (20×20) | Typical Use Cases |
| :--- | :--- | :--- | :--- |
| **Circle** | Ø16 | Ø20 | Settings, user, clock, globe, info |
| **Square** | 14 × 14 | 18 × 18 | Apps, grid, windows, folder, shield |
| **Vertical Rectangle** | 12 × 16 | 16 × 20 | Mobile phone, document, lock, battery |
| **Horizontal Rectangle** | 16 × 12 | 20 × 16 | Mail, desktop screen, credit card, camera |
| **45° Diagonal / Cross** | 10 × 10 | 14 × 14 | Add (`+`), Close (`✕`), Check (`✓`), Arrow |

---

## 3. Negative Space, Clearances & Counters

- **Minimum Counter Clearance**: Gaps and interior cutouts must be at least **2px** wide to prevent optical closing when rendered at 100% scale.
- **Envelope / Interior Creases**: Angles and fold lines (e.g. mail flap, home roof pitch) must maintain clear negative space above intersecting base strokes.
- **Corner Radii**:
  - Exterior corners use standard radii (typically 1px to 2px depending on size).
  - Interior intersections remain clean and sharp or minimally rounded to maximize counter openness.

---

## 4. Slashes & "Off / Disabled" States

- **Standard 45° Angle**: All negation/disabled slashes (e.g. `eye-off`, `mic-off`, `bell-off`, `camera-off`, `slash`) must follow a strict **45° angle** running diagonally.
- **Knockout Gap Clearance**: A **2px knockout clearance (mask)** must separate the slash from the underlying icon shape so the slash never visually merges with the base glyph.

---

## 5. Badges, Modifiers & Action Glyphs

When adding a modifier (e.g. `plus`, `minus`, `lock`, `check`, `alert dot`):
- **Quadrant Placement**: Standard modifiers are anchored in the **bottom-right** or **top-right** quadrant.
- **Knockout Mask**: The badge element must cut out a **2px clear gap** from the base icon behind it.
- **Modifier Scale**: Badges must use standard simplified sub-primitives (e.g. 6×6 or 8×8 bounding area) designed specifically for legibility within the icon frame.

---

## 6. Sizing & Canvas Parity (16px vs 24px)

| Specification | 16px Icon | 24px Icon |
| :--- | :--- | :--- |
| **Canvas Size** | 16 × 16 px | 24 × 24 px |
| **Padding / Trim** | **0 px** (full bleed) | **2 px** |
| **Live Area** | **16 × 16 px** | **20 × 20 px** |
| **Stroke Width** | **2 px** | **2 px** |
| **Stroke-to-Canvas Ratio** | 12.5% | 8.3% (10% of live area) |
| **Level of Detail** | **Simplified**: Micro-details merged or removed for crispness. | **Full**: Standard expressive geometry. |

> [!IMPORTANT]
> Because stroke width remains **2px** at both sizes, a 16px icon is **not** a scaled-down 24px icon. It must be drawn specifically to fit the 16px grid without overcrowding.

---

## 7. Enclosed Characters & Badges

- **Optical Centering**: Characters, numbers, or currency glyphs inside circular or square badges (e.g. `(P)`, `(E)`, `(L)`, `($)`, `(¥)`) must be optically centered based on visual mass, not mathematical bounding box.
- **Stroke Balance**: Interior character strokes should be balanced with the 2px outer bounding ring so negative space is uniform.

## 8. Brand & Third-Party Logos

- **Keyline Conformance**: Third-party brand logos (e.g. Google Maps, PayPal, Visa, WhatsApp) must be scaled to conform to standard optical keyline bounds (circle/square/rect).
- **Recognizable Mark**: Preserve the brand’s authentic proportions and silhouette while conforming to the system canvas.
- **Dual Support**: When multi-color brand icons are required, provide both the official full-color SVG and a monochromatic system-aligned version.

---

## 9. Visual QA & Icon Testing Suite Requirements

All icons must pass the automated/interactive visual QA suite defined in [icon-testing-environment.md](icon-testing-environment.md):
1. **Resemblance Check**: 5×5 matrix comparison against peer system icons (Line & Fill, Light & Dark).
2. **Optical Balance (Rotations & Flips)**: Evaluated at -90°, +90°, Horizontally Flipped, and Vertically Flipped to reveal optical center.
3. **Affordance & Obstruction**:
   - 45° Slash Obstruction with 2px knockout mask.
   - 4-Quadrant Corner Obstruction badges.
   - Low vision / progressive Gaussian blur test for silhouette clarity.
4. **Colorization**: Default (Light) and Contrast (Dark) theme validation.
5. **Scale Ladder**: 24px ladder (200%, 150%, 100%) and 16px down-sampling ladder (100%, 75%, 62%, 50%).

