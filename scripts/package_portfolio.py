"""Create a deterministic-content sharing archive without raw data or local caches.

Notebook outputs are omitted in the archive to avoid exporting local execution paths.
The source notebooks remain unchanged. This command does not publish to GitHub.
"""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_DIRS = {'notebooks', 'sql', 'powerbi', 'images', 'reports', 'scripts', 'docs'}
ROOT_FILES = {'README.md', '.gitignore', '.gitattributes', 'requirements.txt', 'requirements-core.txt'}
EXCLUDED_DATA = {'sales_clean.csv', 'sales_sql_import.csv'}


def files_to_share():
    for file in sorted(ROOT.rglob('*')):
        if not file.is_file():
            continue
        rel = file.relative_to(ROOT)
        if any(x in {'.venv', '.git', 'tmp', 'dist', '__pycache__', '.ipynb_checkpoints'} for x in rel.parts):
            continue
        if file.name.startswith('~$') or file.suffix in {'.tmp', '.bak', '.pyc'}:
            continue
        allowed = (len(rel.parts) == 1 and rel.name in ROOT_FILES) or rel.parts[0] in ALLOWED_DIRS
        allowed |= rel.as_posix() == 'data/raw/README.md'
        allowed |= len(rel.parts) == 3 and rel.parts[:2] == ('data', 'processed') and rel.name not in EXCLUDED_DATA and file.suffix == '.csv'
        if allowed:
            if file.stat().st_size > 25_000_000:
                raise ValueError(f'Unexpectedly large publishing artifact: {rel}')
            yield file, rel


def main():
    output = ROOT / 'dist'
    output.mkdir(exist_ok=True)
    archive = output / 'ecommerce-sales-analysis-portfolio.zip'
    manifest = []
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for file, rel in files_to_share():
            data = file.read_bytes()
            if file.suffix == '.ipynb':
                nb = json.loads(data)
                for cell in nb['cells']:
                    if cell['cell_type'] == 'code':
                        cell['outputs'] = []
                        cell['execution_count'] = None
                data = (json.dumps(nb, ensure_ascii=False, indent=1)+'\n').encode('utf-8')
            z.writestr('ecommerce-sales-analysis/' + rel.as_posix(), data)
            manifest.append({'path': rel.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    (output / 'portfolio_manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == len(manifest)
    print(f'{archive}: {len(manifest)} files, {archive.stat().st_size:,} bytes')


if __name__ == '__main__':
    main()
