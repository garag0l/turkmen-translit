"""turkmen-translit: Turkmen Cyrillic <-> Latin transliteration.

>>> from turkmen_translit import cyrillic_to_latin, latin_to_cyrillic
>>> cyrillic_to_latin("Түркменистан")
'Türkmenistan'
>>> latin_to_cyrillic("Aşgabat")
'Ашгабат'
"""

from __future__ import annotations

from .translit import cyrillic_to_latin, detect_script, latin_to_cyrillic

__all__ = ["__version__", "cyrillic_to_latin", "detect_script", "latin_to_cyrillic"]
__version__ = "0.1.0"
