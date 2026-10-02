# Software Requirements Specification: Security and Privacy Requirements Analysis Tool

## 1. Scope and Context

### [SC-001]
SPRAT is a collaborative workbench for aligning web-system requirements with privacy and security policies.

### [SC-002]
SPRAT shall centralize goals, scenarios, policies, requirements, and compliance information in one place to support consistent reasoning and traceability.

### [SC-003]
SPRAT shall fit into existing requirements and project workflows used alongside document and issue-tracking tools.

## 2. Actors

### [SA-001]
The system shall support the roles of administrator, project manager, analyst, and guest.

### [SA-002]
Administrators shall manage the system and user access.

### [SA-003]
Project managers shall oversee projects and review work.

### [SA-004]
Analysts shall create and update requirements and policy mappings.

### [SA-005]
Guests shall have limited read-only access.

## 3. Functional Requirements

### [FR-001]
The system shall support capturing goals, scenarios, policies, requirements, and compliance references.

### [FR-002]
The system shall support tracing goals back to their source policies.

### [FR-003]
The system shall support comparing analyses produced by different analysts.

### [FR-004]
The system shall support side-by-side comparison of analyses.

### [FR-005]
The system shall show when two analysts traced the same goal to different policies or produced different requirements.

### [FR-006]
The system shall support comments or discussion notes tied directly to a disputed item.

### [FR-007]
The system shall support a controlled vocabulary or shared glossary.

### [FR-008]
The system shall show accepted definitions when a user enters a term.

### [FR-009]
The system shall warn when a new term is too close to an existing one or is being used inconsistently.

### [FR-010]
The system shall check terms as they are entered and flag likely duplicates, near matches, or uses that do not fit the approved definition.

### [FR-011]
The system shall provide immediate but non-disruptive term-entry warnings.

### [FR-012]
The system shall allow analysts to reuse a term, revise it, or add a clarification in response to a term-entry warning.

### [FR-013]
The system shall show the existing context for a term during entry.

### [FR-014]
The system shall provide hard errors only when something is clearly invalid or not allowed.

### [FR-015]
The system shall provide softer warnings for possible duplicates, ambiguous wording, or terms that do not exactly match the glossary.

### [FR-016]
The system shall provide suggestions for approved alternative terms and examples of prior usage.

### [FR-017]
The system shall allow analysts to accept a suggested term with one click.

### [FR-018]
The system shall capture rationale, source notes, assumptions, and status for artifacts.

### [FR-019]
The system shall organize artifacts by project or analysis case.

### [FR-020]
The system shall support organizing artifacts by system, stakeholder, or policy source.

### [FR-021]
The system shall support artifact lifecycle states including draft, review, approved or accepted, and archived.

### [FR-022]
The system shall support versioning so that older versions remain traceable for audit and comparison.

### [FR-023]
The system shall keep archived items searchable and traceable.

### [FR-025]
The system shall allow reviewers to comment and suggest changes without silently altering the approved record.

### [FR-026]
The system shall allow guests to have read-only access.

### [FR-027]
The system shall detect overlapping edits and warn the user before changes are finalized.

### [FR-028]
The system shall flag broken trace links and records that point to deleted policies.

### [FR-029]
The system shall keep records recoverable when a consistency issue is detected.

### [FR-030]
The system shall show who made the last change and what changed for conflict resolution.

### [FR-031]
The system shall provide a guided resolution workflow for conflicts.

### [FR-032]
The system shall show conflicting versions side by side and highlight exactly what changed.

### [FR-033]
The system shall send notifications to the people involved in a conflict.

### [FR-034]
The system shall provide a comment thread or notes area for conflict resolution.

### [FR-035]
The system shall allow the user to merge conflicting content, keep one version, or reopen the item for further review depending on the situation.

### [FR-036]
The system shall support importing source policies and supporting files from document repositories.

### [FR-039]
The system shall preserve source, timestamps, ownership, and existing trace links or classifications during migration when they can be mapped cleanly.

### [FR-040]
The system shall preserve the original value and mark it for review when a link or field cannot be resolved automatically during import.

### [FR-041]
The system shall support a guided import process that lets a user match fields, preview incoming data, and catch missing links before data is committed.

### [FR-042]
The system shall import data into a staging area before publishing it into the live project.

### [FR-043]
The system shall keep unmatched items or broken links visible in a review queue until someone confirms them.

### [FR-044]
The system shall support notifications or watch alerts when a related policy, requirement, or trace link is updated and needs review.

### [FR-045]
The system shall keep old link history and show what was updated when a mapping changes.

### [FR-046]
The system shall allow analysts to compare before and after values when a mapping changes.

### [FR-047]
The system shall distinguish items still inherited from import from items that have been manually corrected.

### [FR-048]
The system shall stop automation and flag a set for human review when automatic mapping is incorrect in context or when a source file changes structure after import.

### [FR-049]
The system shall preserve original data when automatic mapping or batch updates fail unexpectedly.

### [FR-050]
The system shall surface high-priority updates first, especially when they are tied to legal compliance, a security control, or a policy that affects multiple requirements.

### [FR-051]
The system shall show impact counts, urgency, and whether a change breaks existing traceability to help analysts prioritize updates.

### [FR-052]
The system shall make flagged items visible in the workspace with a status such as needs review, conflicting mapping, or unresolved import.

### [FR-053]
The system shall show the original source value, the suggested mapping if one exists, and the reason a mapping was rejected or left ambiguous.

### [FR-054]
The system shall allow analysts to open a flagged item, compare competing values, choose the correct mapping or mark it for escalation, and record the decision.

### [FR-055]
The system shall log who made a conflict or import resolution decision, when it was made, and what evidence or reasoning was used.

### [FR-056]
The system shall update related trace links and mark the item as resolved after a resolution.

### [FR-057]
The system shall keep the previous state available for audit after a resolution.

### [FR-058]
The system shall provide a notification or activity feed entry when a conflict has been handled and when downstream items are affected.

### [FR-059]
The system shall support a dashboard-style interface with quick access to the current project, recent items, unresolved conflicts, and review tasks.

### [FR-060]
The system shall provide fast search and filtering across goals, requirements, policies, and trace links.

### [FR-061]
The system shall support templates, autocomplete, and inline editing to reduce repetitive data entry.

### [FR-062]
The system shall save changes automatically and give clear feedback when something has not synced yet.

### [FR-063]
The system shall provide a clear indicator for saved, pending sync, and failed sync states.

### [FR-064]
The system shall support easy recovery from interrupted sessions.

### [FR-066]
The system shall update small parts of the screen instead of requiring long full-page refreshes.

### [FR-068]
The system shall provide a guided first-use walkthrough.

### [FR-069]
The walkthrough shall cover how goals, policies, and requirements connect, and it shall include the main workflow of creating or opening a project, adding a goal or requirement, linking it back to a policy, and reviewing traceability.

### [FR-070]
The system shall provide short contextual help inside the screens.

### [FR-071]
The system shall provide sample projects or templates for new users.

### [FR-072]
The walkthrough shall be interactive enough for a user to complete one small example, but not so long that the user feels trapped in a tutorial.

### [FR-073]
The system shall provide plain-language explanations for classifications, compliance fields, and comparison views when users first encounter them.

### [FR-074]
The system shall explain autosave and sync status early in onboarding.

### [FR-075]
The system shall provide a clear recovery message if the connection drops.

### [FR-076]
The system shall avoid vague warnings and technical jargon when reporting sync or recovery problems.

### [FR-077]
The system shall support collaboration changes that are easy to review without reloading everything.

### [FR-078]
The system shall support incremental loading of data rather than rendering everything at once in large projects.

### [FR-079]
The system shall avoid locking people out while others are editing and shall support concurrent work being visible and reconciled cleanly.

### [FR-080]
The system shall support keeping projects isolated enough that one large project does not slow down other projects.

### [FR-081]
The system shall support loading commonly used views quickly without waiting for the entire project to load.

### [FR-082]
The system shall support graceful handling of disconnects.

### [FR-083]
The system shall prevent users from losing work if the connection drops temporarily.

### [FR-084]
The system shall run in the organization’s managed environment unless public cloud deployment is specifically approved.

## 4. Business Rules and Constraints

### [BR-001]
The system shall use role-based permissions so only the right people can edit sensitive analysis content or view work that is not meant to be shared broadly.

### [BR-002]
The system shall restrict editing once an artifact is approved unless a user creates a new version or has admin-level permission to reopen it.

### [BR-003]
Hard errors shall be used only when something is clearly invalid or not allowed.

### [BR-004]
Approved older versions shall remain accessible for audit purposes and shall not be overwritten.

### [BR-005]
Imported data shall be reviewed before publication to the live project.

### [BR-006]
The system shall stop automation and require human review when an import mapping is ambiguous or contextually incorrect.

### [BR-007]
The system shall prioritize items with higher compliance or project risk over lower-risk items.

## 5. Data and External Interfaces

### [DI-001]
The system shall support import and export in common formats.

### [DI-002]
The system shall support importing from document repositories.

### [DI-003]
The system shall support linking to issue-tracking items or syncing basic status with issue-tracking systems.

### [DI-004]
The system shall support migration input from structured documents such as spreadsheets, Word files, and exported requirement databases.

### [DI-005]
The system shall support import of legacy documents, analyses, and traceability information into a staging area.

### [DI-006]
The system shall preserve and display the original source value when an imported item cannot be mapped automatically.

### [DI-007]
The system shall support showing the suggested mapping for an imported item when one exists.

## 6. Quality Requirements

### [FR-065]
The system shall be lightweight and responsive and avoid heavy pages or long full-page refreshes.

### [FR-067]
The system shall keep the most important project information accessible when the connection is slow.

### [QR-001]
The system shall reduce the time required to complete an analysis.

### [QR-002]
The system shall reduce missing traces between requirements and source policies.

### [QR-003]
The system shall reduce issues found later during review or compliance checking.

### [QR-004]
The system shall improve consistency between analysts.

### [QR-005]
The system shall be responsive as projects grow and shall not feel sluggish as the number of users, projects, artifacts, or trace links increases.

### [QR-006]
The system shall remain usable over slow or unstable connections and through VPN or secured remote access.

### [QR-007]
The system shall comply with internal security policies including single sign-on and role-based access.

### [QR-008]
The system shall provide access control, audit logging, and secure storage because it is treated as a sensitive internal system.

### [QR-009]
The system shall be resilient to slow connections and session timeouts.

### [QR-010]
The system shall keep users from losing work when a connection drops temporarily.

### [QR-011]
The interface shall be clean, lightweight, and responsive.

### [QR-012]
The system shall be forgiving and low-friction for analysts to use.

### [QR-013]
The system shall minimize repetitive data entry.

### [QR-014]
The system shall make comparison, search, filtering, and cross-references fast even with large datasets and many trace links.

### [QR-015]
The system shall keep the interface usable and avoid clutter when artifact counts are high.

### [QR-016]
The system shall provide clear status labels and plain-language messages for sync and recovery problems.

### [QR-017]
The system shall provide a notification digest or summary view for minor flagged items instead of excessive alerts.

### [QR-018]
The system shall allow analysts to manage collaboration without having to switch to email.

## 7. Exceptions and Boundary Conditions

### [EX-001]
When multiple analysts edit related items at the same time, the system shall detect overlapping edits and warn the user before changes are finalized.

### [EX-002]
When a requirement points to a deleted policy or a trace link is broken, the system shall flag the problem and keep the record recoverable.

### [EX-003]
When a connection drops or a session is interrupted, the system shall preserve the user’s work and provide recovery guidance.

### [EX-004]
When automatic mapping or batch updates fail unexpectedly, the system shall preserve the original data and flag the affected set for human review rather than forcing a best guess.

### [EX-005]
When imported items or mappings are ambiguous, the system shall keep them visible in a review queue until someone confirms them.

### [EX-006]
When an artifact is archived, the system shall allow it to be viewed and traced, and it shall clearly mark it so users do not mistake it for current requirements.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
The exact hosting setup for SPRAT needs to be confirmed with IT.

### [UN-002]
The specific external systems SPRAT should integrate with directly are not yet confirmed.

### [UN-003]
The exact formal KPI targets for analysis time reduction, error reduction, and compliance improvement have not yet been defined.

### [UN-004]
The specific legacy formats that SPRAT must support during migration have not yet been confirmed.

### [UN-005]
Whether full offline editing is required is not yet decided.

### [UN-006]
Whether public cloud deployment is allowed depends on specific approval.
