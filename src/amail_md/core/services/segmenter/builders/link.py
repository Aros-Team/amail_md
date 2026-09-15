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
Link builder: converts GenericToken to Link EmailStructure.

Note: link_open tokens with button class are handled by the Button builder.
This module provides build_link() for non-button links, but does NOT register
in the registry — the Button builder delegates to this function when appropriate.
"""

from amail_md.core.models.email_structure.link import Link
from amail_md.core.ports.generic_token import GenericToken


def build_link(token: GenericToken) -> Link:
    """
    Build a Link from a link_open token.

    Args:
        token: A GenericToken of type ``link_open``.

    Returns:
        A Link EmailStructure instance.

    """
    href = token.attrs.get("href", "")
    return Link(href=href, text=token.content)
