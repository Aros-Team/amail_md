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

"""Quote builder: converts GenericToken to Quote EmailStructure."""

from amail_md.core.models.email_structure.quote import Quote
from amail_md.core.ports.generic_token import GenericToken

from ..registry import register_builder


@register_builder("blockquote_open")
def build_quote(token: GenericToken) -> Quote:
    """
    Build a Quote from a blockquote_open token.

    Args:
        token: A GenericToken of type ``blockquote_open``.

    Returns:
        A Quote EmailStructure instance.

    """
    text_parts: list[str] = []
    for child in token.children:
        if child.content:
            text_parts.append(child.content)
    return Quote(text=" ".join(text_parts))
