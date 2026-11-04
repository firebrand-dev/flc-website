---
name: Forever Leveling Companion
description: The official website of FLC, a free leveling companion addon for World of Warcraft Forever, bound as an adventurer's codex.
colors:
  leather-950: "#090706"
  leather-900: "#100d0b"
  leather-850: "#15110e"
  leather-800: "#1b1612"
  leather-700: "#261f19"
  leather-600: "#3a2f24"
  text: "#ede4cc"
  text-2: "#cbc1a8"
  text-3: "#ada389"
  gilt: "#c9a24d"
  gilt-hi: "#e3c47c"
  gilt-lo: "#7a6232"
  vellum: "#e9dcbc"
  vellum-2: "#ddcca2"
  vellum-3: "#cbb789"
  ink: "#2a2016"
  ink-2: "#4f4130"
  rubric: "#8f2a17"
  rubric-deep: "#6e1e0f"
  rubric-ink: "#7c2412"
  seal-green: "#2f8a5f"
  seal-green-text: "#93e0b8"
  seal-amber: "#c4862c"
  seal-amber-text: "#f2c776"
  waypoint: "#4fc3c0"
typography:
  display:
    fontFamily: "IM Fell English SC, Iowan Old Style, Palatino Linotype, Georgia, serif"
    fontSize: "clamp(2.3rem, 1.4rem + 3.2vw, 4rem)"
    fontWeight: 400
    lineHeight: 1.04
    letterSpacing: "0.005em"
  quest-title:
    fontFamily: "IM Fell English SC, Iowan Old Style, Palatino Linotype, Georgia, serif"
    fontSize: "clamp(2.1rem, 1.3rem + 2vw, 3.2rem)"
    fontWeight: 400
    lineHeight: 1.02
  headline:
    fontFamily: "IM Fell English SC, Iowan Old Style, Palatino Linotype, Georgia, serif"
    fontSize: "clamp(1.75rem, 1.2rem + 1.8vw, 2.6rem)"
    fontWeight: 400
    lineHeight: 1.02
    letterSpacing: "0.005em"
  rubric-label:
    fontFamily: "IM Fell English SC, Iowan Old Style, Palatino Linotype, Georgia, serif"
    fontSize: "1.35rem"
    fontWeight: 400
    lineHeight: 1.12
  title:
    fontFamily: "Alegreya Sans, Segoe UI, system-ui, sans-serif"
    fontSize: "1.22rem"
    fontWeight: 700
    lineHeight: 1.12
  body:
    fontFamily: "Alegreya Sans, Segoe UI, system-ui, sans-serif"
    fontSize: "1.125rem"
    fontWeight: 400
    lineHeight: 1.62
  caption:
    fontFamily: "Alegreya Sans, Segoe UI, system-ui, sans-serif"
    fontSize: "0.95rem"
    fontWeight: 400
    lineHeight: 1.3
  mono:
    fontFamily: "ui-monospace, Cascadia Mono, Consolas, Liberation Mono, monospace"
    fontSize: "0.86em"
    fontWeight: 400
rounded:
  leaf: "1px"
  edge: "2px"
  pill: "999px"
  seal: "50%"
spacing:
  gutter: "clamp(16px, 4vw, 48px)"
  wrap: "1240px"
  masthead: "1360px"
  narrow: "860px"
  touch: "44px"
  chapter: "clamp(20px, 3vw, 36px)"
  folio: "clamp(28px, 4vw, 56px)"
  section: "clamp(48px, 7vw, 96px)"
components:
  button-primary:
    backgroundColor: "{colors.rubric}"
    textColor: "#f8eed6"
    typography: "{typography.title}"
    rounded: "{rounded.edge}"
    padding: "0.7em 1.3em"
    height: "48px"
  button-primary-big:
    backgroundColor: "{colors.rubric}"
    textColor: "#f8eed6"
    rounded: "{rounded.edge}"
    padding: "0.85em 1.6em"
    height: "56px"
  button-ghost:
    backgroundColor: "{colors.leather-800}"
    textColor: "{colors.text}"
    rounded: "{rounded.edge}"
    padding: "0.7em 1.3em"
    height: "48px"
  button-ghost-on-leaf:
    textColor: "{colors.ink}"
    rounded: "{rounded.edge}"
    padding: "0.7em 1.3em"
    height: "48px"
  button-quiet:
    textColor: "{colors.text-2}"
    padding: "0.7em 0.5em"
    height: "44px"
  masthead-download:
    backgroundColor: "{colors.rubric}"
    textColor: "#f8eed6"
    rounded: "{rounded.edge}"
    padding: "0 14px"
    height: "44px"
  leaf:
    backgroundColor: "{colors.vellum}"
    textColor: "{colors.ink}"
    rounded: "{rounded.leaf}"
  folio:
    backgroundColor: "{colors.leather-700}"
    textColor: "{colors.text}"
    padding: "clamp(28px, 4vw, 56px) clamp(24px, 4vw, 56px) clamp(36px, 5vw, 64px)"
  plate:
    backgroundColor: "{colors.leather-950}"
    padding: "5px"
  nav-link:
    textColor: "{colors.text-2}"
    padding: "8px 12px"
    height: "44px"
  nav-link-current:
    textColor: "{colors.text}"
  count:
    backgroundColor: "{colors.gilt-hi}"
    textColor: "{colors.leather-950}"
    rounded: "{rounded.pill}"
    padding: "2px 9px"
---

# Design System: Forever Leveling Companion

## Overview

**Creative North Star: "The Adventurer's Codex"**

The site is a book an adventurer carries. The ground is a midnight leather binding (a tiled leather texture over near-black brown); the reading surfaces that matter most are parchment leaves written in iron-gall ink; quest titles and the one primary action are rubricated in red, as a scribe would mark the line a reader must not miss; gold-leaf rules divide, frame and underline; proof is pressed as wax seals. FLC's real windows are pasted into the codex as plates with photo corners, at their native size, never redrawn and never stretched.

Pages are chapters, not sections. On the home page a dashed gold route runs down the codex margin with a rubric diamond waypoint at every chapter opening, each chapter is a folio (a tooled leather panel, a ruled spread, an inset panel, or loose matter on the binding) and carries a small italic folio number ("fol. i") at its foot. The hero is the quest you accept: the real in-game scene fills the first viewport and a parchment quest page sits inside it with its objectives and counts. Density is that of a well-set book: generous measure limits (56 to 66ch), large reading type, and few elements per spread.

The world refuses the split SaaS hero, rows of icon cards and glossy buttons. Motion is one grammar only: an ink check drawn once when an objective or install step is ticked, and the count stepping. Nothing animates on entry.

**Key Characteristics:**
- Leather ground, parchment leaves, gold-leaf rules, rubric red, wax seals; nothing else carries meaning.
- Captures are plates: native size, gold-lo frame, vellum photo corners, a provenance line under every one.
- FLC's own objective format (diamond marker, mono count "0/2") reused as the site's list of things to do.
- IM Fell English SC for titles, Alegreya Sans for reading, a system mono for commands and counts.
- Square, bookbound corners (1 to 2px); depth from paper lift, never from floating cards.

## Colors

A warm, low-light palette: brown-black leather, cream ink, aged gold, one rubric red, and two seal colours reserved for test status.

### Primary
- **Rubric Red** (`rubric`, with `rubric-deep` for the lower stop of its gradient): the primary action button's face, the phone masthead Download, chapter waypoints on the route, and the compare slider's accent. It is the only saturated warm colour on the page.
- **Rubric Ink** (`rubric-ink`): red written on parchment. Quest titles, release and board titles, leaf links, objective diamonds, drop caps and folio numbers on a leaf.

### Secondary
- **Gold Leaf** (`gilt`, `gilt-hi`, `gilt-lo`): rules, frames, underlines and small marks on the binding. `gilt-hi` for links and gilt headings on leather (rules list terms, install move titles, table heads, footer heads), `gilt` for nav underlines, folio numbers and icons, `gilt-lo` for plate frames and quiet button borders. Rules use it translucent: `rgba(201,162,77,.34)` for structural rules and `.17` for soft dividers.

### Tertiary
- **Seal Green** (`seal-green`, text `seal-green-text`): "tested in client" seals, done objectives, checked install steps, released changelog entries.
- **Seal Amber** (`seal-amber`, text `seal-amber-text`): "in review" seals, release-candidate entries; `seal-amber-text` also tints `em` and quoted terms on leather.
- **Waypoint Teal** (`waypoint`): focus outlines, code chips and hint icons on the binding. It is FLC's own in-game accent, used as the site's interaction signal, never as decoration.

### Neutral
- **Leather** (`leather-950` to `leather-600`): 950 for masthead, footer, plate mats, menus and the lightbox; 900 is the page ground under the leather texture; 850 for callouts and report kinds; 800/700 for hover fills, tabs and the folio gradient; 600 for keyboard keys and hint borders.
- **Binding Ink** (`text`, `text-2`, `text-3`): cream text on leather; `text-2` for body paragraphs and captions on the binding; `text-3` for the faintest marks (pending seal ring, step anchors, language icon).
- **Vellum** (`vellum`, `vellum-2`, `vellum-3`): parchment leaves; `vellum-3` is the photo-corner colour on plates.
- **Iron-gall Ink** (`ink`, `ink-2`): headings and body on parchment; leaf inner rules use `rgba(42,32,22,.28)`.

### Named Rules
**The One Red Action Rule.** Each view's content carries at most one rubric-red button, the action the page exists for (Accept: Download on home, the release download on Download). Everything else is ghost, quiet or an arrow link. On phones the masthead Download is the only standing red outside the content, because the download must stay one tap away.

**The Seals Are Proof Rule.** Green and amber appear only where a real test status is being stated (seals, done objectives, checked steps, release entries). Never use them for decoration, success-toned marketing, or emphasis.

**The Gold Is Structure Rule.** Gold leaf draws rules, frames and underlines; it is never a fill for buttons or panels (the only gold fill is the small count pill).

## Typography

**Display Font:** IM Fell English SC (with Iowan Old Style, Palatino Linotype, Georgia)
**Body Font:** Alegreya Sans (with Segoe UI, system-ui)
**Label/Mono Font:** ui-monospace, Cascadia Mono, Consolas (commands, objective counts, file names in buttons)

**Character:** A seventeenth-century small-caps book face for every title, paired with a humanist sans that stays legible at long reading lengths and in Spanish. Both are self-hosted (latin and latin-ext for Alegreya Sans).

### Hierarchy
- **Display** (400, `clamp(2.3rem, 1.4rem + 3.2vw, 4rem)`, 1.04): inner-page titles, max 20ch.
- **Quest Title** (400, `clamp(2.1rem, 1.3rem + 2vw, 3.2rem)`, 1.02, rubric ink): the home quest page title; release, board and party titles use the same rubric treatment at headline size.
- **Headline** (400, `clamp(1.75rem, 1.2rem + 1.8vw, 2.6rem)`, 1.02): chapter and section titles (h2), balanced, max ~16ch in chapters.
- **Rubric Label** (IM Fell, 400, 1.05 to 1.6rem): small display-face terms inside a structure: objectives heading, rules list terms, install move titles, table heads, footer heads, board platform names, mode names.
- **Title** (Alegreya Sans 700, 1.22rem, 1.12): h3, quest rows, FAQ questions (1.18rem).
- **Body** (400, 1.125rem / 1.62; 1.0625rem under 420px): paragraphs at 56 to 66ch.
- **Caption** (italic 400, 0.95rem): provenance lines under plates and scenes ("In-game capture · FLC 0.8.1.1"), always with the eye icon.
- **Mono** (0.86em in prose, 700 1rem for counts): commands, counts, build ids.

### Named Rules
**The No Kicker Rule.** Nothing sits above a heading: no eyebrow, label, tag line or icon row. A title opens its block; status seals and counts follow the text they qualify.

**The Drop Cap Rule.** A chapter's lead paragraph opens with a two-line initial in the display face (`initial-letter: 2`, float fallback), rubric red. Only the lead paragraph of a chapter.

## Layout

A centred column of 1240px (`wrap`, masthead 1360px, prose 860px) with fluid gutters `clamp(16px, 4vw, 48px)`. Chapters stack vertically; inside them two-column grids use book proportions (5fr/7fr text/plates, flipped 7/5; 5/6 for features and quest logs; 4/8 for rules; 3/9 for install moves). All grids collapse to one column at 860px. Folio padding `clamp(28px, 4vw, 56px)`; major sections `clamp(48px, 7vw, 96px)` vertically.

The home hero is a full-bleed scene with the quest page (40rem column) overlapping its lower part (negative top margin of 35.8vw); at 1600px and up the scene becomes an inset frontispiece plate (gutters on both sides, gilt hairline, lift shadow) and a one-line vellum ink note points at the guide window in the scene instead of a second plate. Under 680px phones get their own composition: a different, real mobile capture, the guide plate riding on its lower edge at full width, then the quest page with the action reordered first. The route line and waypoints disappear on phones.

Breakpoints: 1600 (hero frontispiece and note), 1080 (footer, camp), 960 (masthead becomes menu button plus red Download), 860 (single column), 680 (phone compositions), 420 (brand name hidden, body 1.0625rem). Every interactive target is at least 44px.

## Elevation & Depth

Depth is paper on leather. Leaves, plates, folios and menus lift off the binding with one shared shadow, `--lift`; nothing else floats. Leaves add an inner gold hairline and inner brown burn so the edges look aged, and a ruled inner border 9px in. Folios are tooled: a 1px gold rule plus a 5px dark inset and a 6px soft gold inset.

### Shadow Vocabulary
- **Lift** (`box-shadow: 0 22px 44px -22px rgba(0,0,0,.85), 0 3px 8px rgba(0,0,0,.35)`): leaves, plates, folios, nav panel, campfire images.
- **Leaf burn** (`inset 0 0 0 1px rgba(122,98,50,.55), inset 0 0 48px rgba(122,88,40,.28)`): parchment edge, combined with Lift.
- **Tooling** (`inset 0 0 0 5px rgba(9,7,6,.55), inset 0 0 0 6px rgba(201,162,77,.17)`): folio panels.
- **Rubric press** (`inset 0 1px 0 rgba(255,220,190,.25), inset 0 0 0 1px rgba(0,0,0,.25), 0 10px 18px -12px rgba(0,0,0,.9)`): the primary button only.

### Named Rules
**The One Lift Rule.** There is a single elevation. Do not invent hover lifts, glows or stacked card shadows.

## Shapes

Bookbound and square: leaves at 1px, buttons, tabs, inputs and chips at 2px. Circles exist only for wax seals, numbered-step medallions and the gold count pill. The recurring geometry is the diamond (a square turned 45 degrees): objective markers, route waypoints, changelog nodes, party mode markers and the install checkboxes are all diamonds. Plates carry vellum triangular photo corners at top-left and bottom-right. The "coming soon" stamp on the support board is a rubric outline tilted -3 degrees.

## Components

### Buttons
- **Shape:** squared edge (2px), min height 48px (56px for the big download).
- **Primary (rubric):** red gradient face from `#9f3219` through `rubric` to `rubric-deep`, cream text, `#b5492c` border, Rubric press shadow; may carry a mono `small` with version or file name. Hover warms the gradient and turns the border `gilt-hi`.
- **Ghost:** translucent leather fill with a `gilt-lo` border; on a leaf it becomes translucent vellum with an ink border. Hover deepens the fill.
- **Quiet:** borderless text button, `text-2` (rubric ink on leaves).
- **Pending:** dashed border, `text-2`, used when the download is not yet published.
- **Arrow link:** bold text with an arrow icon that slides 3px on hover; the default secondary action.
- **Focus:** a 2px waypoint-teal outline at 3px offset, everywhere.

### Proof Seals
- **Style:** a 30px wax seal image (green "tested", amber "in review") with a bold status label in the matching seal text colour; on leaves the label darkens to `#1f5a3c` / `#6b440a`. Planned features get an empty dashed ring.
- **Use:** in proof lists directly after the claim they back; never as decoration.

### Cards / Containers
- **Leaf:** parchment with grain, lit top-left and burned bottom-right, Lift plus Leaf burn, ruled inner border; ink text, rubric-ink links. Used for the quest page, the party chapter, the release, the support board and honesty notes.
- **Folio:** tooled leather chapter panel with a folio number; variants: spread (rules top and bottom only, a gold gutter rule between its two pages), inset (max 1040px, right-aligned), loose (no panel at all).
- **Callout / Kind:** leather-850 fill with a gold rule border.

### Plates (signature)
A capture sits on a 5px leather-950 mat inside a `gilt-lo` frame with Lift and vellum photo corners. UI captures size to their native width (`fit-content`, never wider than the source). Under every plate: the eye icon, an italic provenance line and the caption at 62ch. Plates open in a lightbox on click.

### Objectives (signature)
FLC's own step format: a list of rows, each with a rubric-ink diamond, the objective text and a right-aligned mono count (0/1, 0/2). Done rows fill the diamond seal green, colour the count green and strike the text; the diamond is stamped once with the ink check animation.

### Install checklist
Each install step is a row with a 24px diamond checkbox in a 44px target, gold-bordered, turning seal green with a drawn tick when checked; the active step gets a soft gold halo, steps are anchor-linkable and progress is counted in mono green. Steps are grouped into moves with gilt display titles.

### Compare slider
Two same-size captures stacked in one plate; the top one is clipped from the left by a native range input (rubric accent) and a 2px gilt-hi handle marks the seam. The two endpoint names flank the range.

### Campfire board
The support board is a leaf listing donation platforms: display-face name, ink description, and either the platform's link or a tilted rubric "coming soon" stamp. A real brazier capture in a gold frame sits beside the support heading under a faint red glow.

### Navigation
Sticky leather-950 masthead with a soft gold bottom rule: emblem, "FLC" in display caps, nav links in Alegreya Sans 500 that gain a gold underline drawn from the centre on hover or current page, dropdown panels on leather-950 with gold rule. At 960px and below the links collapse into a menu button (gold bars) opening a full-height leather sheet with display-face group labels, and a red Download button stays in the masthead. Language switch: current language in gilt-hi with a gold bottom bar.

## Do's and Don'ts

### Do:
- **Do** keep one rubric-red action per view's content; use ghost buttons and arrow links for everything else.
- **Do** show FLC's real windows as plates at their native size with the provenance line under each one.
- **Do** put status in a wax seal next to the claim it proves, in seal green or amber only.
- **Do** use the diamond for every marker, checkbox and waypoint, and the objective format for any list of things the reader will do.
- **Do** set titles in IM Fell English SC at weight 400 and reading text in Alegreya Sans at 1.125rem / 1.62.
- **Do** give phones their own composition (own capture, action first) rather than a shrunk desktop.

### Don't:
- **Don't** stretch a capture past its native size or redraw FLC's UI.
- **Don't** put labels, kickers or eyebrows above headings.
- **Don't** use seal green or amber for anything but proof.
- **Don't** add a second elevation, hover lifts, glows or rounded cards; leaves stay at 1px, controls at 2px.
- **Don't** animate on entry; the ink check and the count are the only motion.
- **Don't** use gold as a fill for buttons or panels.
