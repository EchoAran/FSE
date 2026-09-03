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

### Directory Structure

```text
hashimoto/
├── config/
│   ├── default.yaml               # Runtime configuration (prompts_re, fill_rate_threshold=0.8)
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
│   ├── models.py                  # Domain data classes (Slot, DialogueTurn, InterviewTurn, etc.)
│   └── transcript.py              # Transcript and Checkpoint JSON persistence
├── tests/
│   ├── mock_client.py             # Deterministic multi-stage mock client
│   ├── test_slot_operations.py    # Unit tests for individual stages
│   ├── test_interviewer_flow.py   # Multi-turn conversation and atomicity tests
│   ├── test_method_fidelity.py    # Method fidelity and regression tests
│   └── test_transcript_restoration.py # 100% lossless session resume tests
├── examples/
│   ├── sample_cases/              # Sample YAML software requirement cases
│   ├── career_toy_run.py          # Career domain demonstration run
│   └── run_sample_interview.py    # CLI interview demonstration script
├── requirements.txt
├── METHOD_SPEC.md                 # Method specification
└── README.md
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

### Running Demonstrations

```bash
# Run career domain reference demonstration
python examples/career_toy_run.py

# Run RE domain sample interview in offline mock mode
python examples/run_sample_interview.py --mock --case examples/sample_cases/clinic_management.yaml

# Run RE domain interview in live mode (requires OPENAI_API_KEY)
python examples/run_sample_interview.py --case examples/sample_cases/clinic_management.yaml
```

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

# 2. Initialize interviewer
config = InterviewConfig(model="gpt-4o", max_turns=20, fill_rate_threshold=0.8)
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

# 6. Lossless session resumption from checkpoint
resumed = HashimotoInterviewer(config=config)
loaded_checkpoint = TranscriptExporter.load_checkpoint("output/clinic_checkpoint.json")
resumed.resume_from_checkpoint(loaded_checkpoint)
```
