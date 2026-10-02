"""
Plot Script for Running Example Figure (FSE Paper) - Aligned & Compact Publication Edition
Target width: 394 pt (matches acmsmall \linewidth / \textwidth exactly at 100% native scale).
Height compressed to 260 pt with perfect 3-column content alignment and clean orthogonal arrows.
"""

from __future__ import annotations
import subprocess
import shutil
from pathlib import Path
import pymupdf

OUTPUT_DIR = Path(__file__).resolve().parent
OVERLEAF_FIG_DIR = Path(r"D:\论文撰写\FSE\overleaf\figures")

HTML_PATH = OUTPUT_DIR / "running_example.html"
PNG_PATH = OUTPUT_DIR / "running_example.png"
PDF_PATH = OUTPUT_DIR / "running_example.pdf"

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

PAGE_WIDTH_PT = 394
PAGE_HEIGHT_PT = 268

HTML_CONTENT = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  @page {{
    size: {PAGE_WIDTH_PT}pt {PAGE_HEIGHT_PT}pt;
    margin: 0;
  }}
  html, body {{
    width: {PAGE_WIDTH_PT}pt;
    height: {PAGE_HEIGHT_PT}pt;
    margin: 0;
    padding: 2.5pt 2.5pt;
    background-color: #ffffff;
    color: #111827;
    font-family: "Times New Roman", Times, Georgia, serif;
    font-size: 8.0pt;
    line-height: 1.25;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  /* 3-Column Continuous Flow Grid */
  .grid-flow {{
    display: grid;
    grid-template-columns: 114pt 146pt 122pt;
    column-gap: 6pt;
    height: 263pt;
    align-items: stretch;
    position: relative;
    break-inside: avoid;
    page-break-inside: avoid;
  }}

  /* Column Panels */
  .panel-col {{
    border: 0.75pt solid #9ca3af;
    border-radius: 2pt;
    background: #ffffff;
    padding: 3pt 3.5pt;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }}

  .panel-center {{
    border: 1pt solid #4b5563;
    border-radius: 2pt;
    background: #ffffff;
    padding: 3pt 3.5pt;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }}

  /* Top Column Titles */
  .col-title {{
    font-size: 9.0pt;
    font-weight: bold;
    color: #111827;
    border-bottom: 0.75pt solid #9ca3af;
    padding-bottom: 1.5pt;
    margin-bottom: 2.5pt;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }}
  .col-title-sub {{
    font-size: 8.0pt;
    font-weight: normal;
    color: #4b5563;
  }}

  /* Stage Card Blocks */
  .stage-card {{
    border: 0.5pt solid #d1d5db;
    border-radius: 2pt;
    background: #ffffff;
    padding: 2.5pt 3pt;
    margin-bottom: 2.5pt;
  }}

  .stage-head {{
    font-size: 8.4pt;
    font-weight: bold;
    color: #111827;
    margin-bottom: 1.5pt;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }}

  .gap-text {{
    font-size: 7.6pt;
    color: #374151;
    line-height: 1.2;
    background: #f9fafb;
    border: 0.5pt solid #e5e7eb;
    padding: 1.5pt 2pt;
    border-radius: 1.5pt;
    margin-bottom: 2pt;
  }}

  .plan-field {{
    font-size: 7.8pt;
    color: #374151;
    line-height: 1.2;
    margin-bottom: 1pt;
  }}
  .plan-field b {{
    color: #111827;
  }}

  .dialog-text {{
    font-size: 8.0pt;
    line-height: 1.22;
    color: #111827;
  }}

  /* 2-Column State Table (40% / 60%) */
  .state-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 7.8pt;
    line-height: 1.2;
    margin-top: 1pt;
    border: 0.5pt solid #d1d5db;
  }}
  .state-table th {{
    font-size: 7.8pt;
    font-weight: bold;
    color: #111827;
    background: #f3f4f6;
    text-align: left;
    padding: 2.5pt 2.5pt;
    border-bottom: 0.75pt solid #9ca3af;
  }}
  .state-table td {{
    padding: 3pt 2.5pt;
    border-bottom: 0.5pt solid #e5e7eb;
    vertical-align: middle;
  }}
  .table-group {{
    background: #f9fafb;
    font-weight: bold;
    font-size: 7.8pt;
    color: #1f2937;
    border-top: 0.75pt solid #d1d5db;
  }}

  /* Highlighted Target Row in Table (Soft Blue Trace) */
  .row-target {{
    background: #f0f7ff;
  }}
  .row-target td {{
    color: #111827;
  }}

  /* Right-side Target Highlight Box (Soft Blue Trace) */
  .target-highlight {{
    background: #f0f7ff;
    border: 0.5pt solid #93c5fd;
    border-radius: 1.5pt;
    padding: 1pt 2pt;
    color: #111827;
  }}

  /* Right-side Update Card (Soft Blue Trace) */
  .update-card {{
    background: #f0f7ff;
    border: 0.75pt solid #93c5fd;
    border-radius: 2pt;
    padding: 2.5pt 3pt;
  }}

  /* Connector SVG Overlay */
  .svg-overlay {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 20;
  }}
</style>
</head>
<body>

  <!-- Three-Column Continuous Flow Grid -->
  <div class="grid-flow">

    <!-- SVG Connectors (Clean Orthogonal Stepped Lines) -->
    <svg class="svg-overlay" viewBox="0 0 389 257">
      <defs>
        <marker id="arrow-blue" viewBox="0 0 6 6" refX="5" refY="3" markerWidth="4.5" markerHeight="4.5" orient="auto-start-reverse">
          <path d="M 0 0 L 6 3 L 0 6 z" fill="#1d4ed8"/>
        </marker>
        <marker id="arrow-gray" viewBox="0 0 6 6" refX="5" refY="3" markerWidth="4.5" markerHeight="4.5" orient="auto-start-reverse">
          <path d="M 0 0 L 6 3 L 0 6 z" fill="#4b5563"/>
        </marker>
      </defs>

      <!-- Connection 1: Interviewee Response in Col 1 -> C. Understanding Evolution in Col 2 (Clean Orthogonal Step) -->
      <path d="M 116.5 143 L 119.5 143 L 119.5 34 L 123 34" fill="none" stroke="#4b5563" stroke-width="1.1" marker-end="url(#arrow-gray)"/>

      <!-- Connection 2: Timeout Handling row in Col 2 -> Target Slot: Timeout Handling in Col 3 (Clean Orthogonal Step) -->
      <path d="M 268.5 129.4 L 271.5 129.4 L 271.5 55.2 L 278 55.2" fill="none" stroke="#1d4ed8" stroke-width="1.2" stroke-dasharray="2.5,1.5" marker-end="url(#arrow-blue)"/>
    </svg>

    <!-- ==================== LEFT COLUMN: Round t+1 ==================== -->
    <div class="panel-col">
      <div class="col-title">
        <span>Round <i>t</i>+1</span>
      </div>

      <!-- B. Interview Planning with Gap Rationale -->
      <div class="stage-card">
        <div class="stage-head"><span>B. Interview Planning</span></div>
        <div class="gap-text">
          <b>Current Gap:</b> No approver role is specified in <i>U<sub>t</sub></i>.
        </div>
        <div class="plan-field">Topic: Approval Process</div>
        <div class="plan-field">Target Slot: <b>Approver Role</b></div>
        <div class="plan-field">Strategy: <b>Fill Gaps</b></div>
        <div class="dialog-text" style="margin-top:1.5pt;">
          <b><i>q<sub>t+1</sub></i>:</b> "Who approves submitted equipment reservations?"
        </div>
      </div>

      <!-- Interviewee Response -->
      <div class="stage-card" style="margin-bottom:0;">
        <div class="stage-head"><span>Interviewee Response <i>r<sub>t+1</sub></i></span></div>
        <div class="dialog-text">
          "The <b>lab administrator</b> approves regular reservations; the <b>on-duty lead</b> approves urgent weekend reservations. We prefer <b>SMS notifications</b>, but the channel is not finalized."
        </div>
      </div>
    </div>

    <!-- ==================== MIDDLE COLUMN: Understanding Evolution U_(t+1) ==================== -->
    <div class="panel-center">
      <div class="col-title" style="border-bottom-color:#4b5563; margin-bottom:2pt;">
        <span>C. Understanding Evolution</span>
        <span class="col-title-sub"><i>U<sub>t+1</sub></i></span>
      </div>

      <!-- Central 2-Column State Table (40% / 60%) -->
      <table class="state-table">
        <thead>
          <tr>
            <th style="width: 40%;">Slot</th>
            <th style="width: 60%;">Current Content</th>
          </tr>
        </thead>
        <tbody>
          <!-- Topic: Approval Process -->
          <tr class="table-group">
            <td colspan="2">&bull; Topic: Approval Process</td>
          </tr>
          <tr>
            <td style="padding-left: 3.5pt;">Approver Role</td>
            <td>Regular reservations: lab administrator</td>
          </tr>
          <tr>
            <td style="padding-left: 3.5pt;">Weekend Approval Rule</td>
            <td>Urgent weekend reservations: on-duty lead</td>
          </tr>
          <tr class="row-target" id="row-timeout">
            <td style="padding-left: 3.5pt; font-weight:bold;">Timeout Handling</td>
            <td style="color:#6b7280; font-weight:bold;">&mdash;</td>
          </tr>

          <!-- Topic: System Notification -->
          <tr class="table-group">
            <td colspan="2">&bull; Topic: System Notification</td>
          </tr>
          <tr>
            <td style="padding-left: 3.5pt;">Notification Channel</td>
            <td>Prefer SMS; not finalized</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ==================== RIGHT COLUMN: Round t+2 ==================== -->
    <div class="panel-col">
      <div class="col-title">
        <span>Round <i>t</i>+2</span>
      </div>

      <!-- B. Interview Planning -->
      <div class="stage-card">
        <div class="stage-head"><span>B. Interview Planning</span></div>
        <div class="plan-field">Topic: Approval Process</div>
        <div class="plan-field target-highlight" id="target-slot-t2">
          Target Slot: <b>Timeout Handling</b>
        </div>
        <div class="plan-field">Strategy: <b>Deepen</b></div>
        <div class="dialog-text" style="margin-top:1.5pt;">
          <b><i>q<sub>t+2</sub></i>:</b> "What should happen if an urgent weekend reservation remains unapproved?"
        </div>
      </div>

      <!-- Interviewee Response -->
      <div class="stage-card">
        <div class="stage-head"><span>Interviewee Response <i>r<sub>t+2</sub></i></span></div>
        <div class="dialog-text">
          "After two hours without approval, the system automatically <b>reassigns approval to the lab director</b>."
        </div>
      </div>

      <!-- C. Understanding Evolution (Updated Slot Only - Single Paragraph) -->
      <div class="update-card">
        <div class="stage-head" style="margin-bottom:1.5pt;">
          <span>C. Understanding Evolution</span>
          <span class="col-title-sub"><i>U<sub>t+2</sub></i></span>
        </div>
        <div class="plan-field" style="margin-top:1pt; margin-bottom:1.5pt;">Slot: <b>Timeout Handling</b></div>
        <div class="dialog-text">
          For urgent weekend reservations, automatically reassign approval to the lab director after 2 h without approval.
        </div>
      </div>
    </div>

  </div>

</body>
</html>
"""

def main():
    print(f"Writing HTML to {HTML_PATH}...")
    HTML_PATH.write_text(HTML_CONTENT, encoding="utf-8")

    # Render vector PDF via Edge Headless
    print("Rendering vector PDF via Edge Headless...")
    cmd_pdf = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={PDF_PATH.resolve()}",
        str(HTML_PATH.resolve()),
    ]
    subprocess.run(cmd_pdf, check=True)

    # Inspect PDF metrics and trim blank pages if any
    doc = pymupdf.open(PDF_PATH)
    while len(doc) > 1 and len(doc[-1].get_text("blocks")) == 0:
        doc.delete_page(len(doc) - 1)
    
    page_count = len(doc)
    print(f"Generated PDF page count: {page_count}")
    assert page_count == 1, f"Expected strictly 1 page, got {page_count} pages!"

    p = doc[0]
    pix = p.get_pixmap(dpi=260)
    pix.save(PNG_PATH)
    print(f"Saved PNG to {PNG_PATH}")

    # Save cleaned 1-page PDF
    temp_pdf = OUTPUT_DIR / "temp_clean.pdf"
    doc.save(temp_pdf)
    doc.close()
    shutil.move(temp_pdf, PDF_PATH)

    # Copy to Overleaf figures directory
    if OVERLEAF_FIG_DIR.exists():
        overleaf_pdf = OVERLEAF_FIG_DIR / "running_example.pdf"
        overleaf_png = OVERLEAF_FIG_DIR / "running_example.png"
        shutil.copy2(PDF_PATH, overleaf_pdf)
        shutil.copy2(PNG_PATH, overleaf_png)
        print(f"Copied to Overleaf figures: {overleaf_pdf}")

    print("[SUCCESS] Aligned and compact running example figure created successfully!")

if __name__ == "__main__":
    main()
