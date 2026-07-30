"""Build the Open Icons site: one self-contained HTML file.

The set is re-derived at every weight on the axis and all of them are embedded,
because the whole claim of this library is that a weight is a different drawing
rather than the same paths at a different `stroke-width`. A site that could only
ship one weight and restyle it would be arguing against its own thesis.

Four full sets of 174 icons is a lot of string, so the markup is tokenised: the
recurring attribute runs become one control byte plus an index, and the page
expands them back on load. Coordinates round to 2dp, which is a twentieth of a
pixel at 24 and invisible at 48.

    python3 tools/site.py

Writes site/index.html from site/template.html.
"""
import base64
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import generate as gen  # noqa: E402

WEIGHTS = [1.0, 1.5, 2.0, 2.5]

# The sibling checkout that carries the actual design system. Same convention
# palette/scripts/sync-icons.mjs uses for the reverse direction (this repo's
# icons, read by a sibling) — a fixed relative path, no registry, no version
# pin, because both repos live in one workspace and move together.
LDS_ROOT = os.path.join(ROOT, '..', 'matthewlew.github.io', 'design-system', 'dist')

# Longest first: the table is applied in order, so a short token must not eat
# the prefix of a long one before the long one gets its turn.
TOKENS = [
    ' fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"',
    ' fill="none" stroke="#000" stroke-linecap="round" stroke-linejoin="round"',
    '<rect width="24" height="24" fill="#fff"/>',
    ' stroke-linecap="round" stroke-linejoin="round"',
    'maskUnits="userSpaceOnUse"',
    ' fill="none" stroke="currentColor"',
    ' fill="currentColor" stroke="currentColor"',
    ' fill="none" stroke="#000"',
    ' stroke-linejoin="round"',
    ' fill="currentColor"',
    ' stroke-width="',
    '<path d="',
    '<circle cx="',
    'mask="url(#',
    ' fill="#fff"',
    ' fill="#000"',
    '${u}',
    '"/><',
]
TOKENS.sort(key=len, reverse=True)
assert len(TOKENS) <= 60, 'token index must stay in one printable byte'


def round2(markup):
    return re.sub(r'-?\d+\.\d+',
                  lambda m: '%g' % round(float(m.group()), 2), markup)


def pack(markup):
    for i, t in enumerate(TOKENS):
        markup = markup.replace(t, '\x01' + chr(48 + i))
    return markup


# ---------------------------------------------------------------------------
# Metadata. Categories are for the filter; keywords are for the search box, and
# only exist where the name alone would not find the icon (nobody types
# "log-out" when they mean "sign out").
# ---------------------------------------------------------------------------
CATEGORY = [
    ('Direction', ('arrow-', 'chevron-', 'caret-'),
     ('navigation',)),
    ('Action', (),
     ('add', 'close', 'check', 'minus', 'copy', 'download', 'upload', 'edit',
      'trash', 'share', 'refresh', 'search', 'search-add', 'search-minus',
      'filter', 'sort', 'sort-order', 'link', 'external', 'log-out', 'swap',
      'pin', 'settings', 'menu', 'more-horizontal', 'more-vertical')),
    ('Status', (),
     ('info', 'help', 'warning', 'check-circle', 'close-circle', 'add-circle',
      'minus-circle', 'add-square', 'check-square', 'close-square',
      'minus-square', 'eye', 'eye-off', 'lock', 'lock-open', 'bell', 'bell-off',
      'history', 'clock', 'timer')),
    ('Form', ('checkbox-', 'radio-'), ()),
    ('Media', ('skip-', 'volume'),
     ('play', 'pause')),
    ('Commerce', ('cart',),
     ('money', 'price')),
    ('People', ('person', 'people'), ()),
    ('Content', (),
     ('file', 'folder', 'folder-open', 'photo', 'photo-stack', 'grid',
      'grid-dense', 'grid-masonry', 'list', 'calendar', 'mail', 'chat', 'call',
      'bookmark', 'flag', 'star', 'heart', 'home', 'location')),
]

KEYWORDS = {
    'log-out': 'sign out exit logout leave',
    'external': 'new window open outside launch',
    'more-horizontal': 'ellipsis overflow kebab meatball',
    'more-vertical': 'ellipsis overflow kebab',
    'close': 'x cross dismiss cancel',
    'check': 'tick done confirm success',
    'edit': 'pencil write compose rename',
    'trash': 'delete remove bin',
    'photo': 'image picture',
    'photo-stack': 'images gallery album',
    'people': 'group team users',
    'person': 'user account profile avatar',
    'money': 'cash currency payment',
    'price': 'tag label cost',
    'chat': 'message comment speech bubble',
    'call': 'phone telephone dial',
    'mail': 'email envelope inbox message',
    'bell': 'notification alert alarm',
    'star': 'favorite rate rating',
    'heart': 'like love favorite save',
    'bookmark': 'save read later',
    'pin': 'pin push pin stick attach keep',
    'location': 'map marker place where address geo',
    'grid': 'layout tiles view gallery',
    'grid-dense': 'layout compact small tiles view',
    'grid-masonry': 'layout waterfall staggered pinterest view',
    'list': 'rows bullets index',
    'menu': 'hamburger nav navigation',
    'settings': 'gear cog preferences options config',
    'refresh': 'reload sync retry rotate',
    'swap': 'exchange transfer switch reverse',
    'sort': 'order arrange rank',
    'filter': 'funnel refine narrow',
    'link': 'chain url anchor copy link',
    'lock': 'secure private locked',
    'lock-open': 'unlock unsecured public',
    'eye': 'view visible show preview',
    'eye-off': 'hide hidden invisible conceal',
    'warning': 'caution alert danger error',
    'help': 'question support faq',
    'info': 'about details information',
    'home': 'house dashboard start',
    'file': 'document page doc',
    'folder': 'directory files',
    'clock': 'time recent schedule',
    'timer': 'stopwatch countdown duration',
    'history': 'recent undo revert past',
    'calendar': 'date schedule event day',
    'navigation': 'compass direction locate route',
    'arrow-all': 'move drag pan reposition',
    'checkbox-mixed': 'indeterminate partial some',
    'volume': 'sound audio speaker loud',
    'volume-off': 'mute silent sound off',
    'skip-forward': 'next track forward',
    'skip-back': 'previous track rewind back',
    'swap-': '',
}


def categorise(base):
    for label, prefixes, exact in CATEGORY:
        if base in exact:
            return label
        for p in prefixes:
            if base.startswith(p):
                return label
    return 'Content'


def build():
    sets = {}
    for w in WEIGHTS:
        raw = gen.build(w)
        sets['%g' % w] = {k: pack(round2(v)) for k, v in sorted(raw.items())}

    names = sorted(gen.build(2.0))
    at2 = gen.build(2.0)

    meta = {}
    for n in names:
        base = n[:-5] if n.endswith('-fill') else n
        meta[n] = {
            'c': categorise(base),
            'f': 1 if n.endswith('-fill') else 0,
            'm': 1 if '${u}' in at2[n] else 0,
            'k': KEYWORDS.get(base, ''),
        }

    counts = {}
    for n in names:
        counts[meta[n]['c']] = counts.get(meta[n]['c'], 0) + 1

    return {
        'tok': TOKENS,
        'weights': ['%g' % w for w in WEIGHTS],
        'names': names,
        'meta': meta,
        'cats': [c for c, _, _ in CATEGORY],
        'counts': counts,
        'sets': sets,
    }


# Only `core` (no theme class — the portfolio's own identity) uses custom
# faces; `theme-product` and `theme-palette` both declare system-font stacks,
# so those two ride free. Embedding is what an Artifact's CSP requires — it
# blocks every external request, including a same-origin `url('fonts/…')`.
FONT_FILES = [
    'Coconat-Regular', 'Coconat-Demi', 'Coconat-Bold',
    'Ronzino-Regular', 'Ronzino-Medium', 'Ronzino-Bold',
    'MartianMono-Regular', 'MartianMono-Medium', 'MartianMono-SemiBold',
]


def read(*parts):
    with open(os.path.join(LDS_ROOT, *parts), encoding='utf-8') as f:
        return f.read()


def build_lds():
    """Bundle the design system as one CSS string, load order preserved:
       hue ramps, then core, then the two system-font themes. `core.css`'s
       @font-face block still points at 'fonts/Name.woff2'; inline each as a
       base64 data URI so the stylesheet needs no second request — an Artifact
       has no server behind it to serve that request from."""
    css = read('apca-palette.css') + '\n' + read('lds.css')

    def inline(m):
        name = m.group(1)
        with open(os.path.join(LDS_ROOT, 'fonts', name + '.woff2'), 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('ascii')
        return "url(data:font/woff2;base64,%s)" % b64

    missing = [n for n in FONT_FILES
               if ("fonts/%s.woff2" % n) not in css]
    assert not missing, 'lds.css no longer references: %s' % missing
    css, n = re.subn(r"url\('fonts/([\w-]+)\.woff2'\)", inline, css)
    assert n == len(FONT_FILES), 'expected %d font urls, inlined %d' % (len(FONT_FILES), n)
    assert "url('fonts/" not in css, 'a font url survived inlining'

    css += '\n' + read('themes', 'product.css')
    css += '\n' + read('themes', 'palette.css')
    return css


def main():
    data = build()
    payload = json.dumps(data, separators=(',', ':'))
    lds_css = build_lds()

    tpl_path = os.path.join(ROOT, 'site', 'template.html')
    with open(tpl_path, encoding='utf-8') as f:
        tpl = f.read()

    marker = '@@DATA@@'
    assert tpl.count(marker) == 1, 'template must hold exactly one %s' % marker
    # The payload sits inside a <script>, which the HTML tokeniser reads as raw
    # text until it meets "</script". The markup is full of closing tags, so
    # every "<" becomes a < escape. That is legal JSON and JSON.parse gives
    # the character back; and "<" only ever occurs inside a string value here,
    # never as JSON structure, so a blanket replace cannot corrupt the shape.
    payload = payload.replace('<', '\\u003c')
    assert '<' not in payload
    out = tpl.replace(marker, payload)

    lds_marker = '@@LDS_CSS@@'
    assert out.count(lds_marker) == 1, 'template must hold exactly one %s' % lds_marker
    # Same hazard, same fix: the bundle carries raw CSS (comments, selectors)
    # but no markup, so this is a purely defensive escape, not a live case.
    out = out.replace(lds_marker, lds_css.replace('</', '<\\/'))

    dest = os.path.join(ROOT, 'site', 'index.html')
    # No <meta charset> reaches the artifact wrapper, so anything non-ASCII is
    # at the mercy of the server default. Entities are not.
    with open(dest, 'w', encoding='ascii', errors='xmlcharrefreplace') as f:
        f.write(out)

    print('%d icons x %d weights -> %s (%.0f KB)'
          % (len(data['names']), len(data['weights']), dest,
             os.path.getsize(dest) / 1024))
    print('   icon payload %.0f KB, lds bundle %.0f KB, page chrome %.0f KB'
          % (len(payload) / 1024, len(lds_css) / 1024,
             (len(out) - len(payload) - len(lds_css)) / 1024))


if __name__ == '__main__':
    main()
