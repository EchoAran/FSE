"""LLM Engine instantiation and invocation dispatcher."""

import os
from typing import Any, Dict

from src.utils.llm.models.data import ModelResponse


def get_engine(model_name: str, **kwargs: Any) -> Any:
    """Create and return a language model engine based on the model name."""
    if "temperature" not in kwargs:
        kwargs["temperature"] = 0.0

    max_tokens = kwargs.pop("max_tokens", None)
    max_output_tokens = kwargs.pop("max_output_tokens", None)
    max_tokens_to_sample = kwargs.pop("max_tokens_to_sample", None)
    token_limit = max_output_tokens or max_tokens or max_tokens_to_sample or 8192

    if model_name == "gpt-4o-mini":
        model_name = "gpt-4o-mini-2024-07-18"

    # Lazy import optional vendor engines
    if "claude" in model_name.lower():
        from src.utils.llm.models.claude import ClaudeVertexEngine
        kwargs["max_tokens_to_sample"] = token_limit
        return ClaudeVertexEngine(model_name=model_name, **kwargs)

    if "gemini" in model_name.lower():
        from src.utils.llm.models.gemini import GeminiVertexEngine
        kwargs["max_output_tokens"] = token_limit
        return GeminiVertexEngine(model_name=model_name, **kwargs)

    if "deepseek" in model_name.lower():
        from src.utils.llm.models.deepseek import DeepSeekEngine
        kwargs["max_tokens"] = token_limit
        return DeepSeekEngine(model_name=model_name, **kwargs)

    if model_name.startswith("vllm:"):
        from src.utils.llm.models.vllm import VLLMEngine
        actual_model_name = model_name[5:]
        kwargs["max_tokens"] = token_limit
        return VLLMEngine(model_name=actual_model_name, **kwargs)

    if "llama" in model_name.lower() or "together" in model_name.lower():
        from langchain_together import ChatTogether
        kwargs["max_tokens"] = token_limit
        kwargs["model_name"] = model_name
        return ChatTogether(**kwargs)

    # Standard OpenAI models
    from langchain_openai import ChatOpenAI
    kwargs["max_tokens"] = token_limit
    kwargs["model_name"] = model_name
    return ChatOpenAI(**kwargs)


def invoke_engine(engine: Any, prompt: str, **kwargs: Any) -> ModelResponse:
    """Invoke the language model engine and return structured ModelResponse."""
    response = engine.invoke(prompt, **kwargs)

    if isinstance(response, ModelResponse):
        return response

    content = getattr(response, "content", str(response))
    model_response = ModelResponse(content)

    if hasattr(response, "response_metadata") and "token_usage" in response.response_metadata:
        model_response.response_metadata = {
            "token_usage": response.response_metadata["token_usage"]
        }

    return model_response
