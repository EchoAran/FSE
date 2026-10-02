# Software Requirements Specification: Nenios Child Care Management

## 1. Scope and Context

### [SC-001]
The project is for a web-based child care management system for a child care center.

### [SC-002]
The system shall reduce administrative work and support information sharing through a central database.

## 2. Actors

### [ACT-001]
Administrators shall be able to register families and manage enrollment, classroom capacity, and waiting lists.

### [ACT-002]
Authorized staff shall be able to support routine activities including tracking child immunizations, processing invoices, and producing information for customers and center operations.

## 3. Functional Requirements

### [FR-001]
The system shall support registering a family and child.

### [FR-002]
The system shall support checking whether a space is available for a child or placing the child on a waiting list.

### [FR-003]
The system shall support assigning a child to the appropriate classroom.

### [FR-004]
The system shall support keeping child records current, including immunizations and changes in attendance or family details.

### [FR-005]
The system shall support invoicing.

### [FR-006]
The system shall support checking children in and out.

### [FR-007]
The system shall support reviewing attendance.

### [FR-008]
The system shall support looking up family contact information.

### [FR-009]
The system shall support viewing child information needed for daily care, including classroom assignments, contacts, immunization status, allergy alerts, and pickup-authority information according to the user's access level.

### [FR-010]
The system shall support generating operational reports for authorized users.

### [FR-011]
The system shall support storing and displaying current, due soon, overdue, exempt, and missing statuses for immunization records.

### [FR-012]
The system shall flag immunization records that are nearing expiration, overdue, incomplete, expired, or missing, and notify staff and the family as appropriate.

### [FR-013]
The system shall allow families to upload replacement immunization records.

### [FR-014]
The system shall keep a child marked as not compliant until an incomplete, overdue, expired, missing, or otherwise unacceptable immunization record is verified or updated and staff confirms compliance.

### [FR-015]
The system shall support family self-service for updating contact information, submitting or updating enrollment forms, viewing invoices and payment history, and uploading documents.

### [FR-016]
The system shall allow families to request basic schedule changes, contact changes, enrollment changes, billing-related updates, pickup-authority changes, and custody-related changes online, but those requests shall remain pending staff review before becoming active.

### [FR-017]
The system shall allow basic profile edits such as address, phone number, email, and password changes to take effect immediately when they do not change care arrangements or safety-related information.

### [FR-018]
The system shall allow families to submit document uploads immediately when the upload does not change care arrangements or safety-related information.

### [FR-019]
The system shall support online payment processing.

### [FR-020]
The system shall support credit card payments and debit card payments, and may also support bank transfer if it can be supported securely.

### [FR-021]
The system shall allow the account holder or an authorized guardian to make payments.

### [FR-022]
The system shall support partial payments and keep the invoice open for the remaining balance.

### [FR-023]
The system shall log failed payments and show them to staff and the payer right away.

### [FR-024]
The system shall support recording payments made by a trusted family member or other non-account-holder in rare cases when staff verify the person against account notes, obtain confirmation from the account holder, or receive manager approval in an emergency.

### [FR-025]
The system shall support classroom capacity tracking by storing a maximum capacity for each classroom and automatically counting enrolled children against that capacity.

### [FR-026]
The system shall display the current enrolled count versus the classroom limit and show whether the classroom is full or available.

### [FR-027]
The system shall flag classrooms that reach capacity and prevent additional enrollments unless a manager or administrator overrides the restriction or moves a child off the waiting list.

### [FR-028]
The system shall support waiting list review and management.

### [FR-029]
The system shall support assigning and managing children in classrooms and room types based on age or developmental stage.

### [FR-030]
The system shall support route selection from a simple dashboard or search screen so staff can pick a child or family and complete a task without navigating many menus.

### [FR-031]
The system shall support quick access to routine items such as attendance and immunization checks during the normal day.

### [FR-032]
The system shall support phased rollout with training and a parallel running period before full cutover.

### [FR-033]
The system shall support temporary access for designated backups when an authorized staff member is out, and that access shall be limited to the duties being covered and shall end automatically or be easy to remove when the person returns.

### [FR-034]
The system shall support quick login and easy switching between users for shared workstations.

### [FR-035]
The system shall support use on shared desktop computers and tablets.

### [FR-036]
The system shall support migration of active family accounts, enrolled children, classroom assignments, immunization status, outstanding invoices or balances, current waiting list entries, contact history, and authorized pickup lists at go-live.

### [FR-037]
The system shall support site-based access so staff can only see and manage records for their own site unless they have a higher-level cross-site role.

### [FR-038]
The system shall support family accounts with children at more than one site while keeping contact information and billing unified under one family account.

### [FR-039]
The system shall support siblings and reports rolling up across locations for authorized users.

### [FR-040]
The system shall support exports and imports in CSV format and may also support Excel and PDF where appropriate.

### [FR-041]
The system shall validate import files field by field and reject only the affected row or record when values are missing, mismatched, or out of range, leaving existing data unchanged.

### [FR-042]
The system shall support exports and imports for sensitive family or child data only with strict permission controls and field restrictions.

### [FR-043]
The system shall support billing adjustments as invoice adjustments rather than silently changing the original charge.

### [FR-044]
The system shall keep disputed charges visible with a status for billing staff review.

### [FR-045]
The system shall record credits and refunds with a reason and link them to the original invoice.

### [FR-046]
The system shall maintain an audit trail for invoice adjustments, credits, refunds, and reversals so it is clear who made the change and why.

### [FR-047]
The system shall support sibling discounts on eligible tuition charges when two or more enrolled children belong to the same family account, according to the policy configured by staff.

### [FR-048]
The system shall support late fees when payment is overdue after a configured grace period.

### [FR-049]
The system shall support prorating when a child starts or leaves partway through a billing period or when enrollment changes mid-cycle.

### [FR-050]
The system shall allow absences to affect tuition only according to configurable policy rather than hardcoded rules.

### [FR-051]
The system shall allow authorized users to review, approve, or override sensitive changes and exceptions including enrollment exceptions, capacity overrides, payment reversals, and temporary access grants.

### [FR-052]
The system shall support keeping a child enrolled but clearly marked as not compliant when immunization records are incomplete, overdue, or missing at go-live.

### [FR-053]
The system shall support a clear workflow for staff to follow up on missing or noncompliant immunization records until the record is verified or updated.

### [FR-054]
The system shall support a central dashboard or search screen for staff to access common daily tasks.

### [FR-055]
The system shall support training administrators and office staff first, followed by classroom staff and other users who need to view child or family information.

### [FR-056]
The system shall support go-live only after core data is loaded and staff can complete the main workflows reliably.

### [FR-057]
The system shall support keeping reports, billing, and attendance information consistent with expected center outputs before full cutover.

### [FR-058]
The system shall support moving children in and out of classrooms only when classroom capacity allows, unless an authorized override is used.

### [FR-059]
The system shall support staff review before any change that affects custody, safety, immunization compliance, fees, billing arrangements, or who is allowed to pick up a child.

### [FR-060]
The system shall support immediate visibility of allergy alerts and restricted pickup lists before a child is released.

### [FR-061]
The system shall support queued or delayed handling of non-urgent tasks such as end-of-day reporting, invoice review, routine record updates, routine edits, reporting, and billing tasks during peak periods.

### [FR-062]
The system shall support at-a-glance visibility of whether an item is current, due soon, overdue, exempt, or missing so staff can determine the needed follow-up action without opening detailed records.

## 4. Business Rules and Constraints

### [BR-001]
Only administrators and authorized staff shall handle enrollment, capacity, billing, and most record management.

### [BR-002]
Teaching and support staff shall be restricted from sensitive billing information and full administrative settings.

### [BR-003]
System administrators shall be the only users who can change security settings, user permissions, and other system-wide configuration.

### [BR-004]
System administrators, senior administrators, or authorized supervisors shall be among the only users who can see unmasked sensitive export details.

### [BR-005]
Routine operational exports shall exclude or mask sensitive fields unless there is a clear business need and the user has the right permission.

### [BR-006]
Sensitive exports shall exclude or mask full custody details, emergency contacts, full payment information, health or immunization notes, notes about a child's special needs, custody restrictions, and other staff-inappropriate fields by default.

### [BR-007]
If a classroom reaches capacity, additional enrollments shall be blocked by default.

### [BR-008]
Sibling discounts shall not stack with other discounts unless the policy explicitly allows it.

### [BR-009]
Payments shall be restricted so random staff cannot make or change payments without permission.

### [BR-010]
Temporary access for exceptional payment or billing cases shall be time-limited and tied to a reason.

### [BR-011]
The system shall hold payments for review when they are unusually large, made right after a dispute, come from an account with failed payments, involve an inactive payer, have overdue balances beyond a certain point, or appear suspicious.

### [BR-012]
Normal recurring tuition payments shall go through right away unless there is a clear problem.

### [BR-013]
Attendance actions shall remain fast and reliable during peak periods.

### [BR-014]
The system shall not overwrite source or existing records silently during migration or import when data is missing, inconsistent, mismatched, or conflicting.

## 5. Data and External Interfaces

### [DI-001]
The system shall import and export data in CSV format.

### [DI-002]
The system may import and export data in Excel format.

### [DI-003]
The system may export PDF reports or records for read-only use.

### [DI-004]
Import files shall support field validation for required names, dates, phone numbers, emails, and immunization dates.

### [DI-005]
For imports, the system shall reject only the affected row or record when a value is missing, mismatched, or out of range, and shall preserve the current data for that record.

## 6. Quality Requirements

### [QR-001]
The system shall improve accuracy, speed, and consistency for staff operations.

### [QR-002]
The system shall reduce duplicate data entry and manual coordination.

### [QR-003]
The system shall be easy to read and simple to navigate.

### [QR-004]
The system shall not rely on tiny controls.

### [QR-005]
The system shall remain responsive during arrival, pickup, and meal-time peak periods and shall not slow down or time out even with many users entering information at the same time.

### [QR-006]
The system shall provide simple updates and good support when issues come up.

### [QR-007]
The system shall be built so future enhancements and added classrooms or sites do not require starting over.

### [QR-008]
The system shall be flexible enough to add more classrooms or additional sites if the center grows.

### [QR-009]
The system shall work well on the devices staff actually use, including shared desktop computers and tablets.

### [QR-010]
The system shall support quick login for shared workstations.

### [QR-011]
The system shall make critical attendance actions fast and reliable even if other tasks are queued or delayed.

### [QR-012]
The system shall support clear at-a-glance status display for immunization records and classroom capacity.

## 7. Exceptions and Boundary Conditions

### [EX-001]
The system shall handle major holidays, school breaks, and staff training days as scheduling exceptions without requiring staff to work around them manually.

### [EX-002]
The system shall allow reduced or special scheduling during school breaks or staff training days.

### [EX-003]
The system shall allow a manager or administrator to override classroom capacity only in exceptional cases, and the override shall be logged.

### [EX-004]
The system shall hold a child release for review when allergy information, pickup authority, or other safety information is incomplete or conflicting.

### [EX-005]
The system shall allow temporary exceptions for immunization noncompliance only if the center has a policy for them.

### [EX-006]
The system shall allow payment reversals to require approval or a second review depending on the amount, and unusual or large reversals shall need extra approval or manager review.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
It is unresolved whether the system must treat room types as separate program types or as classroom categories.

### [UN-002]
It is unresolved whether the system must support exact operating times for each site or program, because the interviewee stated the exact times still need verification.

### [UN-003]
It is unresolved which future enhancements, such as richer parent communication, online forms, more detailed reporting, online payment processing, and automated reminders, will be priorities for first implementation after the initial release.
