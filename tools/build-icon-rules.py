#!/usr/bin/env python3
"""Build data/icon-rules.json.

has_fill and every icon name are derived from icons/names.json, so the file
cannot drift out of sync with the set by a typo. Run it again after adding
icons; it is cheap and it re-validates every reference.
"""
import json, os, sys

ROOT = os.path.expanduser('~/Desktop/design-systems-workspace/open-icons-playground')
NAMES = set(json.load(open(os.path.join(ROOT, 'icons/names.json'))))

CLUSTERS = {
  "menu-affordance": {
    "question": "Which menu affordance opens this?",
    "tiebreaker": "Scope decides, not shape. Ask what the menu acts ON: the whole view, one row, or the current object. Hamburger is the view, kebab is the row, meatball is the object in front of you.",
  },
  "dismiss-close-delete": {
    "question": "Is this closing, dismissing, removing, or destroying?",
    "tiebreaker": "Reversibility, in order: close (nothing lost) < dismiss (this one, now) < remove (from a collection) < delete (destroys data). Never use a heavier icon than the action earns — a trash can on a dismissible toast reads as data loss.",
  },
  "place-marker": {
    "question": "Am I marking a place, an act, or a direction?",
    "tiebreaker": "location answers WHERE. pin is a verb — someone chose to fasten this. navigation answers WHICH WAY. The silhouettes share nothing on purpose: teardrop, tack, arrowhead.",
  },
  "save-signal": {
    "question": "What does saving this mean?",
    "tiebreaker": "Who is the signal for? bookmark and star are for the user's own retrieval; heart is a public sentiment; flag is for someone else to action.",
  },
  "outward": {
    "question": "Where does this send the user?",
    "tiebreaker": "share hands content to a person. external leaves the app. link is the address itself, not the act of going.",
  },
  "severity": {
    "question": "How loud should this be?",
    "tiebreaker": "info is neutral and unrequested. help is neutral and requested. warning means something is wrong or about to be. Do not use warning for emphasis — it spends the one signal that has to still work when it matters.",
  },
  "figure": {
    "question": "One person, several, or a facility?",
    "tiebreaker": "person is an individual or an account. people is a group or a social relation. restroom-figures is a FACILITY sign and is never a stand-in for users.",
  },
  "landform-camping": {
    "question": "One site, a whole facility, or terrain?",
    "tiebreaker": "campsite is one reservable pitch; campground is the facility around it; mountain and park are terrain and never bookable. Reservability is the line.",
  },
  "droplet": {
    "question": "Which droplet-derived icon?",
    "tiebreaker": "All three share one construction. water is potable water as an amenity; fuel is a dispensing machine; location is a marker that happens to be teardrop-shaped and is not about liquid at all.",
  },
  "data-shape": {
    "question": "Discrete values, signal strength, or a trace over time?",
    "tiebreaker": "chart and signal are deliberately the same block with the same footprint — only the profile differs. If the bars must ascend to mean anything, it is signal. If a bar can fall, it is chart. If it is continuous, it is activity.",
  },
  "zoom-vs-search": {
    "question": "Searching, or changing magnification?",
    "tiebreaker": "search-add and search-minus ARE zoom-in and zoom-out. Do not draw new icons for zoom; alias these.",
  },
  "vehicle": {
    "question": "Which vehicle class does the site accept?",
    "tiebreaker": "Towing is the axis. car is self-propelled and small; rv is self-propelled and large (cab-over step); trailer is towed (the tongue is the tell). A site that takes an rv may not take a trailer.",
  },
}

# icon -> (cluster, scope, use_when, not_when, instead_use, rationale)
I = {}

def add(icon, cluster, use_when, not_when, instead_use, rationale, scope="generic"):
    I[icon] = dict(cluster=cluster, scope=scope, use_when=use_when,
                   not_when=not_when, instead_use=instead_use, rationale=rationale)

# --- menu affordance -------------------------------------------------------
add("menu", "menu-affordance",
    "Opens navigation for the whole view or app. The top-level drawer.",
    "Never for actions scoped to a single item.",
    {"more-vertical": "the actions belong to one row or card, not the view"},
    "Hamburger has meant 'the app's navigation' since it was three lines on a Xerox Star. Using it for a row menu makes every row look like it can navigate away.")

add("more-vertical", "menu-affordance",
    "Row-level or card-level overflow. The kebab: actions that apply to the one thing it sits beside.",
    "Not for view-wide navigation, and not when there is horizontal room to show the actions outright.",
    {"menu": "the target is the whole view", "more-horizontal": "the menu belongs to the current object rather than a row in a list"},
    "Vertical because it sits in a vertical list and its axis reads as 'this row'. Two or three overflow actions in a row is the canonical case.")

add("more-horizontal", "menu-affordance",
    "Overflow for the object currently in front of the user — a toolbar tail, a detail header, a composer.",
    "Not inside a repeated list row.",
    {"more-vertical": "you are in a repeated row and the menu is that row's"},
    "Horizontal because it terminates a horizontal run of controls. In a list it competes with the row's own axis.")

add("list", "menu-affordance",
    "A view-mode toggle: show these items as a list. Pairs with grid.",
    "Never as a menu affordance — it is a destination, not a disclosure.",
    {"menu": "you meant the navigation drawer", "grid": "the other half of the same toggle"},
    "Three lines with bullets reads as content layout. Three lines without reads as menu. They are one pixel apart in silhouette and opposite in meaning, which is exactly why this entry exists.")

# --- dismiss / close / delete ---------------------------------------------
add("close", "dismiss-close-delete",
    "Close a surface that owns the screen: modal, sheet, full-screen takeover, drawer.",
    "Not for removing an item from a collection.",
    {"close-circle": "the X sits on top of content and needs its own hit surface",
     "minus-circle": "you are removing a row from a list, not closing a surface"},
    "Bare X is the lightest possible dismissal. Nothing is lost and nothing is undone.")

add("close-circle", "dismiss-close-delete",
    "Dismiss one transient thing in place: a chip, a filter token, a toast, a thumbnail in an upload tray.",
    "Not as the primary close on a modal — the container reads as a button and competes with the modal's own controls.",
    {"close": "the surface owns the screen", "minus-circle": "the collection is a list of peers rather than a set of tokens"},
    "The circle gives the mark a hit target where there is no chrome to provide one, and it scopes the dismissal to the token it is attached to.")

add("minus-circle", "dismiss-close-delete",
    "Remove one row from a collection the user is assembling — a cart, an invite list, a set of filters.",
    "Not when the underlying record is destroyed.",
    {"trash": "the record itself is destroyed", "close-circle": "it is a token or chip, not a row"},
    "Minus is arithmetic on a set. It says the thing still exists, it just is not in this collection any more — which is the promise an X does not make.")

add("trash", "dismiss-close-delete",
    "Destroy the record. The action needs confirmation or an undo.",
    "Never for closing, dismissing, clearing a field, or removing from a cart.",
    {"minus-circle": "the record survives — you are only removing it from a collection",
     "close": "nothing is being destroyed at all"},
    "Trash is the heaviest icon in the set and the only one that should make someone hesitate. Spending it on a dismissible toast is how it stops working.")

# --- place / marker --------------------------------------------------------
add("location", "place-marker",
    "Mark WHERE something is. A POI on a map, an address on a card, a 'near me' control.",
    "Not for the act of saving or fastening something.",
    {"pin": "a person chose to fasten this — it is a verb", "navigation": "you mean a heading, not a place"},
    "Balloon head, hole in the middle, tapering to a point. It answers 'where'.")

add("pin", "place-marker",
    "The ACT of fastening: pin this message, pin this column, keep this to the top.",
    "Never as a map marker.",
    {"location": "you mean a place on a map"},
    "Flat wide cap, solid needle, leaning. Deliberately shares no silhouette with location — a teardrop against a T — because the two sit next to each other and a reader has to tell them apart at 16px without a label.")

add("navigation", "place-marker",
    "A heading or an active route — 'directions', 'navigate here', the live-position arrow.",
    "Not for a static place, and not for trending or growth.",
    {"location": "the thing is a place, not a direction", "route": "you mean the whole path between two points"},
    "Roadtrip currently uses a trending-up arrow for directions, which is a misuse; the fix is this icon, not a new one.")

# --- save signals ----------------------------------------------------------
add("bookmark", "save-signal",
    "Save for the user's own later retrieval. Private, binary, no ranking.",
    "Not for expressing an opinion about the item.",
    {"star": "the product treats saving as rating or favouriting",
     "heart": "the signal is public sentiment"},
    "A bookmark is a filing action. It says nothing about whether the thing is good.")

add("star", "save-signal",
    "Favourite or rate. Use when the product's own language is 'starred' or when it feeds ranking.",
    "Not when the save is private and unranked.",
    {"bookmark": "it is filing, not rating"},
    "Star carries a quality judgement that bookmark does not. Picking the wrong one leaks into copy — 'your starred items' and 'your bookmarks' are different promises.")

add("heart", "save-signal",
    "Public sentiment: like, love, react. Visible to others or aggregated into a count.",
    "Not for private saves.",
    {"bookmark": "the save is private", "star": "the signal drives ranking rather than sentiment"},
    "Heart is the only one of the four that implies an audience.")

add("flag", "save-signal",
    "Escalate to someone else: report, mark for review, raise for moderation.",
    "Never as a save or a favourite.",
    {"bookmark": "the user is filing this for themselves"},
    "Flag hands the item to a third party. It is the only one of the four whose audience is not the user or their peers.")

# --- outward ---------------------------------------------------------------
add("share", "outward",
    "Hand this content to a person or another app. Opens a share sheet or a recipient picker.",
    "Not for opening a URL.",
    {"external": "the user is leaving the app", "link": "you mean the address itself"},
    "Share is about a recipient. If nothing is being handed to anybody, it is the wrong icon.")

add("external", "outward",
    "This leaves the app or opens a new tab. Sits INSIDE or after the link text.",
    "Not as a standalone button, and never for in-app navigation.",
    {"share": "content is going to a person", "arrow-right": "navigation stays in the app"},
    "It is an annotation on a link, warning about a context switch — not an action of its own.")

add("link", "outward",
    "The address itself: copy link, attach a URL, 'linked accounts'.",
    "Not for navigating anywhere.",
    {"external": "the user is being sent out of the app", "copy": "the action is copying generally, not copying a URL"},
    "Chain links are the object, not the journey.")

# --- severity --------------------------------------------------------------
add("info", "severity",
    "Neutral, unrequested context. A note the user did not ask for and does not have to act on.",
    "Not for anything the user must resolve.",
    {"warning": "something is wrong or about to be", "help": "the user asked"},
    "Info is the floor of the severity scale. Nothing is broken. Ships FILLED in a banner or "
    "alert (info-fill); the line form is for neutral inline hints.")

add("help", "severity",
    "The user asked. Tooltips, 'what is this?', a link into docs.",
    "Not for volunteering context the user did not request.",
    {"info": "the system is volunteering it"},
    "Same neutrality as info; the difference is who initiated. A question mark the user did not ask reads as the interface being unsure of itself.")

add("warning", "severity",
    "Something is wrong, at risk, or about to be. The user should act.",
    "Never for emphasis, novelty, or 'heads up, this is new'.",
    {"info": "it is neutral context", "help": "the user is asking a question"},
    "The triangle is the loudest shape in the set, and it ships FILLED (warning-fill) wherever "
    "it is alerting — the solid mass is what makes it read before the sentence next to it. It "
    "only keeps working if it is rationed.")

# --- figures ---------------------------------------------------------------
add("person", "figure",
    "One individual: an account, a profile, an assignee, 'my stuff'.",
    "Not for a facility.",
    {"people": "more than one, or a social relation", "restroom-figures": "you mean a restroom"},
    "Head and shoulders. The whole family shares one head-to-shoulder datum of exactly 1.0 — a seam, not a gap.")

add("people", "figure",
    "A group, a team, a shared thing, a social relation.",
    "Not as a restroom sign.",
    {"person": "a single individual", "restroom-figures": "it is a facility, not users"},
    "Two overlapping figures of different sizes. The overlap is what says 'group' rather than 'two users'.")

add("restroom-figures", "figure",
    "A restroom exists here. The neutral default when amenity data does not confirm plumbing.",
    "Never as a stand-in for users, accounts or a group.",
    {"people": "you mean users or a group"},
    "Two equal figures, separated and symmetric — deliberately not people's overlapping unequal pair. Says 'restroom here' without asserting flush or vault, which the data often cannot back up.",
    scope="travel")

# --- landform / camping ----------------------------------------------------
add("campsite", "landform-camping",
    "ONE specific, reservable pitch. A booking, a pin on a site map, a confirmed stay.",
    "Not for the facility as a whole.",
    {"campground": "you mean the whole facility or area"},
    "One tent with a door, alone on a ground line. Matches the NPS campsite symbol.",
    scope="travel")

add("campground", "landform-camping",
    "The whole facility or area — a park with sites in it, a search result for a place to camp.",
    "Not for one bookable pitch.",
    {"campsite": "you mean a single reservable site"},
    "A near tent plus a second behind it, moated. 'More of something', not an echo of campsite.",
    scope="travel")

add("mountain", "landform-camping",
    "Terrain, elevation, scenery, a trail's character. Never bookable.",
    "Not as a generic 'outdoors' catch-all where a specific amenity icon exists.",
    {"park": "you mean maintained green space rather than elevation",
     "campground": "the thing can be booked"},
    "Two peaks in ONE silhouette with a saddle, plus a snow line — all three separators exist to keep it out of campground's territory at 16px.",
    scope="travel")

add("park", "landform-camping",
    "Maintained green space, shade, a picnic area's setting, 'trees here'.",
    "Not for wilderness or elevation.",
    {"mountain": "you mean terrain and elevation"},
    "A broadleaf canopy and trunk. Deliberately not a conifer: a triangle here would collide with both campsite and mountain at small size.",
    scope="travel")

# --- droplet family --------------------------------------------------------
add("water", "droplet",
    "Potable water as an amenity — a spigot, a fill station, 'water available'.",
    "Not for fuel, not for weather, not for a map marker.",
    {"fuel": "it is a dispensing machine", "location": "you mean a place"},
    "location's droplet inverted: apex up, no counter. The two never share a silhouette.",
    scope="travel")

add("fuel", "droplet",
    "A fuel stop — petrol, diesel. The machine, not the liquid.",
    "Not for EV charging.",
    {"ev-charger": "the site charges rather than fuels", "water": "you mean drinking water"},
    "Shares its whole pump body with ev-charger; only the face mark and what the arm ends in differ. That the two are the same kind of object is true by construction.",
    scope="travel")

# --- data shapes -----------------------------------------------------------
add("chart", "data-shape",
    "Discrete values across categories or time buckets — busy times, usage by day.",
    "Not for signal strength.",
    {"signal": "the bars must ascend to carry meaning", "activity": "the data is continuous"},
    "Same block, pitch and footprint as signal. Its profile falls at least once, and that is the only separator — so never draw it monotonic.")

add("signal", "data-shape",
    "Strength or level on an ordered scale — cell coverage, wifi strength, capacity.",
    "Not for arbitrary data.",
    {"chart": "a value is allowed to fall"},
    "Five bars in even steps. Ascending is load-bearing: it is what makes the icon mean 'more is better'.")

add("activity", "data-shape",
    "A continuous trace: live occupancy, a pulse, something happening now.",
    "Not for categorical values.",
    {"chart": "the values are discrete buckets"},
    "A level run, one spike, a level run. Continuity is the message.")

# --- zoom ------------------------------------------------------------------
add("search", "zoom-vs-search",
    "Find something. A search field, a search action.",
    "Not for magnification controls.",
    {"search-add": "you mean zoom in"},
    "The lens alone is search. The lens with a mark is magnification.")

add("search-add", "zoom-vs-search",
    "Zoom in. This IS zoom-in — alias it rather than drawing a second icon.",
    "Not as 'add a saved search'.",
    {"add": "you mean creating something"},
    "The proposal's redundancy call: zoom-in and zoom-out already exist under these names.")

add("search-minus", "zoom-vs-search",
    "Zoom out. This IS zoom-out — alias it.",
    "Not as 'remove a saved search'.",
    {"minus": "you mean subtraction"},
    "See search-add.")

# --- vehicles --------------------------------------------------------------
add("car", "vehicle",
    "A standard vehicle — parking suitability, a drive-time estimate, 'accessible by car'.",
    "Not for oversized rigs.",
    {"rv": "the vehicle is a large self-propelled motorhome", "trailer": "the vehicle is towed"},
    "Cabin bulge on a low body. Shares its chassis, wheel datum and belt-line counter with rv and trailer.",
    scope="travel")

add("rv", "vehicle",
    "A large self-propelled motorhome. Site length limits, hookups, RV-accessible.",
    "Not for a towed unit.",
    {"trailer": "it is towed, and a site that takes one may not take the other"},
    "The cab-over step is the whole icon — without it this is a bus.",
    scope="travel")

add("trailer", "vehicle",
    "A towed unit — travel trailer, caravan. Distinct from rv because sites often accept one and not the other.",
    "Not for a motorhome.",
    {"rv": "the vehicle drives itself"},
    "The tongue is what says trailer, which is why the tow vehicle is not drawn: two vehicles inside 20 units leaves each about 8, and neither is legible.",
    scope="travel")

# ---------------------------------------------------------------------------
missing = sorted(k for k in I if k not in NAMES)
if missing:
    sys.exit('icons referenced but not in the set: %s' % missing)
bad_ref = sorted({r for e in I.values() for r in e['instead_use'] if r not in NAMES})
if bad_ref:
    sys.exit('instead_use points at icons not in the set: %s' % bad_ref)
bad_cluster = sorted({e['cluster'] for e in I.values()} - set(CLUSTERS))
if bad_cluster:
    sys.exit('unknown clusters: %s' % bad_cluster)

for name, c in CLUSTERS.items():
    c['members'] = sorted(k for k, v in I.items() if v['cluster'] == name)

for k, v in I.items():
    v['has_fill'] = (k + '-fill') in NAMES
    v['confusable_with'] = sorted(set(CLUSTERS[v['cluster']]['members']) - {k})

doc = {
  "name": "open-icons selection rules",
  "version": "1.0.0",
  "grid": 24,
  "generated_by": "tools/build-icon-rules.py — do not hand-edit; has_fill and every "
                  "cross-reference are validated against icons/names.json at build time",
  "purpose": "Selection context for a consuming AI. Answers 'when do I reach for this one "
             "instead of that one', which prose cannot be queried for. Construction rules "
             "— grid, stroke, corners, clearance — are NOT here; they are in "
             "data/construction-tokens.json.",
  "how_to_query": {
    "by_icon": "icons[<name>] — use_when, not_when, instead_use, confusable_with.",
    "by_confusion": "Look up any candidate, read confusable_with, then read the cluster's "
                    "tiebreaker. The tiebreaker names the ONE axis that separates the members.",
    "choosing_a_variant": "See fill_axis. Line is the default; fill is the emphasis style.",
    "choosing_a_container": "See container_shape.",
    "if_absent": "An icon with no entry has no twin worth disambiguating. Absence means "
                 "unambiguous, not undocumented."
  },
  "coverage": {
    "policy": "Confusable clusters only. An entry earns its place by naming what it rules out.",
    "icons_in_set": len(NAMES),
    "icons_with_rules": len(I),
    "clusters": len(CLUSTERS)
  },
  "fill_axis": {
    "rule": "LINE IS THE DEFAULT. Fill is a style you choose when an icon has to carry more "
            "weight than the words around it. Assume line unless there is a reason.",
    "default": "line",
    "endpoints_only": "There is nothing between line and fill. No intermediate values, no "
                      "weight axis, no grade axis. Switching is a swap, not a dial.",
    "use_fill_when": [
      "status and severity — see status_icons, which are filled by default",
      "the item is the selected tab, filter, or nav destination",
      "the marker represents the user's current place or choice",
      "an icon has to survive at a glance in a dense surface and line is losing"
    ],
    "status_icons": {
      "rule": "Status and severity icons ship FILLED. They are the one family where the icon "
              "has to be read before the sentence beside it, and a line glyph does not win "
              "that race.",
      "success": "check-circle-fill",
      "error": "close-circle-fill",
      "warning": "warning-fill",
      "info": "info-fill",
      "note": "The line forms of these still exist and are correct in neutral, non-alerting "
              "contexts — a help link, an inline hint, a list of statuses at rest."
    },
    "do_not_use_fill_when": [
      "the icon is one of many in a toolbar, list or nav at rest — that is line's job",
      "you are reaching for it out of habit rather than to raise emphasis",
      "the icon has no fill variant, which is a construction fact and not an oversight"
    ],
    "no_fill_variant_means": "The icon is built entirely from open strokes and has no interior "
                             "to flood, OR nothing in any product ever needs to emphasise it. "
                             "A fill identical to its line variant is a bug, not a variant.",
    "line_only_families": {
      "map_chrome": ["map", "layers", "route", "compass"],
      "list_markers": ["campfire", "pets", "food", "store", "wifi", "shower"],
      "no_interior": ["picnic-table", "chart", "signal", "activity", "menu", "list"]
    }
  },
  "container_shape": {
    "rule": "A bare mark, a circled mark and a squared mark are three different affordances, "
            "not three styles.",
    "bare": "The mark alone (add, close, check). Inline, or where surrounding chrome already "
            "provides the hit target.",
    "circle": "The mark needs its own hit surface and sits on content — chips, tokens, "
              "avatars, floating controls.",
    "square": "The mark is a form control or sits in a grid of controls — checkboxes, "
              "toolbar cells, anything aligned to a rectangular rhythm.",
    "note": "Do not mix containers within one control group. A circled add beside a squared "
            "close reads as two systems."
  },
  "scopes": {
    "generic": "Universal. Any product, any context.",
    "travel": "Generic within the travel / mapping / booking domain. Opt-in at import.",
    "product": "One product only. Cannot be repurposed.",
    "status": "The `travel` scope is recommended and in use here but not ratified, and nothing "
              "enforces it at import. See docs/decisions.md."
  },
  "clusters": CLUSTERS,
  "icons": dict(sorted(I.items())),
}

out = os.path.join(ROOT, 'data/icon-rules.json')
json.dump(doc, open(out, 'w'), indent=2, ensure_ascii=False)
open(out, 'a').write('\n')
print('wrote %s — %d icons across %d clusters, %d bytes'
      % (out, len(I), len(CLUSTERS), os.path.getsize(out)))
