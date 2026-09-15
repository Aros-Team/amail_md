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

"""Paragraph builder: converts GenericToken to Paragraph EmailStructure."""

from amail_md.core.models.email_structure.paragraph import Paragraph
from amail_md.core.ports.generic_token import GenericToken

from ..registry import register_builder


@register_builder("paragraph_open")
def build_paragraph(token: GenericToken) -> Paragraph:
    """
    Build a Paragraph from a paragraph_open token.

    Args:
        token: A GenericToken of type ``paragraph_open``.

    Returns:
        A Paragraph EmailStructure instance.

    """
    return Paragraph(text=token.content)
