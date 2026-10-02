import json
import subprocess
import sys
from pathlib import Path

ROOT = Path('/workspace')
SCRIPT = ROOT / 'pdf_tool.py'


def make_doc(path: Path, pages: int):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({'magic': 'PDFTOOL1', 'pages': [{'rotation': 0, 'content': f'p{i+1}'} for i in range(pages)]}, f)


def read_doc(path: Path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_workflow(tmp_path: Path):
    a = tmp_path / 'a.pdf'
    b = tmp_path / 'b.pdf'
    make_doc(a, 3)
    make_doc(b, 2)

    outdir = tmp_path / 'split'
    subprocess.check_call([sys.executable, str(SCRIPT), 'split', str(a), str(outdir)])
    assert len(list(outdir.glob('*.pdf'))) == 3

    extracted = tmp_path / 'extracted.pdf'
    subprocess.check_call([sys.executable, str(SCRIPT), 'extract', str(a), '1,3', str(extracted)])
    assert len(read_doc(extracted)['pages']) == 2

    rotated = tmp_path / 'rotated.pdf'
    subprocess.check_call([sys.executable, str(SCRIPT), 'rotate', str(a), '90', str(rotated), '--pages', '2'])
    assert read_doc(rotated)['pages'][1]['rotation'] == 90

    merged = tmp_path / 'merged.pdf'
    subprocess.check_call([sys.executable, str(SCRIPT), 'merge', str(merged), f'{a}:1-2', str(b)])
    assert len(read_doc(merged)['pages']) == 4

    reordered = tmp_path / 'reordered.pdf'
    subprocess.check_call([sys.executable, str(SCRIPT), 'reorder', str(a), '3,1,2', str(reordered)])
    assert [p['content'] for p in read_doc(reordered)['pages']] == ['p3', 'p1', 'p2']

    alternating = tmp_path / 'alt.pdf'
    subprocess.check_call([sys.executable, str(SCRIPT), 'alternate', str(alternating), str(a), str(b)])
    assert len(read_doc(alternating)['pages']) == 5

    setup = tmp_path / 'setup.json'
    subprocess.check_call([sys.executable, str(SCRIPT), 'save-setup', str(setup), '--operation', 'extract={"pages":"1,2"}', '--operation', 'rotate={"degrees":180,"pages":"1"}'])
    run_out = tmp_path / 'run.pdf'
    subprocess.check_call([sys.executable, str(SCRIPT), 'run-setup', str(setup), str(a), str(run_out)])
    assert len(read_doc(run_out)['pages']) == 2
    assert read_doc(run_out)['pages'][0]['rotation'] == 180
