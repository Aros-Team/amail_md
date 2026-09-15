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

"""MjmlCompiler port: compiles MJML to HTML."""

from typing import Protocol


class MjmlCompiler(Protocol):
    """
    Protocol for MJML compilers.

    Implementations must compile MJML documents to email-safe HTML.
    """

    def compile(self, mjml: str) -> str:
        """
        Compile MJML to HTML.

        Args:
            mjml: MJML document string.

        Returns:
            Email-safe HTML string.

        """
        ...
