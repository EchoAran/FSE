# PURE Requirements Interview Cases

This repository contains project-level starting contexts for automated requirements interviews. The cases were derived from public requirements documents in PURE through source-grounded abstraction. Each case establishes enough project and business context to begin an interview while deliberately leaving detailed functions, rules, exceptions, quality requirements, and implementation decisions open for subsequent exploration.

The completed dataset contains 69 independently reviewed and accepted cases. All 79 PURE documents were screened: 71 source documents contributed to cases, seven were excluded, and one lower-level duplicate was recorded.

## Dataset Design

The dataset is intended for project-level requirements interviewing rather than classification or matching of individual requirement statements. Every runtime case has the following form:

```json
{
  "case_id": "PURE_001",
  "project_name": "...",
  "initial_requirements": "..."
}
```

The initial description normally identifies the project purpose or central business setting, principal actors when available, and a small number of core capabilities. It is not a summary of the complete source specification.

## Planned Construction Method

The construction plan consisted of four stages:

1. **Document screening.** Read every PURE document and retain it when an identifiable software system or software-supported setting, understandable project context, sufficient requirements material, and meaningful interview potential were present. Documents dominated by APIs, protocols, hardware parameters, low-level configuration, or implementation instructions were not suitable.
2. **Initial requirements construction.** Read each retained source in full and create one concise English paragraph through source-grounded abstraction. Preserve supported project goals, business context, actors, and selected high-level capabilities. Omit most detailed workflows, exceptions, algorithms, interface parameters, technology versions, and implementation constraints.
3. **Provenance recording.** Record the source document, project-name basis, domain, supporting sections, pages, and a concise evidence note for every case. Multiple related passages could support one abstraction, and complementary documents describing one project could be combined.
4. **Independent review and finalization.** Review every candidate against groundedness, context sufficiency, exploration openness, and detail appropriateness. The available decisions were `Accept`, `Minor Revision`, and `Reject`. Minor revisions required reconstruction and confirmation; unsuitable source documents were removed from the case collection.

## Actual Construction Outcome

| Outcome | Documents | Result |
|---|---:|---|
| Included source documents | 71 | Contributed to 69 accepted cases |
| Excluded source documents | 7 | Failed the project-level screening criteria |
| Duplicate source documents | 1 | Represented by a retained higher-level source |
| Total screened | 79 | No pending screening records |
| Accepted cases | 69 | No pending review records |

### Multi-Document Cases

Two cases combine complementary documents describing one project:

| Case | Source documents | Rationale |
|---|---|---|
| `PURE_043` — EVLA Correlator Operations System | `2002 - evla back.pdf`; `2002 - evla corr.pdf` | The backend-processing and correlator-monitoring specifications describe complementary parts of the same EVLA operational system. |
| `PURE_058` — EIRENE Railway Mobile Communications System | `2006 - eirene sys 15.pdf`; `2007 - eirene fun 7.pdf` | The system-level and functional specifications jointly describe one interoperable railway radio system. |

### Duplicate Handling

`2005 - clarus low.pdf` was recorded as a lower-level duplicate of the Clarus project. The project is represented by the higher-level requirements document used for `PURE_017`, avoiding two cases for the same system.

### Excluded Documents

| PURE document | Exclusion code | Reason |
|---|---|---|
| `2002 - sce api.pdf` | `PRIMARILY_API_OR_PROTOCOL` | Specifies a standardized co-emulation interface rather than an interview-ready project context. |
| `2004 - e-procurement.rtf` | `PRIMARILY_INTEROPERABILITY_MESSAGE_SPECIFICATION` | Defines procurement-message information content and structure rather than an identifiable software system. |
| `2004 - watcom gui.pdf` | `PRIMARILY_LOW_LEVEL_TECHNICAL_SPECIFICATION` | Is dominated by implementation-level GUI library porting guidance. |
| `2004 - watcom.pdf` | `PRIMARILY_LOW_LEVEL_TECHNICAL_SPECIFICATION` | Specifies compiler and linker porting work at an implementation level. |
| `2008 - caiso.pdf` | `NON_SOFTWARE_OPERATIONAL_PLAN` | Is an electric-grid restoration, testing, recordkeeping, and training plan rather than software requirements. |
| `2010 - blit draft.pdf` | `INSUFFICIENT_PROJECT_SPECIFIC_CONTENT` | Retains company and system placeholders and lacks sufficient project-specific business context. |
| `2011 - opensg 0.1.doc` | `INCOMPLETE_REFERENCE_ARCHITECTURE_DRAFT` | Contains mainly an architecture outline, headings, and unresolved notes without substantive project requirements. |

## Repository Contents

- `cases.jsonl`: Final runtime inputs for requirements interview systems.
- `construction_records/metadata.jsonl`: Case-level source and evidence-location records.
- `construction_records/review_records.jsonl`: Completed independent review decisions and feedback.
- `construction_records/screening_records.jsonl`: Screening evidence and decisions for all 79 documents.
- `construction_records/document_inventory.jsonl`: Inventory and processing status for every PURE source document.
- `source/requirements/req/`: The 79 original PURE documents used for screening and traceability.

No construction scripts, extracted-text caches, generated digests, or page-rendering QA images are retained in the completed dataset.

## Review Records

Each accepted case has a completed record covering:

- `groundedness`
- `context_sufficiency`
- `exploration_openness`
- `detail_appropriateness`
- final decision and reviewer feedback

Detailed provenance and review information are kept outside the runtime case input so interview systems receive only the project name and initial requirements.

## Source

PURE is available from Zenodo at <https://zenodo.org/records/7118517> under DOI `10.5281/zenodo.7118517`.
