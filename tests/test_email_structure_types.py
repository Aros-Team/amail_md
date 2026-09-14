"""
Tests for EmailStructure types.

These tests define the contract for the 13 basic EmailStructure types.
They should FAIL until the types are implemented (test-first workflow).

Test naming: test_<unit>_<behavior>_<condition>.
AAA pattern: Arrange → Act → Assert.
"""

# ─── Paragraph ────────────────────────────────────────────────────────────────


class TestParagraph:
    """Tests for Paragraph email structure type."""

    def test_paragraph_can_be_imported(self) -> None:
        """Paragraph must be importable from email_structure."""
        from amail_md.email_structure import Paragraph

        # Verify it's a class that can be instantiated
        assert callable(Paragraph)

    def test_paragraph_inherits_from_email_structure(self) -> None:
        """Paragraph must inherit from EmailStructure base class."""
        from amail_md.email_structure import EmailStructure, Paragraph

        assert issubclass(Paragraph, EmailStructure)

    def test_paragraph_has_text_field(self) -> None:
        """Paragraph must accept a text field."""
        from amail_md.email_structure import Paragraph

        p = Paragraph(text="Hello world")
        assert p.text == "Hello world"

    def test_paragraph_text_is_string(self) -> None:
        """Paragraph must preserve text content as-is."""
        from amail_md.email_structure import Paragraph

        p = Paragraph(text="Test content")
        assert p.text == "Test content"

    def test_paragraph_with_inline_markdown(self) -> None:
        """Paragraph must support inline Markdown content."""
        from amail_md.email_structure import Paragraph

        p = Paragraph(text="**bold** and *italic*")
        assert p.text == "**bold** and *italic*"


# ─── Heading ──────────────────────────────────────────────────────────────────


class TestHeading:
    """Tests for Heading email structure type."""

    def test_heading_can_be_imported(self) -> None:
        """Heading must be importable from email_structure."""
        from amail_md.email_structure import Heading

        assert callable(Heading)

    def test_heading_inherits_from_email_structure(self) -> None:
        """Heading must inherit from EmailStructure base class."""
        from amail_md.email_structure import EmailStructure, Heading

        assert issubclass(Heading, EmailStructure)

    def test_heading_has_level_and_text(self) -> None:
        """Heading must accept level and text fields."""
        from amail_md.email_structure import Heading

        h = Heading(level=1, text="Title")
        assert h.level == 1
        assert h.text == "Title"

    def test_heading_level_range(self) -> None:
        """Heading.level must accept values 1-6."""
        from amail_md.email_structure import Heading

        for level in range(1, 7):
            h = Heading(level=level, text=f"H{level}")
            assert h.level == level

    def test_heading_text_is_string(self) -> None:
        """Heading must preserve text content as-is."""
        from amail_md.email_structure import Heading

        h = Heading(level=2, text="Subtitle text")
        assert h.text == "Subtitle text"


# ─── Button ───────────────────────────────────────────────────────────────────


class TestButton:
    """Tests for Button email structure type."""

    def test_button_can_be_imported(self) -> None:
        """Button must be importable from email_structure."""
        from amail_md.email_structure import Button

        assert callable(Button)

    def test_button_inherits_from_email_structure(self) -> None:
        """Button must inherit from EmailStructure base class."""
        from amail_md.email_structure import Button, EmailStructure

        assert issubclass(Button, EmailStructure)

    def test_button_has_href_and_text(self) -> None:
        """Button must accept href and text fields."""
        from amail_md.email_structure import Button

        b = Button(href="https://example.com", text="Click me")
        assert b.href == "https://example.com"
        assert b.text == "Click me"

    def test_button_default_variant_is_primary(self) -> None:
        """Button.variant must default to 'primary'."""
        from amail_md.email_structure import Button

        b = Button(href="https://example.com", text="Click")
        assert b.variant == "primary"

    def test_button_accepts_variant(self) -> None:
        """Button must accept variant parameter."""
        from amail_md.email_structure import Button

        b = Button(href="https://example.com", text="Click", variant="secondary")
        assert b.variant == "secondary"

    def test_button_accepts_color(self) -> None:
        """Button must accept optional color parameter."""
        from amail_md.email_structure import Button

        b = Button(href="https://example.com", text="Click", color="#ff0000")
        assert b.color == "#ff0000"

    def test_button_color_defaults_to_none(self) -> None:
        """Button.color must default to None."""
        from amail_md.email_structure import Button

        b = Button(href="https://example.com", text="Click")
        assert b.color is None

    def test_button_accepts_width(self) -> None:
        """Button must accept optional width parameter."""
        from amail_md.email_structure import Button

        b = Button(href="https://example.com", text="Click", width="full")
        assert b.width == "full"

    def test_button_accepts_border_radius(self) -> None:
        """Button must accept border_radius parameter."""
        from amail_md.email_structure import Button

        b = Button(href="https://example.com", text="Click", border_radius="16px")
        assert b.border_radius == "16px"

    def test_button_border_radius_default(self) -> None:
        """Button.border_radius must default to '8px'."""
        from amail_md.email_structure import Button

        b = Button(href="https://example.com", text="Click")
        assert b.border_radius == "8px"


# ─── List ─────────────────────────────────────────────────────────────────────


class TestList:
    """Tests for List email structure type."""

    def test_list_can_be_imported(self) -> None:
        """List must be importable from email_structure."""
        from amail_md.email_structure import List

        assert callable(List)

    def test_list_inherits_from_email_structure(self) -> None:
        """List must inherit from EmailStructure base class."""
        from amail_md.email_structure import EmailStructure, List

        assert issubclass(List, EmailStructure)

    def test_list_has_items(self) -> None:
        """List must accept items field."""
        from amail_md.email_structure import List

        lst = List(items=["a", "b", "c"])
        assert lst.items == ["a", "b", "c"]

    def test_list_items_is_list_of_strings(self) -> None:
        """List must preserve items as list of strings."""
        from amail_md.email_structure import List

        lst = List(items=["one", "two", "three"])
        assert lst.items == ["one", "two", "three"]

    def test_list_ordered_defaults_to_false(self) -> None:
        """List.ordered must default to False (unordered list)."""
        from amail_md.email_structure import List

        lst = List(items=["a", "b"])
        assert lst.ordered is False

    def test_list_accepts_ordered(self) -> None:
        """List must accept ordered parameter."""
        from amail_md.email_structure import List

        lst = List(items=["1", "2", "3"], ordered=True)
        assert lst.ordered is True

    def test_list_can_be_empty(self) -> None:
        """List must accept empty items list."""
        from amail_md.email_structure import List

        lst = List(items=[])
        assert lst.items == []


# ─── Quote ────────────────────────────────────────────────────────────────────


class TestQuote:
    """Tests for Quote email structure type."""

    def test_quote_can_be_imported(self) -> None:
        """Quote must be importable from email_structure."""
        from amail_md.email_structure import Quote

        assert callable(Quote)

    def test_quote_inherits_from_email_structure(self) -> None:
        """Quote must inherit from EmailStructure base class."""
        from amail_md.email_structure import EmailStructure, Quote

        assert issubclass(Quote, EmailStructure)

    def test_quote_has_text(self) -> None:
        """Quote must accept text field."""
        from amail_md.email_structure import Quote

        q = Quote(text="The best way to predict the future is to create it.")
        assert q.text == "The best way to predict the future is to create it."

    def test_quote_text_is_string(self) -> None:
        """Quote must preserve text content as-is."""
        from amail_md.email_structure import Quote

        q = Quote(text="Test quote content")
        assert q.text == "Test quote content"


# ─── Image ────────────────────────────────────────────────────────────────────


class TestImage:
    """Tests for Image email structure type."""

    def test_image_can_be_imported(self) -> None:
        """Image must be importable from email_structure."""
        from amail_md.email_structure import Image

        assert callable(Image)

    def test_image_inherits_from_email_structure(self) -> None:
        """Image must inherit from EmailStructure base class."""
        from amail_md.email_structure import EmailStructure, Image

        assert issubclass(Image, EmailStructure)

    def test_image_has_src(self) -> None:
        """Image must accept src field."""
        from amail_md.email_structure import Image

        img = Image(src="https://example.com/photo.jpg")
        assert img.src == "https://example.com/photo.jpg"

    def test_image_alt_defaults_to_empty(self) -> None:
        """Image.alt must default to empty string."""
        from amail_md.email_structure import Image

        img = Image(src="https://example.com/photo.jpg")
        assert img.alt == ""

    def test_image_accepts_alt(self) -> None:
        """Image must accept alt parameter."""
        from amail_md.email_structure import Image

        img = Image(src="https://example.com/photo.jpg", alt="A photo")
        assert img.alt == "A photo"

    def test_image_accepts_width(self) -> None:
        """Image must accept optional width parameter."""
        from amail_md.email_structure import Image

        img = Image(src="https://example.com/photo.jpg", width="400")
        assert img.width == "400"

    def test_image_accepts_height(self) -> None:
        """Image must accept optional height parameter."""
        from amail_md.email_structure import Image

        img = Image(src="https://example.com/photo.jpg", height="300")
        assert img.height == "300"

    def test_image_alignment_defaults_to_center(self) -> None:
        """Image.alignment must default to 'center'."""
        from amail_md.email_structure import Image

        img = Image(src="https://example.com/photo.jpg")
        assert img.alignment == "center"

    def test_image_accepts_alignment(self) -> None:
        """Image must accept alignment parameter."""
        from amail_md.email_structure import Image

        img = Image(src="https://example.com/photo.jpg", alignment="left")
        assert img.alignment == "left"

    def test_image_accepts_border_radius(self) -> None:
        """Image must accept optional border_radius parameter."""
        from amail_md.email_structure import Image

        img = Image(src="https://example.com/photo.jpg", border_radius="50%")
        assert img.border_radius == "50%"


# ─── Divider ──────────────────────────────────────────────────────────────────


class TestDivider:
    """Tests for Divider email structure type."""

    def test_divider_can_be_imported(self) -> None:
        """Divider must be importable from email_structure."""
        from amail_md.email_structure import Divider

        assert callable(Divider)

    def test_divider_inherits_from_email_structure(self) -> None:
        """Divider must inherit from EmailStructure base class."""
        from amail_md.email_structure import Divider, EmailStructure

        assert issubclass(Divider, EmailStructure)

    def test_divider_can_be_instantiated(self) -> None:
        """Divider must be instantiable with no arguments."""
        from amail_md.email_structure import Divider

        d = Divider()
        # Verify it's a Divider instance (not just not None)
        assert type(d).__name__ == "Divider"


# ─── Spacer ───────────────────────────────────────────────────────────────────


class TestSpacer:
    """Tests for Spacer email structure type."""

    def test_spacer_can_be_imported(self) -> None:
        """Spacer must be importable from email_structure."""
        from amail_md.email_structure import Spacer

        assert callable(Spacer)

    def test_spacer_inherits_from_email_structure(self) -> None:
        """Spacer must inherit from EmailStructure base class."""
        from amail_md.email_structure import EmailStructure, Spacer

        assert issubclass(Spacer, EmailStructure)

    def test_spacer_height_defaults_to_24px(self) -> None:
        """Spacer.height must default to '24px'."""
        from amail_md.email_structure import Spacer

        s = Spacer()
        assert s.height == "24px"

    def test_spacer_accepts_height(self) -> None:
        """Spacer must accept height parameter."""
        from amail_md.email_structure import Spacer

        s = Spacer(height="48px")
        assert s.height == "48px"


# ─── Columns ──────────────────────────────────────────────────────────────────


class TestColumns:
    """Tests for Columns email structure type."""

    def test_columns_can_be_imported(self) -> None:
        """Columns must be importable from email_structure."""
        from amail_md.email_structure import Columns

        assert callable(Columns)

    def test_columns_inherits_from_email_structure(self) -> None:
        """Columns must inherit from EmailStructure base class."""
        from amail_md.email_structure import Columns, EmailStructure

        assert issubclass(Columns, EmailStructure)

    def test_columns_has_columns_field(self) -> None:
        """Columns must accept columns field."""
        from amail_md.email_structure import ColumnCell, Columns

        col = ColumnCell(children=[])
        c = Columns(columns=[col])
        assert len(c.columns) == 1

    def test_columns_gap_defaults_to_16px(self) -> None:
        """Columns.gap must default to '16px'."""
        from amail_md.email_structure import ColumnCell, Columns

        col = ColumnCell(children=[])
        c = Columns(columns=[col])
        assert c.gap == "16px"

    def test_columns_accepts_gap(self) -> None:
        """Columns must accept gap parameter."""
        from amail_md.email_structure import ColumnCell, Columns

        col = ColumnCell(children=[])
        c = Columns(columns=[col], gap="24px")
        assert c.gap == "24px"

    def test_columns_can_be_empty(self) -> None:
        """Columns must accept empty columns list."""
        from amail_md.email_structure import Columns

        c = Columns(columns=[])
        assert c.columns == []


# ─── ColumnCell ───────────────────────────────────────────────────────────────


class TestColumnCell:
    """Tests for ColumnCell email structure type."""

    def test_column_cell_can_be_imported(self) -> None:
        """ColumnCell must be importable from email_structure."""
        from amail_md.email_structure import ColumnCell

        assert callable(ColumnCell)

    def test_column_cell_inherits_from_email_structure(self) -> None:
        """ColumnCell must inherit from EmailStructure base class."""
        from amail_md.email_structure import ColumnCell, EmailStructure

        assert issubclass(ColumnCell, EmailStructure)

    def test_column_cell_has_children(self) -> None:
        """ColumnCell must accept children field."""
        from amail_md.email_structure import ColumnCell, Paragraph

        cell = ColumnCell(children=[Paragraph(text="Hello")])
        assert len(cell.children) == 1

    def test_column_cell_children_is_list(self) -> None:
        """ColumnCell.children must be a list."""
        from amail_md.email_structure import ColumnCell

        cell = ColumnCell(children=[])
        assert isinstance(cell.children, list)

    def test_column_cell_can_be_empty(self) -> None:
        """ColumnCell must accept empty children list."""
        from amail_md.email_structure import ColumnCell

        cell = ColumnCell(children=[])
        assert cell.children == []


# ─── Table ────────────────────────────────────────────────────────────────────


class TestTable:
    """Tests for Table email structure type."""

    def test_table_can_be_imported(self) -> None:
        """Table must be importable from email_structure."""
        from amail_md.email_structure import Table

        assert callable(Table)

    def test_table_inherits_from_email_structure(self) -> None:
        """Table must inherit from EmailStructure base class."""
        from amail_md.email_structure import EmailStructure, Table

        assert issubclass(Table, EmailStructure)

    def test_table_has_headers_and_rows(self) -> None:
        """Table must accept headers and rows fields."""
        from amail_md.email_structure import Table

        t = Table(headers=["Name", "Role"], rows=[["Alice", "Dev"], ["Bob", "Design"]])
        assert t.headers == ["Name", "Role"]
        assert len(t.rows) == 2

    def test_table_headers_is_list_of_strings(self) -> None:
        """Table must preserve headers as list of strings."""
        from amail_md.email_structure import Table

        t = Table(headers=["Alpha", "Beta"], rows=[])
        assert t.headers == ["Alpha", "Beta"]

    def test_table_rows_is_list_of_lists(self) -> None:
        """Table must preserve rows as list of lists."""
        from amail_md.email_structure import Table

        t = Table(headers=["X"], rows=[["row1"], ["row2"]])
        assert t.rows == [["row1"], ["row2"]]

    def test_table_alignment_defaults_to_none(self) -> None:
        """Table.alignment must default to None."""
        from amail_md.email_structure import Table

        t = Table(headers=["A"], rows=[])
        assert t.alignment is None

    def test_table_accepts_alignment(self) -> None:
        """Table must accept alignment parameter."""
        from amail_md.email_structure import Table

        t = Table(headers=["A", "B"], rows=[], alignment=["left", "right"])
        assert t.alignment == ["left", "right"]

    def test_table_can_be_empty(self) -> None:
        """Table must accept empty headers and rows."""
        from amail_md.email_structure import Table

        t = Table(headers=[], rows=[])
        assert t.headers == []
        assert t.rows == []


# ─── Code ─────────────────────────────────────────────────────────────────────


class TestCode:
    """Tests for Code email structure type."""

    def test_code_can_be_imported(self) -> None:
        """Code must be importable from email_structure."""
        from amail_md.email_structure import Code

        assert callable(Code)

    def test_code_inherits_from_email_structure(self) -> None:
        """Code must inherit from EmailStructure base class."""
        from amail_md.email_structure import Code, EmailStructure

        assert issubclass(Code, EmailStructure)

    def test_code_has_code_field(self) -> None:
        """Code must accept code field."""
        from amail_md.email_structure import Code

        c = Code(code="print('hello')")
        assert c.code == "print('hello')"

    def test_code_language_defaults_to_none(self) -> None:
        """Code.language must default to None."""
        from amail_md.email_structure import Code

        c = Code(code="x = 1")
        assert c.language is None

    def test_code_accepts_language(self) -> None:
        """Code must accept language parameter."""
        from amail_md.email_structure import Code

        c = Code(code="def foo(): pass", language="python")
        assert c.language == "python"

    def test_code_code_is_string(self) -> None:
        """Code must preserve code content as-is."""
        from amail_md.email_structure import Code

        c = Code(code="x = 42")
        assert c.code == "x = 42"


# ─── Link ─────────────────────────────────────────────────────────────────────


class TestLink:
    """Tests for Link email structure type."""

    def test_link_can_be_imported(self) -> None:
        """Link must be importable from email_structure."""
        from amail_md.email_structure import Link

        assert callable(Link)

    def test_link_inherits_from_email_structure(self) -> None:
        """Link must inherit from EmailStructure base class."""
        from amail_md.email_structure import EmailStructure, Link

        assert issubclass(Link, EmailStructure)

    def test_link_has_href_and_text(self) -> None:
        """Link must accept href and text fields."""
        from amail_md.email_structure import Link

        link = Link(href="https://example.com", text="Click here")
        assert link.href == "https://example.com"
        assert link.text == "Click here"

    def test_link_href_is_string(self) -> None:
        """Link must preserve href content as-is."""
        from amail_md.email_structure import Link

        link = Link(href="https://example.com", text="Test")
        assert link.href == "https://example.com"

    def test_link_text_is_string(self) -> None:
        """Link must preserve text content as-is."""
        from amail_md.email_structure import Link

        link = Link(href="https://example.com", text="Test content")
        assert link.text == "Test content"
