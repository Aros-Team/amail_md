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

"""Base class for all email structure elements."""


class EmailStructure:
    """
    Base class for all email structure elements.

    Every email piece (paragraph, heading, button, etc.) inherits from
    this class. The segmenter produces EmailStructure instances from
    the markdown-it-py AST, and the MJML adapter renders them to
    markup via the registry pattern.
    """
