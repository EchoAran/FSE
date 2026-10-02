# Implementation task: Security and Privacy Requirements Analysis Tool

The requirements below were elicited in an interview and reviewed before delivery.

## Reviewed requirements

# Software Requirements Specification: Security and Privacy Requirements Analysis Tool

## 1. Scope and Context

### [SC-001]
SPRAT is a collaborative workbench for aligning web-system requirements with privacy and security policies.

## 2. Actors

### [ST-001]
The system shall support administrators, project managers, analysts, and guests with role-based access.

## 3. Functional Requirements

### [FR-001]
The system shall allow users to capture goals, scenarios, policies, requirements, and legal-compliance information.

### [FR-002]
The system shall trace goals back to their source policies.

### [FR-003]
The system shall provide flexible classifications for organizing analysis items.

### [FR-004]
The system shall allow users to compare analyses produced by different people.

### [FR-005]
The system shall make it easier to connect security and privacy requirements back to the policies and legal obligations they came from without losing traceability.

### [FR-006]
The system shall support collaboration so different people can work on the same analysis, compare their results, and spot gaps or inconsistencies quickly.

### [FR-007]
The system shall provide clear evidence of how each requirement was derived.

### [FR-008]
The system shall control access so that people with different roles can use it appropriately while protecting sensitive information.

### [FR-009]
The system shall keep a full history of changes.

### [FR-010]
The system shall identify the user who made each change and the timestamp of the change.

### [FR-011]
The system shall record the reason for a change when the user provides one.

### [FR-012]
The system shall support side-by-side comparison of earlier versions, especially for differences in goals, requirements, or trace links.

### [FR-013]
The system shall save changes immediately when an analyst edits an item.

### [FR-014]
For most edits, the system shall place the item in a draft or pending state until review occurs, especially when the change affects traceability, policy interpretation, or legal compliance.

### [FR-015]
The system shall use peer review as the normal review path, with project managers stepping in for higher-risk or contentious changes and administrators handling access or system-level issues.

### [FR-016]
While an item is in draft or pending, the analyst who created it shall be able to keep editing it.

### [FR-017]
While an item is in draft or pending, the analyst who created it shall be able to withdraw or revise it before review.

### [FR-018]
Other analysts and project managers shall be able to see that a draft exists.

### [FR-019]
The system shall limit visibility of draft items when they contain sensitive material or have not been approved yet.

### [FR-020]
An item shall move to reviewed or final only after the required reviewer signs off.

### [FR-021]
The system shall record approval in the history when an item is reviewed or finalized.

### [FR-022]
Once an item is final, edits shall create a new revision rather than overwriting the approved version.

### [FR-023]
The system shall keep the approved version intact for audit and comparison after finalization.

### [FR-024]
For draft items, other roles shall usually be able to see that a draft exists, who owns it, what it is roughly about, and its review status.

### [FR-025]
The system shall hide the full content of a draft item when it is sensitive or still under discussion.

### [FR-026]
Project managers and assigned reviewers shall see more detail than general analysts for draft items.

### [FR-027]
Guests shall not see anything about drafts unless a project explicitly allows it.

### [FR-028]
For users with the right project access, the system shall make an item's existence and basic metadata visible, but keep the content hidden until the item is approved or explicitly shared.

### [FR-029]
If an item is marked sensitive, the system shall limit even the metadata to the author, reviewers, and administrators.

### [FR-030]
During import, the system shall preserve the structure of the analysis, including goals, scenarios, requirements, policy links, and traceability.

### [FR-031]
During import, the system shall retain classifications, tags, and version references where possible.

## 4. Business Rules and Constraints

None specified.

## 5. Data and External Interfaces

### [DI-001]
The system shall import from common document sources.

### [DI-002]
The system shall import from spreadsheets or structured exports from other requirements tools.

### [DI-003]
The system shall support importing policy or compliance references from upstream repositories.

## 6. Quality Requirements

### [QR-001]
The system shall support producing more complete and consistent analyses in less time.

## 7. Exceptions and Boundary Conditions

### [EX-001]
If a source policy is incomplete or a legal obligation is missing, the system shall let the analyst flag the gap, record assumptions, and mark the item as unresolved so it is visible in the analysis.

### [EX-002]
For conflicting policies or requirements, the system shall allow both versions to be captured and highlight the conflict for later resolution.

### [EX-003]
If traceability cannot be established for an item, the system shall treat it as a documented exception rather than silently ignoring it, so partial analyses remain usable and clearly labeled as partial.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
Whether the system should support branching and merging is not yet decided.

### [UN-002]
The exact approval rule for changes depends on the project's configuration and is not yet specified.

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
