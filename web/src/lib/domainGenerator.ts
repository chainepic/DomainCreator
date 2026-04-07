import data from './data.json';

export type GenerationMode = 'brute' | 'words' | 'pattern' | 'hacks';

export interface GeneratorConfig {
  mode: GenerationMode;
  minLen: number;
  maxLen: number;
  charset: string;
  excludeChars: string;
  customWords: string;
  patternStr: string;
  tlds: string[];
}

export const CATEGORIZED_TLDS = data.CATEGORIZED_TLDS as Record<string, string[]>;

export const ALL_TLDS = Array.from(
  new Set(Object.values(CATEGORIZED_TLDS).flat())
).sort();

// Helper to generate cartesian product
function* cartesianProduct<T>(...arrays: T[][]): Generator<T[]> {
  if (arrays.length === 0) {
    yield [];
    return;
  }
  const [first, ...rest] = arrays;
  for (const item of first) {
    for (const restItems of cartesianProduct(...rest)) {
      yield [item, ...restItems];
    }
  }
}

export function generateBrutePrefixes(
  minLen: number,
  maxLen: number,
  charset: string,
  excludeChars: string = ''
): string[] {
  const validChars = charset.split('').filter((c) => !excludeChars.includes(c));
  const prefixes: string[] = [];

  if (validChars.length === 0) return prefixes;

  for (let len = minLen; len <= maxLen; len++) {
    const arrays = Array(len).fill(validChars);
    for (const combo of cartesianProduct(...arrays)) {
      prefixes.push(combo.join(''));
    }
  }

  return prefixes;
}

export function generatePatternPrefixes(patternStr: string): string[] {
  const mapping: Record<string, string> = {
    C: 'bcdfghjklmnpqrstvwxyz',
    V: 'aeiou',
    L: 'abcdefghijklmnopqrstuvwxyz',
    N: '0123456789',
  };

  const pools: string[][] = [];
  for (const char of patternStr.toUpperCase()) {
    if (mapping[char]) {
      pools.push(mapping[char].split(''));
    } else {
      pools.push([char]);
    }
  }

  const prefixes: string[] = [];
  for (const combo of cartesianProduct(...pools)) {
    prefixes.push(combo.join(''));
  }

  return prefixes;
}

export function generateWordsPrefixes(
  minLen: number,
  maxLen: number,
  customWords: string = ''
): string[] {
  const prefixes = new Set<string>();

  if (minLen <= 2 && 2 <= maxLen) data.WORDS_2.forEach((w) => prefixes.add(w));
  if (minLen <= 3 && 3 <= maxLen) data.WORDS_3.forEach((w) => prefixes.add(w));
  if (minLen <= 4 && 4 <= maxLen) data.WORDS_4.forEach((w) => prefixes.add(w));
  if (minLen <= 5 && 5 <= maxLen) data.WORDS_5.forEach((w) => prefixes.add(w));
  if (minLen <= 6 && 6 <= maxLen) data.WORDS_6.forEach((w) => prefixes.add(w));

  if (customWords) {
    const cwList = customWords
      .split(',')
      .map((w) => w.trim().toLowerCase())
      .filter(Boolean);
    cwList.forEach((w) => prefixes.add(w));
  }

  return Array.from(prefixes);
}

export function generateDomains(prefixes: string[], tlds: string[]): string[] {
  const domains: string[] = [];
  for (const tld of tlds) {
    for (const prefix of prefixes) {
      domains.push(`${prefix}.${tld}`);
    }
  }
  return domains;
}

export function generateHacks(customWords: string, tlds: string[]): string[] {
  const words = new Set<string>();
  data.WORDS_2.forEach((w) => words.add(w));
  data.WORDS_3.forEach((w) => words.add(w));
  data.WORDS_4.forEach((w) => words.add(w));
  data.WORDS_5.forEach((w) => words.add(w));
  data.WORDS_6.forEach((w) => words.add(w));

  if (customWords) {
    const cwList = customWords
      .split(',')
      .map((w) => w.trim().toLowerCase())
      .filter(Boolean);
    cwList.forEach((w) => words.add(w));
  }

  const domains: string[] = [];
  const wordsArray = Array.from(words);

  for (const word of wordsArray) {
    for (const tld of tlds) {
      if (word.endsWith(tld) && word.length > tld.length) {
        const prefix = word.slice(0, -tld.length);
        domains.push(`${prefix}.${tld}`);
      }
    }
  }

  return domains;
}

export function generate(config: GeneratorConfig): string[] {
  if (config.tlds.length === 0) return [];

  let prefixes: string[] = [];

  if (config.mode === 'brute') {
    prefixes = generateBrutePrefixes(
      config.minLen,
      config.maxLen,
      config.charset,
      config.excludeChars
    );
  } else if (config.mode === 'words') {
    prefixes = generateWordsPrefixes(
      config.minLen,
      config.maxLen,
      config.customWords
    );
  } else if (config.mode === 'pattern') {
    prefixes = generatePatternPrefixes(config.patternStr);
  } else if (config.mode === 'hacks') {
    return generateHacks(config.customWords, config.tlds);
  }

  return generateDomains(prefixes, config.tlds);
}
