"use client";

import { useState, useEffect } from "react";
import { Search, Settings, Download, Star, StarOff, Copy, Check } from "lucide-react";
import {
  CATEGORIZED_TLDS,
  ALL_TLDS,
  generate,
  GenerationMode,
  GeneratorConfig,
} from "@/lib/domainGenerator";

export default function Home() {
  const [mode, setMode] = useState<GenerationMode>("brute");
  const [minLen, setMinLen] = useState(1);
  const [maxLen, setMaxLen] = useState(2);
  const [charset, setCharset] = useState("abcdefghijklmnopqrstuvwxyz0123456789");
  const [excludeChars, setExcludeChars] = useState("");
  const [customWords, setCustomWords] = useState("");
  const [patternStr, setPatternStr] = useState("CVC");
  const [selectedTlds, setSelectedTlds] = useState<Set<string>>(new Set(["com", "net", "org"]));
  const [results, setResults] = useState<string[]>([]);
  const [favorites, setFavorites] = useState<Set<string>>(new Set());
  const [copied, setCopied] = useState<string | null>(null);

  useEffect(() => {
    const saved = localStorage.getItem("domainCreatorFavorites");
    if (saved) {
      try {
        setFavorites(new Set(JSON.parse(saved)));
      } catch (e) {}
    }
  }, []);

  const saveFavorites = (newFavs: Set<string>) => {
    setFavorites(newFavs);
    localStorage.setItem("domainCreatorFavorites", JSON.stringify(Array.from(newFavs)));
  };

  const toggleFavorite = (domain: string) => {
    const newFavs = new Set(favorites);
    if (newFavs.has(domain)) {
      newFavs.delete(domain);
    } else {
      newFavs.add(domain);
    }
    saveFavorites(newFavs);
  };

  const handleGenerate = () => {
    const config: GeneratorConfig = {
      mode,
      minLen,
      maxLen,
      charset,
      excludeChars,
      customWords,
      patternStr,
      tlds: Array.from(selectedTlds),
    };
    const generated = generate(config);
    setResults(generated);
  };

  const handleCopy = (domain: string) => {
    navigator.clipboard.writeText(domain);
    setCopied(domain);
    setTimeout(() => setCopied(null), 2000);
  };

  const handleExport = () => {
    const content = results.join("\n");
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "domains.txt";
    a.click();
    URL.revokeObjectURL(url);
  };

  const toggleTld = (tld: string) => {
    const newTlds = new Set(selectedTlds);
    if (newTlds.has(tld)) {
      newTlds.delete(tld);
    } else {
      newTlds.add(tld);
    }
    setSelectedTlds(newTlds);
  };

  const selectCategory = (cat: string) => {
    const newTlds = new Set(selectedTlds);
    CATEGORIZED_TLDS[cat].forEach((tld) => newTlds.add(tld));
    setSelectedTlds(newTlds);
  };

  const selectByLength = (len: number, exact: boolean = true) => {
    const newTlds = new Set(selectedTlds);
    ALL_TLDS.forEach((tld) => {
      if (exact && tld.length === len) newTlds.add(tld);
      if (!exact && tld.length >= len) newTlds.add(tld);
    });
    setSelectedTlds(newTlds);
  };

  const clearTlds = () => setSelectedTlds(new Set());

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <div className="w-80 bg-panel-dark border-r border-border-standard flex flex-col overflow-y-auto">
        <div className="p-6 border-b border-border-subtle">
          <h1 className="text-h3 text-primary-white flex items-center gap-2">
            <Settings className="w-5 h-5 text-brand-indigo" />
            DomainCreator
          </h1>
        </div>

        <div className="p-6 space-y-8">
          {/* Mode Selection */}
          <section className="space-y-4">
            <h2 className="text-caption-lg text-primary-white">Generation Mode</h2>
            <div className="grid grid-cols-2 gap-2">
              {(["brute", "words", "pattern", "hacks"] as GenerationMode[]).map((m) => (
                <button
                  key={m}
                  onClick={() => setMode(m)}
                  className={`px-3 py-2 rounded-comfortable text-small-medium transition-colors ${
                    mode === m
                      ? "bg-brand-indigo text-white"
                      : "bg-ghost-bg text-secondary-gray border border-border-standard hover:bg-subtle-bg"
                  }`}
                >
                  {m.charAt(0).toUpperCase() + m.slice(1)}
                </button>
              ))}
            </div>
          </section>

          {/* Mode Specific Options */}
          <section className="space-y-4">
            {mode === "brute" && (
              <div className="space-y-4">
                <div className="flex gap-4">
                  <div className="flex-1">
                    <label className="block text-label text-tertiary-gray mb-1">Min Length</label>
                    <input
                      type="number"
                      value={minLen}
                      onChange={(e) => setMinLen(Number(e.target.value))}
                      className="input-standard w-full"
                    />
                  </div>
                  <div className="flex-1">
                    <label className="block text-label text-tertiary-gray mb-1">Max Length</label>
                    <input
                      type="number"
                      value={maxLen}
                      onChange={(e) => setMaxLen(Number(e.target.value))}
                      className="input-standard w-full"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-label text-tertiary-gray mb-1">Charset</label>
                  <input
                    type="text"
                    value={charset}
                    onChange={(e) => setCharset(e.target.value)}
                    className="input-standard w-full"
                  />
                </div>
                <div>
                  <label className="block text-label text-tertiary-gray mb-1">Exclude Chars</label>
                  <input
                    type="text"
                    value={excludeChars}
                    onChange={(e) => setExcludeChars(e.target.value)}
                    placeholder="e.g. 0o1l"
                    className="input-standard w-full"
                  />
                </div>
              </div>
            )}

            {mode === "words" && (
              <div className="space-y-4">
                <div className="flex gap-4">
                  <div className="flex-1">
                    <label className="block text-label text-tertiary-gray mb-1">Min Length</label>
                    <input
                      type="number"
                      value={minLen}
                      onChange={(e) => setMinLen(Number(e.target.value))}
                      className="input-standard w-full"
                    />
                  </div>
                  <div className="flex-1">
                    <label className="block text-label text-tertiary-gray mb-1">Max Length</label>
                    <input
                      type="number"
                      value={maxLen}
                      onChange={(e) => setMaxLen(Number(e.target.value))}
                      className="input-standard w-full"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-label text-tertiary-gray mb-1">Custom Words (comma separated)</label>
                  <textarea
                    value={customWords}
                    onChange={(e) => setCustomWords(e.target.value)}
                    className="input-standard w-full h-24 resize-none"
                    placeholder="e.g. watch,spell,super"
                  />
                </div>
              </div>
            )}

            {mode === "pattern" && (
              <div className="space-y-4">
                <div>
                  <label className="block text-label text-tertiary-gray mb-1">Pattern Formula</label>
                  <input
                    type="text"
                    value={patternStr}
                    onChange={(e) => setPatternStr(e.target.value)}
                    placeholder="e.g. CVC, LVN"
                    className="input-standard w-full uppercase"
                  />
                  <p className="text-micro text-quaternary-gray mt-2">
                    C=Consonant, V=Vowel, L=Letter, N=Number
                  </p>
                </div>
              </div>
            )}

            {mode === "hacks" && (
              <div className="space-y-4">
                <div>
                  <label className="block text-label text-tertiary-gray mb-1">Custom Words (optional)</label>
                  <textarea
                    value={customWords}
                    onChange={(e) => setCustomWords(e.target.value)}
                    className="input-standard w-full h-24 resize-none"
                    placeholder="Leave empty for built-in words"
                  />
                  <p className="text-micro text-quaternary-gray mt-2">
                    Matches words with TLDs (e.g. internet + net -{">"} inter.net)
                  </p>
                </div>
              </div>
            )}
          </section>

          {/* TLD Selection */}
          <section className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-caption-lg text-primary-white">TLD Selection</h2>
              <button onClick={clearTlds} className="text-micro text-tertiary-gray hover:text-primary-white">
                Clear All
              </button>
            </div>
            
            <div className="space-y-2">
              <p className="text-label text-tertiary-gray">Quick Select</p>
              <div className="flex flex-wrap gap-2">
                <button onClick={() => selectByLength(2)} className="btn-subtle">2-char</button>
                <button onClick={() => selectByLength(3)} className="btn-subtle">3-char</button>
                <button onClick={() => selectByLength(4, false)} className="btn-subtle">4+ char</button>
              </div>
            </div>

            <div className="space-y-2">
              <p className="text-label text-tertiary-gray">Categories</p>
              <div className="flex flex-wrap gap-2">
                {Object.keys(CATEGORIZED_TLDS).map((cat) => (
                  <button key={cat} onClick={() => selectCategory(cat)} className="btn-subtle">
                    {cat.split(' ')[0]}
                  </button>
                ))}
              </div>
            </div>

            <div className="space-y-2">
              <p className="text-label text-tertiary-gray">Selected ({selectedTlds.size})</p>
              <div className="flex flex-wrap gap-1 max-h-40 overflow-y-auto p-2 bg-ghost-bg border border-border-subtle rounded-comfortable">
                {Array.from(selectedTlds).map((tld) => (
                  <button
                    key={tld}
                    onClick={() => toggleTld(tld)}
                    className="px-2 py-0.5 bg-surface-secondary text-secondary-gray rounded-pill text-micro border border-border-tertiary hover:bg-border-secondary"
                  >
                    .{tld}
                  </button>
                ))}
              </div>
            </div>
          </section>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 bg-marketing-black flex flex-col">
        {/* Header */}
        <header className="h-16 border-b border-border-subtle flex items-center justify-between px-8">
          <div className="flex items-center gap-4">
            <button onClick={handleGenerate} className="btn-primary flex items-center gap-2">
              <Search className="w-4 h-4" />
              Generate Domains
            </button>
            <span className="text-small text-tertiary-gray">
              {results.length} results
            </span>
          </div>
          <div className="flex items-center gap-4">
            <button onClick={handleExport} className="btn-ghost flex items-center gap-2" disabled={results.length === 0}>
              <Download className="w-4 h-4" />
              Export
            </button>
          </div>
        </header>

        {/* Results Grid */}
        <main className="flex-1 overflow-y-auto p-8">
          {results.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-tertiary-gray">
              <Search className="w-12 h-12 mb-4 opacity-20" />
              <p className="text-body-lg">No domains generated yet.</p>
              <p className="text-small mt-2">Adjust your settings and click Generate.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {results.map((domain) => (
                <div key={domain} className="card-panel p-4 flex items-center justify-between group">
                  <span className="text-body-medium text-primary-white font-mono">{domain}</span>
                  <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={() => handleCopy(domain)}
                      className="p-1.5 text-tertiary-gray hover:text-primary-white rounded-comfortable hover:bg-surface-secondary transition-colors"
                      title="Copy"
                    >
                      {copied === domain ? <Check className="w-4 h-4 text-success-emerald" /> : <Copy className="w-4 h-4" />}
                    </button>
                    <button
                      onClick={() => toggleFavorite(domain)}
                      className="p-1.5 text-tertiary-gray hover:text-accent-violet rounded-comfortable hover:bg-surface-secondary transition-colors"
                      title="Favorite"
                    >
                      {favorites.has(domain) ? (
                        <Star className="w-4 h-4 text-accent-violet fill-accent-violet" />
                      ) : (
                        <StarOff className="w-4 h-4" />
                      )}
                    </button>
                    <a
                      href={`https://www.namecheap.com/domains/registration/results/?domain=${domain}`}
                      target="_blank"
                      rel="noreferrer"
                      className="p-1.5 text-tertiary-gray hover:text-primary-white rounded-comfortable hover:bg-surface-secondary transition-colors text-micro font-semibold"
                      title="Check Availability"
                    >
                      Buy
                    </a>
                  </div>
                </div>
              ))}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
