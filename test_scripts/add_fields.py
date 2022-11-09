import typing
from pathlib import Path

from borb.pdf import Document, PDF, TextField, Page
from borb.pdf.canvas.geometry.rectangle import Rectangle
from decimal import Decimal


def paint_to(text_field: TextField, p: Page, left: float, bottom: float, width: float, height: float):
    # floats are in inches; multiply by 72 to get proper Decimal units
    rect: Rectangle = Rectangle(
        Decimal(left * 72),
        Decimal(bottom * 72),
        Decimal(width * 72),
        Decimal(height * 72)
    )
    text_field.paint(p, rect)


# Path to blank front page
pdf_path = (
    Path.home()
    / "PycharmProjects"
    / "giftlist"
    / "data"
    / "front_no_acroforms.pdf"
)

# Use borb to open pdf_form_example.pdf
doc: typing.Optional[Document] = None
with open(str(pdf_path), "rb") as in_file_handle:
    doc = PDF.loads(in_file_handle)
page = doc.get_page(0)

# Buyer Fields
paint_to(TextField(field_name="b_acct_num"), page, 0.6647, 10.4796, 1.5, 0.25)
paint_to(TextField(field_name="b_key_code"), page, 2.9798, 10.4796, 0.6976, 0.25)
paint_to(TextField(field_name="b_name"), page, 0.275, 9.75, 3.4183, 0.25)
paint_to(TextField(field_name="b_address_1"), page, 0.275, 9.5, 3.4183, 0.25)
paint_to(TextField(field_name="b_address_2"), page, 0.275, 9.25, 3.4183, 0.25)
paint_to(TextField(field_name="b_address_3"), page, 0.275, 9, 3.4183, 0.25)
paint_to(TextField(field_name="b_address_4"), page, 0.275, 8.75, 3.4183, 0.25)

for i in range(5):
    recip = f"r{i+1}_"
    paint_to(TextField(field_name=f"{recip}name"), page, 0.275, 7.5 - i * 1.485, 2.1, 0.19)
    paint_to(TextField(field_name=f"{recip}address_1"), page, 0.275, 7.31 - i * 1.485, 2.1, 0.19)
    paint_to(TextField(field_name=f"{recip}address_2"), page, 0.275, 7.12 - i * 1.485, 2.1, 0.19)
    paint_to(TextField(field_name=f"{recip}acct_num"), page, 2.65, 7.5 - i * 1.485, 1.05, 0.19)
    paint_to(TextField(field_name=f"{recip}item_desc"), page, 0.275, 6.7985 - i * 1.485, 2.1, 0.19)
    paint_to(TextField(field_name=f"{recip}greeting_1"), page, 0.275, 6.6085 - i * 1.485, 2.1, 0.19)
    paint_to(TextField(field_name=f"{recip}greeting_2"), page, 0.275, 6.4185 - i * 1.485, 2.1, 0.19)
    paint_to(TextField(field_name=f"{recip}greeting_3"), page, 0.275, 6.2285 - i * 1.485, 2.1, 0.19)

output_path = (
    Path.home()
    / "PycharmProjects"
    / "giftlist"
    / "data"
    / "buyer_page.pdf"
)
with open(str(output_path), "wb") as pdf_file_handle:
    PDF.dumps(pdf_file_handle, doc)


