# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

- **Primary: a player looking for a leveling addon for World of Warcraft: Forever.** Arrives from a search, Reddit or
  Discord, often on a phone, and decides in seconds whether FLC is worth downloading. Needs to understand what it does,
  see that it is real (in-game captures), and get the official zip installed without technical knowledge.
- **Primary: a group of friends who will level together.** Looks for something that keeps the group coordinated:
  Party Mode (help a friend without losing your own guide, level together, catch up).
- Secondary: a player who already uses FLC and comes back to update, read what changed, solve a problem, report a bug
  or donate.
- Languages: English first (international players), Spanish second (the owner is Argentine; a large Spanish-speaking
  audience). Every page exists in both.

## Product Purpose

Forever Leveling Companion (FLC) is a free leveling companion addon for World of Warcraft: Forever: step-by-step quest
guides with an arrow, quests accepted and turned in by themselves, Party Mode, dungeon and raid guides with boss cards,
a Loot Atlas with upgrade ratings and a wishlist, an adaptive look that matches the player's UI, and a minimap button.
The website exists so that a player can discover FLC, understand how it works, see authentic captures, download the
published version, install it, get help, follow updates, report problems and, voluntarily, support development.
Success: a visitor installs FLC correctly on the first try, and groups of friends recognise Party Mode as the reason to
pick it.

## Positioning

Confirmed by the owner (2026-11-04), all four together:
- **Level with friends:** Party Mode (help a player and return to your own guide where you left it, Level Together,
  Group Catch-Up).
- **All in one:** guide, arrow, dungeons and raids, boss cards, Loot Atlas and adaptive look in one addon.
- **Free, for real:** no premium version, nothing locked, no ads, no money requests inside the game.
- **Made for WoW: Forever:** routes and data built for Forever, with honest "in review" / "(?)" labels where data is not
  confirmed on the official realms yet.

## Operating Context

- Distribution: GitHub Releases of `firebrand-dev/ForeverLevelingCompanion` (public, release files only). Current:
  **0.8.1.1**, published 2026-11-04, `FLC-0.8.1.1.zip`, 1,004,876 bytes, SHA-256
  `756879fd789f9d6506d4e0a8b6bc30db83d5a1b3a3e0684a7228973d4cb63761`. Tested on client 1.60.1.70755 on the team's own
  development server, not on the official realms. Source of truth:
  `E:\Firebrand\FoLeCom-0811\docs\release\WEB_HANDOFF_LAUNCH.md`.
- Install: two folders (`ForeverLevelingCompanion`, `FLC_Guides_Catalog`) into
  `World of Warcraft\_forever_\Interface\AddOns`; welcome setup on first start.
- Reports: GitHub Issues at `firebrand-dev/FLC-reportes`, prepared in game with `/flc bug` and `/flc review`.
- Website: static, built with Python + Jinja2 (`tools/build.py`), EN/ES, to be hosted on GitHub Pages at
  `https://flc.quest` (domain owned; not published yet). A stopgap one-page site from the addon repository is live at
  `firebrand-dev.github.io/ForeverLevelingCompanion` and is not this project.
- Donations: Ko-fi (international, via PayPal) and Cafecito (Argentina, pesos). Accounts not configured yet: both stay
  "coming soon" with no link.

## Capabilities and Constraints

- Static site, no JavaScript framework, no database, no credentials in the frontend; content centralised in
  `content/*.json` and `i18n/*.json`; captures in `media/manifest.json`.
- Must keep working under a subfolder (GitHub Pages project URL) as well as at the domain root.
- Never alter: the downloadable version, zip, checksum, licenses, verified release notes, correct install
  instructions, the reports system.
- No invented data: no download counts, testimonials, ratings, fundraising numbers or "best addon" claims.
- No Blizzard assets beyond in-game captures of FLC running; no copying other addons' or Blizzard's sites.
- Donations unlock nothing and are asked for only on the website, never in the game.

## Brand Commitments

- Name: Forever Leveling Companion, short **FLC**. The owner gave full freedom on logo, typography and palette.
- Voice: plain, honest, player-to-player; English and natural rioplatense Spanish.
- Fan project, not affiliated with Blizzard Entertainment; the disclaimer stays.

## Evidence on Hand

- Real in-game captures from the addon's automated client runs (`E:\Firebrand\FoLeCom\build\gametest\`), cropped into
  `media/src/` with provenance in `media/manifest.json` (FLC 0.4.0 to 0.8.1.1-rc1, clients 70532 to 70755).
- Test evidence: launch battery on 1.60.1.70755 (10/10 suites, 0 Lua errors from FLC); feature status per
  `content/features.json`.
- Absent and not to be fabricated: download numbers, user reviews, press, official-realm verification, donation totals.

## Product Principles

1. Show, don't claim: every feature is backed by a real capture and its real test status.
2. Install must be foolproof: the download and the folder structure are the most important page after the home.
3. Honest by default: "in review" is a feature, not an embarrassment.
4. Built for players: the site should feel like part of the game's world, not a software company.
5. Free means free: support is voluntary, discreet and never a gate.

## Accessibility & Inclusion

WCAG 2.1 AA contrast; keyboard navigation; reduced-motion respected; readable from 320 px phones to 1920 px screens.
