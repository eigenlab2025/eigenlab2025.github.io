#!/usr/bin/env python3
"""Create self-hosted Noto CJK subsets for the text currently used by the site.

Requires fonttools[woff] and Noto Sans CJK Regular/Bold TTC files. Supply their
directory as the first argument if it differs from the Linux default below.
"""
from pathlib import Path
import sys
from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent
FONT_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/usr/share/fonts/opentype/noto')
text = ''.join(p.read_text() for p in (ROOT / 'content').glob('*.json'))
text += (ROOT / 'build.py').read_text()
text += ''.join(chr(i) for i in range(32, 256)) + '↶→↓↗†λ–—−…'
for language, index in [('jp', 0), ('sc', 2)]:
    for weight, label in [(400, 'Regular'), (700, 'Bold')]:
        font = TTFont(FONT_DIR / f'NotoSansCJK-{label}.ttc', fontNumber=index)
        options = subset.Options()
        options.flavor = 'woff2'
        options.layout_features = ['*']
        sub = subset.Subsetter(options=options)
        sub.populate(text=text)
        sub.subset(font)
        font.flavor = 'woff2'
        path = ROOT / 'docs/assets' / f'noto-{language}-{weight}.woff2'
        font.save(path)
        print(path.name, path.stat().st_size)
