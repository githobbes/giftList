from borb.pdf import Document, PDF, TextField, Page
from borb.pdf.canvas.geometry.rectangle import Rectangle

from decimal import Decimal

doc = Document()
page = Page()
doc.add_page(page)
second_page = Page()
doc.add_page(second_page)

rect = Rectangle(Decimal(72), Decimal(10*72), Decimal(72), Decimal(72))

textfield = TextField(field_name="name")
textfield.paint(page, rect)

with open("textfield_test.pdf", "wb") as pdf_file_handle:
    PDF.dumps(pdf_file_handle, doc)

with open("textfield_test.pdf", "rb") as pdf_file_handle:
    new_doc = PDF.loads(pdf_file_handle)

new_page = new_doc.get_page(0)
new_page.set_form_field_value('name', 'value')

with open("textfield_test.pdf", "wb") as pdf_file_handle:
    PDF.dumps(pdf_file_handle, new_doc)
