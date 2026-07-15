#!/usr/bin/env python3
"""Embed design.html into index.html (and airfoil-lab.html) as base64.
Run this after any edit to design.html, then commit all files."""
import base64, re, sys

with open('design.html', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('ascii')
# wrap for readable diffs
wrapped = '\n'.join(b64[i:i+120] for i in range(0, len(b64), 120))
block = f'<script id="ds-embed" type="text/plain">\n{wrapped}\n</script>'

for target in ['index.html', 'airfoil-lab.html']:
    try:
        src = open(target).read()
    except FileNotFoundError:
        continue
    if 'id="ds-embed"' in src:
        src = re.sub(r'<script id="ds-embed" type="text/plain">.*?</script>', block, src, flags=re.S)
        action = 'updated'
    else:
        # insert just before the first main <script> tag
        idx = src.index('<script>')
        src = src[:idx] + block + '\n' + src[idx:]
        action = 'inserted'
    open(target, 'w').write(src)
    print(f'{action} ds-embed in {target} ({len(b64)} b64 chars)')
