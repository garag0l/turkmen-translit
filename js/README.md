# @garag0l/turkmen-translit

**Transliterate Turkmen between the legacy Cyrillic and the current official Latin alphabet — in Node or the browser, zero dependencies.**

The JavaScript/TypeScript port of [turkmen-translit](https://github.com/garag0l/turkmen-translit). It uses the exact same letter tables as the Python package, so results are identical, and ships with TypeScript types.

## Install

```bash
npm install @garag0l/turkmen-translit
```

## Use

```js
import {
  cyrillicToLatin,
  latinToCyrillic,
  detectScript,
} from "@garag0l/turkmen-translit";

cyrillicToLatin("Түркменистан"); // "Türkmenistan"
latinToCyrillic("Aşgabat");      // "Ашгабат"
detectScript("salam");           // "latin"
```

It is pure ESM with no dependencies, so it runs the same in Node (18+) and in the
browser via a bundler. TypeScript definitions are included.

## CLI

```bash
npx @garag0l/turkmen-translit "Түркменистан"   # Türkmenistan
tr-tm --to-cyrillic "Aşgabat"                   # Ашгабат (after global install)
tr-tm --detect "salam"                          # latin
echo "salam" | tr-tm                            # салам
```

## Which direction is reliable?

Cyrillic → Latin is authoritative (legacy text to the current official script).
Latin → Cyrillic is a documented best-effort inverse: the 30 core letters invert
exactly, and the glide letter `ý` maps back to `Й`, not to an iotated vowel. Full
rules and rationale: [docs/orthography.md](../docs/orthography.md).

## License

[MIT](../LICENSE). Built by [Murat Bekgi](https://muratbekgi.com).
