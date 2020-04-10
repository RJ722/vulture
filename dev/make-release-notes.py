#! /usr/bin/env python3

import re
import sys

_, VERSION, CHANGELOG, LIST = sys.argv  # skipcq: PYL-W0632
HEADER_REGEX = fr"# {VERSION} \(\d\d\d\d-\d\d-\d\d\)\n"

notes_list = []


with open(CHANGELOG) as f:
    first_line = next(f)
    if not re.match(HEADER_REGEX, first_line):
        sys.exit(
            f'First changelog line "{first_line.rstrip()}" must '
            f'start with "{HEADER_REGEX.rstrip()}"'
        )
    notes_list.extend([first_line[2:], "\n"])
    next(f)  # Skip empty line.
    for line in f:
        if not line.strip():
            break
        else:
            notes_list.append(line)


def check(name, text):
    print("*" * 60)
    print(text)
    print("*" * 60)
    response = input("Accept this %s (Y/n)? " % name).strip().lower()
    if response and response != "y":
        sys.exit(1)


check("changelog", "".join(notes_list))

with open(LIST, "w") as f:
    f.writelines(notes_list)
