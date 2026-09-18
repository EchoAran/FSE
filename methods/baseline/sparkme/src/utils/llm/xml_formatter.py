"""XML serialization and parsing utilities for LLM tool calls."""

import ast
import html
import json
import re
from typing import Any, Dict, List, Type
import xml.etree.ElementTree as ET

from langchain_core.tools import BaseTool
from pydantic import BaseModel

from src.utils.constants.colors import ORANGE, RESET


def format_tool_as_xml_v2(tool: Type[BaseTool]) -> str:
    """Format a tool definition as XML for inclusion in system prompts."""
    lines = []
    lines.append(f"<{tool.name}>")
    lines.append("  <description>")
    lines.append(f"    {tool.description}")
    lines.append("  </description>")

    if tool.args_schema and issubclass(tool.args_schema, BaseModel):
        lines.append("  <arguments>")
        for field_name, field in tool.args_schema.model_fields.items():
            lines.append(f"    <{field_name}>")
            lines.append(f"      <type>{getattr(field.annotation, '__name__', str(field.annotation))}</type>")
            if field.description:
                lines.append("      <description>")
                lines.append(f"        {field.description}")
                lines.append("      </description>")
            lines.append(f"    </{field_name}>")
        lines.append("  </arguments>")

    lines.append(f"</{tool.name}>")
    return "\n".join(lines)


def parse_value(text: str) -> Any:
    """Parse a scalar or serialized value (int, float, bool, list, dict, or string)."""
    if not text:
        return ""
    text = text.strip()

    if text.lower() == "true":
        return True
    if text.lower() == "false":
        return False

    if re.match(r"^-?\d+$", text):
        try:
            return int(text)
        except ValueError:
            pass
    elif re.match(r"^-?\d+\.\d+$", text):
        try:
            return float(text)
        except ValueError:
            pass

    if (text.startswith("[") and text.endswith("]")) or (text.startswith("{") and text.endswith("}")):
        try:
            return json.loads(text)
        except (json.JSONDecodeError, TypeError):
            try:
                return ast.literal_eval(text)
            except Exception:
                pass

    return text


def _parse_xml_node(element: ET.Element) -> Any:
    """Recursively parse an XML element into appropriate Python types (dict, list, or scalar)."""
    children = list(element)
    if not children:
        text = element.text if element.text is not None else ""
        text_str = text.strip()
        if element.tag.endswith("_id") or element.tag in ("id", "subtopic_id", "topic_id", "user_id", "case_id"):
            return text_str
        return parse_value(text)

    child_tags = [child.tag for child in children]

    # If all child tags are identical (e.g., <insight>, <question>, <item>), treat as a list
    if len(set(child_tags)) == 1:
        return [_parse_xml_node(child) for child in children]

    result_dict: Dict[str, Any] = {}
    for child in children:
        tag = child.tag
        val = _parse_xml_node(child)
        if tag in result_dict:
            if not isinstance(result_dict[tag], list):
                result_dict[tag] = [result_dict[tag]]
            result_dict[tag].append(val)
        else:
            result_dict[tag] = val
    return result_dict


TOOL_CALL_TAG_PATTERN = re.compile(r"<(/?)([A-Za-z_][\w.-]*)\s*(/?)>")


def _parse_xml_tolerant(xml_string: str) -> ET.Element:
    """Parse XML into an Element tree, tolerating unbalanced tags.

    LLM-generated tool calls occasionally drop or add a closing tag, which an
    ElementTree parse rejects outright; such a slip should not abort the
    session, so tags left open are closed implicitly by their parent's end tag.
    """
    root = ET.Element("tool_calls")
    stack = [root]
    cursor = 0

    for match in TOOL_CALL_TAG_PATTERN.finditer(xml_string):
        text = xml_string[cursor:match.start()]
        if text:
            stack[-1].text = (stack[-1].text or "") + html.unescape(text)
        cursor = match.end()

        closing, tag, self_closing = match.group(1), match.group(2), match.group(3)
        if self_closing:
            ET.SubElement(stack[-1], tag)
        elif closing:
            for index in range(len(stack) - 1, 0, -1):
                if stack[index].tag == tag:
                    del stack[index:]
                    break
        elif tag != root.tag or len(stack) > 1:
            stack.append(ET.SubElement(stack[-1], tag))

    text = xml_string[cursor:]
    if text:
        stack[-1].text = (stack[-1].text or "") + html.unescape(text)

    return root


def parse_tool_calls(xml_string: str) -> List[Dict[str, Any]]:
    """Parse XML tool calls with support for nested tags and entity escaping."""
    xml_string = xml_string.replace("&", "&amp;")
    xml_string = xml_string.replace('"', "&quot;")
    xml_string = xml_string.replace("'", "&apos;")

    def escape_response_content(match: re.Match) -> str:
        content = match.group(1)
        escaped_content = content.replace("<", "&lt;").replace(">", "&gt;")
        return f"<response>{escaped_content}</response>"

    xml_string = re.sub(r"<response>(.*?)</response>", escape_response_content, xml_string, flags=re.DOTALL)

    root = _parse_xml_tolerant(xml_string)
    result = []

    for tool_element in root:
        tool_name = tool_element.tag
        arguments = {}

        for arg in tool_element:
            arguments[arg.tag] = _parse_xml_node(arg)

        result.append({
            "tool_name": tool_name,
            "arguments": arguments,
        })

    return result


def call_tool_from_xml(tool_calls_xml_string: str, available_tools: Dict[str, BaseTool]) -> str:
    """Execute parsed tool calls against available tools dictionary."""
    parsed_calls = parse_tool_calls(tool_calls_xml_string)
    results = []

    for call in parsed_calls:
        tool_name = call["tool_name"]
        arguments = call["arguments"]

        if tool_name not in available_tools:
            results.append(f"Error: Tool '{tool_name}' not found.")
            continue

        tool = available_tools[tool_name]
        try:
            result = tool._run(**arguments)
            results.append(f"Tool '{tool_name}' executed successfully. Result: {result}")
        except Exception as e:
            results.append(f"Error calling tool '{tool_name}': {str(e)}")

    return "\n".join(results)


def extract_tool_calls_xml(response: str) -> str:
    """Extract the tool_calls XML block from a model response string."""
    tool_calls_start = response.find("<tool_calls>")
    tool_calls_end = response.find("</tool_calls>")
    if tool_calls_start == -1 or tool_calls_end == -1:
        return ""
    return response[tool_calls_start:tool_calls_end + len("</tool_calls>")]


def clean_malformed_xml(xml_string: str) -> str:
    """Clean malformed XML by removing unmatched tags."""
    tokens = []
    current_token = ""

    for char in xml_string:
        if char == "<":
            if current_token:
                tokens.append(current_token)
            current_token = "<"
        elif char == ">":
            current_token += ">"
            tokens.append(current_token)
            current_token = ""
        else:
            current_token += char

    if current_token:
        tokens.append(current_token)

    tag_stack = []
    result_tokens = []

    for token in tokens:
        if not token.startswith("<"):
            result_tokens.append(token)
            continue

        if token.startswith("</"):
            tag_name = token[2:-1].strip()
            if tag_stack and tag_stack[-1] == tag_name:
                tag_stack.pop()
                result_tokens.append(token)
        elif token.startswith("<"):
            tag_name = token[1:-1].strip()
            if not tag_name.startswith("?") and not tag_name.startswith("!"):
                tag_stack.append(tag_name)
            result_tokens.append(token)

    return "".join(result_tokens)


def extract_tool_arguments(response: str, tool_name: str, arg_name: str) -> List[Any]:
    """Extract specific argument values from tool calls in a response."""
    if "<tool_calls>" not in response:
        return []

    tool_calls_start = response.find("<tool_calls>")
    tool_calls_end = response.find("</tool_calls>")
    if tool_calls_start == -1 or tool_calls_end == -1:
        return []

    tool_calls_xml = response[tool_calls_start:tool_calls_end + len("</tool_calls>")]
    cleaned_xml = clean_malformed_xml(tool_calls_xml)

    values = []
    for call in parse_tool_calls(cleaned_xml):
        if call["tool_name"] == tool_name:
            value = call["arguments"].get(arg_name)
            if value is not None:
                values.append(value)

    return values
