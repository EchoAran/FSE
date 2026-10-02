from pathlib import Path
from pypdf import PdfWriter, PdfReader
import pdf_tool


def make_pdf(path: Path, n: int):
    w = PdfWriter()
    for _ in range(n):
        w.add_blank_page(width=72, height=72)
    with path.open('wb') as f:
        w.write(f)


def count_pages(path: Path):
    return len(PdfReader(str(path)).pages)


def test_split_extract_merge_rotate_reorder_interleave(tmp_path):
    a = tmp_path / 'a.pdf'
    b = tmp_path / 'b.pdf'
    make_pdf(a, 3)
    make_pdf(b, 2)

    pdf_tool.main(['split', str(a), str(tmp_path / 'split')])
    assert len(list((tmp_path / 'split').glob('*.pdf'))) == 3

    extracted = tmp_path / 'extracted.pdf'
    pdf_tool.main(['extract', str(a), '1-2', str(extracted)])
    assert count_pages(extracted) == 2

    rotated = tmp_path / 'rotated.pdf'
    pdf_tool.main(['rotate', str(a), '90', str(rotated), '--pages', '2'])
    assert count_pages(rotated) == 3

    merged = tmp_path / 'merged.pdf'
    pdf_tool.main(['merge', str(merged), str(a), str(b)])
    assert count_pages(merged) == 5

    reordered = tmp_path / 'reordered.pdf'
    pdf_tool.main(['reorder', str(a), '3,1,2', str(reordered)])
    assert count_pages(reordered) == 3

    interleaved = tmp_path / 'interleaved.pdf'
    pdf_tool.main(['interleave', str(interleaved), str(a), str(b)])
    assert count_pages(interleaved) == 5

    assert count_pages(a) == 3
    assert count_pages(b) == 2
