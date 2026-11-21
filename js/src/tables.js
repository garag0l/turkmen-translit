// Letter tables for Turkmen Cyrillic (1940-1993) <-> Latin (1999-present).
// Ported verbatim from the Python package's tables.py so both stay identical.
// See ../../docs/orthography.md for the rationale behind every pairing.

// Core 1:1 correspondences, lowercase Cyrillic -> lowercase Latin (reversible).
export const CORE = {
  "а": "a", // а -> a
  "б": "b", // б -> b
  "в": "w", // в -> w
  "г": "g", // г -> g
  "д": "d", // д -> d
  "ж": "ž", // ж -> ž (z-caron)
  "з": "z", // з -> z
  "и": "i", // и -> i
  "й": "ý", // й -> ý (y-acute)
  "к": "k", // к -> k
  "л": "l", // л -> l
  "м": "m", // м -> m
  "н": "n", // н -> n
  "ң": "ň", // ң -> ň (n-caron)
  "о": "o", // о -> o
  "ө": "ö", // ө -> ö
  "п": "p", // п -> p
  "р": "r", // р -> r
  "с": "s", // с -> s
  "т": "t", // т -> t
  "у": "u", // у -> u
  "ү": "ü", // ү -> ü
  "ф": "f", // ф -> f
  "х": "h", // х -> h
  "ч": "ç", // ч -> ç
  "ш": "ş", // ш -> ş
  "ы": "y", // ы -> y
  "е": "e", // е -> e (common /e/; the one Latin e reverses to)
  "ә": "ä", // ә -> ä
  "җ": "j", // җ -> j (zhe with descender)
};

// Cyrillic letters with no single-letter Latin form (forward only).
export const CYR_ONLY = {
  "э": "e", // э -> e (rare; same Latin e as е)
  "ё": "ýo", // ё -> ýo
  "ю": "ýu", // ю -> ýu
  "я": "ýa", // я -> ýa
  "ц": "s", // ц -> s (loanword convention)
  "щ": "şç", // щ -> şç
  "ъ": "", // ъ -> (hard sign dropped)
  "ь": "", // ь -> (soft sign dropped)
};

function titlecaseMulti(s) {
  return s ? s[0].toUpperCase() + s.slice(1) : s;
}

// Full Cyrillic->Latin map, both cases. Uppercase sources record the title form
// (Ýa); the transliterator upcases all-caps runs using neighbour case.
export const CYR_TO_LAT = (() => {
  const out = {};
  for (const [cyr, lat] of Object.entries({ ...CORE, ...CYR_ONLY })) {
    out[cyr] = lat;
    out[cyr.toUpperCase()] = titlecaseMulti(lat);
  }
  return out;
})();

// Latin->Cyrillic: only the core 1:1 letters invert. ý -> й, never an iotated vowel.
export const LAT_TO_CYR = (() => {
  const out = {};
  for (const [cyr, lat] of Object.entries(CORE)) {
    out[lat] = cyr;
    out[lat.toUpperCase()] = cyr.toUpperCase();
  }
  return out;
})();

export const LAT_MAX_KEY = Math.max(1, ...Object.keys(LAT_TO_CYR).map((k) => k.length));

// The 30 letters of the modern Turkmen Latin alphabet, official order.
export const LATIN_ALPHABET = [
  "A", "B", "Ç", "D", "E", "Ä", "F", "G", "H", "I",
  "J", "Ž", "K", "L", "M", "N", "Ň", "O", "Ö", "P",
  "R", "S", "Ş", "T", "U", "Ü", "W", "Y", "Ý", "Z",
];
