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
GenericToken: parser-agnostic token for segmenter consumption.

See ADR-010 for the design rationale.
"""

from dataclasses import dataclass, field


@dataclass
class GenericToken:
    """
    Parser-agnostic token for segmenter consumption.

    Each parser adapter converts its specific AST format to a GenericToken
    that builders consume. This decouples builders from any particular
    markdown parser implementation.

    Attributes:
        type: Token type (e.g. 'paragraph', 'heading_open', 'link_open').
        content: Text content of the token.
        attrs: Dictionary of attributes (e.g. {'button': True}).
        children: Nested tokens.
        tag: HTML tag name (e.g. 'h1', 'a').
        nesting: Nesting level (-1 open, 0 self-closing, 1 close).

    """

    type: str
    content: str = ""
    attrs: dict[str, str] = field(default_factory=dict)
    children: list["GenericToken"] = field(default_factory=list)
    tag: str = ""
    nesting: int = 0
    info: str = ""
