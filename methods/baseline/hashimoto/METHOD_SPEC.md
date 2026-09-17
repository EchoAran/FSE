# Hashimoto Method Specification: Dynamic Slot Generation + Abduction

Specification for reproducing Hashimoto et al. (COLING 2025): *A Career Interview Dialogue System using Large Language Model-based Dynamic Slot Generation*.

## 1. System Overview

Hashimoto Proposed Method 2 performs semi-structured interviews through an explicit, expandable slot-filling architecture powered by Large Language Models.

### Operational Loop (Proposed Method 2)

Each conversational turn follows a three-stage sequential pipeline:

```text
Stakeholder Utterance
        ↓
1. Slot Filling (LLM Stage 1 - Appendix A Figure 6)
   Updates values of existing slots based on conversation history and background context.
   Outputs JSON object with {<Slot Name>: {"category": "...", "value": ...}}.
   Constraint: Does not add new slots or delete existing slots.
        ↓
2. Abductive Slot Generation (LLM Stage 2 - Appendix A Figures 4 & 5)
   Infers Surprising Fact C and Reason to Suspect A from dialogue.
   Generates new probing/dynamic slots directly guided by A and emerging topics:
   Outputs {"Surprising Fact C": ..., "Reason to Suspect A": ..., "New Slot": {<name>: {category, value}}}.
   Constraint: Proposes at most 5 new candidate slots in total per turn; all initialized with value = null.
   Deduplication: Prevents duplicate (C, A) records in Abduction History; binds records only to successfully added slots.
        ↓
[Check Termination Conditions]
   - turn >= max_turns OR
   - fill_rate > fill_rate_threshold (strictly > 80%)
        ↓
3. Question Generation (LLM Stage 3 - Appendix A Figure 7)
   Synthesizes exactly ONE targeted question focusing on unfilled / abduced slots.
   Outputs {"Target Slot S": {<slot_name>: {category, value}}, "Question": "..."}.
   Internal State: Maintains active Target Slot S in InterviewTurn and InterviewCheckpoint.
        ↓
Interviewer Utterance
```

## 2. State Model

- **Initial Context**: Background context (`initial_requirements` in RE or `self-assessment` in Career) injected across all stages.
- **Slots Dictionary**: `dict[str, Slot]` where `Slot = {name: str, category: str, value: str | None}`.
- **Abduction History**: Chronological list of `AbductionRecord = {surprising_fact: str, suspected_reason: str, new_slot: str}`.
- **Dialogue History**: Sequence of `Message(role, content)`.
- **Public Transcript**: Clean user-facing conversation transcript (`case_id`, `project_name`, `turns: list[DialogueTurn]`) containing only dialogue utterances and turn IDs.
- **Internal Checkpoint**: Complete internal execution snapshot (`case_id`, `project_name`, `initial_requirements`, `turns: list[InterviewTurn]`, `slots`, `abduction_history`, `pending_question`, `pending_target_slots`, `is_finished`) for 100% lossless session restoration.

## 3. Domain Assets

- **Original Career Domain (Paper Table 2 & Appendix A)**:
  - Initial Slots (Table 2):
    1. `Career aspirations for next year` (Category: `Career`)
    2. `Career development plan` (Category: `Career, Plan`)
    3. `Future department preferences` (Category: `Career, Preference`)
    4. `Career-related concerns` (Category: `Career, Concerns`)
    5. `Training preferences` (Category: `Training, Preference`)
    6. `Current job duties` (Category: `Job`)
    7. `Job satisfaction` (Category: `Job, Satisfaction`)
    8. `Job dissatisfaction` (Category: `Job, Dissatisfaction`)
  - Persona (Figure 7): Keiko Naasu (34 years old, experienced nurse with over 10 years clinical experience across multiple departments, mentor to junior nurses, friendly and casual speaking style).
  - JSON Shapes: Appendix A Figure 5 (`Surprising Fact C`, `Reason to Suspect A`, `New Slot`), Figure 6 (`{Slot: {category, value}}`), Figure 7 (`Target Slot S`, `Question`).
- **Software RE Domain (Adapted)**:
  - Initial Slots: 8 software requirements slots derived from Volere / IREB / ISO 29148 (`project_goals`, `stakeholder_roles`, `functional_needs`, `business_rules`, `data_entities`, `constraints`, `quality_concerns`, `boundary_conditions`).
  - Persona: Senior Requirements Analyst.
  - Abduction Semantics: Surprising constraint/risk fact $C \rightarrow$ underlying technical/business reason $A \rightarrow$ probing slot.
