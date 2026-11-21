import assert from "node:assert/strict";
import { test } from "node:test";

import {
  cyrillicToLatin,
  latinToCyrillic,
  detectScript,
  LATIN_ALPHABET,
} from "../src/index.js";
import { CORE, CYR_TO_LAT } from "../src/tables.js";

test("modern Latin alphabet has 30 unique letters", () => {
  assert.equal(LATIN_ALPHABET.length, 30);
  assert.equal(new Set(LATIN_ALPHABET).size, 30);
});

test("the tricky pairs are correct", () => {
  assert.equal(CYR_TO_LAT["ж"], "ž"); // Ж -> ž, NOT j
  assert.equal(CYR_TO_LAT["җ"], "j"); // Җ -> j, NOT ž
  assert.equal(CYR_TO_LAT["й"], "ý"); // Й -> ý
  assert.equal(CYR_TO_LAT["ң"], "ň"); // Ң -> ň
  assert.equal(CYR_TO_LAT["ә"], "ä"); // Ә -> ä
  assert.equal(CYR_TO_LAT["в"], "w"); // В -> w
  assert.equal(CYR_TO_LAT["ы"], "y"); // Ы -> y
});

test("every core letter round-trips, both cases", () => {
  for (const cyr of Object.keys(CORE)) {
    assert.equal(latinToCyrillic(cyrillicToLatin(cyr)), cyr, `lower ${cyr}`);
    const up = cyr.toUpperCase();
    assert.equal(latinToCyrillic(cyrillicToLatin(up)), up, `upper ${up}`);
  }
});

test("known words", () => {
  assert.equal(cyrillicToLatin("Түркменистан"), "Türkmenistan");
  assert.equal(latinToCyrillic("Aşgabat"), "Ашгабат");
  assert.equal(cyrillicToLatin("салам"), "salam");
  assert.equal(latinToCyrillic("Türkmenistan"), "Түркменистан");
});

test("case handling of the glide letters", () => {
  assert.equal(cyrillicToLatin("Я"), "Ýa"); // single capital -> title
  assert.equal(cyrillicToLatin("ЯН"), "ÝAN"); // all-caps run
  assert.equal(cyrillicToLatin("Яз"), "Ýaz"); // title word
  assert.equal(cyrillicToLatin("я"), "ýa"); // lowercase
});

test("passthrough and empty", () => {
  assert.equal(cyrillicToLatin("OK! 123 (test)"), "OK! 123 (test)");
  assert.equal(cyrillicToLatin("салам\nсалам"), "salam\nsalam");
  assert.equal(cyrillicToLatin(""), "");
  assert.equal(latinToCyrillic(""), "");
});

test("documented lossy cases", () => {
  assert.equal(cyrillicToLatin("ъь"), "");
  assert.equal(cyrillicToLatin("ц"), "s");
  assert.equal(latinToCyrillic(cyrillicToLatin("я")), "йа"); // я -> ýa -> йа
});

test("detect", () => {
  assert.equal(detectScript("Түркмен"), "cyrillic");
  assert.equal(detectScript("Turkmen dili"), "latin");
  assert.equal(detectScript("Aşgabat"), "latin");
  assert.equal(detectScript("Aşgabat Ашгабат"), "mixed");
  assert.equal(detectScript("123 !@#"), "unknown");
});
