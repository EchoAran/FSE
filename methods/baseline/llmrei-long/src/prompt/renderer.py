"""Context renderer integrating software case requirements with the base prompt."""

from src.models import RequirementCase


class PromptRenderer:
    """Combines a base system prompt template with project case requirements."""

    @staticmethod
    def render(base_prompt: str, case: RequirementCase) -> str:
        """Append software project background context to the base interview prompt."""
        context_block = (
            f"\n\n---\n"
            f"Project Name: {case.project_name}\n"
            f"Project Background and Initial Requirements:\n"
            f"{case.initial_requirements.strip()}\n"
            f"---"
        )
        return f"{base_prompt.strip()}{context_block}"
