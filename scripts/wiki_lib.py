"""Shared parsing/rendering helpers for World Explorer Wiki markdown files.

Expected file structure (see CLAUDE.md):

    # Tables

    ## <Category>

    | Name | ... | Link |
    |------|-----|------|
    | ...  | ... | ...  |

    # Detailed Notes

    ## <Place>

    <body text>

Not run directly; imported by the other scripts in this directory.
"""

import re
from dataclasses import dataclass, field

H1_RE = re.compile(r"^# (.+)$", re.M)
H2_RE = re.compile(r"^## (.+)$", re.M)


@dataclass
class Table:
    category: str
    header: list
    rows: list


@dataclass
class Note:
    heading: str
    body: str


@dataclass
class WikiFile:
    tables: list = field(default_factory=list)
    notes: list = field(default_factory=list)
    preamble: str = ""


def _split_sections(text, heading_re):
    """Split text on a heading regex into (preamble, [(heading, body), ...])."""
    parts = heading_re.split(text)
    preamble = parts[0]
    sections = []
    for i in range(1, len(parts), 2):
        heading = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        sections.append((heading, body))
    return preamble, sections


def parse_table_block(body):
    """Parse the first markdown table found in `body` into (header, rows)."""
    lines = [l for l in body.split("\n") if l.strip().startswith("|")]
    if not lines:
        return [], []

    def split_row(line):
        line = line.strip()
        inner = line[1:-1] if line.endswith("|") else line[1:]
        return [c.strip() for c in inner.split("|")]

    header = split_row(lines[0])
    rows = [split_row(l) for l in lines[2:]]  # lines[1] is the |---|---| separator
    return header, rows


def parse_file(text):
    """Parse a wiki file's text into a WikiFile."""
    preamble, h1_sections = _split_sections(text, H1_RE)
    tables_body = notes_body = None
    for heading, body in h1_sections:
        name = heading.strip()
        if name == "Tables":
            tables_body = body
        elif name == "Detailed Notes":
            notes_body = body
        else:
            raise ValueError(f"Unexpected top-level heading: {heading!r}")

    if tables_body is None:
        raise ValueError("No '# Tables' section found")
    if notes_body is None:
        raise ValueError("No '# Detailed Notes' section found")

    tables = []
    _, table_sections = _split_sections(tables_body, H2_RE)
    for category, body in table_sections:
        header, rows = parse_table_block(body)
        tables.append(Table(category=category.strip(), header=header, rows=rows))

    notes = []
    _, note_sections = _split_sections(notes_body, H2_RE)
    for heading, body in note_sections:
        notes.append(Note(heading=heading.strip(), body=body.strip("\n")))

    return WikiFile(tables=tables, notes=notes, preamble=preamble)


def render_table(header, rows):
    """Render a header + rows back into padded markdown table lines."""
    widths = [len(h) for h in header]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(cell))

    def render_row(cells):
        padded = [
            cell.ljust(widths[i]) if i < len(widths) else cell
            for i, cell in enumerate(cells)
        ]
        return "| " + " | ".join(padded) + " |"

    lines = [render_row(header), "|" + "|".join("-" * (w + 2) for w in widths) + "|"]
    lines.extend(render_row(row) for row in rows)
    return lines


def render_file(wf):
    """Render a WikiFile back into the file's full markdown text."""
    out = []
    if wf.preamble.strip():
        out.append(wf.preamble.strip("\n"))
        out.append("")
    out.append("# Tables")
    out.append("")
    for table in wf.tables:
        out.append(f"## {table.category}")
        out.append("")
        out.extend(render_table(table.header, table.rows))
        out.append("")
    out.append("# Detailed Notes")
    out.append("")
    for note in wf.notes:
        out.append(f"## {note.heading}")
        out.append("")
        out.append(note.body.strip())
        out.append("")
    return "\n".join(out).rstrip("\n") + "\n"


def github_slug(heading):
    """Approximate GitHub's heading-anchor slug algorithm.

    Lowercases, strips anything that's not a (unicode) word character, space, or
    hyphen, then turns each space into a hyphen — without collapsing runs of
    spaces first, so e.g. "4505 Burgers & BBQ" (where "&" is stripped, leaving two
    spaces) slugs to "4505-burgers--bbq", matching GitHub's actual behavior.
    """
    s = heading.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    return "-".join(s.strip().split(" "))


def area_index(header):
    """Return the index of the 'Area' column, or None if not present."""
    return header.index("Area") if "Area" in header else None
