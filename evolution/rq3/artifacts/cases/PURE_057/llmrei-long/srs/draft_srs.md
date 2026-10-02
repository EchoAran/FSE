# Software Requirements Specification: Security and Privacy Requirements Analysis Tool

## 1. Scope and Context

### [SC-001] (stated)
SPRAT is a collaborative workbench for aligning web-system requirements with privacy and security policies.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Requirements and privacy analysts need SPRAT, a collaborative workbench for aligning web-system requirements with privacy and security policies. Users should be able to capture goals, scenarios, policies, requirements, and legal-compliance information; trace goals back to their source policies; organize them with flexible classifications; and compare analyses produced by different people. Access should vary for administrators, project managers, analysts, and guests."

## 2. Actors

### [ACT-001] (stated)
The system shall support administrators, project managers, analysts, and guests with differentiated access.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Requirements and privacy analysts need SPRAT, a collaborative workbench for aligning web-system requirements with privacy and security policies. Users should be able to capture goals, scenarios, policies, requirements, and legal-compliance information; trace goals back to their source policies; organize them with flexible classifications; and compare analyses produced by different people. Access should vary for administrators, project managers, analysts, and guests."
- `[interview_turn:T010]` "Yes, role-based access is important too. Administrators, project managers, analysts, and guests should not all see or edit the same things, and we need a clear way to control that. It would also help if the tool supported collaboration without overwriting each other’s work."

## 3. Functional Requirements

### [FR-001] (stated)
The system shall allow users to capture goals, scenarios, policies, requirements, and legal-compliance information in one place.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Requirements and privacy analysts need SPRAT, a collaborative workbench for aligning web-system requirements with privacy and security policies. Users should be able to capture goals, scenarios, policies, requirements, and legal-compliance information; trace goals back to their source policies; organize them with flexible classifications; and compare analyses produced by different people. Access should vary for administrators, project managers, analysts, and guests."
- `[interview_turn:T008]` "We want to centralize the whole analysis workflow so people can capture goals, scenarios, policies, requirements, and compliance notes in one place. The big improvement is making traceability and comparison easier, especially when different analysts produce slightly different interpretations. We also want the classifications to be flexible enough to match the way our teams actually work."
- `[interview_turn:T018]` "We’d need to store goals at a high level, then the scenarios or use cases that explain how those goals are realized. We also need the actual requirements, both security and privacy related, plus the policies or legal sources they come from, and any compliance notes or rationale that explain why a requirement exists. The key thing is that each of those artifacts should be linkable to each other, especially from a requirement back to the source policy or legal reference."

### [FR-002] (stated)
The system shall allow users to store goals as high-level artifacts.

**Source Evidence:**
- `[interview_turn:T018]` "We’d need to store goals at a high level, then the scenarios or use cases that explain how those goals are realized. We also need the actual requirements, both security and privacy related, plus the policies or legal sources they come from, and any compliance notes or rationale that explain why a requirement exists. The key thing is that each of those artifacts should be linkable to each other, especially from a requirement back to the source policy or legal reference."

### [FR-003] (stated)
The system shall allow users to store scenarios or use cases that explain how goals are realized.

**Source Evidence:**
- `[interview_turn:T018]` "We’d need to store goals at a high level, then the scenarios or use cases that explain how those goals are realized. We also need the actual requirements, both security and privacy related, plus the policies or legal sources they come from, and any compliance notes or rationale that explain why a requirement exists. The key thing is that each of those artifacts should be linkable to each other, especially from a requirement back to the source policy or legal reference."

### [FR-004] (stated)
The system shall allow users to store security and privacy requirements.

**Source Evidence:**
- `[interview_turn:T018]` "We’d need to store goals at a high level, then the scenarios or use cases that explain how those goals are realized. We also need the actual requirements, both security and privacy related, plus the policies or legal sources they come from, and any compliance notes or rationale that explain why a requirement exists. The key thing is that each of those artifacts should be linkable to each other, especially from a requirement back to the source policy or legal reference."

### [FR-005] (stated)
The system shall allow users to store policies or legal sources from which requirements originate.

**Source Evidence:**
- `[interview_turn:T018]` "We’d need to store goals at a high level, then the scenarios or use cases that explain how those goals are realized. We also need the actual requirements, both security and privacy related, plus the policies or legal sources they come from, and any compliance notes or rationale that explain why a requirement exists. The key thing is that each of those artifacts should be linkable to each other, especially from a requirement back to the source policy or legal reference."

### [FR-006] (stated)
The system shall allow users to store compliance notes or rationale that explain why a requirement exists.

**Source Evidence:**
- `[interview_turn:T008]` "We want to centralize the whole analysis workflow so people can capture goals, scenarios, policies, requirements, and compliance notes in one place. The big improvement is making traceability and comparison easier, especially when different analysts produce slightly different interpretations. We also want the classifications to be flexible enough to match the way our teams actually work."
- `[interview_turn:T018]` "We’d need to store goals at a high level, then the scenarios or use cases that explain how those goals are realized. We also need the actual requirements, both security and privacy related, plus the policies or legal sources they come from, and any compliance notes or rationale that explain why a requirement exists. The key thing is that each of those artifacts should be linkable to each other, especially from a requirement back to the source policy or legal reference."

### [FR-007] (stated)
The system shall support explicit and navigable links between artifacts.

**Source Evidence:**
- `[interview_turn:T020]` "Ideally, the links should be explicit and navigable, so if I open a requirement I can immediately see which policy, regulation, or internal rule justified it. I’d also want the trace to work both ways, so from a policy or legal reference I can see all the requirements that came from it. If there are multiple sources, the system should show that clearly instead of forcing one single parent."

### [FR-008] (stated)
The system shall allow a user to view, from a requirement, the policy, regulation, or internal rule that justified it.

**Source Evidence:**
- `[interview_turn:T020]` "Ideally, the links should be explicit and navigable, so if I open a requirement I can immediately see which policy, regulation, or internal rule justified it. I’d also want the trace to work both ways, so from a policy or legal reference I can see all the requirements that came from it. If there are multiple sources, the system should show that clearly instead of forcing one single parent."

### [FR-009] (stated)
The system shall allow a user to view, from a policy or legal reference, all requirements that came from it.

**Source Evidence:**
- `[interview_turn:T020]` "Ideally, the links should be explicit and navigable, so if I open a requirement I can immediately see which policy, regulation, or internal rule justified it. I’d also want the trace to work both ways, so from a policy or legal reference I can see all the requirements that came from it. If there are multiple sources, the system should show that clearly instead of forcing one single parent."

### [FR-010] (stated)
The system shall support requirements with multiple source policies or legal references.

**Source Evidence:**
- `[interview_turn:T020]` "Ideally, the links should be explicit and navigable, so if I open a requirement I can immediately see which policy, regulation, or internal rule justified it. I’d also want the trace to work both ways, so from a policy or legal reference I can see all the requirements that came from it. If there are multiple sources, the system should show that clearly instead of forcing one single parent."
- `[interview_turn:T022]` "I’d treat all sources as valid, but it would still be useful to let users mark one as primary for convenience or reporting. In practice, some requirements come from several overlapping policies, and we shouldn’t lose that detail just to force a single origin. So the system should keep the full set of sources and allow one to be highlighted if needed."

### [FR-011] (stated)
The system shall keep the full set of sources for a requirement when multiple source policies or legal references apply.

**Source Evidence:**
- `[interview_turn:T020]` "Ideally, the links should be explicit and navigable, so if I open a requirement I can immediately see which policy, regulation, or internal rule justified it. I’d also want the trace to work both ways, so from a policy or legal reference I can see all the requirements that came from it. If there are multiple sources, the system should show that clearly instead of forcing one single parent."
- `[interview_turn:T022]` "I’d treat all sources as valid, but it would still be useful to let users mark one as primary for convenience or reporting. In practice, some requirements come from several overlapping policies, and we shouldn’t lose that detail just to force a single origin. So the system should keep the full set of sources and allow one to be highlighted if needed."

### [FR-012] (conditional)
The system shall allow users to mark one source as primary for convenience or reporting when a requirement has multiple sources.

**Source Evidence:**
- `[interview_turn:T022]` "I’d treat all sources as valid, but it would still be useful to let users mark one as primary for convenience or reporting. In practice, some requirements come from several overlapping policies, and we shouldn’t lose that detail just to force a single origin. So the system should keep the full set of sources and allow one to be highlighted if needed."

### [FR-013] (stated)
The system shall allow users to compare analyses produced by different people.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Requirements and privacy analysts need SPRAT, a collaborative workbench for aligning web-system requirements with privacy and security policies. Users should be able to capture goals, scenarios, policies, requirements, and legal-compliance information; trace goals back to their source policies; organize them with flexible classifications; and compare analyses produced by different people. Access should vary for administrators, project managers, analysts, and guests."
- `[interview_turn:T008]` "We want to centralize the whole analysis workflow so people can capture goals, scenarios, policies, requirements, and compliance notes in one place. The big improvement is making traceability and comparison easier, especially when different analysts produce slightly different interpretations. We also want the classifications to be flexible enough to match the way our teams actually work."

### [FR-014] (stated)
The system shall allow users to organize artifacts with flexible classifications.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Requirements and privacy analysts need SPRAT, a collaborative workbench for aligning web-system requirements with privacy and security policies. Users should be able to capture goals, scenarios, policies, requirements, and legal-compliance information; trace goals back to their source policies; organize them with flexible classifications; and compare analyses produced by different people. Access should vary for administrators, project managers, analysts, and guests."
- `[interview_turn:T008]` "We want to centralize the whole analysis workflow so people can capture goals, scenarios, policies, requirements, and compliance notes in one place. The big improvement is making traceability and comparison easier, especially when different analysts produce slightly different interpretations. We also want the classifications to be flexible enough to match the way our teams actually work."

### [FR-015] (stated)
The system shall provide role-based access control so that administrators, project managers, analysts, and guests do not all see or edit the same things.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Requirements and privacy analysts need SPRAT, a collaborative workbench for aligning web-system requirements with privacy and security policies. Users should be able to capture goals, scenarios, policies, requirements, and legal-compliance information; trace goals back to their source policies; organize them with flexible classifications; and compare analyses produced by different people. Access should vary for administrators, project managers, analysts, and guests."
- `[interview_turn:T010]` "Yes, role-based access is important too. Administrators, project managers, analysts, and guests should not all see or edit the same things, and we need a clear way to control that. It would also help if the tool supported collaboration without overwriting each other’s work."

### [FR-016] (stated)
The system shall support collaboration without users overwriting each other’s work.

**Source Evidence:**
- `[interview_turn:T010]` "Yes, role-based access is important too. Administrators, project managers, analysts, and guests should not all see or edit the same things, and we need a clear way to control that. It would also help if the tool supported collaboration without overwriting each other’s work."

### [FR-017] (stated)
The system shall record who changed what and when.

**Source Evidence:**
- `[interview_turn:T012]` "Yes, definitely. We would want to see who changed what and when, and ideally be able to go back if something was entered incorrectly or replaced by mistake. That would make the collaboration much safer and easier to review."

### [FR-018] (stated)
The system shall allow users to go back if something was entered incorrectly or replaced by mistake.

**Source Evidence:**
- `[interview_turn:T012]` "Yes, definitely. We would want to see who changed what and when, and ideally be able to go back if something was entered incorrectly or replaced by mistake. That would make the collaboration much safer and easier to review."

## 4. Business Rules and Constraints

### [BR-001] (stated)
The trace between artifacts shall work both ways between requirements and their source policies or legal references.

**Source Evidence:**
- `[interview_turn:T020]` "Ideally, the links should be explicit and navigable, so if I open a requirement I can immediately see which policy, regulation, or internal rule justified it. I’d also want the trace to work both ways, so from a policy or legal reference I can see all the requirements that came from it. If there are multiple sources, the system should show that clearly instead of forcing one single parent."

## 5. Data and External Interfaces

None specified.

## 6. Quality Requirements

### [QR-001] (stated)
The system shall make traceability and comparison easier than the current manual process.

**Source Evidence:**
- `[interview_turn:T006]` "Right now, most of it is spread across documents, spreadsheets, and email threads, so it’s pretty manual. People capture requirements in one place, keep policy references somewhere else, and then try to maintain traceability by hand, which makes comparisons and reviews difficult."
- `[interview_turn:T008]` "We want to centralize the whole analysis workflow so people can capture goals, scenarios, policies, requirements, and compliance notes in one place. The big improvement is making traceability and comparison easier, especially when different analysts produce slightly different interpretations. We also want the classifications to be flexible enough to match the way our teams actually work."

### [QR-002] (stated)
The system shall make collaboration safer and easier to review through versioning and change history.

**Source Evidence:**
- `[interview_turn:T012]` "Yes, definitely. We would want to see who changed what and when, and ideally be able to go back if something was entered incorrectly or replaced by mistake. That would make the collaboration much safer and easier to review."

## 7. Exceptions and Boundary Conditions

None specified.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
Whether any additional features beyond the main ones are required has not been decided and must be confirmed with the team.

**Source Evidence:**
- `[interview_turn:T014]` "I think those are the main ones. Anything beyond that would be nice to have, but I’d need to check with the team before saying it’s required."
