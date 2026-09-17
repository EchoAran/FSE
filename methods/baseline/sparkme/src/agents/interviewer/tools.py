"""Interviewer tool definitions for dispatching responses to the user."""

import asyncio
from typing import Any, Callable, Optional, Type
from langchain_core.callbacks.manager import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field, SkipValidation


class ResponseToUserInput(BaseModel):
    """Input parameters for responding to the interviewee."""

    subtopic_id: str = Field(description="The chosen subtopic ID from the suggested subtopics.")
    response: str = Field(description="The response question formulated for the user.")


class RespondToUser(BaseTool):
    """Tool for formulating and dispatching the interviewer question to the user."""

    name: str = "respond_to_user"
    description: str = "A tool for responding to the user."
    args_schema: Type[BaseModel] = ResponseToUserInput

    on_response: SkipValidation[Callable[[str, str], Any]] = Field(
        description="Callback function to be called when responding to user"
    )
    on_turn_complete: SkipValidation[Callable[[], Any]] = Field(
        description="Callback function to be called when turn is complete"
    )

    async def _run(
        self,
        subtopic_id: str,
        response: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        """Run the tool to post the interviewer question."""
        quantified_response = await self.on_response(response, subtopic_id)
        await self.on_turn_complete()
        return f"Successfully responded to user: {quantified_response}"
