#!chapter_004/src/snippet_012.py
from decimal import Decimal

from borb.pdf import HexColor
from borb.pdf import CountryDropDownList
from borb.pdf import TextField
from borb.pdf import SingleColumnLayout
from borb.pdf import PageLayout
from borb.pdf import FixedColumnWidthTable
from borb.pdf import Paragraph
from borb.pdf import Document
from borb.pdf import Page
from borb.pdf import PDF
from borb.pdf import JavaScriptPushButton
from borb.pdf import Alignment


# create Document
doc: Document = Document()

# create Page
page: Page = Page()

# add Page to Document
doc.add_page(page)

# set a PageLayout
layout: PageLayout = SingleColumnLayout(page)

# add FixedColumnWidthTable containing Paragraph and TextField objects
layout.add(
    FixedColumnWidthTable(number_of_columns=2, number_of_rows=4)
    .add(Paragraph("Name:"))
    .add(TextField(field_name="name", font_color=HexColor("f1cd2e")))
    .add(Paragraph("Firstname:"))
    .add(TextField(field_name="firstname", font_color=HexColor("f1cd2e")))
    .add(Paragraph("Country"))
    .add(CountryDropDownList(field_name="country"))
    .add(Paragraph(" "))
    .add(
        JavaScriptPushButton(
            text="Set",
            javascript="this.getField('name').value = 'Schellekens';",
            horizontal_alignment=Alignment.RIGHT,
        )
    )
    .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    .no_borders()
)

# store
with open("output.pdf", "wb") as pdf_file_handle:
    PDF.dumps(pdf_file_handle, doc)
