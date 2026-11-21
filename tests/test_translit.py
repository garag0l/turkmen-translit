from turkmen_translit import cyrillic_to_latin, detect_script, latin_to_cyrillic


class TestKnownWords:
    def test_turkmenistan(self):
        assert cyrillic_to_latin("Түркменистан") == "Türkmenistan"

    def test_ashgabat(self):
        # Latin -> Cyrillic (ş -> ш)
        assert latin_to_cyrillic("Aşgabat") == ("Ашгабат")

    def test_salam(self):
        # All-core-letter word round-trips both ways.
        assert cyrillic_to_latin("салам") == "salam"
        assert latin_to_cyrillic("salam") == "салам"


class TestCase:
    def test_single_capital_iotated_is_titlecase(self):
        # Я alone -> Ýa (title case), not ÝA
        assert cyrillic_to_latin("Я") == "Ýa"

    def test_capital_iotated_in_allcaps_run(self):
        # ЯН -> ÝAN (all caps, neighbour is uppercase)
        assert cyrillic_to_latin("ЯН") == "ÝAN"

    def test_capital_iotated_titlecase_word(self):
        # Яз -> Ýaz (title word, neighbour is lowercase)
        assert cyrillic_to_latin("Яз") == "Ýaz"

    def test_lowercase_iotated(self):
        assert cyrillic_to_latin("я") == "ýa"  # я -> ýa


class TestPassthrough:
    def test_ascii_and_punctuation_untouched(self):
        assert cyrillic_to_latin("OK! 123 (test)") == "OK! 123 (test)"

    def test_newlines_and_spaces_preserved(self):
        src = "салам\nсалам"
        assert cyrillic_to_latin(src) == "salam\nsalam"

    def test_empty_string(self):
        assert cyrillic_to_latin("") == ""
        assert latin_to_cyrillic("") == ""


class TestDocumentedLossyCases:
    """These are intentionally NOT round-trip identity; see tables.py docstring."""

    def test_hard_and_soft_signs_dropped(self):
        assert cyrillic_to_latin("ъь") == ""

    def test_tse_maps_to_s(self):
        assert cyrillic_to_latin("ц") == "s"  # ц -> s

    def test_iotated_does_not_recover_from_latin(self):
        # я -> ýa, and ýa -> йа (not back to я). Documented behaviour.
        lat = cyrillic_to_latin("я")  # -> ýa
        assert latin_to_cyrillic(lat) == "йа"  # йа


class TestDetect:
    def test_cyrillic(self):
        assert detect_script("Түркмен") == "cyrillic"

    def test_latin(self):
        assert detect_script("Turkmen dili") == "latin"

    def test_latin_with_diacritics(self):
        assert detect_script("Aşgabat") == "latin"

    def test_mixed(self):
        assert detect_script("Aşgabat Ашгабат") == "mixed"

    def test_unknown(self):
        assert detect_script("123 !@#") == "unknown"
