---
name: Forever Leveling Companion
description: The official website of FLC, a free leveling companion addon for World of Warcraft Forever.
colors:
  night-abyss: "#060a12"
  night-paper: "#0b1220"
  night-panel: "#121c31"
  night-raised: "#1b2742"
  night-rule: "#273556"
  vellum-ink: "#ece4d0"
  vellum-ink-muted: "#c9c1ae"
  vellum-ink-faint: "#aaa38e"
  aged-bronze: "#a9814a"
  burnished-gold: "#d4b16f"
  tarnished-bronze: "#6b5232"
  parchment: "#ddd0b0"
  parchment-ink: "#2b2317"
  verdant-proof: "#3fbf8a"
  lantern-amber: "#e4ad4f"
  waypoint-teal: "#4fc3c0"
typography:
  display:
    fontFamily: "Cinzel, Trajan Pro, Georgia, serif"
    fontSize: "clamp(2.1rem, 1rem + 3.6vw, 3.9rem)"
    fontWeight: 500
    lineHeight: 1.05
  headline:
    fontFamily: "Cinzel, Trajan Pro, Georgia, serif"
    fontSize: "clamp(1.55rem, 1.1rem + 1.6vw, 2.25rem)"
    fontWeight: 500
    lineHeight: 1.15
  title:
    fontFamily: "Alegreya Sans, Segoe UI, system-ui, sans-serif"
    fontSize: "1.25rem"
    fontWeight: 700
    lineHeight: 1.15
  body:
    fontFamily: "Alegreya Sans, Segoe UI, system-ui, sans-serif"
    fontSize: "1.125rem"
    fontWeight: 400
    lineHeight: 1.62
  label:
    fontFamily: "Cinzel, Trajan Pro, Georgia, serif"
    fontSize: "0.88rem"
    fontWeight: 500
    letterSpacing: "0.14em"
rounded:
  hairline: "2px"
  sm: "3px"
  pill: "999px"
spacing:
  gutter: "clamp(16px, 4vw, 40px)"
  wrap: "1180px"
components:
  button-primary:
    backgroundColor: "{colors.burnished-gold}"
    textColor: "#1c1408"
    rounded: "{rounded.sm}"
    padding: "0.7em 1.25em"
    height: "48px"
  button-ghost:
    backgroundColor: "{colors.night-panel}"
    textColor: "{colors.vellum-ink}"
    rounded: "{rounded.sm}"
    padding: "0.7em 1.25em"
  badge-tested:
    textColor: "#8fe3bd"
    rounded: "{rounded.hairline}"
  badge-review:
    textColor: "#f2c779"
    rounded: "{rounded.hairline}"
  parchment-note:
    backgroundColor: "{colors.parchment}"
    textColor: "{colors.parchment-ink}"
    rounded: "{rounded.hairline}"
---

# Design System: Forever Leveling Companion

<!-- Incumbent system, documented 2026-11-04 before the Impeccable redesign (branch redesign/impeccable).
     The redesign replaces this file; this version stays in git history (commit on main). -->

## Overview

**Creative North Star: "The Cartographer's Night Journal"**

A journal opened under lantern light: night-blue paper, aged-bronze rules, parchment notes pinned at the margins and
faint contour lines running under every page. Real in-game captures are the illustrations, framed like inventory
slots with bronze corner brackets. Gold is rare and reserved for the main call to action and the active state.

The density is editorial and calm: generous vertical rhythm, one idea per band, long readable measures in a humanist
sans. Ornament is sober and crafted (a compass rose turning slowly behind the hero, a dashed route line that draws
itself down the benefits), never decorative noise. Honesty is part of the look: green "tested in client" and amber
"in review" badges sit next to every claim.

**Key Characteristics:**
- Dark night-blue canvas with tonal layers instead of cards on cards.
- Cinzel capitals for headings, Alegreya Sans for reading.
- Captures framed as inventory slots; parchment for the honesty notes.
- Bronze hairlines and nearly square corners (2-3 px).
- Proof badges (green tested, amber in review) beside each feature.

## Colors

A nocturnal palette: deep navy layers, warm parchment inks, bronze for structure and gold for the one action that
matters, with two signal colours for proof.

### Primary
- **Burnished Gold** (#d4b16f): the primary button's gradient top, active navigation underline, links and kickers.
- **Aged Bronze** (#a9814a): hairline rules, frame corners, icons, borders of ghost buttons.

### Secondary
- **Verdant Proof** (#3fbf8a): "tested in the game client" badges, the "free" line, the "available now" ribbon.
- **Lantern Amber** (#e4ad4f): "in review" badges and the "(?)" mark.

### Tertiary
- **Waypoint Teal** (#4fc3c0): focus rings, inline code, approach-hint markers (echoes the addon's own accent).

### Neutral
- **Night Paper** (#0b1220): page background. **Night Abyss** (#060a12): footer, menu panel, code wells.
- **Night Panel** (#121c31) and **Night Raised** (#1b2742): layered surfaces; **Night Rule** (#273556): table rules.
- **Vellum Ink** (#ece4d0) for text, **Vellum Ink Muted** (#c9c1ae) for secondary text, **Vellum Ink Faint**
  (#aaa38e) only for tertiary labels.
- **Parchment** (#ddd0b0) with **Parchment Ink** (#2b2317): honesty notes and pin captions.

### Named Rules
**The Lantern Rule.** Gold marks the single most important action in view; everything else is bronze or ink.
**The Proof Colour Rule.** Green and amber mean "tested" and "in review" only, never decoration.

## Typography

**Display Font:** Cinzel (with Trajan Pro, Georgia)
**Body Font:** Alegreya Sans (with Segoe UI, system-ui)
**Label/Mono Font:** system monospace for commands and checksums

**Character:** inscriptional Roman capitals over a warm humanist sans: a carved title on a readable page.

### Hierarchy
- **Display** (500, clamp(2.1rem, 1rem + 3.6vw, 3.9rem), 1.05): the hero's three lines.
- **Headline** (500, clamp(1.55rem, 1.1rem + 1.6vw, 2.25rem), 1.15): section titles; page titles use clamp(2.1rem, 1.3rem + 3vw, 3.6rem) and 1.85rem under 420 px.
- **Title** (700, 1.25rem): step and item titles in the body face.
- **Body** (400, 1.125rem, 1.62): reading text, ~62-70ch measures; 1.0625rem under 560 px.
- **Label** (500, 0.88rem, 0.14em, uppercase): kickers in Cinzel; badges in Alegreya Sans 700 0.8rem uppercase.

### Named Rules
**The No-Split Rule.** Headings never hyphenate or break words; they balance their lines instead.

## Layout

A centred column of 1180 px with a fluid gutter (16-40 px). Bands alternate text and capture in a 5:6 grid; the home
page's benefits run down a dashed route with numbered diamond markers. Breakpoints: 1080 (hero stacks), 960 (menu
becomes a full-screen panel), 860 (grids collapse to one column), 680 (phone hero composition), 560, 420.

## Elevation & Depth

Flat tonal layering by default. Shadows appear only under objects that sit "on" the page: framed captures, pinned
notes and parchment.

### Shadow Vocabulary
- **Pinned object** (`box-shadow: 0 18px 40px -18px rgba(0,0,0,.75), 0 2px 6px rgba(0,0,0,.35)`): frames, parchment.
- **Gold lift** (`box-shadow: inset 0 1px 0 rgba(255,255,255,.35), 0 6px 18px -8px rgba(212,177,111,.6)`): primary button.

## Shapes

Nearly square: 2-3 px corners on buttons, badges and frames; full circles only for the status dot, coins and step
numbers; pill only for the Support link. Bronze corner brackets (14 px L-shapes) mark framed captures. Diamonds
(rotated squares) are the recurring marker: route stops, list bullets, quest-log entries.

## Components

### Buttons
- **Shape:** nearly square (3 px), minimum height 48 px.
- **Primary:** gold gradient (#e2c27f → #b68d4f → #9d7640) with dark ink text.
- **Ghost:** translucent night panel with an aged-bronze border; hover raises to Night Raised.
- **Pending:** dashed border, muted text, for "coming soon" states.

### Chips (badges)
- **Style:** uppercase 0.8rem labels on a tinted ground: green for tested, amber with a "?" coin for in review.

### Cards / Containers
- **Corner Style:** 2 px. **Background:** Night Panel at 70-80 %. **Border:** bronze hairline. Used sparingly: install
  steps, donation tokens, report kinds.

### Navigation
- Sticky dark masthead; top level Download, Reports, FAQ and an "The addon" dropdown with one-line descriptions;
  Support as a pill. Under 960 px a full-screen panel with the addon's pages listed open.

### Framed capture (signature)
- Inventory-slot frame: 6 px dark inset, bronze hairline, two corner brackets, provenance line ("In-game capture ·
  FLC x.y") and a caption below. UI captures are never stretched beyond their native size.

## Do's and Don'ts

### Do:
- **Do** show a real capture next to every feature claim, with its provenance.
- **Do** keep gold for one action per view (The Lantern Rule).
- **Do** keep corners at 2-3 px and rules as bronze hairlines.

### Don't:
- **Don't** use green or amber for anything but proof states.
- **Don't** stretch, rotate or upscale addon captures.
- **Don't** hyphenate or split words in headings.
