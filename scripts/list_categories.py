#!/usr/bin/env python3
"""List each file's category tables (the '##' headings under '# Tables') and their row counts.

Usage:
    scripts/list_categories.py FILE...
"""

import sys

from wiki_lib import parse_file


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    for path in argv:
        with open(path, encoding="utf-8") as f:
            wf = parse_file(f.read())
        print(f"{path}:")
        for table in wf.tables:
            print(f"  {table.category} ({len(table.rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
