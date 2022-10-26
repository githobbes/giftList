import typing
from pathlib import Path

from borb.pdf import Document, PDF

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

annot_list = page.get("Annots", [])
type(print(annot_list[0]))
