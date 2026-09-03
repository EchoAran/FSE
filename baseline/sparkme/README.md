# SparkMe: Multi-Agent Software Requirements Engineering Interviewer

An agentic software requirements elicitation system adapted from the SparkMe multi-agent architecture.

---

## Overview

SparkMe operates as an asynchronous, multi-agent conversational requirements elicitation framework comprising three specialized collaborating agents:

1. **Interviewer Agent**: Engages with human stakeholders to ask structured, context-aware requirement questions probing system goals, functional behaviors, business rules, and constraints.
2. **Agenda Manager Agent**: Observes the ongoing interview in real-time, extracts requirement facts into a vector memory bank, maps findings to active subtopics in the requirements agenda, and tracks coverage.
3. **Exploration Planner Agent**: Operates periodically across interaction turns to perform simulated dialogue rollouts, identify novel emergent requirement insights, evaluate multi-turn utility ($U = \alpha \cdot \Delta\text{Coverage} - \beta \cdot \text{Cost} + \gamma \cdot \Delta\text{Emergence}$), and generate high-priority strategic questions.

---

## Repository Structure

```
sparkme/
├── data/
│   └── configs/
│       └── topics.json                # 9-dimensional Software Requirements Topic Guide
├── examples/
│   ├── run_sample_interview.py        # CLI execution runner
│   └── sample_cases/
│       └── clinic_management.yaml     # Sample software requirements case
├── src/
│   ├── agents/
│   │   ├── interviewer/               # Interviewer agent implementation & prompts
│   │   ├── agenda_manager/            # Agenda manager agent & tools
│   │   └── exploration_planner/       # Exploration planner agent & rollouts
│   ├── content/
│   │   ├── session_agenda/            # Topic manager, evaluators & agenda models
│   │   ├── memory_bank/               # Vector memory bank & persistence
│   │   ├── question_bank/             # Question bank vector database
│   │   └── embeddings/                # Configurable embedding backends
│   ├── interview_session/             # Multi-agent session orchestrator & user participant
│   ├── utils/                         # LLM engine dispatchers, token tracker & XML formatters
│   ├── interviewer.py                 # SparkMeInterviewer high-level facade adapter
│   ├── models.py                      # RequirementCase, DialogueTurn, InterviewTranscript
│   ├── transcript.py                  # Public transcript export & persistence
│   └── main.py                        # Interactive CLI entry point
├── .env_sample                        # Environment configuration sample
├── requirements.txt                   # Converged dependencies
└── README.md                          # System documentation
```

---

## Software Requirements Topic Guide

The requirements agenda in `data/configs/topics.json` covers 9 core dimensions:
1. **Project Goals & Success Criteria**: High-level business objectives, measurable KPIs, and scope boundaries.
2. **Stakeholders, Roles & Access Permissions**: Target user personas, permissions, and cross-team responsibilities.
3. **Current Business Workflows & Operational Pain Points**: As-is processes, manual bottlenecks, and operational workarounds.
4. **Functional Requirements & System Behaviors**: Transaction workflows, automated processing, and edge cases.
5. **Data Entities, Interfaces & External Integrations**: Domain data models, external APIs, and sync protocols.
6. **Business Rules, Validation Logic & Exceptions**: Policy enforcement, input validation, and error recovery.
7. **Quality Attributes & Non-Functional Requirements**: Throughput, privacy/security, uptime, and accessibility.
8. **Technical Constraints, Dependencies & Risks**: Deployment environments, vendor limits, and delivery risks.
9. **Acceptance Criteria & Unresolved Issues**: Acceptance criteria, sign-off milestones, and open architectural choices.

---

## Upstream Bug Fixes & Improvements

1. **Duplicate Subtopic Check Fix**: Resolved a tuple unpacking mismatch in `InterviewTopicManager._check_duplicate_subtopic` so it consistently returns a `(bool, float)` 2-tuple on all execution paths.
2. **Recursive Nested XML Parser**: Enhanced `parse_tool_calls` in `xml_formatter.py` to parse nested XML structures into lists of dictionaries, preserving dotted ID strings (`subtopic_id: "5.3"`) without lossy float conversion.
3. **Conversational Turn Completion**: Handled direct conversational responses in `Interviewer.on_message` to complete turns cleanly without timing out on maximum consideration iterations.

---

## Usage

### Programmatic API

```python
from src.interviewer import SparkMeInterviewer
from src.models import RequirementCase
from src.transcript import TranscriptExporter

# 1. Define requirement case
case = RequirementCase(
    case_id="CASE-001",
    project_name="Clinic Management Platform",
    initial_requirements="Cloud-based clinic system with offline EMR caching.",
)

# 2. Initialize interviewer
interviewer = SparkMeInterviewer(max_turns=10)
interviewer.initialize(case)

# 3. Step through dialogue
first_q = interviewer.get_first_question()
print(f"Interviewer: {first_q}")

next_q = interviewer.step("We require offline EMR caching for rural healthcare facilities.")
print(f"Interviewer: {next_q}")

# 4. Export clean transcript
transcript = interviewer.export_transcript()
TranscriptExporter.save_transcript(transcript, "output/transcript.json")
```

### CLI Demo

```bash
python examples/run_sample_interview.py --max-turns 3 --output output/sample_transcript.json
```
