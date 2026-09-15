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
Segmenter registry: maps token types to builder functions.

See ADR-009 for the design rationale.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from amail_md.core.models.email_structure.base import EmailStructure

BUILDER_REGISTRY: dict[str, Callable[[Any], EmailStructure]] = {}

BuilderFunc = Callable[[Any], EmailStructure]
DecoratorType = Callable[[BuilderFunc], BuilderFunc]


def register_builder(token_type: str) -> DecoratorType:
    """
    Register a builder for a specific AST token type.

    Args:
        token_type: The GenericToken type string that this builder handles.

    Returns:
        A decorator that registers the function in BUILDER_REGISTRY.

    """

    def decorator(func: BuilderFunc) -> BuilderFunc:
        """Register the builder function."""
        BUILDER_REGISTRY[token_type] = func
        return func

    return decorator
