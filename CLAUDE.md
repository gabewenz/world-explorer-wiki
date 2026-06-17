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

Each file starts with a table of things, for a concise reference. If more detail is
warranted, a separate sub-section can be added to the document.

```markdown

# Summary

| Name | Type | Area | Rating (1-10) | Notes | Links |
|---|---|---|---|---|---|
| Example Place    | Museum     | Downtown | TODO | Strong modern art collection | [Map](https://example.com) |
| Some Restaaurant | Restaurant | Uptown   |  6 | | Great appetizers; expensive  | |

# Detailed Notes

## Some Restaurant

Some information about dishes tried

```

### Links

Include only links that are genuinely useful. Typical options are:

- `Map`
- `Website`
- `Tickets`
- `Note`

Example:

```markdown
[Map](https://example.com) · [Website](https://example.com) · [Note](../notes/los-angeles/example-place.md)
```

Prefer a map link when adding only one link.
