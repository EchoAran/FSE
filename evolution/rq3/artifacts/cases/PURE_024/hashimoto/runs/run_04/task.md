# Implementation task: Nenios Child Care Management

The requirements below were elicited in an interview and reviewed before delivery.

## Reviewed requirements

# Software Requirements Specification: Nenios Child Care Management

## 1. Scope and Context

### [SC-001]
The system is a web-based child care management system for a child care center.

### [SC-002]
The system shall reduce administrative work.

### [SC-003]
The system shall keep family, child, classroom, and billing information in one place so staff can work from the same records.

## 2. Actors

### [ST-001]
Administrators are a primary user group of the system.

### [ST-002]
Front office or enrollment staff are a primary user group of the system.

### [ST-003]
Teachers are a primary user group of the system.

### [ST-004]
Other authorized center staff who need child or billing information are a primary user group of the system.

## 3. Functional Requirements

### [FR-001]
The system shall allow administrators to register families.

### [FR-002]
The system shall support enrollment management.

### [FR-003]
The system shall support classroom capacity management.

### [FR-004]
The system shall support waiting list management.

### [FR-005]
The system shall support tracking child immunizations.

### [FR-006]
The system shall support invoicing.

### [FR-007]
The system shall support reporting for center operations.

### [FR-008]
The system shall support reporting to produce information for customers and center operations.

### [FR-009]
The system shall help make invoicing easier.

### [FR-010]
The system shall help make reporting easier.

## 4. Business Rules and Constraints

### [BR-001]
The system shall manage enrollments and waiting lists more consistently.

## 5. Data and External Interfaces

None specified.

## 6. Quality Requirements

None specified.

## 7. Exceptions and Boundary Conditions

None specified.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
It is not yet confirmed whether parents or guardians will interact with the system to view forms, invoices, or updates.

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
