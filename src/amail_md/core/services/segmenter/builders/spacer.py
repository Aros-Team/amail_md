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

"""Spacer builder: converts GenericToken to Spacer EmailStructure."""

from amail_md.core.models.email_structure.spacer import Spacer
from amail_md.core.ports.generic_token import GenericToken

from ..registry import register_builder


@register_builder("spacer")
def build_spacer(token: GenericToken) -> Spacer:
    """
    Build a Spacer from a spacer token.

    Args:
        token: A GenericToken of type ``spacer``.

    Returns:
        A Spacer EmailStructure instance.

    """
    height = token.attrs.get("height", "24px")
    return Spacer(height=height)
