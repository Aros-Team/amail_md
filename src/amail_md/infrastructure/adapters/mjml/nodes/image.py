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

"""Image MJML node: renders Image EmailStructure to ``<mj-image>``."""

from amail_md.core.models.email_structure.image import Image

from ..registry import register_node


@register_node(Image)
def render_image(element: Image) -> str:
    """
    Render an Image to an MJML ``<mj-image>`` element.

    Args:
        element: The Image EmailStructure to render.

    Returns:
        An MJML string ``<mj-image src="..." ... />``.

    """
    attrs = [f'src="{element.src}"']

    if element.alt:
        attrs.append(f'alt="{element.alt}"')

    if element.width:
        attrs.append(f'width="{element.width}"')

    if element.height:
        attrs.append(f'height="{element.height}"')

    if element.border_radius:
        attrs.append(f'border-radius="{element.border_radius}"')

    attrs_str = " ".join(attrs)
    return f"<mj-image {attrs_str} />"
