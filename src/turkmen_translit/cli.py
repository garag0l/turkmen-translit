"""Command-line interface for turkmen-translit.

tr-tm "Түркменистан"            # auto-detect, convert to the other script
tr-tm --to-latin "Aşgabat"      # force a direction
echo "..." | tr-tm              # read stdin
tr-tm --detect "salam"          # just report the script
tr-tm -i in.txt -o out.txt      # files (UTF-8)
"""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .translit import cyrillic_to_latin, detect_script, latin_to_cyrillic


def _convert(text: str, direction: str) -> str:
    if direction == "to-latin":
        return cyrillic_to_latin(text)
    if direction == "to-cyrillic":
        return latin_to_cyrillic(text)
    # auto
    script = detect_script(text)
    if script == "cyrillic":
        return cyrillic_to_latin(text)
    if script == "latin":
        return latin_to_cyrillic(text)
    # mixed/unknown: default to normalising toward the current official script
    return cyrillic_to_latin(text)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="tr-tm",
        description="Transliterate Turkmen between Cyrillic (legacy) and Latin "
        "(current official script).",
    )
    p.add_argument("text", nargs="*", help="text to convert (or read stdin)")
    g = p.add_mutually_exclusive_group()
    g.add_argument(
        "--to-latin",
        action="store_const",
        dest="direction",
        const="to-latin",
        help="Cyrillic -> Latin",
    )
    g.add_argument(
        "--to-cyrillic",
        action="store_const",
        dest="direction",
        const="to-cyrillic",
        help="Latin -> Cyrillic (best effort)",
    )
    p.add_argument("--detect", action="store_true", help="print the detected script and exit")
    p.add_argument("-i", "--input", help="read UTF-8 text from this file")
    p.add_argument("-o", "--output", help="write UTF-8 result to this file")
    p.add_argument("--version", action="version", version=f"turkmen-translit {__version__}")
    p.set_defaults(direction="auto")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.input:
        with open(args.input, encoding="utf-8") as fh:
            text = fh.read()
    elif args.text:
        text = " ".join(args.text)
    else:
        text = sys.stdin.read()

    if args.detect:
        result = detect_script(text) + "\n"
    else:
        result = _convert(text, args.direction)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(result)
    else:
        # Force UTF-8 on a real console (e.g. Windows cp1252) when possible;
        # test/capture streams don't expose reconfigure, so guard it.
        reconfigure = getattr(sys.stdout, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except (ValueError, OSError):
                pass
        sys.stdout.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
