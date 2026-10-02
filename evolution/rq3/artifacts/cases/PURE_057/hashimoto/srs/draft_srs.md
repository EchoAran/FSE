# Software Requirements Specification: Security and Privacy Requirements Analysis Tool

## 1. Scope and Context

### [SC-001] (stated)
SPRAT is a collaborative workbench for aligning web-system requirements with privacy and security policies.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Requirements and privacy analysts need SPRAT, a collaborative workbench for aligning web-system requirements with privacy and security policies. Users should be able to capture goals, scenarios, policies, requirements, and legal-compliance information; trace goals back to their source policies; organize them with flexible classifications; and compare analyses produced by different people. Access should vary for administrators, project managers, analysts, and guests."

## 2. Actors

### [ST-001] (stated)
The system shall support administrators, project managers, analysts, and guests with role-based access.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Requirements and privacy analysts need SPRAT, a collaborative workbench for aligning web-system requirements with privacy and security policies. Users should be able to capture goals, scenarios, policies, requirements, and legal-compliance information; trace goals back to their source policies; organize them with flexible classifications; and compare analyses produced by different people. Access should vary for administrators, project managers, analysts, and guests."

## 3. Functional Requirements

### [FR-001] (stated)
The system shall allow users to capture goals, scenarios, policies, requirements, and legal-compliance information.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Requirements and privacy analysts need SPRAT, a collaborative workbench for aligning web-system requirements with privacy and security policies. Users should be able to capture goals, scenarios, policies, requirements, and legal-compliance information; trace goals back to their source policies; organize them with flexible classifications; and compare analyses produced by different people. Access should vary for administrators, project managers, analysts, and guests."

### [FR-002] (stated)
The system shall trace goals back to their source policies.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Requirements and privacy analysts need SPRAT, a collaborative workbench for aligning web-system requirements with privacy and security policies. Users should be able to capture goals, scenarios, policies, requirements, and legal-compliance information; trace goals back to their source policies; organize them with flexible classifications; and compare analyses produced by different people. Access should vary for administrators, project managers, analysts, and guests."

### [FR-003] (stated)
The system shall provide flexible classifications for organizing analysis items.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Requirements and privacy analysts need SPRAT, a collaborative workbench for aligning web-system requirements with privacy and security policies. Users should be able to capture goals, scenarios, policies, requirements, and legal-compliance information; trace goals back to their source policies; organize them with flexible classifications; and compare analyses produced by different people. Access should vary for administrators, project managers, analysts, and guests."

### [FR-004] (stated)
The system shall allow users to compare analyses produced by different people.

**Source Evidence:**
- `[initial_requirement:INITIAL_REQUIREMENTS]` "Requirements and privacy analysts need SPRAT, a collaborative workbench for aligning web-system requirements with privacy and security policies. Users should be able to capture goals, scenarios, policies, requirements, and legal-compliance information; trace goals back to their source policies; organize them with flexible classifications; and compare analyses produced by different people. Access should vary for administrators, project managers, analysts, and guests."

### [FR-005] (stated)
The system shall make it easier to connect security and privacy requirements back to the policies and legal obligations they came from without losing traceability.

**Source Evidence:**
- `[interview_turn:T002]` "From our perspective, SPRAT should make it much easier for analysts to connect security and privacy requirements back to the policies and legal obligations they came from, without losing traceability. It also needs to support collaboration, so different people can work on the same analysis, compare their results, and spot gaps or inconsistencies quickly.
We’d consider it successful if teams can produce more complete and consistent analyses in less time, with clear evidence of how each requirement was derived. Another big sign of success would be that people with different roles can use it appropriately, with access controlled in a way that protects sensitive information but doesn’t slow down the work."

### [FR-006] (stated)
The system shall support collaboration so different people can work on the same analysis, compare their results, and spot gaps or inconsistencies quickly.

**Source Evidence:**
- `[interview_turn:T002]` "From our perspective, SPRAT should make it much easier for analysts to connect security and privacy requirements back to the policies and legal obligations they came from, without losing traceability. It also needs to support collaboration, so different people can work on the same analysis, compare their results, and spot gaps or inconsistencies quickly.
We’d consider it successful if teams can produce more complete and consistent analyses in less time, with clear evidence of how each requirement was derived. Another big sign of success would be that people with different roles can use it appropriately, with access controlled in a way that protects sensitive information but doesn’t slow down the work."

### [FR-007] (stated)
The system shall provide clear evidence of how each requirement was derived.

**Source Evidence:**
- `[interview_turn:T002]` "From our perspective, SPRAT should make it much easier for analysts to connect security and privacy requirements back to the policies and legal obligations they came from, without losing traceability. It also needs to support collaboration, so different people can work on the same analysis, compare their results, and spot gaps or inconsistencies quickly.
We’d consider it successful if teams can produce more complete and consistent analyses in less time, with clear evidence of how each requirement was derived. Another big sign of success would be that people with different roles can use it appropriately, with access controlled in a way that protects sensitive information but doesn’t slow down the work."

### [FR-008] (stated)
The system shall control access so that people with different roles can use it appropriately while protecting sensitive information.

**Source Evidence:**
- `[interview_turn:T002]` "From our perspective, SPRAT should make it much easier for analysts to connect security and privacy requirements back to the policies and legal obligations they came from, without losing traceability. It also needs to support collaboration, so different people can work on the same analysis, compare their results, and spot gaps or inconsistencies quickly.
We’d consider it successful if teams can produce more complete and consistent analyses in less time, with clear evidence of how each requirement was derived. Another big sign of success would be that people with different roles can use it appropriately, with access controlled in a way that protects sensitive information but doesn’t slow down the work."

### [FR-009] (stated)
The system shall keep a full history of changes.

**Source Evidence:**
- `[interview_turn:T006]` "We do need a full history of changes, because in practice people will want to see how an analysis evolved and who made each change. It should identify the user, the timestamp, and ideally the reason for the change if they provide one, since that helps with review and accountability.
Side-by-side comparison of earlier versions is important, especially for spotting differences in goals, requirements, or trace links. Branching and merging might be useful, but I’d treat that as a nice-to-have unless teams are working in parallel a lot; I’m not sure we need full version-control style workflows on day one."

### [FR-010] (stated)
The system shall identify the user who made each change and the timestamp of the change.

**Source Evidence:**
- `[interview_turn:T006]` "We do need a full history of changes, because in practice people will want to see how an analysis evolved and who made each change. It should identify the user, the timestamp, and ideally the reason for the change if they provide one, since that helps with review and accountability.
Side-by-side comparison of earlier versions is important, especially for spotting differences in goals, requirements, or trace links. Branching and merging might be useful, but I’d treat that as a nice-to-have unless teams are working in parallel a lot; I’m not sure we need full version-control style workflows on day one."

### [FR-011] (conditional)
The system shall record the reason for a change when the user provides one.

**Source Evidence:**
- `[interview_turn:T006]` "We do need a full history of changes, because in practice people will want to see how an analysis evolved and who made each change. It should identify the user, the timestamp, and ideally the reason for the change if they provide one, since that helps with review and accountability.
Side-by-side comparison of earlier versions is important, especially for spotting differences in goals, requirements, or trace links. Branching and merging might be useful, but I’d treat that as a nice-to-have unless teams are working in parallel a lot; I’m not sure we need full version-control style workflows on day one."

### [FR-012] (stated)
The system shall support side-by-side comparison of earlier versions, especially for differences in goals, requirements, or trace links.

**Source Evidence:**
- `[interview_turn:T006]` "We do need a full history of changes, because in practice people will want to see how an analysis evolved and who made each change. It should identify the user, the timestamp, and ideally the reason for the change if they provide one, since that helps with review and accountability.
Side-by-side comparison of earlier versions is important, especially for spotting differences in goals, requirements, or trace links. Branching and merging might be useful, but I’d treat that as a nice-to-have unless teams are working in parallel a lot; I’m not sure we need full version-control style workflows on day one."

### [FR-013] (stated)
The system shall save changes immediately when an analyst edits an item.

**Source Evidence:**
- `[interview_turn:T008]` "The change should be saved immediately so the analyst doesn’t lose work, but it shouldn’t always be considered final right away. For most edits, I’d expect a draft or pending state until a review happens, especially when the change affects traceability, policy interpretation, or legal compliance.
I think peer review should be the normal path, with project managers stepping in for anything higher risk or contentious, and administrators only handling access or system-level issues. The exact approval rule probably depends on the project’s configuration, because not every team will want the same level of control."

### [FR-014] (stated)
For most edits, the system shall place the item in a draft or pending state until review occurs, especially when the change affects traceability, policy interpretation, or legal compliance.

**Source Evidence:**
- `[interview_turn:T008]` "The change should be saved immediately so the analyst doesn’t lose work, but it shouldn’t always be considered final right away. For most edits, I’d expect a draft or pending state until a review happens, especially when the change affects traceability, policy interpretation, or legal compliance.
I think peer review should be the normal path, with project managers stepping in for anything higher risk or contentious, and administrators only handling access or system-level issues. The exact approval rule probably depends on the project’s configuration, because not every team will want the same level of control."

### [FR-015] (stated)
The system shall use peer review as the normal review path, with project managers stepping in for higher-risk or contentious changes and administrators handling access or system-level issues.

**Source Evidence:**
- `[interview_turn:T008]` "The change should be saved immediately so the analyst doesn’t lose work, but it shouldn’t always be considered final right away. For most edits, I’d expect a draft or pending state until a review happens, especially when the change affects traceability, policy interpretation, or legal compliance.
I think peer review should be the normal path, with project managers stepping in for anything higher risk or contentious, and administrators only handling access or system-level issues. The exact approval rule probably depends on the project’s configuration, because not every team will want the same level of control."

### [FR-016] (stated)
While an item is in draft or pending, the analyst who created it shall be able to keep editing it.

**Source Evidence:**
- `[interview_turn:T010]` "While something is in draft or pending, the analyst who created it should be able to keep editing it and probably withdraw or revise it before review. Other analysts and project managers should at least be able to see that it exists, but I’d expect visibility to be limited if the item contains sensitive material or has not been approved yet.
It should move to reviewed or final only after the required reviewer signs off, and that approval should be recorded in the history. Once it’s final, edits should create a new revision rather than overwriting the approved one, so the approved version stays intact for audit and comparison."

### [FR-017] (stated)
While an item is in draft or pending, the analyst who created it shall be able to withdraw or revise it before review.

**Source Evidence:**
- `[interview_turn:T010]` "While something is in draft or pending, the analyst who created it should be able to keep editing it and probably withdraw or revise it before review. Other analysts and project managers should at least be able to see that it exists, but I’d expect visibility to be limited if the item contains sensitive material or has not been approved yet.
It should move to reviewed or final only after the required reviewer signs off, and that approval should be recorded in the history. Once it’s final, edits should create a new revision rather than overwriting the approved one, so the approved version stays intact for audit and comparison."

### [FR-018] (stated)
Other analysts and project managers shall be able to see that a draft exists.

**Source Evidence:**
- `[interview_turn:T010]` "While something is in draft or pending, the analyst who created it should be able to keep editing it and probably withdraw or revise it before review. Other analysts and project managers should at least be able to see that it exists, but I’d expect visibility to be limited if the item contains sensitive material or has not been approved yet.
It should move to reviewed or final only after the required reviewer signs off, and that approval should be recorded in the history. Once it’s final, edits should create a new revision rather than overwriting the approved one, so the approved version stays intact for audit and comparison."

### [FR-019] (stated)
The system shall limit visibility of draft items when they contain sensitive material or have not been approved yet.

**Source Evidence:**
- `[interview_turn:T010]` "While something is in draft or pending, the analyst who created it should be able to keep editing it and probably withdraw or revise it before review. Other analysts and project managers should at least be able to see that it exists, but I’d expect visibility to be limited if the item contains sensitive material or has not been approved yet.
It should move to reviewed or final only after the required reviewer signs off, and that approval should be recorded in the history. Once it’s final, edits should create a new revision rather than overwriting the approved one, so the approved version stays intact for audit and comparison."

### [FR-020] (stated)
An item shall move to reviewed or final only after the required reviewer signs off.

**Source Evidence:**
- `[interview_turn:T010]` "While something is in draft or pending, the analyst who created it should be able to keep editing it and probably withdraw or revise it before review. Other analysts and project managers should at least be able to see that it exists, but I’d expect visibility to be limited if the item contains sensitive material or has not been approved yet.
It should move to reviewed or final only after the required reviewer signs off, and that approval should be recorded in the history. Once it’s final, edits should create a new revision rather than overwriting the approved one, so the approved version stays intact for audit and comparison."

### [FR-021] (stated)
The system shall record approval in the history when an item is reviewed or finalized.

**Source Evidence:**
- `[interview_turn:T010]` "While something is in draft or pending, the analyst who created it should be able to keep editing it and probably withdraw or revise it before review. Other analysts and project managers should at least be able to see that it exists, but I’d expect visibility to be limited if the item contains sensitive material or has not been approved yet.
It should move to reviewed or final only after the required reviewer signs off, and that approval should be recorded in the history. Once it’s final, edits should create a new revision rather than overwriting the approved one, so the approved version stays intact for audit and comparison."

### [FR-022] (stated)
Once an item is final, edits shall create a new revision rather than overwriting the approved version.

**Source Evidence:**
- `[interview_turn:T010]` "While something is in draft or pending, the analyst who created it should be able to keep editing it and probably withdraw or revise it before review. Other analysts and project managers should at least be able to see that it exists, but I’d expect visibility to be limited if the item contains sensitive material or has not been approved yet.
It should move to reviewed or final only after the required reviewer signs off, and that approval should be recorded in the history. Once it’s final, edits should create a new revision rather than overwriting the approved one, so the approved version stays intact for audit and comparison."

### [FR-023] (stated)
The system shall keep the approved version intact for audit and comparison after finalization.

**Source Evidence:**
- `[interview_turn:T010]` "While something is in draft or pending, the analyst who created it should be able to keep editing it and probably withdraw or revise it before review. Other analysts and project managers should at least be able to see that it exists, but I’d expect visibility to be limited if the item contains sensitive material or has not been approved yet.
It should move to reviewed or final only after the required reviewer signs off, and that approval should be recorded in the history. Once it’s final, edits should create a new revision rather than overwriting the approved one, so the approved version stays intact for audit and comparison."

### [FR-024] (stated)
For draft items, other roles shall usually be able to see that a draft exists, who owns it, what it is roughly about, and its review status.

**Source Evidence:**
- `[interview_turn:T012]` "Other roles should usually be able to see that a draft exists, who owns it, what it is roughly about, and its review status, but not necessarily the full content if it’s sensitive or still under discussion. I’d expect project managers and assigned reviewers to see more detail than general analysts, while guests should probably see nothing about drafts unless a project explicitly allows it.
As a rule, the item’s existence and basic metadata can be visible to people with the right project access, but the content itself should be hidden until it is approved or explicitly shared. If an item is marked sensitive, then even the metadata may need to be limited to only the author, reviewers, and admins."

### [FR-025] (stated)
The system shall hide the full content of a draft item when it is sensitive or still under discussion.

**Source Evidence:**
- `[interview_turn:T012]` "Other roles should usually be able to see that a draft exists, who owns it, what it is roughly about, and its review status, but not necessarily the full content if it’s sensitive or still under discussion. I’d expect project managers and assigned reviewers to see more detail than general analysts, while guests should probably see nothing about drafts unless a project explicitly allows it.
As a rule, the item’s existence and basic metadata can be visible to people with the right project access, but the content itself should be hidden until it is approved or explicitly shared. If an item is marked sensitive, then even the metadata may need to be limited to only the author, reviewers, and admins."

### [FR-026] (stated)
Project managers and assigned reviewers shall see more detail than general analysts for draft items.

**Source Evidence:**
- `[interview_turn:T012]` "Other roles should usually be able to see that a draft exists, who owns it, what it is roughly about, and its review status, but not necessarily the full content if it’s sensitive or still under discussion. I’d expect project managers and assigned reviewers to see more detail than general analysts, while guests should probably see nothing about drafts unless a project explicitly allows it.
As a rule, the item’s existence and basic metadata can be visible to people with the right project access, but the content itself should be hidden until it is approved or explicitly shared. If an item is marked sensitive, then even the metadata may need to be limited to only the author, reviewers, and admins."

### [FR-027] (stated)
Guests shall not see anything about drafts unless a project explicitly allows it.

**Source Evidence:**
- `[interview_turn:T012]` "Other roles should usually be able to see that a draft exists, who owns it, what it is roughly about, and its review status, but not necessarily the full content if it’s sensitive or still under discussion. I’d expect project managers and assigned reviewers to see more detail than general analysts, while guests should probably see nothing about drafts unless a project explicitly allows it.
As a rule, the item’s existence and basic metadata can be visible to people with the right project access, but the content itself should be hidden until it is approved or explicitly shared. If an item is marked sensitive, then even the metadata may need to be limited to only the author, reviewers, and admins."

### [FR-028] (stated)
For users with the right project access, the system shall make an item's existence and basic metadata visible, but keep the content hidden until the item is approved or explicitly shared.

**Source Evidence:**
- `[interview_turn:T012]` "Other roles should usually be able to see that a draft exists, who owns it, what it is roughly about, and its review status, but not necessarily the full content if it’s sensitive or still under discussion. I’d expect project managers and assigned reviewers to see more detail than general analysts, while guests should probably see nothing about drafts unless a project explicitly allows it.
As a rule, the item’s existence and basic metadata can be visible to people with the right project access, but the content itself should be hidden until it is approved or explicitly shared. If an item is marked sensitive, then even the metadata may need to be limited to only the author, reviewers, and admins."

### [FR-029] (stated)
If an item is marked sensitive, the system shall limit even the metadata to the author, reviewers, and administrators.

**Source Evidence:**
- `[interview_turn:T012]` "Other roles should usually be able to see that a draft exists, who owns it, what it is roughly about, and its review status, but not necessarily the full content if it’s sensitive or still under discussion. I’d expect project managers and assigned reviewers to see more detail than general analysts, while guests should probably see nothing about drafts unless a project explicitly allows it.
As a rule, the item’s existence and basic metadata can be visible to people with the right project access, but the content itself should be hidden until it is approved or explicitly shared. If an item is marked sensitive, then even the metadata may need to be limited to only the author, reviewers, and admins."

### [FR-030] (stated)
During import, the system shall preserve the structure of the analysis, including goals, scenarios, requirements, policy links, and traceability.

**Source Evidence:**
- `[interview_turn:T014]` "We definitely expect SPRAT to import from common document sources and possibly spreadsheets or structured exports from other requirements tools, since a lot of analyses start outside the system. I’d also expect support for importing policy or compliance references from upstream repositories if the team already maintains those separately, but I’m not sure we’ve narrowed down the exact systems yet.
What matters most is preserving the structure of the analysis, not just the text, so goals, scenarios, requirements, policy links, and traceability need to come across intact. If there are classifications, tags, or version references in the source, those should be retained too where possible, though we may need to map them if the source format doesn’t match SPRAT exactly."

### [FR-031] (stated)
During import, the system shall retain classifications, tags, and version references where possible.

**Source Evidence:**
- `[interview_turn:T014]` "We definitely expect SPRAT to import from common document sources and possibly spreadsheets or structured exports from other requirements tools, since a lot of analyses start outside the system. I’d also expect support for importing policy or compliance references from upstream repositories if the team already maintains those separately, but I’m not sure we’ve narrowed down the exact systems yet.
What matters most is preserving the structure of the analysis, not just the text, so goals, scenarios, requirements, policy links, and traceability need to come across intact. If there are classifications, tags, or version references in the source, those should be retained too where possible, though we may need to map them if the source format doesn’t match SPRAT exactly."

## 4. Business Rules and Constraints

None specified.

## 5. Data and External Interfaces

### [DI-001] (stated)
The system shall import from common document sources.

**Source Evidence:**
- `[interview_turn:T014]` "We definitely expect SPRAT to import from common document sources and possibly spreadsheets or structured exports from other requirements tools, since a lot of analyses start outside the system. I’d also expect support for importing policy or compliance references from upstream repositories if the team already maintains those separately, but I’m not sure we’ve narrowed down the exact systems yet.
What matters most is preserving the structure of the analysis, not just the text, so goals, scenarios, requirements, policy links, and traceability need to come across intact. If there are classifications, tags, or version references in the source, those should be retained too where possible, though we may need to map them if the source format doesn’t match SPRAT exactly."

### [DI-002] (stated)
The system shall import from spreadsheets or structured exports from other requirements tools.

**Source Evidence:**
- `[interview_turn:T014]` "We definitely expect SPRAT to import from common document sources and possibly spreadsheets or structured exports from other requirements tools, since a lot of analyses start outside the system. I’d also expect support for importing policy or compliance references from upstream repositories if the team already maintains those separately, but I’m not sure we’ve narrowed down the exact systems yet.
What matters most is preserving the structure of the analysis, not just the text, so goals, scenarios, requirements, policy links, and traceability need to come across intact. If there are classifications, tags, or version references in the source, those should be retained too where possible, though we may need to map them if the source format doesn’t match SPRAT exactly."

### [DI-003] (stated)
The system shall support importing policy or compliance references from upstream repositories.

**Source Evidence:**
- `[interview_turn:T014]` "We definitely expect SPRAT to import from common document sources and possibly spreadsheets or structured exports from other requirements tools, since a lot of analyses start outside the system. I’d also expect support for importing policy or compliance references from upstream repositories if the team already maintains those separately, but I’m not sure we’ve narrowed down the exact systems yet.
What matters most is preserving the structure of the analysis, not just the text, so goals, scenarios, requirements, policy links, and traceability need to come across intact. If there are classifications, tags, or version references in the source, those should be retained too where possible, though we may need to map them if the source format doesn’t match SPRAT exactly."

## 6. Quality Requirements

### [QR-001] (stated)
The system shall support producing more complete and consistent analyses in less time.

**Source Evidence:**
- `[interview_turn:T002]` "From our perspective, SPRAT should make it much easier for analysts to connect security and privacy requirements back to the policies and legal obligations they came from, without losing traceability. It also needs to support collaboration, so different people can work on the same analysis, compare their results, and spot gaps or inconsistencies quickly.
We’d consider it successful if teams can produce more complete and consistent analyses in less time, with clear evidence of how each requirement was derived. Another big sign of success would be that people with different roles can use it appropriately, with access controlled in a way that protects sensitive information but doesn’t slow down the work."

## 7. Exceptions and Boundary Conditions

### [EX-001] (stated)
If a source policy is incomplete or a legal obligation is missing, the system shall let the analyst flag the gap, record assumptions, and mark the item as unresolved so it is visible in the analysis.

**Source Evidence:**
- `[interview_turn:T004]` "Yes, those situations do come up, and SPRAT should handle them explicitly instead of forcing analysts to pretend everything is complete. If a source policy is incomplete or a legal obligation is missing, the system should let the analyst flag that gap, record assumptions, and mark the item as unresolved so it’s visible in the analysis.
For conflicting policies or requirements, SPRAT should allow both versions to be captured and highlight the conflict so a reviewer can resolve it later. And if traceability can’t be established for something, that should be treated as a documented exception, not silently ignored, so partial analyses are still usable and clearly labeled as partial."

### [EX-002] (stated)
For conflicting policies or requirements, the system shall allow both versions to be captured and highlight the conflict for later resolution.

**Source Evidence:**
- `[interview_turn:T004]` "Yes, those situations do come up, and SPRAT should handle them explicitly instead of forcing analysts to pretend everything is complete. If a source policy is incomplete or a legal obligation is missing, the system should let the analyst flag that gap, record assumptions, and mark the item as unresolved so it’s visible in the analysis.
For conflicting policies or requirements, SPRAT should allow both versions to be captured and highlight the conflict so a reviewer can resolve it later. And if traceability can’t be established for something, that should be treated as a documented exception, not silently ignored, so partial analyses are still usable and clearly labeled as partial."

### [EX-003] (stated)
If traceability cannot be established for an item, the system shall treat it as a documented exception rather than silently ignoring it, so partial analyses remain usable and clearly labeled as partial.

**Source Evidence:**
- `[interview_turn:T004]` "Yes, those situations do come up, and SPRAT should handle them explicitly instead of forcing analysts to pretend everything is complete. If a source policy is incomplete or a legal obligation is missing, the system should let the analyst flag that gap, record assumptions, and mark the item as unresolved so it’s visible in the analysis.
For conflicting policies or requirements, SPRAT should allow both versions to be captured and highlight the conflict so a reviewer can resolve it later. And if traceability can’t be established for something, that should be treated as a documented exception, not silently ignored, so partial analyses are still usable and clearly labeled as partial."

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
Whether the system should support branching and merging is not yet decided.

**Source Evidence:**
- `[interview_turn:T006]` "We do need a full history of changes, because in practice people will want to see how an analysis evolved and who made each change. It should identify the user, the timestamp, and ideally the reason for the change if they provide one, since that helps with review and accountability.
Side-by-side comparison of earlier versions is important, especially for spotting differences in goals, requirements, or trace links. Branching and merging might be useful, but I’d treat that as a nice-to-have unless teams are working in parallel a lot; I’m not sure we need full version-control style workflows on day one."

### [UN-002]
The exact approval rule for changes depends on the project's configuration and is not yet specified.

**Source Evidence:**
- `[interview_turn:T008]` "The change should be saved immediately so the analyst doesn’t lose work, but it shouldn’t always be considered final right away. For most edits, I’d expect a draft or pending state until a review happens, especially when the change affects traceability, policy interpretation, or legal compliance.
I think peer review should be the normal path, with project managers stepping in for anything higher risk or contentious, and administrators only handling access or system-level issues. The exact approval rule probably depends on the project’s configuration, because not every team will want the same level of control."
