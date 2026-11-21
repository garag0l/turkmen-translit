"""Letter tables for Turkmen Cyrillic (1940-1993) <-> Latin (1999-present).

The modern Turkmen Latin alphabet has 30 letters and is the current official
script of Turkmenistan. The Cyrillic alphabet is the legacy 1940-1993 script.

Source of the letter correspondences: Wikipedia "Turkmen alphabet", cross-checked
against the BGN/PCGN 2000 romanization system for Turkmen. The reputation-
critical pairs are encoded explicitly below so they can be reviewed at a glance:

    Ж -> z-caron (z with hacek)   "zh" sound /zh/
    Dzh (Cyrillic) -> j            "j"  sound /dzh/
    Й -> y-acute                   /j/ glide
    Ң -> n-caron                   /ng/
    Ә -> a-diaeresis               /ae/
    В -> w                         /w ~ beta/
    Ы -> y                         /back unrounded i/
    И -> i                         /i/

Design note (read docs/orthography.md for the full rationale):

Cyrillic -> Latin is the authoritative, well-defined direction (legacy text
converted to the current script). Every core letter is 1:1. A small set of
legacy Cyrillic letters has no single-letter Latin form:

    Yo -> "yo"-glide,  Yu -> "yu"-glide,  Ya -> "ya"-glide   (iotated)
    Shch -> two letters,  hard sign / soft sign -> dropped
    Ц -> s                                               (loanword convention)

Latin -> Cyrillic is a documented best-effort inverse: it maps the 30 core
letters back exactly, and treats the Latin glide letter as the plain consonant
(not as an iotated vowel), because modern Latin text uses it as a standalone
consonant and the iotated reading is genuinely ambiguous. So the round trip is
identity on the core alphabet, and intentionally not identity on the iotated and
loanword letters. The tests pin this behaviour precisely.
"""

from __future__ import annotations

# --- Core 1:1 correspondences, lowercase Cyrillic -> lowercase Latin. --------
# These are reversible. Written with explicit unicode escapes so the exact code
# point is unambiguous in review and never mangled by an editor or a shell.

_CORE: dict[str, str] = {
    "а": "a",  # а  -> a
    "б": "b",  # б  -> b
    "в": "w",  # в  -> w
    "г": "g",  # г  -> g
    "д": "d",  # д  -> d
    "ж": "ž",  # ж  -> ž  (z-caron)
    "з": "z",  # з  -> z
    "и": "i",  # и  -> i
    "й": "ý",  # й  -> ý  (y-acute)
    "к": "k",  # к  -> k
    "л": "l",  # л  -> l
    "м": "m",  # м  -> m
    "н": "n",  # н  -> n
    "ң": "ň",  # ң  -> ň  (n-caron)
    "о": "o",  # о  -> o
    "ө": "ö",  # ө  -> ö
    "п": "p",  # п  -> p
    "р": "r",  # р  -> r
    "с": "s",  # с  -> s
    "т": "t",  # т  -> t
    "у": "u",  # у  -> u
    "ү": "ü",  # ү  -> ü
    "ф": "f",  # ф  -> f
    "х": "h",  # х  -> h
    "ч": "ç",  # ч  -> ç
    "ш": "ş",  # ш  -> ş
    "ы": "y",  # ы  -> y
    "е": "e",  # е  -> e  (common /e/; the one Latin e reverses to)
    "ә": "ä",  # ә  -> ä
    "җ": "j",  # җ  -> j  (Cyrillic zhe with descender)
}

# --- Cyrillic letters with no single-letter Latin form (forward only). -------
# Documented conventions; see docs/orthography.md. Cyrillic -> Latin only.

_CYR_ONLY: dict[str, str] = {
    "э": "e",  # э  -> e   (rare; same Latin e as е, which e reverses to)
    "ё": "ýo",  # ё  -> ýo
    "ю": "ýu",  # ю  -> ýu
    "я": "ýa",  # я  -> ýa
    "ц": "s",  # ц  -> s   (loanword convention)
    "щ": "şç",  # щ -> şç
    "ъ": "",  # ъ  -> (hard sign dropped)
    "ь": "",  # ь  -> (soft sign dropped)
}


def _titlecase_multi(s: str) -> str:
    """Capitalise only the first letter of a multi-char Latin output (Ýa)."""
    return s[:1].upper() + s[1:] if s else s


def _build_cyr_to_lat() -> dict[str, str]:
    """Full Cyrillic->Latin map, both cases, including multi-char outputs.

    For an uppercase Cyrillic source letter we cannot know from the letter alone
    whether to emit "ÝA" or "Ýa"; that depends on the following letter's case.
    So here we only record the *title* form (Ýa) for uppercase sources; the
    transliterator fixes up all-caps runs using neighbour case.
    """
    out: dict[str, str] = {}
    for cyr, lat in {**_CORE, **_CYR_ONLY}.items():
        out[cyr] = lat
        out[cyr.upper()] = _titlecase_multi(lat)
    return out


def _build_lat_to_cyr() -> list[tuple[str, str]]:
    """Latin->Cyrillic pairs, longest Latin sequence first for greedy matching.

    Only the core 1:1 letters invert. The glide letter ý inverts to й (not to an
    iotated vowel); see the module docstring.
    """
    pairs: list[tuple[str, str]] = []
    for cyr, lat in _CORE.items():
        pairs.append((lat, cyr))
        pairs.append((lat.upper(), cyr.upper()))
    # Longest Latin key first so multi-codepoint sequences would win if added.
    pairs.sort(key=lambda p: len(p[0]), reverse=True)
    return pairs


CYR_TO_LAT: dict[str, str] = _build_cyr_to_lat()
LAT_TO_CYR_PAIRS: list[tuple[str, str]] = _build_lat_to_cyr()

# The 30 letters of the modern Turkmen Latin alphabet, in official order.
LATIN_ALPHABET: tuple[str, ...] = (
    "A",
    "B",
    "Ç",
    "D",
    "E",
    "Ä",
    "F",
    "G",
    "H",
    "I",
    "J",
    "Ž",
    "K",
    "L",
    "M",
    "N",
    "Ň",
    "O",
    "Ö",
    "P",
    "R",
    "S",
    "Ş",
    "T",
    "U",
    "Ü",
    "W",
    "Y",
    "Ý",
    "Z",
)
