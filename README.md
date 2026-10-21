# Esteban Triviño — Portfolio / CV

Interactive, bilingual (EN / ES) portfolio built as a single self-contained `index.html`, inspired by Apple's Human Interface Guidelines.

**Live:** https://estebantrivino.com/ (English) · https://estebantrivino.com/es/ (Español)

- Dynamic Island header with availability status, email and EN | ES switcher
- Interactive iPhone simulator: digital wallet transfer, live theme switcher, animated Swift/TCA code
- AI-augmented engineering metrics (Claude Code + GitHub Copilot CLI)
- Interactive career timeline with tech filters
- "Download CV" downloads the PDF résumé (`Esteban-Trivino-CV-iOS-Developer.pdf`)

## Editing

1. Edit content in the `I18N` and `EXPERIENCE` objects inside `index.html` (the only source file).
2. Regenerate the Spanish page: `python3 scripts/build-es.py` → writes `es/index.html` (never edit it by hand).
3. Optional — regenerate favicons and link-preview images: `python3 scripts/gen-assets.py` (needs `playwright` + `pillow`).

## SEO & sharing

- Open Graph / Twitter cards with 1200×630 previews (`og-image.png`, `og-image-es.png`) for WhatsApp, LinkedIn, Slack, X.
- JSON-LD `Person` / `WebSite` / `ProfilePage`, canonical + `hreflang` (en / es), `robots.txt`, `sitemap.xml`.
- Favicons: `favicon.ico`, `favicon.svg`, `apple-touch-icon.png`, `site.webmanifest`.
