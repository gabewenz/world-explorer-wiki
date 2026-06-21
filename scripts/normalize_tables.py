#!/usr/bin/env python3
"""Re-sort every table's rows alphabetically by Area, and re-pad columns.

Per CLAUDE.md, rows within a table should be sorted alphabetically by the Area
column (ties broken by Name), and columns should be space-padded to stay aligned.
This script restores both invariants after manual edits drift out of sync.

Usage:
    scripts/normalize_tables.py FILE...           # print a diff, don't write
    scripts/normalize_tables.py --write FILE...   # apply changes in place
"""

import difflib
import sys

from wiki_lib import area_index, parse_file, render_file


def normalize_text(text):
    wf = parse_file(text)
    for table in wf.tables:
        idx = area_index(table.header)
        if idx is None:
            continue
        name_idx = table.header.index("Name") if "Name" in table.header else 0
        table.rows.sort(key=lambda r: (r[idx].lower(), r[name_idx].lower()))
    return render_file(wf)


def main(argv):
    write = "--write" in argv
    paths = [a for a in argv if a != "--write"]
    if not paths:
        print(__doc__)
        return 1

    changed = False
    for path in paths:
        with open(path, encoding="utf-8") as f:
            original = f.read()
        updated = normalize_text(original)
        if updated == original:
            continue
        changed = True
        if write:
            with open(path, "w", encoding="utf-8") as f:
                f.write(updated)
            print(f"normalized {path}")
        else:
            diff = difflib.unified_diff(
                original.splitlines(keepends=True),
                updated.splitlines(keepends=True),
                fromfile=path,
                tofile=path,
            )
            sys.stdout.writelines(diff)

    if changed and not write:
        print("\n(no changes written; pass --write to apply)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
