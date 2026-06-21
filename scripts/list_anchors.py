#!/usr/bin/env python3
"""List every anchor under '# Detailed Notes' in each file, and flag collisions.

An anchor is the GitHub-style slug of a '##' heading in Detailed Notes. Check this
before adding a new place, so its heading doesn't collide with an existing slug
(GitHub would silently disambiguate collisions with a '-1', '-2', ... suffix, which
this wiki's Link columns don't account for).

Usage:
    scripts/list_anchors.py FILE...
"""

import sys
from collections import defaultdict

from wiki_lib import github_slug, parse_file


def main(argv):
    if not argv:
        print(__doc__)
        return 1

    exit_code = 0
    for path in argv:
        with open(path, encoding="utf-8") as f:
            wf = parse_file(f.read())

        by_slug = defaultdict(list)
        for note in wf.notes:
            by_slug[github_slug(note.heading)].append(note.heading)

        print(f"{path}:")
        for slug in sorted(by_slug):
            headings = by_slug[slug]
            if len(headings) > 1:
                print(f"  #{slug}  COLLISION: {headings!r}")
                exit_code = 1
            else:
                print(f"  #{slug}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
