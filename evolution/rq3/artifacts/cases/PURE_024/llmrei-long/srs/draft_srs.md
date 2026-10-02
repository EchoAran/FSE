# Software Requirements Specification: Nenios Child Care Management

## 1. Scope and Context

### [SC-001] (stated)
The system shall be a web-based management system for a child care center.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "A child care center needs a web-based management system that reduces administrative work and lets employees share information through a central database. Administrators should be able to register families and manage enrollment, classroom capacity, and waiting lists, while authorized staff need support for routine activities such as tracking child immunizations, processing invoices, and producing information for customers and center operations."

### [SC-002] (stated)
The system shall support day-to-day administration, staff workflows, and central records for families, enrollment, billing, and child information.

**Source Evidence:**
- `[interview_turn:T002]` "Yes, that sounds aligned with what we need. I’m expecting us to focus on the child care center’s day-to-day administration, staff workflows, and the central records we need to manage families, enrollment, billing, and child information. I’m not looking to get into unrelated areas beyond what supports those operations."
- `[initial_requirement:INITIAL_REQUIREMENTS]` "A child care center needs a web-based management system that reduces administrative work and lets employees share information through a central database. Administrators should be able to register families and manage enrollment, classroom capacity, and waiting lists, while authorized staff need support for routine activities such as tracking child immunizations, processing invoices, and producing information for customers and center operations."

## 2. Actors

### [ST-001] (stated)
The system shall support administrators, office staff, teachers, and parents or guardians as stakeholders or users of system outputs.

**Source Evidence:**
- `[interview_turn:T032]` "The main people to include would be the administrators, office staff, teachers, and probably the parents or guardians, because they all use or depend on the system in different ways. Administrators care about enrollment, reporting, and control; teachers need quick access to child and classroom information; office staff handle billing and records; and parents care about clear communication and accurate account information. I’d also consider compliance or licensing requirements, since those can affect what data we need to store and report."

## 3. Functional Requirements

### [FR-001] (stated)
The system shall allow staff to register and maintain family profiles with parent or guardian contact details and linked children.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "A child care center needs a web-based management system that reduces administrative work and lets employees share information through a central database. Administrators should be able to register families and manage enrollment, classroom capacity, and waiting lists, while authorized staff need support for routine activities such as tracking child immunizations, processing invoices, and producing information for customers and center operations."
- `[interview_turn:T020]` "Family registration should let us create and maintain a complete family profile with parent or guardian contact details and linked children, so we don’t have to re-enter the same information in different places. Enrollment and waiting list management should show us which children are enrolled, which are pending, and where they stand on the waiting list, so we can move children in as openings come up. Classroom capacity tracking should prevent us from placing too many children in a room and give staff a quick view of available spots by classroom and age group."

### [FR-002] (stated)
The system shall support enrollment management, including showing which children are enrolled, which are pending, and their waiting list position.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "A child care center needs a web-based management system that reduces administrative work and lets employees share information through a central database. Administrators should be able to register families and manage enrollment, classroom capacity, and waiting lists, while authorized staff need support for routine activities such as tracking child immunizations, processing invoices, and producing information for customers and center operations."
- `[interview_turn:T020]` "Family registration should let us create and maintain a complete family profile with parent or guardian contact details and linked children, so we don’t have to re-enter the same information in different places. Enrollment and waiting list management should show us which children are enrolled, which are pending, and where they stand on the waiting list, so we can move children in as openings come up. Classroom capacity tracking should prevent us from placing too many children in a room and give staff a quick view of available spots by classroom and age group."

### [FR-003] (stated)
The system shall support moving a child from the waiting list to active enrollment when a spot opens.

**Source Evidence:**
- `[interview_turn:T022]` "When a spot opens, staff should be able to see who is next in line for the right classroom or age group and move that child from waiting list to active enrollment with a few steps. I’d expect the system to check capacity before confirming the move, and if possible it should notify staff so they know which child is eligible next. If there are special priorities, like siblings or approved dates, that should probably be reflected too, but I’d need to confirm the exact rules."

### [FR-004] (stated)
The system shall allow staff to identify the next child in line for the appropriate classroom or age group when a spot opens.

**Source Evidence:**
- `[interview_turn:T022]` "When a spot opens, staff should be able to see who is next in line for the right classroom or age group and move that child from waiting list to active enrollment with a few steps. I’d expect the system to check capacity before confirming the move, and if possible it should notify staff so they know which child is eligible next. If there are special priorities, like siblings or approved dates, that should probably be reflected too, but I’d need to confirm the exact rules."

### [FR-005] (stated)
The system shall check classroom capacity before confirming a waiting-list-to-enrollment move.

**Source Evidence:**
- `[interview_turn:T022]` "When a spot opens, staff should be able to see who is next in line for the right classroom or age group and move that child from waiting list to active enrollment with a few steps. I’d expect the system to check capacity before confirming the move, and if possible it should notify staff so they know which child is eligible next. If there are special priorities, like siblings or approved dates, that should probably be reflected too, but I’d need to confirm the exact rules."

### [FR-006] (stated)
The system shall support classroom capacity tracking by classroom and age group.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "A child care center needs a web-based management system that reduces administrative work and lets employees share information through a central database. Administrators should be able to register families and manage enrollment, classroom capacity, and waiting lists, while authorized staff need support for routine activities such as tracking child immunizations, processing invoices, and producing information for customers and center operations."
- `[interview_turn:T020]` "Family registration should let us create and maintain a complete family profile with parent or guardian contact details and linked children, so we don’t have to re-enter the same information in different places. Enrollment and waiting list management should show us which children are enrolled, which are pending, and where they stand on the waiting list, so we can move children in as openings come up. Classroom capacity tracking should prevent us from placing too many children in a room and give staff a quick view of available spots by classroom and age group."

### [FR-007] (stated)
The system shall provide staff with a quick view of available classroom spots by classroom and age group.

**Source Evidence:**
- `[interview_turn:T020]` "Family registration should let us create and maintain a complete family profile with parent or guardian contact details and linked children, so we don’t have to re-enter the same information in different places. Enrollment and waiting list management should show us which children are enrolled, which are pending, and where they stand on the waiting list, so we can move children in as openings come up. Classroom capacity tracking should prevent us from placing too many children in a room and give staff a quick view of available spots by classroom and age group."

### [FR-008] (stated)
The system shall store each child’s profile along with health and immunization information.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "A child care center needs a web-based management system that reduces administrative work and lets employees share information through a central database. Administrators should be able to register families and manage enrollment, classroom capacity, and waiting lists, while authorized staff need support for routine activities such as tracking child immunizations, processing invoices, and producing information for customers and center operations."
- `[interview_turn:T010]` "Yes, that captures the core of it. I’d also want immunization tracking included as part of the child records, since that’s something we need to monitor closely. Beyond that, the system should make it easy to produce basic information for parents and for internal center operations."
- `[interview_turn:T026]` "It should store each child’s profile along with health and immunization information so staff can quickly see whether records are current or if anything is missing. We mainly need it to help us monitor compliance and avoid overlooking required updates. If there are alerts for overdue immunizations or incomplete records, that would be very helpful."

### [FR-009] (stated)
The system shall allow staff to quickly see whether child health and immunization records are current or missing information.

**Source Evidence:**
- `[interview_turn:T026]` "It should store each child’s profile along with health and immunization information so staff can quickly see whether records are current or if anything is missing. We mainly need it to help us monitor compliance and avoid overlooking required updates. If there are alerts for overdue immunizations or incomplete records, that would be very helpful."

### [FR-010] (stated)
The system shall support monitoring compliance related to child health and immunization information.

**Source Evidence:**
- `[interview_turn:T026]` "It should store each child’s profile along with health and immunization information so staff can quickly see whether records are current or if anything is missing. We mainly need it to help us monitor compliance and avoid overlooking required updates. If there are alerts for overdue immunizations or incomplete records, that would be very helpful."

### [FR-011] (stated)
The system shall generate charges for each family based on the child’s enrollment and any applicable care schedule or fees.

**Source Evidence:**
- `[interview_turn:T028]` "Invoicing should let us generate charges for each family based on the child’s enrollment and any applicable care schedule or fees. We need to be able to see what has been billed, what has been paid, and what is still outstanding, so billing stays organized. If the system can also produce statements or receipts for parents, that would be useful."

### [FR-012] (stated)
The system shall allow staff to see what has been billed, what has been paid, and what is still outstanding.

**Source Evidence:**
- `[interview_turn:T028]` "Invoicing should let us generate charges for each family based on the child’s enrollment and any applicable care schedule or fees. We need to be able to see what has been billed, what has been paid, and what is still outstanding, so billing stays organized. If the system can also produce statements or receipts for parents, that would be useful."

### [FR-013] (conditional)
The system shall produce statements or receipts for parents if needed.

**Source Evidence:**
- `[interview_turn:T028]` "Invoicing should let us generate charges for each family based on the child’s enrollment and any applicable care schedule or fees. We need to be able to see what has been billed, what has been paid, and what is still outstanding, so billing stays organized. If the system can also produce statements or receipts for parents, that would be useful."

### [FR-014] (stated)
The system shall produce clear information for parents about enrollment status, billing, and appropriate child or center updates.

**Source Evidence:**
- `[interview_turn:T012]` "Yes, I think so. Parents will need some kind of information output, especially around enrollment status, billing, and maybe child record-related updates that are appropriate to share. I’m not sure yet how much should be visible directly to parents versus generated by staff, so that would need to be confirmed with the team."
- `[interview_turn:T030]` "It should produce clear information that we can give to parents about things like enrollment status, billing, and important child or center updates. Ideally this would reduce the need for staff to prepare everything manually, so we can share consistent information faster. If there are printable or email-friendly formats, that would be helpful."

### [FR-015] (stated)
The system shall reduce the need for staff to prepare parent-facing information manually by enabling faster sharing of consistent information.

**Source Evidence:**
- `[interview_turn:T030]` "It should produce clear information that we can give to parents about things like enrollment status, billing, and important child or center updates. Ideally this would reduce the need for staff to prepare everything manually, so we can share consistent information faster. If there are printable or email-friendly formats, that would be helpful."

### [FR-016] (stated)
The system shall support internal operational reporting for enrollment counts, vacancies, outstanding balances, and upcoming immunization issues.

**Source Evidence:**
- `[interview_turn:T036]` "One thing I’d add is reporting for the center’s internal operations, like enrollment counts, vacancies, outstanding balances, and upcoming immunization issues, because that would help management make decisions faster. I’d also want the system to be easy enough for staff to learn quickly, since not everyone will be very technical. Beyond that, nothing major comes to mind right now, but I’d want to review anything related to security and data privacy before finalizing."

### [FR-017] (stated)
The system shall provide a daily snapshot of enrollment and classroom occupancy.

**Source Evidence:**
- `[interview_turn:T038]` "The first ones I’d want are a daily snapshot of enrollment and classroom occupancy, plus a view of the waiting list and any open spots. I’d also want a billing summary showing unpaid invoices and a health reminder view for immunizations that are due or missing. Those would cover the most urgent day-to-day decisions for the center."

### [FR-018] (stated)
The system shall provide a view of the waiting list and any open spots.

**Source Evidence:**
- `[interview_turn:T038]` "The first ones I’d want are a daily snapshot of enrollment and classroom occupancy, plus a view of the waiting list and any open spots. I’d also want a billing summary showing unpaid invoices and a health reminder view for immunizations that are due or missing. Those would cover the most urgent day-to-day decisions for the center."

### [FR-019] (stated)
The system shall provide a billing summary showing unpaid invoices.

**Source Evidence:**
- `[interview_turn:T038]` "The first ones I’d want are a daily snapshot of enrollment and classroom occupancy, plus a view of the waiting list and any open spots. I’d also want a billing summary showing unpaid invoices and a health reminder view for immunizations that are due or missing. Those would cover the most urgent day-to-day decisions for the center."

### [FR-020] (stated)
The system shall provide a health reminder view for immunizations that are due or missing.

**Source Evidence:**
- `[interview_turn:T038]` "The first ones I’d want are a daily snapshot of enrollment and classroom occupancy, plus a view of the waiting list and any open spots. I’d also want a billing summary showing unpaid invoices and a health reminder view for immunizations that are due or missing. Those would cover the most urgent day-to-day decisions for the center."

### [FR-021] (stated)
The system shall allow authorized staff to share up-to-date information through a central system.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "A child care center needs a web-based management system that reduces administrative work and lets employees share information through a central database. Administrators should be able to register families and manage enrollment, classroom capacity, and waiting lists, while authorized staff need support for routine activities such as tracking child immunizations, processing invoices, and producing information for customers and center operations."
- `[interview_turn:T008]` "We want to replace the scattered manual tracking with one central system that everyone authorized can use. The biggest improvements are faster family registration, better enrollment and waiting list management, clearer classroom capacity tracking, and less time spent on invoicing and looking up child records. We also want staff to be able to share up-to-date information without relying on paper or separate files."

### [FR-022] (stated)
The system shall support central storage and lookup of family, enrollment, billing, and child information.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "A child care center needs a web-based management system that reduces administrative work and lets employees share information through a central database. Administrators should be able to register families and manage enrollment, classroom capacity, and waiting lists, while authorized staff need support for routine activities such as tracking child immunizations, processing invoices, and producing information for customers and center operations."
- `[interview_turn:T004]` "I’m one of the stakeholders for the child care center, and I’m speaking from the operational side of the business. My focus is on how the staff and administrators will use the system day to day to reduce manual work and keep family, child, and billing information organized in one place."
- `[interview_turn:T008]` "We want to replace the scattered manual tracking with one central system that everyone authorized can use. The biggest improvements are faster family registration, better enrollment and waiting list management, clearer classroom capacity tracking, and less time spent on invoicing and looking up child records. We also want staff to be able to share up-to-date information without relying on paper or separate files."

### [FR-023] (stated)
The system shall support reviewing audit trail entries to review decisions, track errors, and answer questions if there is a dispute.

**Source Evidence:**
- `[interview_turn:T024]` "Role-based access control should make sure each employee only sees and edits the parts of the system that match their job, so for example office staff, teachers, and administrators don’t all have the same access. The audit trail should record who changed a record, what changed, and when, so we can review decisions, track errors, and answer questions if there’s ever a dispute. I’d also want those logs to be searchable enough for management to review them when needed."

## 4. Business Rules and Constraints

### [BR-001] (stated)
The system shall prevent staff from placing too many children in a classroom.

**Source Evidence:**
- `[interview_turn:T020]` "Family registration should let us create and maintain a complete family profile with parent or guardian contact details and linked children, so we don’t have to re-enter the same information in different places. Enrollment and waiting list management should show us which children are enrolled, which are pending, and where they stand on the waiting list, so we can move children in as openings come up. Classroom capacity tracking should prevent us from placing too many children in a room and give staff a quick view of available spots by classroom and age group."

### [BR-002] (stated)
Role-based access control shall restrict each employee to seeing and editing only the parts of the system that match their job.

**Source Evidence:**
- `[interview_turn:T016]` "Yes, I’d consider role-based access control a core requirement because of the sensitivity of family, billing, and child health information. The audit trail is also very important, and I’d lean toward treating it as core as well since we need accountability and a way to trace updates."
- `[interview_turn:T024]` "Role-based access control should make sure each employee only sees and edits the parts of the system that match their job, so for example office staff, teachers, and administrators don’t all have the same access. The audit trail should record who changed a record, what changed, and when, so we can review decisions, track errors, and answer questions if there’s ever a dispute. I’d also want those logs to be searchable enough for management to review them when needed."

### [BR-003] (stated)
Role-based access control shall ensure that office staff, teachers, and administrators do not all have the same access.

**Source Evidence:**
- `[interview_turn:T024]` "Role-based access control should make sure each employee only sees and edits the parts of the system that match their job, so for example office staff, teachers, and administrators don’t all have the same access. The audit trail should record who changed a record, what changed, and when, so we can review decisions, track errors, and answer questions if there’s ever a dispute. I’d also want those logs to be searchable enough for management to review them when needed."

### [BR-004] (stated)
Only authorized staff shall be able to see or change sensitive information.

**Source Evidence:**
- `[interview_turn:T014]` "Nothing major beyond what we’ve discussed, but role-based access is important so only authorized staff can see or change sensitive information. It would also help if the system kept an audit trail or history of changes, since we may need to know who updated a record and when. That said, I’d want to verify whether those are must-haves or nice-to-haves with the rest of the team."

### [BR-005] (stated)
The system shall maintain an audit trail that records who changed a record, what changed, and when.

**Source Evidence:**
- `[interview_turn:T016]` "Yes, I’d consider role-based access control a core requirement because of the sensitivity of family, billing, and child health information. The audit trail is also very important, and I’d lean toward treating it as core as well since we need accountability and a way to trace updates."
- `[interview_turn:T024]` "Role-based access control should make sure each employee only sees and edits the parts of the system that match their job, so for example office staff, teachers, and administrators don’t all have the same access. The audit trail should record who changed a record, what changed, and when, so we can review decisions, track errors, and answer questions if there’s ever a dispute. I’d also want those logs to be searchable enough for management to review them when needed."

### [BR-006] (stated)
Audit trail logs shall be searchable enough for management to review them when needed.

**Source Evidence:**
- `[interview_turn:T024]` "Role-based access control should make sure each employee only sees and edits the parts of the system that match their job, so for example office staff, teachers, and administrators don’t all have the same access. The audit trail should record who changed a record, what changed, and when, so we can review decisions, track errors, and answer questions if there’s ever a dispute. I’d also want those logs to be searchable enough for management to review them when needed."

## 5. Data and External Interfaces

None specified.

## 6. Quality Requirements

### [QR-001] (stated)
The system shall reduce manual work for staff.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "A child care center needs a web-based management system that reduces administrative work and lets employees share information through a central database. Administrators should be able to register families and manage enrollment, classroom capacity, and waiting lists, while authorized staff need support for routine activities such as tracking child immunizations, processing invoices, and producing information for customers and center operations."
- `[interview_turn:T004]` "I’m one of the stakeholders for the child care center, and I’m speaking from the operational side of the business. My focus is on how the staff and administrators will use the system day to day to reduce manual work and keep family, child, and billing information organized in one place."
- `[interview_turn:T034]` "We’d consider it successful if it reduces the amount of manual work staff do and keeps family, enrollment, and billing information accurate in one place. It should also make it easier to find current child and classroom information without calling around or checking paper files. If staff can use it reliably in day-to-day operations without causing more confusion, that would be a good sign."

### [QR-002] (stated)
The system shall keep family, enrollment, and billing information accurate in one place.

**Source Evidence:**
- `[interview_turn:T034]` "We’d consider it successful if it reduces the amount of manual work staff do and keeps family, enrollment, and billing information accurate in one place. It should also make it easier to find current child and classroom information without calling around or checking paper files. If staff can use it reliably in day-to-day operations without causing more confusion, that would be a good sign."

### [QR-003] (stated)
The system shall be easy enough for staff to learn quickly.

**Source Evidence:**
- `[interview_turn:T036]` "One thing I’d add is reporting for the center’s internal operations, like enrollment counts, vacancies, outstanding balances, and upcoming immunization issues, because that would help management make decisions faster. I’d also want the system to be easy enough for staff to learn quickly, since not everyone will be very technical. Beyond that, nothing major comes to mind right now, but I’d want to review anything related to security and data privacy before finalizing."

### [QR-004] (stated)
The system shall be usable reliably in day-to-day operations without causing more confusion.

**Source Evidence:**
- `[interview_turn:T034]` "We’d consider it successful if it reduces the amount of manual work staff do and keeps family, enrollment, and billing information accurate in one place. It should also make it easier to find current child and classroom information without calling around or checking paper files. If staff can use it reliably in day-to-day operations without causing more confusion, that would be a good sign."

## 7. Exceptions and Boundary Conditions

None specified.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
The exact parent-facing visibility model, including how much information is shown directly to parents versus generated by staff, remains to be confirmed.

**Source Evidence:**
- `[interview_turn:T012]` "Yes, I think so. Parents will need some kind of information output, especially around enrollment status, billing, and maybe child record-related updates that are appropriate to share. I’m not sure yet how much should be visible directly to parents versus generated by staff, so that would need to be confirmed with the team."

### [UN-002]
The exact special waiting list priority rules, such as sibling priority or approved dates, remain to be confirmed.

**Source Evidence:**
- `[interview_turn:T022]` "When a spot opens, staff should be able to see who is next in line for the right classroom or age group and move that child from waiting list to active enrollment with a few steps. I’d expect the system to check capacity before confirming the move, and if possible it should notify staff so they know which child is eligible next. If there are special priorities, like siblings or approved dates, that should probably be reflected too, but I’d need to confirm the exact rules."

### [UN-003]
Compliance and licensing requirements that may affect the data stored and reported remain to be confirmed.

**Source Evidence:**
- `[interview_turn:T032]` "The main people to include would be the administrators, office staff, teachers, and probably the parents or guardians, because they all use or depend on the system in different ways. Administrators care about enrollment, reporting, and control; teachers need quick access to child and classroom information; office staff handle billing and records; and parents care about clear communication and accurate account information. I’d also consider compliance or licensing requirements, since those can affect what data we need to store and report."

### [UN-004]
Security and data privacy requirements must be reviewed before finalization.

**Source Evidence:**
- `[interview_turn:T036]` "One thing I’d add is reporting for the center’s internal operations, like enrollment counts, vacancies, outstanding balances, and upcoming immunization issues, because that would help management make decisions faster. I’d also want the system to be easy enough for staff to learn quickly, since not everyone will be very technical. Beyond that, nothing major comes to mind right now, but I’d want to review anything related to security and data privacy before finalizing."
