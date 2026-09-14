# Examples

## Simple Email

```python
from amail_md import markdown_to_email_html

md = """
---
subject: Welcome!
---

# Welcome to Our Service

Thanks for signing up. Here's what you need to know:

- **Step 1**: Verify your email
- **Step 2**: Complete your profile
- **Step 3**: Start creating

[Get Started](https://example.com/start)
"""

result = markdown_to_email_html(md)
```

## With Buttons

```markdown
---
subject: Launch Announcement
---

# We Just Launched!

Try our new product today.

{{button text="Learn More" href="https://example.com" variant="primary"}}
```

## Multi-Column Layout

```markdown
---
subject: Monthly Digest
---

{{columns}}

{{column}}

### Left Side

Content for the left column.

{{/column}}

{{column}}

### Right Side

Content for the right column.

{{/column}}

{{/columns}}
```

## Custom Theme

```python
from amail_md import markdown_to_email_html

md = """
---
subject: Branded Email
theme:
  primary_color: "#1a73e8"
  secondary_color: "#ea4335"
  font_family: "Roboto, sans-serif"
  content_width: 600
---

# Branded Content

This email uses a custom theme.
"""

result = markdown_to_email_html(md)
```

## With Plaintext Fallback

```python
from amail_md import markdown_to_email_html

result = markdown_to_email_html("# Hello\n\nWorld")

# Use both in your email client
email_body = result.html
email_text = result.text
```
