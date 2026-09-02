# Icon Design Principles and Contribution Guidelines

Always apply the following principles and criteria when designing, evaluating, generating, or modifying icons in this repository:

## 1. Icon Qualification Criteria (Ask Yourself)
Before designing or adding any new icon:
1. **Check Existing Assets**: Verify if an equivalent icon or modifier variant already exists in `icons/` or `icons-inspiration/`.
2. **Qualification Requirements**: Only add a new icon if it meets at least one condition:
   - **Product Identity**: Represents a core product or brand concept.
   - **New Concept**: Communicates an essential concept unserved by existing glyphs.
   - **Recognized Metaphor**: Employs a widely established, industry-standard metaphor.
   - **Universal Utility**: Has broad, cross-product utility rather than a single niche use case.
3. **Reusability & Context**: Ensure the metaphor functions across multiple surfaces (navigation, actions, badges, tables).

## 2. Core Icon Design Values
- **Readable**: Instantly recognizable silhouette; high legibility at 16px and 24px; distinct negative space and counters.
- **Meaningful**: Unambiguous visual communication; culturally and contextually intuitive metaphor.
- **Classic**: Built from fundamental geometric primitives (circle, square, rect, 45°); avoids ephemeral stylistic trends.
- **Reusable**: Modular, system-aligned, and cleanly pairable across line (`*-line.svg`) and fill (`*-fill.svg`) variants.

## 3. Technical & Construction Alignment
When generating or editing SVG code for icons, enforce the construction spec in `docs/icon-construction-spec.md`:
- **Stroke Width**: Exactly 2px across both 16px and 24px sizes.
- **Grid & Live Area**:
  - 16px icon: 16×16 canvas, 16×16 live area (no padding).
  - 24px icon: 24×24 canvas, 20×20 live area (2px padding).
- **Keyline Anchors**: Circle, square, vertical/horizontal rectangle, diagonal.
- **Centerline Skeleton**: Derive strokes from centerline geometry with clean integer/half-integer coordinates.
