from pathlib import Path
from pypdf import PdfWriter, PdfReader
import app


def make_pdf(path: Path, pages: int):
    w = PdfWriter()
    for _ in range(pages):
        w.add_blank_page(width=72, height=72)
    with open(path, 'wb') as f:
        w.write(f)


def test_split_merge_extract_rotate_reorder_alternate_compose(tmp_path):
    a = tmp_path / 'a.pdf'
    b = tmp_path / 'b.pdf'
    make_pdf(a, 2)
    make_pdf(b, 3)

    split_dir = tmp_path / 'split'
    outs = app.split_pdf(a, split_dir)
    assert len(outs) == 2

    merged = tmp_path / 'merged.pdf'
    app.merge_pdfs([str(a), str(b)], str(merged))
    assert len(PdfReader(str(merged)).pages) == 5

    extracted = tmp_path / 'extracted.pdf'
    app.extract_pages(str(b), '1,3', str(extracted))
    assert len(PdfReader(str(extracted)).pages) == 2

    rotated = tmp_path / 'rotated.pdf'
    app.rotate_pages(str(b), str(rotated), '2', 90)
    assert len(PdfReader(str(rotated)).pages) == 3

    reordered = tmp_path / 'reordered.pdf'
    app.reorder_pages(str(b), str(reordered), '3,1,2')
    assert len(PdfReader(str(reordered)).pages) == 3

    alt = tmp_path / 'alt.pdf'
    app.alternate_pdfs([str(a), str(b)], str(alt))
    assert len(PdfReader(str(alt)).pages) == 5

    comp = tmp_path / 'comp.pdf'
    app.compose_pdfs([str(a), str(b)], str(comp), '1')
    assert len(PdfReader(str(comp)).pages) == 2
