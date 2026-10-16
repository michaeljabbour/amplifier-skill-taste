#!/usr/bin/env python3
"""Build a portable static site and skill bundle using only Python's standard library."""
import argparse
import html
import json
import re
import shutil
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]


def escape(value):
    return html.escape(str(value), quote=True)


def build(output):
    site = ROOT / 'site'
    config = json.loads((site / 'site.json').read_text(encoding='utf-8'))
    skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
    calibration = (ROOT / 'references/calibration.md').read_text(encoding='utf-8')
    # The site presents the canonical anchors and questions, not a second rubric.
    taste_block, elegance_block = calibration.split('Taste:\n', 1)[1].split('Elegance:\n', 1)
    taste = re.findall(r'^- [1-5]: (.+)$', taste_block, re.M)
    elegance = re.findall(r'^- [1-5]: (.+)$', elegance_block, re.M)
    questions = re.findall(r'^\d\. (.+)$', calibration, re.M)
    if len(taste) != 5 or len(elegance) != 5 or len(questions) != 8:
        raise ValueError('Expected five canonical anchors per axis and eight questions')
    if not config['examples']:
        raise ValueError('At least one illustrative example is required')
    for example in config['examples']:
        for key in ('before', 'after'):
            if len(example[key]) != 2 or any(type(n) is not int or not 1 <= n <= 5 for n in example[key]):
                raise ValueError('Illustrative coordinates must use two whole anchors from 1 to 5')
        if example['before'] == example['after']:
            raise ValueError('A movement example needs different positions')
    first = config['examples'][0]
    replacements = {
        'NAME': escape(config['name']),
        'DESCRIPTION': escape(config['description']),
        'DETAIL_URL': escape(config['skill_detail_url']),
        'EXAMPLE_OPTIONS': ''.join(f'<option value="{escape(item["id"])}">{escape(item["label"])}</option>' for item in config['examples']),
        'EXAMPLE_BRIEF': escape(first['brief']),
        'EXAMPLE_DIRECTION': escape(first['direction']),
        'EXAMPLE_TITLE': escape(first['proposal']),
        'EXAMPLE_DETAIL': escape(first['proposal_detail']),
        'ANCHORS': ''.join(f'<li><p><span class="mobile-axis-label">Taste</span>{escape(t)}</p><p><span class="mobile-axis-label">Elegance</span>{escape(e)}</p></li>' for t, e in zip(taste, elegance)),
        'QUESTIONS': ''.join(f'<li>{escape(question)}</li>' for question in questions),
        'SKILL_SOURCE': escape(skill),
    }
    for key in ('bottleneck', 'risk', 'verification', 'growth'):
        replacements['EXAMPLE_' + key.upper()] = escape(first[key])
    page = (site / 'template.html').read_text(encoding='utf-8')
    for key, value in replacements.items():
        page = page.replace('@@' + key + '@@', value)
    if re.search(r'@@[A-Z_]+@@', page):
        raise ValueError('Unresolved template placeholder')
    output.mkdir(parents=True, exist_ok=True)
    assets = output / 'assets'
    assets.mkdir(exist_ok=True)
    (output / 'index.html').write_text(page, encoding='utf-8')
    shutil.copy2(site / 'theme/style.css', assets / 'family.css')
    shutil.copy2(site / 'style.css', assets / 'style.css')
    shutil.copy2(site / 'site.js', assets / 'site.js')
    shutil.copy2(site / 'theme/LICENSE', assets / 'family-LICENSE.txt')
    for asset in sorted((site / 'assets').iterdir()):
        if asset.is_file():
            shutil.copy2(asset, assets / asset.name)
    (assets / 'examples.json').write_text(json.dumps(config['examples'], ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    documentation = ['SKILL.md', 'references/calibration.md', 'README.md', 'LICENSE', 'site/README.md', 'site/theme/LICENSE']
    documentation.extend(str(path.relative_to(ROOT)) for path in sorted((ROOT / 'docs').glob('*.md')))
    documentation.extend(str(path.relative_to(ROOT)) for path in sorted((ROOT / 'docs/screenshots').glob('*.jpg')))
    for name in documentation:
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, target)
    (output / '.nojekyll').touch()
    # Fixed archive metadata makes download contents reproducible across builds.
    with ZipFile(output / 'improve-taste-and-elegance.zip', 'w', ZIP_DEFLATED) as bundle:
        for name in ('SKILL.md', 'references/calibration.md'):
            info = ZipInfo('improve-taste-and-elegance/' + name, (2026, 10, 16, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            bundle.writestr(info, (ROOT / name).read_bytes())
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / '_site', help='Static output directory (default: _site)')
    args = parser.parse_args()
    print(f'Built {build(args.output.resolve())}')
