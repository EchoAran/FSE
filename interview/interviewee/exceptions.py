"""Custom exceptions for the interviewee agent."""


class IntervieweeError(Exception):
    """Base exception for all interviewee agent errors."""
    pass


class IntervieweeLLMError(IntervieweeError):
    """Raised when the LLM service fails, times out, or cannot be reached."""
    pass


class IntervieweeEmptyAnswerError(IntervieweeError):
    """Raised when the LLM produces an empty or whitespace-only response."""
    pass
