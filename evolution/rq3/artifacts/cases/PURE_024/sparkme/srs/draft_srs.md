# Software Requirements Specification: Nenios Child Care Management

## 1. Scope and Context

### [SC-001] (stated)
The system shall be a web-based child care management system that uses a central database to reduce administrative work and support staff information sharing.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "A child care center needs a web-based management system that reduces administrative work and lets employees share information through a central database. Administrators should be able to register families and manage enrollment, classroom capacity, and waiting lists, while authorized staff need support for routine activities such as tracking child immunizations, processing invoices, and producing information for customers and center operations."
- `[interview_turn:T002]` "We need a central web system because a lot of our information is still scattered across paper files, spreadsheets, and separate staff notes, which makes it easy to miss things or duplicate work. The biggest issues are keeping family records accurate, managing enrollments against classroom limits, and making sure staff can quickly see things like immunizations, billing status, and who is on the waiting list. We also want to cut down on time spent on routine admin tasks so the center can focus more on the children and parents."

## 2. Actors

### [ST-001] (stated)
The system shall support administrators, teachers, and office or front-desk staff as user roles.

**Source Evidence:**
- `[interview_turn:T018]` "Administrators handle registration, enrollment, classroom assignments, capacity, and waiting lists, so they need the broadest access to family and child records. Teachers or classroom staff mainly use the system to look up children in their care, check immunizations or basic profile details, and record day-to-day information relevant to the classroom. Front-desk or office staff would likely manage check-in style administrative work, answer parent questions, and help with invoices or general records, but I’d need to confirm the exact role names we want to use."
- `[interview_turn:T020]` "We usually think of them as administrators, teachers, and office or front-desk staff, though the exact titles can vary a bit by center. There are definitely overlaps, because some people help with both classroom and administrative tasks, and a manager might also step in to cover front-desk duties when needed. The system should probably support multiple roles for one user rather than forcing a single fixed title."

### [ST-002] (stated)
The system shall allow a single user to have multiple roles rather than forcing one fixed role.

**Source Evidence:**
- `[interview_turn:T020]` "We usually think of them as administrators, teachers, and office or front-desk staff, though the exact titles can vary a bit by center. There are definitely overlaps, because some people help with both classroom and administrative tasks, and a manager might also step in to cover front-desk duties when needed. The system should probably support multiple roles for one user rather than forcing a single fixed title."

## 3. Functional Requirements

### [FR-001] (stated)
The system shall allow administrators to register families.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "A child care center needs a web-based management system that reduces administrative work and lets employees share information through a central database. Administrators should be able to register families and manage enrollment, classroom capacity, and waiting lists, while authorized staff need support for routine activities such as tracking child immunizations, processing invoices, and producing information for customers and center operations."
- `[interview_turn:T018]` "Administrators handle registration, enrollment, classroom assignments, capacity, and waiting lists, so they need the broadest access to family and child records. Teachers or classroom staff mainly use the system to look up children in their care, check immunizations or basic profile details, and record day-to-day information relevant to the classroom. Front-desk or office staff would likely manage check-in style administrative work, answer parent questions, and help with invoices or general records, but I’d need to confirm the exact role names we want to use."

### [FR-002] (stated)
The system shall allow administrators to manage enrollments.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "A child care center needs a web-based management system that reduces administrative work and lets employees share information through a central database. Administrators should be able to register families and manage enrollment, classroom capacity, and waiting lists, while authorized staff need support for routine activities such as tracking child immunizations, processing invoices, and producing information for customers and center operations."
- `[interview_turn:T018]` "Administrators handle registration, enrollment, classroom assignments, capacity, and waiting lists, so they need the broadest access to family and child records. Teachers or classroom staff mainly use the system to look up children in their care, check immunizations or basic profile details, and record day-to-day information relevant to the classroom. Front-desk or office staff would likely manage check-in style administrative work, answer parent questions, and help with invoices or general records, but I’d need to confirm the exact role names we want to use."
- `[interview_turn:T022]` "Administrators are usually dealing with enrollment, waiting lists, room capacity, and approvals, so they spend a lot of time updating family and child records and checking overall center status. Teachers use it more during the day to confirm which children are in their room, review important child details like allergies or immunizations, and update routine classroom-related notes if that’s part of the workflow. Office or front-desk staff are often the first point of contact, so they’ll look up family information, help with invoicing questions, and make sure basic records are current when parents call or come in."

### [FR-003] (stated)
The system shall allow administrators to manage classroom assignments.

**Source Evidence:**
- `[interview_turn:T018]` "Administrators handle registration, enrollment, classroom assignments, capacity, and waiting lists, so they need the broadest access to family and child records. Teachers or classroom staff mainly use the system to look up children in their care, check immunizations or basic profile details, and record day-to-day information relevant to the classroom. Front-desk or office staff would likely manage check-in style administrative work, answer parent questions, and help with invoices or general records, but I’d need to confirm the exact role names we want to use."
- `[interview_turn:T022]` "Administrators are usually dealing with enrollment, waiting lists, room capacity, and approvals, so they spend a lot of time updating family and child records and checking overall center status. Teachers use it more during the day to confirm which children are in their room, review important child details like allergies or immunizations, and update routine classroom-related notes if that’s part of the workflow. Office or front-desk staff are often the first point of contact, so they’ll look up family information, help with invoicing questions, and make sure basic records are current when parents call or come in."

### [FR-004] (stated)
The system shall allow administrators to manage classroom capacity.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "A child care center needs a web-based management system that reduces administrative work and lets employees share information through a central database. Administrators should be able to register families and manage enrollment, classroom capacity, and waiting lists, while authorized staff need support for routine activities such as tracking child immunizations, processing invoices, and producing information for customers and center operations."
- `[interview_turn:T018]` "Administrators handle registration, enrollment, classroom assignments, capacity, and waiting lists, so they need the broadest access to family and child records. Teachers or classroom staff mainly use the system to look up children in their care, check immunizations or basic profile details, and record day-to-day information relevant to the classroom. Front-desk or office staff would likely manage check-in style administrative work, answer parent questions, and help with invoices or general records, but I’d need to confirm the exact role names we want to use."
- `[interview_turn:T022]` "Administrators are usually dealing with enrollment, waiting lists, room capacity, and approvals, so they spend a lot of time updating family and child records and checking overall center status. Teachers use it more during the day to confirm which children are in their room, review important child details like allergies or immunizations, and update routine classroom-related notes if that’s part of the workflow. Office or front-desk staff are often the first point of contact, so they’ll look up family information, help with invoicing questions, and make sure basic records are current when parents call or come in."

### [FR-005] (stated)
The system shall allow administrators to manage waiting lists.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "A child care center needs a web-based management system that reduces administrative work and lets employees share information through a central database. Administrators should be able to register families and manage enrollment, classroom capacity, and waiting lists, while authorized staff need support for routine activities such as tracking child immunizations, processing invoices, and producing information for customers and center operations."
- `[interview_turn:T018]` "Administrators handle registration, enrollment, classroom assignments, capacity, and waiting lists, so they need the broadest access to family and child records. Teachers or classroom staff mainly use the system to look up children in their care, check immunizations or basic profile details, and record day-to-day information relevant to the classroom. Front-desk or office staff would likely manage check-in style administrative work, answer parent questions, and help with invoices or general records, but I’d need to confirm the exact role names we want to use."
- `[interview_turn:T022]` "Administrators are usually dealing with enrollment, waiting lists, room capacity, and approvals, so they spend a lot of time updating family and child records and checking overall center status. Teachers use it more during the day to confirm which children are in their room, review important child details like allergies or immunizations, and update routine classroom-related notes if that’s part of the workflow. Office or front-desk staff are often the first point of contact, so they’ll look up family information, help with invoicing questions, and make sure basic records are current when parents call or come in."

### [FR-006] (stated)
The system shall allow authorized staff to track child immunizations.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "A child care center needs a web-based management system that reduces administrative work and lets employees share information through a central database. Administrators should be able to register families and manage enrollment, classroom capacity, and waiting lists, while authorized staff need support for routine activities such as tracking child immunizations, processing invoices, and producing information for customers and center operations."
- `[interview_turn:T002]` "We need a central web system because a lot of our information is still scattered across paper files, spreadsheets, and separate staff notes, which makes it easy to miss things or duplicate work. The biggest issues are keeping family records accurate, managing enrollments against classroom limits, and making sure staff can quickly see things like immunizations, billing status, and who is on the waiting list. We also want to cut down on time spent on routine admin tasks so the center can focus more on the children and parents."
- `[interview_turn:T018]` "Administrators handle registration, enrollment, classroom assignments, capacity, and waiting lists, so they need the broadest access to family and child records. Teachers or classroom staff mainly use the system to look up children in their care, check immunizations or basic profile details, and record day-to-day information relevant to the classroom. Front-desk or office staff would likely manage check-in style administrative work, answer parent questions, and help with invoices or general records, but I’d need to confirm the exact role names we want to use."
- `[interview_turn:T022]` "Administrators are usually dealing with enrollment, waiting lists, room capacity, and approvals, so they spend a lot of time updating family and child records and checking overall center status. Teachers use it more during the day to confirm which children are in their room, review important child details like allergies or immunizations, and update routine classroom-related notes if that’s part of the workflow. Office or front-desk staff are often the first point of contact, so they’ll look up family information, help with invoicing questions, and make sure basic records are current when parents call or come in."

### [FR-007] (stated)
The system shall allow authorized staff to process invoices.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "A child care center needs a web-based management system that reduces administrative work and lets employees share information through a central database. Administrators should be able to register families and manage enrollment, classroom capacity, and waiting lists, while authorized staff need support for routine activities such as tracking child immunizations, processing invoices, and producing information for customers and center operations."
- `[interview_turn:T018]` "Administrators handle registration, enrollment, classroom assignments, capacity, and waiting lists, so they need the broadest access to family and child records. Teachers or classroom staff mainly use the system to look up children in their care, check immunizations or basic profile details, and record day-to-day information relevant to the classroom. Front-desk or office staff would likely manage check-in style administrative work, answer parent questions, and help with invoices or general records, but I’d need to confirm the exact role names we want to use."
- `[interview_turn:T022]` "Administrators are usually dealing with enrollment, waiting lists, room capacity, and approvals, so they spend a lot of time updating family and child records and checking overall center status. Teachers use it more during the day to confirm which children are in their room, review important child details like allergies or immunizations, and update routine classroom-related notes if that’s part of the workflow. Office or front-desk staff are often the first point of contact, so they’ll look up family information, help with invoicing questions, and make sure basic records are current when parents call or come in."

### [FR-008] (stated)
The system shall allow staff to look up family and child information.

**Source Evidence:**
- `[interview_turn:T004]` "The main goal is to make daily administration much faster and more reliable, especially around enrollment, billing, and record keeping. We want staff to have one trusted place for family and child information so they are not chasing down paperwork or checking multiple systems. Ideally, it should also improve communication and give us better visibility into capacity and waiting lists so decisions can be made more quickly."
- `[interview_turn:T018]` "Administrators handle registration, enrollment, classroom assignments, capacity, and waiting lists, so they need the broadest access to family and child records. Teachers or classroom staff mainly use the system to look up children in their care, check immunizations or basic profile details, and record day-to-day information relevant to the classroom. Front-desk or office staff would likely manage check-in style administrative work, answer parent questions, and help with invoices or general records, but I’d need to confirm the exact role names we want to use."
- `[interview_turn:T022]` "Administrators are usually dealing with enrollment, waiting lists, room capacity, and approvals, so they spend a lot of time updating family and child records and checking overall center status. Teachers use it more during the day to confirm which children are in their room, review important child details like allergies or immunizations, and update routine classroom-related notes if that’s part of the workflow. Office or front-desk staff are often the first point of contact, so they’ll look up family information, help with invoicing questions, and make sure basic records are current when parents call or come in."

### [FR-009] (stated)
The system shall allow office or front-desk staff to help with invoicing questions.

**Source Evidence:**
- `[interview_turn:T018]` "Administrators handle registration, enrollment, classroom assignments, capacity, and waiting lists, so they need the broadest access to family and child records. Teachers or classroom staff mainly use the system to look up children in their care, check immunizations or basic profile details, and record day-to-day information relevant to the classroom. Front-desk or office staff would likely manage check-in style administrative work, answer parent questions, and help with invoices or general records, but I’d need to confirm the exact role names we want to use."
- `[interview_turn:T022]` "Administrators are usually dealing with enrollment, waiting lists, room capacity, and approvals, so they spend a lot of time updating family and child records and checking overall center status. Teachers use it more during the day to confirm which children are in their room, review important child details like allergies or immunizations, and update routine classroom-related notes if that’s part of the workflow. Office or front-desk staff are often the first point of contact, so they’ll look up family information, help with invoicing questions, and make sure basic records are current when parents call or come in."

### [FR-010] (stated)
The system shall allow teachers to review child details such as allergies and immunizations.

**Source Evidence:**
- `[interview_turn:T022]` "Administrators are usually dealing with enrollment, waiting lists, room capacity, and approvals, so they spend a lot of time updating family and child records and checking overall center status. Teachers use it more during the day to confirm which children are in their room, review important child details like allergies or immunizations, and update routine classroom-related notes if that’s part of the workflow. Office or front-desk staff are often the first point of contact, so they’ll look up family information, help with invoicing questions, and make sure basic records are current when parents call or come in."

### [FR-011] (conditional)
The system shall allow teachers to record routine classroom-related notes if that is part of the workflow.

**Source Evidence:**
- `[interview_turn:T022]` "Administrators are usually dealing with enrollment, waiting lists, room capacity, and approvals, so they spend a lot of time updating family and child records and checking overall center status. Teachers use it more during the day to confirm which children are in their room, review important child details like allergies or immunizations, and update routine classroom-related notes if that’s part of the workflow. Office or front-desk staff are often the first point of contact, so they’ll look up family information, help with invoicing questions, and make sure basic records are current when parents call or come in."

### [FR-012] (stated)
The system shall allow office or front-desk staff to look up family information and help keep basic records current.

**Source Evidence:**
- `[interview_turn:T022]` "Administrators are usually dealing with enrollment, waiting lists, room capacity, and approvals, so they spend a lot of time updating family and child records and checking overall center status. Teachers use it more during the day to confirm which children are in their room, review important child details like allergies or immunizations, and update routine classroom-related notes if that’s part of the workflow. Office or front-desk staff are often the first point of contact, so they’ll look up family information, help with invoicing questions, and make sure basic records are current when parents call or come in."

### [FR-013] (stated)
The system shall support routine administrative tasks so the center can reduce time spent on administration.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "A child care center needs a web-based management system that reduces administrative work and lets employees share information through a central database. Administrators should be able to register families and manage enrollment, classroom capacity, and waiting lists, while authorized staff need support for routine activities such as tracking child immunizations, processing invoices, and producing information for customers and center operations."
- `[interview_turn:T002]` "We need a central web system because a lot of our information is still scattered across paper files, spreadsheets, and separate staff notes, which makes it easy to miss things or duplicate work. The biggest issues are keeping family records accurate, managing enrollments against classroom limits, and making sure staff can quickly see things like immunizations, billing status, and who is on the waiting list. We also want to cut down on time spent on routine admin tasks so the center can focus more on the children and parents."
- `[interview_turn:T004]` "The main goal is to make daily administration much faster and more reliable, especially around enrollment, billing, and record keeping. We want staff to have one trusted place for family and child information so they are not chasing down paperwork or checking multiple systems. Ideally, it should also improve communication and give us better visibility into capacity and waiting lists so decisions can be made more quickly."

### [FR-014] (stated)
The system shall support parent notices and reminders through email integration from day one.

**Source Evidence:**
- `[interview_turn:T008]` "I know email integration will be important because we send notices to parents all the time, and it would be helpful if the system could generate or send those messages directly. For accounting, we do use software outside the child care system, but I’m not sure yet which product is the one we’d need to connect to. Beyond that, I’d need to verify whether we also need calendar, SMS, or payment processor integrations."
- `[interview_turn:T010]` "Email notifications feel essential from day one because we rely on them for routine parent communication and reminders. Accounting connectivity is also important, but if it takes longer to sort out, we could start with invoice generation in the system and handle export or manual transfer as a temporary step. Calendar and SMS would be nice to have, but I’d see those as later enhancements unless we find a strong operational need."
- `[interview_turn:T034]` "We definitely use email and some kind of accounting or billing tool already, and we may also rely on calendar tools for scheduling and reminders. I’d like the new system to share invoice and payment information with accounting, and maybe send notifications or reminders through email without staff having to copy details manually. If there’s a payment processor involved, it would be helpful if payments could be recorded automatically, but I’d need to verify what specific products we already have."

### [FR-015] (conditional)
The system shall support invoice generation even if accounting connectivity is not available immediately.

**Source Evidence:**
- `[interview_turn:T010]` "Email notifications feel essential from day one because we rely on them for routine parent communication and reminders. Accounting connectivity is also important, but if it takes longer to sort out, we could start with invoice generation in the system and handle export or manual transfer as a temporary step. Calendar and SMS would be nice to have, but I’d see those as later enhancements unless we find a strong operational need."

### [FR-016] (conditional)
The system shall support exporting or manual transfer of invoice data as a temporary step when accounting connectivity is not yet available.

**Source Evidence:**
- `[interview_turn:T010]` "Email notifications feel essential from day one because we rely on them for routine parent communication and reminders. Accounting connectivity is also important, but if it takes longer to sort out, we could start with invoice generation in the system and handle export or manual transfer as a temporary step. Calendar and SMS would be nice to have, but I’d see those as later enhancements unless we find a strong operational need."

### [FR-017] (stated)
The system shall allow staff to log in from shared computers without friction.

**Source Evidence:**
- `[interview_turn:T012]` "The main limitation is that not every staff member has a dedicated device, so the system should let multiple people log in from shared computers without friction. Internet is usually fine, but there can be occasional slowdowns, so it would help if common tasks still loaded quickly and didn’t require a lot of back-and-forth refreshing. I don’t think we need offline mode right now, but we do want the system to be forgiving if the connection is temporarily unreliable."

### [FR-018] (stated)
The system shall support browser-based use without special software.

**Source Evidence:**
- `[interview_turn:T006]` "We’re assuming staff will use standard office computers and probably tablets in some areas, so it should work well in a browser without special software. Internet access is generally available at the center, but we’d want the system to be stable and easy to use if the connection is slow. I know we use some external tools for email and possibly accounting, but I’d need to check with the team before saying exactly what integrations are required."

### [FR-019] (stated)
The system shall support use on tablets.

**Source Evidence:**
- `[interview_turn:T006]` "We’re assuming staff will use standard office computers and probably tablets in some areas, so it should work well in a browser without special software. Internet access is generally available at the center, but we’d want the system to be stable and easy to use if the connection is slow. I know we use some external tools for email and possibly accounting, but I’d need to check with the team before saying exactly what integrations are required."
- `[interview_turn:T054]` "The staff won’t all be very technical, so the system needs to be simple and consistent, with clear labels and not too many clicks for common tasks. It should work well on a browser and be readable on tablets too, since some people may use it at the front desk or while moving around the center. Accessibility matters as well, so good contrast, keyboard support, and screen-reader-friendly design would be important for anyone with visual or mobility needs."

### [FR-020] (stated)
The system shall support temporary interruptions by saving work in draft or autosaved form so staff do not lose entered data.

**Source Evidence:**
- `[interview_turn:T024]` "It should save work as safely as possible so people don’t lose a whole enrollment or invoice if the connection drops or they click the wrong thing. At minimum, I’d want some kind of draft or confirmation step before final submission, plus a clear way to resume or correct a task if it was interrupted. If something does go wrong, staff should be able to see whether it actually went through and get a simple message telling them what to do next."
- `[interview_turn:T036]` "Yes, that can happen if the network drops, if someone closes the browser, or if a staff member realizes they entered something wrong halfway through. The system should clearly show whether the task was saved as a draft or fully completed, and it should let staff safely resume or cancel without creating duplicate records. For billing especially, I’d want it to avoid double charges and make it easy to see what already went through versus what still needs attention."
- `[interview_turn:T040]` "If a task gets interrupted, I’d want the system to save progress automatically in the background so staff do not lose everything they entered. When they come back, it should reopen the form with the last saved values and a clear message saying it was saved as a draft or completed successfully. For invoices or enrollments, it should also show a status like pending, submitted, or paid so staff can immediately tell whether they need to finish anything or whether it already went through."
- `[interview_turn:T056]` "Some staff may have limited experience with software, so built-in help tips and clear error messages would be very useful. It would also help to have larger text options, simple navigation, and forms that don’t lose entered data if someone makes a mistake. For support tools, I’d like a search function that is easy to use and maybe printable views or summaries for staff who still rely on paper in some situations."

### [FR-021] (stated)
The system shall allow staff to resume interrupted enrollment or invoice tasks from the last saved values.

**Source Evidence:**
- `[interview_turn:T024]` "It should save work as safely as possible so people don’t lose a whole enrollment or invoice if the connection drops or they click the wrong thing. At minimum, I’d want some kind of draft or confirmation step before final submission, plus a clear way to resume or correct a task if it was interrupted. If something does go wrong, staff should be able to see whether it actually went through and get a simple message telling them what to do next."
- `[interview_turn:T040]` "If a task gets interrupted, I’d want the system to save progress automatically in the background so staff do not lose everything they entered. When they come back, it should reopen the form with the last saved values and a clear message saying it was saved as a draft or completed successfully. For invoices or enrollments, it should also show a status like pending, submitted, or paid so staff can immediately tell whether they need to finish anything or whether it already went through."

### [FR-022] (stated)
The system shall allow staff to cancel or correct interrupted tasks without creating duplicate records.

**Source Evidence:**
- `[interview_turn:T024]` "It should save work as safely as possible so people don’t lose a whole enrollment or invoice if the connection drops or they click the wrong thing. At minimum, I’d want some kind of draft or confirmation step before final submission, plus a clear way to resume or correct a task if it was interrupted. If something does go wrong, staff should be able to see whether it actually went through and get a simple message telling them what to do next."
- `[interview_turn:T036]` "Yes, that can happen if the network drops, if someone closes the browser, or if a staff member realizes they entered something wrong halfway through. The system should clearly show whether the task was saved as a draft or fully completed, and it should let staff safely resume or cancel without creating duplicate records. For billing especially, I’d want it to avoid double charges and make it easy to see what already went through versus what still needs attention."

### [FR-023] (stated)
The system shall show whether an enrollment or invoice task was saved as a draft, submitted, completed, or paid.

**Source Evidence:**
- `[interview_turn:T036]` "Yes, that can happen if the network drops, if someone closes the browser, or if a staff member realizes they entered something wrong halfway through. The system should clearly show whether the task was saved as a draft or fully completed, and it should let staff safely resume or cancel without creating duplicate records. For billing especially, I’d want it to avoid double charges and make it easy to see what already went through versus what still needs attention."
- `[interview_turn:T040]` "If a task gets interrupted, I’d want the system to save progress automatically in the background so staff do not lose everything they entered. When they come back, it should reopen the form with the last saved values and a clear message saying it was saved as a draft or completed successfully. For invoices or enrollments, it should also show a status like pending, submitted, or paid so staff can immediately tell whether they need to finish anything or whether it already went through."
- `[interview_turn:T042]` "I’d prefer a warning if someone else is already editing the same record, with the option to open it read-only or wait until it’s available. If both people do make changes, the system should not silently overwrite anything; it should force a review of the conflicting fields and show who changed what and when. For payments, the record should show a simple current status, like unpaid, partial, or paid, plus a visible transaction history with dates, amounts, and any refunds or adjustments so staff can follow the full trail."

### [FR-024] (stated)
The system shall warn staff when another user is already editing the same record.

**Source Evidence:**
- `[interview_turn:T038]` "One tricky case is when two staff members are looking at the same family or invoice at the same time and both try to update it, which can cause conflicting information. Another is when a partial payment is entered and then the rest comes in later, so staff need to know whether the invoice is still open, partly paid, or fully settled. The system should show the last saved status very clearly, warn about concurrent edits, and keep a visible history so staff can tell what happened without guessing."
- `[interview_turn:T042]` "I’d prefer a warning if someone else is already editing the same record, with the option to open it read-only or wait until it’s available. If both people do make changes, the system should not silently overwrite anything; it should force a review of the conflicting fields and show who changed what and when. For payments, the record should show a simple current status, like unpaid, partial, or paid, plus a visible transaction history with dates, amounts, and any refunds or adjustments so staff can follow the full trail."

### [FR-025] (stated)
The system shall allow a record opened under concurrent editing to be viewed read-only or waited on until it becomes available.

**Source Evidence:**
- `[interview_turn:T042]` "I’d prefer a warning if someone else is already editing the same record, with the option to open it read-only or wait until it’s available. If both people do make changes, the system should not silently overwrite anything; it should force a review of the conflicting fields and show who changed what and when. For payments, the record should show a simple current status, like unpaid, partial, or paid, plus a visible transaction history with dates, amounts, and any refunds or adjustments so staff can follow the full trail."

### [FR-026] (stated)
The system shall force a review of conflicting fields if two users make changes to the same record.

**Source Evidence:**
- `[interview_turn:T042]` "I’d prefer a warning if someone else is already editing the same record, with the option to open it read-only or wait until it’s available. If both people do make changes, the system should not silently overwrite anything; it should force a review of the conflicting fields and show who changed what and when. For payments, the record should show a simple current status, like unpaid, partial, or paid, plus a visible transaction history with dates, amounts, and any refunds or adjustments so staff can follow the full trail."

### [FR-027] (stated)
The system shall display who changed a record and when.

**Source Evidence:**
- `[interview_turn:T038]` "One tricky case is when two staff members are looking at the same family or invoice at the same time and both try to update it, which can cause conflicting information. Another is when a partial payment is entered and then the rest comes in later, so staff need to know whether the invoice is still open, partly paid, or fully settled. The system should show the last saved status very clearly, warn about concurrent edits, and keep a visible history so staff can tell what happened without guessing."
- `[interview_turn:T042]` "I’d prefer a warning if someone else is already editing the same record, with the option to open it read-only or wait until it’s available. If both people do make changes, the system should not silently overwrite anything; it should force a review of the conflicting fields and show who changed what and when. For payments, the record should show a simple current status, like unpaid, partial, or paid, plus a visible transaction history with dates, amounts, and any refunds or adjustments so staff can follow the full trail."
- `[interview_turn:T044]` "The biggest concern is making sure staff only see the children and families they actually need for their job, especially if someone works across classrooms or only helps with billing. I’d want role-based access with the ability to limit by function and maybe by classroom or site, and sensitive details like health information should be restricted more tightly than general contact info. The system should also keep an audit log of logins and changes to important records, including who viewed or edited them and when, so we can review issues if something looks off."

### [FR-028] (stated)
The system shall show the last saved status of a record clearly.

**Source Evidence:**
- `[interview_turn:T038]` "One tricky case is when two staff members are looking at the same family or invoice at the same time and both try to update it, which can cause conflicting information. Another is when a partial payment is entered and then the rest comes in later, so staff need to know whether the invoice is still open, partly paid, or fully settled. The system should show the last saved status very clearly, warn about concurrent edits, and keep a visible history so staff can tell what happened without guessing."

### [FR-029] (stated)
The system shall show a visible history of payment transactions, including dates, amounts, refunds, and adjustments.

**Source Evidence:**
- `[interview_turn:T042]` "I’d prefer a warning if someone else is already editing the same record, with the option to open it read-only or wait until it’s available. If both people do make changes, the system should not silently overwrite anything; it should force a review of the conflicting fields and show who changed what and when. For payments, the record should show a simple current status, like unpaid, partial, or paid, plus a visible transaction history with dates, amounts, and any refunds or adjustments so staff can follow the full trail."

### [FR-030] (stated)
The system shall show invoice payment states as unpaid, partial, or paid.

**Source Evidence:**
- `[interview_turn:T042]` "I’d prefer a warning if someone else is already editing the same record, with the option to open it read-only or wait until it’s available. If both people do make changes, the system should not silently overwrite anything; it should force a review of the conflicting fields and show who changed what and when. For payments, the record should show a simple current status, like unpaid, partial, or paid, plus a visible transaction history with dates, amounts, and any refunds or adjustments so staff can follow the full trail."

### [FR-031] (stated)
The system shall show whether a payment or invoice task has gone through and what still needs attention.

**Source Evidence:**
- `[interview_turn:T024]` "It should save work as safely as possible so people don’t lose a whole enrollment or invoice if the connection drops or they click the wrong thing. At minimum, I’d want some kind of draft or confirmation step before final submission, plus a clear way to resume or correct a task if it was interrupted. If something does go wrong, staff should be able to see whether it actually went through and get a simple message telling them what to do next."
- `[interview_turn:T036]` "Yes, that can happen if the network drops, if someone closes the browser, or if a staff member realizes they entered something wrong halfway through. The system should clearly show whether the task was saved as a draft or fully completed, and it should let staff safely resume or cancel without creating duplicate records. For billing especially, I’d want it to avoid double charges and make it easy to see what already went through versus what still needs attention."
- `[interview_turn:T040]` "If a task gets interrupted, I’d want the system to save progress automatically in the background so staff do not lose everything they entered. When they come back, it should reopen the form with the last saved values and a clear message saying it was saved as a draft or completed successfully. For invoices or enrollments, it should also show a status like pending, submitted, or paid so staff can immediately tell whether they need to finish anything or whether it already went through."

### [FR-032] (stated)
The system shall allow staff to create family and child records when someone first applies or enrolls.

**Source Evidence:**
- `[interview_turn:T030]` "Family and child records are usually created when someone first applies or enrolls, and then they get updated whenever contact details, emergency contacts, medical information, or billing details change. If a child leaves the center, we would normally mark the record inactive or archived rather than delete it, so we still have the history for reporting and billing reference. I’m not sure we have a fixed retention rule yet, so that would need to be checked with management or whatever compliance requirements apply."

### [FR-033] (stated)
The system shall allow family and child records to be updated when contact details, emergency contacts, medical information, or billing details change.

**Source Evidence:**
- `[interview_turn:T030]` "Family and child records are usually created when someone first applies or enrolls, and then they get updated whenever contact details, emergency contacts, medical information, or billing details change. If a child leaves the center, we would normally mark the record inactive or archived rather than delete it, so we still have the history for reporting and billing reference. I’m not sure we have a fixed retention rule yet, so that would need to be checked with management or whatever compliance requirements apply."

### [FR-034] (stated)
The system shall allow child records to be marked inactive or archived when a child leaves the center.

**Source Evidence:**
- `[interview_turn:T030]` "Family and child records are usually created when someone first applies or enrolls, and then they get updated whenever contact details, emergency contacts, medical information, or billing details change. If a child leaves the center, we would normally mark the record inactive or archived rather than delete it, so we still have the history for reporting and billing reference. I’m not sure we have a fixed retention rule yet, so that would need to be checked with management or whatever compliance requirements apply."
- `[interview_turn:T032]` "Right now it’s mostly informal, and we tend to keep financial records and child history on file for a long time rather than deleting them. Immunization information is kept as long as the child is active and usually archived afterward, since we may need it for reference. I’d want the system to support marking records inactive, archiving them, and only allowing deletion for very limited cases, with an audit trail if possible."
- `[interview_turn:T052]` "Older records should stay accessible for compliance and reference, especially enrollment and billing history, but they could be moved to an archived state once they’re no longer actively used. I’d prefer that archived records are still searchable, just not part of the day-to-day screens unless someone needs them. As the database grows, reports should still run in a reasonable time, and the system should not slow down just because there are years of historical data behind it."

### [FR-035] (stated)
The system shall allow records to be deleted only in very limited cases.

**Source Evidence:**
- `[interview_turn:T032]` "Right now it’s mostly informal, and we tend to keep financial records and child history on file for a long time rather than deleting them. Immunization information is kept as long as the child is active and usually archived afterward, since we may need it for reference. I’d want the system to support marking records inactive, archiving them, and only allowing deletion for very limited cases, with an audit trail if possible."

### [FR-036] (stated)
The system shall support archival of records while preserving history for reporting and billing reference.

**Source Evidence:**
- `[interview_turn:T030]` "Family and child records are usually created when someone first applies or enrolls, and then they get updated whenever contact details, emergency contacts, medical information, or billing details change. If a child leaves the center, we would normally mark the record inactive or archived rather than delete it, so we still have the history for reporting and billing reference. I’m not sure we have a fixed retention rule yet, so that would need to be checked with management or whatever compliance requirements apply."
- `[interview_turn:T032]` "Right now it’s mostly informal, and we tend to keep financial records and child history on file for a long time rather than deleting them. Immunization information is kept as long as the child is active and usually archived afterward, since we may need it for reference. I’d want the system to support marking records inactive, archiving them, and only allowing deletion for very limited cases, with an audit trail if possible."
- `[interview_turn:T052]` "Older records should stay accessible for compliance and reference, especially enrollment and billing history, but they could be moved to an archived state once they’re no longer actively used. I’d prefer that archived records are still searchable, just not part of the day-to-day screens unless someone needs them. As the database grows, reports should still run in a reasonable time, and the system should not slow down just because there are years of historical data behind it."

### [FR-037] (stated)
The system shall keep immunization information as long as the child is active and archive it afterward.

**Source Evidence:**
- `[interview_turn:T032]` "Right now it’s mostly informal, and we tend to keep financial records and child history on file for a long time rather than deleting them. Immunization information is kept as long as the child is active and usually archived afterward, since we may need it for reference. I’d want the system to support marking records inactive, archiving them, and only allowing deletion for very limited cases, with an audit trail if possible."

### [FR-038] (stated)
The system shall support guided import of existing data with validation and error reports.

**Source Evidence:**
- `[interview_turn:T062]` "We’d need to bring over family records, child profiles, classroom assignments, immunization information, billing balances, and maybe some historical attendance or enrollment data if it’s available. The biggest challenge will probably be cleaning up inconsistent data, because some of it may be in spreadsheets or paper files and not always formatted the same way. It would help if the system supported a guided import process with validation, error reports, and a way to review records before they’re finalized."

### [FR-039] (stated)
The system shall support review of imported records before they are finalized.

**Source Evidence:**
- `[interview_turn:T062]` "We’d need to bring over family records, child profiles, classroom assignments, immunization information, billing balances, and maybe some historical attendance or enrollment data if it’s available. The biggest challenge will probably be cleaning up inconsistent data, because some of it may be in spreadsheets or paper files and not always formatted the same way. It would help if the system supported a guided import process with validation, error reports, and a way to review records before they’re finalized."

### [FR-040] (stated)
The system shall automatically map common fields during import and flag uncertain mappings for manual review.

**Source Evidence:**
- `[interview_turn:T064]` "Right now, I’d expect most of it to come from Excel spreadsheets, CSV files, and some scanned paper forms, so there probably won’t be one single standard layout. It would be helpful if the system could automatically map common fields like child name, parent contact, dates, and billing amounts, then flag anything uncertain for manual review. For messy data, I’d want it to suggest possible fixes, but still let a staff member correct or confirm the values before they are loaded."

### [FR-041] (stated)
The system shall suggest possible fixes for messy imported data and allow staff to correct or confirm values before loading.

**Source Evidence:**
- `[interview_turn:T064]` "Right now, I’d expect most of it to come from Excel spreadsheets, CSV files, and some scanned paper forms, so there probably won’t be one single standard layout. It would be helpful if the system could automatically map common fields like child name, parent contact, dates, and billing amounts, then flag anything uncertain for manual review. For messy data, I’d want it to suggest possible fixes, but still let a staff member correct or confirm the values before they are loaded."

### [FR-042] (stated)
The system shall support staged migration of active records before historical records.

**Source Evidence:**
- `[interview_turn:T066]` "We’d probably migrate in stages, starting with the most important active records like families, children, enrollments, classroom assignments, and current billing balances. After that, we’d bring over immunization records and any attendance or historical data we decide we still need for reference. The main challenges will be cleaning up duplicates, filling in missing information, and making sure dates and balances match what we already have in our records."

### [FR-043] (stated)
The system shall support search of archived records.

**Source Evidence:**
- `[interview_turn:T052]` "Older records should stay accessible for compliance and reference, especially enrollment and billing history, but they could be moved to an archived state once they’re no longer actively used. I’d prefer that archived records are still searchable, just not part of the day-to-day screens unless someone needs them. As the database grows, reports should still run in a reasonable time, and the system should not slow down just because there are years of historical data behind it."

### [FR-044] (stated)
The system shall support printable views or summaries.

**Source Evidence:**
- `[interview_turn:T056]` "Some staff may have limited experience with software, so built-in help tips and clear error messages would be very useful. It would also help to have larger text options, simple navigation, and forms that don’t lose entered data if someone makes a mistake. For support tools, I’d like a search function that is easy to use and maybe printable views or summaries for staff who still rely on paper in some situations."

### [FR-045] (stated)
The system shall provide built-in help tips and clear error messages.

**Source Evidence:**
- `[interview_turn:T056]` "Some staff may have limited experience with software, so built-in help tips and clear error messages would be very useful. It would also help to have larger text options, simple navigation, and forms that don’t lose entered data if someone makes a mistake. For support tools, I’d like a search function that is easy to use and maybe printable views or summaries for staff who still rely on paper in some situations."

### [FR-046] (stated)
The system shall provide step-by-step wizards for tasks such as enrolling a new family and setting up invoices.

**Source Evidence:**
- `[interview_turn:T058]` "Yes, step-by-step wizards would be helpful for things like enrolling a new family or setting up invoices, because those are the kinds of tasks people are most likely to do incorrectly if the screen is too busy. Contextual hints near the fields would also be useful, especially for required information or unusual cases. If someone makes a mistake, the system should let them review before submitting, and where possible it should allow edits or reversal without needing an administrator to fix everything manually."

### [FR-047] (stated)
The system shall provide contextual hints near fields, especially for required information or unusual cases.

**Source Evidence:**
- `[interview_turn:T058]` "Yes, step-by-step wizards would be helpful for things like enrolling a new family or setting up invoices, because those are the kinds of tasks people are most likely to do incorrectly if the screen is too busy. Contextual hints near the fields would also be useful, especially for required information or unusual cases. If someone makes a mistake, the system should let them review before submitting, and where possible it should allow edits or reversal without needing an administrator to fix everything manually."

### [FR-048] (stated)
The system shall allow users to review information before submitting complex tasks.

**Source Evidence:**
- `[interview_turn:T058]` "Yes, step-by-step wizards would be helpful for things like enrolling a new family or setting up invoices, because those are the kinds of tasks people are most likely to do incorrectly if the screen is too busy. Contextual hints near the fields would also be useful, especially for required information or unusual cases. If someone makes a mistake, the system should let them review before submitting, and where possible it should allow edits or reversal without needing an administrator to fix everything manually."

### [FR-049] (stated)
The system shall allow edits or reversal of mistakes where possible without requiring manual administrator intervention.

**Source Evidence:**
- `[interview_turn:T058]` "Yes, step-by-step wizards would be helpful for things like enrolling a new family or setting up invoices, because those are the kinds of tasks people are most likely to do incorrectly if the screen is too busy. Contextual hints near the fields would also be useful, especially for required information or unusual cases. If someone makes a mistake, the system should let them review before submitting, and where possible it should allow edits or reversal without needing an administrator to fix everything manually."

### [FR-050] (stated)
The system shall support a pilot with a small group of users before broader rollout.

**Source Evidence:**
- `[interview_turn:T060]` "I’d prefer a pilot with a small group first, probably a few administrators and lead staff, so we can catch problems before everyone depends on it. After that, a phased rollout would feel safer than a big switch-over, especially for enrollment and billing functions. We’d want very little downtime, good training materials, and extra support available during the first few weeks in case staff need quick help or something needs to be corrected."

### [FR-051] (stated)
The system shall support a phased rollout rather than a big switch-over.

**Source Evidence:**
- `[interview_turn:T060]` "I’d prefer a pilot with a small group first, probably a few administrators and lead staff, so we can catch problems before everyone depends on it. After that, a phased rollout would feel safer than a big switch-over, especially for enrollment and billing functions. We’d want very little downtime, good training materials, and extra support available during the first few weeks in case staff need quick help or something needs to be corrected."

### [FR-052] (stated)
The system shall support hands-on training for the pilot group and refresher sessions or job aids for the rest of the staff.

**Source Evidence:**
- `[interview_turn:T068]` "We’d want hands-on training for the pilot group first, then shorter refresher sessions or job aids for the rest of the staff before each phase goes live. A helpdesk or quick-response support channel during business hours would be important, and for the first few weeks I’d like there to be someone who can help right away if billing or enrollment problems come up. We’d also need a fallback plan in case something fails during release, because we can’t afford long disruptions when families are checking in or payments are being processed."

### [FR-053] (stated)
The system shall support a helpdesk or quick-response support channel during business hours.

**Source Evidence:**
- `[interview_turn:T068]` "We’d want hands-on training for the pilot group first, then shorter refresher sessions or job aids for the rest of the staff before each phase goes live. A helpdesk or quick-response support channel during business hours would be important, and for the first few weeks I’d like there to be someone who can help right away if billing or enrollment problems come up. We’d also need a fallback plan in case something fails during release, because we can’t afford long disruptions when families are checking in or payments are being processed."

### [FR-054] (stated)
The system shall support a fallback plan for release failures to avoid long disruptions.

**Source Evidence:**
- `[interview_turn:T068]` "We’d want hands-on training for the pilot group first, then shorter refresher sessions or job aids for the rest of the staff before each phase goes live. A helpdesk or quick-response support channel during business hours would be important, and for the first few weeks I’d like there to be someone who can help right away if billing or enrollment problems come up. We’d also need a fallback plan in case something fails during release, because we can’t afford long disruptions when families are checking in or payments are being processed."

### [FR-055] (stated)
The system shall support import of family records, child profiles, classroom assignments, immunization information, billing balances, and historical attendance or enrollment data if available.

**Source Evidence:**
- `[interview_turn:T062]` "We’d need to bring over family records, child profiles, classroom assignments, immunization information, billing balances, and maybe some historical attendance or enrollment data if it’s available. The biggest challenge will probably be cleaning up inconsistent data, because some of it may be in spreadsheets or paper files and not always formatted the same way. It would help if the system supported a guided import process with validation, error reports, and a way to review records before they’re finalized."
- `[interview_turn:T066]` "We’d probably migrate in stages, starting with the most important active records like families, children, enrollments, classroom assignments, and current billing balances. After that, we’d bring over immunization records and any attendance or historical data we decide we still need for reference. The main challenges will be cleaning up duplicates, filling in missing information, and making sure dates and balances match what we already have in our records."

### [FR-056] (stated)
The system shall support generation or sending of parent notices directly from the system through email integration.

**Source Evidence:**
- `[interview_turn:T008]` "I know email integration will be important because we send notices to parents all the time, and it would be helpful if the system could generate or send those messages directly. For accounting, we do use software outside the child care system, but I’m not sure yet which product is the one we’d need to connect to. Beyond that, I’d need to verify whether we also need calendar, SMS, or payment processor integrations."
- `[interview_turn:T010]` "Email notifications feel essential from day one because we rely on them for routine parent communication and reminders. Accounting connectivity is also important, but if it takes longer to sort out, we could start with invoice generation in the system and handle export or manual transfer as a temporary step. Calendar and SMS would be nice to have, but I’d see those as later enhancements unless we find a strong operational need."

### [FR-057] (stated)
The system shall share invoice and payment information with accounting systems.

**Source Evidence:**
- `[interview_turn:T034]` "We definitely use email and some kind of accounting or billing tool already, and we may also rely on calendar tools for scheduling and reminders. I’d like the new system to share invoice and payment information with accounting, and maybe send notifications or reminders through email without staff having to copy details manually. If there’s a payment processor involved, it would be helpful if payments could be recorded automatically, but I’d need to verify what specific products we already have."

### [FR-058] (conditional)
The system shall allow payments to be recorded automatically if payment processor integration is available.

**Source Evidence:**
- `[interview_turn:T034]` "We definitely use email and some kind of accounting or billing tool already, and we may also rely on calendar tools for scheduling and reminders. I’d like the new system to share invoice and payment information with accounting, and maybe send notifications or reminders through email without staff having to copy details manually. If there’s a payment processor involved, it would be helpful if payments could be recorded automatically, but I’d need to verify what specific products we already have."

### [FR-059] (stated)
The system shall support multiple users using the system simultaneously without freezing.

**Source Evidence:**
- `[interview_turn:T048]` "The busiest times are usually morning drop-off, late afternoon pickup, and the start of billing periods when a lot of staff may be checking attendance, child information, or invoices at once. The system should stay responsive during those periods, because even a short delay can create a backup at the front desk. I’d want it to handle multiple users without freezing, and if something is taking longer, it should still show progress clearly so staff know it hasn’t failed."

### [FR-060] (stated)
The system shall show progress clearly when an operation takes longer to complete.

**Source Evidence:**
- `[interview_turn:T048]` "The busiest times are usually morning drop-off, late afternoon pickup, and the start of billing periods when a lot of staff may be checking attendance, child information, or invoices at once. The system should stay responsive during those periods, because even a short delay can create a backup at the front desk. I’d want it to handle multiple users without freezing, and if something is taking longer, it should still show progress clearly so staff know it hasn’t failed."

### [FR-061] (stated)
The system shall support adding users and records as the center grows without significant slowdown.

**Source Evidence:**
- `[interview_turn:T050]` "I’d expect the center to grow gradually, maybe more classrooms, more families, and more staff over time, so the system should not feel cramped once the numbers go up. It should be able to add users and records without slowing down much, and reporting should still work well as the database gets larger. It would also help if the system could support multiple sites later, even if we only start with one location now."

### [FR-062] (stated)
The system shall continue to support reporting well as the database grows.

**Source Evidence:**
- `[interview_turn:T050]` "I’d expect the center to grow gradually, maybe more classrooms, more families, and more staff over time, so the system should not feel cramped once the numbers go up. It should be able to add users and records without slowing down much, and reporting should still work well as the database gets larger. It would also help if the system could support multiple sites later, even if we only start with one location now."
- `[interview_turn:T052]` "Older records should stay accessible for compliance and reference, especially enrollment and billing history, but they could be moved to an archived state once they’re no longer actively used. I’d prefer that archived records are still searchable, just not part of the day-to-day screens unless someone needs them. As the database grows, reports should still run in a reasonable time, and the system should not slow down just because there are years of historical data behind it."

### [FR-063] (conditional)
The system shall support multiple sites later.

**Source Evidence:**
- `[interview_turn:T050]` "I’d expect the center to grow gradually, maybe more classrooms, more families, and more staff over time, so the system should not feel cramped once the numbers go up. It should be able to add users and records without slowing down much, and reporting should still work well as the database gets larger. It would also help if the system could support multiple sites later, even if we only start with one location now."

### [FR-064] (stated)
The system shall keep older records accessible for compliance and reference.

**Source Evidence:**
- `[interview_turn:T052]` "Older records should stay accessible for compliance and reference, especially enrollment and billing history, but they could be moved to an archived state once they’re no longer actively used. I’d prefer that archived records are still searchable, just not part of the day-to-day screens unless someone needs them. As the database grows, reports should still run in a reasonable time, and the system should not slow down just because there are years of historical data behind it."

### [FR-065] (stated)
The system shall mark older records as archived once they are no longer actively used.

**Source Evidence:**
- `[interview_turn:T052]` "Older records should stay accessible for compliance and reference, especially enrollment and billing history, but they could be moved to an archived state once they’re no longer actively used. I’d prefer that archived records are still searchable, just not part of the day-to-day screens unless someone needs them. As the database grows, reports should still run in a reasonable time, and the system should not slow down just because there are years of historical data behind it."

### [FR-066] (stated)
The system shall allow archived records to remain searchable while excluding them from day-to-day screens by default.

**Source Evidence:**
- `[interview_turn:T052]` "Older records should stay accessible for compliance and reference, especially enrollment and billing history, but they could be moved to an archived state once they’re no longer actively used. I’d prefer that archived records are still searchable, just not part of the day-to-day screens unless someone needs them. As the database grows, reports should still run in a reasonable time, and the system should not slow down just because there are years of historical data behind it."

### [FR-067] (stated)
The system shall support a browser-based interface that is straightforward, consistent, and easy to use for non-technical staff.

**Source Evidence:**
- `[interview_turn:T014]` "Yes, staff technical skill levels vary a lot, so the interface needs to be straightforward and not overly complicated. Privacy is a big concern because we’re handling children’s and family information, so access needs to be controlled carefully and people should only see what they need for their role. Work schedules also matter because some updates happen during busy drop-off and pickup times, so the system should be quick to use in short, interrupted sessions."
- `[interview_turn:T054]` "The staff won’t all be very technical, so the system needs to be simple and consistent, with clear labels and not too many clicks for common tasks. It should work well on a browser and be readable on tablets too, since some people may use it at the front desk or while moving around the center. Accessibility matters as well, so good contrast, keyboard support, and screen-reader-friendly design would be important for anyone with visual or mobility needs."
- `[interview_turn:T056]` "Some staff may have limited experience with software, so built-in help tips and clear error messages would be very useful. It would also help to have larger text options, simple navigation, and forms that don’t lose entered data if someone makes a mistake. For support tools, I’d like a search function that is easy to use and maybe printable views or summaries for staff who still rely on paper in some situations."

### [FR-068] (stated)
The system shall support readable use on tablets.

**Source Evidence:**
- `[interview_turn:T054]` "The staff won’t all be very technical, so the system needs to be simple and consistent, with clear labels and not too many clicks for common tasks. It should work well on a browser and be readable on tablets too, since some people may use it at the front desk or while moving around the center. Accessibility matters as well, so good contrast, keyboard support, and screen-reader-friendly design would be important for anyone with visual or mobility needs."

### [FR-069] (stated)
The system shall support keyboard navigation and screen-reader-friendly design.

**Source Evidence:**
- `[interview_turn:T054]` "The staff won’t all be very technical, so the system needs to be simple and consistent, with clear labels and not too many clicks for common tasks. It should work well on a browser and be readable on tablets too, since some people may use it at the front desk or while moving around the center. Accessibility matters as well, so good contrast, keyboard support, and screen-reader-friendly design would be important for anyone with visual or mobility needs."

### [FR-070] (stated)
The system shall support larger text options.

**Source Evidence:**
- `[interview_turn:T056]` "Some staff may have limited experience with software, so built-in help tips and clear error messages would be very useful. It would also help to have larger text options, simple navigation, and forms that don’t lose entered data if someone makes a mistake. For support tools, I’d like a search function that is easy to use and maybe printable views or summaries for staff who still rely on paper in some situations."

### [FR-071] (stated)
The system shall support simple navigation with clear labels and minimal clicks for common tasks.

**Source Evidence:**
- `[interview_turn:T054]` "The staff won’t all be very technical, so the system needs to be simple and consistent, with clear labels and not too many clicks for common tasks. It should work well on a browser and be readable on tablets too, since some people may use it at the front desk or while moving around the center. Accessibility matters as well, so good contrast, keyboard support, and screen-reader-friendly design would be important for anyone with visual or mobility needs."
- `[interview_turn:T056]` "Some staff may have limited experience with software, so built-in help tips and clear error messages would be very useful. It would also help to have larger text options, simple navigation, and forms that don’t lose entered data if someone makes a mistake. For support tools, I’d like a search function that is easy to use and maybe printable views or summaries for staff who still rely on paper in some situations."

### [FR-072] (stated)
The system shall support role-based access control so users see only information relevant to their jobs.

**Source Evidence:**
- `[interview_turn:T014]` "Yes, staff technical skill levels vary a lot, so the interface needs to be straightforward and not overly complicated. Privacy is a big concern because we’re handling children’s and family information, so access needs to be controlled carefully and people should only see what they need for their role. Work schedules also matter because some updates happen during busy drop-off and pickup times, so the system should be quick to use in short, interrupted sessions."
- `[interview_turn:T016]` "Access should definitely be role-based, so front-desk staff, teachers, and administrators each see only the information relevant to their jobs. We’d also want strong password protection and audit logs so we can see who changed what and when. Remote or off-hours access may be needed for some administrators, but I’d want that controlled carefully, and I’m not sure yet whether we’d require extra approval or multi-factor authentication."
- `[interview_turn:T044]` "The biggest concern is making sure staff only see the children and families they actually need for their job, especially if someone works across classrooms or only helps with billing. I’d want role-based access with the ability to limit by function and maybe by classroom or site, and sensitive details like health information should be restricted more tightly than general contact info. The system should also keep an audit log of logins and changes to important records, including who viewed or edited them and when, so we can review issues if something looks off."
- `[interview_turn:T076]` "Yes, one common issue is that staff want to pull up child or billing details very quickly, especially when a parent calls or there’s a check-in problem, but we can’t let that become an open door to sensitive information. Another tricky situation is when someone temporarily covers for another employee, because they may need access to do the job but not to everything the regular staff member can see. In those cases, we’d want role-based access and a way to grant temporary permissions without making privacy rules too loose."

### [FR-073] (conditional)
The system shall support limiting access by function and, where needed, by classroom or site.

**Source Evidence:**
- `[interview_turn:T044]` "The biggest concern is making sure staff only see the children and families they actually need for their job, especially if someone works across classrooms or only helps with billing. I’d want role-based access with the ability to limit by function and maybe by classroom or site, and sensitive details like health information should be restricted more tightly than general contact info. The system should also keep an audit log of logins and changes to important records, including who viewed or edited them and when, so we can review issues if something looks off."

### [FR-074] (stated)
The system shall restrict sensitive health information more tightly than general contact information.

**Source Evidence:**
- `[interview_turn:T044]` "The biggest concern is making sure staff only see the children and families they actually need for their job, especially if someone works across classrooms or only helps with billing. I’d want role-based access with the ability to limit by function and maybe by classroom or site, and sensitive details like health information should be restricted more tightly than general contact info. The system should also keep an audit log of logins and changes to important records, including who viewed or edited them and when, so we can review issues if something looks off."

### [FR-075] (stated)
The system shall support temporary permissions for staff who temporarily cover another employee.

**Source Evidence:**
- `[interview_turn:T076]` "Yes, one common issue is that staff want to pull up child or billing details very quickly, especially when a parent calls or there’s a check-in problem, but we can’t let that become an open door to sensitive information. Another tricky situation is when someone temporarily covers for another employee, because they may need access to do the job but not to everything the regular staff member can see. In those cases, we’d want role-based access and a way to grant temporary permissions without making privacy rules too loose."

### [FR-076] (stated)
The system shall provide audit logs of logins and changes to important records, including who viewed or edited them and when.

**Source Evidence:**
- `[interview_turn:T016]` "Access should definitely be role-based, so front-desk staff, teachers, and administrators each see only the information relevant to their jobs. We’d also want strong password protection and audit logs so we can see who changed what and when. Remote or off-hours access may be needed for some administrators, but I’d want that controlled carefully, and I’m not sure yet whether we’d require extra approval or multi-factor authentication."
- `[interview_turn:T044]` "The biggest concern is making sure staff only see the children and families they actually need for their job, especially if someone works across classrooms or only helps with billing. I’d want role-based access with the ability to limit by function and maybe by classroom or site, and sensitive details like health information should be restricted more tightly than general contact info. The system should also keep an audit log of logins and changes to important records, including who viewed or edited them and when, so we can review issues if something looks off."

### [FR-077] (stated)
The system shall provide strong individual logins for every staff member and shall not allow shared accounts.

**Source Evidence:**
- `[interview_turn:T046]` "I’d expect strong individual logins for every staff member, no shared accounts, and passwords that meet a reasonable complexity standard and expire only if there’s a real security reason, not constantly. Multi-factor authentication would be important for administrators and anyone handling billing or health records, especially for remote access. It would also help to have automatic session timeouts, encrypted data in transit and at rest, and alerts for suspicious activity like repeated failed logins or access from unusual locations."

### [FR-078] (stated)
The system shall support password complexity requirements and password expiration only for real security reasons.

**Source Evidence:**
- `[interview_turn:T046]` "I’d expect strong individual logins for every staff member, no shared accounts, and passwords that meet a reasonable complexity standard and expire only if there’s a real security reason, not constantly. Multi-factor authentication would be important for administrators and anyone handling billing or health records, especially for remote access. It would also help to have automatic session timeouts, encrypted data in transit and at rest, and alerts for suspicious activity like repeated failed logins or access from unusual locations."

### [FR-079] (stated)
The system shall support multi-factor authentication for administrators and for anyone handling billing or health records, especially for remote access.

**Source Evidence:**
- `[interview_turn:T046]` "I’d expect strong individual logins for every staff member, no shared accounts, and passwords that meet a reasonable complexity standard and expire only if there’s a real security reason, not constantly. Multi-factor authentication would be important for administrators and anyone handling billing or health records, especially for remote access. It would also help to have automatic session timeouts, encrypted data in transit and at rest, and alerts for suspicious activity like repeated failed logins or access from unusual locations."
- `[interview_turn:T016]` "Access should definitely be role-based, so front-desk staff, teachers, and administrators each see only the information relevant to their jobs. We’d also want strong password protection and audit logs so we can see who changed what and when. Remote or off-hours access may be needed for some administrators, but I’d want that controlled carefully, and I’m not sure yet whether we’d require extra approval or multi-factor authentication."

### [FR-080] (stated)
The system shall support automatic session timeouts.

**Source Evidence:**
- `[interview_turn:T046]` "I’d expect strong individual logins for every staff member, no shared accounts, and passwords that meet a reasonable complexity standard and expire only if there’s a real security reason, not constantly. Multi-factor authentication would be important for administrators and anyone handling billing or health records, especially for remote access. It would also help to have automatic session timeouts, encrypted data in transit and at rest, and alerts for suspicious activity like repeated failed logins or access from unusual locations."

### [FR-081] (stated)
The system shall encrypt data in transit and at rest.

**Source Evidence:**
- `[interview_turn:T046]` "I’d expect strong individual logins for every staff member, no shared accounts, and passwords that meet a reasonable complexity standard and expire only if there’s a real security reason, not constantly. Multi-factor authentication would be important for administrators and anyone handling billing or health records, especially for remote access. It would also help to have automatic session timeouts, encrypted data in transit and at rest, and alerts for suspicious activity like repeated failed logins or access from unusual locations."

### [FR-082] (stated)
The system shall alert on suspicious activity such as repeated failed logins or access from unusual locations.

**Source Evidence:**
- `[interview_turn:T046]` "I’d expect strong individual logins for every staff member, no shared accounts, and passwords that meet a reasonable complexity standard and expire only if there’s a real security reason, not constantly. Multi-factor authentication would be important for administrators and anyone handling billing or health records, especially for remote access. It would also help to have automatic session timeouts, encrypted data in transit and at rest, and alerts for suspicious activity like repeated failed logins or access from unusual locations."

### [FR-083] (conditional)
The system shall support temporary or off-hours access for some administrators under controlled conditions.

**Source Evidence:**
- `[interview_turn:T016]` "Access should definitely be role-based, so front-desk staff, teachers, and administrators each see only the information relevant to their jobs. We’d also want strong password protection and audit logs so we can see who changed what and when. Remote or off-hours access may be needed for some administrators, but I’d want that controlled carefully, and I’m not sure yet whether we’d require extra approval or multi-factor authentication."

### [FR-084] (stated)
The system shall clearly indicate the current status of invoices and enrollments, including pending, submitted, and paid where applicable.

**Source Evidence:**
- `[interview_turn:T040]` "If a task gets interrupted, I’d want the system to save progress automatically in the background so staff do not lose everything they entered. When they come back, it should reopen the form with the last saved values and a clear message saying it was saved as a draft or completed successfully. For invoices or enrollments, it should also show a status like pending, submitted, or paid so staff can immediately tell whether they need to finish anything or whether it already went through."

### [FR-085] (stated)
The system shall provide a simple message telling staff what to do next when something goes wrong.

**Source Evidence:**
- `[interview_turn:T024]` "It should save work as safely as possible so people don’t lose a whole enrollment or invoice if the connection drops or they click the wrong thing. At minimum, I’d want some kind of draft or confirmation step before final submission, plus a clear way to resume or correct a task if it was interrupted. If something does go wrong, staff should be able to see whether it actually went through and get a simple message telling them what to do next."

### [FR-086] (stated)
The system shall support quick lookup of child or billing details for authorized staff.

**Source Evidence:**
- `[interview_turn:T076]` "Yes, one common issue is that staff want to pull up child or billing details very quickly, especially when a parent calls or there’s a check-in problem, but we can’t let that become an open door to sensitive information. Another tricky situation is when someone temporarily covers for another employee, because they may need access to do the job but not to everything the regular staff member can see. In those cases, we’d want role-based access and a way to grant temporary permissions without making privacy rules too loose."

### [FR-087] (stated)
The system shall support check-in and check-out routines.

**Source Evidence:**
- `[interview_turn:T026]` "Yes, we use terms like enrollment, tuition, invoices, attendance, ratios, and capacity pretty regularly, and everyone generally understands those. Classroom capacity and ratios can mean slightly different things depending on whether you’re talking about how many children fit in a room or how many staff are required to meet licensing rules. We also talk about waitlist, withdrawals, and check-in or check-out for daily routines, and those can sometimes be interpreted a little differently by office staff versus teachers."
- `[interview_turn:T072]` "One example is check-in and check-out, where staff need to move quickly at busy times, but we still need safeguards so the wrong child can’t be signed in or out. Another is invoice processing, where it should be simple for authorized staff, but changes to charges or payments should probably require tighter permissions or an audit trail. During rollout, I’d rather delay a feature a little than launch it with weak controls if it could affect family records or billing accuracy."

### [FR-088] (stated)
The system shall allow staff to view whether a payment or invoice is still open, partly paid, or fully settled.

**Source Evidence:**
- `[interview_turn:T038]` "One tricky case is when two staff members are looking at the same family or invoice at the same time and both try to update it, which can cause conflicting information. Another is when a partial payment is entered and then the rest comes in later, so staff need to know whether the invoice is still open, partly paid, or fully settled. The system should show the last saved status very clearly, warn about concurrent edits, and keep a visible history so staff can tell what happened without guessing."

## 4. Business Rules and Constraints

### [BR-001] (stated)
Administrators shall have the broadest access to family and child records.

**Source Evidence:**
- `[interview_turn:T018]` "Administrators handle registration, enrollment, classroom assignments, capacity, and waiting lists, so they need the broadest access to family and child records. Teachers or classroom staff mainly use the system to look up children in their care, check immunizations or basic profile details, and record day-to-day information relevant to the classroom. Front-desk or office staff would likely manage check-in style administrative work, answer parent questions, and help with invoices or general records, but I’d need to confirm the exact role names we want to use."

### [BR-002] (stated)
The system shall not silently overwrite changes when concurrent edits occur.

**Source Evidence:**
- `[interview_turn:T042]` "I’d prefer a warning if someone else is already editing the same record, with the option to open it read-only or wait until it’s available. If both people do make changes, the system should not silently overwrite anything; it should force a review of the conflicting fields and show who changed what and when. For payments, the record should show a simple current status, like unpaid, partial, or paid, plus a visible transaction history with dates, amounts, and any refunds or adjustments so staff can follow the full trail."

### [BR-003] (stated)
Only very limited cases shall allow deletion of records.

**Source Evidence:**
- `[interview_turn:T032]` "Right now it’s mostly informal, and we tend to keep financial records and child history on file for a long time rather than deleting them. Immunization information is kept as long as the child is active and usually archived afterward, since we may need it for reference. I’d want the system to support marking records inactive, archiving them, and only allowing deletion for very limited cases, with an audit trail if possible."

### [BR-004] (stated)
The system shall avoid double charges for billing.

**Source Evidence:**
- `[interview_turn:T036]` "Yes, that can happen if the network drops, if someone closes the browser, or if a staff member realizes they entered something wrong halfway through. The system should clearly show whether the task was saved as a draft or fully completed, and it should let staff safely resume or cancel without creating duplicate records. For billing especially, I’d want it to avoid double charges and make it easy to see what already went through versus what still needs attention."

### [BR-005] (stated)
The system shall keep a visible history for staff to understand what happened without guessing.

**Source Evidence:**
- `[interview_turn:T038]` "One tricky case is when two staff members are looking at the same family or invoice at the same time and both try to update it, which can cause conflicting information. Another is when a partial payment is entered and then the rest comes in later, so staff need to know whether the invoice is still open, partly paid, or fully settled. The system should show the last saved status very clearly, warn about concurrent edits, and keep a visible history so staff can tell what happened without guessing."

### [BR-006] (stated)
The system shall not use shared staff accounts.

**Source Evidence:**
- `[interview_turn:T046]` "I’d expect strong individual logins for every staff member, no shared accounts, and passwords that meet a reasonable complexity standard and expire only if there’s a real security reason, not constantly. Multi-factor authentication would be important for administrators and anyone handling billing or health records, especially for remote access. It would also help to have automatic session timeouts, encrypted data in transit and at rest, and alerts for suspicious activity like repeated failed logins or access from unusual locations."

### [BR-007] (stated)
The system shall support only very limited data deletion and prefer inactive or archived states for departed children and historical records.

**Source Evidence:**
- `[interview_turn:T030]` "Family and child records are usually created when someone first applies or enrolls, and then they get updated whenever contact details, emergency contacts, medical information, or billing details change. If a child leaves the center, we would normally mark the record inactive or archived rather than delete it, so we still have the history for reporting and billing reference. I’m not sure we have a fixed retention rule yet, so that would need to be checked with management or whatever compliance requirements apply."
- `[interview_turn:T032]` "Right now it’s mostly informal, and we tend to keep financial records and child history on file for a long time rather than deleting them. Immunization information is kept as long as the child is active and usually archived afterward, since we may need it for reference. I’d want the system to support marking records inactive, archiving them, and only allowing deletion for very limited cases, with an audit trail if possible."

### [BR-008] (stated)
The system shall preserve family and child history for reporting and billing reference after archival.

**Source Evidence:**
- `[interview_turn:T030]` "Family and child records are usually created when someone first applies or enrolls, and then they get updated whenever contact details, emergency contacts, medical information, or billing details change. If a child leaves the center, we would normally mark the record inactive or archived rather than delete it, so we still have the history for reporting and billing reference. I’m not sure we have a fixed retention rule yet, so that would need to be checked with management or whatever compliance requirements apply."
- `[interview_turn:T032]` "Right now it’s mostly informal, and we tend to keep financial records and child history on file for a long time rather than deleting them. Immunization information is kept as long as the child is active and usually archived afterward, since we may need it for reference. I’d want the system to support marking records inactive, archiving them, and only allowing deletion for very limited cases, with an audit trail if possible."

### [BR-009] (conditional)
The system shall require careful control of remote or off-hours access.

**Source Evidence:**
- `[interview_turn:T016]` "Access should definitely be role-based, so front-desk staff, teachers, and administrators each see only the information relevant to their jobs. We’d also want strong password protection and audit logs so we can see who changed what and when. Remote or off-hours access may be needed for some administrators, but I’d want that controlled carefully, and I’m not sure yet whether we’d require extra approval or multi-factor authentication."

### [BR-010] (stated)
The system shall allow only authorized staff to process invoices.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "A child care center needs a web-based management system that reduces administrative work and lets employees share information through a central database. Administrators should be able to register families and manage enrollment, classroom capacity, and waiting lists, while authorized staff need support for routine activities such as tracking child immunizations, processing invoices, and producing information for customers and center operations."
- `[interview_turn:T018]` "Administrators handle registration, enrollment, classroom assignments, capacity, and waiting lists, so they need the broadest access to family and child records. Teachers or classroom staff mainly use the system to look up children in their care, check immunizations or basic profile details, and record day-to-day information relevant to the classroom. Front-desk or office staff would likely manage check-in style administrative work, answer parent questions, and help with invoices or general records, but I’d need to confirm the exact role names we want to use."
- `[interview_turn:T072]` "One example is check-in and check-out, where staff need to move quickly at busy times, but we still need safeguards so the wrong child can’t be signed in or out. Another is invoice processing, where it should be simple for authorized staff, but changes to charges or payments should probably require tighter permissions or an audit trail. During rollout, I’d rather delay a feature a little than launch it with weak controls if it could affect family records or billing accuracy."

## 5. Data and External Interfaces

### [DI-001] (stated)
The system shall integrate with email for parent notices and reminders.

**Source Evidence:**
- `[interview_turn:T008]` "I know email integration will be important because we send notices to parents all the time, and it would be helpful if the system could generate or send those messages directly. For accounting, we do use software outside the child care system, but I’m not sure yet which product is the one we’d need to connect to. Beyond that, I’d need to verify whether we also need calendar, SMS, or payment processor integrations."
- `[interview_turn:T010]` "Email notifications feel essential from day one because we rely on them for routine parent communication and reminders. Accounting connectivity is also important, but if it takes longer to sort out, we could start with invoice generation in the system and handle export or manual transfer as a temporary step. Calendar and SMS would be nice to have, but I’d see those as later enhancements unless we find a strong operational need."
- `[interview_turn:T034]` "We definitely use email and some kind of accounting or billing tool already, and we may also rely on calendar tools for scheduling and reminders. I’d like the new system to share invoice and payment information with accounting, and maybe send notifications or reminders through email without staff having to copy details manually. If there’s a payment processor involved, it would be helpful if payments could be recorded automatically, but I’d need to verify what specific products we already have."

### [DI-002] (stated)
The system shall support integration with accounting software for invoice and payment information.

**Source Evidence:**
- `[interview_turn:T006]` "We’re assuming staff will use standard office computers and probably tablets in some areas, so it should work well in a browser without special software. Internet access is generally available at the center, but we’d want the system to be stable and easy to use if the connection is slow. I know we use some external tools for email and possibly accounting, but I’d need to check with the team before saying exactly what integrations are required."
- `[interview_turn:T008]` "I know email integration will be important because we send notices to parents all the time, and it would be helpful if the system could generate or send those messages directly. For accounting, we do use software outside the child care system, but I’m not sure yet which product is the one we’d need to connect to. Beyond that, I’d need to verify whether we also need calendar, SMS, or payment processor integrations."
- `[interview_turn:T034]` "We definitely use email and some kind of accounting or billing tool already, and we may also rely on calendar tools for scheduling and reminders. I’d like the new system to share invoice and payment information with accounting, and maybe send notifications or reminders through email without staff having to copy details manually. If there’s a payment processor involved, it would be helpful if payments could be recorded automatically, but I’d need to verify what specific products we already have."

### [DI-003] (conditional)
The system shall support calendar integration if later deemed necessary.

**Source Evidence:**
- `[interview_turn:T008]` "I know email integration will be important because we send notices to parents all the time, and it would be helpful if the system could generate or send those messages directly. For accounting, we do use software outside the child care system, but I’m not sure yet which product is the one we’d need to connect to. Beyond that, I’d need to verify whether we also need calendar, SMS, or payment processor integrations."
- `[interview_turn:T034]` "We definitely use email and some kind of accounting or billing tool already, and we may also rely on calendar tools for scheduling and reminders. I’d like the new system to share invoice and payment information with accounting, and maybe send notifications or reminders through email without staff having to copy details manually. If there’s a payment processor involved, it would be helpful if payments could be recorded automatically, but I’d need to verify what specific products we already have."

### [DI-004] (conditional)
The system shall support SMS integration if later deemed necessary.

**Source Evidence:**
- `[interview_turn:T008]` "I know email integration will be important because we send notices to parents all the time, and it would be helpful if the system could generate or send those messages directly. For accounting, we do use software outside the child care system, but I’m not sure yet which product is the one we’d need to connect to. Beyond that, I’d need to verify whether we also need calendar, SMS, or payment processor integrations."

### [DI-005] (conditional)
The system shall support payment processor integration if later deemed necessary.

**Source Evidence:**
- `[interview_turn:T008]` "I know email integration will be important because we send notices to parents all the time, and it would be helpful if the system could generate or send those messages directly. For accounting, we do use software outside the child care system, but I’m not sure yet which product is the one we’d need to connect to. Beyond that, I’d need to verify whether we also need calendar, SMS, or payment processor integrations."
- `[interview_turn:T034]` "We definitely use email and some kind of accounting or billing tool already, and we may also rely on calendar tools for scheduling and reminders. I’d like the new system to share invoice and payment information with accounting, and maybe send notifications or reminders through email without staff having to copy details manually. If there’s a payment processor involved, it would be helpful if payments could be recorded automatically, but I’d need to verify what specific products we already have."

## 6. Quality Requirements

### [QR-001] (stated)
The system shall be stable and easy to use when the internet connection is slow or temporarily unreliable.

**Source Evidence:**
- `[interview_turn:T006]` "We’re assuming staff will use standard office computers and probably tablets in some areas, so it should work well in a browser without special software. Internet access is generally available at the center, but we’d want the system to be stable and easy to use if the connection is slow. I know we use some external tools for email and possibly accounting, but I’d need to check with the team before saying exactly what integrations are required."
- `[interview_turn:T012]` "The main limitation is that not every staff member has a dedicated device, so the system should let multiple people log in from shared computers without friction. Internet is usually fine, but there can be occasional slowdowns, so it would help if common tasks still loaded quickly and didn’t require a lot of back-and-forth refreshing. I don’t think we need offline mode right now, but we do want the system to be forgiving if the connection is temporarily unreliable."

### [QR-002] (stated)
The system shall load common tasks quickly.

**Source Evidence:**
- `[interview_turn:T012]` "The main limitation is that not every staff member has a dedicated device, so the system should let multiple people log in from shared computers without friction. Internet is usually fine, but there can be occasional slowdowns, so it would help if common tasks still loaded quickly and didn’t require a lot of back-and-forth refreshing. I don’t think we need offline mode right now, but we do want the system to be forgiving if the connection is temporarily unreliable."

### [QR-003] (stated)
The system shall remain responsive during busy periods such as morning drop-off, late afternoon pickup, and billing periods.

**Source Evidence:**
- `[interview_turn:T048]` "The busiest times are usually morning drop-off, late afternoon pickup, and the start of billing periods when a lot of staff may be checking attendance, child information, or invoices at once. The system should stay responsive during those periods, because even a short delay can create a backup at the front desk. I’d want it to handle multiple users without freezing, and if something is taking longer, it should still show progress clearly so staff know it hasn’t failed."

### [QR-004] (stated)
The system shall support use in short, interrupted sessions.

**Source Evidence:**
- `[interview_turn:T014]` "Yes, staff technical skill levels vary a lot, so the interface needs to be straightforward and not overly complicated. Privacy is a big concern because we’re handling children’s and family information, so access needs to be controlled carefully and people should only see what they need for their role. Work schedules also matter because some updates happen during busy drop-off and pickup times, so the system should be quick to use in short, interrupted sessions."

### [QR-005] (stated)
The system shall provide a straightforward interface because staff technical skill levels vary.

**Source Evidence:**
- `[interview_turn:T014]` "Yes, staff technical skill levels vary a lot, so the interface needs to be straightforward and not overly complicated. Privacy is a big concern because we’re handling children’s and family information, so access needs to be controlled carefully and people should only see what they need for their role. Work schedules also matter because some updates happen during busy drop-off and pickup times, so the system should be quick to use in short, interrupted sessions."
- `[interview_turn:T054]` "The staff won’t all be very technical, so the system needs to be simple and consistent, with clear labels and not too many clicks for common tasks. It should work well on a browser and be readable on tablets too, since some people may use it at the front desk or while moving around the center. Accessibility matters as well, so good contrast, keyboard support, and screen-reader-friendly design would be important for anyone with visual or mobility needs."

### [QR-006] (stated)
The system shall keep tasks from taking too many clicks.

**Source Evidence:**
- `[interview_turn:T054]` "The staff won’t all be very technical, so the system needs to be simple and consistent, with clear labels and not too many clicks for common tasks. It should work well on a browser and be readable on tablets too, since some people may use it at the front desk or while moving around the center. Accessibility matters as well, so good contrast, keyboard support, and screen-reader-friendly design would be important for anyone with visual or mobility needs."

### [QR-007] (stated)
The system shall show progress clearly during longer operations.

**Source Evidence:**
- `[interview_turn:T048]` "The busiest times are usually morning drop-off, late afternoon pickup, and the start of billing periods when a lot of staff may be checking attendance, child information, or invoices at once. The system should stay responsive during those periods, because even a short delay can create a backup at the front desk. I’d want it to handle multiple users without freezing, and if something is taking longer, it should still show progress clearly so staff know it hasn’t failed."

### [QR-008] (stated)
The system shall support reporting that still runs in a reasonable time as the database grows.

**Source Evidence:**
- `[interview_turn:T052]` "Older records should stay accessible for compliance and reference, especially enrollment and billing history, but they could be moved to an archived state once they’re no longer actively used. I’d prefer that archived records are still searchable, just not part of the day-to-day screens unless someone needs them. As the database grows, reports should still run in a reasonable time, and the system should not slow down just because there are years of historical data behind it."

### [QR-009] (stated)
The system shall support future growth in the number of classrooms, families, staff, and records without feeling cramped.

**Source Evidence:**
- `[interview_turn:T050]` "I’d expect the center to grow gradually, maybe more classrooms, more families, and more staff over time, so the system should not feel cramped once the numbers go up. It should be able to add users and records without slowing down much, and reporting should still work well as the database gets larger. It would also help if the system could support multiple sites later, even if we only start with one location now."

### [QR-010] (stated)
The system shall support accessibility features including good contrast and keyboard support.

**Source Evidence:**
- `[interview_turn:T054]` "The staff won’t all be very technical, so the system needs to be simple and consistent, with clear labels and not too many clicks for common tasks. It should work well on a browser and be readable on tablets too, since some people may use it at the front desk or while moving around the center. Accessibility matters as well, so good contrast, keyboard support, and screen-reader-friendly design would be important for anyone with visual or mobility needs."

### [QR-011] (stated)
The system shall be forgiving if a connection is temporarily unreliable.

**Source Evidence:**
- `[interview_turn:T012]` "The main limitation is that not every staff member has a dedicated device, so the system should let multiple people log in from shared computers without friction. Internet is usually fine, but there can be occasional slowdowns, so it would help if common tasks still loaded quickly and didn’t require a lot of back-and-forth refreshing. I don’t think we need offline mode right now, but we do want the system to be forgiving if the connection is temporarily unreliable."

### [QR-012] (stated)
The system shall not slow down just because it contains years of historical data.

**Source Evidence:**
- `[interview_turn:T052]` "Older records should stay accessible for compliance and reference, especially enrollment and billing history, but they could be moved to an archived state once they’re no longer actively used. I’d prefer that archived records are still searchable, just not part of the day-to-day screens unless someone needs them. As the database grows, reports should still run in a reasonable time, and the system should not slow down just because there are years of historical data behind it."

## 7. Exceptions and Boundary Conditions

### [EX-001] (stated)
If a task is interrupted, the system shall allow staff to determine whether it was saved as a draft or completed successfully.

**Source Evidence:**
- `[interview_turn:T036]` "Yes, that can happen if the network drops, if someone closes the browser, or if a staff member realizes they entered something wrong halfway through. The system should clearly show whether the task was saved as a draft or fully completed, and it should let staff safely resume or cancel without creating duplicate records. For billing especially, I’d want it to avoid double charges and make it easy to see what already went through versus what still needs attention."
- `[interview_turn:T040]` "If a task gets interrupted, I’d want the system to save progress automatically in the background so staff do not lose everything they entered. When they come back, it should reopen the form with the last saved values and a clear message saying it was saved as a draft or completed successfully. For invoices or enrollments, it should also show a status like pending, submitted, or paid so staff can immediately tell whether they need to finish anything or whether it already went through."

### [EX-002] (stated)
If a critical task is interrupted, the system shall allow staff to resume or cancel it safely.

**Source Evidence:**
- `[interview_turn:T036]` "Yes, that can happen if the network drops, if someone closes the browser, or if a staff member realizes they entered something wrong halfway through. The system should clearly show whether the task was saved as a draft or fully completed, and it should let staff safely resume or cancel without creating duplicate records. For billing especially, I’d want it to avoid double charges and make it easy to see what already went through versus what still needs attention."

### [EX-003] (stated)
If a record is being edited by another user, the system shall warn the staff member and offer a read-only or wait path.

**Source Evidence:**
- `[interview_turn:T042]` "I’d prefer a warning if someone else is already editing the same record, with the option to open it read-only or wait until it’s available. If both people do make changes, the system should not silently overwrite anything; it should force a review of the conflicting fields and show who changed what and when. For payments, the record should show a simple current status, like unpaid, partial, or paid, plus a visible transaction history with dates, amounts, and any refunds or adjustments so staff can follow the full trail."

### [EX-004] (stated)
If conflicting changes occur, the system shall require review rather than silently overwriting data.

**Source Evidence:**
- `[interview_turn:T042]` "I’d prefer a warning if someone else is already editing the same record, with the option to open it read-only or wait until it’s available. If both people do make changes, the system should not silently overwrite anything; it should force a review of the conflicting fields and show who changed what and when. For payments, the record should show a simple current status, like unpaid, partial, or paid, plus a visible transaction history with dates, amounts, and any refunds or adjustments so staff can follow the full trail."

### [EX-005] (stated)
If data import contains uncertain or messy values, the system shall flag them for manual review before loading.

**Source Evidence:**
- `[interview_turn:T064]` "Right now, I’d expect most of it to come from Excel spreadsheets, CSV files, and some scanned paper forms, so there probably won’t be one single standard layout. It would be helpful if the system could automatically map common fields like child name, parent contact, dates, and billing amounts, then flag anything uncertain for manual review. For messy data, I’d want it to suggest possible fixes, but still let a staff member correct or confirm the values before they are loaded."

### [EX-006] (stated)
If a release fails, the system or rollout process shall support fallback handling to avoid long disruptions.

**Source Evidence:**
- `[interview_turn:T068]` "We’d want hands-on training for the pilot group first, then shorter refresher sessions or job aids for the rest of the staff before each phase goes live. A helpdesk or quick-response support channel during business hours would be important, and for the first few weeks I’d like there to be someone who can help right away if billing or enrollment problems come up. We’d also need a fallback plan in case something fails during release, because we can’t afford long disruptions when families are checking in or payments are being processed."

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
The specific accounting product to integrate with has not been determined.

**Source Evidence:**
- `[interview_turn:T008]` "I know email integration will be important because we send notices to parents all the time, and it would be helpful if the system could generate or send those messages directly. For accounting, we do use software outside the child care system, but I’m not sure yet which product is the one we’d need to connect to. Beyond that, I’d need to verify whether we also need calendar, SMS, or payment processor integrations."
- `[interview_turn:T034]` "We definitely use email and some kind of accounting or billing tool already, and we may also rely on calendar tools for scheduling and reminders. I’d like the new system to share invoice and payment information with accounting, and maybe send notifications or reminders through email without staff having to copy details manually. If there’s a payment processor involved, it would be helpful if payments could be recorded automatically, but I’d need to verify what specific products we already have."

### [UN-002]
Whether calendar integration is required has not been decided.

**Source Evidence:**
- `[interview_turn:T008]` "I know email integration will be important because we send notices to parents all the time, and it would be helpful if the system could generate or send those messages directly. For accounting, we do use software outside the child care system, but I’m not sure yet which product is the one we’d need to connect to. Beyond that, I’d need to verify whether we also need calendar, SMS, or payment processor integrations."
- `[interview_turn:T010]` "Email notifications feel essential from day one because we rely on them for routine parent communication and reminders. Accounting connectivity is also important, but if it takes longer to sort out, we could start with invoice generation in the system and handle export or manual transfer as a temporary step. Calendar and SMS would be nice to have, but I’d see those as later enhancements unless we find a strong operational need."
- `[interview_turn:T034]` "We definitely use email and some kind of accounting or billing tool already, and we may also rely on calendar tools for scheduling and reminders. I’d like the new system to share invoice and payment information with accounting, and maybe send notifications or reminders through email without staff having to copy details manually. If there’s a payment processor involved, it would be helpful if payments could be recorded automatically, but I’d need to verify what specific products we already have."

### [UN-003]
Whether SMS integration is required has not been decided.

**Source Evidence:**
- `[interview_turn:T008]` "I know email integration will be important because we send notices to parents all the time, and it would be helpful if the system could generate or send those messages directly. For accounting, we do use software outside the child care system, but I’m not sure yet which product is the one we’d need to connect to. Beyond that, I’d need to verify whether we also need calendar, SMS, or payment processor integrations."
- `[interview_turn:T010]` "Email notifications feel essential from day one because we rely on them for routine parent communication and reminders. Accounting connectivity is also important, but if it takes longer to sort out, we could start with invoice generation in the system and handle export or manual transfer as a temporary step. Calendar and SMS would be nice to have, but I’d see those as later enhancements unless we find a strong operational need."

### [UN-004]
Whether a payment processor integration is required has not been decided.

**Source Evidence:**
- `[interview_turn:T008]` "I know email integration will be important because we send notices to parents all the time, and it would be helpful if the system could generate or send those messages directly. For accounting, we do use software outside the child care system, but I’m not sure yet which product is the one we’d need to connect to. Beyond that, I’d need to verify whether we also need calendar, SMS, or payment processor integrations."
- `[interview_turn:T034]` "We definitely use email and some kind of accounting or billing tool already, and we may also rely on calendar tools for scheduling and reminders. I’d like the new system to share invoice and payment information with accounting, and maybe send notifications or reminders through email without staff having to copy details manually. If there’s a payment processor involved, it would be helpful if payments could be recorded automatically, but I’d need to verify what specific products we already have."

### [UN-005]
Whether offline mode is required has not been decided.

**Source Evidence:**
- `[interview_turn:T012]` "The main limitation is that not every staff member has a dedicated device, so the system should let multiple people log in from shared computers without friction. Internet is usually fine, but there can be occasional slowdowns, so it would help if common tasks still loaded quickly and didn’t require a lot of back-and-forth refreshing. I don’t think we need offline mode right now, but we do want the system to be forgiving if the connection is temporarily unreliable."

### [UN-006]
Whether extra approval is required for remote or off-hours access has not been decided.

**Source Evidence:**
- `[interview_turn:T016]` "Access should definitely be role-based, so front-desk staff, teachers, and administrators each see only the information relevant to their jobs. We’d also want strong password protection and audit logs so we can see who changed what and when. Remote or off-hours access may be needed for some administrators, but I’d want that controlled carefully, and I’m not sure yet whether we’d require extra approval or multi-factor authentication."

### [UN-007]
Whether multi-factor authentication is required for all users or only specific roles beyond administrators and staff handling billing or health records has not been decided.

**Source Evidence:**
- `[interview_turn:T016]` "Access should definitely be role-based, so front-desk staff, teachers, and administrators each see only the information relevant to their jobs. We’d also want strong password protection and audit logs so we can see who changed what and when. Remote or off-hours access may be needed for some administrators, but I’d want that controlled carefully, and I’m not sure yet whether we’d require extra approval or multi-factor authentication."
- `[interview_turn:T046]` "I’d expect strong individual logins for every staff member, no shared accounts, and passwords that meet a reasonable complexity standard and expire only if there’s a real security reason, not constantly. Multi-factor authentication would be important for administrators and anyone handling billing or health records, especially for remote access. It would also help to have automatic session timeouts, encrypted data in transit and at rest, and alerts for suspicious activity like repeated failed logins or access from unusual locations."

### [UN-008]
The exact staff role titles to be used in the system have not been finalized.

**Source Evidence:**
- `[interview_turn:T018]` "Administrators handle registration, enrollment, classroom assignments, capacity, and waiting lists, so they need the broadest access to family and child records. Teachers or classroom staff mainly use the system to look up children in their care, check immunizations or basic profile details, and record day-to-day information relevant to the classroom. Front-desk or office staff would likely manage check-in style administrative work, answer parent questions, and help with invoices or general records, but I’d need to confirm the exact role names we want to use."
- `[interview_turn:T020]` "We usually think of them as administrators, teachers, and office or front-desk staff, though the exact titles can vary a bit by center. There are definitely overlaps, because some people help with both classroom and administrative tasks, and a manager might also step in to cover front-desk duties when needed. The system should probably support multiple roles for one user rather than forcing a single fixed title."

### [UN-009]
Whether classroom or site-based access restrictions are required has not been fully decided.

**Source Evidence:**
- `[interview_turn:T044]` "The biggest concern is making sure staff only see the children and families they actually need for their job, especially if someone works across classrooms or only helps with billing. I’d want role-based access with the ability to limit by function and maybe by classroom or site, and sensitive details like health information should be restricted more tightly than general contact info. The system should also keep an audit log of logins and changes to important records, including who viewed or edited them and when, so we can review issues if something looks off."

### [UN-010]
The fixed retention rules for records have not been determined.

**Source Evidence:**
- `[interview_turn:T030]` "Family and child records are usually created when someone first applies or enrolls, and then they get updated whenever contact details, emergency contacts, medical information, or billing details change. If a child leaves the center, we would normally mark the record inactive or archived rather than delete it, so we still have the history for reporting and billing reference. I’m not sure we have a fixed retention rule yet, so that would need to be checked with management or whatever compliance requirements apply."

### [UN-011]
The center has not yet verified whether the system should support additional integrations, including calendar, SMS, or payment processor connections.

**Source Evidence:**
- `[interview_turn:T008]` "I know email integration will be important because we send notices to parents all the time, and it would be helpful if the system could generate or send those messages directly. For accounting, we do use software outside the child care system, but I’m not sure yet which product is the one we’d need to connect to. Beyond that, I’d need to verify whether we also need calendar, SMS, or payment processor integrations."
