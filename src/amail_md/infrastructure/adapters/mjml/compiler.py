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
MrmlCompiler adapter: compiles MJML to email-safe HTML.

Uses the mrml Rust library for fast, email-safe HTML compilation.
"""

from __future__ import annotations

import mrml

from amail_md.core.models.email_structure.base import EmailStructure

from . import nodes  # noqa: F401 — forces decorator execution
from .registry import RENDER_REGISTRY


def compile_mjml(elements: list[EmailStructure]) -> str:
    """
    Compile EmailStructure list to email-safe HTML.

    Renders each element to MJML via the registry, wraps in mjml tags,
    and compiles to HTML via mrml.

    Args:
        elements: List of EmailStructure objects to render.

    Returns:
        Email-safe HTML string.

    Raises:
        NotImplementedError: If no renderer is registered for an element type.

    """
    mjml_lines = [
        "<mjml>",
        "<mj-head>",
        "<mj-attributes>",
        '<mj-all font-family="Arial, sans-serif" />',
        "</mj-attributes>",
        "</mj-head>",
        "<mj-body>",
    ]

    for element in elements:
        model_type = type(element)

        if model_type not in RENDER_REGISTRY:
            raise NotImplementedError(
                f"No MJML renderer registered for {model_type.__name__}"
            )

        render_func = RENDER_REGISTRY[model_type]
        mjml_lines.append(render_func(element))

    mjml_lines.extend(["</mj-body>", "</mjml>"])

    mjml_str = "\n".join(mjml_lines)
    output = mrml.to_html(mjml_str)
    return output.content
