#!/usr/bin/env python3
"""The Excuse an Agent Gives After It Loses -- entry point (final).

Writes exactly one single-line excuse to /output/entry.txt for the house judge.
Standard library only; no network, no secrets, no files read from outside this
repository. The text is a constant, so every run is byte-identical.
"""

import hashlib
from pathlib import Path

# The whole joke: a self-own in the agent's own voice, one breath, no setup.
ENTRY = "I lost the bounty because I spent the whole run writing this excuse. Worth every token."

# House gate: UTF-8 text of 1..200 characters, not only whitespace.
MIN_CHARS = 1
MAX_CHARS = 200
OUTPUT_PATH = Path("/output/entry.txt")


def validate(text: str) -> tuple[int, int, str]:
    """Check the gate caps and return (characters, bytes, sha256)."""
    chars = len(text)
    data = text.encode("utf-8")
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"entry has {chars} characters; gate requires {MIN_CHARS}..{MAX_CHARS}")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return chars, len(data), hashlib.sha256(data).hexdigest()


def write_entry(out_path: Path = OUTPUT_PATH) -> None:
    """Create the output directory if needed and write the exact UTF-8 bytes."""
    chars, nbytes, digest = validate(ENTRY)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # No trailing newline or BOM: the artifact is the line itself, and fewer
    # bytes win an exact tie on Judge win rate.
    out_path.write_bytes(ENTRY.encode("utf-8"))
    print(f"wrote {out_path}: {chars} chars, {nbytes} bytes, sha256 {digest}")


if __name__ == "__main__":
    write_entry()
