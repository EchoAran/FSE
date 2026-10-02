# Implementation task: PDF Split and Merge

The requirements below were elicited in an interview and reviewed before delivery.

## Reviewed requirements

# Software Requirements Specification: PDF Split and Merge

## 1. Scope and Context

### [SC-001]
The product is a free graphical tool for manipulating PDF documents without altering the original input files.

## 2. Actors

### [SA-001]
The tool shall support regular office users who need quick one-off PDF fixes.

### [SA-002]
The tool shall support power users or support staff who repeat the same operations often.

## 3. Functional Requirements

### [FR-001]
The tool shall support splitting PDF documents.

### [FR-002]
The tool shall support merging selected files or sections.

### [FR-003]
The tool shall support extracting pages from PDF documents.

### [FR-004]
The tool shall support rotating pages.

### [FR-005]
The tool shall support reordering pages.

### [FR-006]
The tool shall support alternating pages from different documents.

### [FR-007]
The tool shall support visually composing new documents.

### [FR-008]
The tool shall provide a command-line option for repeatable or automated tasks.

### [FR-009]
The tool shall allow users to save and reuse their setup or work environment.

### [FR-010]
The tool shall perform PDF manipulation quickly.

### [FR-011]
The graphical tool shall support a simple visual interface with minimal setup for one-off PDF tasks.

### [FR-012]
The tool shall support careful page-level control with a clear preview of the result.

### [FR-013]
The tool shall write output as a new file unless the user explicitly chooses otherwise.

### [FR-014]
The tool shall support a default output folder for simple workflows.

### [FR-015]
The tool shall allow users to save output alongside the source when that makes sense for the workflow.

### [FR-016]
The tool shall support naming rules or a saved destination in the reusable workspace for repeated jobs.

### [FR-017]
The graphical tool shall provide a clear confirmation before writing if there is any chance of replacing an existing file.

### [FR-018]
The graphical tool shall provide a clear confirmation before writing if the chosen operation would produce multiple outputs.

### [FR-019]
The command-line interface shall require the destination to be explicit in the command or configurable through the saved setup.

### [FR-020]
The graphical tool shall let users review the full set of outputs before anything is saved.

### [FR-021]
When one operation creates multiple files, the tool shall support a consistent naming pattern or bulk destination assignment.

### [FR-022]
In command-line mode, the output behavior shall be fully defined up front.

### [FR-023]
In command-line mode, naming patterns or destination rules shall be passed in as part of the command or saved configuration.

## 4. Business Rules and Constraints

### [BR-001]
The tool shall avoid overwriting the original files by default.

## 5. Data and External Interfaces

None specified.

## 6. Quality Requirements

None specified.

## 7. Exceptions and Boundary Conditions

### [FR-024]
In automated command-line runs, the tool shall fail safely or require explicit overwrite options instead of stopping for interactive confirmation.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
Whether there are separate stakeholder groups on the business side beyond the user groups described is not yet known.

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
