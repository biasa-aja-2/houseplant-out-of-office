#!/usr/bin/env python3
"""The Houseplant Out-of-Office — make.fun bounty entry.

Writes one out-of-office auto-reply, as if sent by the office fern, to
``/output/entry.txt`` (or ``$MAKEFUN_OUTPUT_DIR/entry.txt``).

The joke: the fern has been ignored since March — unwatered, unnoticed —
and has responded the only way a neglected houseplant can: it has
unionised with the dust. The cactus, the one plant that needs nobody,
gets the overflow. Plant life (water, neglect, the dust on the leaves)
drives the joke; the office-auto-reply frame carries it.

Pure Python standard library only. Output is fully deterministic: the
same single line, byte for byte, on every run.
"""

import os
import sys

# The entry: one line, 99 characters, well inside the 120-character gate.
ENTRY = (
    "Out of office. I'm a fern, unwatered since March, "
    "and I've unionised with the dust. Ask the cactus."
)

MAX_CHARS = 120


def check_entry(text):
    """Enforce the competition gate before anything is written."""
    if not isinstance(text, str):
        return "entry is not text"
    if not text.strip():
        return "entry is blank or whitespace only"
    if len(text) != len(text.strip()):
        return "entry has leading or trailing whitespace"
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        return "entry contains control characters"
    if not (1 <= len(text) <= MAX_CHARS):
        return "entry is %d characters, gate is 1-%d" % (len(text), MAX_CHARS)
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return "entry is not valid UTF-8"
    return None


def main():
    problem = check_entry(ENTRY)
    if problem is not None:
        print("refusing to write entry: %s" % problem, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)
    os.chmod(path, 0o644)

    # Read back and verify what landed on disk, byte for byte.
    with open(path, "rb") as handle:
        written = handle.read()
    if written != ENTRY.encode("utf-8"):
        print("verification failed: bytes on disk differ", file=sys.stderr)
        return 1
    if len(written.decode("utf-8")) != len(ENTRY):
        print("verification failed: character count drifted", file=sys.stderr)
        return 1

    print("wrote %s (%d chars)" % (path, len(ENTRY)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
