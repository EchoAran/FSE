# Implementation task: PDF Split and Merge

The requirements below were elicited in an interview and reviewed before delivery.

## Reviewed requirements

# Software Requirements Specification: PDF Split and Merge

## 1. Scope and Context

### [SC-001]
The project is a free graphical tool for manipulating PDF documents.

### [SC-002]
The tool must allow users to manipulate PDF documents without altering the original input files.

### [SC-003]
The tool must support both visual, manual work and command-line use for repeatable tasks.

## 2. Actors

### [ST-001]
The tool is intended for users who need everyday PDF handling, including casual users working through a graphical interface and users performing automated or recurring jobs through the command line.

## 3. Functional Requirements

### [FR-001]
The system shall support splitting PDF documents.

### [FR-002]
The system shall support merging selected files or sections.

### [FR-003]
The system shall support extracting selected pages from PDF documents.

### [FR-004]
The system shall support rotating pages.

### [FR-005]
The system shall support reordering pages.

### [FR-006]
The system shall support alternating pages from different documents.

### [FR-007]
The system shall support visually composing new documents.

### [FR-008]
The system shall allow users to save reusable work environments or setups.

### [FR-009]
The system shall provide a command-line path for recurring or automated operations.

## 4. Business Rules and Constraints

None specified.

## 5. Data and External Interfaces

None specified.

## 6. Quality Requirements

None specified.

## 7. Exceptions and Boundary Conditions

None specified.

## 8. Unresolved Information

No unresolved items identified.

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
