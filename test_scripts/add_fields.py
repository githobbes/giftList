import typing
from pathlib import Path

from borb.pdf import Document, PDF, TextField, Page
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.io.read.types import Dictionary, List, Name, Stream, String

from decimal import Decimal


def paint_to(text_field: TextField, p: Page, left: float, bottom: float, width: float):
    # floats are in inches; multiply by 72 to get proper Decimal units
    rect: Rectangle = Rectangle(
        Decimal(left * 72),
        Decimal(bottom * 72),
        Decimal(width * 72),
        Decimal(0.1333 * 72)
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
paint_to(TextField(field_name="b_acct_num", font_size=Decimal(8)), page, 0.6647, 10.5129, 1.5)
paint_to(TextField(field_name="b_key_code", font_size=Decimal(8)), page, 2.9798, 10.5129, 0.6976)
paint_to(TextField(field_name="b_name", font_size=Decimal(8)), page, 0.275, 9.4222, 3.4183)
paint_to(TextField(field_name="b_address_1", font_size=Decimal(8)), page, 0.275, 9.2889, 3.4183)
paint_to(TextField(field_name="b_address_2", font_size=Decimal(8)), page, 0.275, 9.1556, 3.4183)
paint_to(TextField(field_name="b_address_3", font_size=Decimal(8)), page, 0.275, 9.0223, 3.4183)
paint_to(TextField(field_name="b_address_4", font_size=Decimal(8)), page, 0.275, 8.889, 3.4183)

for i in range(5):
    r = f"r{i + 1}_"
    paint_to(TextField(field_name=f"{r}name", font_size=Decimal(8)), page, 0.275, 7.55 - i * 1.485, 2.1)
    paint_to(TextField(field_name=f"{r}address_1", font_size=Decimal(8)), page, 0.275, 7.4167 - i * 1.485, 2.1)
    paint_to(TextField(field_name=f"{r}address_2", font_size=Decimal(8)), page, 0.275, 7.2834 - i * 1.485, 2.1)
    paint_to(TextField(field_name=f"{r}acct_num", font_size=Decimal(8)), page, 2.65, 7.55 - i * 1.485, 1.05)
    paint_to(TextField(field_name=f"{r}item_desc", font_size=Decimal(8)), page, 0.275, 6.75 - i * 1.485, 3.42)
    paint_to(TextField(field_name=f"{r}greeting_1", font_size=Decimal(8)), page, 0.275, 6.6167 - i * 1.485, 3.42)
    paint_to(TextField(field_name=f"{r}greeting_2", font_size=Decimal(8)), page, 0.275, 6.4834 - i * 1.485, 3.42)
    paint_to(TextField(field_name=f"{r}greeting_3", font_size=Decimal(8)), page, 0.275, 6.3501 - i * 1.485, 3.42)


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
    paint_to(TextField(field_name=f"{r}name", font_size=Decimal(8)), page, 0.275, 9.77 - i * 1.607, 2.1)
    paint_to(TextField(field_name=f"{r}address_1", font_size=Decimal(8)), page, 0.275, 9.6367 - i * 1.607, 2.1)
    paint_to(TextField(field_name=f"{r}address_2", font_size=Decimal(8)), page, 0.275, 9.5034 - i * 1.607, 2.1)
    paint_to(TextField(field_name=f"{r}acct_num", font_size=Decimal(8)), page, 2.65, 9.77 - i * 1.607, 1.05)
    paint_to(TextField(field_name=f"{r}item_desc", font_size=Decimal(8)), page, 0.275, 8.97 - i * 1.607, 3.42)
    paint_to(TextField(field_name=f"{r}greeting_1", font_size=Decimal(8)), page, 0.275, 8.8367 - i * 1.607, 3.42)
    paint_to(TextField(field_name=f"{r}greeting_2", font_size=Decimal(8)), page, 0.275, 8.7034 - i * 1.607, 3.42)
    paint_to(TextField(field_name=f"{r}greeting_3", font_size=Decimal(8)), page, 0.275, 8.5701 - i * 1.607, 3.42)

output_path = (
    Path.home()
    / "PycharmProjects"
    / "giftlist"
    / "data"
    / "output_1.pdf"
)
with open(str(output_path), "wb") as pdf_file_handle:
    PDF.dumps(pdf_file_handle, doc)

