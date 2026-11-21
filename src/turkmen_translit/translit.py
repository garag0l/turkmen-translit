"""Turkmen Cyrillic <-> Latin transliteration.

Public API:
    cyrillic_to_latin(text) -> str
    latin_to_cyrillic(text) -> str
    detect_script(text) -> "cyrillic" | "latin" | "mixed" | "unknown"

Characters the tables don't cover (ASCII, digits, punctuation, whitespace,
emoji, other scripts) pass through unchanged.
"""

from __future__ import annotations

from .tables import CYR_TO_LAT, LAT_TO_CYR_PAIRS

# Build a lookup dict and the longest key length once, for greedy matching.
_LAT_TO_CYR: dict[str, str] = {lat: cyr for lat, cyr in LAT_TO_CYR_PAIRS}
_LAT_MAX_KEY: int = max((len(lat) for lat, _ in LAT_TO_CYR_PAIRS), default=1)

# Cyrillic block membership, for script detection.
_CYR_RANGES = ((0x0400, 0x04FF), (0x0500, 0x052F))


def _is_cyrillic_char(ch: str) -> bool:
    cp = ord(ch)
    return any(lo <= cp <= hi for lo, hi in _CYR_RANGES)


def _nearest_neighbour_is_upper(text: str, i: int) -> bool:
    """True if the closest adjacent cased letter (prev first, then next) is
    uppercase. Used to decide whether a multi-char expansion of an uppercase
    source letter (e.g. Я) should be title-case (Ýa) or all-caps (ÝA)."""
    j = i - 1
    while j >= 0:
        if text[j].isalpha():
            return text[j].isupper()
        j -= 1
    j = i + 1
    while j < len(text):
        if text[j].isalpha():
            return text[j].isupper()
        j += 1
    return False


def cyrillic_to_latin(text: str) -> str:
    """Transliterate Turkmen Cyrillic text to the modern Latin alphabet."""
    out: list[str] = []
    for i, ch in enumerate(text):
        mapped = CYR_TO_LAT.get(ch)
        if mapped is None:
            out.append(ch)
            continue
        if ch.isupper() and len(mapped) > 1:
            # Multi-char expansion (ýo/ýu/ýa/şç) of an uppercase source letter.
            if _nearest_neighbour_is_upper(text, i):
                out.append(mapped.upper())
            else:
                out.append(mapped[:1].upper() + mapped[1:])
        else:
            out.append(mapped)
    return "".join(out)


def latin_to_cyrillic(text: str) -> str:
    """Transliterate modern Turkmen Latin text to the legacy Cyrillic alphabet.

    Best-effort inverse (see tables.py module docstring): the 30 core letters
    invert exactly; the glide letter ý inverts to й, not to an iotated vowel.
    """
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        matched = False
        upper = min(_LAT_MAX_KEY, n - i)
        for length in range(upper, 0, -1):
            chunk = text[i : i + length]
            cyr = _LAT_TO_CYR.get(chunk)
            if cyr is not None:
                out.append(cyr)
                i += length
                matched = True
                break
        if not matched:
            out.append(text[i])
            i += 1
    return "".join(out)


def detect_script(text: str) -> str:
    """Classify text as 'cyrillic', 'latin', 'mixed', or 'unknown'.

    Only cased letters count. A string with no letters is 'unknown'.
    """
    cyr = lat = 0
    for ch in text:
        if not ch.isalpha():
            continue
        if _is_cyrillic_char(ch):
            cyr += 1
        elif ch.isascii() or ch in CYR_TO_LAT.values() or _looks_latin(ch):
            lat += 1
    if cyr and lat:
        return "mixed"
    if cyr:
        return "cyrillic"
    if lat:
        return "latin"
    return "unknown"


_LATIN_EXTRA = set("çÇşŞžŽňŇäÄöÖüÜýÝ")


def _looks_latin(ch: str) -> bool:
    if ch in _LATIN_EXTRA:
        return True
    cp = ord(ch)
    return 0x0041 <= cp <= 0x024F  # Latin + Latin-1 supplement + extended
