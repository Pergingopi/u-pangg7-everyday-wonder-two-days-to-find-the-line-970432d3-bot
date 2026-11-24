#!/usr/bin/env python3
"""Everyday Wonder, Two Days to Find the Line - one sentence of wonder.

Pure Python 3.13 standard library. The program writes one sentence to
/output/entry.txt. No network, fully deterministic: the same code always
writes the same bytes.

The entry (109 characters, no trailing newline):
    The washing machine window turns my dirty socks into a small, patient aquarium where nothing ever swims away.

Why this line: a washing machine's round window is an everyday sight, and
calling it a patient aquarium reframes the tumbling laundry as something
quietly alive - then the twist, nothing ever swims away, lands the wonder
in a single read while staying grounded in a real chore. Before writing,
the program asserts the entry is a single non-blank sentence of 1-200
characters, so a bad edit fails loudly here instead of shipping an
invalid entry.

Usage: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os

ENTRY = "The washing machine window turns my dirty socks into a small, patient aquarium where nothing ever swims away."


def _write_all(f, data):
    view = memoryview(data)
    while view:
        n = f.write(view)
        if n is None:
            raise OSError("write returned None")
        view = view[n:]


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    # Clean only the contents of the output directory, never the folder
    # itself: the grader mounts it.
    for name in os.listdir(out_dir):
        path = os.path.join(out_dir, name)
        if os.path.isfile(path) or os.path.islink(path):
            os.unlink(path)
    # Gate check: one sentence, 1-200 characters, no trailing newline.
    assert 1 <= len(ENTRY) <= 200, "ENTRY must be 1-200 characters"
    assert ENTRY == ENTRY.strip(), "ENTRY must not have leading/trailing whitespace"
    assert "\n" not in ENTRY and "\r" not in ENTRY, "ENTRY must be a single line"
    assert ENTRY.endswith("."), "ENTRY must end with a single terminator"
    assert ENTRY.count(".") == 1, "ENTRY must be exactly one sentence"
    data = ENTRY.encode("utf-8")
    assert 1 <= len(data) <= 200, "entry.txt must be 1-200 bytes"
    tmp = os.path.join(out_dir, ".entry.txt.tmp")
    final = os.path.join(out_dir, "entry.txt")
    # Stale-tmp retry: a leftover temp file from an earlier run is removed.
    for attempt in range(3):
        try:
            with open(tmp, "wb") as f:
                _write_all(f, data)
                f.flush()
                os.fsync(f.fileno())
            os.chmod(tmp, 0o644)
            os.replace(tmp, final)
            os.chmod(final, 0o644)
            break
        except OSError:
            try:
                if os.path.exists(tmp):
                    os.unlink(tmp)
            except OSError:
                pass
            if attempt == 2:
                raise


if __name__ == "__main__":
    main()
