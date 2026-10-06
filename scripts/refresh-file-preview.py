"""Copy a built site to a local-file preview, making generated links portable.

Usage: python3 scripts/refresh-file-preview.py _site /absolute/preview/path
This changes generated output only; deployed routes remain unchanged.
"""
from pathlib import Path
from urllib.parse import urlsplit
import re
import shutil
import sys

source = Path(sys.argv[1]).resolve()
target = Path(sys.argv[2]).resolve()
assert source != target and source.is_dir()
shutil.copytree(source, target, dirs_exist_ok=True)
for page in target.rglob('*.html'):
    def relative(match):
        attr, quote, value = match.groups()
        if not value.startswith('/') or value.startswith('//'):
            return match.group()
        url = urlsplit(value)
        destination = target / url.path.lstrip('/')
        if url.path.endswith('/'):
            destination = destination / 'index.html'
        import os
        path = os.path.relpath(destination, page.parent).replace(os.sep, '/')
        if url.query:
            path += '?' + url.query
        if url.fragment:
            path += '#' + url.fragment
        return attr + '=' + quote + path + quote
    # data-image is used by the enlargement dialog and must match the inline asset.
    text = re.sub(r'\b(href|src|data-image)=(["\'])(.*?)\2', relative, page.read_text())
    page.write_text(text)
print('Refreshed portable preview:', target)
