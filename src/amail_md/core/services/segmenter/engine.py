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
Segmenter engine: walks GenericToken list and builds EmailStructure objects.

Uses BUILDER_REGISTRY to dispatch token types to registered builders.
"""

from __future__ import annotations

from amail_md.core.models.email_structure.base import EmailStructure
from amail_md.core.ports.generic_token import GenericToken

from . import builders  # noqa: F401 — forces decorator execution
from .registry import BUILDER_REGISTRY


def segment(tokens: list[GenericToken]) -> list[EmailStructure]:
    """
    Walk tokens and build EmailStructure objects.

    Iterates through the token list (including children), looking up
    each token type in BUILDER_REGISTRY.  If a builder exists, it is
    called to produce an EmailStructure instance.

    For inline elements like links/buttons, the text content is in a
    sibling token.  The segmenter collects text between open/close
    pairs and injects it into the open token's content field.

    Args:
        tokens: List of GenericToken from the parser.

    Returns:
        List of EmailStructure objects.

    """
    elements: list[EmailStructure] = []

    for token in tokens:
        _process_token(token, elements)

    return elements


def _process_token(token: GenericToken, elements: list[EmailStructure]) -> None:
    """
    Process a single token and its children recursively.

    Args:
        token: The token to process.
        elements: Accumulator for produced EmailStructure objects.

    """
    if token.type in BUILDER_REGISTRY:
        builder = BUILDER_REGISTRY[token.type]
        element = builder(token)
        elements.append(element)

    if token.children:
        _process_inline_children(token.children, elements)


def _process_inline_children(
    children: list[GenericToken], elements: list[EmailStructure]
) -> None:
    """
    Process inline children, collecting text for open/close pairs.

    When a token with nesting=+1 (open) is followed by text tokens and
    a matching close token, the text content is injected into the open
    token's content field before building.

    Args:
        children: List of child tokens from an inline token.
        elements: Accumulator for produced EmailStructure objects.

    """
    i = 0
    while i < len(children):
        child = children[i]

        if child.nesting == 1 and child.type in BUILDER_REGISTRY:
            # Collect text from subsequent tokens until close
            text_parts: list[str] = []
            j = i + 1
            while j < len(children):
                next_child = children[j]
                if next_child.nesting == -1:
                    break
                if next_child.type == "text" and next_child.content:
                    text_parts.append(next_child.content)
                j += 1

            # Inject collected text into the open token
            if text_parts:
                child.content = "".join(text_parts)

            builder = BUILDER_REGISTRY[child.type]
            element = builder(child)
            elements.append(element)
            i = j + 1  # Skip past the close token
        else:
            _process_token(child, elements)
            i += 1
