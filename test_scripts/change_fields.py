import typing
from pathlib import Path

from borb.pdf import Document, PDF
from borb.io.read.types import Dictionary, List, Name, Stream, String

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


def has_acroforms(self) -> bool:
    """
    This function returns True if this Page contains fields from an AcroForm
    :return:    True if this Page contains fields from an AcroForm, False otherwise
    """
    return (
            len(
                [
                    x
                    for x in self.get("Annots", [])
                    if "Type" in x
                       and x["Type"] == "Annot"
                       and "Subtype" in x
                       and x["Subtype"] == "Widget"
                       and "FT" in x
                       and x["FT"] in ["Btn", "Ch", "Tx"]
                ]
            )
            != 0
    )


def has_form_field(self, field_name: str) -> bool:
    """
    This function returns True if this Page contains a form field with the given name
    :param field_name:  the field_name to be queried
    :return:            True if this Page contains a form field with the given field_name
    """
    assert len(field_name) != 0
    return (
            len(
                [
                    x
                    for x in self.get("Annots", [])
                    if "Type" in x
                       and x["Type"] == "Annot"
                       and "Subtype" in x
                       and x["Subtype"] == "Widget"
                       and "FT" in x
                       and x["FT"] in ["Btn", "Ch", "Tx"]
                       and "T" in x
                       and x["T"] == field_name
                ]
            )
            != 0
    )


# Step 1: call page.get("Annots", []) to acquire list of "Annots"
form_fields = [ x for x in page.get("Annots", []) if x
                and "Type" in x
                and x["Type"] == "Annot"
                and "Subtype" in x
                and x["Subtype"] == "Widget"
                and "FT" in x
                and x["FT"] in ["Btn", "Ch", "Tx"]
                and "T" in x]


def set_form_field_value(self, field_name: str, value: str) -> "Page":
    """
    This function sets the value of the form field with the given field_name
    This function returns self
    :param field_name:  the field_name of the field being queried
    :param value:       the new value of the field
    :return:            self
    """
    field_dictionaries: typing.List[Dictionary] = [
        x
        for x in self.get("Annots", [])
        if "Type" in x
           and x["Type"] == "Annot"
           and "Subtype" in x
           and x["Subtype"] == "Widget"
           and "FT" in x
           and x["FT"] in ["Btn", "Ch", "Tx"]
           and "T" in x
           and x["T"] == field_name
    ]
    assert len(field_dictionaries) == 1
    assert "V" in field_dictionaries[0]
    field_dictionaries[0][Name("V")] = String(value)
    return self


