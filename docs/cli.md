# CLI

Command-line interface for amail-md.

---

## Installation

The CLI is an optional extra. Install it with:

```bash
pip install amail-md[cli]
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add amail-md --optional cli
```

---

## Commands

### `amail-md lint`

Validate a Markdown email template and show errors.

```bash
amail-md lint <file>
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `file` | Markdown file to validate (or `-` for stdin) |

**Examples:**

```bash
# Lint a file
amail-md lint bienvenida.md

# Lint from stdin
echo "# Hello" | amail-md lint -

# Lint multiple files
amail-md lint emails/*.md
```

**Output:**

```
✓ no errors found
```

Or with errors:

```
✗ 2 error(s) found

  Line 5: [BUTTON_RELATIVE_URL] Button 'Click' uses relative URL: /page
    → Use an absolute URL: https://example.com/page

  Line 8: [IMAGE_MISSING_ALT] Image is missing alt text
    → Add description for accessibility
```

**Exit codes:**

| Code | Meaning |
|------|---------|
| 0 | No errors found |
| 1 | Errors found |
| 2 | Usage error (file not found, etc.) |

---

### `amail-md render`

Convert a Markdown email template to HTML.

```bash
amail-md render <file> [options]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `file` | Markdown file to render (or `-` for stdin) |

**Options:**

| Flag | Description |
|------|-------------|
| `-o`, `--output` | Output file (default: stdout) |
| `--text` | Output text/plain only |
| `--html` | Output HTML only |

**Examples:**

```bash
# Render to stdout
amail-md render bienvenida.md

# Render to file
amail-md render bienvenida.md -o output.html

# Plain text only
amail-md render bienvenida.md --text

# Pipe from stdin
cat email.md | amail-md render - -o output.html
```

**Output format:**

By default, outputs HTML. With `--text`, outputs text/plain only.

---

## Configuration

The CLI reads configuration from the Markdown frontmatter, not from flags.
See [Getting Started](getting-started.md) for details.

---

## Error handling

If the Markdown has errors, `lint` shows them and exits with code 1.
`render` still produces output regardless of lint errors.
