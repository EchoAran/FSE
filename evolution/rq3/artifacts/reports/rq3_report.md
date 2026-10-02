# RQ3 Evaluation Report

## Environment

- Artifacts root: `evolution/rq3/artifacts`
- Source results root: `results`
- Case file: `evolution/rq3/cases.jsonl`
- Methods: hashimoto, llmrei-long, sparkme, proposed_method
- Runs per SRS: 5
- Artifact processor model: gpt-5.4-mini-2026-03-17
- Coding model: openai/gpt-5.4-mini-2026-03-17
- Evaluator model: gpt-6-sol
- Container image: rq3-coding
- Container network: none

Evidence paths in the tables below are relative to the artifacts root.

## Input coverage

| case_id | method_id | source_status | completed_turns | prepare_status | reason |
| --- | --- | --- | --- | --- | --- |
| PURE_002 | hashimoto | method_finished | 11 | ready | Transcript validated successfully |
| PURE_002 | llmrei-long | method_finished | 16 | ready | Transcript validated successfully |
| PURE_002 | sparkme | method_finished | 51 | ready | Transcript validated successfully |
| PURE_002 | proposed_method | method_finished | 47 | ready | Transcript validated successfully |
| PURE_004 | hashimoto | method_finished | 3 | ready | Transcript validated successfully |
| PURE_004 | llmrei-long | method_finished | 21 | ready | Transcript validated successfully |
| PURE_004 | sparkme | method_finished | 36 | ready | Transcript validated successfully |
| PURE_004 | proposed_method | method_finished | 27 | ready | Transcript validated successfully |
| PURE_024 | hashimoto | method_finished | 1 | ready | Transcript validated successfully |
| PURE_024 | llmrei-long | method_finished | 19 | ready | Transcript validated successfully |
| PURE_024 | sparkme | method_finished | 38 | ready | Transcript validated successfully |
| PURE_024 | proposed_method | method_finished | 46 | ready | Transcript validated successfully |
| PURE_057 | hashimoto | method_finished | 7 | ready | Transcript validated successfully |
| PURE_057 | llmrei-long | method_finished | 11 | ready | Transcript validated successfully |
| PURE_057 | sparkme | method_finished | 43 | ready | Transcript validated successfully |
| PURE_057 | proposed_method | method_finished | 50 | ready | Transcript validated successfully |
| PURE_069 | hashimoto | method_finished | 4 | ready | Transcript validated successfully |
| PURE_069 | llmrei-long | method_finished | 6 | ready | Transcript validated successfully |
| PURE_069 | sparkme | method_finished | 38 | ready | Transcript validated successfully |
| PURE_069 | proposed_method | method_finished | 58 | ready | Transcript validated successfully |

## SRS inventory

| case_id | method_id | project_name | srs_status | item_count | requirement_ids | scenario_count | pending_scenario_fields | unresolved_reviews |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PURE_002 | hashimoto | GAMMA-J Web Store | reviewed | 59 | SC-001; FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; QR-001; BR-012; UN-001; BR-013; BR-014; UN-002; BR-015; FR-008; FR-009; UN-003; UN-004; BR-016; BR-017; BR-018; BR-019; BR-020; UN-005; FR-010; BR-021; BR-022; BR-023; BR-024; BR-025; FR-011; UN-006; BR-026; FR-012; FR-013; FR-014; BR-027; BR-028; BR-029; FR-015; BR-030; BR-031; FR-016; FR-017; BR-032; BR-033; BR-034 | 59 |  | 0 |
| PURE_002 | llmrei-long | GAMMA-J Web Store | reviewed | 31 | SC-001; ACT-001; ACT-002; ACT-003; FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; BR-001; BR-002; BR-003; BR-004; BR-005; UN-001 | 31 |  | 0 |
| PURE_002 | sparkme | GAMMA-J Web Store | reviewed | 114 | SC-001; SC-002; SA-001; SA-002; SA-003; FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062; FR-063; FR-064; FR-065; FR-066; FR-067; FR-068; FR-069; FR-070; FR-071; BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; DI-001; DI-002; DI-003; DI-004; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; QR-007; QR-008; QR-009; QR-010; QR-011; QR-012; QR-013; EX-001; EX-002; EX-003; EX-004; EX-005; UN-001; UN-002; UN-003; UN-004 | 114 |  | 0 |
| PURE_002 | proposed_method | GAMMA-J Web Store | reviewed | 148 | SC-001; SC-002; ACT-001; ACT-002; ACT-003; ACT-004; FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062; FR-063; FR-064; FR-065; FR-066; FR-067; FR-068; FR-069; FR-070; FR-071; FR-072; FR-073; FR-074; FR-075; FR-076; FR-077; FR-078; FR-079; FR-080; FR-081; FR-082; FR-083; FR-084; FR-085; FR-086; FR-087; FR-088; FR-089; BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; BR-013; BR-014; BR-015; BR-016; BR-017; BR-018; BR-019; BR-020; DI-001; DI-002; DI-003; DI-004; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; QR-007; QR-008; QR-009; QR-010; QR-011; QR-012; QR-013; QR-014; QR-015; QR-016; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006; UN-001; UN-002; UN-003; UN-004; UN-005; UN-006; UN-007 | 148 |  | 0 |
| PURE_004 | hashimoto | Qheadache | reviewed | 26 | SC-001; SC-002; SC-003; FR-001; FR-002; FR-003; FR-005; FR-007; FR-009; FR-010; FR-011; SC-004; ST-001; ST-002; ST-003; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; UN-001 | 26 |  | 0 |
| PURE_004 | llmrei-long | Qheadache | reviewed | 44 | SC-001; SC-002; FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; BR-001; BR-002; BR-003; BR-004; BR-005; DI-001; DI-002; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; EX-001; EX-002; UN-001; UN-002 | 44 |  | 0 |
| PURE_004 | sparkme | Qheadache | reviewed | 100 | SC-001; SC-002; SC-003; SC-004; ST-001; ST-002; ST-003; FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; BR-013; BR-014; BR-015; BR-016; BR-017; BR-018; BR-019; DI-001; DI-002; DI-003; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; QR-007; QR-008; QR-009; QR-010; QR-011; QR-012; QR-013; QR-014; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006; EX-007; UN-001; UN-002; UN-003; UN-004; UN-005 | 100 |  | 0 |
| PURE_004 | proposed_method | Qheadache | reviewed | 54 | SC-001; SC-002; FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; QR-007; QR-008; QR-009; QR-010; EX-001; EX-002; EX-003; EX-004; UN-001; UN-002; UN-003; UN-004; UN-005; UN-006 | 54 |  | 0 |
| PURE_024 | hashimoto | Nenios Child Care Management | reviewed | 19 | SC-001; SC-002; SC-003; ST-001; ST-002; ST-003; ST-004; UN-001; FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; BR-001 | 19 |  | 0 |
| PURE_024 | llmrei-long | Nenios Child Care Management | reviewed | 40 | SC-001; SC-002; ST-001; FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; BR-001; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; QR-001; QR-002; QR-003; QR-004; BR-002; BR-003; BR-004; BR-005; BR-006; FR-023; UN-001; UN-002; UN-003; UN-004 | 40 |  | 0 |
| PURE_024 | sparkme | Nenios Child Care Management | reviewed | 135 | SC-001; ST-001; ST-002; FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062; FR-063; FR-064; FR-065; FR-066; FR-067; FR-068; FR-069; FR-070; FR-071; FR-072; FR-073; FR-074; FR-075; FR-076; FR-077; FR-078; FR-079; FR-080; FR-081; FR-082; FR-083; FR-084; FR-085; FR-086; FR-087; FR-088; BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; DI-001; DI-002; DI-003; DI-004; DI-005; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; QR-007; QR-008; QR-009; QR-010; QR-011; QR-012; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006; UN-001; UN-002; UN-003; UN-004; UN-005; UN-006; UN-007; UN-008; UN-009; UN-010; UN-011 | 135 |  | 0 |
| PURE_024 | proposed_method | Nenios Child Care Management | reviewed | 106 | SC-001; SC-002; ACT-001; ACT-002; FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062; BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; BR-013; BR-014; DI-001; DI-002; DI-003; DI-004; DI-005; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; QR-007; QR-008; QR-009; QR-010; QR-011; QR-012; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006; UN-001; UN-002; UN-003 | 106 |  | 0 |
| PURE_057 | hashimoto | Security and Privacy Requirements Analysis Tool | reviewed | 42 | SC-001; ST-001; FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; QR-001; FR-007; FR-008; EX-001; EX-002; EX-003; FR-009; FR-010; FR-011; FR-012; UN-001; FR-013; FR-014; FR-015; UN-002; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; DI-001; DI-002; DI-003; FR-030; FR-031 | 42 |  | 0 |
| PURE_057 | llmrei-long | Security and Privacy Requirements Analysis Tool | reviewed | 24 | SC-001; ACT-001; FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; BR-001; QR-001; QR-002; UN-001 | 24 |  | 0 |
| PURE_057 | sparkme | Security and Privacy Requirements Analysis Tool | reviewed | 133 | SC-001; SC-002; SC-003; SA-001; SA-002; SA-003; SA-004; SA-005; FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062; FR-063; FR-064; FR-065; FR-066; FR-067; FR-068; FR-069; FR-070; FR-071; FR-072; FR-073; FR-074; FR-075; FR-076; FR-077; FR-078; FR-079; FR-080; FR-081; FR-082; FR-083; FR-084; BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; DI-001; DI-002; DI-003; DI-004; DI-005; DI-006; DI-007; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; QR-007; QR-008; QR-009; QR-010; QR-011; QR-012; QR-013; QR-014; QR-015; QR-016; QR-017; QR-018; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006; UN-001; UN-002; UN-003; UN-004; UN-005; UN-006 | 133 |  | 0 |
| PURE_057 | proposed_method | Security and Privacy Requirements Analysis Tool | reviewed | 108 | SC-001; SC-002; AK-001; FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062; FR-063; BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; BR-013; BR-014; BR-015; BR-016; BR-017; BR-018; BR-019; BR-020; BR-021; BR-022; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; QR-007; QR-008; QR-009; QR-010; QR-011; QR-012; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006; UN-001; UN-002 | 108 |  | 0 |
| PURE_069 | hashimoto | PDF Split and Merge | reviewed | 29 | SC-001; FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; BR-001; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; SA-001; SA-002; UN-001 | 29 |  | 0 |
| PURE_069 | llmrei-long | PDF Split and Merge | reviewed | 13 | SC-001; SC-002; SC-003; ST-001; FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009 | 13 |  | 0 |
| PURE_069 | sparkme | PDF Split and Merge | reviewed | 82 | SC-001; FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; BR-013; BR-014; DI-001; DI-002; DI-003; DI-004; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; QR-007; QR-008; QR-009; QR-010; QR-011; QR-012; QR-013; QR-014; QR-015; QR-016; QR-017; EX-001; EX-002; EX-003; UN-001; UN-002; UN-003; UN-004; UN-005; UN-006; UN-007 | 82 |  | 0 |
| PURE_069 | proposed_method | PDF Split and Merge | reviewed | 145 | SC-001; FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062; FR-063; FR-064; FR-065; FR-066; FR-067; FR-068; FR-069; FR-070; FR-071; FR-072; FR-073; FR-074; FR-075; FR-076; FR-077; FR-078; FR-079; FR-080; FR-081; FR-082; FR-083; FR-084; FR-085; FR-086; FR-087; FR-088; FR-089; FR-090; FR-091; FR-092; FR-093; FR-094; FR-095; FR-096; FR-097; FR-098; FR-099; BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; DI-001; DI-002; DI-003; DI-004; DI-005; DI-006; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; QR-007; QR-008; QR-009; QR-010; QR-011; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006; EX-007; EX-008; EX-009; EX-010; UN-001; UN-002; UN-003; UN-004; UN-005; UN-006 | 145 |  | 0 |

## Run coverage

| case_id | method_id | run_index | coding_status | build | run | evidence_count | judgment_count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PURE_002 | hashimoto | 1 | completed |  |  | 0 | 0 |
| PURE_002 | hashimoto | 2 | completed |  |  | 0 | 0 |
| PURE_002 | hashimoto | 3 | completed |  |  | 0 | 0 |
| PURE_002 | hashimoto | 4 | completed |  |  | 0 | 0 |
| PURE_002 | hashimoto | 5 | completed |  |  | 0 | 0 |
| PURE_002 | llmrei-long | 1 | completed |  |  | 0 | 0 |
| PURE_002 | llmrei-long | 2 | completed |  |  | 0 | 0 |
| PURE_002 | llmrei-long | 3 | completed |  |  | 0 | 0 |
| PURE_002 | llmrei-long | 4 | completed |  |  | 0 | 0 |
| PURE_002 | llmrei-long | 5 | completed |  |  | 0 | 0 |
| PURE_002 | sparkme | 1 | completed |  |  | 0 | 0 |
| PURE_002 | sparkme | 2 | completed |  |  | 0 | 0 |
| PURE_002 | sparkme | 3 | completed |  |  | 0 | 0 |
| PURE_002 | sparkme | 4 | completed |  |  | 0 | 0 |
| PURE_002 | sparkme | 5 | completed |  |  | 0 | 0 |
| PURE_002 | proposed_method | 1 | completed |  |  | 0 | 0 |
| PURE_002 | proposed_method | 2 | completed |  |  | 0 | 0 |
| PURE_002 | proposed_method | 3 | completed |  |  | 0 | 0 |
| PURE_002 | proposed_method | 4 | completed |  |  | 0 | 0 |
| PURE_002 | proposed_method | 5 | completed |  |  | 0 | 0 |
| PURE_004 | hashimoto | 1 | completed |  |  | 0 | 0 |
| PURE_004 | hashimoto | 2 | completed |  |  | 0 | 0 |
| PURE_004 | hashimoto | 3 | completed |  |  | 0 | 0 |
| PURE_004 | hashimoto | 4 | completed |  |  | 0 | 0 |
| PURE_004 | hashimoto | 5 | completed |  |  | 0 | 0 |
| PURE_004 | llmrei-long | 1 | completed |  |  | 0 | 0 |
| PURE_004 | llmrei-long | 2 | completed |  |  | 0 | 0 |
| PURE_004 | llmrei-long | 3 | completed |  |  | 0 | 0 |
| PURE_004 | llmrei-long | 4 | completed |  |  | 0 | 0 |
| PURE_004 | llmrei-long | 5 | completed |  |  | 0 | 0 |
| PURE_004 | sparkme | 1 | completed |  |  | 0 | 0 |
| PURE_004 | sparkme | 2 | completed |  |  | 0 | 0 |
| PURE_004 | sparkme | 3 | completed |  |  | 0 | 0 |
| PURE_004 | sparkme | 4 | completed |  |  | 0 | 0 |
| PURE_004 | sparkme | 5 | completed |  |  | 0 | 0 |
| PURE_004 | proposed_method | 1 | completed |  |  | 0 | 0 |
| PURE_004 | proposed_method | 2 | completed |  |  | 0 | 0 |
| PURE_004 | proposed_method | 3 | completed |  |  | 0 | 0 |
| PURE_004 | proposed_method | 4 | completed |  |  | 0 | 0 |
| PURE_004 | proposed_method | 5 | completed |  |  | 0 | 0 |
| PURE_024 | hashimoto | 1 | completed |  |  | 0 | 0 |
| PURE_024 | hashimoto | 2 | completed |  |  | 0 | 0 |
| PURE_024 | hashimoto | 3 | completed |  |  | 0 | 0 |
| PURE_024 | hashimoto | 4 | completed |  |  | 0 | 0 |
| PURE_024 | hashimoto | 5 | completed |  |  | 0 | 0 |
| PURE_024 | llmrei-long | 1 | completed |  |  | 0 | 0 |
| PURE_024 | llmrei-long | 2 | completed |  |  | 0 | 0 |
| PURE_024 | llmrei-long | 3 | completed |  |  | 0 | 0 |
| PURE_024 | llmrei-long | 4 | completed |  |  | 0 | 0 |
| PURE_024 | llmrei-long | 5 | completed |  |  | 0 | 0 |
| PURE_024 | sparkme | 1 | completed |  |  | 0 | 0 |
| PURE_024 | sparkme | 2 | completed |  |  | 0 | 0 |
| PURE_024 | sparkme | 3 | completed |  |  | 0 | 0 |
| PURE_024 | sparkme | 4 | completed |  |  | 0 | 0 |
| PURE_024 | sparkme | 5 | completed |  |  | 0 | 0 |
| PURE_024 | proposed_method | 1 | completed |  |  | 0 | 0 |
| PURE_024 | proposed_method | 2 | completed |  |  | 0 | 0 |
| PURE_024 | proposed_method | 3 | completed |  |  | 0 | 0 |
| PURE_024 | proposed_method | 4 | completed |  |  | 0 | 0 |
| PURE_024 | proposed_method | 5 | completed |  |  | 0 | 0 |
| PURE_057 | hashimoto | 1 | completed |  |  | 0 | 0 |
| PURE_057 | hashimoto | 2 | completed |  |  | 0 | 0 |
| PURE_057 | hashimoto | 3 | completed |  |  | 0 | 0 |
| PURE_057 | hashimoto | 4 | completed |  |  | 0 | 0 |
| PURE_057 | hashimoto | 5 | completed |  |  | 0 | 0 |
| PURE_057 | llmrei-long | 1 | completed |  |  | 0 | 0 |
| PURE_057 | llmrei-long | 2 | completed |  |  | 0 | 0 |
| PURE_057 | llmrei-long | 3 | completed |  |  | 0 | 0 |
| PURE_057 | llmrei-long | 4 | completed |  |  | 0 | 0 |
| PURE_057 | llmrei-long | 5 | completed |  |  | 0 | 0 |
| PURE_057 | sparkme | 1 | completed |  |  | 0 | 0 |
| PURE_057 | sparkme | 2 | completed |  |  | 0 | 0 |
| PURE_057 | sparkme | 3 | completed |  |  | 0 | 0 |
| PURE_057 | sparkme | 4 | completed |  |  | 0 | 0 |
| PURE_057 | sparkme | 5 | completed |  |  | 0 | 0 |
| PURE_057 | proposed_method | 1 | completed |  |  | 0 | 0 |
| PURE_057 | proposed_method | 2 | completed |  |  | 0 | 0 |
| PURE_057 | proposed_method | 3 | completed |  |  | 0 | 0 |
| PURE_057 | proposed_method | 4 | completed |  |  | 0 | 0 |
| PURE_057 | proposed_method | 5 | completed |  |  | 0 | 0 |
| PURE_069 | hashimoto | 1 | completed |  |  | 0 | 0 |
| PURE_069 | hashimoto | 2 | completed |  |  | 0 | 0 |
| PURE_069 | hashimoto | 3 | completed |  |  | 0 | 0 |
| PURE_069 | hashimoto | 4 | completed |  |  | 0 | 0 |
| PURE_069 | hashimoto | 5 | completed |  |  | 0 | 0 |
| PURE_069 | llmrei-long | 1 | completed |  |  | 0 | 0 |
| PURE_069 | llmrei-long | 2 | completed |  |  | 0 | 0 |
| PURE_069 | llmrei-long | 3 | completed |  |  | 0 | 0 |
| PURE_069 | llmrei-long | 4 | completed |  |  | 0 | 0 |
| PURE_069 | llmrei-long | 5 | completed |  |  | 0 | 0 |
| PURE_069 | sparkme | 1 | completed |  |  | 0 | 0 |
| PURE_069 | sparkme | 2 | completed |  |  | 0 | 0 |
| PURE_069 | sparkme | 3 | completed |  |  | 0 | 0 |
| PURE_069 | sparkme | 4 | completed |  |  | 0 | 0 |
| PURE_069 | sparkme | 5 | completed |  |  | 0 | 0 |
| PURE_069 | proposed_method | 1 | completed |  |  | 0 | 0 |
| PURE_069 | proposed_method | 2 | completed |  |  | 0 | 0 |
| PURE_069 | proposed_method | 3 | completed |  |  | 0 | 0 |
| PURE_069 | proposed_method | 4 | completed |  |  | 0 | 0 |
| PURE_069 | proposed_method | 5 | completed |  |  | 0 | 0 |

## Four-direction comparison

An unanswered dimension is reported as `pending`; a symbol of `?` means that no
conclusion was recorded and is not an observed failure.

| case_id | method_id | dimension | symbol | consistency_status | run_indices | requirement_ids | evidence_ids | rationale | limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PURE_002 | hashimoto | build_run | ? | pending |  |  |  |  |  |
| PURE_002 | hashimoto | core_requirement | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017 |  |  |  |
| PURE_002 | hashimoto | boundary_constraint | ? | pending |  | BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; BR-013; BR-014; BR-015; BR-016; BR-017; BR-018; BR-019; BR-020; BR-021; BR-022; BR-023; BR-024; BR-025; BR-026; BR-027; BR-028; BR-029; BR-030; BR-031; BR-032; BR-033; BR-034 |  |  |  |
| PURE_002 | hashimoto | observable_behavior | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; QR-001; BR-012; BR-013; BR-014; BR-015; FR-008; FR-009; BR-016; BR-017; BR-018; BR-019; BR-020; FR-010; BR-021; BR-022; BR-023; BR-024; BR-025; FR-011; BR-026; FR-012; FR-013; FR-014; BR-027; BR-028; BR-029; FR-015; BR-030; BR-031; FR-016; FR-017; BR-032; BR-033; BR-034 |  |  |  |
| PURE_002 | llmrei-long | build_run | ? | pending |  |  |  |  |  |
| PURE_002 | llmrei-long | core_requirement | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021 |  |  |  |
| PURE_002 | llmrei-long | boundary_constraint | ? | pending |  | BR-001; BR-002; BR-003; BR-004; BR-005 |  |  |  |
| PURE_002 | llmrei-long | observable_behavior | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; BR-001; BR-002; BR-003; BR-004; BR-005 |  |  |  |
| PURE_002 | sparkme | build_run | ? | pending |  |  |  |  |  |
| PURE_002 | sparkme | core_requirement | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062; FR-063; FR-064; FR-065; FR-066; FR-067; FR-068; FR-069; FR-070; FR-071 |  |  |  |
| PURE_002 | sparkme | boundary_constraint | ? | pending |  | BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; EX-001; EX-002; EX-003; EX-004; EX-005 |  |  |  |
| PURE_002 | sparkme | observable_behavior | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062; FR-063; FR-064; FR-065; FR-066; FR-067; FR-068; FR-069; FR-070; FR-071; BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; DI-001; DI-002; DI-003; DI-004; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; QR-007; QR-008; QR-009; QR-010; QR-011; QR-012; QR-013; EX-001; EX-002; EX-003; EX-004; EX-005 |  |  |  |
| PURE_002 | proposed_method | build_run | ? | pending |  |  |  |  |  |
| PURE_002 | proposed_method | core_requirement | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062; FR-063; FR-064; FR-065; FR-066; FR-067; FR-068; FR-069; FR-070; FR-071; FR-072; FR-073; FR-074; FR-075; FR-076; FR-077; FR-078; FR-079; FR-080; FR-081; FR-082; FR-083; FR-084; FR-085; FR-086; FR-087; FR-088; FR-089 |  |  |  |
| PURE_002 | proposed_method | boundary_constraint | ? | pending |  | BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; BR-013; BR-014; BR-015; BR-016; BR-017; BR-018; BR-019; BR-020; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006 |  |  |  |
| PURE_002 | proposed_method | observable_behavior | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062; FR-063; FR-064; FR-065; FR-066; FR-067; FR-068; FR-069; FR-070; FR-071; FR-072; FR-073; FR-074; FR-075; FR-076; FR-077; FR-078; FR-079; FR-080; FR-081; FR-082; FR-083; FR-084; FR-085; FR-086; FR-087; FR-088; FR-089; BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; BR-013; BR-014; BR-015; BR-016; BR-017; BR-018; BR-019; BR-020; DI-001; DI-002; DI-003; DI-004; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; QR-007; QR-008; QR-009; QR-010; QR-011; QR-012; QR-013; QR-014; QR-015; QR-016; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006 |  |  |  |
| PURE_004 | hashimoto | build_run | ? | pending |  |  |  |  |  |
| PURE_004 | hashimoto | core_requirement | ? | pending |  | FR-001; FR-002; FR-003; FR-005; FR-007; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020 |  |  |  |
| PURE_004 | hashimoto | boundary_constraint | ? | pending |  | FR-021 |  |  |  |
| PURE_004 | hashimoto | observable_behavior | ? | pending |  | FR-001; FR-002; FR-003; FR-005; FR-007; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021 |  |  |  |
| PURE_004 | llmrei-long | build_run | ? | pending |  |  |  |  |  |
| PURE_004 | llmrei-long | core_requirement | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025 |  |  |  |
| PURE_004 | llmrei-long | boundary_constraint | ? | pending |  | BR-001; BR-002; BR-003; BR-004; BR-005; EX-001; EX-002 |  |  |  |
| PURE_004 | llmrei-long | observable_behavior | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; BR-001; BR-002; BR-003; BR-004; BR-005; DI-001; DI-002; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; EX-001; EX-002 |  |  |  |
| PURE_004 | sparkme | build_run | ? | pending |  |  |  |  |  |
| PURE_004 | sparkme | core_requirement | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-045 |  |  |  |
| PURE_004 | sparkme | boundary_constraint | ? | pending |  | BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; BR-013; BR-014; BR-015; BR-016; BR-017; BR-018; BR-019; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006; EX-007 |  |  |  |
| PURE_004 | sparkme | observable_behavior | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; BR-013; BR-014; BR-015; BR-016; BR-017; BR-018; BR-019; DI-001; DI-002; DI-003; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; QR-007; QR-008; QR-009; QR-010; QR-011; QR-012; QR-013; QR-014; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006; EX-007 |  |  |  |
| PURE_004 | proposed_method | build_run | ? | pending |  |  |  |  |  |
| PURE_004 | proposed_method | core_requirement | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-010; FR-011; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-026; FR-027; FR-028; FR-029; FR-030; FR-032 |  |  |  |
| PURE_004 | proposed_method | boundary_constraint | ? | pending |  | FR-008; FR-009; FR-012; FR-025; EX-001; EX-002; EX-003; EX-004 |  |  |  |
| PURE_004 | proposed_method | observable_behavior | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; QR-007; QR-008; QR-009; QR-010; EX-001; EX-002; EX-003; EX-004 |  |  |  |
| PURE_024 | hashimoto | build_run | ? | pending |  |  |  |  |  |
| PURE_024 | hashimoto | core_requirement | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010 |  |  |  |
| PURE_024 | hashimoto | boundary_constraint | ? | pending |  | BR-001 |  |  |  |
| PURE_024 | hashimoto | observable_behavior | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; BR-001 |  |  |  |
| PURE_024 | llmrei-long | build_run | ? | pending |  |  |  |  |  |
| PURE_024 | llmrei-long | core_requirement | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023 |  |  |  |
| PURE_024 | llmrei-long | boundary_constraint | ? | pending |  | BR-001; BR-002; BR-003; BR-004; BR-005; BR-006 |  |  |  |
| PURE_024 | llmrei-long | observable_behavior | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; BR-001; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; QR-001; QR-002; QR-003; QR-004; BR-002; BR-003; BR-004; BR-005; BR-006; FR-023 |  |  |  |
| PURE_024 | sparkme | build_run | ? | pending |  |  |  |  |  |
| PURE_024 | sparkme | core_requirement | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062; FR-063; FR-065; FR-066; FR-067; FR-068; FR-069; FR-070; FR-071; FR-072; FR-073; FR-074; FR-075; FR-076; FR-077; FR-078; FR-079; FR-080; FR-081; FR-082; FR-083; FR-084; FR-085; FR-086; FR-087; FR-088 |  |  |  |
| PURE_024 | sparkme | boundary_constraint | ? | pending |  | BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006 |  |  |  |
| PURE_024 | sparkme | observable_behavior | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062; FR-063; FR-064; FR-065; FR-066; FR-067; FR-068; FR-069; FR-070; FR-071; FR-072; FR-073; FR-074; FR-075; FR-076; FR-077; FR-078; FR-079; FR-080; FR-081; FR-082; FR-083; FR-084; FR-085; FR-086; FR-087; FR-088; BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; DI-001; DI-002; DI-003; DI-004; DI-005; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; QR-007; QR-008; QR-009; QR-010; QR-011; QR-012; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006 |  |  |  |
| PURE_024 | proposed_method | build_run | ? | pending |  |  |  |  |  |
| PURE_024 | proposed_method | core_requirement | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062 |  |  |  |
| PURE_024 | proposed_method | boundary_constraint | ? | pending |  | BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; BR-013; BR-014; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006 |  |  |  |
| PURE_024 | proposed_method | observable_behavior | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062; BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; BR-013; BR-014; DI-001; DI-002; DI-003; DI-004; DI-005; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; QR-007; QR-008; QR-009; QR-010; QR-011; QR-012; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006 |  |  |  |
| PURE_057 | hashimoto | build_run | ? | pending |  |  |  |  |  |
| PURE_057 | hashimoto | core_requirement | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031 |  |  |  |
| PURE_057 | hashimoto | boundary_constraint | ? | pending |  | EX-001; EX-002; EX-003 |  |  |  |
| PURE_057 | hashimoto | observable_behavior | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; QR-001; FR-007; FR-008; EX-001; EX-002; EX-003; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; DI-001; DI-002; DI-003; FR-030; FR-031 |  |  |  |
| PURE_057 | llmrei-long | build_run | ? | pending |  |  |  |  |  |
| PURE_057 | llmrei-long | core_requirement | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018 |  |  |  |
| PURE_057 | llmrei-long | boundary_constraint | ? | pending |  | BR-001 |  |  |  |
| PURE_057 | llmrei-long | observable_behavior | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; BR-001; QR-001; QR-002 |  |  |  |
| PURE_057 | sparkme | build_run | ? | pending |  |  |  |  |  |
| PURE_057 | sparkme | core_requirement | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062; FR-063; FR-064; FR-066; FR-068; FR-069; FR-070; FR-071; FR-072; FR-073; FR-074; FR-075; FR-076; FR-077; FR-078; FR-079; FR-080; FR-081; FR-082; FR-083; FR-084 |  |  |  |
| PURE_057 | sparkme | boundary_constraint | ? | pending |  | BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006 |  |  |  |
| PURE_057 | sparkme | observable_behavior | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062; FR-063; FR-064; FR-065; FR-066; FR-067; FR-068; FR-069; FR-070; FR-071; FR-072; FR-073; FR-074; FR-075; FR-076; FR-077; FR-078; FR-079; FR-080; FR-081; FR-082; FR-083; FR-084; BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; DI-001; DI-002; DI-003; DI-004; DI-005; DI-006; DI-007; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; QR-007; QR-008; QR-009; QR-010; QR-011; QR-012; QR-013; QR-014; QR-015; QR-016; QR-017; QR-018; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006 |  |  |  |
| PURE_057 | proposed_method | build_run | ? | pending |  |  |  |  |  |
| PURE_057 | proposed_method | core_requirement | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062; FR-063 |  |  |  |
| PURE_057 | proposed_method | boundary_constraint | ? | pending |  | BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; BR-013; BR-014; BR-015; BR-016; BR-017; BR-018; BR-019; BR-020; BR-021; BR-022; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006 |  |  |  |
| PURE_057 | proposed_method | observable_behavior | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062; FR-063; BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; BR-013; BR-014; BR-015; BR-016; BR-017; BR-018; BR-019; BR-020; BR-021; BR-022; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; QR-007; QR-008; QR-009; QR-010; QR-011; QR-012; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006 |  |  |  |
| PURE_069 | hashimoto | build_run | ? | pending |  |  |  |  |  |
| PURE_069 | hashimoto | core_requirement | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023 |  |  |  |
| PURE_069 | hashimoto | boundary_constraint | ? | pending |  | BR-001; FR-024 |  |  |  |
| PURE_069 | hashimoto | observable_behavior | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; BR-001; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024 |  |  |  |
| PURE_069 | llmrei-long | build_run | ? | pending |  |  |  |  |  |
| PURE_069 | llmrei-long | core_requirement | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009 |  |  |  |
| PURE_069 | llmrei-long | boundary_constraint | ? | pending |  |  |  |  |  |
| PURE_069 | llmrei-long | observable_behavior | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009 |  |  |  |
| PURE_069 | sparkme | build_run | ? | pending |  |  |  |  |  |
| PURE_069 | sparkme | core_requirement | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036 |  |  |  |
| PURE_069 | sparkme | boundary_constraint | ? | pending |  | BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; BR-013; BR-014; EX-001; EX-002; EX-003 |  |  |  |
| PURE_069 | sparkme | observable_behavior | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; BR-013; BR-014; DI-001; DI-002; DI-003; DI-004; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; QR-007; QR-008; QR-009; QR-010; QR-011; QR-012; QR-013; QR-014; QR-015; QR-016; QR-017; EX-001; EX-002; EX-003 |  |  |  |
| PURE_069 | proposed_method | build_run | ? | pending |  |  |  |  |  |
| PURE_069 | proposed_method | core_requirement | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062; FR-063; FR-064; FR-065; FR-066; FR-067; FR-068; FR-069; FR-070; FR-071; FR-072; FR-073; FR-074; FR-075; FR-076; FR-077; FR-078; FR-079; FR-080; FR-081; FR-082; FR-083; FR-084; FR-085; FR-086; FR-087; FR-088; FR-089; FR-090; FR-091; FR-092; FR-093; FR-094; FR-095; FR-096; FR-097; FR-098; FR-099 |  |  |  |
| PURE_069 | proposed_method | boundary_constraint | ? | pending |  | BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006; EX-007; EX-008; EX-009; EX-010 |  |  |  |
| PURE_069 | proposed_method | observable_behavior | ? | pending |  | FR-001; FR-002; FR-003; FR-004; FR-005; FR-006; FR-007; FR-008; FR-009; FR-010; FR-011; FR-012; FR-013; FR-014; FR-015; FR-016; FR-017; FR-018; FR-019; FR-020; FR-021; FR-022; FR-023; FR-024; FR-025; FR-026; FR-027; FR-028; FR-029; FR-030; FR-031; FR-032; FR-033; FR-034; FR-035; FR-036; FR-037; FR-038; FR-039; FR-040; FR-041; FR-042; FR-043; FR-044; FR-045; FR-046; FR-047; FR-048; FR-049; FR-050; FR-051; FR-052; FR-053; FR-054; FR-055; FR-056; FR-057; FR-058; FR-059; FR-060; FR-061; FR-062; FR-063; FR-064; FR-065; FR-066; FR-067; FR-068; FR-069; FR-070; FR-071; FR-072; FR-073; FR-074; FR-075; FR-076; FR-077; FR-078; FR-079; FR-080; FR-081; FR-082; FR-083; FR-084; FR-085; FR-086; FR-087; FR-088; FR-089; FR-090; FR-091; FR-092; FR-093; FR-094; FR-095; FR-096; FR-097; FR-098; FR-099; BR-001; BR-002; BR-003; BR-004; BR-005; BR-006; BR-007; BR-008; BR-009; BR-010; BR-011; BR-012; DI-001; DI-002; DI-003; DI-004; DI-005; DI-006; QR-001; QR-002; QR-003; QR-004; QR-005; QR-006; QR-007; QR-008; QR-009; QR-010; QR-011; EX-001; EX-002; EX-003; EX-004; EX-005; EX-006; EX-007; EX-008; EX-009; EX-010 |  |  |  |

## Evidence limitations

`recorded` marks an artifact that is present, `artifact_missing` marks a record whose
file is absent, and `collection_incomplete` marks a run whose build and run check did
not complete or did not succeed.

| case_id | method_id | run_index | scenario_id | evidence_id | evidence_type | relative_path | status | detail |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PURE_002 | hashimoto | 1 |  |  |  | cases/PURE_002/hashimoto/runs/run_01/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_002 | hashimoto | 2 |  |  |  | cases/PURE_002/hashimoto/runs/run_02/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_002 | hashimoto | 3 |  |  |  | cases/PURE_002/hashimoto/runs/run_03/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_002 | hashimoto | 4 |  |  |  | cases/PURE_002/hashimoto/runs/run_04/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_002 | hashimoto | 5 |  |  |  | cases/PURE_002/hashimoto/runs/run_05/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_002 | llmrei-long | 1 |  |  |  | cases/PURE_002/llmrei-long/runs/run_01/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_002 | llmrei-long | 2 |  |  |  | cases/PURE_002/llmrei-long/runs/run_02/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_002 | llmrei-long | 3 |  |  |  | cases/PURE_002/llmrei-long/runs/run_03/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_002 | llmrei-long | 4 |  |  |  | cases/PURE_002/llmrei-long/runs/run_04/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_002 | llmrei-long | 5 |  |  |  | cases/PURE_002/llmrei-long/runs/run_05/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_002 | sparkme | 1 |  |  |  | cases/PURE_002/sparkme/runs/run_01/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_002 | sparkme | 2 |  |  |  | cases/PURE_002/sparkme/runs/run_02/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_002 | sparkme | 3 |  |  |  | cases/PURE_002/sparkme/runs/run_03/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_002 | sparkme | 4 |  |  |  | cases/PURE_002/sparkme/runs/run_04/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_002 | sparkme | 5 |  |  |  | cases/PURE_002/sparkme/runs/run_05/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_002 | proposed_method | 1 |  |  |  | cases/PURE_002/proposed_method/runs/run_01/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_002 | proposed_method | 2 |  |  |  | cases/PURE_002/proposed_method/runs/run_02/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_002 | proposed_method | 3 |  |  |  | cases/PURE_002/proposed_method/runs/run_03/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_002 | proposed_method | 4 |  |  |  | cases/PURE_002/proposed_method/runs/run_04/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_002 | proposed_method | 5 |  |  |  | cases/PURE_002/proposed_method/runs/run_05/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_004 | hashimoto | 1 |  |  |  | cases/PURE_004/hashimoto/runs/run_01/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_004 | hashimoto | 2 |  |  |  | cases/PURE_004/hashimoto/runs/run_02/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_004 | hashimoto | 3 |  |  |  | cases/PURE_004/hashimoto/runs/run_03/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_004 | hashimoto | 4 |  |  |  | cases/PURE_004/hashimoto/runs/run_04/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_004 | hashimoto | 5 |  |  |  | cases/PURE_004/hashimoto/runs/run_05/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_004 | llmrei-long | 1 |  |  |  | cases/PURE_004/llmrei-long/runs/run_01/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_004 | llmrei-long | 2 |  |  |  | cases/PURE_004/llmrei-long/runs/run_02/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_004 | llmrei-long | 3 |  |  |  | cases/PURE_004/llmrei-long/runs/run_03/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_004 | llmrei-long | 4 |  |  |  | cases/PURE_004/llmrei-long/runs/run_04/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_004 | llmrei-long | 5 |  |  |  | cases/PURE_004/llmrei-long/runs/run_05/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_004 | sparkme | 1 |  |  |  | cases/PURE_004/sparkme/runs/run_01/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_004 | sparkme | 2 |  |  |  | cases/PURE_004/sparkme/runs/run_02/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_004 | sparkme | 3 |  |  |  | cases/PURE_004/sparkme/runs/run_03/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_004 | sparkme | 4 |  |  |  | cases/PURE_004/sparkme/runs/run_04/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_004 | sparkme | 5 |  |  |  | cases/PURE_004/sparkme/runs/run_05/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_004 | proposed_method | 1 |  |  |  | cases/PURE_004/proposed_method/runs/run_01/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_004 | proposed_method | 2 |  |  |  | cases/PURE_004/proposed_method/runs/run_02/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_004 | proposed_method | 3 |  |  |  | cases/PURE_004/proposed_method/runs/run_03/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_004 | proposed_method | 4 |  |  |  | cases/PURE_004/proposed_method/runs/run_04/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_004 | proposed_method | 5 |  |  |  | cases/PURE_004/proposed_method/runs/run_05/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_024 | hashimoto | 1 |  |  |  | cases/PURE_024/hashimoto/runs/run_01/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_024 | hashimoto | 2 |  |  |  | cases/PURE_024/hashimoto/runs/run_02/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_024 | hashimoto | 3 |  |  |  | cases/PURE_024/hashimoto/runs/run_03/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_024 | hashimoto | 4 |  |  |  | cases/PURE_024/hashimoto/runs/run_04/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_024 | hashimoto | 5 |  |  |  | cases/PURE_024/hashimoto/runs/run_05/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_024 | llmrei-long | 1 |  |  |  | cases/PURE_024/llmrei-long/runs/run_01/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_024 | llmrei-long | 2 |  |  |  | cases/PURE_024/llmrei-long/runs/run_02/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_024 | llmrei-long | 3 |  |  |  | cases/PURE_024/llmrei-long/runs/run_03/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_024 | llmrei-long | 4 |  |  |  | cases/PURE_024/llmrei-long/runs/run_04/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_024 | llmrei-long | 5 |  |  |  | cases/PURE_024/llmrei-long/runs/run_05/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_024 | sparkme | 1 |  |  |  | cases/PURE_024/sparkme/runs/run_01/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_024 | sparkme | 2 |  |  |  | cases/PURE_024/sparkme/runs/run_02/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_024 | sparkme | 3 |  |  |  | cases/PURE_024/sparkme/runs/run_03/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_024 | sparkme | 4 |  |  |  | cases/PURE_024/sparkme/runs/run_04/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_024 | sparkme | 5 |  |  |  | cases/PURE_024/sparkme/runs/run_05/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_024 | proposed_method | 1 |  |  |  | cases/PURE_024/proposed_method/runs/run_01/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_024 | proposed_method | 2 |  |  |  | cases/PURE_024/proposed_method/runs/run_02/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_024 | proposed_method | 3 |  |  |  | cases/PURE_024/proposed_method/runs/run_03/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_024 | proposed_method | 4 |  |  |  | cases/PURE_024/proposed_method/runs/run_04/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_024 | proposed_method | 5 |  |  |  | cases/PURE_024/proposed_method/runs/run_05/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_057 | hashimoto | 1 |  |  |  | cases/PURE_057/hashimoto/runs/run_01/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_057 | hashimoto | 2 |  |  |  | cases/PURE_057/hashimoto/runs/run_02/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_057 | hashimoto | 3 |  |  |  | cases/PURE_057/hashimoto/runs/run_03/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_057 | hashimoto | 4 |  |  |  | cases/PURE_057/hashimoto/runs/run_04/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_057 | hashimoto | 5 |  |  |  | cases/PURE_057/hashimoto/runs/run_05/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_057 | llmrei-long | 1 |  |  |  | cases/PURE_057/llmrei-long/runs/run_01/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_057 | llmrei-long | 2 |  |  |  | cases/PURE_057/llmrei-long/runs/run_02/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_057 | llmrei-long | 3 |  |  |  | cases/PURE_057/llmrei-long/runs/run_03/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_057 | llmrei-long | 4 |  |  |  | cases/PURE_057/llmrei-long/runs/run_04/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_057 | llmrei-long | 5 |  |  |  | cases/PURE_057/llmrei-long/runs/run_05/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_057 | sparkme | 1 |  |  |  | cases/PURE_057/sparkme/runs/run_01/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_057 | sparkme | 2 |  |  |  | cases/PURE_057/sparkme/runs/run_02/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_057 | sparkme | 3 |  |  |  | cases/PURE_057/sparkme/runs/run_03/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_057 | sparkme | 4 |  |  |  | cases/PURE_057/sparkme/runs/run_04/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_057 | sparkme | 5 |  |  |  | cases/PURE_057/sparkme/runs/run_05/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_057 | proposed_method | 1 |  |  |  | cases/PURE_057/proposed_method/runs/run_01/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_057 | proposed_method | 2 |  |  |  | cases/PURE_057/proposed_method/runs/run_02/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_057 | proposed_method | 3 |  |  |  | cases/PURE_057/proposed_method/runs/run_03/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_057 | proposed_method | 4 |  |  |  | cases/PURE_057/proposed_method/runs/run_04/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_057 | proposed_method | 5 |  |  |  | cases/PURE_057/proposed_method/runs/run_05/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_069 | hashimoto | 1 |  |  |  | cases/PURE_069/hashimoto/runs/run_01/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_069 | hashimoto | 2 |  |  |  | cases/PURE_069/hashimoto/runs/run_02/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_069 | hashimoto | 3 |  |  |  | cases/PURE_069/hashimoto/runs/run_03/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_069 | hashimoto | 4 |  |  |  | cases/PURE_069/hashimoto/runs/run_04/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_069 | hashimoto | 5 |  |  |  | cases/PURE_069/hashimoto/runs/run_05/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_069 | llmrei-long | 1 |  |  |  | cases/PURE_069/llmrei-long/runs/run_01/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_069 | llmrei-long | 2 |  |  |  | cases/PURE_069/llmrei-long/runs/run_02/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_069 | llmrei-long | 3 |  |  |  | cases/PURE_069/llmrei-long/runs/run_03/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_069 | llmrei-long | 4 |  |  |  | cases/PURE_069/llmrei-long/runs/run_04/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_069 | llmrei-long | 5 |  |  |  | cases/PURE_069/llmrei-long/runs/run_05/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_069 | sparkme | 1 |  |  |  | cases/PURE_069/sparkme/runs/run_01/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_069 | sparkme | 2 |  |  |  | cases/PURE_069/sparkme/runs/run_02/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_069 | sparkme | 3 |  |  |  | cases/PURE_069/sparkme/runs/run_03/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_069 | sparkme | 4 |  |  |  | cases/PURE_069/sparkme/runs/run_04/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_069 | sparkme | 5 |  |  |  | cases/PURE_069/sparkme/runs/run_05/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_069 | proposed_method | 1 |  |  |  | cases/PURE_069/proposed_method/runs/run_01/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_069 | proposed_method | 2 |  |  |  | cases/PURE_069/proposed_method/runs/run_02/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_069 | proposed_method | 3 |  |  |  | cases/PURE_069/proposed_method/runs/run_03/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_069 | proposed_method | 4 |  |  |  | cases/PURE_069/proposed_method/runs/run_04/evidence | collection_incomplete | No build and run verification was recorded for this run. |
| PURE_069 | proposed_method | 5 |  |  |  | cases/PURE_069/proposed_method/runs/run_05/evidence | collection_incomplete | No build and run verification was recorded for this run. |
