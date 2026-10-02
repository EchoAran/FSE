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
The system shall support merging selected PDF files or sections.

### [FR-003]
The system shall support extracting pages from PDF documents.

### [FR-004]
The system shall support rotating PDF pages.

### [FR-005]
The system shall support reordering PDF pages.

### [FR-006]
The system shall support alternating pages from different PDF documents.

### [FR-007]
The system shall support visually composing a new PDF document.

### [FR-008]
The system shall preserve original PDF input files untouched during normal use and after errors.

### [FR-009]
The system shall allow users to save reusable workspaces, setups, or job configurations for repeat use.

### [FR-010]
The system shall provide a command-line interface for recurring, automated, or scripted operations.

### [FR-011]
The system shall allow users to load PDF files and perform document operations in a single workflow without switching among multiple tools.

### [FR-012]
The system shall generate a new output PDF after document manipulation.

### [FR-013]
The system shall support saving the final PDF output without modifying the original files.

### [FR-014]
The system shall provide batch processing that can continue with valid files when that is safe.

### [FR-015]
The system shall allow the user to rerun only failed batch items after fixing the issue.

### [FR-016]
The system shall preserve the current workspace or document arrangement so the user can correct an error and retry without rebuilding the setup.

### [FR-017]
The system shall provide an import wizard for bringing in saved workspaces, presets, or job files.

### [FR-018]
The import wizard shall validate imported workflow or settings files before finalizing the import.

### [FR-019]
The import wizard shall provide a preview or side-by-side view of imported workflows before finalizing them.

### [FR-020]
The system shall allow users to edit imported jobs or configurations before saving them.

### [FR-021]
The system shall support an import process that completes the parts it can understand and reports unsupported items without failing silently.

### [FR-022]
The system shall support mapping terminology from older tools to the new tool during migration.

### [FR-023]
The system shall provide inline guidance during import when issues are detected.

### [FR-024]
The system shall support plain-language help for migration and common import scenarios.

### [FR-025]
The system shall support local file-system-based input and output operations.

### [FR-026]
The system shall support keyboard navigation in the graphical interface.

### [FR-027]
The system shall support screen reader use in the graphical interface.

### [FR-028]
The system shall provide good visual contrast and clear labels in the graphical interface.

### [FR-029]
The system shall remain usable with larger text and simpler layouts when needed.

### [FR-030]
The system shall display error messages inline when an error is tied to a specific file or page.

### [FR-031]
The system shall display pop-up messages for blocking issues, in addition to inline messages when appropriate.

### [FR-032]
The system shall keep the current workspace intact after an error so the user can fix the problem and retry.

### [FR-033]
The system shall show processing progress for long-running jobs.

### [FR-034]
The system shall allow separate jobs to be queued or run in the background without making the interface feel unresponsive.

### [FR-035]
The system shall support pausing, resuming, or reordering queued jobs.

### [FR-036]
The system shall support importing saved workspaces or presets from existing tools when possible.

## 4. Business Rules and Constraints

### [BR-001]
The system shall not be a full editing suite.

### [BR-002]
The system shall not modify original files during error handling.

### [BR-003]
The system shall avoid forcing a special filing structure and shall rely on existing team naming and folder conventions for outputs.

### [BR-004]
The system shall allow users to choose whether batch processing stops on the first error or continues.

### [BR-005]
The system shall support local, offline processing by default.

### [BR-006]
The system shall automatically clean up temporary files when a job finishes or is canceled.

### [BR-007]
Encryption for saved workspaces or output files shall be optional for regular users and may be mandatory in managed or enterprise settings through policy.

### [BR-008]
The system shall protect saved workspaces at least as carefully as output files because they can contain file paths and workflow details.

### [BR-009]
The system shall support modern, widely accepted encryption and password protection for sensitive work.

### [BR-010]
The system shall support audit trails in team or regulated environments.

### [BR-011]
Audit trails shall capture user identity, timestamp, source and output files, operation type, and success or failure.

### [BR-012]
The system shall handle temporary files with stronger protections as an advanced option for high-security environments.

### [BR-013]
The system shall allow users to adjust selection, replace a bad file, or rerun an operation after a failure.

### [BR-014]
The system shall communicate practical limits before processing when practical limits exist.

## 5. Data and External Interfaces

### [DI-001]
The system shall interact with the local file system for reading and writing PDF files.

### [DI-002]
The system shall provide a command-line interface for automation and scripts.

### [DI-003]
The system shall support importing workflow or settings files in an import process.

### [DI-004]
The system shall support output files and saved workspaces as generated artifacts.

## 6. Quality Requirements

### [QR-001]
The system shall be simple and easy enough for casual users to use without training on complex software.

### [QR-002]
The system shall feel simpler than current alternatives.

### [QR-003]
The system shall improve routine PDF cleanup and assembly time.

### [QR-004]
The system shall reduce manual rework errors such as incorrect page order or accidental source-file changes.

### [QR-005]
The system shall fail gracefully and provide clear, specific error information rather than generic errors.

### [QR-006]
The system shall provide detailed diagnostic logs, especially for command-line, batch, and automated runs.

### [QR-007]
The system shall keep the interface responsive during large jobs.

### [QR-008]
The system shall support typical batch jobs completing in a few seconds to about a minute when possible.

### [QR-009]
The system shall degrade gracefully and remain usable when processing large PDFs or large batches.

### [QR-010]
The system shall scale smoothly for moderate batches and larger jobs without freezing.

### [QR-011]
The system shall support visibility into which files failed, what operation was running, and the cause category in diagnostics.

### [QR-012]
The system shall be usable with accessibility features such as keyboard navigation, screen reader support, high contrast, clear labels, and larger text.

### [QR-013]
The system shall provide plain, specific error messages and next-step guidance.

### [QR-014]
The system shall provide a visual workflow arrangement interface for composing and adjusting document order.

### [QR-015]
The system shall keep users informed of progress during long-running or large processing tasks.

### [QR-016]
The system shall support transparent migration by explaining what was preserved and what was not during import.

### [QR-017]
The system shall support easy deployment, maintenance, and troubleshooting for IT or desktop support.

## 7. Exceptions and Boundary Conditions

### [EX-001]
If one file in a batch is bad, the system should keep the rest of the job intact where possible.

### [EX-002]
If processing multiple inputs, the system should continue with valid files when that is safe.

### [EX-003]
If an import contains unsupported items, the system should continue with the rest of the import and report the unsupported items.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
Whether the system must support integrations with email, DMS, or cloud services has not been confirmed.

### [UN-002]
A specific encryption standard or method has not been determined.

### [UN-003]
Whether audit trails are mandatory for all users has not been confirmed.

### [UN-004]
The exact archival or retention policy for output PDFs and saved workspace setups has not been defined.

### [UN-005]
Exact hard limits for file size, page count, and batch size have not been defined.

### [UN-006]
Whether true multi-user concurrency is required in the desktop application has not been confirmed.

### [UN-007]
Whether the job queue must support pausing, resuming, or reordering is not a fixed requirement and is only a nice-to-have.

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
