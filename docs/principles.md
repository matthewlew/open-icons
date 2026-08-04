# Open Icons — ten principles

Everything else in this repo is detail. This is the part that shouldn't change.

If you only read one page here, read this one. It's written for anyone — a
designer, an engineer, a PM, someone who just needs to pick the right icon on a
Tuesday. There are no measurements in it.

---

## 1. Line is the default

Almost every icon, in almost every screen, is a line icon. Toolbars, navigation,
lists, forms, empty states — line.

Line isn't the quiet option or the safe one. It's the normal one. If you're
reaching for something else, you should be able to say why.

## 2. Fill is for emphasis

Use a filled icon when it has to be read *before* the words next to it.

The clearest case is status: a warning, an error, a success, a piece of critical
info. In a banner or an alert, the icon's job is to land first, and a line icon
loses that race. Those ship filled.

The other case is the thing you're currently on — the selected tab, the active
filter, your own location on a map. Fill is the strongest emphasis the system
has, so that's what "you are here" gets.

Outside those two, ask what the fill is doing. If the answer is "it looked
nice", use line.

## 3. One idea, one icon

If two icons mean the same thing, one of them is a bug.

Before anything gets drawn, the first question is what already says it. Most
"missing" icons turn out to be present under a different name. A library that
grows by addition alone stops being a system and becomes a folder.

## 4. An icon that needs explaining has failed

No legend. No tooltip to make it make sense. If someone has to be told what it
is, it isn't doing the job an icon exists to do.

This is a real constraint on ambition. Some ideas are too abstract to draw —
"compliance", "synergy", "eligibility". When that happens the answer is usually
a word, not a cleverer drawing.

## 5. Product need is the reason we add anything

We draw an icon because something real needs it and nothing we have will do.

Not because a set feels incomplete, not because a competitor has one, not
because it might be useful later. The need comes first and it comes from a
product. Right now that's Roadtrip; next time it'll be something else.

## 6. Icons are built from rules, not drawn one at a time

This is the thing that makes the set a set. Every icon is produced by the same
small kit of shapes and spacings, so two hundred of them look like one family
rather than two hundred opinions.

It also means the whole library can be changed at once — made bolder, made
lighter — and everything stays in proportion. A drawing made by hand can't
follow. It's a sketch of an icon, not an icon.

## 7. You bring the idea; the system brings the rest

Your job is the *concept*: what the thing is, what it means, what makes it
recognisable at a glance.

Line weight, corner softness, how much air sits between parts, how the filled
version differs from the line one — all of that is already decided, consistently,
for every icon. It isn't a per-icon choice, and nudging it on one icon is how a
set starts to drift.

## 8. Every size is its own drawing

A small icon is not a big icon shrunk down.

Shrink one and the lines get too thin to survive and the gaps close up into mush.
So each size is drawn again: the shape is placed fresh, the lines are set at the
right weight for that size, and detail is *reduced* rather than crushed. Three
dots become two. Eight teeth become six. The icon keeps its whole vocabulary at
every size — it just says it with fewer words.

## 9. Measure it, then look at it

Both, in that order, always.

Measuring catches what the eye forgives: a gap that's a hair too tight, a shape
that's a fraction off its grid, a filled version heavier than its outline. Looking
catches what measuring can't see at all: that it reads as the wrong object, or
that it's technically perfect and still ugly.

Skipping either one has bitten this project. A set of icons once passed every
number and still had to be rebuilt.

## 10. Write down what you rejected

"We chose this" isn't a decision. It's a preference with a date on it.

"We chose this over that, because that failed in this specific way" — that's a
decision, and it's the only kind that survives. It stops the same argument being
had twice, and it stops a future change quietly undoing a hard-won call without
knowing it.

The test is simple: **if nothing was ruled out, it isn't a decision.** It's just
a fact about the system, and facts belong somewhere else.

---

# How to contribute

## If you just need to pick an icon

1. **Search what exists first.** The name you'd guess is usually the name it has.
2. **If two candidates both seem right,** that's a known ambiguity and there's a
   written answer for it — hamburger vs kebab, plain X vs circled X, line vs
   fill. Ask, or check the selection rules.
3. **Default to line.** See principle 2 before reaching for fill.
4. **If nothing fits,** don't improvise one. Go to the next section.

## If you need a new icon

**Step 1 — Say what it's for.** Not "we need a trailer icon" but "campsites list
whether they take towed units, and there's nothing that says towed". The need,
the screen, the thing a user is trying to tell apart. This is the most useful
thing you can bring and the only step nobody else can do for you.

**Step 2 — We check what's already there.** Often the answer is an existing icon
used correctly, or two existing icons in a pattern. Roughly nineteen in twenty
"new icon" requests end here, and that's a good outcome, not a brush-off.

**Step 3 — We look for the shape underneath.** If three icons you've asked for
share a form, we build the form once and the three fall out of it. Doing it this
way is slower for the first icon and much faster for the next five.

**Step 4 — It gets built and checked.** Generated from the rules, measured
against them, then looked at by a person. Principle 9.

**Step 5 — The reasoning gets written down.** Whatever was rejected on the way —
the drawing that didn't survive, the meaning that turned out to be two meanings —
goes into the record. Principle 10.

## What will get pushed back on

Not to be difficult — each of these has cost us something before:

- **A hand-drawn SVG dropped into the set.** It can't follow the system when the
  system moves. Bring the idea instead and we'll build it.
- **A near-duplicate of something we have.** See principle 3.
- **An icon for an abstract concept.** See principle 4. Usually this wants a word.
- **A one-product icon presented as a general one.** Icons scoped to a product
  leaking into everything else is one of the things this repo exists to stop.
- **"Just make this one a bit lighter."** Line weight is not a per-icon dial.

---

## Where to go deeper

| If you want | Read |
|---|---|
| What we're building toward | [`north-star.md`](north-star.md) |
| Why the system is shaped this way | [`decisions.md`](decisions.md) |
| Exactly how an icon is drawn | [`icon-construction-spec.md`](icon-construction-spec.md) |
| Which icon to reach for, in detail | [`../data/icon-rules.json`](../data/icon-rules.json) |

If this page and any of those disagree, **this page is wrong** — tell us, and
we'll fix it here. Principles that quietly drift out of date are worse than no
principles at all.
