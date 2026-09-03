# Hashimoto: Dynamic Slot Generation + Abduction for Requirements Elicitation

Modular reproduction of the **Dynamic Slot Generation + Abduction** interview approach (Hashimoto et al., COLING 2025), adapted for Software Requirements Engineering (RE).

## Method Overview

The system conducts semi-structured requirements interviews by maintaining an explicit requirement slot dictionary and performing three sequential operational stages in each interaction turn:

```text
Stakeholder Utterance
        ↓
1. Slot Filling (updates existing slots with initial requirements context)
        ↓
2. Abductive Slot Generation (hypothesizes root cause and adds new slots ≤ 5)
        ↓
[Termination Check: turn >= max_turns or fill_rate > 80%]
        ↓
3. Question Generation (targets empty / newly abduced slots)
        ↓
Next Interviewer Question
```

## Reproduction and Adaptation Changes

This project implements the published Hashimoto Dynamic Slot Generation and Abduction workflow as a runnable software requirements interviewer.

- **Preserved method loop**: slot filling, abductive dynamic-slot generation, termination checking, and target-slot question generation remain separate and execute in that order.
- **Domain adaptation**: the reference career-domain assets remain under `prompts_original/` and `config/career_initial_slots.yaml`. The default runtime instead uses `prompts_re/` and eight software-requirements slots from `config/re_initial_slots.yaml`.
- **Prompt changes**: career, nurse, and self-assessment language was adapted to software projects, stakeholders, requirements analysts, constraints, risks, and implicit requirements. The structured slot-filling, abduction, and target-question output contracts are retained, while `initial_requirements` and conversation history are supplied to all three LLM stages.
- **Runtime interface**: `RequirementCase`, the OpenAI-compatible client, the high-level `HashimotoInterviewer`, public transcripts, internal checkpoints, and filesystem CLI scripts were added to make the method runnable and recoverable between turns.
- **Lifecycle and outputs**: the implementation applies the published method's explicit termination rule: `turn >= max_turns` or `fill_rate > fill_rate_threshold`. A terminal CLI step writes `final_state.json`, `transcript.json`, and the slot/abduction-based `summary.md`.

### Directory Structure

```text
hashimoto/
├── config/
│   ├── default.example.yaml       # Safe model/runtime configuration template
│   ├── re_initial_slots.yaml      # Standard RE initial slots (Volere / IREB / ISO 29148)
│   └── career_initial_slots.yaml  # Reference career initial slots (Table 2)
├── prompts_original/              # Career domain reference prompts maintaining method contract
│   ├── slot_filling.txt           # Structured dict-format slot filling
│   ├── abductive_slot_generation.txt # Unified abduction and slot generation
│   └── question_generation.txt    # Target Slot S question generation
├── prompts_re/                    # RE domain adapted prompts
│   ├── slot_filling.txt           # RE-adapted slot filling
│   ├── abductive_slot_generation.txt # RE-adapted abduction with deduplication
│   └── question_generation.txt    # RE Requirements Analyst question generation
├── src/
│   ├── client/
│   │   ├── base.py                # Abstract BaseLLMClient interface
│   │   └── openai_client.py       # OpenAI-compatible REST client
│   ├── core/
│   │   ├── slot_filler.py         # Dual-format SlotFiller component
│   │   ├── abductive_slot_generator.py # Unified abductive slot generator component
│   │   └── question_generator.py  # Dual-format QuestionGenerator component
│   ├── prompt/
│   │   └── loader.py              # Package-root aware prompt loader
│   ├── config.py                  # Typed configuration model
│   ├── interviewer.py             # HashimotoInterviewer multi-stage coordinator
│   ├── main.py                    # Interactive terminal entry point
│   ├── models.py                  # Domain data classes (Slot, DialogueTurn, InterviewTurn, etc.)
│   ├── project_store.py           # Checkpoint, transcript, and report storage
│   └── transcript.py              # Transcript and Checkpoint JSON persistence
├── scripts/
│   ├── init_project.py            # Create a persisted interview project
│   ├── step.py                    # Run one full method turn
│   ├── inspect_state.py           # Inspect slots, abductions, and dialogue
│   └── resume.py                  # Validate an unfinished checkpoint
├── requirements.txt
├── METHOD_SPEC.md                 # Method specification
└── README.md
```

## Quickstart

### Installation

```bash
pip install -r requirements.txt
```

### Model Configuration

From the `baseline/hashimoto` directory, create the local configuration file:

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
from src.interviewer import HashimotoInterviewer
from src.models import RequirementCase
from src.transcript import TranscriptExporter

# 1. Define requirement case
case = RequirementCase(
    case_id="CASE-001",
    project_name="Smart Clinic System",
    initial_requirements="Cloud-based clinic management and electronic medical records.",
)

# 2. Load local configuration and initialize interviewer
config = InterviewConfig.from_yaml("config/default.yaml")
interviewer = HashimotoInterviewer(config=config)
interviewer.initialize(case)

# 3. Start dialogue
first_question = interviewer.get_first_question()
print(first_question)

# 4. Multi-turn interaction
next_question = interviewer.step("Doctors need to access EMR offline during network drops.")
print(f"Active slots: {len(interviewer.slots)} | Fill rate: {interviewer.fill_rate:.0%}")
print(next_question)

# 5. Export clean public transcript and internal checkpoint
transcript = interviewer.export_transcript()
checkpoint = interviewer.export_checkpoint()
TranscriptExporter.save_transcript(transcript, "output/clinic_transcript.json")
TranscriptExporter.save_checkpoint(checkpoint, "output/clinic_checkpoint.json")

# 6. Lossless session resumption from an unfinished checkpoint
resumed = HashimotoInterviewer(config=config)
loaded_checkpoint = TranscriptExporter.load_checkpoint("output/clinic_checkpoint.json")
resumed.resume_from_checkpoint(loaded_checkpoint)
```

### CLI Tool Suite (`scripts/`)

The CLI tools save the current checkpoint and public transcript under `runs/{project_id}/`:

#### 1. Initialize Project (`init_project.py`)
```bash
python scripts/init_project.py --input project_input.json
```
*Creates project under `runs/{project_id}/`, saves initial checkpoint, and prints the first question.*

#### 2. Advance Dialogue Turn (`step.py`)
```bash
python scripts/step.py --project-id <PROJECT_ID> --answer "Doctors need offline EMR access during network outages."
```
*Advances one dialogue turn and updates slots and abductions. When the method's termination rule is met, it marks the project completed and writes the final checkpoint, transcript, and slot-based summary automatically.*

#### 3. Inspect Project State (`inspect_state.py`)
```bash
python scripts/inspect_state.py --project-id <PROJECT_ID> [--verbose]
```
*Displays current turn count, slot completion rate, slot details, and abduction reasoning history.*

#### 4. Validate and Resume Interrupted Session (`resume.py`)
```bash
python scripts/resume.py --project-id <PROJECT_ID>
```
*Restores an unfinished checkpoint and displays the pending question awaiting a stakeholder answer.*

### Interactive CLI Entry Point (`src.main`)

For interactive terminal conversations:
```bash
python -m src.main --input project_input.json
# or pass parameters directly:
python -m src.main --case_id CASE-001 --project_name "Smart Clinic" --initial_requirements "EMR system..."
```
