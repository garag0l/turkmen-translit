"""The letter tables are the reputation-critical part: pin every pairing."""

from turkmen_translit.tables import _CORE, CYR_TO_LAT, LATIN_ALPHABET
from turkmen_translit.translit import cyrillic_to_latin, latin_to_cyrillic


def test_modern_latin_alphabet_has_30_letters():
    assert len(LATIN_ALPHABET) == 30
    assert len(set(LATIN_ALPHABET)) == 30


def test_the_tricky_pairs_are_correct():
    # The pairs that transliteration tools most often get wrong.
    assert CYR_TO_LAT["ж"] == "ž"  # Ж -> ž (z-caron), NOT j
    assert CYR_TO_LAT["җ"] == "j"  # Җ -> j, NOT ž
    assert CYR_TO_LAT["й"] == "ý"  # Й -> ý (y-acute)
    assert CYR_TO_LAT["ң"] == "ň"  # Ң -> ň (n-caron)
    assert CYR_TO_LAT["ә"] == "ä"  # Ә -> ä
    assert CYR_TO_LAT["в"] == "w"  # В -> w, NOT v
    assert CYR_TO_LAT["ы"] == "y"  # Ы -> y
    assert CYR_TO_LAT["и"] == "i"  # И -> i
    assert CYR_TO_LAT["ү"] == "ü"  # Ү -> ü
    assert CYR_TO_LAT["ө"] == "ö"  # Ө -> ö


def test_every_core_letter_round_trips_cyrillic_latin_cyrillic():
    for cyr in _CORE:
        lat = cyrillic_to_latin(cyr)
        assert latin_to_cyrillic(lat) == cyr, f"{cyr!r} -> {lat!r} did not return"


def test_every_core_letter_round_trips_uppercase():
    for cyr in _CORE:
        up = cyr.upper()
        lat = cyrillic_to_latin(up)
        assert latin_to_cyrillic(lat) == up, f"{up!r} -> {lat!r} did not return"
