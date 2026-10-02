# Implementation task: Nenios Child Care Management

The requirements below were elicited in an interview and reviewed before delivery.

## Reviewed requirements

# Software Requirements Specification: Nenios Child Care Management

## 1. Scope and Context

### [SC-001]
The system shall be a web-based child care management system that uses a central database to reduce administrative work and support staff information sharing.

## 2. Actors

### [ST-001]
The system shall support administrators, teachers, and office or front-desk staff as user roles.

### [ST-002]
The system shall allow a single user to have multiple roles rather than forcing one fixed role.

## 3. Functional Requirements

### [FR-001]
The system shall allow administrators to register families.

### [FR-002]
The system shall allow administrators to manage enrollments.

### [FR-003]
The system shall allow administrators to manage classroom assignments.

### [FR-004]
The system shall allow administrators to manage classroom capacity.

### [FR-005]
The system shall allow administrators to manage waiting lists.

### [FR-006]
The system shall allow authorized staff to track child immunizations.

### [FR-007]
The system shall allow authorized staff to process invoices.

### [FR-008]
The system shall allow staff to look up family and child information.

### [FR-009]
The system shall allow office or front-desk staff to help with invoicing questions.

### [FR-010]
The system shall allow teachers to review child details such as allergies and immunizations.

### [FR-011]
The system shall allow teachers to record routine classroom-related notes if that is part of the workflow.

### [FR-012]
The system shall allow office or front-desk staff to look up family information and help keep basic records current.

### [FR-013]
The system shall support routine administrative tasks so the center can reduce time spent on administration.

### [FR-014]
The system shall support parent notices and reminders through email integration from day one.

### [FR-015]
The system shall support invoice generation even if accounting connectivity is not available immediately.

### [FR-016]
The system shall support exporting or manual transfer of invoice data as a temporary step when accounting connectivity is not yet available.

### [FR-017]
The system shall allow staff to log in from shared computers without friction.

### [FR-018]
The system shall support browser-based use without special software.

### [FR-019]
The system shall support use on tablets.

### [FR-020]
The system shall support temporary interruptions by saving work in draft or autosaved form so staff do not lose entered data.

### [FR-021]
The system shall allow staff to resume interrupted enrollment or invoice tasks from the last saved values.

### [FR-022]
The system shall allow staff to cancel or correct interrupted tasks without creating duplicate records.

### [FR-023]
The system shall show whether an enrollment or invoice task was saved as a draft, submitted, completed, or paid.

### [FR-024]
The system shall warn staff when another user is already editing the same record.

### [FR-025]
The system shall allow a record opened under concurrent editing to be viewed read-only or waited on until it becomes available.

### [FR-026]
The system shall force a review of conflicting fields if two users make changes to the same record.

### [FR-027]
The system shall display who changed a record and when.

### [FR-028]
The system shall show the last saved status of a record clearly.

### [FR-029]
The system shall show a visible history of payment transactions, including dates, amounts, refunds, and adjustments.

### [FR-030]
The system shall show invoice payment states as unpaid, partial, or paid.

### [FR-031]
The system shall show whether a payment or invoice task has gone through and what still needs attention.

### [FR-032]
The system shall allow staff to create family and child records when someone first applies or enrolls.

### [FR-033]
The system shall allow family and child records to be updated when contact details, emergency contacts, medical information, or billing details change.

### [FR-034]
The system shall allow child records to be marked inactive or archived when a child leaves the center.

### [FR-035]
The system shall allow records to be deleted only in very limited cases.

### [FR-036]
The system shall support archival of records while preserving history for reporting and billing reference.

### [FR-037]
The system shall keep immunization information as long as the child is active and archive it afterward.

### [FR-038]
The system shall support guided import of existing data with validation and error reports.

### [FR-039]
The system shall support review of imported records before they are finalized.

### [FR-040]
The system shall automatically map common fields during import and flag uncertain mappings for manual review.

### [FR-041]
The system shall suggest possible fixes for messy imported data and allow staff to correct or confirm values before loading.

### [FR-042]
The system shall support staged migration of active records before historical records.

### [FR-043]
The system shall support search of archived records.

### [FR-044]
The system shall support printable views or summaries.

### [FR-045]
The system shall provide built-in help tips and clear error messages.

### [FR-046]
The system shall provide step-by-step wizards for tasks such as enrolling a new family and setting up invoices.

### [FR-047]
The system shall provide contextual hints near fields, especially for required information or unusual cases.

### [FR-048]
The system shall allow users to review information before submitting complex tasks.

### [FR-049]
The system shall allow edits or reversal of mistakes where possible without requiring manual administrator intervention.

### [FR-050]
The system shall support a pilot with a small group of users before broader rollout.

### [FR-051]
The system shall support a phased rollout rather than a big switch-over.

### [FR-052]
The system shall support hands-on training for the pilot group and refresher sessions or job aids for the rest of the staff.

### [FR-053]
The system shall support a helpdesk or quick-response support channel during business hours.

### [FR-054]
The system shall support a fallback plan for release failures to avoid long disruptions.

### [FR-055]
The system shall support import of family records, child profiles, classroom assignments, immunization information, billing balances, and historical attendance or enrollment data if available.

### [FR-056]
The system shall support generation or sending of parent notices directly from the system through email integration.

### [FR-057]
The system shall share invoice and payment information with accounting systems.

### [FR-058]
The system shall allow payments to be recorded automatically if payment processor integration is available.

### [FR-059]
The system shall support multiple users using the system simultaneously without freezing.

### [FR-060]
The system shall show progress clearly when an operation takes longer to complete.

### [FR-061]
The system shall support adding users and records as the center grows without significant slowdown.

### [FR-062]
The system shall continue to support reporting well as the database grows.

### [FR-063]
The system shall support multiple sites later.

### [FR-065]
The system shall mark older records as archived once they are no longer actively used.

### [FR-066]
The system shall allow archived records to remain searchable while excluding them from day-to-day screens by default.

### [FR-067]
The system shall support a browser-based interface that is straightforward, consistent, and easy to use for non-technical staff.

### [FR-068]
The system shall support readable use on tablets.

### [FR-069]
The system shall support keyboard navigation and screen-reader-friendly design.

### [FR-070]
The system shall support larger text options.

### [FR-071]
The system shall support simple navigation with clear labels and minimal clicks for common tasks.

### [FR-072]
The system shall support role-based access control so users see only information relevant to their jobs.

### [FR-073]
The system shall support limiting access by function and, where needed, by classroom or site.

### [FR-074]
The system shall restrict sensitive health information more tightly than general contact information.

### [FR-075]
The system shall support temporary permissions for staff who temporarily cover another employee.

### [FR-076]
The system shall provide audit logs of logins and changes to important records, including who viewed or edited them and when.

### [FR-077]
The system shall provide strong individual logins for every staff member and shall not allow shared accounts.

### [FR-078]
The system shall support password complexity requirements and password expiration only for real security reasons.

### [FR-079]
The system shall support multi-factor authentication for administrators and for anyone handling billing or health records, especially for remote access.

### [FR-080]
The system shall support automatic session timeouts.

### [FR-081]
The system shall encrypt data in transit and at rest.

### [FR-082]
The system shall alert on suspicious activity such as repeated failed logins or access from unusual locations.

### [FR-083]
The system shall support temporary or off-hours access for some administrators under controlled conditions.

### [FR-084]
The system shall clearly indicate the current status of invoices and enrollments, including pending, submitted, and paid where applicable.

### [FR-085]
The system shall provide a simple message telling staff what to do next when something goes wrong.

### [FR-086]
The system shall support quick lookup of child or billing details for authorized staff.

### [FR-087]
The system shall support check-in and check-out routines.

### [FR-088]
The system shall allow staff to view whether a payment or invoice is still open, partly paid, or fully settled.

## 4. Business Rules and Constraints

### [BR-001]
Administrators shall have the broadest access to family and child records.

### [BR-002]
The system shall not silently overwrite changes when concurrent edits occur.

### [BR-003]
Only very limited cases shall allow deletion of records.

### [BR-004]
The system shall avoid double charges for billing.

### [BR-005]
The system shall keep a visible history for staff to understand what happened without guessing.

### [BR-006]
The system shall not use shared staff accounts.

### [BR-007]
The system shall support only very limited data deletion and prefer inactive or archived states for departed children and historical records.

### [BR-008]
The system shall preserve family and child history for reporting and billing reference after archival.

### [BR-009]
The system shall require careful control of remote or off-hours access.

### [BR-010]
The system shall allow only authorized staff to process invoices.

## 5. Data and External Interfaces

### [DI-001]
The system shall integrate with email for parent notices and reminders.

### [DI-002]
The system shall support integration with accounting software for invoice and payment information.

### [DI-003]
The system shall support calendar integration if later deemed necessary.

### [DI-004]
The system shall support SMS integration if later deemed necessary.

### [DI-005]
The system shall support payment processor integration if later deemed necessary.

## 6. Quality Requirements

### [FR-064]
The system shall keep older records accessible for compliance and reference.

### [QR-001]
The system shall be stable and easy to use when the internet connection is slow or temporarily unreliable.

### [QR-002]
The system shall load common tasks quickly.

### [QR-003]
The system shall remain responsive during busy periods such as morning drop-off, late afternoon pickup, and billing periods.

### [QR-004]
The system shall support use in short, interrupted sessions.

### [QR-005]
The system shall provide a straightforward interface because staff technical skill levels vary.

### [QR-006]
The system shall keep tasks from taking too many clicks.

### [QR-007]
The system shall show progress clearly during longer operations.

### [QR-008]
The system shall support reporting that still runs in a reasonable time as the database grows.

### [QR-009]
The system shall support future growth in the number of classrooms, families, staff, and records without feeling cramped.

### [QR-010]
The system shall support accessibility features including good contrast and keyboard support.

### [QR-011]
The system shall be forgiving if a connection is temporarily unreliable.

### [QR-012]
The system shall not slow down just because it contains years of historical data.

## 7. Exceptions and Boundary Conditions

### [EX-001]
If a task is interrupted, the system shall allow staff to determine whether it was saved as a draft or completed successfully.

### [EX-002]
If a critical task is interrupted, the system shall allow staff to resume or cancel it safely.

### [EX-003]
If a record is being edited by another user, the system shall warn the staff member and offer a read-only or wait path.

### [EX-004]
If conflicting changes occur, the system shall require review rather than silently overwriting data.

### [EX-005]
If data import contains uncertain or messy values, the system shall flag them for manual review before loading.

### [EX-006]
If a release fails, the system or rollout process shall support fallback handling to avoid long disruptions.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
The specific accounting product to integrate with has not been determined.

### [UN-002]
Whether calendar integration is required has not been decided.

### [UN-003]
Whether SMS integration is required has not been decided.

### [UN-004]
Whether a payment processor integration is required has not been decided.

### [UN-005]
Whether offline mode is required has not been decided.

### [UN-006]
Whether extra approval is required for remote or off-hours access has not been decided.

### [UN-007]
Whether multi-factor authentication is required for all users or only specific roles beyond administrators and staff handling billing or health records has not been decided.

### [UN-008]
The exact staff role titles to be used in the system have not been finalized.

### [UN-009]
Whether classroom or site-based access restrictions are required has not been fully decided.

### [UN-010]
The fixed retention rules for records have not been determined.

### [UN-011]
The center has not yet verified whether the system should support additional integrations, including calendar, SMS, or payment processor connections.

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
