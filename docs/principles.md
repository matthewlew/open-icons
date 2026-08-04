# Open Icons — ten principles

Everything else in this repo is detail. This is the part that shouldn't change.

If you only read one page here, read this one. It's written for anyone — a
designer, an engineer, a PM, someone who just needs to pick the right icon on a
Tuesday. There are no measurements in it.

The first three are about whether to use an icon at all. That order is
deliberate: it's the question people skip.

---

# Before you reach for one

## 1. Sometimes the answer is a word

Not every action needs an icon. Often the clearest thing you can put in front of
someone is the word for what will happen.

Icons added for their own sake are noise. A screen where every row, button and
label carries a glyph has no emphasis left to spend — everything is decorated,
so nothing stands out, and the eye has more to sort through before it finds the
one control that mattered.

The test: **would someone understand this faster with just the word?** If yes,
use the word. "Export CSV" beats a tray-with-an-arrow that people have to stop
and decode. This is especially true for anything abstract — compliance,
eligibility, entitlement. Those don't have shapes, and trying to give them one
produces a symbol nobody can read.

Text is not the fallback for when we couldn't think of an icon. It's frequently
the right answer.

## 2. Icons work by convention, not invention

An icon is recognised from memory. It is not deduced. Nobody looks at a shape
and reasons their way to its meaning — they either already know it or they
don't.

That makes the set of icons that genuinely work without a label quite small, and
it's mostly the ones everybody has already learned:

- **Overflow** — the kebab and the meatball
- **Disclosure** — chevrons and carets, dropdowns, expanding rows
- **Navigation** — back, forward, close, search, home
- **A handful of objects** — trash, printer, calendar, camera

Those are safe because they've been the same for decades across every platform
someone has used. Use icons *there*, where the convention is doing the work.

Outside that set, an icon needs a label beside it — and if it needs a label
anyway, ask principle 1 whether it's earning its space. **You cannot teach a new
symbol inside one product.** People don't arrive willing to learn your
vocabulary; they arrive with the one they already have.

## 3. Icons carry culture

A mark does not mean the same thing everywhere, and the places it differs are
rarely the places you'd guess.

In Japan — and broadly across Japan, Korea and Taiwan — **○ means correct and ✕
means wrong**. A circle is a yes. Western products use ✓ for correct and treat a
circle as neutral: a radio button, a status dot, an empty state. Ship a Western
"select the circle" pattern into a Japanese context and you may be saying
something you didn't intend, in either direction.

That's one example of a general problem:

- **Direction flips.** This set has 53 icons that point somewhere. In
  right-to-left locales — Arabic, Hebrew, Farsi, Urdu — "next" points the other
  way, and an unmirrored arrow means backwards.
- **Objects are local.** A flag-on-a-post mailbox is North American. A dollar
  sign is not currency. A postbox, a plug socket, a light switch — all of these
  look different depending on where you're standing.
- **Hands and gestures carry the most risk.** A thumb, an OK sign, a pointing
  finger: each of these is rude somewhere.

**We have not done this audit yet.** Principle 3 is currently a warning, not a
cleared list — the known hazards in this set are recorded, the full review is
still open. Until it's done, treat any icon that encodes correctness, direction,
a hand, or a physical object as *unverified* outside a Western context.

---

# Choosing and using

## 4. Line is the default

Almost every icon, in almost every screen, is a line icon. Toolbars, navigation,
lists, forms, empty states — line.

Line isn't the quiet option or the safe one. It's the normal one. If you're
reaching for something else, you should be able to say why.

## 5. Fill is for emphasis

Use a filled icon when it has to be read *before* the words next to it.

The clearest case is status: a warning, an error, a success, a piece of critical
info. In a banner or an alert the icon's job is to land first, and a line icon
loses that race. Those ship filled.

The other case is the thing you're currently on — the selected tab, the active
filter, your own location on a map. Fill is the strongest emphasis the system
has, so that's what "you are here" gets.

Outside those two, ask what the fill is doing. If the answer is "it looked
nice", use line.

## 6. The library holds the drawing; the product binds the meaning

The library's job is that there is **one good drawing of each thing** — one
trash can, one calendar, one tent. Two drawings of the same object is
redundancy, and it's a bug.

But an icon is not the same as a meaning, and trying to force them one-to-one
breaks in both directions. **One icon often carries several meanings** — a plus
is add, create, invite and expand depending on where it sits. And **several
icons can be defensible for one action** — remove could be an X, a minus or a
trash can, and which is right depends on what happens next.

That ambiguity is not something to eliminate. It's something to **resolve per
product**, in a manifest: *in this product, this action uses this icon.* Written
down once, it stops being a debate that gets re-had in every review.

> The library says what an icon **is**.
> The product says what it **does here**.

Two products can bind the same icon differently and both be right. What they
can't do is leave it unbound and hope everyone guesses the same way.

## 7. Never brand an icon for a feature

Icons should name **actions**, not features.

The pattern to avoid: a new feature launches, it needs a mark, and it takes an
existing abstract icon as its badge. A sparkle is the usual victim — it's vague
enough to mean anything, so it gets drafted to mean "AI", or "new", or
"premium".

The cost shows up later. Sparkle already meant something concrete in places —
clean this up, highlight this, make this special — and now those uses read as
feature promotion instead. The icon stops being a verb and becomes a campaign,
and it's very hard to take back: every screen that used it innocently now looks
like an ad.

Features get renamed, repositioned and retired. The icon outlives all of that.
Bind an icon to what a user *does*, and it stays true.

---

# Making them

## 8. You bring the idea; the system brings the craft

Your job is the **concept**: what the thing is, what it means, what makes it
recognisable at a glance.

Everything else is already decided, consistently, for every icon — line weight,
corner softness, how much air sits between parts, how the filled version differs
from the line one. It isn't a per-icon choice, and nudging it on one icon is how
a set starts to drift.

This is also why **every size is drawn again rather than scaled down**. Shrink an
icon and the lines get too thin to survive and the gaps close into mush. Each
size gets the shape placed fresh, lines set at the right weight for that size,
and detail *reduced* rather than crushed: three dots become two, eight teeth
become six. The icon keeps its whole vocabulary at every size — it just says it
with fewer words.

A drawing made by hand can't follow any of this when the system moves. It's a
sketch of an icon, not an icon.

## 9. Measure it, then look at it

Both, in that order, always.

Measuring catches what the eye forgives: a gap that's a hair too tight, a shape
that's a fraction off its grid, a filled version heavier than its outline.
Looking catches what measuring can't see at all: that it reads as the wrong
object, or that it's technically perfect and still ugly.

Skipping either one has bitten this project. A set of icons once passed every
number and still had to be rebuilt.

## 10. Write down what you rejected

"We chose this" isn't a decision. It's a preference with a date on it.

"We chose this over that, because that failed in this specific way" — that's a
decision, and it's the only kind that survives. It stops the same argument being
had twice, and it stops a future change quietly undoing a hard-won call without
knowing it.

> The test is simple: **if nothing was ruled out, it isn't a decision.** It's
> just a fact about the system, and facts belong somewhere else.

---

# How to contribute

## If you just need to pick an icon

1. **Ask whether it should be an icon.** Principle 1. A label is often better.
2. **Check the product's manifest.** If your product has bound this action
   already, that binding wins — don't re-litigate it in a review.
3. **Search what exists.** The name you'd guess is usually the name it has.
4. **If two candidates both seem right,** that's a known ambiguity with a written
   answer — hamburger vs kebab, plain X vs circled X, line vs fill.
5. **Default to line.** Principle 4.

## If you need a new icon

**Step 1 — A product need is the reason.** We draw an icon because something
real needs it and nothing we have will do. Not because a set feels incomplete,
not because a competitor has one, not because it might be useful later.

**Step 2 — Say what it's for.** Not "we need a trailer icon" but "campsites list
whether they take towed units, and there's nothing that says towed". The need,
the screen, the thing a user is trying to tell apart. This is the most useful
thing you can bring and the only step nobody else can do for you.

**Step 3 — We check what's already there.** Often the answer is an existing icon
used correctly, an existing icon *bound* in your product's manifest, or two
existing icons in a pattern. Roughly nineteen in twenty "new icon" requests end
here — that's a good outcome, not a brush-off.

**Step 4 — We look for the shape underneath.** If three icons you've asked for
share a form, we build the form once and the three fall out of it. Slower for the
first icon, much faster for the next five.

**Step 5 — It gets built and checked.** Generated from the rules, measured
against them, then looked at by a person. Principle 9.

**Step 6 — The reasoning gets written down.** Whatever was rejected on the way
goes into the record. Principle 10.

## What will get pushed back on

Not to be difficult — each of these has cost something before:

- **An icon where a word would be clearer.** Principle 1, and it's the most
  common one.
- **A hand-drawn SVG dropped into the set.** It can't follow the system when the
  system moves.
- **A second drawing of something we already have.** Principle 6 — note this is
  about the *drawing*, not the meaning. Meanings are allowed to overlap.
- **An icon for an abstract concept.** Usually wants a word.
- **An icon adopted as a feature's badge.** Principle 7.
- **A one-product icon presented as a general one.** Product-scoped icons
  leaking into everything else is one of the things this repo exists to stop.
- **"Just make this one a bit lighter."** Line weight is not a per-icon dial.

---

## Where to go deeper

| If you want | Read |
|---|---|
| What we're building toward | [`north-star.md`](north-star.md) |
| Why the system is shaped this way | [`decisions.md`](decisions.md) |
| Exactly how an icon is drawn | [`icon-construction-spec.md`](icon-construction-spec.md) |
| Which icon to reach for, and the known cultural hazards | [`../data/icon-rules.json`](../data/icon-rules.json) |

If this page and any of those disagree, **this page is wrong** — tell us, and
we'll fix it here. Principles that quietly drift out of date are worse than no
principles at all.
