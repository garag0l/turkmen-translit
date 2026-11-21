export type Script = "cyrillic" | "latin" | "mixed" | "unknown";

/** Transliterate Turkmen Cyrillic text to the modern Latin alphabet. */
export function cyrillicToLatin(text: string): string;

/**
 * Transliterate modern Turkmen Latin text to legacy Cyrillic (best effort).
 * The 30 core letters invert exactly; ý inverts to й, not an iotated vowel.
 */
export function latinToCyrillic(text: string): string;

/** Classify text as "cyrillic", "latin", "mixed", or "unknown". */
export function detectScript(text: string): Script;

/** The 30 letters of the modern Turkmen Latin alphabet, in official order. */
export const LATIN_ALPHABET: readonly string[];
