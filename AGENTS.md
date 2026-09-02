# Open Icons — Agent Guidelines

## 1. Icon Design Values & Principles
All icons created or modified in this repository must align with the core system values and qualification criteria:

*   **Readable**: High legibility, distinct silhouettes, and clean negative space at both 16px and 24px sizes.
*   **Meaningful**: Clear, intuitive metaphors that convey the exact intent without visual ambiguity.
*   **Classic**: Timeless geometry based on standard primitives (circles, squares, rectangles, 45° angles); avoid trendy styling.
*   **Reusable**: Versatile across diverse products, surfaces, and paired line (`*-line.svg`) / fill (`*-fill.svg`) variants.

## 2. Qualification Checklist Before Creating Icons
1. **Search first**: Confirm the icon does not already exist in the library.
2. **Criteria**: Ensure it meets at least one qualification:
   - Product Identity
   - New Concept
   - Recognized Metaphor
   - Universal Utility
3. **Reusability**: Must be applicable across broader contexts, not just a single one-off feature.

## 3. Strict Design Standards & System Rules
- **Stroke Width**: Strictly **2px** for all strokes, curves, and angles (at both 16px and 24px).
- **16px Canvas**: 16×16 box, 16×16 live area (0 padding).
- **24px Canvas**: 24×24 box, 20×20 live area (2px padding).
- **Monochrome & Variants**: Monochrome `currentColor` with paired `*-line.svg` and `*-fill.svg` files.
- **Negative Space & Clearances**: Minimum 2px counter clearance.
- **Slashes (Off/Disabled)**: Strict 45° diagonal with 2px knockout mask around the slash.
- **Badges/Modifiers**: Standard quadrant placement (bottom-right/top-right) with 2px knockout clearance.

## 4. Visual QA & Icon Testing Suite
When creating or editing icons, or building the icon testing/editing environment, incorporate the following test conditions:
- **Resemblance Check**: 5×5 matrix comparison against system peers (Line & Fill, Light & Dark).
- **Optical Balance**: Test rotations (-90°, +90°) and flips (Horiz/Vert) to verify true optical center of gravity.
- **Affordance & Obstruction**:
  - 45° Slash Obstruction with 2px knockout gap.
  - 4-Quadrant Corner Obstruction badges.
  - Low vision / progressive Gaussian blur test for silhouette legibility.
- **Colorization**: Default (#FFFFFF bg) and Inverted (#111111 bg) contrast checks.
- **Scale Ladder**: 24px (200%, 150%, 100%) and 16px down-sampling (100%, 75%, 62%, 50%).

## 5. Technical Docs & Specs
- **Principles & Process**: [docs/icon-design-principles.md](docs/icon-design-principles.md)
- **Design Standards**: [docs/icon-design-standards.md](docs/icon-design-standards.md)
- **Testing & QA Environment Spec**: [docs/icon-testing-environment.md](docs/icon-testing-environment.md)
- **Construction Spec**: [docs/icon-construction-spec.md](docs/icon-construction-spec.md)

