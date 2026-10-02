# Implementation task: PDF Split and Merge

The requirements below were elicited in an interview and reviewed before delivery.

## Reviewed requirements

# Software Requirements Specification: PDF Split and Merge

## 1. Scope and Context

### [SC-001]
The system is a free graphical tool for manipulating PDF documents without altering the original input files.

## 2. Actors

None specified.

## 3. Functional Requirements

### [FR-001]
The system shall support splitting PDF documents.

### [FR-002]
The system shall support merging selected files or sections into a new PDF.

### [FR-003]
The system shall support extracting pages from PDF documents.

### [FR-004]
The system shall support rotating pages in 90-degree left or right steps.

### [FR-005]
The system shall support reordering pages.

### [FR-006]
The system shall support alternating pages from different documents.

### [FR-007]
The system shall support visually composing new PDF documents from selected pages and sections.

### [FR-008]
The system shall allow users to preview assembled or split results before saving or exporting.

### [FR-010]
The system shall allow users to add PDFs, remove items, and reorder pages or whole files in the graphical workflow.

### [FR-011]
The system shall provide a visual composition preview that shows the final page sequence page by page before saving.

### [FR-012]
The system shall show which source file each page came from in the composition preview.

### [FR-013]
The system shall show which pages are included or left out in preview.

### [FR-014]
The system shall allow users to rearrange or remove items directly in the preview before saving.

### [FR-015]
The system shall support zooming in on pages during preview or inspection.

### [FR-016]
The system shall support stepping through pages one by one during inspection.

### [FR-017]
The system shall support opening a page in a larger view for closer inspection.

### [FR-018]
The system shall support page-range based splitting, including splitting after certain pages and extracting specific sections into separate files.

### [FR-019]
The system shall allow users to adjust split boundaries in the preview before creating output.

### [FR-020]
The system shall support previewing the resulting split output documents in the order they will be created, with clear page ranges and included pages for each file.

### [FR-021]
The system shall support visually building a new output from selected sections while preserving the intended order before export.

### [FR-022]
The system shall support alternating page sequences from multiple source documents according to a user-chosen pattern.

### [FR-023]
The system shall keep the original order within each source document during interleaving.

### [FR-024]
The system shall continue alternating pages until one source runs out, then follow the chosen mode to stop or continue with the remaining pages.

### [FR-025]
The system shall preserve available pages and flag gaps when a source page is missing during interleaving.

### [FR-026]
The system shall allow an explicit option for a source to repeat more than once during interleaving or assembly.

### [FR-027]
The system shall flag mismatches or possible accidental duplication in the preview instead of automatically correcting them.

### [FR-028]
The system shall steer users away from interleaving when incompatible page sizes or booklet-like layouts would clearly break the document.

### [FR-029]
The system shall allow a controlled interleaving or merge with warning and strong preview when the mismatch is a risk rather than a hard blocker.

### [FR-030]
The system shall let users load source documents and preview the resulting page sequence before saving when alternating pages.

### [FR-031]
The system shall allow users to confirm page order, included sections, and rotations in a preview before saving the final PDF.

### [FR-032]
The system shall allow users to perform split-related corrections, such as adjusting a wrong boundary or restoring an omitted page, directly in the split preview.

### [FR-033]
The system shall allow users to relink a missing, moved, renamed, or replaced source file before export.

### [FR-034]
The system shall let users browse for a new file when a source item needs to be relinked.

### [FR-035]
The system shall keep the assembly usable for unaffected parts when a saved project is reopened and one source file is broken.

### [FR-036]
The system shall let users remap affected pages, reorder them, or remove and re-add a problematic section after a relinked file has changed page count or page order.

### [FR-037]
The system shall preserve each repeated instance as independently editable in the workspace.

### [FR-038]
The system shall let users change just one repeated instance's position, rotation, or inclusion without forcing the same change on every repetition.

### [FR-039]
The system shall make broken links obvious in the workspace.

### [FR-040]
The system shall preserve source references or enough information to let the user replace or reselect an item that was already added to an assembly.

### [FR-041]
The system shall allow users to choose exactly which pages repeat and how many times they repeat in the assembly.

### [FR-042]
The system shall let users visually duplicate a page or page range and adjust the sequence in the workspace before export.

### [FR-043]
The system shall allow users to save reusable workspaces or project files for later restoration.

### [FR-044]
The system shall restore the full working context from a saved workspace as much as possible, including layout, file selections, page order, split or merge structure, page ranges, rotations, repetitions, merge settings, and other layout choices.

### [FR-045]
The system shall restore document list and output settings from a saved workspace or project file.

### [FR-046]
The system shall keep file references as paths and detect when a source has moved, changed, or gone missing when reopening a saved project.

### [FR-047]
The system shall warn the user clearly when a saved workflow includes a missing, changed, or unavailable setting or source, and preserve the saved file intact.

### [FR-048]
The system shall open a saved project with broken sources marked as broken and ready to relink.

### [FR-049]
The system shall allow users to save the final output to a user-chosen location and name by default.

### [FR-050]
The system shall remember the last folder used for saving.

### [FR-051]
The system shall help avoid overwriting existing files by prompting, auto-numbering, or using a naming pattern when creating multiple versions or running batch jobs.

### [FR-052]
The system shall use a sensible default naming pattern for multiple split outputs based on the original file name and split sequence.

### [FR-053]
The system shall allow users to rename split outputs manually.

### [FR-054]
The system shall derive a safe, predictable default output name from the input when the user does not specify an output.

### [FR-055]
The system shall place the default output in the same folder as the input or in a clearly defined output folder if one was set in the profile.

### [FR-056]
The system shall reflect the operation type in the default output filename, such as split, merged, or extracted.

### [FR-057]
The system shall support command-line operation without requiring the graphical interface.

### [FR-058]
The system shall allow command-line users to define inputs, output paths, split and merge options, selected pages or ranges, ordering, naming pattern, and overwrite behavior through parameters or a saved job profile.

### [FR-059]
The system shall allow reusable profile settings to be overridden at runtime from the command line.

### [FR-060]
The system shall fail fast with a clear error message when a required command-line or job-profile parameter is missing.

### [FR-061]
The system shall reject invalid combinations when an explicit command-line value conflicts with a default behavior.

### [FR-062]
The system shall keep command-line behavior explicit and reproducible for recurring or automated operations.

### [FR-063]
The system shall provide command-line runs with stable option names and ordering so scripts behave the same across runs and platforms.

### [FR-064]
The system shall handle multiple input files, explicit page ranges, output paths, and options predictably on the command line.

### [FR-065]
The system shall support quoting of command-line paths that contain spaces.

### [FR-066]
The system shall be usable from standard shells and batch files on Windows, macOS, and Linux.

### [FR-067]
The system shall be installable so that the command is available on the PATH.

### [FR-068]
The system shall support offline operation for local documents.

### [FR-069]
The system shall not require network access for core PDF operations.

### [FR-070]
The system shall keep files local by default and not upload them anywhere.

### [FR-071]
The system shall clean up temporary copies automatically when they are no longer needed to complete the operation.

### [FR-072]
The system shall prevent source PDFs from being modified in place by default and shall write changes only to new output files or separate working copies.

### [FR-073]
The system shall not edit the source PDF in place at all.

### [FR-074]
The system shall allow an advanced mode that works directly on originals only if it is explicit and opt-in.

### [FR-075]
The system shall run on Windows, macOS, and Linux.

### [FR-076]
The system shall be easy to download and install locally without needing a server or cloud account.

### [FR-077]
The system shall be open source.

### [FR-078]
The system shall avoid dependencies or bundled components that force a cloud service dependency.

### [FR-079]
The system shall avoid bundled components with unclear licensing or non-commercial restrictions.

### [FR-080]
The system shall provide a clear statement that it does not inspect or share content beyond what is needed to perform PDF operations.

### [FR-081]
The system shall show progress for longer-running operations and allow the user to know the job has not stalled.

### [FR-082]
The system shall warn the user if a normal-sized file takes unusually long to process.

### [FR-083]
The system shall stop cleanly and explain why if it cannot proceed with a job.

### [FR-084]
The system shall display a simple progress bar plus the current page or file being processed during long jobs.

### [FR-085]
The system shall allow the user to cancel a running job most of the time.

### [FR-086]
The system shall handle cancellation carefully while writing a single output file so it does not leave a corrupted result.

### [FR-087]
The system shall prompt clearly before closing or discarding unsaved changes or open layouts.

### [FR-088]
The system shall handle multiple open layouts separately when prompting about unsaved changes.

### [FR-089]
The system shall let the user save some open layouts and discard only the ones they choose when multiple layouts are open.

### [FR-090]
The system shall show the user which settings are affected when a saved workflow opens with missing or changed options.

### [FR-091]
The system shall fall back to a sensible default or leave a changed setting disabled until the user fixes it.

### [FR-092]
The system shall preserve the saved project state so nothing else is lost when a source file cannot be recovered immediately.

### [FR-093]
The system shall support a workspace save format that is a simple project file or profile file rather than a heavy packaged archive.

### [FR-094]
The system shall support referencing saved workspace files by path and optionally validating that the files still exist.

### [FR-095]
The system shall let users override whether overwriting is allowed on the command line.

### [FR-096]
The system shall ensure explicit user values win over defaults unless the resulting combination is invalid.

### [FR-097]
The system shall support predictable default naming conventions for automated or recurring runs, and those defaults may vary by job profile but remain consistent for the same inputs and settings.

### [FR-098]
The system shall support script-friendly input of split and merge options from the command line.

### [FR-099]
The system shall support operation on local desktop machines as a standalone desktop app and in scripts or batch jobs on the user's own machines.

## 4. Business Rules and Constraints

### [BR-001]
The original PDF files shall remain untouched at all times and shall not be modified in place by default.

### [BR-002]
All document processing shall remain local by default and shall not upload files to any remote service.

### [BR-003]
Temporary data shall be retained only as long as needed to complete the operation.

### [BR-004]
If a protected or unreadable PDF is encountered, the tool shall not fail silently.

### [BR-005]
For protected or unreadable PDFs, the default command-line behavior shall stop on serious read errors and warn on protected files if some parts can still be inspected.

### [BR-006]
When a command-line run or saved job profile has a conflict between an explicit user value and a default behavior, the explicit user value shall prevail unless it creates an invalid combination.

### [BR-007]
If the tool cannot proceed, it shall stop cleanly and explain why.

### [BR-008]
The system shall avoid interleaving when the document mismatch would clearly break the document.

### [BR-009]
If a source is repeated more than once in interleaving, that repetition shall be an explicit user choice.

### [BR-010]
The system shall preserve intentional repeats exactly as chosen by the user and shall not automatically collapse duplicates if that would change intended order or content.

### [BR-011]
The system shall not bundle components with unclear licensing, non-commercial restrictions, or cloud-service dependencies.

### [BR-012]
The system shall prefer clearly permissive dependencies and packaging that does not impose extra legal burden on users.

## 5. Data and External Interfaces

### [DI-001]
The command-line interface shall accept multiple input files, explicit page ranges, output paths, and options.

### [DI-002]
The command-line interface shall support command availability on the PATH.

### [DI-003]
The command-line interface shall behave consistently across Windows, macOS, and Linux while respecting each platform's path and quoting rules.

### [DI-004]
The saved workspace shall store document lists, page operations, output settings, and layout or composition choices for later reloading.

### [DI-005]
The saved project shall store file references as paths and may validate whether referenced files still exist.

### [DI-006]
The preview shall support a side-by-side or thumbnail comparison when a source file has been relinked after replacement.

## 6. Quality Requirements

### [FR-009]
The system shall allow users to make lightweight adjustments during preview, including rotating, rearranging, or removing items, when those changes are obvious during review.

### [QR-001]
A typical split or merge job for a normal-sized file should feel near-instant or complete within a few seconds, and should not generally exceed about ten to fifteen seconds before being considered unusually slow.

### [QR-002]
The system shall show visible progress for longer runs so the user knows the operation has not stalled.

### [QR-003]
The system shall be reasonably capable of handling occasional larger scans or combined documents.

### [QR-004]
The system shall support visual verification of page order, included or omitted pages, rotations, margins, alignment, and text clarity where visually accuracy matters.

### [QR-005]
The system shall provide enough resolution for visual inspection of scanned documents, forms, or layout-sensitive pages.

### [QR-006]
The system shall make assembly easy to verify before saving so users can trust the final document without repeated correction cycles.

### [QR-007]
The system shall remain usable and predictable for automated or repeatable runs.

### [QR-008]
The system shall behave predictably and safely so users do not accidentally replace a source file or a previously generated PDF.

### [QR-009]
The system shall not lose work unexpectedly and shall prompt before discarding unsaved layouts.

### [QR-010]
The system shall keep scripts stable across runs and platforms by maintaining consistent option names and ordering.

### [QR-011]
The system shall support a clear progress indicator during longer operations, including the current page or file and the number of pages or outputs completed out of the total.

## 7. Exceptions and Boundary Conditions

### [EX-001]
Protected or unreadable PDFs may be skipped or reported as unprocessable, depending on user choice or command-line configuration.

### [EX-002]
The system shall stop automatically if a required command-line input or other required parameter is missing.

### [EX-003]
The system shall reject malformed arguments or arguments that point to non-existent files on the command line.

### [EX-004]
If a split or merge job runs unusually long on a normal-sized file, the system shall warn the user instead of remaining silent.

### [EX-005]
If a cancellation occurs while writing a single output file, the system shall handle the interruption carefully to avoid a corrupted result.

### [EX-006]
When a saved workflow includes an option or output setting that is no longer available or has changed, the system shall preserve the rest of the workflow and disable or default the affected part until the user fixes it.

### [EX-007]
If source documents differ in page sizes or have booklet-like structures that would clearly break interleaving, the system shall steer the user to a different workflow rather than proceeding normally.

### [EX-008]
If a source file is missing, changed, or unreadable in a saved project, the system shall mark it broken and allow the user to relink it before export.

### [EX-009]
If a source file has been replaced with a different version, the system shall warn the user when page counts or page order have changed and let the user adjust the selection before export.

### [EX-010]
If a source file cannot be processed, the system shall tell the user exactly which file failed and why.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
The primary user groups for the command-line workflow are tentative and not yet confirmed in final scope.

### [UN-002]
The exact usage frequency for recurring editing sessions has not been defined and remains open for later quantification.

### [UN-003]
The tool's support for arbitrary rotation angles is not decided, and only fixed 90-degree steps are confirmed for now.

### [UN-004]
Optional update checks or help resources are not yet specified as part of the core document-processing workflow.

### [UN-005]
The exact license choice for the open-source distribution has not been selected.

### [UN-006]
Whether the minimum viable release includes a fully polished command-line scope or a lighter first version remains open.

## Delivery requirements

Implement the software described by the requirements above in `/workspace`.
`/workspace` is the only directory available to this task and starts empty.

1. Create a runnable program that implements the requirements.
2. Decide a build command, a test command and a run command for the program.
3. Run the build and test commands that apply and fix the problems you find.
4. Write `/workspace/delivery.json` describing how to build, test and run the program.

`delivery.json` is a JSON object with exactly these fields:

- `build_command`: shell command that prepares the program, or an empty string when no build step is needed
- `test_command`: shell command that runs the delivered tests, or an empty string when no tests are delivered
- `run_command`: shell command that starts the program
- `interface_type`: one of `http`, `cli`, `gui`, `file`
- `local_url`: URL that reaches the program when `interface_type` is `http`, otherwise an empty string
- `known_limitations`: list of strings describing what the delivered software does not do

An empty `test_command` records that no test entry point was delivered. It does
not mean that the software passes tests. Implement only what the requirements
state and do not assume behaviour that the requirements leave open.
