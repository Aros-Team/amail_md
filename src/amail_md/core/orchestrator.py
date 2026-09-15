# Copyright 2026 Aros Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Orchestrator: drives the markdown-to-email pipeline.

Pure functions only — no I/O, no global state.
"""

from __future__ import annotations

from amail_md.core.models.email_structure.base import EmailStructure
from amail_md.core.services.segmenter.engine import segment
from amail_md.infrastructure.adapters.markdown_parser import MarkdownItParser
from amail_md.infrastructure.adapters.mjml.compiler import compile_mjml


def markdown_to_email_parts(source: str) -> dict[str, object]:
    """
    Convert markdown to EmailStructure list and MJML.

    This is the internal pipeline orchestrator.  It parses markdown,
    segments into EmailStructure objects, and compiles to MJML/HTML.

    Args:
        source: Markdown source string.

    Returns:
        Dict with 'elements' (list[EmailStructure]), 'mjml' (str),
        and 'html' (str).

    """
    parser = MarkdownItParser()
    tokens = parser.parse(source)
    elements = segment(tokens)
    html = compile_mjml(elements)

    return {
        "elements": elements,
        "mjml": _build_mjml(elements),
        "html": html,
    }


def _build_mjml(elements: list[EmailStructure]) -> str:
    """
    Build MJML string from EmailStructure list (for inspection).

    Args:
        elements: List of EmailStructure objects.

    Returns:
        MJML string.

    """
    from amail_md.infrastructure.adapters.mjml.registry import RENDER_REGISTRY

    lines = [
        "<mjml>",
        "<mj-body>",
    ]

    for element in elements:
        model_type = type(element)
        if model_type in RENDER_REGISTRY:
            render_func = RENDER_REGISTRY[model_type]
            lines.append(render_func(element))

    lines.extend(["</mj-body>", "</mjml>"])
    return "\n".join(lines)
