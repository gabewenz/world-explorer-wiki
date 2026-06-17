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

Each file starts with a table of things, for a concise reference. Keep the summary table
short — notes and links live in a `Detailed Notes` section below, with one sub-section per
place, and the table's `Link` column points to that sub-section by anchor.

Pad each column with spaces so the raw Markdown stays aligned and easy to scan in a plain
text editor, not just when rendered.

```markdown

# Summary

| Name          | Type       | Area     | Rating (1-10) | Link                      |
|---------------|------------|----------|----------------|---------------------------|
| Example Place | Museum     | Downtown | TODO           | [link](#example-place)    |
| Some Restaurant | Restaurant | Uptown | 6              | [link](#some-restaurant)  |

# Detailed Notes

## Example Place

Strong modern art collection.

[Map](https://example.com)

## Some Restaurant

Great appetizers; expensive. Some information about dishes tried.

[Map](https://example.com)

```

The `Name` column holds plain text (no link) — the section anchor lives only in the `Link`
column, so the table stays scannable. The anchor is the place's GitHub-style heading slug
(lowercase, spaces to hyphens, punctuation stripped).

### Type

Use a `Category - Subtype` format when a finer distinction is useful, e.g. `Cafe - Coffee`,
`Restaurant - Taco`, `Museum - Art`. Fall back to just the category if no finer distinction
is needed.

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
