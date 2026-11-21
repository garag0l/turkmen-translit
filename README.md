# turkmen-translit

**Convert Turkmen text between the legacy Cyrillic alphabet and the current official Latin alphabet — correctly, including the letters other tools get wrong.**

[![CI](https://github.com/garag0l/turkmen-translit/actions/workflows/ci.yml/badge.svg)](https://github.com/garag0l/turkmen-translit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)
![Zero dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)

Turkmenistan's official script is the Latin alphabet (30 letters). A lot of
older text — books, documents, websites — is still in the 1940–1993 Cyrillic
alphabet. This converts between them from the command line or from Python, with
no dependencies, and with the tricky letters handled explicitly rather than
guessed.

```console
$ tr-tm "Түркменистан"
Türkmenistan
$ tr-tm "Aşgabat"
Ашгабат
$ tr-tm --detect "salam"
latin
```

## Why this exists

Most quick transliterators get the same handful of Turkmen letters wrong,
because they borrow a Russian or Turkish table:

- **Ж → ž** (the /ʒ/ sound) and **Җ → j** (the /dʒ/ sound) are two different
  Cyrillic letters. Tools that map both to `j` (or both to `zh`) corrupt words.
- **В → w**, not `v`.
- **Й → ý**, **Ы → y**, **И → i** — and Turkmen does *not* use the Turkish
  dotless `ı`.

This library encodes the full 30-letter correspondence from the Wikipedia
*Turkmen alphabet* table, cross-checked against the BGN/PCGN 2000 romanization,
and documents every edge case in [docs/orthography.md](docs/orthography.md).

## Install

```bash
pipx install turkmen-translit     # for the tr-tm command
# or
pip install turkmen-translit      # for the library
```

Python 3.9+, no third-party dependencies.

**JavaScript / TypeScript:** the same tables are available as an npm package for
Node and the browser — see [`js/`](js/README.md):

```bash
npm install @garag0l/turkmen-translit
```

## Command line

```bash
tr-tm "Түркменистан"              # auto-detect script, convert to the other one
tr-tm --to-latin "Ашгабат"        # force Cyrillic -> Latin
tr-tm --to-cyrillic "Aşgabat"     # force Latin -> Cyrillic (best effort)
tr-tm --detect "salam"            # just report: cyrillic | latin | mixed | unknown
echo "salam" | tr-tm              # read stdin
tr-tm -i book.txt -o book-latin.txt   # whole files, UTF-8
```

## Python

```python
from turkmen_translit import cyrillic_to_latin, latin_to_cyrillic, detect_script

cyrillic_to_latin("Түркменистан")  # 'Türkmenistan'
latin_to_cyrillic("Aşgabat")  # 'Ашгабат'
detect_script("salam")  # 'latin'
```

Characters outside the alphabet (ASCII, digits, punctuation, whitespace, other
scripts) pass through unchanged. Capitalisation is preserved, including all-caps
words with the multi-letter glides (`ЯН → ÝAN`, `Яз → Ýaz`).

## Which direction is reliable?

**Cyrillic → Latin is the authoritative direction** — converting legacy text to
the current official script. Every core letter is 1:1.

**Latin → Cyrillic is a documented best-effort.** The modern Latin script merged
some distinctions the old Cyrillic kept, so the reverse can't always be exact:

- The 30 core letters invert exactly: `salam ↔ салам`.
- The glide letter `ý` goes back to `Й`, never guessed into `Я/Ё/Ю`: `ýa → йа`.
- Letters that are dropped one way (hard/soft sign) don't come back.

Full rules and rationale: [docs/orthography.md](docs/orthography.md). If you find
a word that converts wrong, open an issue with the word and the expected result.

## Tested

- Every one of the 30 core letters round-trips Cyrillic → Latin → Cyrillic,
  upper and lower case.
- The letters tools most often get wrong (Ж/Җ, Й, Ң, Ә, В, Ы) are pinned by
  explicit assertions.
- Known words (`Türkmenistan`, `Aşgabat`, `salam`), capitalisation of the glide
  letters, passthrough, the documented lossy cases, and the CLI (stdin, files,
  flags) all have tests.
- CI runs on Linux/macOS/Windows across Python 3.9–3.13.

## Roadmap

- ~~A JavaScript/TypeScript port sharing these exact tables.~~ Shipped — see
  [`js/`](js/README.md).
- Optional Е/Э disambiguation heuristics for the reverse direction.

## Contributing

Issues and PRs welcome — especially real Turkmen words that transliterate wrong,
with a source for the correct spelling.

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
pytest && ruff check .
```

## License

[MIT](LICENSE). Built by [Murat Bekgi](https://muratbekgi.com).
