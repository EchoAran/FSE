"""Prompt templates for the Exploration Planner agent in requirements elicitation."""

from src.utils.llm.prompt_utils import format_prompt


def get_prompt(prompt_type: str) -> str:
    """Return formatted prompt string based on the requested prompt type."""
    if prompt_type == "draft_rollouts":
        return format_prompt(DRAFT_ROLLOUTS_PROMPT, {
            "CONTEXT": DRAFT_ROLLOUTS_CONTEXT,
            "SESSION_STATE": DRAFT_ROLLOUTS_SESSION_STATE,
            "INSTRUCTIONS": DRAFT_ROLLOUTS_INSTRUCTIONS,
            "OUTPUT_FORMAT": DRAFT_ROLLOUTS_OUTPUT_FORMAT,
        })
    elif prompt_type == "judge_coverage":
        return format_prompt(JUDGE_COVERAGE_PROMPT, {
            "CONTEXT": JUDGE_COVERAGE_CONTEXT,
            "ROLLOUT_DATA": JUDGE_COVERAGE_ROLLOUT_DATA,
            "INSTRUCTIONS": JUDGE_COVERAGE_INSTRUCTIONS,
            "OUTPUT_FORMAT": JUDGE_COVERAGE_OUTPUT_FORMAT,
        })
    elif prompt_type == "brainstorm_emergent_subtopic":
        return format_prompt(BRAINSTORM_EMERGENT_SUBTOPIC_PROMPT, {
            "CONTEXT": BRAINSTORM_EMERGENT_SUBTOPIC_CONTEXT,
            "INSTRUCTIONS": BRAINSTORM_EMERGENT_SUBTOPIC_INSTRUCTIONS,
            "ADDITIONAL_CONTEXT": BRAINSTORM_EMERGENT_SUBTOPIC_ADDITIONAL_CONTEXT,
            "TOPICS_AND_SUBTOPICS": BRAINSTORM_EMERGENT_SUBTOPIC_TOPICS_AND_SUBTOPICS,
            "TOOL_DESCRIPTIONS": BRAINSTORM_EMERGENT_SUBTOPIC_TOOL,
            "OUTPUT_FORMAT": BRAINSTORM_EMERGENT_SUBTOPIC_OUTPUT_FORMAT,
        })
    elif prompt_type == "identify_emergent_insights":
        return format_prompt(IDENTIFY_EMERGENT_INSIGHTS_PROMPT, {
            "CONTEXT": IDENTIFY_EMERGENT_INSIGHTS_CONTEXT,
            "INSTRUCTIONS": IDENTIFY_EMERGENT_INSIGHTS_INSTRUCTIONS,
            "TOPICS_AND_SUBTOPICS": IDENTIFY_EMERGENT_INSIGHTS_TOPICS_AND_SUBTOPICS,
            "ADDITIONAL_CONTEXT": IDENTIFY_EMERGENT_INSIGHTS_ADDITIONAL_CONTEXT,
            "TOOL_DESCRIPTIONS": IDENTIFY_EMERGENT_INSIGHTS_TOOL,
            "OUTPUT_FORMAT": IDENTIFY_EMERGENT_INSIGHTS_OUTPUT_FORMAT,
        })
    elif prompt_type == "generate_strategic_questions":
        return format_prompt(GENERATE_STRATEGIC_QUESTIONS_PROMPT, {
            "CONTEXT": GENERATE_STRATEGIC_QUESTIONS_CONTEXT,
            "INSTRUCTIONS": GENERATE_STRATEGIC_QUESTIONS_INSTRUCTIONS,
            "ADDITIONAL_CONTEXT": GENERATE_STRATEGIC_QUESTIONS_ADDITIONAL_CONTEXT,
            "TOPICS_AND_SUBTOPICS": GENERATE_STRATEGIC_QUESTIONS_TOPICS_AND_SUBTOPICS,
            "TOOL_DESCRIPTIONS": GENERATE_STRATEGIC_QUESTIONS_TOOL,
            "OUTPUT_FORMAT": GENERATE_STRATEGIC_QUESTIONS_OUTPUT_FORMAT,
        })
    else:
        raise ValueError(f"Unknown prompt type: {prompt_type}")


# =============================================================================
# BRAINSTORM EMERGENT SUBTOPIC
# =============================================================================

BRAINSTORM_EMERGENT_SUBTOPIC_PROMPT = """
{CONTEXT}

{TOPICS_AND_SUBTOPICS}

{ADDITIONAL_CONTEXT}

{TOOL_DESCRIPTIONS}

{INSTRUCTIONS}

{OUTPUT_FORMAT}
"""

BRAINSTORM_EMERGENT_SUBTOPIC_CONTEXT = """
<exploration_planner_persona>
You are an Exploration Planner analyzing software requirements elicitation dialogues.
Your role is to identify newly emerging, unmapped requirement themes from stakeholder responses that fit under an existing major topic but are not covered by any current predefined subtopic.
Be concise and avoid redundancy.
</exploration_planner_persona>

<context>
Review the active dialogue and requirements agenda.
</context>
"""

BRAINSTORM_EMERGENT_SUBTOPIC_TOPICS_AND_SUBTOPICS = """
Current Requirements Agenda:
<topics_list>
{topics_and_subtopics}
</topics_list>
"""

BRAINSTORM_EMERGENT_SUBTOPIC_ADDITIONAL_CONTEXT = """
Recent Dialogue and Notes:
<additional_context>
{additional_context}
</additional_context>
"""

BRAINSTORM_EMERGENT_SUBTOPIC_TOOL = """
<tool_descriptions>
{tool_descriptions}
</tool_descriptions>
"""

BRAINSTORM_EMERGENT_SUBTOPIC_INSTRUCTIONS = """
<instructions>
1. Check if the stakeholder introduced an important new requirement theme (e.g., unexpected compliance constraint, specific third-party integration, novel workflow exception).
2. If it is truly distinct and fits under an existing parent topic, call `add_emergent_subtopic` with the topic ID and a concise subtopic description.
3. If no new subtopics are introduced, take no action.
</instructions>
"""

BRAINSTORM_EMERGENT_SUBTOPIC_OUTPUT_FORMAT = """
<output_format>
Enclose tool calls within <tool_calls> tags.
</output_format>
"""

# =============================================================================
# IDENTIFY EMERGENT INSIGHTS
# =============================================================================

IDENTIFY_EMERGENT_INSIGHTS_PROMPT = """
{CONTEXT}

{TOPICS_AND_SUBTOPICS}

{ADDITIONAL_CONTEXT}

{TOOL_DESCRIPTIONS}

{INSTRUCTIONS}

{OUTPUT_FORMAT}
"""

IDENTIFY_EMERGENT_INSIGHTS_CONTEXT = """
<exploration_planner_persona>
You identify novel, non-obvious, or critical architectural insights and edge cases from stakeholder statements.
</exploration_planner_persona>
"""

IDENTIFY_EMERGENT_INSIGHTS_TOPICS_AND_SUBTOPICS = """
Requirements Agenda:
{topics_and_subtopics}
"""

IDENTIFY_EMERGENT_INSIGHTS_ADDITIONAL_CONTEXT = """
Recent Notes:
{additional_context}
"""

IDENTIFY_EMERGENT_INSIGHTS_TOOL = """
{tool_descriptions}
"""

IDENTIFY_EMERGENT_INSIGHTS_INSTRUCTIONS = """
<instructions>
Identify counter-intuitive or high-impact requirement constraints and call `identify_emergent_insights` with:
- subtopic_id
- description
- novelty_score (1 to 5)
- evidence
- conventional_belief
</instructions>
"""

IDENTIFY_EMERGENT_INSIGHTS_OUTPUT_FORMAT = """
<output_format>
Enclose tool calls in <tool_calls> tags.
</output_format>
"""

# =============================================================================
# GENERATE STRATEGIC QUESTIONS
# =============================================================================

GENERATE_STRATEGIC_QUESTIONS_PROMPT = """
{CONTEXT}

{TOPICS_AND_SUBTOPICS}

{ADDITIONAL_CONTEXT}

{TOOL_DESCRIPTIONS}

{INSTRUCTIONS}

{OUTPUT_FORMAT}
"""

GENERATE_STRATEGIC_QUESTIONS_CONTEXT = """
<exploration_planner_persona>
You formulate high-utility strategic questions to guide the interviewer toward addressing critical coverage gaps and exploring novel requirement findings.
</exploration_planner_persona>
"""

GENERATE_STRATEGIC_QUESTIONS_TOPICS_AND_SUBTOPICS = """
Requirements Agenda:
{topics_and_subtopics}
"""

GENERATE_STRATEGIC_QUESTIONS_ADDITIONAL_CONTEXT = """
Planning State & Utility Context:
{additional_context}
"""

GENERATE_STRATEGIC_QUESTIONS_TOOL = """
{tool_descriptions}
"""

GENERATE_STRATEGIC_QUESTIONS_INSTRUCTIONS = """
<instructions>
Generate strategic candidate questions and call `suggest_strategic_questions` with:
- content
- subtopic_id
- strategy_type ("coverage_gap" or "emergent_insight")
- priority (1-10)
- reasoning
</instructions>
"""

GENERATE_STRATEGIC_QUESTIONS_OUTPUT_FORMAT = """
<output_format>
Enclose tool calls in <tool_calls> tags.
</output_format>
"""

# =============================================================================
# DRAFT ROLLOUTS & JUDGE COVERAGE
# =============================================================================

DRAFT_ROLLOUTS_PROMPT = """
{CONTEXT}

{SESSION_STATE}

{INSTRUCTIONS}

{OUTPUT_FORMAT}
"""

DRAFT_ROLLOUTS_CONTEXT = """
<exploration_planner_persona>
You simulate future conversation trajectories (rollouts) between the interviewer and stakeholder to estimate expected requirements coverage and novelty gains.
</exploration_planner_persona>
"""

DRAFT_ROLLOUTS_SESSION_STATE = """
Current Requirements Agenda & History:
{session_state}
"""

DRAFT_ROLLOUTS_INSTRUCTIONS = """
<instructions>
Simulate multi-turn requirement elicitation exchanges for each candidate exploration path.
</instructions>
"""

DRAFT_ROLLOUTS_OUTPUT_FORMAT = """
<output_format>
Provide the simulated dialogue rollouts enclosed in <rollouts> tags.
</output_format>
"""

JUDGE_COVERAGE_PROMPT = """
{CONTEXT}

{ROLLOUT_DATA}

{INSTRUCTIONS}

{OUTPUT_FORMAT}
"""

JUDGE_COVERAGE_CONTEXT = """
<exploration_planner_persona>
You evaluate simulated dialogue rollouts to calculate expected coverage gain, conversational cost, and emergent novelty.
</exploration_planner_persona>
"""

JUDGE_COVERAGE_ROLLOUT_DATA = """
Simulated Rollouts to Evaluate:
{rollout_data}
"""

JUDGE_COVERAGE_INSTRUCTIONS = """
<instructions>
Evaluate each simulated rollout and score coverage gains across target subtopics.
</instructions>
"""

JUDGE_COVERAGE_OUTPUT_FORMAT = """
<output_format>
Output the evaluated scores.
</output_format>
"""
