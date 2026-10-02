# Implementation task: Security and Privacy Requirements Analysis Tool

The requirements below were elicited in an interview and reviewed before delivery.

## Reviewed requirements

# Software Requirements Specification: Security and Privacy Requirements Analysis Tool

## 1. Scope and Context

### [SC-001]
SPRAT is a collaborative workbench for aligning web-system requirements with privacy and security policies.

## 2. Actors

### [ACT-001]
The system shall support administrators, project managers, analysts, and guests with differentiated access.

## 3. Functional Requirements

### [FR-001]
The system shall allow users to capture goals, scenarios, policies, requirements, and legal-compliance information in one place.

### [FR-002]
The system shall allow users to store goals as high-level artifacts.

### [FR-003]
The system shall allow users to store scenarios or use cases that explain how goals are realized.

### [FR-004]
The system shall allow users to store security and privacy requirements.

### [FR-005]
The system shall allow users to store policies or legal sources from which requirements originate.

### [FR-006]
The system shall allow users to store compliance notes or rationale that explain why a requirement exists.

### [FR-007]
The system shall support explicit and navigable links between artifacts.

### [FR-008]
The system shall allow a user to view, from a requirement, the policy, regulation, or internal rule that justified it.

### [FR-009]
The system shall allow a user to view, from a policy or legal reference, all requirements that came from it.

### [FR-010]
The system shall support requirements with multiple source policies or legal references.

### [FR-011]
The system shall keep the full set of sources for a requirement when multiple source policies or legal references apply.

### [FR-012]
The system shall allow users to mark one source as primary for convenience or reporting when a requirement has multiple sources.

### [FR-013]
The system shall allow users to compare analyses produced by different people.

### [FR-014]
The system shall allow users to organize artifacts with flexible classifications.

### [FR-015]
The system shall provide role-based access control so that administrators, project managers, analysts, and guests do not all see or edit the same things.

### [FR-016]
The system shall support collaboration without users overwriting each other’s work.

### [FR-017]
The system shall record who changed what and when.

### [FR-018]
The system shall allow users to go back if something was entered incorrectly or replaced by mistake.

## 4. Business Rules and Constraints

### [BR-001]
The trace between artifacts shall work both ways between requirements and their source policies or legal references.

## 5. Data and External Interfaces

None specified.

## 6. Quality Requirements

### [QR-001]
The system shall make traceability and comparison easier than the current manual process.

### [QR-002]
The system shall make collaboration safer and easier to review through versioning and change history.

## 7. Exceptions and Boundary Conditions

None specified.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
Whether any additional features beyond the main ones are required has not been decided and must be confirmed with the team.

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
