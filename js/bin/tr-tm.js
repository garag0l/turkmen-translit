#!/usr/bin/env node
// CLI for @garag0l/turkmen-translit. Mirrors the Python tr-tm command.

import { cyrillicToLatin, latinToCyrillic, detectScript } from "../src/index.js";

const USAGE = `tr-tm — Turkmen Cyrillic <-> Latin transliteration

Usage:
  tr-tm "Түркменистан"            auto-detect, convert to the other script
  tr-tm --to-latin "Ашгабат"      force Cyrillic -> Latin
  tr-tm --to-cyrillic "Aşgabat"   force Latin -> Cyrillic (best effort)
  tr-tm --detect "salam"          print the detected script and exit
  echo "salam" | tr-tm            read stdin
  tr-tm --help | --version
`;

function convert(text, direction) {
  if (direction === "to-latin") return cyrillicToLatin(text);
  if (direction === "to-cyrillic") return latinToCyrillic(text);
  const script = detectScript(text);
  if (script === "cyrillic") return cyrillicToLatin(text);
  if (script === "latin") return latinToCyrillic(text);
  return cyrillicToLatin(text); // mixed/unknown: normalise toward Latin
}

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  return Buffer.concat(chunks).toString("utf8");
}

async function main(argv) {
  let direction = "auto";
  let detect = false;
  const words = [];
  for (const arg of argv) {
    if (arg === "--to-latin") direction = "to-latin";
    else if (arg === "--to-cyrillic") direction = "to-cyrillic";
    else if (arg === "--detect") detect = true;
    else if (arg === "--help" || arg === "-h") {
      process.stdout.write(USAGE);
      return 0;
    } else if (arg === "--version" || arg === "-V") {
      const { readFileSync } = await import("node:fs");
      const { fileURLToPath } = await import("node:url");
      const pkg = JSON.parse(
        readFileSync(new URL("../package.json", import.meta.url), "utf8"),
      );
      void fileURLToPath; // (kept for clarity; URL form is used above)
      process.stdout.write(`turkmen-translit ${pkg.version}\n`);
      return 0;
    } else words.push(arg);
  }

  const text = words.length ? words.join(" ") : await readStdin();
  const result = detect ? detectScript(text) + "\n" : convert(text, direction);
  process.stdout.write(result);
  return 0;
}

main(process.argv.slice(2)).then((code) => process.exit(code));
