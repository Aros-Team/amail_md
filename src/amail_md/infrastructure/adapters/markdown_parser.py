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
MarkdownItParser adapter: converts markdown to GenericToken list.

Uses markdown-it-py with attrs_plugin for extended syntax support.
"""

from __future__ import annotations

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins.attrs import attrs_plugin

from amail_md.core.ports.generic_token import GenericToken


class MarkdownItParser:
    """
    Markdown parser adapter using markdown-it-py.

    Parses markdown source into a list of GenericToken objects that
    the segmenter engine can consume.
    """

    def __init__(self) -> None:
        """Initialize the parser with attrs_plugin enabled."""
        self._md = MarkdownIt().use(attrs_plugin)

    def parse(self, source: str) -> list[GenericToken]:
        """
        Parse markdown source to GenericToken list.

        Args:
            source: Markdown source string.

        Returns:
            List of GenericToken representing the parsed markdown.

        """
        tokens = self._md.parse(source)
        return [self._convert_token(t) for t in tokens]

    def _convert_token(self, token: Token) -> GenericToken:
        """
        Convert a markdown-it token to GenericToken.

        Args:
            token: A markdown-it Token object.

        Returns:
            A GenericToken representation.

        """
        attrs = {k: str(v) for k, v in token.attrs.items()} if token.attrs else {}

        children: list[GenericToken] = []
        if token.children:
            children = [self._convert_token(c) for c in token.children]

        return GenericToken(
            type=token.type,
            content=token.content or "",
            attrs=attrs,
            children=children,
            tag=token.tag or "",
            nesting=token.nesting,
        )
