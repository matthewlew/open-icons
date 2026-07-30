# tools/

Measurement and conformance tooling for the [construction spec](../docs/icon-construction-spec.md).

## `icon-lint.py`

Scores every SVG in `icons-inspiration/` against the spec and sorts the library into three buckets:

```bash
python3 -m venv .venv && .venv/bin/pip install numpy
.venv/bin/python tools/icon-lint.py
```

Point it elsewhere with `ICON_ROOT=/path/to/icons`. Writes `lint.json` next to itself.

### What it checks

| Check | Rule | Severity |
|---|---|---|
| Stroke mode | modal local thickness = 2.0 ± 0.08 | error |
| Stroke consistency | ≥ 45% of contour samples measure 2.0 | warn |
| Minimum feature | < 4% of the form thinner than 0.9 | error |
| Clearance | < 6% of gaps below 0.9 | warn |
| Keyline | ink bbox lands on a keyline (§2.2) | warn / info |
| Grid discipline | ≥ 30% of on-path anchors on the 0.25 grid | warn |
| Complexity | ≤ 60 path commands at 24px, 55 at 16px | warn |

Solid masses (blobs, logos) are detected and exempted from the stroke checks.

### Buckets

- **CLEAN** (score 0) — baseline-ready, import as-is
- **MINOR** (1–15) — usable, note the deviation
- **REWORK** (> 15) — redraw queue

### How the measurement works

Not a path-string parser — it measures rendered geometry. `thickness.py` flattens every path to
polygons, then ray-casts along surface normals from ~900 contour samples to get the local stroke
thickness and local clearance at each point. That recovers the skeleton from a flattened outline,
which is what makes conformance checkable at all. See [Appendix B](../docs/icon-construction-spec.md)
of the spec.

`svgparse.py` is a minimal path parser (M/L/H/V/C/S/Z, both cases) plus circular-arc fitting via
normal intersection — used to detect circles, corner radii, and round terminals.
