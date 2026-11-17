# Eigen Lab — Shen Laboratory

Multilingual laboratory website of Xun Shen at Tokyo University of Agriculture and Technology.

- Japanese: https://eigenlab2025.github.io/ja/index.html
- English: https://eigenlab2025.github.io/en/index.html
- Chinese: https://eigenlab2025.github.io/zh/index.html

## Editing

Edit the JSON files in `content/`: `copy.json` for translated page text, `news.json` for dated multilingual announcements, `members.json` for the roster, `publications.json` for the bibliography, and `projects.json` for research projects. Keep publication IDs stable. Student-author markers must match the listed authors exactly.

Run `python3 build.py --production` after editing. Commit the changed source and generated `docs/` files. GitHub Pages serves the `main` branch's `/docs` directory. Templates live in `build.py`; CSS and images live in `docs/assets/`. The site is static, with no database, analytics, external font service, or npm build.

The 27 pages cover Home, News, Research, Projects, People, Publications, Lab life, Join us, and Contact in Japanese, English, and simplified Chinese. Publication filters and language navigation run locally in the browser.

## Fonts and images

Bundled Noto Sans CJK subsets work offline; their license is in `docs/assets/NOTO-LICENSE.txt`. If new characters are added, install `fonttools[woff]` and Noto Sans CJK Regular/Bold TTC fonts, then run `python3 build_fonts.py /path/to/fonts` before rebuilding. Ordinary builds need only Python 3.

Member photographs and the principal investigator's portrait were supplied by the laboratory. Concept illustrations depict research aims and settings, not experimental evidence. Rights to photographs and supplied materials remain with their respective owners.

## Research records

The bibliography includes journal articles, conference papers, talks, theses, and a published patent application. Each record links to its publisher, proceedings, DOI, or investigator record when available. Co-supervised students at Institute of Science Tokyo are identified separately from TUAT students.

## News and member updates

Add announcements to `content/news.json` in newest-first order, with stable IDs and Japanese, English, and Chinese translations. Home shows the latest three entries; News lists the complete archive. Use source links for external announcements. For members awaiting photos, set `image` to `null`; a localized neutral placeholder is rendered automatically.
