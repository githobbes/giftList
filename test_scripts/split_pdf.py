from PyPDF2 import PdfFileReader, PdfFileWriter
from pathlib import Path

pdf_path = (
    Path.home()
    / "PycharmProjects"
    / "giftlist"
    / "test_scripts"
    / "Blank PDFs.pdf"
)

pdf_savepath = (
    Path.home()
    / "PycharmProjects"
    / "giftlist"
    / "test_scripts"
)

my_doc = PdfFileReader(str(pdf_path))
for i in range(my_doc.getNumPages()):
    new_doc = PdfFileWriter()
    new_doc.addPage(my_doc.getPage(i))
    new_path = f"{str(pdf_savepath)}\\sample_page_{i}.pdf"
    with Path(new_path).open(mode="wb") as output_file:
        new_doc.write(output_file)

