# Software Requirements Specification: PDF Split and Merge

## 1. Scope and Context

### [SC-001] (stated)
The system is a free graphical tool for manipulating PDF documents without altering the original input files.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."

## 2. Actors

None specified.

## 3. Functional Requirements

### [FR-001] (stated)
The system shall support splitting PDF documents.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."

### [FR-002] (stated)
The system shall support merging selected files or sections into a new PDF.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."

### [FR-003] (stated)
The system shall support extracting pages from PDF documents.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."

### [FR-004] (stated)
The system shall support rotating pages in 90-degree left or right steps.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T022]` "For this tool, fixed increments are enough, mainly 90-degree steps for left or right rotation. That covers the common use case of correcting scanned pages or aligning documents, and it keeps the workflow simple and predictable. I don’t see a need for arbitrary angles unless we later find a niche use case that really depends on that."

### [FR-005] (stated)
The system shall support reordering pages.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."

### [FR-006] (stated)
The system shall support alternating pages from different documents.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T046]` "They should be able to load the source documents, choose the alternating pattern, and then preview the resulting page sequence before saving. The tool should help with interleaving when they’re combining things like two-sided scans, duplicate sets from different sources, or documents that need to be matched page by page rather than just appended. In those cases, plain merge or separate reordering would be too manual and error-prone."

### [FR-007] (stated)
The system shall support visually composing new PDF documents from selected pages and sections.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T006]` "A successful result is that they can visually build the final PDF with the pages in the right order, the right sections included, and no surprises compared to what they saw while assembling it. In day-to-day work, that usually means quickly combining separate files, pulling selected pages from a larger document, and rearranging or rotating pages until the output matches the intended packet or report. The most important part is making that assembly process easy to verify before saving, so they can trust the final document without having to open and fix it multiple times."
- `[interview_turn:T094]` "On day one, it should definitely support adding PDFs, reordering pages or whole files, removing items, rotating pages, splitting and merging, and visually building a new output from selected sections. I’d also want simple page previewing so the user can verify what they’re assembling before exporting. As for safeguards, it should never change the source files, and it should make it hard to accidentally lose work by prompting before closing or discarding an unsaved layout."

### [FR-008] (stated)
The system shall allow users to preview assembled or split results before saving or exporting.

**Source Evidence:**
- `[interview_turn:T006]` "A successful result is that they can visually build the final PDF with the pages in the right order, the right sections included, and no surprises compared to what they saw while assembling it. In day-to-day work, that usually means quickly combining separate files, pulling selected pages from a larger document, and rearranging or rotating pages until the output matches the intended packet or report. The most important part is making that assembly process easy to verify before saving, so they can trust the final document without having to open and fix it multiple times."
- `[interview_turn:T030]` "Usually they decide by page ranges, like splitting after certain pages or extracting specific sections into separate files. What matters most is that the split is accurate, fast, and produces outputs that keep the original page quality without changing the source file. It’s also important that they can preview the result before creating the output so they know each new PDF is organized the way they intended."
- `[interview_turn:T032]` "The preview should show the resulting output documents in the order they’ll be created, with clear page ranges and the pages included in each file. If they notice a wrong boundary or an omitted page, they should be able to adjust the split right there before committing. That kind of quick correction is important, but it should still be limited to split-related changes rather than full document editing."
- `[interview_turn:T042]` "They should be able to review a visual composition preview that shows the final sequence page by page, including which source file each page came from and any rotations that will be applied. It should be easy to spot missing sections, duplicates, or pages in the wrong order before they save. If something looks off, they need to be able to rearrange or remove items right in that preview so they can trust the final PDF before committing."

### [FR-009] (conditional)
The system shall allow users to make lightweight adjustments during preview, including rotating, rearranging, or removing items, when those changes are obvious during review.

**Source Evidence:**
- `[interview_turn:T020]` "I’d prefer it not be strictly read-only if a simple adjustment is obvious during review, like rotating a page or moving it in the sequence. That said, I wouldn’t want full editing there; it should stay focused on lightweight corrections so the user can fix a mistake without backing out of the preview. If the change is more involved, they should go back to the assembly workspace rather than trying to do it in the inspection view."
- `[interview_turn:T032]` "The preview should show the resulting output documents in the order they’ll be created, with clear page ranges and the pages included in each file. If they notice a wrong boundary or an omitted page, they should be able to adjust the split right there before committing. That kind of quick correction is important, but it should still be limited to split-related changes rather than full document editing."
- `[interview_turn:T042]` "They should be able to review a visual composition preview that shows the final sequence page by page, including which source file each page came from and any rotations that will be applied. It should be easy to spot missing sections, duplicates, or pages in the wrong order before they save. If something looks off, they need to be able to rearrange or remove items right in that preview so they can trust the final PDF before committing."

### [FR-010] (stated)
The system shall allow users to add PDFs, remove items, and reorder pages or whole files in the graphical workflow.

**Source Evidence:**
- `[interview_turn:T094]` "On day one, it should definitely support adding PDFs, reordering pages or whole files, removing items, rotating pages, splitting and merging, and visually building a new output from selected sections. I’d also want simple page previewing so the user can verify what they’re assembling before exporting. As for safeguards, it should never change the source files, and it should make it hard to accidentally lose work by prompting before closing or discarding an unsaved layout."

### [FR-011] (stated)
The system shall provide a visual composition preview that shows the final page sequence page by page before saving.

**Source Evidence:**
- `[interview_turn:T042]` "They should be able to review a visual composition preview that shows the final sequence page by page, including which source file each page came from and any rotations that will be applied. It should be easy to spot missing sections, duplicates, or pages in the wrong order before they save. If something looks off, they need to be able to rearrange or remove items right in that preview so they can trust the final PDF before committing."

### [FR-012] (stated)
The system shall show which source file each page came from in the composition preview.

**Source Evidence:**
- `[interview_turn:T042]` "They should be able to review a visual composition preview that shows the final sequence page by page, including which source file each page came from and any rotations that will be applied. It should be easy to spot missing sections, duplicates, or pages in the wrong order before they save. If something looks off, they need to be able to rearrange or remove items right in that preview so they can trust the final PDF before committing."

### [FR-013] (stated)
The system shall show which pages are included or left out in preview.

**Source Evidence:**
- `[interview_turn:T016]` "The preview should let them confirm page order, which pages are included or left out, and whether any pages need rotation or rearrangement before saving. In day-to-day use, that’s usually enough to catch mistakes like a missing section or an upside-down page. A quick preview may not be enough for very detailed work, like scanned pages with tiny text or documents where exact layout and margins really matter, because people may need to zoom in or inspect those more carefully."

### [FR-014] (stated)
The system shall allow users to rearrange or remove items directly in the preview before saving.

**Source Evidence:**
- `[interview_turn:T042]` "They should be able to review a visual composition preview that shows the final sequence page by page, including which source file each page came from and any rotations that will be applied. It should be easy to spot missing sections, duplicates, or pages in the wrong order before they save. If something looks off, they need to be able to rearrange or remove items right in that preview so they can trust the final PDF before committing."

### [FR-015] (stated)
The system shall support zooming in on pages during preview or inspection.

**Source Evidence:**
- `[interview_turn:T018]` "It should at least support zooming in and stepping through pages one by one so people can inspect individual pages closely before they commit. Margin checks and text clarity matter mostly for scanned or packed documents, so if the tool can show the page at a good resolution and let the user verify those visually, that would be enough. I don’t think it needs full editing features for that stage, just a reliable way to inspect what will actually be saved."
- `[interview_turn:T044]` "The preview should support zooming and opening a page in a larger view so users can inspect fine detail, and it should be good enough to check margins, alignment, and whether a rotated page really looks right. I wouldn’t make deeper inspection mandatory in every case, but it should be available for scanned documents, forms, or anything where visual accuracy matters more. In those cases, it’s especially important because a page can look fine in thumbnail view and still be wrong when printed or archived."

### [FR-016] (stated)
The system shall support stepping through pages one by one during inspection.

**Source Evidence:**
- `[interview_turn:T018]` "It should at least support zooming in and stepping through pages one by one so people can inspect individual pages closely before they commit. Margin checks and text clarity matter mostly for scanned or packed documents, so if the tool can show the page at a good resolution and let the user verify those visually, that would be enough. I don’t think it needs full editing features for that stage, just a reliable way to inspect what will actually be saved."

### [FR-017] (stated)
The system shall support opening a page in a larger view for closer inspection.

**Source Evidence:**
- `[interview_turn:T044]` "The preview should support zooming and opening a page in a larger view so users can inspect fine detail, and it should be good enough to check margins, alignment, and whether a rotated page really looks right. I wouldn’t make deeper inspection mandatory in every case, but it should be available for scanned documents, forms, or anything where visual accuracy matters more. In those cases, it’s especially important because a page can look fine in thumbnail view and still be wrong when printed or archived."

### [FR-018] (stated)
The system shall support page-range based splitting, including splitting after certain pages and extracting specific sections into separate files.

**Source Evidence:**
- `[interview_turn:T030]` "Usually they decide by page ranges, like splitting after certain pages or extracting specific sections into separate files. What matters most is that the split is accurate, fast, and produces outputs that keep the original page quality without changing the source file. It’s also important that they can preview the result before creating the output so they know each new PDF is organized the way they intended."

### [FR-019] (stated)
The system shall allow users to adjust split boundaries in the preview before creating output.

**Source Evidence:**
- `[interview_turn:T032]` "The preview should show the resulting output documents in the order they’ll be created, with clear page ranges and the pages included in each file. If they notice a wrong boundary or an omitted page, they should be able to adjust the split right there before committing. That kind of quick correction is important, but it should still be limited to split-related changes rather than full document editing."

### [FR-020] (stated)
The system shall support previewing the resulting split output documents in the order they will be created, with clear page ranges and included pages for each file.

**Source Evidence:**
- `[interview_turn:T032]` "The preview should show the resulting output documents in the order they’ll be created, with clear page ranges and the pages included in each file. If they notice a wrong boundary or an omitted page, they should be able to adjust the split right there before committing. That kind of quick correction is important, but it should still be limited to split-related changes rather than full document editing."

### [FR-021] (stated)
The system shall support visually building a new output from selected sections while preserving the intended order before export.

**Source Evidence:**
- `[interview_turn:T094]` "On day one, it should definitely support adding PDFs, reordering pages or whole files, removing items, rotating pages, splitting and merging, and visually building a new output from selected sections. I’d also want simple page previewing so the user can verify what they’re assembling before exporting. As for safeguards, it should never change the source files, and it should make it hard to accidentally lose work by prompting before closing or discarding an unsaved layout."

### [FR-022] (stated)
The system shall support alternating page sequences from multiple source documents according to a user-chosen pattern.

**Source Evidence:**
- `[interview_turn:T046]` "They should be able to load the source documents, choose the alternating pattern, and then preview the resulting page sequence before saving. The tool should help with interleaving when they’re combining things like two-sided scans, duplicate sets from different sources, or documents that need to be matched page by page rather than just appended. In those cases, plain merge or separate reordering would be too manual and error-prone."

### [FR-023] (stated)
The system shall keep the original order within each source document during interleaving.

**Source Evidence:**
- `[interview_turn:T050]` "It should keep the original order within each source and flag the mismatch for the user rather than trying to automatically skip ahead. If the sources don’t line up cleanly, the preview should make that obvious so the user can decide whether to continue, adjust the pattern, or leave pages out. Pausing the workflow for confirmation would be fine if it helps prevent a bad output."
- `[interview_turn:T052]` "Intentional repeats should be preserved exactly as they appear in the source, as long as the user has chosen to include that range. The tool shouldn’t automatically collapse duplicates if that would change the intended order or content. If something looks like accidental duplication, I’d rather have it flagged as a possible issue in the preview than have the software decide on its own."

### [FR-024] (conditional)
The system shall continue alternating pages until one source runs out, then follow the chosen mode to stop or continue with the remaining pages.

**Source Evidence:**
- `[interview_turn:T048]` "If the documents are different lengths, the tool should keep alternating until one source runs out, then either stop or continue with the remaining pages based on the chosen mode. For missing pages, I’d expect the tool to preserve whatever is available and flag the gap rather than trying to invent a replacement. If one source needs to repeat more than once, that should be an explicit option, because otherwise the result could be surprising and hard to trust."

### [FR-025] (stated)
The system shall preserve available pages and flag gaps when a source page is missing during interleaving.

**Source Evidence:**
- `[interview_turn:T048]` "If the documents are different lengths, the tool should keep alternating until one source runs out, then either stop or continue with the remaining pages based on the chosen mode. For missing pages, I’d expect the tool to preserve whatever is available and flag the gap rather than trying to invent a replacement. If one source needs to repeat more than once, that should be an explicit option, because otherwise the result could be surprising and hard to trust."

### [FR-026] (stated)
The system shall allow an explicit option for a source to repeat more than once during interleaving or assembly.

**Source Evidence:**
- `[interview_turn:T048]` "If the documents are different lengths, the tool should keep alternating until one source runs out, then either stop or continue with the remaining pages based on the chosen mode. For missing pages, I’d expect the tool to preserve whatever is available and flag the gap rather than trying to invent a replacement. If one source needs to repeat more than once, that should be an explicit option, because otherwise the result could be surprising and hard to trust."
- `[interview_turn:T110]` "It should let the user choose exactly which pages repeat and how many times they repeat in the assembly. I’d expect that to be set visually in the workspace, so they can duplicate a page or page range and adjust the sequence as needed before export. If the same source is reused several times, the app should keep those repetitions clear so the user can still edit them independently."

### [FR-027] (stated)
The system shall flag mismatches or possible accidental duplication in the preview instead of automatically correcting them.

**Source Evidence:**
- `[interview_turn:T050]` "It should keep the original order within each source and flag the mismatch for the user rather than trying to automatically skip ahead. If the sources don’t line up cleanly, the preview should make that obvious so the user can decide whether to continue, adjust the pattern, or leave pages out. Pausing the workflow for confirmation would be fine if it helps prevent a bad output."
- `[interview_turn:T052]` "Intentional repeats should be preserved exactly as they appear in the source, as long as the user has chosen to include that range. The tool shouldn’t automatically collapse duplicates if that would change the intended order or content. If something looks like accidental duplication, I’d rather have it flagged as a possible issue in the preview than have the software decide on its own."

### [FR-028] (stated)
The system shall steer users away from interleaving when incompatible page sizes or booklet-like layouts would clearly break the document.

**Source Evidence:**
- `[interview_turn:T054]` "Yes, in some cases it should avoid interleaving and steer the user toward a different workflow. I’d expect that for documents with very different page sizes, mixed orientations that would make the result messy, or forms and booklets where page position matters structurally rather than just visually. If the pages depend on internal relationships like spreads or sectioning, keeping them separate or merging them in a more controlled way is safer."
- `[interview_turn:T056]` "If the mismatch would clearly break the document, like incompatible page sizes or a booklet layout that would lose its structure, the tool should steer the user away immediately. If it’s more of a risk than a hard blocker, then it should still allow the operation but only with a warning and a strong preview so the user can judge the output. The main rule is whether the result is likely to be unusable or just needs careful review."

### [FR-029] (conditional)
The system shall allow a controlled interleaving or merge with warning and strong preview when the mismatch is a risk rather than a hard blocker.

**Source Evidence:**
- `[interview_turn:T054]` "Yes, in some cases it should avoid interleaving and steer the user toward a different workflow. I’d expect that for documents with very different page sizes, mixed orientations that would make the result messy, or forms and booklets where page position matters structurally rather than just visually. If the pages depend on internal relationships like spreads or sectioning, keeping them separate or merging them in a more controlled way is safer."
- `[interview_turn:T056]` "If the mismatch would clearly break the document, like incompatible page sizes or a booklet layout that would lose its structure, the tool should steer the user away immediately. If it’s more of a risk than a hard blocker, then it should still allow the operation but only with a warning and a strong preview so the user can judge the output. The main rule is whether the result is likely to be unusable or just needs careful review."

### [FR-030] (stated)
The system shall let users load source documents and preview the resulting page sequence before saving when alternating pages.

**Source Evidence:**
- `[interview_turn:T046]` "They should be able to load the source documents, choose the alternating pattern, and then preview the resulting page sequence before saving. The tool should help with interleaving when they’re combining things like two-sided scans, duplicate sets from different sources, or documents that need to be matched page by page rather than just appended. In those cases, plain merge or separate reordering would be too manual and error-prone."

### [FR-031] (stated)
The system shall allow users to confirm page order, included sections, and rotations in a preview before saving the final PDF.

**Source Evidence:**
- `[interview_turn:T016]` "The preview should let them confirm page order, which pages are included or left out, and whether any pages need rotation or rearrangement before saving. In day-to-day use, that’s usually enough to catch mistakes like a missing section or an upside-down page. A quick preview may not be enough for very detailed work, like scanned pages with tiny text or documents where exact layout and margins really matter, because people may need to zoom in or inspect those more carefully."
- `[interview_turn:T042]` "They should be able to review a visual composition preview that shows the final sequence page by page, including which source file each page came from and any rotations that will be applied. It should be easy to spot missing sections, duplicates, or pages in the wrong order before they save. If something looks off, they need to be able to rearrange or remove items right in that preview so they can trust the final PDF before committing."

### [FR-032] (stated)
The system shall allow users to perform split-related corrections, such as adjusting a wrong boundary or restoring an omitted page, directly in the split preview.

**Source Evidence:**
- `[interview_turn:T032]` "The preview should show the resulting output documents in the order they’ll be created, with clear page ranges and the pages included in each file. If they notice a wrong boundary or an omitted page, they should be able to adjust the split right there before committing. That kind of quick correction is important, but it should still be limited to split-related changes rather than full document editing."

### [FR-033] (stated)
The system shall allow users to relink a missing, moved, renamed, or replaced source file before export.

**Source Evidence:**
- `[interview_turn:T103]` "When an assembly still points to a source that has been moved, renamed, or replaced, what should the app let the user do to relink it before export?"
- `[interview_turn:T104]` "It should let the user browse for the new file and relink that source item before export. If the file was replaced with a different version, the user should be able to point the assembly at the new one and then verify the pages or section still match what they expected. I’d also want the app to make any broken links obvious in the workspace so they don’t get overlooked."
- `[interview_turn:T106]` "It should prompt the user to relink the item, then show a side-by-side or at least page-thumbnail comparison so they can confirm they’re still using the right content. If the replacement version has different page counts or changed page order, the app should warn them before export and let them adjust the selection. I’d want that check to happen inside the workspace, not only at the final save step."
- `[interview_turn:T116]` "It should open the project with the broken source clearly flagged, but keep the rest of the assembly usable so the user can still work on the unaffected parts. Then it should let them relink the missing file, and if it was changed, confirm the page mapping before they export. If they can’t recover it right away, the app should preserve the project state so nothing else is lost."

### [FR-034] (stated)
The system shall let users browse for a new file when a source item needs to be relinked.

**Source Evidence:**
- `[interview_turn:T104]` "It should let the user browse for the new file and relink that source item before export. If the file was replaced with a different version, the user should be able to point the assembly at the new one and then verify the pages or section still match what they expected. I’d also want the app to make any broken links obvious in the workspace so they don’t get overlooked."

### [FR-035] (stated)
The system shall keep the assembly usable for unaffected parts when a saved project is reopened and one source file is broken.

**Source Evidence:**
- `[interview_turn:T116]` "It should open the project with the broken source clearly flagged, but keep the rest of the assembly usable so the user can still work on the unaffected parts. Then it should let them relink the missing file, and if it was changed, confirm the page mapping before they export. If they can’t recover it right away, the app should preserve the project state so nothing else is lost."

### [FR-036] (stated)
The system shall let users remap affected pages, reorder them, or remove and re-add a problematic section after a relinked file has changed page count or page order.

**Source Evidence:**
- `[interview_turn:T108]` "It should let the user remap the affected pages, reorder them, or remove and re-add the problematic section right there in the workspace. If the page count changed, the app should highlight which extracted ranges no longer line up so the user can fix them manually. The goal is to make the assembly editable again without forcing them to start over from scratch."

### [FR-037] (stated)
The system shall preserve each repeated instance as independently editable in the workspace.

**Source Evidence:**
- `[interview_turn:T114]` "It should treat each repeated instance as independently editable in the workspace, even if they came from the same original page or range. That way the user can change just one copy’s position, rotation, or whether it stays included, without forcing the same change on every repetition. If possible, the app should make it clear which instances are linked and which are already unique so there’s no confusion."

### [FR-038] (stated)
The system shall let users change just one repeated instance's position, rotation, or inclusion without forcing the same change on every repetition.

**Source Evidence:**
- `[interview_turn:T114]` "It should treat each repeated instance as independently editable in the workspace, even if they came from the same original page or range. That way the user can change just one copy’s position, rotation, or whether it stays included, without forcing the same change on every repetition. If possible, the app should make it clear which instances are linked and which are already unique so there’s no confusion."

### [FR-039] (stated)
The system shall make broken links obvious in the workspace.

**Source Evidence:**
- `[interview_turn:T104]` "It should let the user browse for the new file and relink that source item before export. If the file was replaced with a different version, the user should be able to point the assembly at the new one and then verify the pages or section still match what they expected. I’d also want the app to make any broken links obvious in the workspace so they don’t get overlooked."
- `[interview_turn:T112]` "It should preserve the full workspace state: the selected source files, page ranges, order, rotations, repetitions, merge settings, and any other layout choices needed to reopen the job exactly as it was. Yes, it should keep file references as paths, and ideally also store enough metadata to detect when a source has moved, changed, or gone missing so the user gets a clear warning on reopen. If a source can’t be found, the project should still open with that item marked as broken and ready to relink."

### [FR-040] (stated)
The system shall preserve source references or enough information to let the user replace or reselect an item that was already added to an assembly.

**Source Evidence:**
- `[interview_turn:T102]` "If a source item is missing or unreadable, the app should stop that item from being included and clearly tell the user before the final output is created, rather than silently skipping it. If something was already added to an assembly and later needs to be edited again, I’d want the assembly to keep the reference to the source or at least keep enough information to let the user replace or reselect it easily. The important part is that the user can see what’s broken and fix it before exporting, instead of discovering it afterward."

### [FR-041] (stated)
The system shall allow users to choose exactly which pages repeat and how many times they repeat in the assembly.

**Source Evidence:**
- `[interview_turn:T110]` "It should let the user choose exactly which pages repeat and how many times they repeat in the assembly. I’d expect that to be set visually in the workspace, so they can duplicate a page or page range and adjust the sequence as needed before export. If the same source is reused several times, the app should keep those repetitions clear so the user can still edit them independently."

### [FR-042] (stated)
The system shall let users visually duplicate a page or page range and adjust the sequence in the workspace before export.

**Source Evidence:**
- `[interview_turn:T110]` "It should let the user choose exactly which pages repeat and how many times they repeat in the assembly. I’d expect that to be set visually in the workspace, so they can duplicate a page or page range and adjust the sequence as needed before export. If the same source is reused several times, the app should keep those repetitions clear so the user can still edit them independently."

### [FR-043] (stated)
The system shall allow users to save reusable workspaces or project files for later restoration.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T024]` "It should remember the last working setup as much as practical, especially the selected files, page order, and any split or merge structure the user was building. Saved presets or reusable workspaces would be very helpful too, because people often do the same kind of job repeatedly. For command-line use, it should preserve the parameters in a way that can be reused or copied into scripts, since that’s the main point of having the CLI path."
- `[interview_turn:T080]` "I’d prefer a simple project file or profile file rather than a heavy packaged archive, because the main need is to restore the workflow state, not necessarily bundle all the PDFs inside it. It should store the document list, page operations, output settings, and any layout or composition choices in a way that’s easy to reload later. If there’s an option to reference files by path and optionally validate they still exist, that would be very useful for recurring work."
- `[interview_turn:T112]` "It should preserve the full workspace state: the selected source files, page ranges, order, rotations, repetitions, merge settings, and any other layout choices needed to reopen the job exactly as it was. Yes, it should keep file references as paths, and ideally also store enough metadata to detect when a source has moved, changed, or gone missing so the user gets a clear warning on reopen. If a source can’t be found, the project should still open with that item marked as broken and ready to relink."

### [FR-044] (stated)
The system shall restore the full working context from a saved workspace as much as possible, including layout, file selections, page order, split or merge structure, page ranges, rotations, repetitions, merge settings, and other layout choices.

**Source Evidence:**
- `[interview_turn:T028]` "It should restore the full working context as much as possible, including layout, file selections, page order, and the split or merge structure. The idea is that the user opens a saved workspace and is very close to where they left off, not just starting from a template. I’d still expect some job-specific choices, like the final output file name or destination, to be confirmed again before saving."
- `[interview_turn:T080]` "I’d prefer a simple project file or profile file rather than a heavy packaged archive, because the main need is to restore the workflow state, not necessarily bundle all the PDFs inside it. It should store the document list, page operations, output settings, and any layout or composition choices in a way that’s easy to reload later. If there’s an option to reference files by path and optionally validate they still exist, that would be very useful for recurring work."
- `[interview_turn:T112]` "It should preserve the full workspace state: the selected source files, page ranges, order, rotations, repetitions, merge settings, and any other layout choices needed to reopen the job exactly as it was. Yes, it should keep file references as paths, and ideally also store enough metadata to detect when a source has moved, changed, or gone missing so the user gets a clear warning on reopen. If a source can’t be found, the project should still open with that item marked as broken and ready to relink."

### [FR-045] (stated)
The system shall restore document list and output settings from a saved workspace or project file.

**Source Evidence:**
- `[interview_turn:T080]` "I’d prefer a simple project file or profile file rather than a heavy packaged archive, because the main need is to restore the workflow state, not necessarily bundle all the PDFs inside it. It should store the document list, page operations, output settings, and any layout or composition choices in a way that’s easy to reload later. If there’s an option to reference files by path and optionally validate they still exist, that would be very useful for recurring work."
- `[interview_turn:T112]` "It should preserve the full workspace state: the selected source files, page ranges, order, rotations, repetitions, merge settings, and any other layout choices needed to reopen the job exactly as it was. Yes, it should keep file references as paths, and ideally also store enough metadata to detect when a source has moved, changed, or gone missing so the user gets a clear warning on reopen. If a source can’t be found, the project should still open with that item marked as broken and ready to relink."

### [FR-046] (stated)
The system shall keep file references as paths and detect when a source has moved, changed, or gone missing when reopening a saved project.

**Source Evidence:**
- `[interview_turn:T112]` "It should preserve the full workspace state: the selected source files, page ranges, order, rotations, repetitions, merge settings, and any other layout choices needed to reopen the job exactly as it was. Yes, it should keep file references as paths, and ideally also store enough metadata to detect when a source has moved, changed, or gone missing so the user gets a clear warning on reopen. If a source can’t be found, the project should still open with that item marked as broken and ready to relink."

### [FR-047] (stated)
The system shall warn the user clearly when a saved workflow includes a missing, changed, or unavailable setting or source, and preserve the saved file intact.

**Source Evidence:**
- `[interview_turn:T078]` "It should open as gracefully as possible and preserve the parts it still understands, rather than refusing to load the whole workflow. If something is missing or changed, it should warn the user clearly, show which setting is affected, and fall back to a sensible default or leave that part disabled until the user fixes it. I’d also expect it to keep the saved file intact so the user can still recover the original configuration if needed."
- `[interview_turn:T112]` "It should preserve the full workspace state: the selected source files, page ranges, order, rotations, repetitions, merge settings, and any other layout choices needed to reopen the job exactly as it was. Yes, it should keep file references as paths, and ideally also store enough metadata to detect when a source has moved, changed, or gone missing so the user gets a clear warning on reopen. If a source can’t be found, the project should still open with that item marked as broken and ready to relink."

### [FR-048] (stated)
The system shall open a saved project with broken sources marked as broken and ready to relink.

**Source Evidence:**
- `[interview_turn:T112]` "It should preserve the full workspace state: the selected source files, page ranges, order, rotations, repetitions, merge settings, and any other layout choices needed to reopen the job exactly as it was. Yes, it should keep file references as paths, and ideally also store enough metadata to detect when a source has moved, changed, or gone missing so the user gets a clear warning on reopen. If a source can’t be found, the project should still open with that item marked as broken and ready to relink."
- `[interview_turn:T116]` "It should open the project with the broken source clearly flagged, but keep the rest of the assembly usable so the user can still work on the unaffected parts. Then it should let them relink the missing file, and if it was changed, confirm the page mapping before they export. If they can’t recover it right away, the app should preserve the project state so nothing else is lost."

### [FR-049] (stated)
The system shall allow users to save the final output to a user-chosen location and name by default.

**Source Evidence:**
- `[interview_turn:T010]` "By default, I’d expect the user to choose the save location and name, with the tool remembering the last folder they used to make it easier next time. If they’re creating multiple versions or running a batch, the tool should help avoid overwriting by either prompting, auto-numbering, or using a naming pattern from the saved workspace or command line setup. The main rule is that it should be predictable and safe, so people don’t accidentally replace a source or a previously generated PDF."

### [FR-050] (stated)
The system shall remember the last folder used for saving.

**Source Evidence:**
- `[interview_turn:T010]` "By default, I’d expect the user to choose the save location and name, with the tool remembering the last folder they used to make it easier next time. If they’re creating multiple versions or running a batch, the tool should help avoid overwriting by either prompting, auto-numbering, or using a naming pattern from the saved workspace or command line setup. The main rule is that it should be predictable and safe, so people don’t accidentally replace a source or a previously generated PDF."

### [FR-051] (conditional)
The system shall help avoid overwriting existing files by prompting, auto-numbering, or using a naming pattern when creating multiple versions or running batch jobs.

**Source Evidence:**
- `[interview_turn:T010]` "By default, I’d expect the user to choose the save location and name, with the tool remembering the last folder they used to make it easier next time. If they’re creating multiple versions or running a batch, the tool should help avoid overwriting by either prompting, auto-numbering, or using a naming pattern from the saved workspace or command line setup. The main rule is that it should be predictable and safe, so people don’t accidentally replace a source or a previously generated PDF."

### [FR-052] (stated)
The system shall use a sensible default naming pattern for multiple split outputs based on the original file name and split sequence.

**Source Evidence:**
- `[interview_turn:T034]` "Both would be best. The tool should provide a sensible default naming pattern based on the original file name and the split sequence, but users should be able to rename the outputs if they want more control. For larger jobs, the default saves time, while manual naming matters when they need the files to fit an internal filing convention."

### [FR-053] (stated)
The system shall allow users to rename split outputs manually.

**Source Evidence:**
- `[interview_turn:T034]` "Both would be best. The tool should provide a sensible default naming pattern based on the original file name and the split sequence, but users should be able to rename the outputs if they want more control. For larger jobs, the default saves time, while manual naming matters when they need the files to fit an internal filing convention."

### [FR-054] (stated)
The system shall derive a safe, predictable default output name from the input when the user does not specify an output.

**Source Evidence:**
- `[interview_turn:T076]` "If the user doesn’t specify an output, it should default to a safe, predictable name derived from the input, usually in the same folder or in a clearly defined output folder if that was set in the profile. The filename should reflect the operation in some way, like split, merged, or extracted, and it should avoid overwriting existing files unless the user explicitly allows that. I’d expect the default to vary when the job profile changes, because a reusable profile should carry its own output conventions, but it should stay consistent for the same inputs and settings."

### [FR-055] (conditional)
The system shall place the default output in the same folder as the input or in a clearly defined output folder if one was set in the profile.

**Source Evidence:**
- `[interview_turn:T076]` "If the user doesn’t specify an output, it should default to a safe, predictable name derived from the input, usually in the same folder or in a clearly defined output folder if that was set in the profile. The filename should reflect the operation in some way, like split, merged, or extracted, and it should avoid overwriting existing files unless the user explicitly allows that. I’d expect the default to vary when the job profile changes, because a reusable profile should carry its own output conventions, but it should stay consistent for the same inputs and settings."

### [FR-056] (stated)
The system shall reflect the operation type in the default output filename, such as split, merged, or extracted.

**Source Evidence:**
- `[interview_turn:T076]` "If the user doesn’t specify an output, it should default to a safe, predictable name derived from the input, usually in the same folder or in a clearly defined output folder if that was set in the profile. The filename should reflect the operation in some way, like split, merged, or extracted, and it should avoid overwriting existing files unless the user explicitly allows that. I’d expect the default to vary when the job profile changes, because a reusable profile should carry its own output conventions, but it should stay consistent for the same inputs and settings."

### [FR-057] (stated)
The system shall support command-line operation without requiring the graphical interface.

**Source Evidence:**
- `[interview_turn:T002]` "It’s meant to let people take existing PDFs apart and put them back together again quickly, without needing a full PDF editor. In practice, I’d expect the main users to be office staff, admins, and power users who regularly handle reports, scans, invoices, and similar documents, plus some technical users who want a command-line option for repeat jobs.
The no-modification approach means the original PDFs should stay untouched at all times, so users work on copies or generated output instead of editing the source files directly. That way they can safely experiment with splits, merges, rotations, and page order changes without worrying about damaging the original document."
- `[interview_turn:T036]` "Command-line users should be able to define everything through parameters or a saved job profile, without needing the graphical interface at all. They’ll likely want to point to input and output paths directly, pass split and merge options in a script-friendly way, and rely on predictable default naming unless they override it. The main difference is that CLI usage needs to be more explicit and reproducible, since those runs are usually automated or repeated."

### [FR-058] (stated)
The system shall allow command-line users to define inputs, output paths, split and merge options, selected pages or ranges, ordering, naming pattern, and overwrite behavior through parameters or a saved job profile.

**Source Evidence:**
- `[interview_turn:T036]` "Command-line users should be able to define everything through parameters or a saved job profile, without needing the graphical interface at all. They’ll likely want to point to input and output paths directly, pass split and merge options in a script-friendly way, and rely on predictable default naming unless they override it. The main difference is that CLI usage needs to be more explicit and reproducible, since those runs are usually automated or repeated."
- `[interview_turn:T082]` "The command line should let the user override the inputs, output location, selected pages or ranges, merge versus split behavior, ordering, naming pattern, and whether overwriting is allowed. I’d also want any reusable profile settings to be overrideable at run time, so a script can reuse a base job but change just the few values that matter for that execution. That makes it easier to reproduce runs exactly while still keeping the profile useful for day-to-day automation."

### [FR-059] (stated)
The system shall allow reusable profile settings to be overridden at runtime from the command line.

**Source Evidence:**
- `[interview_turn:T082]` "The command line should let the user override the inputs, output location, selected pages or ranges, merge versus split behavior, ordering, naming pattern, and whether overwriting is allowed. I’d also want any reusable profile settings to be overrideable at run time, so a script can reuse a base job but change just the few values that matter for that execution. That makes it easier to reproduce runs exactly while still keeping the profile useful for day-to-day automation."

### [FR-060] (stated)
The system shall fail fast with a clear error message when a required command-line or job-profile parameter is missing.

**Source Evidence:**
- `[interview_turn:T040]` "If a required parameter is missing, the run should fail fast with a clear error message that says what’s missing and how to provide it. If a supplied value conflicts with the default behavior, the explicit user value should win unless it creates an invalid combination, in which case the tool should reject it rather than guessing. For automation, predictable failure is better than silently doing the wrong thing."
- `[interview_turn:T074]` "It should handle multiple input files, explicit page ranges, output paths, and options in a very predictable way, with clear quoting support for paths that contain spaces. If an argument is missing, malformed, or points to a file that doesn’t exist, it should fail fast with a clear error code and message rather than guessing. For automation, I’d also want it to be stable about option names and ordering so scripts behave the same across runs and platforms."

### [FR-061] (stated)
The system shall reject invalid combinations when an explicit command-line value conflicts with a default behavior.

**Source Evidence:**
- `[interview_turn:T040]` "If a required parameter is missing, the run should fail fast with a clear error message that says what’s missing and how to provide it. If a supplied value conflicts with the default behavior, the explicit user value should win unless it creates an invalid combination, in which case the tool should reject it rather than guessing. For automation, predictable failure is better than silently doing the wrong thing."

### [FR-062] (stated)
The system shall keep command-line behavior explicit and reproducible for recurring or automated operations.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T036]` "Command-line users should be able to define everything through parameters or a saved job profile, without needing the graphical interface at all. They’ll likely want to point to input and output paths directly, pass split and merge options in a script-friendly way, and rely on predictable default naming unless they override it. The main difference is that CLI usage needs to be more explicit and reproducible, since those runs are usually automated or repeated."
- `[interview_turn:T024]` "It should remember the last working setup as much as practical, especially the selected files, page order, and any split or merge structure the user was building. Saved presets or reusable workspaces would be very helpful too, because people often do the same kind of job repeatedly. For command-line use, it should preserve the parameters in a way that can be reused or copied into scripts, since that’s the main point of having the CLI path."

### [FR-063] (stated)
The system shall provide command-line runs with stable option names and ordering so scripts behave the same across runs and platforms.

**Source Evidence:**
- `[interview_turn:T074]` "It should handle multiple input files, explicit page ranges, output paths, and options in a very predictable way, with clear quoting support for paths that contain spaces. If an argument is missing, malformed, or points to a file that doesn’t exist, it should fail fast with a clear error code and message rather than guessing. For automation, I’d also want it to be stable about option names and ordering so scripts behave the same across runs and platforms."

### [FR-064] (stated)
The system shall handle multiple input files, explicit page ranges, output paths, and options predictably on the command line.

**Source Evidence:**
- `[interview_turn:T074]` "It should handle multiple input files, explicit page ranges, output paths, and options in a very predictable way, with clear quoting support for paths that contain spaces. If an argument is missing, malformed, or points to a file that doesn’t exist, it should fail fast with a clear error code and message rather than guessing. For automation, I’d also want it to be stable about option names and ordering so scripts behave the same across runs and platforms."

### [FR-065] (stated)
The system shall support quoting of command-line paths that contain spaces.

**Source Evidence:**
- `[interview_turn:T072]` "Yes, it should behave consistently across the three platforms, but it needs to respect each system’s path and quoting rules so scripts don’t break on spaces or special characters. I’d expect it to work cleanly from standard shells and batch files without requiring users to learn platform-specific quirks. If there are packaging choices, I’d prefer it to be installable in a way that makes the command available on the PATH and usable from automation right away."
- `[interview_turn:T074]` "It should handle multiple input files, explicit page ranges, output paths, and options in a very predictable way, with clear quoting support for paths that contain spaces. If an argument is missing, malformed, or points to a file that doesn’t exist, it should fail fast with a clear error code and message rather than guessing. For automation, I’d also want it to be stable about option names and ordering so scripts behave the same across runs and platforms."

### [FR-066] (stated)
The system shall be usable from standard shells and batch files on Windows, macOS, and Linux.

**Source Evidence:**
- `[interview_turn:T066]` "I’d expect it to run on the common desktop platforms, especially Windows, macOS, and Linux, because people use PDF tools in all of those environments. It should be easy to download and install locally, without needing a server or cloud account, and the command-line option should work in the same local setup for automation. In the normal workflow, that means users get it as a standalone desktop app, and they can also use it in scripts or batch jobs on their own machines."
- `[interview_turn:T072]` "Yes, it should behave consistently across the three platforms, but it needs to respect each system’s path and quoting rules so scripts don’t break on spaces or special characters. I’d expect it to work cleanly from standard shells and batch files without requiring users to learn platform-specific quirks. If there are packaging choices, I’d prefer it to be installable in a way that makes the command available on the PATH and usable from automation right away."

### [FR-067] (stated)
The system shall be installable so that the command is available on the PATH.

**Source Evidence:**
- `[interview_turn:T072]` "Yes, it should behave consistently across the three platforms, but it needs to respect each system’s path and quoting rules so scripts don’t break on spaces or special characters. I’d expect it to work cleanly from standard shells and batch files without requiring users to learn platform-specific quirks. If there are packaging choices, I’d prefer it to be installable in a way that makes the command available on the PATH and usable from automation right away."

### [FR-068] (stated)
The system shall support offline operation for local documents.

**Source Evidence:**
- `[interview_turn:T060]` "The tool should promise that files stay local by default and are not uploaded anywhere. Users should be able to expect that only the files they choose to process are accessed, and that temporary data is not left behind longer than necessary. For privacy, I’d want a clear statement that the application doesn’t inspect or share content beyond what’s needed to perform the PDF operations."
- `[interview_turn:T086]` "It should be fully usable offline for local documents, since that’s the safest default and fits the use case. I wouldn’t expect it to need network access for the core PDF operations at all. If there are any optional update checks or help resources, those should be separate and clearly not part of document processing."

### [FR-069] (stated)
The system shall not require network access for core PDF operations.

**Source Evidence:**
- `[interview_turn:T086]` "It should be fully usable offline for local documents, since that’s the safest default and fits the use case. I wouldn’t expect it to need network access for the core PDF operations at all. If there are any optional update checks or help resources, those should be separate and clearly not part of document processing."

### [FR-070] (stated)
The system shall keep files local by default and not upload them anywhere.

**Source Evidence:**
- `[interview_turn:T060]` "The tool should promise that files stay local by default and are not uploaded anywhere. Users should be able to expect that only the files they choose to process are accessed, and that temporary data is not left behind longer than necessary. For privacy, I’d want a clear statement that the application doesn’t inspect or share content beyond what’s needed to perform the PDF operations."

### [FR-071] (stated)
The system shall clean up temporary copies automatically when they are no longer needed to complete the operation.

**Source Evidence:**
- `[interview_turn:T062]` "Temporary copies should only exist for as long as they’re needed to complete the operation, then be cleaned up automatically. I wouldn’t expect them to be retained longer by default, except maybe if the user explicitly saves a reusable workspace or project state that includes references to the input files and settings. Even then, the actual document content should stay local and not be preserved more than necessary unless the user has clearly chosen that."

### [FR-072] (stated)
The system shall prevent source PDFs from being modified in place by default and shall write changes only to new output files or separate working copies.

**Source Evidence:**
- `[interview_turn:T002]` "It’s meant to let people take existing PDFs apart and put them back together again quickly, without needing a full PDF editor. In practice, I’d expect the main users to be office staff, admins, and power users who regularly handle reports, scans, invoices, and similar documents, plus some technical users who want a command-line option for repeat jobs.
The no-modification approach means the original PDFs should stay untouched at all times, so users work on copies or generated output instead of editing the source files directly. That way they can safely experiment with splits, merges, rotations, and page order changes without worrying about damaging the original document."
- `[interview_turn:T064]` "It should always protect the original source files and work on copies or produce new output files instead. The user should never have the original PDFs modified in place by default. If there were ever an advanced mode that works directly on originals, that would need to be very explicit and opt-in, but I’d consider that outside the normal expected behavior."
- `[interview_turn:T094]` "On day one, it should definitely support adding PDFs, reordering pages or whole files, removing items, rotating pages, splitting and merging, and visually building a new output from selected sections. I’d also want simple page previewing so the user can verify what they’re assembling before exporting. As for safeguards, it should never change the source files, and it should make it hard to accidentally lose work by prompting before closing or discarding an unsaved layout."
- `[interview_turn:T098]` "It should not edit the source PDF in place at all. The original file should always stay untouched, and any changes should be written only to a new output file or a separate working copy inside the app’s own workspace if it needs one. The only time I’d want a copied file is if the tool needs a temporary internal version to support the editing session, but even then it shouldn’t overwrite the user’s source."

### [FR-073] (stated)
The system shall not edit the source PDF in place at all.

**Source Evidence:**
- `[interview_turn:T064]` "It should always protect the original source files and work on copies or produce new output files instead. The user should never have the original PDFs modified in place by default. If there were ever an advanced mode that works directly on originals, that would need to be very explicit and opt-in, but I’d consider that outside the normal expected behavior."
- `[interview_turn:T098]` "It should not edit the source PDF in place at all. The original file should always stay untouched, and any changes should be written only to a new output file or a separate working copy inside the app’s own workspace if it needs one. The only time I’d want a copied file is if the tool needs a temporary internal version to support the editing session, but even then it shouldn’t overwrite the user’s source."

### [FR-074] (conditional)
The system shall allow an advanced mode that works directly on originals only if it is explicit and opt-in.

**Source Evidence:**
- `[interview_turn:T064]` "It should always protect the original source files and work on copies or produce new output files instead. The user should never have the original PDFs modified in place by default. If there were ever an advanced mode that works directly on originals, that would need to be very explicit and opt-in, but I’d consider that outside the normal expected behavior."

### [FR-075] (stated)
The system shall run on Windows, macOS, and Linux.

**Source Evidence:**
- `[interview_turn:T066]` "I’d expect it to run on the common desktop platforms, especially Windows, macOS, and Linux, because people use PDF tools in all of those environments. It should be easy to download and install locally, without needing a server or cloud account, and the command-line option should work in the same local setup for automation. In the normal workflow, that means users get it as a standalone desktop app, and they can also use it in scripts or batch jobs on their own machines."

### [FR-076] (stated)
The system shall be easy to download and install locally without needing a server or cloud account.

**Source Evidence:**
- `[interview_turn:T066]` "I’d expect it to run on the common desktop platforms, especially Windows, macOS, and Linux, because people use PDF tools in all of those environments. It should be easy to download and install locally, without needing a server or cloud account, and the command-line option should work in the same local setup for automation. In the normal workflow, that means users get it as a standalone desktop app, and they can also use it in scripts or batch jobs on their own machines."

### [FR-077] (stated)
The system shall be open source.

**Source Evidence:**
- `[interview_turn:T068]` "Yes, I’d expect it to be open source, because “free” in this context should mean users can use it without payment and also trust what it’s doing locally. I don’t have a specific license mandated, but it should be one that’s widely compatible and doesn’t restrict normal desktop or command-line use. I’d also want to avoid dependencies that would complicate redistribution or force any cloud service or proprietary runtime."

### [FR-078] (stated)
The system shall avoid dependencies or bundled components that force a cloud service dependency.

**Source Evidence:**
- `[interview_turn:T068]` "Yes, I’d expect it to be open source, because “free” in this context should mean users can use it without payment and also trust what it’s doing locally. I don’t have a specific license mandated, but it should be one that’s widely compatible and doesn’t restrict normal desktop or command-line use. I’d also want to avoid dependencies that would complicate redistribution or force any cloud service or proprietary runtime."
- `[interview_turn:T070]` "I’d want to avoid anything with strong copyleft obligations that could make redistribution complicated for downstream packagers, unless we deliberately decide that’s acceptable. Also, I’d avoid bundled components with unclear licensing, non-commercial restrictions, or anything that requires users to accept a cloud service dependency. In practice, I’d prefer clearly permissive dependencies and packaging that doesn’t put extra legal burden on people just trying to install and use the tool."

### [FR-079] (stated)
The system shall avoid bundled components with unclear licensing or non-commercial restrictions.

**Source Evidence:**
- `[interview_turn:T070]` "I’d want to avoid anything with strong copyleft obligations that could make redistribution complicated for downstream packagers, unless we deliberately decide that’s acceptable. Also, I’d avoid bundled components with unclear licensing, non-commercial restrictions, or anything that requires users to accept a cloud service dependency. In practice, I’d prefer clearly permissive dependencies and packaging that doesn’t put extra legal burden on people just trying to install and use the tool."

### [FR-080] (stated)
The system shall provide a clear statement that it does not inspect or share content beyond what is needed to perform PDF operations.

**Source Evidence:**
- `[interview_turn:T060]` "The tool should promise that files stay local by default and are not uploaded anywhere. Users should be able to expect that only the files they choose to process are accessed, and that temporary data is not left behind longer than necessary. For privacy, I’d want a clear statement that the application doesn’t inspect or share content beyond what’s needed to perform the PDF operations."

### [FR-081] (stated)
The system shall show progress for longer-running operations and allow the user to know the job has not stalled.

**Source Evidence:**
- `[interview_turn:T014]` "For a typical document, people would expect it to feel quick, basically a few seconds for simple split or merge jobs and not something that makes them wait long enough to lose confidence. I’d be fine with longer processing on bigger scans or batch jobs, as long as the tool shows progress and it’s clear it hasn’t frozen. If it starts taking unusually long on a normal-sized file, it should warn the user rather than just sit there silently, and if it truly can’t proceed, it should stop cleanly and explain why."
- `[interview_turn:T088]` "For a normal-sized file, I’d expect split or merge to feel near-instant or at least complete within a few seconds, maybe up to ten or fifteen seconds before it starts to feel unusually slow. If it goes beyond that, the tool should show that it’s still working, not freeze, and ideally let the user cancel the job. For longer runs, some visible progress indicator would be important so the user knows it hasn’t stalled."
- `[interview_turn:T090]` "The most useful thing would be a simple progress bar plus the current page or file being processed, and maybe how many pages or outputs are already done out of the total. If there’s an estimated time remaining, that’s helpful too, but not as important as knowing it’s moving. Canceling should still be allowed most of the time, but if the tool is in the middle of writing a single output file, it should handle that carefully so it doesn’t leave a corrupted result."

### [FR-082] (stated)
The system shall warn the user if a normal-sized file takes unusually long to process.

**Source Evidence:**
- `[interview_turn:T014]` "For a typical document, people would expect it to feel quick, basically a few seconds for simple split or merge jobs and not something that makes them wait long enough to lose confidence. I’d be fine with longer processing on bigger scans or batch jobs, as long as the tool shows progress and it’s clear it hasn’t frozen. If it starts taking unusually long on a normal-sized file, it should warn the user rather than just sit there silently, and if it truly can’t proceed, it should stop cleanly and explain why."

### [FR-083] (stated)
The system shall stop cleanly and explain why if it cannot proceed with a job.

**Source Evidence:**
- `[interview_turn:T014]` "For a typical document, people would expect it to feel quick, basically a few seconds for simple split or merge jobs and not something that makes them wait long enough to lose confidence. I’d be fine with longer processing on bigger scans or batch jobs, as long as the tool shows progress and it’s clear it hasn’t frozen. If it starts taking unusually long on a normal-sized file, it should warn the user rather than just sit there silently, and if it truly can’t proceed, it should stop cleanly and explain why."

### [FR-084] (stated)
The system shall display a simple progress bar plus the current page or file being processed during long jobs.

**Source Evidence:**
- `[interview_turn:T090]` "The most useful thing would be a simple progress bar plus the current page or file being processed, and maybe how many pages or outputs are already done out of the total. If there’s an estimated time remaining, that’s helpful too, but not as important as knowing it’s moving. Canceling should still be allowed most of the time, but if the tool is in the middle of writing a single output file, it should handle that carefully so it doesn’t leave a corrupted result."

### [FR-085] (stated)
The system shall allow the user to cancel a running job most of the time.

**Source Evidence:**
- `[interview_turn:T088]` "For a normal-sized file, I’d expect split or merge to feel near-instant or at least complete within a few seconds, maybe up to ten or fifteen seconds before it starts to feel unusually slow. If it goes beyond that, the tool should show that it’s still working, not freeze, and ideally let the user cancel the job. For longer runs, some visible progress indicator would be important so the user knows it hasn’t stalled."
- `[interview_turn:T090]` "The most useful thing would be a simple progress bar plus the current page or file being processed, and maybe how many pages or outputs are already done out of the total. If there’s an estimated time remaining, that’s helpful too, but not as important as knowing it’s moving. Canceling should still be allowed most of the time, but if the tool is in the middle of writing a single output file, it should handle that carefully so it doesn’t leave a corrupted result."

### [FR-086] (stated)
The system shall handle cancellation carefully while writing a single output file so it does not leave a corrupted result.

**Source Evidence:**
- `[interview_turn:T090]` "The most useful thing would be a simple progress bar plus the current page or file being processed, and maybe how many pages or outputs are already done out of the total. If there’s an estimated time remaining, that’s helpful too, but not as important as knowing it’s moving. Canceling should still be allowed most of the time, but if the tool is in the middle of writing a single output file, it should handle that carefully so it doesn’t leave a corrupted result."

### [FR-087] (stated)
The system shall prompt clearly before closing or discarding unsaved changes or open layouts.

**Source Evidence:**
- `[interview_turn:T094]` "On day one, it should definitely support adding PDFs, reordering pages or whole files, removing items, rotating pages, splitting and merging, and visually building a new output from selected sections. I’d also want simple page previewing so the user can verify what they’re assembling before exporting. As for safeguards, it should never change the source files, and it should make it hard to accidentally lose work by prompting before closing or discarding an unsaved layout."
- `[interview_turn:T100]` "If there are unsaved changes, the app should prompt clearly before closing or discarding anything, and if multiple layouts are open it should deal with each one separately so the user knows exactly what will be lost. I’d want it to distinguish between one layout with unsaved edits and several open workspaces, because the warning should be specific rather than generic. If possible, it should let the user save the open layouts that matter and discard only the ones they choose."

### [FR-088] (stated)
The system shall handle multiple open layouts separately when prompting about unsaved changes.

**Source Evidence:**
- `[interview_turn:T100]` "If there are unsaved changes, the app should prompt clearly before closing or discarding anything, and if multiple layouts are open it should deal with each one separately so the user knows exactly what will be lost. I’d want it to distinguish between one layout with unsaved edits and several open workspaces, because the warning should be specific rather than generic. If possible, it should let the user save the open layouts that matter and discard only the ones they choose."

### [FR-089] (conditional)
The system shall let the user save some open layouts and discard only the ones they choose when multiple layouts are open.

**Source Evidence:**
- `[interview_turn:T100]` "If there are unsaved changes, the app should prompt clearly before closing or discarding anything, and if multiple layouts are open it should deal with each one separately so the user knows exactly what will be lost. I’d want it to distinguish between one layout with unsaved edits and several open workspaces, because the warning should be specific rather than generic. If possible, it should let the user save the open layouts that matter and discard only the ones they choose."

### [FR-090] (stated)
The system shall show the user which settings are affected when a saved workflow opens with missing or changed options.

**Source Evidence:**
- `[interview_turn:T078]` "It should open as gracefully as possible and preserve the parts it still understands, rather than refusing to load the whole workflow. If something is missing or changed, it should warn the user clearly, show which setting is affected, and fall back to a sensible default or leave that part disabled until the user fixes it. I’d also expect it to keep the saved file intact so the user can still recover the original configuration if needed."

### [FR-091] (stated)
The system shall fall back to a sensible default or leave a changed setting disabled until the user fixes it.

**Source Evidence:**
- `[interview_turn:T078]` "It should open as gracefully as possible and preserve the parts it still understands, rather than refusing to load the whole workflow. If something is missing or changed, it should warn the user clearly, show which setting is affected, and fall back to a sensible default or leave that part disabled until the user fixes it. I’d also expect it to keep the saved file intact so the user can still recover the original configuration if needed."

### [FR-092] (stated)
The system shall preserve the saved project state so nothing else is lost when a source file cannot be recovered immediately.

**Source Evidence:**
- `[interview_turn:T116]` "It should open the project with the broken source clearly flagged, but keep the rest of the assembly usable so the user can still work on the unaffected parts. Then it should let them relink the missing file, and if it was changed, confirm the page mapping before they export. If they can’t recover it right away, the app should preserve the project state so nothing else is lost."

### [FR-093] (stated)
The system shall support a workspace save format that is a simple project file or profile file rather than a heavy packaged archive.

**Source Evidence:**
- `[interview_turn:T080]` "I’d prefer a simple project file or profile file rather than a heavy packaged archive, because the main need is to restore the workflow state, not necessarily bundle all the PDFs inside it. It should store the document list, page operations, output settings, and any layout or composition choices in a way that’s easy to reload later. If there’s an option to reference files by path and optionally validate they still exist, that would be very useful for recurring work."

### [FR-094] (stated)
The system shall support referencing saved workspace files by path and optionally validating that the files still exist.

**Source Evidence:**
- `[interview_turn:T080]` "I’d prefer a simple project file or profile file rather than a heavy packaged archive, because the main need is to restore the workflow state, not necessarily bundle all the PDFs inside it. It should store the document list, page operations, output settings, and any layout or composition choices in a way that’s easy to reload later. If there’s an option to reference files by path and optionally validate they still exist, that would be very useful for recurring work."

### [FR-095] (stated)
The system shall let users override whether overwriting is allowed on the command line.

**Source Evidence:**
- `[interview_turn:T082]` "The command line should let the user override the inputs, output location, selected pages or ranges, merge versus split behavior, ordering, naming pattern, and whether overwriting is allowed. I’d also want any reusable profile settings to be overrideable at run time, so a script can reuse a base job but change just the few values that matter for that execution. That makes it easier to reproduce runs exactly while still keeping the profile useful for day-to-day automation."

### [FR-096] (stated)
The system shall ensure explicit user values win over defaults unless the resulting combination is invalid.

**Source Evidence:**
- `[interview_turn:T040]` "If a required parameter is missing, the run should fail fast with a clear error message that says what’s missing and how to provide it. If a supplied value conflicts with the default behavior, the explicit user value should win unless it creates an invalid combination, in which case the tool should reject it rather than guessing. For automation, predictable failure is better than silently doing the wrong thing."

### [FR-097] (conditional)
The system shall support predictable default naming conventions for automated or recurring runs, and those defaults may vary by job profile but remain consistent for the same inputs and settings.

**Source Evidence:**
- `[interview_turn:T075]` "For automated or recurring runs, what rules should determine the default output filename or folder when the user doesn’t specify one, and are there any cases where that default should vary by input file, page range, or job profile?"
- `[interview_turn:T076]` "If the user doesn’t specify an output, it should default to a safe, predictable name derived from the input, usually in the same folder or in a clearly defined output folder if that was set in the profile. The filename should reflect the operation in some way, like split, merged, or extracted, and it should avoid overwriting existing files unless the user explicitly allows that. I’d expect the default to vary when the job profile changes, because a reusable profile should carry its own output conventions, but it should stay consistent for the same inputs and settings."

### [FR-098] (stated)
The system shall support script-friendly input of split and merge options from the command line.

**Source Evidence:**
- `[interview_turn:T036]` "Command-line users should be able to define everything through parameters or a saved job profile, without needing the graphical interface at all. They’ll likely want to point to input and output paths directly, pass split and merge options in a script-friendly way, and rely on predictable default naming unless they override it. The main difference is that CLI usage needs to be more explicit and reproducible, since those runs are usually automated or repeated."

### [FR-099] (stated)
The system shall support operation on local desktop machines as a standalone desktop app and in scripts or batch jobs on the user's own machines.

**Source Evidence:**
- `[interview_turn:T066]` "I’d expect it to run on the common desktop platforms, especially Windows, macOS, and Linux, because people use PDF tools in all of those environments. It should be easy to download and install locally, without needing a server or cloud account, and the command-line option should work in the same local setup for automation. In the normal workflow, that means users get it as a standalone desktop app, and they can also use it in scripts or batch jobs on their own machines."

## 4. Business Rules and Constraints

### [BR-001] (stated)
The original PDF files shall remain untouched at all times and shall not be modified in place by default.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Users need a free graphical tool for manipulating PDF documents without altering their original input files. They should be able to split documents, merge selected files or sections, extract pages, rotate or reorder pages, alternate pages from different documents, and compose new documents visually. The tool should also save reusable work environments and offer a command-line path for recurring or automated operations."
- `[interview_turn:T002]` "It’s meant to let people take existing PDFs apart and put them back together again quickly, without needing a full PDF editor. In practice, I’d expect the main users to be office staff, admins, and power users who regularly handle reports, scans, invoices, and similar documents, plus some technical users who want a command-line option for repeat jobs.
The no-modification approach means the original PDFs should stay untouched at all times, so users work on copies or generated output instead of editing the source files directly. That way they can safely experiment with splits, merges, rotations, and page order changes without worrying about damaging the original document."
- `[interview_turn:T008]` "In general, any page that’s in the source PDFs should be available to pull in, reorder, or rotate, as long as the user chooses it. The main rule is that the tool should not change the originals, so all of those actions happen only in the assembled output or in the saved workspace. I’d only expect exceptions for cases like protected or unreadable PDFs, where the tool should either skip them or clearly tell the user it can’t process them."
- `[interview_turn:T064]` "It should always protect the original source files and work on copies or produce new output files instead. The user should never have the original PDFs modified in place by default. If there were ever an advanced mode that works directly on originals, that would need to be very explicit and opt-in, but I’d consider that outside the normal expected behavior."
- `[interview_turn:T072]` "Yes, it should behave consistently across the three platforms, but it needs to respect each system’s path and quoting rules so scripts don’t break on spaces or special characters. I’d expect it to work cleanly from standard shells and batch files without requiring users to learn platform-specific quirks. If there are packaging choices, I’d prefer it to be installable in a way that makes the command available on the PATH and usable from automation right away."
- `[interview_turn:T094]` "On day one, it should definitely support adding PDFs, reordering pages or whole files, removing items, rotating pages, splitting and merging, and visually building a new output from selected sections. I’d also want simple page previewing so the user can verify what they’re assembling before exporting. As for safeguards, it should never change the source files, and it should make it hard to accidentally lose work by prompting before closing or discarding an unsaved layout."
- `[interview_turn:T098]` "It should not edit the source PDF in place at all. The original file should always stay untouched, and any changes should be written only to a new output file or a separate working copy inside the app’s own workspace if it needs one. The only time I’d want a copied file is if the tool needs a temporary internal version to support the editing session, but even then it shouldn’t overwrite the user’s source."

### [BR-002] (stated)
All document processing shall remain local by default and shall not upload files to any remote service.

**Source Evidence:**
- `[interview_turn:T060]` "The tool should promise that files stay local by default and are not uploaded anywhere. Users should be able to expect that only the files they choose to process are accessed, and that temporary data is not left behind longer than necessary. For privacy, I’d want a clear statement that the application doesn’t inspect or share content beyond what’s needed to perform the PDF operations."
- `[interview_turn:T068]` "Yes, I’d expect it to be open source, because “free” in this context should mean users can use it without payment and also trust what it’s doing locally. I don’t have a specific license mandated, but it should be one that’s widely compatible and doesn’t restrict normal desktop or command-line use. I’d also want to avoid dependencies that would complicate redistribution or force any cloud service or proprietary runtime."
- `[interview_turn:T086]` "It should be fully usable offline for local documents, since that’s the safest default and fits the use case. I wouldn’t expect it to need network access for the core PDF operations at all. If there are any optional update checks or help resources, those should be separate and clearly not part of document processing."

### [BR-003] (stated)
Temporary data shall be retained only as long as needed to complete the operation.

**Source Evidence:**
- `[interview_turn:T060]` "The tool should promise that files stay local by default and are not uploaded anywhere. Users should be able to expect that only the files they choose to process are accessed, and that temporary data is not left behind longer than necessary. For privacy, I’d want a clear statement that the application doesn’t inspect or share content beyond what’s needed to perform the PDF operations."
- `[interview_turn:T062]` "Temporary copies should only exist for as long as they’re needed to complete the operation, then be cleaned up automatically. I wouldn’t expect them to be retained longer by default, except maybe if the user explicitly saves a reusable workspace or project state that includes references to the input files and settings. Even then, the actual document content should stay local and not be preserved more than necessary unless the user has clearly chosen that."

### [BR-004] (stated)
If a protected or unreadable PDF is encountered, the tool shall not fail silently.

**Source Evidence:**
- `[interview_turn:T008]` "In general, any page that’s in the source PDFs should be available to pull in, reorder, or rotate, as long as the user chooses it. The main rule is that the tool should not change the originals, so all of those actions happen only in the assembled output or in the saved workspace. I’d only expect exceptions for cases like protected or unreadable PDFs, where the tool should either skip them or clearly tell the user it can’t process them."
- `[interview_turn:T058]` "If a PDF is protected or unreadable, the tool should not fail silently. Ideally it should tell the user exactly which file could not be processed and why, then let them decide whether to skip it, stop, or try again after fixing the issue. For an automated command-line run, I’d expect the behavior to be configurable, but the default should be to stop on serious read errors and warn on protected files if some parts can still be inspected."

### [BR-005] (conditional)
For protected or unreadable PDFs, the default command-line behavior shall stop on serious read errors and warn on protected files if some parts can still be inspected.

**Source Evidence:**
- `[interview_turn:T058]` "If a PDF is protected or unreadable, the tool should not fail silently. Ideally it should tell the user exactly which file could not be processed and why, then let them decide whether to skip it, stop, or try again after fixing the issue. For an automated command-line run, I’d expect the behavior to be configurable, but the default should be to stop on serious read errors and warn on protected files if some parts can still be inspected."

### [BR-006] (stated)
When a command-line run or saved job profile has a conflict between an explicit user value and a default behavior, the explicit user value shall prevail unless it creates an invalid combination.

**Source Evidence:**
- `[interview_turn:T040]` "If a required parameter is missing, the run should fail fast with a clear error message that says what’s missing and how to provide it. If a supplied value conflicts with the default behavior, the explicit user value should win unless it creates an invalid combination, in which case the tool should reject it rather than guessing. For automation, predictable failure is better than silently doing the wrong thing."
- `[interview_turn:T084]` "The structural choices should be locked, like the operation type, the page-processing logic, and any composition layout, because changing those at runtime could make the saved profile meaningless. Things like input files, output path, naming pattern, and overwrite behavior should stay overrideable, since those are the usual differences between runs. If a profile is meant to be reusable, I’d also keep any document-specific page selections flexible unless the profile was created specifically to hard-code them."

### [BR-007] (stated)
If the tool cannot proceed, it shall stop cleanly and explain why.

**Source Evidence:**
- `[interview_turn:T014]` "For a typical document, people would expect it to feel quick, basically a few seconds for simple split or merge jobs and not something that makes them wait long enough to lose confidence. I’d be fine with longer processing on bigger scans or batch jobs, as long as the tool shows progress and it’s clear it hasn’t frozen. If it starts taking unusually long on a normal-sized file, it should warn the user rather than just sit there silently, and if it truly can’t proceed, it should stop cleanly and explain why."

### [BR-008] (stated)
The system shall avoid interleaving when the document mismatch would clearly break the document.

**Source Evidence:**
- `[interview_turn:T056]` "If the mismatch would clearly break the document, like incompatible page sizes or a booklet layout that would lose its structure, the tool should steer the user away immediately. If it’s more of a risk than a hard blocker, then it should still allow the operation but only with a warning and a strong preview so the user can judge the output. The main rule is whether the result is likely to be unusable or just needs careful review."

### [BR-009] (stated)
If a source is repeated more than once in interleaving, that repetition shall be an explicit user choice.

**Source Evidence:**
- `[interview_turn:T048]` "If the documents are different lengths, the tool should keep alternating until one source runs out, then either stop or continue with the remaining pages based on the chosen mode. For missing pages, I’d expect the tool to preserve whatever is available and flag the gap rather than trying to invent a replacement. If one source needs to repeat more than once, that should be an explicit option, because otherwise the result could be surprising and hard to trust."

### [BR-010] (stated)
The system shall preserve intentional repeats exactly as chosen by the user and shall not automatically collapse duplicates if that would change intended order or content.

**Source Evidence:**
- `[interview_turn:T052]` "Intentional repeats should be preserved exactly as they appear in the source, as long as the user has chosen to include that range. The tool shouldn’t automatically collapse duplicates if that would change the intended order or content. If something looks like accidental duplication, I’d rather have it flagged as a possible issue in the preview than have the software decide on its own."

### [BR-011] (stated)
The system shall not bundle components with unclear licensing, non-commercial restrictions, or cloud-service dependencies.

**Source Evidence:**
- `[interview_turn:T070]` "I’d want to avoid anything with strong copyleft obligations that could make redistribution complicated for downstream packagers, unless we deliberately decide that’s acceptable. Also, I’d avoid bundled components with unclear licensing, non-commercial restrictions, or anything that requires users to accept a cloud service dependency. In practice, I’d prefer clearly permissive dependencies and packaging that doesn’t put extra legal burden on people just trying to install and use the tool."

### [BR-012] (stated)
The system shall prefer clearly permissive dependencies and packaging that does not impose extra legal burden on users.

**Source Evidence:**
- `[interview_turn:T070]` "I’d want to avoid anything with strong copyleft obligations that could make redistribution complicated for downstream packagers, unless we deliberately decide that’s acceptable. Also, I’d avoid bundled components with unclear licensing, non-commercial restrictions, or anything that requires users to accept a cloud service dependency. In practice, I’d prefer clearly permissive dependencies and packaging that doesn’t put extra legal burden on people just trying to install and use the tool."

## 5. Data and External Interfaces

### [DI-001] (stated)
The command-line interface shall accept multiple input files, explicit page ranges, output paths, and options.

**Source Evidence:**
- `[interview_turn:T074]` "It should handle multiple input files, explicit page ranges, output paths, and options in a very predictable way, with clear quoting support for paths that contain spaces. If an argument is missing, malformed, or points to a file that doesn’t exist, it should fail fast with a clear error code and message rather than guessing. For automation, I’d also want it to be stable about option names and ordering so scripts behave the same across runs and platforms."

### [DI-002] (stated)
The command-line interface shall support command availability on the PATH.

**Source Evidence:**
- `[interview_turn:T072]` "Yes, it should behave consistently across the three platforms, but it needs to respect each system’s path and quoting rules so scripts don’t break on spaces or special characters. I’d expect it to work cleanly from standard shells and batch files without requiring users to learn platform-specific quirks. If there are packaging choices, I’d prefer it to be installable in a way that makes the command available on the PATH and usable from automation right away."

### [DI-003] (stated)
The command-line interface shall behave consistently across Windows, macOS, and Linux while respecting each platform's path and quoting rules.

**Source Evidence:**
- `[interview_turn:T072]` "Yes, it should behave consistently across the three platforms, but it needs to respect each system’s path and quoting rules so scripts don’t break on spaces or special characters. I’d expect it to work cleanly from standard shells and batch files without requiring users to learn platform-specific quirks. If there are packaging choices, I’d prefer it to be installable in a way that makes the command available on the PATH and usable from automation right away."
- `[interview_turn:T074]` "It should handle multiple input files, explicit page ranges, output paths, and options in a very predictable way, with clear quoting support for paths that contain spaces. If an argument is missing, malformed, or points to a file that doesn’t exist, it should fail fast with a clear error code and message rather than guessing. For automation, I’d also want it to be stable about option names and ordering so scripts behave the same across runs and platforms."

### [DI-004] (stated)
The saved workspace shall store document lists, page operations, output settings, and layout or composition choices for later reloading.

**Source Evidence:**
- `[interview_turn:T080]` "I’d prefer a simple project file or profile file rather than a heavy packaged archive, because the main need is to restore the workflow state, not necessarily bundle all the PDFs inside it. It should store the document list, page operations, output settings, and any layout or composition choices in a way that’s easy to reload later. If there’s an option to reference files by path and optionally validate they still exist, that would be very useful for recurring work."

### [DI-005] (stated)
The saved project shall store file references as paths and may validate whether referenced files still exist.

**Source Evidence:**
- `[interview_turn:T080]` "I’d prefer a simple project file or profile file rather than a heavy packaged archive, because the main need is to restore the workflow state, not necessarily bundle all the PDFs inside it. It should store the document list, page operations, output settings, and any layout or composition choices in a way that’s easy to reload later. If there’s an option to reference files by path and optionally validate they still exist, that would be very useful for recurring work."
- `[interview_turn:T112]` "It should preserve the full workspace state: the selected source files, page ranges, order, rotations, repetitions, merge settings, and any other layout choices needed to reopen the job exactly as it was. Yes, it should keep file references as paths, and ideally also store enough metadata to detect when a source has moved, changed, or gone missing so the user gets a clear warning on reopen. If a source can’t be found, the project should still open with that item marked as broken and ready to relink."

### [DI-006] (stated)
The preview shall support a side-by-side or thumbnail comparison when a source file has been relinked after replacement.

**Source Evidence:**
- `[interview_turn:T106]` "It should prompt the user to relink the item, then show a side-by-side or at least page-thumbnail comparison so they can confirm they’re still using the right content. If the replacement version has different page counts or changed page order, the app should warn them before export and let them adjust the selection. I’d want that check to happen inside the workspace, not only at the final save step."

## 6. Quality Requirements

### [QR-001] (stated)
A typical split or merge job for a normal-sized file should feel near-instant or complete within a few seconds, and should not generally exceed about ten to fifteen seconds before being considered unusually slow.

**Source Evidence:**
- `[interview_turn:T014]` "For a typical document, people would expect it to feel quick, basically a few seconds for simple split or merge jobs and not something that makes them wait long enough to lose confidence. I’d be fine with longer processing on bigger scans or batch jobs, as long as the tool shows progress and it’s clear it hasn’t frozen. If it starts taking unusually long on a normal-sized file, it should warn the user rather than just sit there silently, and if it truly can’t proceed, it should stop cleanly and explain why."
- `[interview_turn:T088]` "For a normal-sized file, I’d expect split or merge to feel near-instant or at least complete within a few seconds, maybe up to ten or fifteen seconds before it starts to feel unusually slow. If it goes beyond that, the tool should show that it’s still working, not freeze, and ideally let the user cancel the job. For longer runs, some visible progress indicator would be important so the user knows it hasn’t stalled."

### [QR-002] (stated)
The system shall show visible progress for longer runs so the user knows the operation has not stalled.

**Source Evidence:**
- `[interview_turn:T014]` "For a typical document, people would expect it to feel quick, basically a few seconds for simple split or merge jobs and not something that makes them wait long enough to lose confidence. I’d be fine with longer processing on bigger scans or batch jobs, as long as the tool shows progress and it’s clear it hasn’t frozen. If it starts taking unusually long on a normal-sized file, it should warn the user rather than just sit there silently, and if it truly can’t proceed, it should stop cleanly and explain why."
- `[interview_turn:T088]` "For a normal-sized file, I’d expect split or merge to feel near-instant or at least complete within a few seconds, maybe up to ten or fifteen seconds before it starts to feel unusually slow. If it goes beyond that, the tool should show that it’s still working, not freeze, and ideally let the user cancel the job. For longer runs, some visible progress indicator would be important so the user knows it hasn’t stalled."
- `[interview_turn:T090]` "The most useful thing would be a simple progress bar plus the current page or file being processed, and maybe how many pages or outputs are already done out of the total. If there’s an estimated time remaining, that’s helpful too, but not as important as knowing it’s moving. Canceling should still be allowed most of the time, but if the tool is in the middle of writing a single output file, it should handle that carefully so it doesn’t leave a corrupted result."

### [QR-003] (stated)
The system shall be reasonably capable of handling occasional larger scans or combined documents.

**Source Evidence:**
- `[interview_turn:T012]` "Most of the time I’d expect fairly modest documents, maybe anywhere from a few pages up to a few hundred pages, like reports, forms, or scanned packets. File sizes would usually be in the small-to-medium range, but there will be occasional larger scans or combined documents that are much heavier. The tool doesn’t need to be specialized only for huge files, but it should still cope reasonably well when people do run into them."

### [QR-004] (stated)
The system shall support visual verification of page order, included or omitted pages, rotations, margins, alignment, and text clarity where visually accuracy matters.

**Source Evidence:**
- `[interview_turn:T016]` "The preview should let them confirm page order, which pages are included or left out, and whether any pages need rotation or rearrangement before saving. In day-to-day use, that’s usually enough to catch mistakes like a missing section or an upside-down page. A quick preview may not be enough for very detailed work, like scanned pages with tiny text or documents where exact layout and margins really matter, because people may need to zoom in or inspect those more carefully."
- `[interview_turn:T018]` "It should at least support zooming in and stepping through pages one by one so people can inspect individual pages closely before they commit. Margin checks and text clarity matter mostly for scanned or packed documents, so if the tool can show the page at a good resolution and let the user verify those visually, that would be enough. I don’t think it needs full editing features for that stage, just a reliable way to inspect what will actually be saved."
- `[interview_turn:T044]` "The preview should support zooming and opening a page in a larger view so users can inspect fine detail, and it should be good enough to check margins, alignment, and whether a rotated page really looks right. I wouldn’t make deeper inspection mandatory in every case, but it should be available for scanned documents, forms, or anything where visual accuracy matters more. In those cases, it’s especially important because a page can look fine in thumbnail view and still be wrong when printed or archived."

### [QR-005] (stated)
The system shall provide enough resolution for visual inspection of scanned documents, forms, or layout-sensitive pages.

**Source Evidence:**
- `[interview_turn:T018]` "It should at least support zooming in and stepping through pages one by one so people can inspect individual pages closely before they commit. Margin checks and text clarity matter mostly for scanned or packed documents, so if the tool can show the page at a good resolution and let the user verify those visually, that would be enough. I don’t think it needs full editing features for that stage, just a reliable way to inspect what will actually be saved."
- `[interview_turn:T044]` "The preview should support zooming and opening a page in a larger view so users can inspect fine detail, and it should be good enough to check margins, alignment, and whether a rotated page really looks right. I wouldn’t make deeper inspection mandatory in every case, but it should be available for scanned documents, forms, or anything where visual accuracy matters more. In those cases, it’s especially important because a page can look fine in thumbnail view and still be wrong when printed or archived."

### [QR-006] (stated)
The system shall make assembly easy to verify before saving so users can trust the final document without repeated correction cycles.

**Source Evidence:**
- `[interview_turn:T006]` "A successful result is that they can visually build the final PDF with the pages in the right order, the right sections included, and no surprises compared to what they saw while assembling it. In day-to-day work, that usually means quickly combining separate files, pulling selected pages from a larger document, and rearranging or rotating pages until the output matches the intended packet or report. The most important part is making that assembly process easy to verify before saving, so they can trust the final document without having to open and fix it multiple times."

### [QR-007] (stated)
The system shall remain usable and predictable for automated or repeatable runs.

**Source Evidence:**
- `[interview_turn:T036]` "Command-line users should be able to define everything through parameters or a saved job profile, without needing the graphical interface at all. They’ll likely want to point to input and output paths directly, pass split and merge options in a script-friendly way, and rely on predictable default naming unless they override it. The main difference is that CLI usage needs to be more explicit and reproducible, since those runs are usually automated or repeated."
- `[interview_turn:T040]` "If a required parameter is missing, the run should fail fast with a clear error message that says what’s missing and how to provide it. If a supplied value conflicts with the default behavior, the explicit user value should win unless it creates an invalid combination, in which case the tool should reject it rather than guessing. For automation, predictable failure is better than silently doing the wrong thing."
- `[interview_turn:T074]` "It should handle multiple input files, explicit page ranges, output paths, and options in a very predictable way, with clear quoting support for paths that contain spaces. If an argument is missing, malformed, or points to a file that doesn’t exist, it should fail fast with a clear error code and message rather than guessing. For automation, I’d also want it to be stable about option names and ordering so scripts behave the same across runs and platforms."

### [QR-008] (stated)
The system shall behave predictably and safely so users do not accidentally replace a source file or a previously generated PDF.

**Source Evidence:**
- `[interview_turn:T010]` "By default, I’d expect the user to choose the save location and name, with the tool remembering the last folder they used to make it easier next time. If they’re creating multiple versions or running a batch, the tool should help avoid overwriting by either prompting, auto-numbering, or using a naming pattern from the saved workspace or command line setup. The main rule is that it should be predictable and safe, so people don’t accidentally replace a source or a previously generated PDF."

### [QR-009] (stated)
The system shall not lose work unexpectedly and shall prompt before discarding unsaved layouts.

**Source Evidence:**
- `[interview_turn:T094]` "On day one, it should definitely support adding PDFs, reordering pages or whole files, removing items, rotating pages, splitting and merging, and visually building a new output from selected sections. I’d also want simple page previewing so the user can verify what they’re assembling before exporting. As for safeguards, it should never change the source files, and it should make it hard to accidentally lose work by prompting before closing or discarding an unsaved layout."
- `[interview_turn:T100]` "If there are unsaved changes, the app should prompt clearly before closing or discarding anything, and if multiple layouts are open it should deal with each one separately so the user knows exactly what will be lost. I’d want it to distinguish between one layout with unsaved edits and several open workspaces, because the warning should be specific rather than generic. If possible, it should let the user save the open layouts that matter and discard only the ones they choose."

### [QR-010] (stated)
The system shall keep scripts stable across runs and platforms by maintaining consistent option names and ordering.

**Source Evidence:**
- `[interview_turn:T074]` "It should handle multiple input files, explicit page ranges, output paths, and options in a very predictable way, with clear quoting support for paths that contain spaces. If an argument is missing, malformed, or points to a file that doesn’t exist, it should fail fast with a clear error code and message rather than guessing. For automation, I’d also want it to be stable about option names and ordering so scripts behave the same across runs and platforms."

### [QR-011] (stated)
The system shall support a clear progress indicator during longer operations, including the current page or file and the number of pages or outputs completed out of the total.

**Source Evidence:**
- `[interview_turn:T090]` "The most useful thing would be a simple progress bar plus the current page or file being processed, and maybe how many pages or outputs are already done out of the total. If there’s an estimated time remaining, that’s helpful too, but not as important as knowing it’s moving. Canceling should still be allowed most of the time, but if the tool is in the middle of writing a single output file, it should handle that carefully so it doesn’t leave a corrupted result."

## 7. Exceptions and Boundary Conditions

### [EX-001] (conditional)
Protected or unreadable PDFs may be skipped or reported as unprocessable, depending on user choice or command-line configuration.

**Source Evidence:**
- `[interview_turn:T008]` "In general, any page that’s in the source PDFs should be available to pull in, reorder, or rotate, as long as the user chooses it. The main rule is that the tool should not change the originals, so all of those actions happen only in the assembled output or in the saved workspace. I’d only expect exceptions for cases like protected or unreadable PDFs, where the tool should either skip them or clearly tell the user it can’t process them."
- `[interview_turn:T058]` "If a PDF is protected or unreadable, the tool should not fail silently. Ideally it should tell the user exactly which file could not be processed and why, then let them decide whether to skip it, stop, or try again after fixing the issue. For an automated command-line run, I’d expect the behavior to be configurable, but the default should be to stop on serious read errors and warn on protected files if some parts can still be inspected."

### [EX-002] (stated)
The system shall stop automatically if a required command-line input or other required parameter is missing.

**Source Evidence:**
- `[interview_turn:T040]` "If a required parameter is missing, the run should fail fast with a clear error message that says what’s missing and how to provide it. If a supplied value conflicts with the default behavior, the explicit user value should win unless it creates an invalid combination, in which case the tool should reject it rather than guessing. For automation, predictable failure is better than silently doing the wrong thing."
- `[interview_turn:T074]` "It should handle multiple input files, explicit page ranges, output paths, and options in a very predictable way, with clear quoting support for paths that contain spaces. If an argument is missing, malformed, or points to a file that doesn’t exist, it should fail fast with a clear error code and message rather than guessing. For automation, I’d also want it to be stable about option names and ordering so scripts behave the same across runs and platforms."

### [EX-003] (stated)
The system shall reject malformed arguments or arguments that point to non-existent files on the command line.

**Source Evidence:**
- `[interview_turn:T074]` "It should handle multiple input files, explicit page ranges, output paths, and options in a very predictable way, with clear quoting support for paths that contain spaces. If an argument is missing, malformed, or points to a file that doesn’t exist, it should fail fast with a clear error code and message rather than guessing. For automation, I’d also want it to be stable about option names and ordering so scripts behave the same across runs and platforms."

### [EX-004] (stated)
If a split or merge job runs unusually long on a normal-sized file, the system shall warn the user instead of remaining silent.

**Source Evidence:**
- `[interview_turn:T014]` "For a typical document, people would expect it to feel quick, basically a few seconds for simple split or merge jobs and not something that makes them wait long enough to lose confidence. I’d be fine with longer processing on bigger scans or batch jobs, as long as the tool shows progress and it’s clear it hasn’t frozen. If it starts taking unusually long on a normal-sized file, it should warn the user rather than just sit there silently, and if it truly can’t proceed, it should stop cleanly and explain why."

### [EX-005] (stated)
If a cancellation occurs while writing a single output file, the system shall handle the interruption carefully to avoid a corrupted result.

**Source Evidence:**
- `[interview_turn:T090]` "The most useful thing would be a simple progress bar plus the current page or file being processed, and maybe how many pages or outputs are already done out of the total. If there’s an estimated time remaining, that’s helpful too, but not as important as knowing it’s moving. Canceling should still be allowed most of the time, but if the tool is in the middle of writing a single output file, it should handle that carefully so it doesn’t leave a corrupted result."

### [EX-006] (stated)
When a saved workflow includes an option or output setting that is no longer available or has changed, the system shall preserve the rest of the workflow and disable or default the affected part until the user fixes it.

**Source Evidence:**
- `[interview_turn:T078]` "It should open as gracefully as possible and preserve the parts it still understands, rather than refusing to load the whole workflow. If something is missing or changed, it should warn the user clearly, show which setting is affected, and fall back to a sensible default or leave that part disabled until the user fixes it. I’d also expect it to keep the saved file intact so the user can still recover the original configuration if needed."

### [EX-007] (stated)
If source documents differ in page sizes or have booklet-like structures that would clearly break interleaving, the system shall steer the user to a different workflow rather than proceeding normally.

**Source Evidence:**
- `[interview_turn:T054]` "Yes, in some cases it should avoid interleaving and steer the user toward a different workflow. I’d expect that for documents with very different page sizes, mixed orientations that would make the result messy, or forms and booklets where page position matters structurally rather than just visually. If the pages depend on internal relationships like spreads or sectioning, keeping them separate or merging them in a more controlled way is safer."
- `[interview_turn:T056]` "If the mismatch would clearly break the document, like incompatible page sizes or a booklet layout that would lose its structure, the tool should steer the user away immediately. If it’s more of a risk than a hard blocker, then it should still allow the operation but only with a warning and a strong preview so the user can judge the output. The main rule is whether the result is likely to be unusable or just needs careful review."

### [EX-008] (stated)
If a source file is missing, changed, or unreadable in a saved project, the system shall mark it broken and allow the user to relink it before export.

**Source Evidence:**
- `[interview_turn:T102]` "If a source item is missing or unreadable, the app should stop that item from being included and clearly tell the user before the final output is created, rather than silently skipping it. If something was already added to an assembly and later needs to be edited again, I’d want the assembly to keep the reference to the source or at least keep enough information to let the user replace or reselect it easily. The important part is that the user can see what’s broken and fix it before exporting, instead of discovering it afterward."
- `[interview_turn:T112]` "It should preserve the full workspace state: the selected source files, page ranges, order, rotations, repetitions, merge settings, and any other layout choices needed to reopen the job exactly as it was. Yes, it should keep file references as paths, and ideally also store enough metadata to detect when a source has moved, changed, or gone missing so the user gets a clear warning on reopen. If a source can’t be found, the project should still open with that item marked as broken and ready to relink."
- `[interview_turn:T116]` "It should open the project with the broken source clearly flagged, but keep the rest of the assembly usable so the user can still work on the unaffected parts. Then it should let them relink the missing file, and if it was changed, confirm the page mapping before they export. If they can’t recover it right away, the app should preserve the project state so nothing else is lost."

### [EX-009] (stated)
If a source file has been replaced with a different version, the system shall warn the user when page counts or page order have changed and let the user adjust the selection before export.

**Source Evidence:**
- `[interview_turn:T106]` "It should prompt the user to relink the item, then show a side-by-side or at least page-thumbnail comparison so they can confirm they’re still using the right content. If the replacement version has different page counts or changed page order, the app should warn them before export and let them adjust the selection. I’d want that check to happen inside the workspace, not only at the final save step."

### [EX-010] (stated)
If a source file cannot be processed, the system shall tell the user exactly which file failed and why.

**Source Evidence:**
- `[interview_turn:T058]` "If a PDF is protected or unreadable, the tool should not fail silently. Ideally it should tell the user exactly which file could not be processed and why, then let them decide whether to skip it, stop, or try again after fixing the issue. For an automated command-line run, I’d expect the behavior to be configurable, but the default should be to stop on serious read errors and warn on protected files if some parts can still be inspected."

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
The primary user groups for the command-line workflow are tentative and not yet confirmed in final scope.

**Source Evidence:**
- `[interview_turn:T038]` "Let’s record it as tentative for the moment. I can say it’s mainly for power users, admins, and automation scripts, but I don’t want to overstate exact user groups until we confirm who will actually adopt it most."

### [UN-002]
The exact usage frequency for recurring editing sessions has not been defined and remains open for later quantification.

**Source Evidence:**
- `[interview_turn:T026]` "We can leave it as an open assumption for now. I’m comfortable saying there will be a recurring group of users who do similar jobs often enough that saving setups and presets matters, but I don’t think we need to pin down exact frequency yet. If we need it later for prioritization or performance decisions, we can come back and quantify it."

### [UN-003]
The tool's support for arbitrary rotation angles is not decided, and only fixed 90-degree steps are confirmed for now.

**Source Evidence:**
- `[interview_turn:T022]` "For this tool, fixed increments are enough, mainly 90-degree steps for left or right rotation. That covers the common use case of correcting scanned pages or aligning documents, and it keeps the workflow simple and predictable. I don’t see a need for arbitrary angles unless we later find a niche use case that really depends on that."

### [UN-004]
Optional update checks or help resources are not yet specified as part of the core document-processing workflow.

**Source Evidence:**
- `[interview_turn:T086]` "It should be fully usable offline for local documents, since that’s the safest default and fits the use case. I wouldn’t expect it to need network access for the core PDF operations at all. If there are any optional update checks or help resources, those should be separate and clearly not part of document processing."

### [UN-005]
The exact license choice for the open-source distribution has not been selected.

**Source Evidence:**
- `[interview_turn:T068]` "Yes, I’d expect it to be open source, because “free” in this context should mean users can use it without payment and also trust what it’s doing locally. I don’t have a specific license mandated, but it should be one that’s widely compatible and doesn’t restrict normal desktop or command-line use. I’d also want to avoid dependencies that would complicate redistribution or force any cloud service or proprietary runtime."

### [UN-006]
Whether the minimum viable release includes a fully polished command-line scope or a lighter first version remains open.

**Source Evidence:**
- `[interview_turn:T092]` "For the minimum viable release, I’d want both included, but the graphical workflow should be the primary focus and the command-line automation can be a lighter first version. The GUI is the core user-facing value, while the command line is important for recurring tasks and scripting, so I wouldn’t want to leave it out entirely. If we have to phase anything, I’d rather reduce the breadth of advanced CLI options before removing CLI support altogether."
- `[interview_turn:T096]` "I’d keep the command-line scope tentative for the moment, but with the expectation that it will be included in some form. That gives us room to trim the first version if we need to without blocking the release on a fully polished CLI. The GUI should stay locked in now, since that’s the main experience."
