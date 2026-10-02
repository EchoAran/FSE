from pathlib import Path
import subprocess
import sys
from pypdf import PdfWriter, PdfReader


def make_pdf(path: Path, pages: int):
    w = PdfWriter()
    for _ in range(pages):
        w.add_blank_page(width=72, height=72)
    with path.open('wb') as f:
        w.write(f)


def run(*args):
    return subprocess.run([sys.executable, 'app.py', *args], cwd='/workspace', capture_output=True, text=True)


def test_merge_extract_reorder(tmp_path):
    a = tmp_path / 'a.pdf'
    b = tmp_path / 'b.pdf'
    make_pdf(a, 2)
    make_pdf(b, 1)
    merged = tmp_path / 'merged.pdf'
    assert run('merge', str(a), str(b), '-o', str(merged)).returncode == 0
    assert len(PdfReader(str(merged)).pages) == 3

    extracted = tmp_path / 'extracted.pdf'
    assert run('extract', str(merged), '-o', str(extracted), '--pages', '2,3').returncode == 0
    assert len(PdfReader(str(extracted)).pages) == 2

    reordered = tmp_path / 'reordered.pdf'
    assert run('reorder', str(merged), '-o', str(reordered), '--order', '3,2,1').returncode == 0
    assert len(PdfReader(str(reordered)).pages) == 3


def test_split_and_rotate(tmp_path):
    src = tmp_path / 'src.pdf'
    make_pdf(src, 3)
    outdir = tmp_path / 'out'
    res = run('split', str(src), '-o', str(outdir), '--pages-per-file', '2')
    assert res.returncode == 0
    assert len(list(outdir.glob('*.pdf'))) == 2

    rotated = tmp_path / 'rotated.pdf'
    assert run('rotate', str(src), '-o', str(rotated), '--degrees', '90').returncode == 0
    assert len(PdfReader(str(rotated)).pages) == 3
