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
Email structure types — public re-export.

This module re-exports EmailStructure types from their canonical location
in ``core.models.email_structure`` so that downstream code can import
from ``amail_md.email_structure``.
"""

from amail_md.core.models.email_structure import Button, EmailStructure

__all__ = ["EmailStructure", "Button"]
