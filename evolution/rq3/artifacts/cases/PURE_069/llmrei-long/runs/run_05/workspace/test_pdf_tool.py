from pathlib import Path

from pypdf import PdfReader, PdfWriter

import pdf_tool


def make_pdf(path: Path, pages: int) -> None:
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=72, height=72)
    with path.open('wb') as f:
        writer.write(f)


def test_split_merge_extract_reorder_rotate_alternate_and_workspace(tmp_path):
    a = tmp_path / 'a.pdf'
    b = tmp_path / 'b.pdf'
    make_pdf(a, 3)
    make_pdf(b, 2)

    split_dir = tmp_path / 'split'
    pdf_tool.split_pdf(a, split_dir)
    assert len(list(split_dir.glob('*.pdf'))) == 3

    merged = tmp_path / 'merged.pdf'
    pdf_tool.merge_pdfs([a, b], merged)
    assert len(PdfReader(str(merged)).pages) == 5

    extracted = tmp_path / 'extracted.pdf'
    pdf_tool.extract_pages(a, extracted, '1,3')
    assert len(PdfReader(str(extracted)).pages) == 2

    reordered = tmp_path / 'reordered.pdf'
    pdf_tool.reorder_pages(a, reordered, '3,1,2')
    assert len(PdfReader(str(reordered)).pages) == 3

    rotated = tmp_path / 'rotated.pdf'
    pdf_tool.rotate_pages(a, rotated, 90, '2')
    assert len(PdfReader(str(rotated)).pages) == 3

    alternated = tmp_path / 'alternated.pdf'
    pdf_tool.alternate_pdfs([a, b], alternated)
    assert len(PdfReader(str(alternated)).pages) == 5

    ws = tmp_path / 'workspace.json'
    pdf_tool.save_workspace(ws, 'demo', [{'op': 'merge'}])
    loaded = pdf_tool.load_workspace(ws)
    assert loaded.name == 'demo'
    assert loaded.steps == [{'op': 'merge'}]
