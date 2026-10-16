#!/usr/bin/env python3
"""Check built local links, source fidelity, and the skill download without external access."""
import argparse
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.references = []
        self.downloads = []
        self.duplicates = []
        self.textarea = False
        self.skill = ''
        self.h1s = 0
        self.lang = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag == 'h1':
            self.h1s += 1
        if 'id' in attrs:
            identifier = attrs['id']
            if identifier in self.ids:
                self.duplicates.append(identifier)
            self.ids.add(identifier)
        for key in ('href', 'src'):
            if key in attrs:
                self.references.append(attrs[key])
        if 'download' in attrs:
            self.downloads.append(attrs.get('href', ''))
        if tag == 'textarea' and attrs.get('id') == 'skill-text':
            self.textarea = True

    def handle_endtag(self, tag):
        if tag == 'textarea':
            self.textarea = False

    def handle_data(self, data):
        if self.textarea:
            self.skill += data


def check(output):
    page = Page()
    raw = (output / 'index.html').read_text(encoding='utf-8')
    page.feed(raw)
    assert not page.duplicates, f'Duplicate IDs: {page.duplicates}'
    assert page.h1s == 1 and page.lang == 'en', 'Expected one page title and an English document language'
    assert not re.search(r'@@[A-Z_]+@@', raw), 'Unresolved placeholders'
    local_count = 0
    for reference in page.references:
        parsed = urlsplit(reference)
        if parsed.scheme or parsed.netloc:
            assert parsed.scheme == 'https', f'Unexpected external protocol: {reference}'
            continue
        assert not parsed.path.startswith('/'), f'Root-relative link would break repository hosting: {reference}'
        target = (output / unquote(parsed.path)).resolve() if parsed.path else output / 'index.html'
        assert target.is_relative_to(output.resolve()), f'Link escapes output: {reference}'
        assert target.exists(), f'Missing link or asset: {reference}'
        if parsed.fragment:
            assert target.name == 'index.html' and parsed.fragment in page.ids, f'Missing anchor: {reference}'
        local_count += 1
    markdown_count = 0
    for document in output.rglob('*.md'):
        for reference in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', document.read_text(encoding='utf-8')):
            parsed = urlsplit(reference)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (document.parent / unquote(parsed.path)).resolve()
            assert target.is_relative_to(output.resolve()), f'Markdown link escapes output: {document.name}: {reference}'
            assert target.exists(), f'Missing Markdown link: {document.relative_to(output)}: {reference}'
            markdown_count += 1
    skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
    assert page.skill == skill, 'Copy source differs from canonical SKILL.md'
    for name in ('SKILL.md', 'references/calibration.md'):
        assert (ROOT / name).read_bytes() == (output / name).read_bytes(), f'Download changed source: {name}'
    with ZipFile(output / 'improve-taste-and-elegance.zip') as bundle:
        assert bundle.namelist() == ['improve-taste-and-elegance/SKILL.md', 'improve-taste-and-elegance/references/calibration.md']
        assert bundle.testzip() is None
        for name in ('SKILL.md', 'references/calibration.md'):
            assert bundle.read('improve-taste-and-elegance/' + name) == (ROOT / name).read_bytes(), f'Bundle changed source: {name}'
    assert len(page.downloads) == 2, 'Expected skill and bundle download links'
    examples = json.loads((output / 'assets/examples.json').read_text(encoding='utf-8'))
    assert len(examples) == 3 and len({e['id'] for e in examples}) == 3
    assert all(e['before'] != e['after'] for e in examples)
    # Locally hosted assets are the only runtime dependencies.
    for name in ('assets/style.css', 'assets/family.css'):
        css = (output / name).read_text(encoding='utf-8')
        assert not re.search(r'@import|url\(\s*[\'"]?https?:', css), f'External CSS dependency: {name}'
    assert 'default-src \'self\'' in raw and 'object-src \'none\'' in raw
    digest = hashlib.sha256((output / 'improve-taste-and-elegance.zip').read_bytes()).hexdigest()
    print(f'PASS: {local_count} local links/assets and fragments; no missing targets or duplicate IDs')
    print(f'PASS: {markdown_count} local destinations in shipped Markdown documentation')
    print('PASS: source textarea, both Markdown downloads, and ZIP match canonical files byte-for-byte')
    print('PASS: three distinct illustrative examples, local assets, static CSP, repository-subpath-safe links')
    print(f'Bundle SHA-256: {digest}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / '_site')
    args = parser.parse_args()
    check(args.output.resolve())
