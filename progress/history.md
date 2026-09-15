# Session History

> Append-only log of completed sessions/activities.

---

## Session: Architecture Definition (2026-09-14)

### Summary
Defined complete project architecture patterns, folder structure, and design decisions.

### Activities Completed
- **CLI (typer)**: Docs + tests created (RED phase)
- **Linter (verify_markdown)**: Docs + tests created (RED phase)
- **Architecture**: Full architecture documented

### Key Decisions
1. **3-file pattern** for EmailStructure elements (Model + Builder + MJML Node)
2. **Registry pattern** for MJML compilation (1:1 relationship)
3. **Rule Engine pattern** for linter (1:N relationship)
4. **Registry pattern** for segmenter (1:1 relationship)
5. **Generic Token** for parser independence

### ADRs Created
- ADR-007: MJML Compilation via Registry Pattern
- ADR-008: Linter Rule Engine Pattern
- ADR-009: Segmenter Registry Pattern
- ADR-010: Generic Token for Parser Independence

### Dependencies Added
- `mdit-py-plugins>=0.6.1` (attrs, container, frontmatter, tasklists)

### Diagrams Updated
- C4_Container.puml
- C4_Component.puml
- Sequence_Pipelines.puml

### Commits
- `83c56e2` — feat: define project architecture patterns

### Next Steps
- GREEN phase: Implement modules to pass tests
- Start with `core/models/email_structure/` (dataclasses)
- Then `core/services/segmenter/` (builders)
- Then `infrastructure/adapters/mjml/` (nodes)

---

## Session: EmailStructure Implementation (2026-09-15)

### Summary
Implemented all 13 EmailStructure types with full pipeline: markdown → AST → EmailStructure → MJML → HTML.

### Activities Completed
- **Tests de builders y MJML nodes**: 22 test files created (RED phase)
- **Implementar 11 tipos restantes**: All 11 types implemented in 4 batches

### Implementation Details

| Batch | Types | Status |
|-------|-------|--------|
| 1 | Paragraph, Heading, Divider, Spacer | ✅ GREEN |
| 2 | Image, Code, Link, Quote | ✅ GREEN |
| 3 | List, Table | ✅ GREEN |
| 4 | Columns, ColumnCell | ✅ GREEN |

### Architecture Decisions
1. **Button builder** registers for `link_open` and always returns Button
2. **Link builder** provides `build_link()` but doesn't register in registry
3. **GenericToken** gained `info` field for fence tokens (language)
4. **List/Table builders** use flat child walking (matching test token structure)
5. **EmailStructure** is plain base class, not ABC (per ADR-007)

### Files Created (50 files)
- 12 dataclasses in `core/models/email_structure/`
- 12 builders in `core/services/segmenter/builders/`
- 12 MJML nodes in `infrastructure/adapters/mjml/nodes/`
- Updated `__init__.py` exports

### Verification
- 287/287 tests GREEN
- Ruff check ✅ | Ruff format ✅ | MyPy ✅
- Harness all green

### Commits
- `0abb167` — feat: add tests for 11 remaining EmailStructure types (RED phase)
- `074941e` — feat: implement all 11 remaining EmailStructure types (Activity 2)

### Key Learnings
- Test token structure uses flat children (siblings), not nested
- Button/Link share `link_open` token type — Button builder handles all
- `mrml.to_html()` returns Output object, must use `.content` attribute
- `attrs_plugin` produces `class` attribute, not `button` key
