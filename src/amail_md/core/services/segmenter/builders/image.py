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

"""Image builder: converts GenericToken to Image EmailStructure."""

from amail_md.core.models.email_structure.image import Image
from amail_md.core.ports.generic_token import GenericToken

from ..registry import register_builder


@register_builder("image")
def build_image(token: GenericToken) -> Image:
    """
    Build an Image from an image token.

    Args:
        token: A GenericToken of type ``image``.

    Returns:
        An Image EmailStructure instance.

    """
    return Image(
        src=token.attrs.get("src", ""),
        alt=token.content,
        width=token.attrs.get("width"),
        height=token.attrs.get("height"),
        alignment=token.attrs.get("alignment", "center"),
        border_radius=token.attrs.get("border-radius"),
    )
