---
target: the existing FLC website (home)
total_score: 26
max_score: 36
na_heuristics: 7
p0_count: 0
p1_count: 3
target_identity: "file:E:\\Firebrand\\FLC-WebSite\\templates\\home.html"
target_fingerprint: "sha256:92649fb9fd4a156d4d61c8cb2d0b6ce6c69e2c27269588d4a642ab85e190a6d4"
target_path: "E:\\Firebrand\\FLC-WebSite\\templates\\home.html"
timestamp: 2026-11-04T17-44-38Z
slug: templates-home-html
---
Method: dual-agent (A: design review sub-agent · B: detector sub-agent). Overlay skipped: owner restriction on Live mode.

## Design Health Score (Nielsen)
| # | Heuristic | Score | Key Issue |
|---|---|---|---|
| 1 | Visibility of System Status | 3 | Copy buttons: no aria-live, no failure feedback |
| 2 | Match System / Real World | 3 | SHA-256/PowerShell, Lua, LibDataBroker, build IDs in high-traffic spots |
| 3 | User Control and Freedom | 3 | Clear exits; language choice overrides redirect |
| 4 | Consistency and Standards | 3 | Label drift: Reports / Report an issue / Report a problem; "Explore features" goes to #journey |
| 5 | Error Prevention | 3 | Good folder trees; on mobile the correct tree clips the folder name |
| 6 | Recognition Rather Than Recall | 3 | On mobile Download hides in the menu while Support has the header pill |
| 7 | Flexibility and Efficiency | n/a | Persuade/docs site |
| 8 | Aesthetic and Minimalist Design | 2 | ~7 elements per home stop; /features/ ~30 identical rows; checksum weighs as much as Download |
| 9 | Error Recovery | 3 | Troubleshooting by symptom, known issues, report path |
| 10 | Help and Documentation | 3 | No help finding the WoW folder; no "it worked" capture |
| Total | | 26/36 | Good, low edge |

## Design Specificity Verdict
Half authored: content (real captures with provenance, proof badges, builds table, folder trees) is FLC's own; the look (night navy + bronze + Cinzel + compass + contour lines) and the home skeleton (split hero, six identical zig-zag rows, three value columns, twin cards) are a dark-fantasy SaaS template. Missing from the brief: quest journals/parchment as structure, old maps, RPG frame chrome, Party Mode in the hero, a tavern/camp donation scene.
Deterministic scan: source 349 findings (mostly CSS repeated per page; design-system-color/font advisories reflect an incomplete DESIGN.md), rendered desktop 67, mobile 19. Real: line-length on intros/notes (101-125 ch), stragglers everywhere (no text-wrap: pretty on p/li), low contrast on the button's version label (~4.0:1), the "in review" em on parchment (4.0:1), skip-link hover (1.2:1). Judgment calls: gold glow under the primary button, gradient text on the hero accent line, kicker above every heading (Impeccable bans it), amber side stripe on the status ribbon. False positives: pulsing dot (animation none on the live ribbon), coin labels, kbd border, short-heading tracking, skin swatch colour, legal footer measure, lightbox img, cramped padding.

## Priority Issues
- [P1] Mobile first viewport has no Download and no distinctive pitch (Support pill in header, CTA below the fold). Fix: Download in the mobile header or a slim sticky bar; free line + CTA before the capture; a "install from your PC" handoff. Command: adapt.
- [P1] Home is a templated skeleton; generic hero; Party Mode buried (stop 2 of 6). Fix: a hero built on one product moment; varied modules; Party Mode up front. Command: shape then bolder/layout/typeset.
- [P1] /download/ not extremely simple: checksum co-equal with the button; 8 flat steps; no success capture; mobile wraps (button text, build IDs, tree clipped); ends on Known issues. Fix: one column, three moves with real captures and a success state, checksum collapsed as optional, "where is my WoW folder" hint. Command: distill then harden, clarify.
- [P2] Mobile route line strikes through every capture caption under 860 px. Command: polish.
- [P2] /features/ and /support/ fall back to identical modules (30 rows, no captures; two identical coin cards with the same notice twice). Command: layout then delight.

## Persona Red Flags
- Casey (phone, from Reddit/Discord): Support not Download in header; CTA below the fold; PowerShell first on /download/; no PC handoff.
- Friends leveling together: Party Mode absent from hero and top nav; "everyone needs FLC and agrees to share" only on /features/; nothing to send to the group.
- Jordan (first-timer): jargon at decision points; no help locating the install; no success confirmation.
- Sam (accessibility): copy buttons without aria-live; small uppercase badges; faint provenance text.

## Minor Observations
"Explore features" points to #journey; 1180 px column leaves ~370 px of wallpaper per side at 1920; two gold CTAs on home (Download and Support share rank); free line in proof green; build number styled as a metric; long ES nav label; two meta lines under every capture; 0.8.2 box mid-home; shots.mjs mobile390 full-page captures repeat past ~5460 CSS px at DPR 3.

## Questions to Consider
1. What if the hero were the Party Mode moment rather than a tagline any fantasy app could carry?
2. Does a player need a checksum before step 1, or a screenshot of the AddOns list with both entries checked?
3. Why is the page called "Quest log" the only one with no captures?
