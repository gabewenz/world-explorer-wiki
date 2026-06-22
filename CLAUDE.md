# World Explorer Wiki

This project area is a "wiki"-like collection of files for maintaining a concise, readable
collection of places of interest (restaurants, museums, parks, etc) in a city or area. It
defines the file structure, table format, status conventions, and rules for both manual
and AI-assisted updates.

## Purpose

Use this project to track places such as:

- Restaurants, cafés, and bars
- Museums, galleries, and cultural institutions
- Music, theater, and event venues
- Parks, gardens, and outdoor spaces
- Tourist sites, landmarks, and neighborhoods
- Shops, markets, and other notable destinations

The system should remain:

- Easy to scan
- Easy to update
- Brief by default
- Flexible enough to hold detailed notes when needed
- Usable as plain Markdown without specialized software

## File Organization

For now, use a flat file organization, one file per city or region of interest. All files
are markdown. Keep an index of all files, so it's easy to navigate from a browser or
markdown editor.

```text
└── project-directory/
    ├── CLAUDE.md (this file)
    ├── index.md
    ├── american-southwest.md
    ├── greece.md
    ├── los-angeles-ca.md
    ├── mexico-city.md
    └── san-francisco-ca.md
```

### File Contents

Each file has exactly two top-level (`#`) sections, in this order: `# Tables` and
`# Detailed Notes`.

`# Tables` holds one or more summary tables, each under its own `##` heading — the heading
text is a free-form category name (e.g. `## Restaurants`, `## Attractions`, `## Fun`).
There's no fixed list of categories: a small file might have just one table (`##
Summary`), a large file can have as many category tables as it needs. This structure (one
H1 wrapping all `##` category tables) lets a script discover the categories in a file just
by reading its headings, with no hardcoded enum to keep in sync — see
`scripts/list_categories.py`.

`# Detailed Notes` holds notes and links, with one `##` sub-section per place. Each table's
`Link` column points to the matching sub-section by anchor. Keep summary tables short — put
notes and links in `Detailed Notes`, not in the table.

Within each table, sort rows alphabetically by the `Area` column (ties broken by `Name`).
This keeps things scannable by neighborhood and gives inserts a deterministic place to go.

Pad each column with spaces so the raw Markdown stays aligned and easy to scan in a plain
text editor, not just when rendered.

```markdown

# Tables

## Summary

| Name             | Type       | Area     | Cost | 🧐 Rating | Link                      |
|------------------|------------|----------|------|-----------|---------------------------|
| Other Restaurant | Restaurant | Downtown | $$$$ | 🟢 8      | [link](#other-restaurant) |
| Example Place    | Museum     | Midtown  | $$   | ? ⚪      | [link](#example-place)    |
| Some  Restaurant | Restaurant | Uptown   | $    | 🟡 6      | [link](#some-restaurant)  |

# Detailed Notes

## Other Restaurant

Great appetizers; expensive. Some information about dishes tried.

[Map](https://example.com)

## Example Place

Strong modern art collection.

[Map](https://example.com)

## Some Restaurant

Great appetizers; expensive. Some information about dishes tried.

[Map](https://example.com)

```

The `Name` column holds plain text (no link) — the section anchor lives only in the `Link`
column, so the table stays scannable. The anchor is the place's GitHub-style heading slug:
lowercase, spaces become hyphens, ASCII punctuation is stripped — but letters with accents
or other diacritics (é, ñ, ó, …) are kept as-is, not dropped. Double-check generated anchors
against this rule; silently dropping an accented letter produces a link that won't actually
jump to the heading.

Every place added to a summary table must have a corresponding `## Heading` in `Detailed
Notes` (even if just a `[Map](...)` link with no notes yet), and vice versa — don't leave
orphaned detail sections for places no longer in any table (e.g. after removing a closed
business, delete its notes too).

### Cost

For food and drink tables, a `Cost` column is used with `Free` / `$` / `$$` / `$$$` /
`$$$$` to indicate relative price.

### Rating

The `Rating` column header is `🧐 Rating` , and every row in the column is prefixed with
exactly one emoji marker — no row is left as a bare number — keeping the column a
consistent visual width when scanning the raw Markdown in a plain text editor.

For places already visited, the marker + number records the actual rating:

| Marker | Meaning   |
|--------|-----------|
| `🟠`    | 1-5       |
| `🟡`    | 6-7       |
| `🟢`    | 8         |
| `⭐`    | 9-10      |

For a place not yet visited, prefix the entry with `?` . After the `?`, add an emoji (and
optionally a number) recording interest level rather than an actual rating, using the same
bucket meanings above — e.g. `? 🟡` (some interest) or `? ⭐ 9` (highly interested, with a
precise score). The number is optional in every bucket. `⚪` is reserved for this
`?`-prefixed, not-yet-visited case and means neutral — no particular interest either way,
e.g. `? ⚪`.

### Type

When a file has just one combined `## Summary` table, use a `Category - Subtype` format
when a finer distinction is useful, e.g. `Cafe - Coffee`, `Restaurant - Taco`,
`Museum - Art`. Fall back to just the category if no finer distinction is needed.

When a file is split into one table per category (see above), the category is already
implied by the table/heading, so the `Type` column should hold just the subtype or cuisine
on its own — e.g. `Coffee`, `Chinese, Dumplings` — without repeating the category prefix.

### Links

Include only links that are genuinely useful, placed in the relevant `Detailed Notes`
sub-section (not the summary table). Typical options are:

- `Map`
- `Website`
- `Tickets`
- `Note`

Example:

```markdown
[Map](https://example.com) · [Website](https://example.com) · [Note](../notes/los-angeles/example-place.md)
```

Prefer a map link when adding only one link.

## Adding a Place

When the user asks to add a place but doesn't give the `Area` (or other missing details,
e.g. correct business name, `Type`/cuisine), look it up yourself (web search, maps) rather
than asking the user. Use the result that best matches the user's intent (e.g. fix an
obvious misspelling of the business name) and briefly mention any correction made. Only ask
the user when the lookup is ambiguous (e.g. multiple distinct businesses/locations with the
same name) or turns up nothing.

## Scripts

`scripts/` holds small Python helpers for working with these files programmatically:

- `scripts/wiki_lib.py` — shared parsing/rendering library (not run directly): reads a
  file's `# Tables` / `# Detailed Notes` structure, parses/renders padded tables, and
  computes GitHub-style heading slugs.
- `scripts/list_categories.py FILE...` — lists each file's category tables (the `##`
  headings under `# Tables`) and their row counts.
- `scripts/list_anchors.py FILE...` — lists every anchor (slugged `##` heading) under
  `# Detailed Notes` in each file, and flags any duplicate slugs within a file — check this
  before adding a place whose name might collide with an existing anchor.
- `scripts/normalize_tables.py FILE...` — re-sorts every table's rows alphabetically by `Area` and
  re-pads columns to stay aligned. Prints a diff by default; pass `--write` to apply.
