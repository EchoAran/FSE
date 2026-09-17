"""Method adapters package."""

from interview.adapters.base import AdapterResult, BaseMethodAdapter
from interview.adapters.registry import (
    METHOD_REGISTRY,
    MethodDescriptor,
    get_method_descriptor,
)
from interview.adapters.worker_client import ProcessWorkerClient

__all__ = [
    "AdapterResult",
    "BaseMethodAdapter",
    "METHOD_REGISTRY",
    "MethodDescriptor",
    "get_method_descriptor",
    "ProcessWorkerClient",
]
