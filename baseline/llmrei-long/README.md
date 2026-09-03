# LLMREI-long: Requirements Elicitation Interview Engine

Modular implementation of the **LLMREI-long** interview approach for automated software requirements elicitation (Korn et al., IEEE RE 2025).

## Overview

LLMREI-long conducts multi-turn requirements elicitation interviews driven by a structured system prompt, contextual software project requirements, and dialogue history.

## Changes from the Official LLMREI-long Assets

This implementation combines the published long prompt with a minimal multi-turn runtime for software requirements interviews.

- **Prompt termination protocol**: `vendor/long_prompt.txt` retains the published interview instructions and adds one final instruction: when the model decides the interview is complete, it must output exactly `[[INTERVIEW_FINISHED]]`. This marker is an engineering addition; it is not part of the original prompt.
- **Project context injection**: `PromptRenderer` appends `project_name` and `initial_requirements` to the system prompt so the same interviewer can run against arbitrary software projects.
- **Reusable runtime interface**: `LLMREIInterviewer`, the OpenAI-compatible client, transcript models, and the CLI scripts were added around the prompt to support initialization, one-turn execution, inspection, persistence, and unfinished-session recovery.
- **Lifecycle behavior**: an exact marker response completes the project automatically. `max_turns` remains a safety cap, empty model responses fail without committing a turn, and completed projects cannot be resumed or advanced.
- **Persistent output**: the CLI stores `state.json` and `transcript.json` after initialization and each successful turn.

### Directory Structure

```text
llmrei-long/
├── config/
│   └── default.example.yaml       # Safe model/runtime configuration template
├── vendor/
│   └── long_prompt.txt            # Official prompt with a fixed completion marker
├── src/
│   ├── client/
│   │   ├── base.py                # Abstract LLM client interface
│   │   └── openai_client.py       # OpenAI-compatible API client
│   ├── prompt/
│   │   ├── loader.py              # Prompt template file loader
│   │   └── renderer.py            # Context rendering for initial requirements
│   ├── config.py                  # Typed configuration model
│   ├── interviewer.py             # Core LLMREI interview session manager
│   ├── main.py                    # Interactive terminal entry point
│   ├── models.py                  # Domain data classes (Case, Turn, Transcript)
│   ├── project_store.py           # Persisted CLI project storage
│   └── transcript.py              # Structured JSON transcript exporter and loader
├── scripts/
│   ├── init_project.py            # Create a persisted interview project
│   ├── step.py                    # Process one stakeholder answer
│   ├── inspect_state.py           # Inspect persisted dialogue state
│   └── resume.py                  # Validate an unfinished project
└── requirements.txt
```

## Quickstart

### Installation

```bash
pip install -r requirements.txt
```

### Model Configuration

From the `baseline/llmrei-long` directory, create the local configuration file:

```powershell
Copy-Item config/default.example.yaml config/default.yaml
```

On macOS/Linux, use `cp config/default.example.yaml config/default.yaml`. Then edit these fields in `config/default.yaml`:

```yaml
api_key: "your-api-key"
base_url: null  # Keep null for OpenAI, or set an OpenAI-compatible endpoint.
model: "gpt-4o"
```

`config/default.example.yaml` is the safe template committed to the repository. The local `config/default.yaml` is ignored by Git and must never be committed because it contains credentials.

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

# 2. Load local configuration and initialize the interviewer
config = InterviewConfig.from_yaml("config/default.yaml")
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

# 6. Lossless resume from an unfinished transcript
resumed_interviewer = LLMREIInterviewer(config=config)
loaded_transcript = TranscriptExporter.load_json("output/clinic_transcript.json")
resumed_interviewer.resume_from_transcript(loaded_transcript)
```

### CLI Tool Suite (`scripts/`)

The CLI tools save the current project state and transcript under `runs/{project_id}/`:

#### 1. Initialize Project (`init_project.py`)
```bash
python scripts/init_project.py --input project_input.json
```
*Creates project under `runs/{project_id}/`, saves initial transcript snapshot, and prints the first question.*

#### 2. Advance Dialogue Turn (`step.py`)
```bash
python scripts/step.py --project-id <PROJECT_ID> --answer "We need an online queue status display for patients."
```
*Advances one dialogue turn and updates the transcript. When the model outputs `[[INTERVIEW_FINISHED]]`, the project is automatically marked as completed.*

#### 3. Inspect Project State (`inspect_state.py`)
```bash
python scripts/inspect_state.py --project-id <PROJECT_ID> [--verbose]
```
*Displays current turn count, interview status, and recent dialogue turns.*

#### 4. Validate and Resume Interrupted Session (`resume.py`)
```bash
python scripts/resume.py --project-id <PROJECT_ID>
```
*Restores an unfinished session and displays the pending question awaiting a stakeholder answer.*

### Interactive CLI Entry Point (`src.main`)

For interactive terminal conversations:
```bash
python -m src.main --input project_input.json
# or pass parameters directly:
python -m src.main --case_id CASE-001 --project_name "Smart Clinic" --initial_requirements "A clinic queue system..."
```
