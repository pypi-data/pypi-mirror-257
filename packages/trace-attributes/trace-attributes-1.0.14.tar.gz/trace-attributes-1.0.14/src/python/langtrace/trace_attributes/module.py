# module.py
from typing import Any, Dict

from .models.openai_span_attributes import OpenAISpanAttributes


def create_span_from_dict(span_data: Dict[str, Any]) -> OpenAISpanAttributes:
    """
    Creates an OpenAISpanAttributes instance from a dictionary.
    This function demonstrates how to use the model for type validation
    and alias handling when receiving data as a dictionary.
    """
    return OpenAISpanAttributes(**span_data)