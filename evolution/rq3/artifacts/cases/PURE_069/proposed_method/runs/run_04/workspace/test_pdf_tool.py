from pathlib import Path
import subprocess
import sys

from pypdf import PdfWriter, PdfReader


def make_pdf(path: Path, num_pages: int):
    w = PdfWriter()
    for _ in range(num_pages):
        w.add_blank_page(width=72, height=72)
    with open(path, 'wb') as f:
        w.write(f)


def run(*args, cwd='/workspace'):
    return subprocess.run([sys.executable, 'pdf_tool.py', *args], cwd=cwd, text=True, capture_output=True)


def test_extract(tmp_path):
    src = tmp_path / 'a.pdf'
    out = tmp_path / 'out.pdf'
    make_pdf(src, 4)
    r = run('extract', str(src), '--pages', '2-3', '-o', str(out))
    assert r.returncode == 0, r.stderr
    assert len(PdfReader(str(out)).pages) == 2


def test_merge(tmp_path):
    a = tmp_path / 'a.pdf'
    b = tmp_path / 'b.pdf'
    out = tmp_path / 'merged.pdf'
    make_pdf(a, 2)
    make_pdf(b, 3)
    r = run('merge', str(a), str(b), '-o', str(out))
    assert r.returncode == 0, r.stderr
    assert len(PdfReader(str(out)).pages) == 5


def test_interleave(tmp_path):
    a = tmp_path / 'a.pdf'
    b = tmp_path / 'b.pdf'
    out = tmp_path / 'interleave.pdf'
    make_pdf(a, 2)
    make_pdf(b, 3)
    r = run('merge', str(a), str(b), '-o', str(out), '--interleave')
    assert r.returncode == 0, r.stderr
    assert len(PdfReader(str(out)).pages) == 5


def test_split(tmp_path):
    src = tmp_path / 'src.pdf'
    outdir = tmp_path / 'splits'
    make_pdf(src, 5)
    r = run('split', str(src), '-o', str(outdir), '--chunk-size', '2')
    assert r.returncode == 0, r.stderr
    outs = sorted(outdir.glob('*.pdf'))
    assert len(outs) == 3
    assert [len(PdfReader(str(p)).pages) for p in outs] == [2, 2, 1]
