# Icon Design Standards & Technical Rules

When designing, generating, or reviewing icons in this repository, strictly enforce these system rules:

## 1. Style & Theming
- **Monochrome**: Use single-color assets (`currentColor`) supporting Light and Dark modes.
- **Line & Fill Pairs**: Always provide both `*-line.svg` (2px outline) and `*-fill.svg` (solid silhouette with knockout counters).

## 2. Geometry & Keylines
- **Stroke Width**: Strictly **2px** for all strokes, curves, and diagonals.
- **Keyline Shapes**:
  - **16px Canvas**: Circle (Ø16), Square (14×14), Vert Rect (12×16), Horiz Rect (16×12), Diagonal (10×10). Live area: 16×16 (0 padding).
  - **24px Canvas**: Circle (Ø20), Square (18×18), Vert Rect (16×20), Horiz Rect (20×16), Diagonal (14×14). Live area: 20×20 (2px padding).
- **Clearance & Counters**: Minimum 2px negative space between strokes and shapes.

## 3. Slashes & Modifiers
- **Slashes (Off/Disabled)**: Strict 45° angle with a **2px knockout gap** cut out around the slash.
- **Badges/Modifiers (`+`, `-`, dot, etc.)**: Anchored in bottom-right or top-right quadrant with a **2px knockout mask** over the underlying icon.

## 4. Size Independence
- Do not blindly scale 24px icons down to 16px. Since the 2px stroke is identical at both sizes, 16px icons must be individually constructed with simplified details to prevent visual clutter.

## 5. Visual QA & Icon Testing Suite
When building testing/editing tools or conducting QA on candidate icons, verify:
- **Resemblance Matrix**: 5×5 grid comparison against system peers (Line & Fill, Light & Dark).
- **Optical Balance**: Rotate (-90°, +90°) and flip (Horiz/Vert) to check optical center of gravity.
- **Affordance & Obstruction**:
  - 45° Slash Obstruction with 2px knockout mask.
  - 4-Quadrant Corner Obstruction badges.
  - Low Vision / Gaussian blur test for silhouette legibility.
- **Colorization**: Default (#FFFFFF bg) and Inverted (#111111 bg) contrast checks.
- **Scale Ladder**: 24px (200%, 150%, 100%) and 16px down-sampling (100%, 75%, 62%, 50%).

