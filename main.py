"""The Printer Finally Answers — one line in the office printer's own voice.

The program writes the entry line to
os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")/entry.txt with no trailing
newline, exactly as the gate requires.
"""

import os
import sys

ENTRY = "I have fed you 14,203 sheets and every single one was the final version."

MAX_CHARS = 240


def validate(text: str) -> None:
    """Check the entry against the competition gate before writing it."""
    if not text:
        raise ValueError("entry is empty")
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} characters, must be 1-240")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        raise ValueError("entry contains control characters")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    # The gate counts characters, but the file is read as UTF-8 bytes: make
    # sure the encoded form is also within bounds and round-trips cleanly.
    encoded = text.encode("utf-8")
    if len(encoded) > MAX_CHARS:
        raise ValueError(f"entry is {len(encoded)} UTF-8 bytes, must be <= 240")
    if encoded.decode("utf-8") != text:
        raise ValueError("entry does not round-trip as UTF-8")


def main() -> int:
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
