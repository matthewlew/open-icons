# Proposal — travel & outdoors pack

**Status:** draft
**Motivation:** the Roadtrip app (`~/Documents/GitHub/roadtrip/web`) currently ships
no icon system at all — five hand-written inline SVGs, fourteen emoji used as
controls (`🗑` `✏️` `⚙` `▶` `🔔` `⚠` `✅` `🛒` `🏕️` `⛰️` `🎟️` `👀` `🔁` `🟢`), and
text glyphs (`☰ ✕ ✓ ★ ☆ ▲ ▼ ▾ ▸ • ×`). Auditing that against the 174-icon set:

- **UI chrome is ~95% already covered.** close, chevron/caret ×4, trash, edit,
  settings, bell, play/pause, warning, check-circle-fill, star, menu, location,
  pin, navigation, mail, search, filter, external, refresh, calendar, clock,
  timer, eye, person, lock, log-out, share, copy, link, sort — all present, most
  with fills. The 11-icon `cart-*` family covers the add-to-cart flow better
  than the app does today.
- **Two clusters are missing entirely**: map primitives, and the outdoors/travel
  domain. That is what this proposal covers.

The gap is not 34 unrelated drawings. It is **ten primitives** the set does not
have yet; the icons fall out of them. Sizing the work as primitives is also the
only way to keep the pack on the weight axis — a one-off drawing at W=2 is a
master, and §"16 → 24" of the spec says never scale a master.

---

## Part 1 — the primitives

Each is a `generate.py`-level helper: geometry as a function of `W`, no
hardcoded clearances. Three of them are **extractions** — the geometry already
exists inside one icon and needs lifting out rather than inventing.

| # | Primitive | Signature (proposed) | Clearance rule | Feeds |
|---|---|---|---|---|
| 1 | **gable** — isosceles apex, mitred at the peak | `gable(apex, half, drop, close=False)` | apex mitre follows `corner()` at `e_tip()`; open ends take round caps | tent, mountain, park |
| 2 | **bolt** — closed lightning zig | `bolt(h=…, kink=…)` | vertex extents at `e_tip()`; the waist is the `gapi()` floor, `0.40 W` | bolt, ev-charger, fuel |
| 3 | **chassis** — body silhouette + two wheels | `chassis(profile, wheels=2)` | wheel ring to body = `gapm()`; wheel r = `r_more()` | car, rv, trailer, boat |
| 4 | **bars** — n stepped bars on a shared baseline | `bars(heights)` | pitch = `pitch_bar()` (already defined, unused outside `volume`) | chart, activity, signal |
| 5 | **fold** — 3-panel quad with alternating vertical creases | `fold(panels=3)` | creases are negative lines at `crease()` = `W`, not moats | map |
| 6 | **stack** — n offset plates | `stack(n, shape)` | plate pitch = `gap()`; reuse `photo-stack`'s offset rule verbatim | layers, photo-stack (refactor) |
| 7 | **droplet** — teardrop, apex up | `droplet(r, apex)` | **extract** from `location()` / `pin()` — three copies today | water, fuel, rain |
| 8 | **arcs** — n concentric arcs from an origin | `arcs(n, a0, a1)` | radial pitch = `gap()`, same as `volume`'s waves | wifi, broadcast, signal-wave |
| 9 | **flame** — asymmetric teardrop with an inner counter | `flame(fill=False)` | counter grows `+0.25` on the knockout flip (§Counters) | campfire, fuel-station |
| 10 | **route** — S-polyline with terminal marks | `route(marks=('dot','pin'))` | terminal mark to path = `gapm()` | route, trail, navigation-active |

**Extractions to do at the same time** (no new icons, strictly debt): `droplet`
out of `location`/`pin`; the roof out of `home()` into `gable`; the offset rule
out of `photo-stack` into `stack`. Each currently exists as inlined geometry, so
each is a place the weight axis can silently drift.

---

## Part 2 — the icons

### 2a. Map chrome (6) — generic

| Name | Built from | Keyline | Fill variant |
|---|---|---|---|
| `map` | `fold` | rect (live − 4) | no |
| `layers` | `stack(3, rhombus)` | rect | no |
| `route` | `route` | live area | no |
| `compass` | `ring` + `arrow(run2)` needle | circle (live area) | no |
| `zoom-in` / `zoom-out` | `search(mark='add'/'minus')` | — | no |

`zoom-in`/`zoom-out` are **aliases, not new drawings** — `search-add` and
`search-minus` already exist and are exactly these. Add them to the alias table
rather than the set; that is the §"Reduce Icon Redundancy" call.

No fills in this group: none of them ever carries a selected state. Map chrome
is always a button, never a marker.

### 2b. POI categories (16) — travel-scoped, **fill variants required**

These are the map-marker and layer-toggle set, and the toggle's on/off state is
exactly the line/fill pair the system already governs. Every one needs both.

| Name | Built from | Notes |
|---|---|---|
| `campsite` | `gable` | single tent, one site. Use for a specific, reservable site — matches NPS's `campsite-black-22.svg` |
| `campground` | `gable` + 2 small `gable` peaks | `campsite`'s own tent, translated, plus two smaller tent-peaks (apex + both legs, not bare strokes) — more sites behind it. Use for the whole facility/area, not one site. Matches NPS's `campground-black-22.svg`, which is exactly this pairing, not a mirrored duplicate |
| `mountain` | `gable` ×2, offset by `gaps()` | replaces ⛰️; two masses, so silhouette gap not stroke gap |
| `park` | `gable` (notched) + trunk | one silhouette, no stroke crossings |
| `ev-charger` | pedestal + cable + `bolt` | supercharger layer; see decision A/B/C |
| `bolt` | `bolt` | bare, for the charging-speed field |
| `car` | `chassis(profile='sedan')` | |
| `rv` | `chassis(profile='box', wheels=2)` | |
| `trailer` | `chassis` ×2 + hitch | must show the tow vehicle or it is just a box |
| `fuel` | `droplet` + pump handle | |
| `parking` | `enclosed('P', 'square')` | uses the existing `enclosed()` path |
| `restroom-figures` | `_person` ×2 | **default.** Composes `_person` rather than redrawing it, so it inherits the head/shoulder `gaps()` datum for free. Says "restroom here", not a plumbing claim — used whenever the amenity data doesn't confirm flush or vault |
| `restroom` | `rrect` + bowl | flush toilet — says "plumbing". Shown only when the data confirms it |
| `restroom-vault` | `rrect` + `gable` | vault / porta-potty — says "no plumbing". Shown only when the data confirms it |
| `shower` | `arcs` + head bar | |
| `water` | `droplet` | |
| `picnic-table` | `gable` inverted + top bar | |

`restroom-figures` is the recommended default, not a third alternative: the app's
amenity data doesn't always say whether a site has plumbing, and the icon has to
render either way. Figures never assert a claim the data can't back up; `restroom`
and `restroom-vault` are specific overlays drawn only once the data actually says
flush or vault. See the decision strip in `site/proposal-travel.html`.

**Known collision:** `restroom-vault` (peaked roof + vent stack) currently sits
close to `home` in silhouette. Needs resolving before it ships.

### 2c. Amenities (5) — travel-scoped, line only

`wifi` (`arcs`), `campfire` (`flame`), `pets`, `food`, `store`. No fills: these
appear only as inline list markers in the drawer, never as a state.

**Resolved: keep both.** `store` (a place — the campground store, a nearby town)
and `cart` (an action — add to cart) answer different questions; confirmed, not
building `cart` twice under two names.

### 2d. Data & status (4) — generic

| Name | Built from | Why |
|---|---|---|
| `chart` | `bars([…])` | the supercharger busy-times sparkline |
| `activity` | `route` flattened | live/occupancy |
| `signal` | `bars` ascending | the campground `cell_coverage` field |
| `circle` / `circle-fill` | `ring` / `dot(r=m_circ())` | the bare status dot (🟢). The set has `check-circle` but no plain one. |

### 2e. Explicitly **not** proposed

- **Brand marks** — Slack, rec.gov, Tesla. Roadtrip inlines these
  ([`topbar/alerts.js:37`](../../../Documents/GitHub/roadtrip/web/topbar/alerts.js)).
  They are multi-colour, off-axis, and off-grid. They stay inline.
- **`directions`** — Roadtrip uses a trending-up arrow for this today, which is
  a misuse, but the fix is `navigation` (already in the set), not a new icon.
- **`ticket`** (🎟️) — `price` and `money` cover the reservation affordance.
- **`drag-handle`** — `more-vertical` is the conventional grip. Alias it.
- **`spinner`** — animation, not geometry. Out of scope for a static set.

---

## Part 3 — the governance question this forces

The README's classification is binary: **Generic** (universal) or **Product**
(scoped, cannot be repurposed). Sections 2b and 2c fit neither. `campground` is
not universal — it would be noise in a CRM. But it is not Roadtrip-specific
either; any travel, mapping, or booking product wants exactly this set.

**Recommendation: add a third scope, `travel`** — a named pack, generic *within*
its domain, opt-in at import. That keeps §"Prevent Product-Specific Icon Misuse"
intact (the pack cannot leak into an unrelated product) without pretending a
14-icon domain vocabulary is one product's custom override.

The alternative — scoping all 19 to `roadtrip` — means the second travel product
re-draws them, which is the redundancy the project exists to prevent.

---

## Counts

| Group | New drawings | Fill variants | Total new files at 24 |
|---|---|---|---|
| Map chrome | 4 (+2 aliases) | 0 | 4 |
| POI categories | 17 | 15 | 32 |
| Amenities | 5 | 0 | 5 |
| Data & status | 4 | 1 | 5 |
| **Total** | **30** | **16** | **46** |

Set grows 174 → 220. Ten new primitives, three extractions.

## Open questions

1. `travel` scope — accept, or scope to `roadtrip`? (Blocks 2b/2c.)
0. **Resolved: restroom default is `restroom-figures`.** The amenity data doesn't always
   say whether a site has plumbing, and the icon has to render either way — figures never
   assert a claim the data can't back up. `restroom` (flush) and `restroom-vault` ship
   alongside it as specific overlays, drawn only once the data actually confirms flush or
   vault. Still open: EV mark (pump+bolt+plug / connector / bolt-in-box) and parking
   container (square / circle). Grounded against the public-domain NPS symbol library
   (`nationalparkservice/symbol-library`): their RV icon has a real cab-over overhang,
   their `electric-car-charging` icon is a pump cabinet with the bolt as its readout and
   their `electrical-hookup` icon (the campground power-pedestal symbol) is a pair of
   straight prongs on a stem — not a bent gas nozzle — which is why `ev-charger`'s cable
   now ends in a plug instead of a hose hook, and their parking symbol has no container at
   all — a bare P, which is the argument for square over circle. Both drawn and compared
   in `site/proposal-travel.html`; each has a recommendation, neither is settled.
0. **Resolved: `campsite` vs `campground` are two icons, not one.** Their `campsite` icon
   is one tent, alone, on a ground line — use it for a specific, reservable site. Their
   `campground` icon is that same tent plus two smaller tent-peaks (apex + both legs, not
   bare strokes) — use it for the whole facility/area. That's the fix for "campground
   reads as campsite's twin": a shared baseline and a repeated silhouette read as an echo,
   not as *more of something*, and a bare diagonal stroke has no peak of its own to read as
   a tent. `campground` is now `campsite`'s own path, translated, plus two small `gable`
   peaks in the same silhouette vocabulary.
0. **Resolved: keep `store` and `cart`.** Different questions — a place vs. an action.
3. `park` vs `mountain` at 16px — needs an A/B render before committing; two
   `gable`-derived silhouettes may not separate at the small size.
4. Do the POI fills need the **container** rule or the **figure** rule? `campground`
   and `mountain` are figures (outer − 0.5, contact datum pinned); `ev-charger` and
   `parking` are containers (knockout, glyph reused verbatim). Confirm per icon
   before generating.
