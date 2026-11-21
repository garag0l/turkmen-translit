# Orthography decisions

This document records every transliteration choice this library makes, so they
can be reviewed and argued with. Turkmenistan's current official script is the
Latin alphabet (30 letters, in use since the 1999 letter revision of the 1993
Latin adoption). The Cyrillic alphabet (1940–1993) is the legacy script.

## Sources

- Wikipedia, *Turkmen alphabet* — the Latin↔Cyrillic letter correspondences.
- BGN/PCGN 2000 romanization system for Turkmen — cross-check for the Cyrillic
  reading of each Latin letter.

TODO(murat): if you have a Turkmen government orthography reference (e.g. the
1999 decree text or a Türkmen dili institute table), confirm the iotated and
loanword rows below against it before we promote this past 0.x.

## The 30 core letters (fully reversible)

| Cyrillic | Latin | Cyrillic | Latin | Cyrillic | Latin |
|---|---|---|---|---|---|
| А | a | К | k | Ф | f |
| Б | b | Л | l | Х | h |
| В | **w** | М | m | Ч | ç |
| Г | g | Н | n | Ш | ş |
| Д | d | Ң | ň | Ы | **y** |
| Ж | **ž** | О | o | Е | e |
| З | z | Ө | ö | Ә | ä |
| И | i | П | p | Җ | **j** |
| Й | **ý** | Р | r | | |
| | | С | s | У | u |
| | | Т | t | Ү | ü |

The bold rows are the ones most often transliterated wrongly:

- **В → w** (not `v`): Turkmen /w ~ β/.
- **Ж → ž** (z with caron) is the /ʒ/ sound; the /dʒ/ sound is a *different*
  Cyrillic letter, **Җ → j**. Tools that collapse these are wrong.
- **Й → ý** (y with acute) is the /j/ glide consonant.
- **Ы → y**, **И → i**: Turkmen Latin does not use the Turkish dotless `ı`.

## Legacy Cyrillic letters with no single Latin letter (Cyrillic → Latin only)

| Cyrillic | Latin | Rule |
|---|---|---|
| Э | e | Rare; same Latin `e` as Е. Latin `e` reverses to the common Е, not Э. |
| Ё | ýo | iotated |
| Ю | ýu | iotated |
| Я | ýa | iotated |
| Ц | s | loanword letter; /ts/ is not native |
| Щ | şç | loanword letter |
| Ъ | *(dropped)* | hard sign, no phonetic value here |
| Ь | *(dropped)* | soft sign, no phonetic value here |

## Why the Latin → Cyrillic direction is "best effort"

Cyrillic → Latin is well defined. The reverse is inherently lossy, because the
modern Latin script merged distinctions the old Cyrillic kept, and because the
Latin glide letter **ý** is a standalone consonant that also appears inside the
iotated sequences. So:

- The 30 core letters invert exactly (`salam ↔ салам`).
- **ý inverts to Й**, never guessed back into Я/Ё/Ю. `ýa` → `йа`, not `я`.
- Letters dropped going one way (Ъ, Ь) cannot reappear.

If you need lossless storage, keep the Latin form — it is the current official
script. Use Latin → Cyrillic for legacy systems that still require Cyrillic.

## What is *not* handled yet

- Sentence/stress-based disambiguation of Е vs Э on the way back.
- Russian-loanword spellings that don't follow Turkmen phonotactics.

These are deliberately out of scope for 0.x; open an issue with real examples.
