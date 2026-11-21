# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/), and this project adheres to
[Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-11-21

Initial release.

### Added
- `cyrillic_to_latin`, `latin_to_cyrillic` and `detect_script` in the
  `turkmen_translit` package (zero third-party dependencies).
- `tr-tm` command-line tool: auto-detect direction, `--to-latin` /
  `--to-cyrillic`, `--detect`, stdin, and `-i`/`-o` UTF-8 file conversion.
- Full 30-letter modern Turkmen Latin alphabet correspondence with the legacy
  1940–1993 Cyrillic alphabet, with the commonly-mistaken letters (Ж→ž vs
  Җ→j, Й→ý, Ң→ň, Ә→ä, В→w, Ы→y) pinned by tests.
- `docs/orthography.md` recording every transliteration decision and its source.
- Case-aware handling of the multi-letter glides (`ЯН → ÝAN`, `Яз → Ýaz`).
- CI across Linux/macOS/Windows on Python 3.9–3.13.

### Notes
- Cyrillic → Latin is the authoritative direction. Latin → Cyrillic is a
  documented best-effort inverse (the glide letter `ý` maps back to `Й`, not to
  an iotated vowel). See `docs/orthography.md`.
