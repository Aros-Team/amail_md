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
Lint rules: auto-discovery and ACTIVE_RULES list.

Each rule is a function ``check(elements) -> list[ValidationError]``.
Add new rules by creating a file in ``rules/`` and appending to
``ACTIVE_RULES``.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from amail_md.core.models.lint.errors import ValidationError

from .no_empty_urls import check as _check_no_empty_urls
from .relative_urls import check as _check_relative_urls

ACTIVE_RULES: list[Callable[[Any], list[ValidationError]]] = [
    _check_no_empty_urls,
    _check_relative_urls,
]
