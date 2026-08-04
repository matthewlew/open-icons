#!/usr/bin/env python3
"""Build data/icon-metadata.json — the per-icon layer.

This is the file the research pass named as the highest-leverage gap: one
sidecar unblocks keyword search, a Figma library with descriptions, aliases,
deprecation pointers and RTL correctness at the same time. Polaris ships it as a
YAML file per icon; here it is one generated JSON, because the set is generated.

Authoring model — rules first, overrides second:

  FAMILY   pattern rules that describe a whole family in one line. The eight
           arrow directions do not want eight hand-written descriptions.
  META     per-icon overrides for anything a rule cannot know.
  derived  has_fill, variants, since — read from names.json and from git, never
           typed, so they cannot drift.

The validator is the point. It exits non-zero if ANY icon lacks a description or
a keyword, if an alias or a deprecation points at something that does not exist,
or if a direction value is not in the vocabulary. Metadata that is allowed to be
partially missing rots immediately.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAMES = json.load(open(os.path.join(ROOT, 'icons/names.json')))
NAMESET = set(NAMES)
VERSION = json.load(open(os.path.join(ROOT, 'package.json')))['version']

# Icons that arrived in the current cycle. Everything else predates the point at
# which this repo started recording, so it gets the honest answer rather than a
# fabricated one.
NEW_THIS_CYCLE = set(json.load(open(os.path.join(ROOT, 'data/added-in-0.12.0.json'))))

# Measured, not judged: an icon whose ink is symmetric about x=12 cannot change
# under a horizontal mirror, so its RTL direction is `none` as a FACT. Produced
# by sampling every icon and comparing each point against its reflection; see
# data/measured-symmetry.json. This is what turns most of the `unreviewed` pile
# into a real answer without anyone having an opinion.
SYMMETRIC = {n for n, v in json.load(
    open(os.path.join(ROOT, 'data/measured-symmetry.json'))).items() if v['symmetric']}

# ---------------------------------------------------------------------------
# Direction vocabulary — Fluent's model, with one addition.
#
#   mirror      flip horizontally in a right-to-left locale
#   none        do not flip; the drawing means the same thing either way
#   unique      needs a separately drawn RTL form, not a flip
#   unreviewed  nobody has decided. NOT a synonym for `none` — it is the
#               honest default, and it keeps the open question machine-visible
#               instead of letting silence read as a decision.
DIRECTIONS = {'mirror', 'none', 'unique', 'unreviewed'}

# Rule: a directional glyph with a horizontal component mirrors; a purely
# vertical or symmetric one does not. Applies to the arrow/chevron/caret
# families only — elsewhere the shape does not encode reading direction.
DIRECTIONAL_FAMILIES = ('arrow-', 'chevron-', 'caret-')

def rule_direction(name):
    if name.startswith(DIRECTIONAL_FAMILIES):
        if re.search(r'-(left|right)$', name):
            return 'mirror'
        if re.search(r'-(up|down)$', name):
            return 'none'
        if name in ('arrow-horizontal', 'arrow-vertical', 'arrow-all'):
            return 'none'
    return None

# ---------------------------------------------------------------------------
# FAMILY rules: (regex, category, naming, description template, keywords)
# `{d}` in a description expands to the direction words in the name.
DIRWORD = {'up': 'up', 'down': 'down', 'left': 'left', 'right': 'right',
           'up-left': 'up and left', 'up-right': 'up and right',
           'down-left': 'down and left', 'down-right': 'down and right'}

FAMILY = [
 (r'^arrow-double-(?P<d>[a-z-]+)$', 'direction', 'literal',
  'A double arrow pointing {d}. Moves further or faster than a single arrow.',
  ['arrow', 'double', 'direction', 'skip', 'fast']),
 (r'^arrow-(?P<d>up|down|left|right|up-left|up-right|down-left|down-right)$',
  'direction', 'literal',
  'An arrow pointing {d}.',
  ['arrow', 'direction', 'next', 'previous', 'move']),
 (r'^chevron-double-(?P<d>[a-z]+)$', 'direction', 'literal',
  'A double chevron pointing {d}. Jumps to the end rather than one step.',
  ['chevron', 'double', 'first', 'last', 'jump']),
 (r'^chevron-(?P<d>up|down|left|right)$', 'direction', 'literal',
  'A chevron pointing {d}. Disclosure and navigation — lighter than an arrow.',
  ['chevron', 'disclosure', 'expand', 'collapse', 'navigate', 'more']),
 (r'^caret-(?P<d>up|down|left|right)$', 'direction', 'literal',
  'A solid caret pointing {d}. Sorting and dropdowns — tighter than a chevron.',
  ['caret', 'triangle', 'dropdown', 'sort', 'select']),
 (r'^cart-(?P<m>[a-z]+)(-fill)?$', 'commerce', 'semantic',
  'A shopping cart with a {m} mark.',
  ['cart', 'basket', 'shop', 'buy', 'checkout']),
]

# ---------------------------------------------------------------------------
# META: per-icon. `d` description, `k` extra keywords, `c` category,
# `n` naming (literal|semantic), `dir` direction override.
def E(d, k=(), c='ui', n='semantic', dir=None):
    return dict(d=d, k=list(k), c=c, n=n, dir=dir)

META = {
 # --- marks ---------------------------------------------------------------
 'add': E('A plus. Create, insert, or add to a collection.', ['plus', 'new', 'create'], 'action', 'literal'),
 'minus': E('A minus. Remove from a collection, or collapse.', ['subtract', 'remove', 'less'], 'action', 'literal'),
 'check': E('A tick. Confirm, complete, or mark as done.', ['tick', 'done', 'confirm', 'yes', 'correct'], 'action', 'literal', 'unreviewed'),
 'close': E('A cross. Close a surface that owns the screen.', ['x', 'cross', 'dismiss', 'cancel', 'exit'], 'action', 'literal', 'unreviewed'),
 'menu': E('Three stacked lines. Opens navigation for the whole view.', ['hamburger', 'nav', 'drawer', 'sidebar'], 'navigation', 'literal'),
 'list': E('Lines with markers. A view-mode toggle: show these as a list.', ['rows', 'view', 'layout', 'bullets'], 'navigation', 'literal'),
 'more-horizontal': E('Three dots in a row. Overflow for the object in front of you.', ['meatball', 'ellipsis', 'overflow', 'options'], 'navigation', 'literal'),
 'more-vertical': E('Three stacked dots. Row-level overflow.', ['kebab', 'ellipsis', 'overflow', 'options', 'row'], 'navigation', 'literal'),
 'arrow-all': E('Arrows to four corners. Move freely, or pan.',
                ['move', 'pan', 'drag', 'reposition', 'fullscreen'], 'direction', 'literal', 'none'),
 'arrow-horizontal': E('A double-headed horizontal arrow. Width, or a two-way exchange.',
                       ['resize', 'width', 'horizontal', 'both ways', 'exchange'], 'direction', 'literal', 'none'),
 'arrow-vertical': E('A double-headed vertical arrow. Height, or a two-way exchange.',
                     ['resize', 'height', 'vertical', 'both ways', 'exchange'], 'direction', 'literal', 'none'),
 'cart': E('A shopping cart. The basket itself.',
           ['basket', 'shop', 'buy', 'checkout', 'bag', 'order'], 'commerce', 'literal'),
 'sort': E('Sort a list.', ['order', 'arrange', 'rank']),
 'sort-order': E('Sort direction — ascending or descending.', ['order', 'ascending', 'descending'], 'ui', 'semantic', 'unreviewed'),
 'swap': E('Exchange two things, or reverse a direction.', ['exchange', 'switch', 'reverse', 'transfer'], 'ui', 'semantic', 'unreviewed'),
 'arrow-turn-left': E('An arrow turning back to the left. Undo or go back a level.', ['undo', 'back', 'return', 'reply'], 'direction', 'literal', 'mirror'),
 'arrow-turn-right': E('An arrow turning forward to the right. Redo or forward.', ['redo', 'forward', 'share', 'next'], 'direction', 'literal', 'mirror'),
 # --- status --------------------------------------------------------------
 'info': E('Neutral context the user did not ask for.', ['information', 'note', 'about', 'detail'], 'status'),
 'help': E('A question mark. The user asked — tooltips and docs.', ['question', 'support', 'faq', 'what'], 'status'),
 'warning': E('A triangle. Something is wrong, at risk, or about to be.', ['alert', 'caution', 'danger', 'attention', 'error'], 'status'),
 'circle': E('A bare circle. The unfilled status dot.', ['dot', 'status', 'ring', 'empty', 'radio'], 'status', 'literal', 'unreviewed'),
 # --- objects & actions ---------------------------------------------------
 'search': E('A magnifying glass. Find something.', ['find', 'magnify', 'lookup', 'query', 'filter'], 'action'),
 'search-add': E('A magnifying glass with a plus. Zoom in.', ['zoom in', 'magnify', 'enlarge', 'closer'], 'action'),
 'search-minus': E('A magnifying glass with a minus. Zoom out.', ['zoom out', 'shrink', 'further', 'wider'], 'action'),
 'filter': E('Narrow a set down.', ['funnel', 'refine', 'narrow', 'facet'], 'action'),
 'edit': E('A pencil. Change something in place.', ['pencil', 'write', 'modify', 'compose', 'rename'], 'action'),
 'trash': E('A bin. Destroy the record — needs confirmation or undo.', ['delete', 'bin', 'remove', 'discard', 'garbage'], 'action'),
 'bookmark': E('Save for the user’s own later retrieval.', ['save', 'later', 'read', 'flag', 'pin'], 'action'),
 'star': E('Favourite or rate.', ['favourite', 'favorite', 'rate', 'rating'], 'action'),
 'heart': E('Public sentiment — like, love, react.', ['like', 'love', 'react', 'favourite'], 'action'),
 'flag': E('Escalate to someone else — report or mark for review.', ['report', 'moderate', 'escalate', 'issue'], 'action'),
 'link': E('Chain links. The address itself.', ['url', 'chain', 'copy link', 'hyperlink'], 'action'),
 'external': E('This leaves the app or opens a new tab.', ['new tab', 'outbound', 'open', 'away'], 'action', 'semantic', 'mirror'),
 'share': E('Hand this content to a person or another app.', ['send', 'export', 'recipient'], 'action', 'semantic', 'unreviewed'),
 'upload': E('Send a file up from the device.', ['import', 'attach', 'send', 'cloud'], 'action', 'semantic', 'none'),
 'download': E('Bring a file down to the device.', ['export', 'save', 'get', 'cloud'], 'action', 'semantic', 'none'),
 'log-out': E('Leave the session.', ['sign out', 'exit', 'logout', 'leave'], 'action', 'semantic', 'mirror'),
 'copy': E('Duplicate to the clipboard.', ['duplicate', 'clipboard', 'clone'], 'action'),
 'refresh': E('Reload or try again.', ['reload', 'retry', 'sync', 'update'], 'action', 'semantic', 'none'),
 'history': E('What happened before.', ['recent', 'past', 'undo', 'log', 'activity'], 'ui', 'semantic', 'none'),
 'settings': E('A cog. Configuration and preferences.', ['cog', 'gear', 'preferences', 'config', 'options'], 'ui'),
 'lock': E('Closed padlock. Restricted or secured.', ['secure', 'private', 'password', 'closed'], 'ui'),
 'lock-open': E('Open padlock. Unrestricted or unlocked.', ['unlock', 'open', 'public', 'access'], 'ui'),
 'eye': E('Visible — preview or reveal.', ['view', 'show', 'preview', 'watch', 'visible'], 'ui'),
 'eye-off': E('Hidden — concealed or muted.', ['hide', 'conceal', 'invisible', 'private'], 'ui'),
 'grid': E('Four cells. A grid view.', ['view', 'layout', 'tiles', 'gallery'], 'ui', 'literal'),
 'grid-masonry': E('A grid with one column merged.', ['layout', 'masonry', 'pinterest', 'staggered'], 'ui', 'literal'),
 'grid-dense': E('Nine cells. A denser grid view.', ['layout', 'compact', 'tiles', 'apps'], 'ui', 'literal'),
 'home': E('A house. The starting place.', ['house', 'start', 'index', 'main', 'dashboard'], 'navigation', 'literal'),
 'file': E('A page with a folded corner.', ['document', 'page', 'doc', 'attachment'], 'object', 'literal'),
 'folder': E('A closed folder.', ['directory', 'collection', 'group'], 'object', 'literal'),
 'folder-open': E('An open folder.', ['directory', 'expanded', 'browse'], 'object', 'literal'),
 'photo': E('An image.', ['image', 'picture', 'media', 'gallery'], 'object', 'literal'),
 'photo-stack': E('Several images.', ['images', 'gallery', 'album', 'media'], 'object', 'literal'),
 'calendar': E('Dates and scheduling.', ['date', 'schedule', 'event', 'month', 'booking'], 'object', 'literal'),
 'clock': E('A time of day.', ['time', 'hour', 'schedule', 'when'], 'object', 'literal'),
 'timer': E('A countdown or elapsed duration.', ['stopwatch', 'countdown', 'duration', 'timing'], 'object', 'literal'),
 'bell': E('Notifications.', ['notification', 'alert', 'ring', 'remind'], 'object', 'literal'),
 'bell-off': E('Notifications silenced.', ['mute', 'silence', 'do not disturb', 'off'], 'object', 'literal'),
 'mail': E('An envelope. Email.', ['email', 'envelope', 'message', 'inbox'], 'object', 'literal'),
 'chat': E('A speech bubble. Conversation.', ['message', 'comment', 'bubble', 'talk', 'support'], 'object', 'literal'),
 'call': E('A handset. Voice call.', ['phone', 'telephone', 'dial', 'voice'], 'object', 'literal'),
 'person': E('One individual — an account, a profile, an assignee.', ['user', 'profile', 'account', 'avatar', 'member'], 'people', 'literal'),
 'people': E('A group, a team, or a social relation.', ['users', 'group', 'team', 'members', 'shared'], 'people', 'literal'),
 'person-add': E('Invite or add a person.', ['invite', 'add user', 'new member'], 'people'),
 'person-check': E('A person confirmed or approved.', ['approved', 'verified', 'accepted'], 'people'),
 'pin': E('A tack. The act of fastening something in place.', ['tack', 'stick', 'keep', 'fix', 'top'], 'object', 'literal'),
 'location': E('A map marker. Where something is.', ['place', 'marker', 'map', 'address', 'where', 'gps'], 'travel', 'literal'),
 'navigation': E('A heading or an active route.', ['direction', 'compass', 'route', 'go', 'heading'], 'travel', 'literal', 'unreviewed'),
 'money': E('A note. Currency and payment.', ['cash', 'payment', 'currency', 'price', 'billing'], 'commerce', 'literal', 'unreviewed'),
 'price': E('A tag. What something costs.', ['tag', 'cost', 'label', 'discount', 'offer'], 'commerce', 'literal'),
 'play': E('Start playback.', ['start', 'resume', 'media', 'video'], 'media', 'literal', 'none'),
 'pause': E('Suspend playback.', ['stop', 'hold', 'media'], 'media', 'literal', 'none'),
 'skip-forward': E('Jump to the next item.', ['next', 'forward', 'advance', 'media'], 'media', 'literal', 'none'),
 'skip-back': E('Jump to the previous item.', ['previous', 'back', 'rewind', 'media'], 'media', 'literal', 'none'),
 'volume': E('Audio at normal level.', ['sound', 'audio', 'speaker', 'loud'], 'media', 'literal', 'none'),
 'volume-low': E('Audio at a low level.', ['sound', 'quiet', 'audio', 'speaker'], 'media', 'literal', 'none'),
 'volume-off': E('Audio muted.', ['mute', 'silent', 'sound off', 'quiet'], 'media', 'literal', 'none'),
 'radio-off': E('An unselected radio button.', ['unselected', 'option', 'choice', 'form'], 'form', 'literal'),
 'radio-on': E('A selected radio button.', ['selected', 'chosen', 'option', 'form'], 'form', 'literal'),
 'checkbox-off': E('An unchecked box.', ['unchecked', 'empty', 'form', 'select'], 'form', 'literal'),
 'checkbox-on': E('A checked box.', ['checked', 'ticked', 'selected', 'form'], 'form', 'literal'),
 'checkbox-mixed': E('A box in an indeterminate state.', ['indeterminate', 'partial', 'mixed', 'form'], 'form', 'literal'),
 # --- map chrome ----------------------------------------------------------
 'map': E('A folded map. The map view itself.', ['atlas', 'plan', 'fold', 'geography'], 'travel', 'literal'),
 'layers': E('Stacked plates. Map layers or z-order.', ['stack', 'overlay', 'levels', 'z-index'], 'travel', 'literal'),
 'route': E('A path between two points.', ['journey', 'trip', 'path', 'directions', 'itinerary'], 'travel', 'semantic', 'mirror'),
 'compass': E('A ring and a needle. Orientation.', ['direction', 'bearing', 'explore', 'north'], 'travel', 'literal', 'none'),
 # --- data & status -------------------------------------------------------
 'chart': E('Columns of varying height. Values across categories.', ['bar chart', 'data', 'stats', 'analytics', 'report'], 'data', 'literal'),
 'signal': E('Bars in even steps. Strength on an ordered scale.', ['strength', 'reception', 'bars', 'coverage', 'cell'], 'data', 'literal'),
 'activity': E('A continuous trace with a spike. Something happening now.', ['pulse', 'live', 'heartbeat', 'realtime', 'monitor'], 'data', 'literal'),
 'bolt': E('A lightning bolt. Power, speed, or charge.', ['lightning', 'power', 'fast', 'energy', 'charge', 'flash'], 'travel', 'literal'),
 # --- travel & outdoors ---------------------------------------------------
 'campsite': E('One tent. A specific, reservable pitch.', ['tent', 'camp', 'pitch', 'site', 'booking'], 'travel'),
 'campground': E('Two tents. The whole facility or area.', ['camp', 'campsite', 'facility', 'park', 'sites'], 'travel'),
 'mountain': E('A range with a snow line. Terrain and elevation.', ['peak', 'hill', 'terrain', 'scenery', 'elevation', 'hike'], 'travel'),
 'park': E('A tree. Maintained green space.', ['tree', 'green', 'nature', 'shade', 'garden'], 'travel'),
 'picnic-table': E('A picnic table. Somewhere to sit and eat.', ['table', 'bench', 'eat', 'rest', 'day use'], 'travel'),
 'car': E('A car. A standard vehicle.', ['vehicle', 'auto', 'drive', 'parking', 'sedan'], 'travel', 'literal'),
 'rv': E('A motorhome with a cab-over. A large self-propelled vehicle.', ['motorhome', 'camper', 'winnebago', 'coach', 'vehicle'], 'travel', 'literal'),
 'trailer': E('A towed unit with a tongue.', ['caravan', 'towed', 'towing', 'hitch', 'camper'], 'travel', 'literal'),
 'ev-charger': E('A charging pedestal with a plug. Electric charging.', ['electric', 'charge', 'ev', 'supercharger', 'plug'], 'travel'),
 'fuel': E('A pump dispensing liquid. A fuel stop.', ['petrol', 'gas', 'diesel', 'pump', 'station'], 'travel'),
 'water': E('A droplet. Potable water as an amenity.', ['drinking', 'potable', 'tap', 'spigot', 'fill'], 'travel'),
 'parking': E('A P in a box. Parking.', ['park', 'car park', 'lot', 'space'], 'travel'),
 'restroom-figures': E('Two figures. A restroom, without claiming plumbing.', ['toilet', 'bathroom', 'wc', 'washroom', 'facilities'], 'travel'),
 'shower': E('A head and falling water.', ['wash', 'bathe', 'facilities', 'bathroom'], 'travel'),
 'campfire': E('A flame over crossed logs.', ['fire', 'flame', 'bonfire', 'wood', 'burn'], 'travel'),
 'pets': E('A paw print. Animals welcome.', ['dog', 'animal', 'paw', 'pet friendly', 'cat'], 'travel'),
 'food': E('A fork and spoon. Food available.', ['eat', 'restaurant', 'dining', 'meal', 'cafe'], 'travel'),
 'store': E('A shopfront under an awning. A place to buy things.', ['shop', 'market', 'retail', 'supplies', 'general store'], 'travel'),
 'wifi': E('Waves from a point. Wireless network.', ['internet', 'wireless', 'network', 'connection', 'hotspot'], 'travel', 'literal'),
}

# Containers and their marks — generated rather than typed out.
MARKWORD = {'add': 'plus', 'minus': 'minus', 'check': 'tick', 'close': 'cross'}
MARKJOB = {'add': 'Add or create', 'minus': 'Remove or collapse',
           'check': 'Confirm or complete', 'close': 'Dismiss or clear'}
for _m, _w in MARKWORD.items():
    for _shape in ('circle', 'square'):
        META['%s-%s' % (_m, _shape)] = E(
            '%s, in a %s. %s.' % (_w.capitalize(), _shape, MARKJOB[_m]),
            [_m, _w, _shape, 'contained'], 'action', 'literal',
            'unreviewed' if _m in ('check', 'close') else None)

ALIASES = {
 # the redundancy call the proposal recorded: these ARE the zoom controls
 'zoom-in': 'search-add', 'zoom-out': 'search-minus',
 'drag-handle': 'more-vertical',
 # names people actually type
 'hamburger': 'menu', 'kebab': 'more-vertical', 'meatball': 'more-horizontal',
 'ellipsis': 'more-horizontal', 'dots': 'more-horizontal',
 'cog': 'settings', 'gear': 'settings', 'preferences': 'settings',
 'bin': 'trash', 'delete': 'trash', 'garbage': 'trash',
 'magnifier': 'search', 'magnifying-glass': 'search', 'find': 'search',
 'tick': 'check', 'x': 'close', 'cross': 'close', 'cancel': 'close',
 'pencil': 'edit', 'compose': 'edit', 'write': 'edit',
 'favorite': 'star', 'favourite': 'star', 'like': 'heart',
 'user': 'person', 'avatar': 'person', 'profile': 'person',
 'users': 'people', 'group': 'people', 'team': 'people',
 'email': 'mail', 'envelope': 'mail',
 'phone': 'call', 'telephone': 'call',
 'image': 'photo', 'picture': 'photo',
 'plus': 'add', 'subtract': 'minus',
 'notification': 'bell', 'alert': 'warning', 'caution': 'warning',
 'gas': 'fuel', 'petrol': 'fuel', 'diesel': 'fuel',
 'toilet': 'restroom-figures', 'bathroom': 'restroom-figures', 'wc': 'restroom-figures',
 'tent': 'campsite', 'caravan': 'trailer', 'motorhome': 'rv',
 'dog': 'pets', 'paw': 'pets',
 'lightning': 'bolt', 'flash': 'bolt', 'power': 'bolt',
}

# Nothing is deprecated yet. The field exists so the first one has somewhere to
# go, and so consumers can rely on its shape from v0.12.0 rather than from
# whenever we first need it. {name: replacement-or-None}
DEPRECATED = {}

# ---------------------------------------------------------------------------
def build_entry(name):
    base = META.get(name)
    if base is None:
        for pat, cat, naming, tmpl, kw in FAMILY:
            m = re.match(pat, name)
            if not m:
                continue
            g = m.groupdict()
            desc = tmpl.format(d=DIRWORD.get(g.get('d', ''), g.get('d', '')),
                               m=g.get('m', ''))
            base = E(desc, kw + [w for w in re.split(r'[-]', name) if len(w) > 2],
                     cat, naming)
            break
    if base is None:
        # a -fill inherits its line partner's copy; the variant field carries
        # the difference, so duplicating the description would only rot
        if name.endswith('-fill') and name[:-5] in NAMESET:
            return None
        return 'MISSING'

    stated = base['dir'] or rule_direction(name)
    if name in SYMMETRIC:
        # measurement beats opinion, and a stated `mirror` on a symmetric glyph
        # is a contradiction worth failing the build over
        if stated == 'mirror':
            CONFLICTS.append(name)
        direction = 'none'
    else:
        direction = stated or 'unreviewed'
    return {
      'description': base['d'],
      'keywords': sorted(set(k.lower() for k in base['k'])),
      'category': base['c'],
      'naming': base['n'],
      'direction': direction,
      'status': 'deprecated' if name in DEPRECATED else 'stable',
      'deprecated_by': DEPRECATED.get(name),
      'since': VERSION if name in NEW_THIS_CYCLE else 'pre-0.12.0',
      'has_fill': (name + '-fill') in NAMESET,
    }

CONFLICTS = []
icons, missing = {}, []
for n in NAMES:
    if n.endswith('-fill'):
        continue                      # a fill is a variant, not an entry
    e = build_entry(n)
    if e == 'MISSING' or e is None:
        missing.append(n)
    else:
        icons[n] = e

# ---- validation: the reason this file is worth having ----------------------
errors = []
if CONFLICTS:
    errors.append('declared `mirror` but measured symmetric (mirroring is a '
                  'no-op for these): %s' % ', '.join(sorted(CONFLICTS)))
if missing:
    errors.append('no description for: %s' % ', '.join(sorted(missing)))
for n, e in icons.items():
    if not e['description'].strip():
        errors.append('%s: empty description' % n)
    if not e['keywords']:
        errors.append('%s: no keywords' % n)
    if e['direction'] not in DIRECTIONS:
        errors.append('%s: direction %r not in %s' % (n, e['direction'], sorted(DIRECTIONS)))
    if e['deprecated_by'] and e['deprecated_by'] not in NAMESET:
        errors.append('%s: deprecated_by points at missing %r' % (n, e['deprecated_by']))
for a, t in ALIASES.items():
    if t not in NAMESET:
        errors.append('alias %r -> missing icon %r' % (a, t))
    if a in NAMESET:
        errors.append('alias %r collides with a real icon name' % a)
if errors:
    sys.exit('icon-metadata: %d problem(s)\n  ' % len(errors) + '\n  '.join(errors))

by_dir = {}
for e in icons.values():
    by_dir[e['direction']] = by_dir.get(e['direction'], 0) + 1

doc = {
  'name': 'open-icons metadata',
  'version': VERSION,
  'grid': 24,
  'generated_by': 'tools/build-icon-metadata.py — do not hand-edit. The build '
                  'exits non-zero if any icon lacks a description or keyword, or '
                  'if an alias or deprecation points at something that does not '
                  'exist, so this file cannot rot silently as icons are added.',
  'schema': {
    'description': 'One sentence. What the drawing is, and what it is for.',
    'keywords': 'Search terms, including words that are NOT in the name.',
    'category': 'Grouping for browse UIs. Not a scope — see icon-rules.json.',
    'naming': 'literal = the name describes the drawing and the icon is '
              'multi-purpose. semantic = the name describes one job. Atlassian’s '
              'split; ours had it by accident and now it is written down.',
    'direction': 'RTL behaviour. mirror | none | unique | unreviewed. '
                 '`unreviewed` is NOT a synonym for `none` — it is the honest '
                 'default and keeps the open question visible.',
    'status': 'stable | deprecated.',
    'deprecated_by': 'The replacement icon, when status is deprecated.',
    'since': 'Version the icon first shipped in.',
    'has_fill': 'Whether a -fill variant exists. Derived, never typed.',
  },
  'conventions': {
    'variants': 'A fill is a variant of its line icon, not a separate entry. '
                'Look up `warning`, read has_fill, then use `warning-fill`.',
    'aliases': 'Alternate names resolve to a real icon. They are search terms '
               'and redirects, not icons — nothing is drawn twice.',
    'rtl_status': '`none` is assigned two ways: measured (the icon is symmetric '
                  'about x=12, so a mirror is a no-op — a fact) or ruled (a '
                  'purely vertical arrow/chevron/caret). `mirror` is a human '
                  'call on the horizontal directional families. Everything left '
                  'as `unreviewed` still needs the locale audit in '
                  'docs/decisions.md — silence is not a decision.',
    'rtl_method': 'tools/build-icon-metadata.py reads data/measured-symmetry.json, '
                  'produced by sampling every icon and comparing each point '
                  'against its reflection. Regenerate it if geometry changes.',
  },
  'counts': {
    'icons_in_set': len(NAMES),
    'entries': len(icons),
    'fill_variants': len(NAMES) - len(icons),
    'aliases': len(ALIASES),
    'deprecated': len(DEPRECATED),
    'by_direction': dict(sorted(by_dir.items())),
  },
  'aliases': dict(sorted(ALIASES.items())),
  'icons': dict(sorted(icons.items())),
}

out = os.path.join(ROOT, 'data/icon-metadata.json')
json.dump(doc, open(out, 'w'), indent=2, ensure_ascii=False)
open(out, 'a').write('\n')
print('wrote %s — %d entries, %d fill variants, %d aliases, %d bytes'
      % (out, len(icons), len(NAMES) - len(icons), len(ALIASES), os.path.getsize(out)))
print('   direction: %s' % ', '.join('%s %d' % kv for kv in sorted(by_dir.items())))
