import typing
from pathlib import Path

from borb.pdf import Document
from borb.pdf import PDF
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf import OrderedList
from borb.pdf import TextField

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
    Decimal(630),  # x: 0 + page_margin
    Decimal(620),  # y: page_height - page_margin - height_of_textbox
    Decimal(243),  # width: page_width - 2 * page_margin
    Decimal(154),  # height
)

# Paint Table!!! containing the BUYER address data
# Table should have NO BORDER
send_to = (
    OrderedList()   # We need to change this to be a table...
    .add(TextField(field_name="send_to_name", value="Michael Phillips"))
    .add(TextField(field_name="send_to_address", value="3080 Colorado Blvd"))
    .add(TextField(field_name="send_to_city_state", value="Denver, CO 80207"))
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


