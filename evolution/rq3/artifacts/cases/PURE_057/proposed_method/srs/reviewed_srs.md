# Software Requirements Specification: Security and Privacy Requirements Analysis Tool

## 1. Scope and Context

### [SC-001]
SPRAT is a collaborative workbench for aligning web-system requirements with privacy and security policies.

### [SC-002]
SPRAT is intended for use during requirements and analysis work before design is finalized, and it remains useful during review, change impact analysis, and compliance checks.

## 2. Actors

### [AK-001]
The system shall support administrators, project managers, analysts, and guests with role-appropriate access.

## 3. Functional Requirements

### [FR-001]
The system shall allow users to capture goals, scenarios, policies, requirements, and legal-compliance information.

### [FR-002]
The system shall allow users to link requirements, goals, policies, scenarios, and derived analyses so that the rationale is traceable.

### [FR-003]
The system shall support tracing a requirement or goal back to its source policy or legal rule.

### [FR-004]
The system shall record the source policy reference, the exact part of the policy that justifies the goal or requirement, and a short rationale for the trace.

### [FR-005]
The system shall show which requirement supports which goal and which policy or legal source justified that goal or requirement.

### [FR-006]
The system shall represent many-to-many relationships among requirements, goals, and policies.

### [FR-007]
The system shall make overlaps and shared dependencies visible rather than hiding them under a single path.

### [FR-008]
The system shall show all relevant links when an item belongs to multiple paths and, if the team has designated one, clearly indicate which link is primary.

### [FR-009]
The system shall allow users to compare two analyses side by side.

### [FR-010]
When comparing analyses, the system shall show where goals, policies, and requirements match, differ, or exist in one analysis but not the other.

### [FR-011]
When comparing analyses, the system shall make visible when two people traced the same requirement back to different source policies.

### [FR-012]
The system shall allow analysts to independently build analyses and then compare them without losing the reasoning behind decisions.

### [FR-013]
The system shall support review, comment, compare-analysis, and traceability-check activities for project managers.

### [FR-014]
The system shall allow guests to view approved materials and, if allowed, compare published analyses.

### [FR-015]
The system shall allow users to organize analysis items with flexible classifications.

### [FR-016]
The system shall allow an artifact to have multiple classifications when it naturally belongs in more than one view.

### [FR-017]
The system shall allow reclassification later when an analyst is refining the analysis or correcting an early placeholder, provided the history is preserved.

### [FR-018]
The system shall allow derived-from links to remain visible even if the source item is later revised or marked inactive.

### [FR-019]
The system shall allow derived-from links to chain through multiple levels when that history matters, while keeping the direct parent clear.

### [FR-020]
The system shall preserve intermediate goals or policy versions in a requirement trace when they help explain the justification path, while keeping the direct policy link prominent.

### [FR-021]
The system shall support a gradual migration of existing analysis work into SPRAT.

### [FR-022]
The system shall allow migrated work to preserve traceability and context so it remains trustworthy and reviewable.

### [FR-023]
During migration, the system shall bring over the core content and links needed for active work, while leaving formatting or historical clutter behind if necessary.

### [FR-024]
The system shall migrate active projects, authoritative source documents, and items needed to maintain traceability for current work first.

### [FR-025]
The system shall include any linked policy source, specific obligation reference, and current supporting notes or evidence needed to prove or understand an active trace link.

### [FR-026]
The system shall support review-only use for project managers and read-only use for guests.

### [FR-027]
The system shall restrict guests from changing anything or viewing restricted details.

### [FR-028]
The system shall block guests from viewing sensitive notes, draft legal-compliance information, and unapproved trace links unless the project owner explicitly grants access.

### [FR-029]
The system shall support web access for office and remote working setups.

### [FR-030]
For sensitive projects, the system shall allow access only from approved corporate networks or trusted devices, and remote access shall require stronger authentication and, for especially sensitive work, explicit approval.

### [FR-031]
The system shall support an exception process for urgent access in sensitive projects, and the exception shall be logged and time-limited.

### [FR-032]
The system shall support basic capture and trace tasks with minimal guidance for new analysts.

### [FR-033]
The system shall allow new analysts in low-risk projects to perform simple editing, reclassifying, and linking to ordinary source types without heavy approval friction once they have learned the workflow.

### [FR-034]
The system shall require project manager or more experienced analyst review before a new analyst can finalize or publish traces in sensitive projects.

### [FR-035]
The system shall support guided setup, examples of acceptable classifications, and a short administrator or project manager review for very sensitive projects or complex policy sets.

### [FR-036]
The system shall provide inline explanations for how comparisons are interpreted.

### [FR-037]
The system shall support capturing a clear title or name and a description for each analysis item.

### [FR-038]
The system shall capture actor, trigger, and outcome for scenarios.

### [FR-039]
The system shall require trace links when a requirement claims to come from a policy.

### [FR-040]
The system shall flag missing or inconsistent classifications rather than silently accepting them.

### [FR-041]
The system shall check structural consistency of the analysis, including whether links exist, whether classifications are used properly, and whether obvious trace gaps are present.

### [FR-042]
The system shall flag questionable analysis content clearly and leave semantic judgment to the analyst or reviewer.

### [FR-043]
The system shall record who made a trace and when it was added.

### [FR-044]
The system shall allow a goal to be supported by several policies together, and it shall allow a trace to be indirect through a requirement or scenario when the relationship is still explainable.

### [FR-045]
The system shall allow analysts to derive requirements from other requirements or from scenarios, and derived-from links shall remain visible even if the source item changes.

### [FR-046]
The system shall show the direct parent in a derived-from chain so the trail is not ambiguous.

### [FR-047]
The system shall preserve a basic audit trail that shows what changed, who changed it, and when it changed.

### [FR-048]
The system shall record the previous version or enough detail to reconstruct the earlier state for goals, requirements, policies, and traces.

### [FR-049]
The system shall show which downstream items were derived from or reviewed against a changed artifact.

### [FR-050]
The system shall support exports in at least one structured machine-readable format such as CSV or JSON and one human-readable format such as PDF or Word.

### [FR-051]
Exports shall preserve trace links and audit metadata.

### [FR-052]
The system shall restrict raw exports to authorized roles.

### [FR-053]
For external sharing, the system shall require a redacted or approved version rather than an unfiltered export.

### [FR-054]
The system shall allow exports to be redacted or blocked when they include personal data, legal interpretations, unresolved disputes, or security weaknesses, depending on sensitivity.

### [FR-055]
The system shall require explicit approval before release when an export could identify individuals or expose a control gap, even if the export can be shared at all.

### [FR-056]
The system shall automatically reduce export detail for lower roles by excluding draft comments, sensitive source links, and personal data.

### [FR-057]
The system shall block export when the user is trying to pull information classified above their clearance or outside their project scope.

### [FR-058]
The system shall provide a mechanism to flag ownership-unclear changes for review and keep the request pending until someone with authority confirms it.

### [FR-059]
The system shall support a fallback process when the responsible person is temporarily unavailable, and the fallback shall be explicit and auditable.

### [FR-060]
The system shall store classifications, rules, and permissions in a way that preserves versioned history or clear provenance instead of rewriting old decisions.

### [FR-061]
The system shall show what changed, when it changed, and which analyses were affected when classifications, rules, or permissions change.

### [FR-062]
The system shall support a strong validation role for the analysis by catching mistakes that would undermine review confidence.

### [FR-063]
The system shall keep a trace link visible when a requirement is traced back to its source policy, and the trace shall preserve intermediate goals or policy versions when that helps explain the justification path.

## 4. Business Rules and Constraints

### [BR-001]
A requirement may be traced to several goals, and one policy may drive many requirements.

### [BR-002]
If a requirement was derived through another requirement or scenario, that connection should be visible.

### [BR-003]
Nothing should be lost just because it appears in more than one analysis route.

### [BR-004]
When an item belongs to multiple paths, the system shall show all relevant links.

### [BR-005]
For sensitive projects, tighter access controls apply, especially for guests and analysts who are not assigned to that project.

### [BR-006]
If location or device restrictions are used, they shall be driven by project sensitivity and the administrator’s policy.

### [BR-007]
One requirement may map to several goals, and one policy may drive many requirements.

### [BR-008]
A classification may be locked when changing it would break established trace links, access rules, or compliance reporting.

### [BR-009]
A classification change that could alter traceability, access, or compliance evidence shall go through review first unless it is an obvious correction that does not change meaning or visibility.

### [BR-010]
Obvious corrections may be applied immediately, but the system shall still log the before and after values and who made the change.

### [BR-011]
The first release should include core collaboration and traceability functions and basic role-based access control.

### [BR-012]
Deep workflow automation, advanced analytics dashboards, and tight integration with every possible document repository are excluded from the first release unless they are essential for a pilot customer or an unmet compliance obligation.

### [BR-013]
If a deferred capability is essential for a pilot customer or compliance obligation, the smallest acceptable version shall do only the one necessary thing and must fit inside the same capture, trace, and compare flow without breaking access control, redaction, or the ability to review and revise analyses.

### [BR-014]
An exception workaround shall be owned by the person accountable for the pilot or compliance outcome, usually the project manager or lead analyst.

### [BR-015]
A workaround shall be tracked in SPRAT as a time-bounded exception with the reason, the workaround used, and the target date or condition for closing it.

### [BR-016]
A workaround shall stop when the deadline is met, the required integration becomes available, or the compliance evidence has been formally accepted and archived.

### [BR-017]
A feature may be considered essential only when the pilot or compliance need cannot be met without it using the normal SPRAT workflow and a real deadline or contractual expectation exists.

### [BR-018]
When a feature is treated as essential, it shall remain limited to the smallest path that directly supports the specific pilot or compliance outcome and does not expand to broader teams, extra document types, or broader reporting.

### [BR-019]
If the action is routine, low risk, and based on an approved template or previously validated pattern, the system may allow a fast path while still capturing who did it, what changed, when it happened, and which source policy or requirement it came from.

### [BR-020]
If the action affects sensitive classifications, legal compliance, access permissions, or a new trace link, the system shall not allow the user to skip extra steps.

### [BR-021]
For sensitive projects, location and device restrictions shall allow access only from approved corporate networks or trusted devices, with stronger authentication for remote access and explicit approval for especially sensitive work.

### [BR-022]
An urgent-access exception for sensitive projects shall be logged and time-limited.

## 5. Data and External Interfaces

None specified.

## 6. Quality Requirements

### [QR-001]
The system shall be available during normal working hours at minimum and should be close to always on.

### [QR-002]
If the system goes down briefly, users shall not lose current work and shall be able to pick up again quickly.

### [QR-003]
The system shall remain responsive for search, trace navigation, saving analyses, loading dense analyses, tracing links, comparing outputs, large imports, and bulk updates.

### [QR-004]
Minor slowdowns are acceptable, but noticeable sluggishness in search, trace navigation, or saving analyses is not acceptable for day-to-day workflow.

### [QR-005]
The system shall support a modest but steady level of concurrent use, approximately a few dozen people at once, while keeping responsiveness acceptable.

### [QR-006]
The system shall handle bursts such as heavy collaborative sessions, large imports, bulk updates, and cross-project reviews without unacceptable slowdown.

### [QR-007]
The system shall be usable from a normal office or remote working setup through the web without special tooling.

### [QR-008]
New analysts should be able to start basic capture and trace tasks with minimal guidance.

### [QR-009]
Advanced classification and comparison features should require more onboarding than basic capture and trace tasks.

### [QR-010]
For very sensitive projects or complex policy sets, the system shall provide guided setup, examples of acceptable classifications, and inline explanations for comparison interpretation.

### [QR-011]
The system shall preserve the original context of migrated and changed analysis work rather than overwriting it.

### [QR-012]
The system shall preserve audit trail information and traceability during migration and export.

## 7. Exceptions and Boundary Conditions

### [EX-001]
Comparing analyses is intended to make sense within the same project or at least the same policy context; comparing unrelated analyses is probably not useful.

### [EX-002]
For low-risk projects, basic capture tasks should mostly remain self-service once the workflow is learned, except that final approval or changes to official compliance wording remain behind a more senior role.

### [EX-003]
A source type that is especially sensitive, such as a legal interpretation or a policy exception, may still require a review step even in a low-risk project.

### [EX-004]
The system shall allow an immediate classification change only for obvious corrections that do not change meaning or visibility.

### [EX-005]
If there is any doubt about the impact of a classification change on traceability, access, or compliance evidence, the change shall be treated as review required.

### [EX-006]
A minimal essential capability shall stay out of scope if it starts serving additional teams, extra document types, broader reporting, or future-proofing beyond the specific pilot or compliance need.

## 8. Unresolved Information

*Note: The following items represent unresolved or tentative information and are not mandatory implementation targets.*

### [UN-001]
The exact conditions and fallback rules for office and remote web access are not yet pinned down and depend on the security policy for each project.

### [UN-002]
The concurrent user level is still a tentative assumption and has not been validated beyond 'a few dozen' users.
