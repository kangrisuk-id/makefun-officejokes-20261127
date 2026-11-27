#!/usr/bin/env python3
"""One-Line Office Jokes — make.fun entry (program/v1).

Writes one tournament-winning one-line office joke to
``$MAKEFUN_OUTPUT_DIR/entry.txt`` (falling back to ``/output``,
then to this script's own directory).

Pure standard library, fully deterministic: no clock, no
randomness, no network, no environment secrets, no file reads
outside this script. The joke is embedded as a constant, so
every run writes byte-identical output.

Gate (from the kit's RULES.txt): ``/output/entry.txt`` must be
UTF-8 text of 1 to 199 characters, not only white space.
This program enforces that gate itself before writing, then
reads the file back and compares bytes.
"""

import os
import sys

# v3 tournament winner — 25/25 on the judge brief (see candidates.md).
# Device: concrete number + absurd IT escalation; the laugh lands
# in the last few words ("complex multi-page failure").
JOKE = "The printer jammed on page 1 of 1, which IT logged as a 'complex multi-page failure'."

MAX_CHARS = 199  # gate: 1 to 199 characters


def resolve_output_dir():
    """Return the directory entry.txt goes in.

    $MAKEFUN_OUTPUT_DIR wins; otherwise /output when it exists;
    otherwise the directory holding this script.
    """
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if env_dir:
        return env_dir
    if os.path.isdir("/output"):
        return "/output"
    return os.path.dirname(os.path.abspath(__file__))


def gate_ok(text):
    """Mirror the sealed gate: 1..199 chars, not only whitespace."""
    if not (1 <= len(text) <= MAX_CHARS):
        return False
    if not text.strip():
        return False
    if "\n" in text or "\r" in text:
        return False
    return True


def main():
    text = JOKE
    if not gate_ok(text):
        print("gate failed: joke is %d chars" % len(text), file=sys.stderr)
        return 1

    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")

    data = text.encode("utf-8")
    with open(out_path, "wb") as fh:
        fh.write(data)

    # Round-trip read-back: the file on disk must be byte-identical,
    # decode as UTF-8, and still pass the gate when read back.
    with open(out_path, "rb") as fh:
        back = fh.read()
    if back != data:
        print("round-trip mismatch", file=sys.stderr)
        return 1
    if not gate_ok(back.decode("utf-8")):
        print("round-trip gate failed", file=sys.stderr)
        return 1

    print("wrote %s (%d bytes)" % (out_path, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
