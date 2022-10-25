import typing
from pathlib import Path

from borb.pdf import Document
from borb.pdf import PDF
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf import OrderedList
from borb.pdf import TextField, Paragraph, TextArea
from borb.pdf import FlexibleColumnWidthTable, FixedColumnWidthTable, TableCell

from decimal import Decimal

### Adding fields to front page!

# Path to blank front page
pdf_path = (
    Path.home()
    / "PycharmProjects"
    / "giftlist"
    / "test_scripts"
    / "sample_page_0.pdf"
)

# Use borb to open pdf_form_example.pdf
doc: typing.Optional[Document] = None
with open(str(pdf_path), "rb") as in_file_handle:
    doc = PDF.loads(in_file_handle)
page = doc.get_page(0)


# Add Rectangle in Main Address box:
r: Rectangle = Rectangle(
    Decimal(635),  # left side
    Decimal(620),  # bottom
    Decimal(240),  # width
    Decimal(150),  # height
)

# Table with Account Number and Key Code (Top line of Buyer Address Box)
send_to = (
    FlexibleColumnWidthTable(number_of_columns=4, number_of_rows=1)
    .add(Paragraph("Acct: ", font_size=Decimal(10)))
    .add(TextField(field_name="b_acct_number", value="1234567890##", font_size=Decimal(10)))
    .add(Paragraph("Key Code: ", font_size=Decimal(10)))
    .add(TextField(field_name="b_key_code", value="12345", font_size=Decimal(10)))
    .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
    .no_borders()
)
send_to._content[3]._preferred_width = Decimal(10)
send_to.paint(page, r)

r: Rectangle = Rectangle(
    Decimal(635),
    Decimal(620),
    Decimal(240),
    Decimal(100),
)

# Table with Buyer's address details
send_to = (
    FixedColumnWidthTable(number_of_columns=1, number_of_rows=1)
    .add(TextArea(field_name='b_address_box', number_of_lines=4, padding_top=Decimal(2), padding_bottom=Decimal(2)))
)
send_to.paint(page, r)

output_path = (
    Path.home()
    / "PycharmProjects"
    / "giftlist"
    / "test_scripts"
    / "output.pdf"
)
with open(str(output_path), "wb") as pdf_file_handle:
    PDF.dumps(pdf_file_handle, doc)


