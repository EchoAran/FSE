# SparkMe: Multi-Agent Software Requirements Engineering Interviewer

An agentic software requirements elicitation system adapted from the SparkMe multi-agent architecture.

---

## Overview

SparkMe operates as an asynchronous, multi-agent conversational requirements elicitation framework comprising three specialized collaborating agents:

1. **Interviewer Agent**: Engages with human stakeholders to ask structured, context-aware requirement questions probing system goals, functional behaviors, business rules, and constraints.
2. **Agenda Manager Agent**: Observes the ongoing interview in real-time, extracts requirement facts into a vector memory bank, maps findings to active subtopics in the requirements agenda, and tracks coverage.
3. **Exploration Planner Agent**: Operates periodically across interaction turns to perform simulated dialogue rollouts, identify novel emergent requirement insights, evaluate multi-turn utility ($U = \alpha \cdot \Delta\text{Coverage} - \beta \cdot \text{Cost} + \gamma \cdot \Delta\text{Emergence}$), and generate high-priority strategic questions.

---

## Changes from the Upstream SparkMe Project

This implementation adapts the SparkMe multi-agent architecture for software requirements interviews and exposes it through a terminal/API interface.

- **Domain assets**: the workforce-oriented interview agenda was replaced with a 10-topic, 48-subtopic software requirements guide covering goals, stakeholders, workflows, functions, data, interfaces, constraints, quality, transition, priorities, validation, and risks.
- **Prompt adaptations**: the Interviewer, Agenda Manager, and Exploration Planner prompts were rewritten for project stakeholders and software requirements. They elicit requirement facts, map them to the RE agenda, evaluate subtopic coverage, discover emergent requirements, and plan strategic questions.
- **Preserved method components**: the three-agent collaboration, Agenda, Memory Bank, Question Bank, coverage evaluation, emergent-subtopic handling, rollout planning, and utility-based exploration remain part of the runtime.
- **Public interface and CLI**: `RequirementCase`, `InterviewTranscript`, `SparkMeInterviewer`, transcript export, JSON Case input, direct CLI arguments, and an optional `max_turns` safety cap were added for standalone use. The default remains uncapped so normal completion is controlled by the Agenda.
- **Delivery simplification**: the terminal/API path removes TTS coupling and development Mock/test/example surfaces, loads local model settings from `.env`, and keeps `.env.example` as the safe configuration template.
- **Lifecycle behavior**: SparkMe completes when all Agenda core topics are covered or when the optional turn cap is reached. The interactive CLI exports the public transcript when the session exits.

---

## Repository Structure

```
sparkme/
├── data/
│   └── configs/
│       └── topics.json                # 10-topic, 48-subtopic Requirements Guide
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
├── .env.example                       # Safe environment configuration template
├── requirements.txt                   # Converged dependencies
└── README.md                          # System documentation
```

---

## Software Requirements Topic Guide

The requirements agenda in `data/configs/topics.json` preserves the official SparkMe scale with 10 core topics and 48 predefined subtopics. Each subtopic is one independently coverable interview concern:
1. **Project Purpose and Context**
2. **Stakeholders and Shared Understanding**
3. **Current Work and Business Scope**
4. **Product Scope and Functional Behavior**
5. **Data and External Interfaces**
6. **Business Rules and Constraints**
7. **Product Experience and Performance**
8. **Operational Quality and Protection**
9. **Transition and Evolution**
10. **Prioritization and Validation**

---

## Upstream Bug Fixes & Improvements

1. **Duplicate Subtopic Check Fix**: Resolved a tuple unpacking mismatch in `InterviewTopicManager._check_duplicate_subtopic` so it consistently returns a `(bool, float)` 2-tuple on all execution paths.
2. **Recursive Nested XML Parser**: Enhanced `parse_tool_calls` in `xml_formatter.py` to parse nested XML structures into lists of dictionaries, preserving dotted ID strings (`subtopic_id: "5.3"`) without lossy float conversion.
3. **Conversational Turn Completion**: Handled direct conversational responses in `Interviewer.on_message` to complete turns cleanly without timing out on maximum consideration iterations.

---

## Usage

### Model Configuration

From the `baseline/sparkme` directory, create the local environment file:

```powershell
Copy-Item .env.example .env
```

On macOS/Linux, use `cp .env.example .env`. At minimum, set `OPENAI_API_KEY`, `MODEL_NAME`, and—when using an OpenAI-compatible service—`OPENAI_BASE_URL` in `.env`. `AGENDA_MANAGER_MODEL_NAME` and `EXPLORATION_PLANNER_MODEL_NAME` may select dedicated models for those agents; the remaining optional provider settings are documented in `.env.example`.

`.env.example` is safe to commit because it contains no credentials. The local `.env` is loaded automatically by both the programmatic API and CLI, is ignored by Git, and must never be committed.

### Programmatic API

```python
from src.interviewer import SparkMeInterviewer
from src.models import RequirementCase
from src.transcript import TranscriptExporter

# 1. Define requirement case
case = RequirementCase(
    case_id="CASE-001",
    project_name="Example System",
    initial_requirements="Describe the initial requirements here.",
)

# 2. Initialize interviewer
interviewer = SparkMeInterviewer()
interviewer.initialize(case)

# 3. Step through dialogue
first_q = interviewer.get_first_question()
print(f"Interviewer: {first_q}")

next_q = interviewer.step("Describe one concrete workflow or constraint here.")
print(f"Interviewer: {next_q}")

# 4. Export clean transcript
transcript = interviewer.export_transcript()
TranscriptExporter.save_transcript(transcript, "output/transcript.json")
```

### CLI Entry Point

```bash
# Using an input JSON file (matching other baselines):
python -m src.main --input project_input.json

# Or passing arguments directly:
python -m src.main --case_id CASE-001 --project_name "Example System" --initial_requirements "Describe the initial requirements here."
```
