// Turkmen Cyrillic <-> Latin transliteration (zero dependencies, ESM).
// Mirrors the Python package turkmen_translit; see ../../docs/orthography.md.

import { CYR_TO_LAT, LAT_TO_CYR, LAT_MAX_KEY } from "./tables.js";

const CYR_RANGES = [
  [0x0400, 0x04ff],
  [0x0500, 0x052f],
];

const LATIN_EXTRA = new Set([..."çÇşŞžŽňŇäÄöÖüÜýÝ"]);

function isCyrillicChar(ch) {
  const cp = ch.codePointAt(0);
  return CYR_RANGES.some(([lo, hi]) => cp >= lo && cp <= hi);
}

function looksLatin(ch) {
  if (LATIN_EXTRA.has(ch)) return true;
  const cp = ch.codePointAt(0);
  return cp >= 0x0041 && cp <= 0x024f;
}

function isAlpha(ch) {
  return ch.toLowerCase() !== ch.toUpperCase();
}

function nearestNeighbourIsUpper(text, i) {
  for (let j = i - 1; j >= 0; j--) {
    if (isAlpha(text[j])) return text[j] === text[j].toUpperCase();
  }
  for (let j = i + 1; j < text.length; j++) {
    if (isAlpha(text[j])) return text[j] === text[j].toUpperCase();
  }
  return false;
}

/** Transliterate Turkmen Cyrillic text to the modern Latin alphabet. */
export function cyrillicToLatin(text) {
  const chars = [...text];
  const out = [];
  for (let i = 0; i < chars.length; i++) {
    const ch = chars[i];
    const mapped = CYR_TO_LAT[ch];
    if (mapped === undefined) {
      out.push(ch);
      continue;
    }
    const isUpper = isAlpha(ch) && ch === ch.toUpperCase();
    if (isUpper && mapped.length > 1) {
      out.push(
        nearestNeighbourIsUpper(chars, i)
          ? mapped.toUpperCase()
          : mapped[0].toUpperCase() + mapped.slice(1),
      );
    } else {
      out.push(mapped);
    }
  }
  return out.join("");
}

/**
 * Transliterate modern Turkmen Latin text to legacy Cyrillic (best effort).
 * The 30 core letters invert exactly; ý inverts to й, not an iotated vowel.
 */
export function latinToCyrillic(text) {
  const chars = [...text];
  const out = [];
  let i = 0;
  while (i < chars.length) {
    let matched = false;
    const upper = Math.min(LAT_MAX_KEY, chars.length - i);
    for (let length = upper; length >= 1; length--) {
      const chunk = chars.slice(i, i + length).join("");
      const cyr = LAT_TO_CYR[chunk];
      if (cyr !== undefined) {
        out.push(cyr);
        i += length;
        matched = true;
        break;
      }
    }
    if (!matched) {
      out.push(chars[i]);
      i += 1;
    }
  }
  return out.join("");
}

/** Classify text as "cyrillic", "latin", "mixed", or "unknown". */
export function detectScript(text) {
  let cyr = 0;
  let lat = 0;
  for (const ch of text) {
    if (!isAlpha(ch)) continue;
    if (isCyrillicChar(ch)) cyr += 1;
    else if (looksLatin(ch)) lat += 1;
  }
  if (cyr && lat) return "mixed";
  if (cyr) return "cyrillic";
  if (lat) return "latin";
  return "unknown";
}

export { LATIN_ALPHABET } from "./tables.js";
