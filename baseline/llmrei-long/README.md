# LLMREI-long: Requirements Elicitation Interview Engine

Modular implementation of the **LLMREI-long** interview approach for automated software requirements elicitation (Korn et al., IEEE RE 2025).

## Overview

LLMREI-long conducts multi-turn requirements elicitation interviews driven by a structured system prompt, contextual software project requirements, and dialogue history.

### Directory Structure

```text
llmrei-long/
├── config/
│   └── default.yaml               # Runtime configuration
├── vendor/
│   └── long_prompt.txt            # Official verbatim prompt template
├── src/
│   ├── client/
│   │   ├── base.py                # Abstract LLM client interface
│   │   └── openai_client.py       # OpenAI-compatible API client
│   ├── prompt/
│   │   ├── loader.py              # Prompt template file loader
│   │   └── renderer.py            # Context rendering for initial requirements
│   ├── config.py                  # Typed configuration model
│   ├── interviewer.py             # Core LLMREI interview session manager
│   ├── models.py                  # Domain data classes (Case, Turn, Transcript)
│   └── transcript.py              # Structured JSON transcript exporter and loader
├── tests/
│   ├── mock_client.py             # Deterministic mock client for tests
│   ├── test_prompt_rendering.py   # Unit tests for prompt loading/rendering
│   └── test_interviewer_flow.py   # Multi-turn conversational flow tests
├── examples/
│   ├── sample_cases/              # Sample YAML software requirement cases
│   └── run_sample_interview.py    # Runnable CLI interview script
└── requirements.txt
```

## Quickstart

### Installation

```bash
pip install -r requirements.txt
```

### Running Tests

```bash
pytest tests/ -v
```

### Python API Usage

```python
from src.config import InterviewConfig
from src.interviewer import LLMREIInterviewer
from src.models import RequirementCase
from src.transcript import TranscriptExporter

# 1. Define the requirement case
case = RequirementCase(
    case_id="CASE-001",
    project_name="Smart Clinic System",
    initial_requirements="A clinic queue management and electronic record system.",
)

# 2. Initialize the interviewer
config = InterviewConfig(model="gpt-4o", max_turns=15)
interviewer = LLMREIInterviewer(config=config)
interviewer.initialize(case)

# 3. Start dialogue
first_question = interviewer.get_first_question()
print(first_question)

# 4. Multi-turn step
next_question = interviewer.step("We need an online queue status display for patients.")
print(next_question)

# 5. Export transcript (Structured JSON)
transcript = interviewer.export_transcript()
TranscriptExporter.save_json(transcript, "output/clinic_transcript.json")

# 6. Lossless resume from transcript
resumed_interviewer = LLMREIInterviewer(config=config)
loaded_transcript = TranscriptExporter.load_json("output/clinic_transcript.json")
resumed_interviewer.resume_from_transcript(loaded_transcript)
```

### Running Sample Interview CLI

```bash
# Offline demonstration mode with mock client
python examples/run_sample_interview.py --mock --case examples/sample_cases/clinic_management.yaml

# Live mode with OpenAI API (requires OPENAI_API_KEY environment variable)
python examples/run_sample_interview.py --case examples/sample_cases/clinic_management.yaml
```
