import os
from pathlib import Path
from pypdf import PdfWriter, PdfReader
import subprocess
import sys


def make_pdf(path, pages=3):
    w = PdfWriter()
    for _ in range(pages):
        w.add_blank_page(width=72, height=72)
    with open(path, 'wb') as f:
        w.write(f)


def run(*args):
    return subprocess.run([sys.executable, 'pdf_tool.py', *args], cwd='/workspace', capture_output=True, text=True)


def test_split_and_merge(tmp_path):
    src = tmp_path / 'src.pdf'
    make_pdf(src, 3)
    outdir = tmp_path / 'split'
    r = run('split', str(src), str(outdir))
    assert r.returncode == 0, r.stderr
    assert len(list(outdir.glob('*.pdf'))) == 3
    merged = tmp_path / 'merged.pdf'
    r = run('merge', str(merged), str(outdir/'page_1.pdf'), str(outdir/'page_2.pdf'))
    assert r.returncode == 0, r.stderr
    assert len(PdfReader(str(merged)).pages) == 2


def test_extract_reorder_rotate(tmp_path):
    src = tmp_path / 'src.pdf'
    make_pdf(src, 4)
    out = tmp_path / 'extract.pdf'
    assert run('extract', str(src), '2-3', str(out)).returncode == 0
    assert len(PdfReader(str(out)).pages) == 2
    reordered = tmp_path / 'reorder.pdf'
    assert run('reorder', str(src), '4,3,2,1', str(reordered)).returncode == 0
    assert len(PdfReader(str(reordered)).pages) == 4
    rotated = tmp_path / 'rotated.pdf'
    assert run('rotate', str(src), '1,3', '90', str(rotated)).returncode == 0
    assert len(PdfReader(str(rotated)).pages) == 4


def test_interleave_and_workspace(tmp_path):
    a = tmp_path / 'a.pdf'
    b = tmp_path / 'b.pdf'
    make_pdf(a, 2)
    make_pdf(b, 3)
    out = tmp_path / 'interleave.pdf'
    assert run('interleave', str(out), str(a), str(b)).returncode == 0
    assert len(PdfReader(str(out)).pages) == 5
    ws = tmp_path / 'ws.json'
    assert run('workspace-save', str(ws), 'out.pdf', str(a), str(b)).returncode == 0
    assert ws.exists()
    assert 'inputs' in ws.read_text()
