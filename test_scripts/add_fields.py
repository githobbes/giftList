import typing
from pathlib import Path

from borb.pdf import Document, PDF, TextField, Page
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.io.read.types import Dictionary, List, Name, Stream, String

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
paint_to(TextField(field_name="b_acct_num", font_size=Decimal(8)), page, 0.6647, 10.4796, 1.5, 0.25)
paint_to(TextField(field_name="b_key_code", font_size=Decimal(8)), page, 2.9798, 10.4796, 0.6976, 0.25)
paint_to(TextField(field_name="b_name", font_size=Decimal(8)), page, 0.275, 9.75, 3.4183, 0.25)
paint_to(TextField(field_name="b_address_1", font_size=Decimal(8)), page, 0.275, 9.5, 3.4183, 0.25)
paint_to(TextField(field_name="b_address_2", font_size=Decimal(8)), page, 0.275, 9.25, 3.4183, 0.25)
paint_to(TextField(field_name="b_address_3", font_size=Decimal(8)), page, 0.275, 9, 3.4183, 0.25)
paint_to(TextField(field_name="b_address_4", font_size=Decimal(8)), page, 0.275, 8.75, 3.4183, 0.25)

for i in range(5):
    r = f"r{i + 1}_"
    paint_to(TextField(field_name=f"{r}name", font_size=Decimal(8)), page, 0.275, 7.5 - i * 1.485, 2.1, 0.19)
    paint_to(TextField(field_name=f"{r}address_1", font_size=Decimal(8)), page, 0.275, 7.31 - i * 1.485, 2.1, 0.19)
    paint_to(TextField(field_name=f"{r}address_2", font_size=Decimal(8)), page, 0.275, 7.12 - i * 1.485, 2.1, 0.19)
    paint_to(TextField(field_name=f"{r}acct_num", font_size=Decimal(8)), page, 2.65, 7.5 - i * 1.485, 1.05, 0.19)
    paint_to(TextField(field_name=f"{r}item_desc", font_size=Decimal(8)), page, 0.275, 6.7985 - i * 1.485, 3.42, 0.19)
    paint_to(TextField(field_name=f"{r}greeting_1", font_size=Decimal(8)), page, 0.275, 6.6085 - i * 1.485, 3.42, 0.19)
    paint_to(TextField(field_name=f"{r}greeting_2", font_size=Decimal(8)), page, 0.275, 6.4185 - i * 1.485, 3.42, 0.19)
    paint_to(TextField(field_name=f"{r}greeting_3", font_size=Decimal(8)), page, 0.275, 6.2285 - i * 1.485, 3.42, 0.19)


output_path = (
    Path.home()
    / "PycharmProjects"
    / "giftlist"
    / "data"
    / "output.pdf"
)
with open(str(output_path), "wb") as pdf_file_handle:
    PDF.dumps(pdf_file_handle, doc)

# Note: Used Adobe Acrobat's Prepare Form tool to modify size of key_code box and MaxLen for relevant TextFields

# Path to blank front page
pdf_path = (
    Path.home()
    / "PycharmProjects"
    / "giftlist"
    / "data"
    / "middle_no_acroforms.pdf"
)

# Use borb to open pdf_form_example.pdf
doc: typing.Optional[Document] = None
with open(str(pdf_path), "rb") as in_file_handle:
    doc = PDF.loads(in_file_handle)
page = doc.get_page(0)

for i in range(6):
    r = f"r{i + 1}_"
    paint_to(TextField(field_name=f"{r}name", font_size=Decimal(8)), page, 0.275, 7.5 - i * 1.485, 2.1, 0.19)
    paint_to(TextField(field_name=f"{r}address_1", font_size=Decimal(8)), page, 0.275, 7.31 - i * 1.485, 2.1, 0.19)
    paint_to(TextField(field_name=f"{r}address_2", font_size=Decimal(8)), page, 0.275, 7.12 - i * 1.485, 2.1, 0.19)
    paint_to(TextField(field_name=f"{r}acct_num", font_size=Decimal(8)), page, 2.65, 7.5 - i * 1.485, 1.05, 0.19)
    paint_to(TextField(field_name=f"{r}item_desc", font_size=Decimal(8)), page, 0.275, 6.7985 - i * 1.485, 3.42, 0.19)
    paint_to(TextField(field_name=f"{r}greeting_1", font_size=Decimal(8)), page, 0.275, 6.6085 - i * 1.485, 3.42, 0.19)
    paint_to(TextField(field_name=f"{r}greeting_2", font_size=Decimal(8)), page, 0.275, 6.4185 - i * 1.485, 3.42, 0.19)
    paint_to(TextField(field_name=f"{r}greeting_3", font_size=Decimal(8)), page, 0.275, 6.2285 - i * 1.485, 3.42, 0.19)
