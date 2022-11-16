import math
import base64
from pathlib import Path
from xml.etree.ElementTree import ElementTree, Element, SubElement
from borb.pdf import Document, PDF, TextField, Page
from borb.pdf.canvas.geometry.rectangle import Rectangle
from decimal import Decimal
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError

# Defining constants
ROOT = Element('root')
BUYER_TREE = ElementTree(ROOT)

MAILCHIMP_API_KEY = 'YRxKQk091G8qZlp9FjIxtw'

PATH_TO_TEMPLATES = (Path.home() / "PycharmProjects" / "giftlist" / "data")
PATH_BUYER_PAGE = (PATH_TO_TEMPLATES / "buyer_page.pdf")
PATH_RECIPIENT_PAGE = (PATH_TO_TEMPLATES / "recipient_page.pdf")
PATH_BACK_PAGE = (PATH_TO_TEMPLATES / "details_page.pdf")
# Use borb to open pdf_form_example.pdf
with open(str(PATH_BUYER_PAGE), "rb") as file:
    BUYER_PAGE = PDF.loads(file).get_page(0)
with open(str(PATH_RECIPIENT_PAGE), "rb") as file:
    RECIPIENT_PAGE = PDF.loads(file).get_page(0)
with open(str(PATH_BACK_PAGE), "rb") as file:
    BACK_PAGE = PDF.loads(file).get_page(0)


def main_loop(input_file: str):
    #######################################################################################
    #   Main Loop for Gift Lift Process
    #       Open input_file
    #           for line in file:
    #               if (new buyer)
    #                   if data
    #                       call make_giftlist(---)
    #                       call email_giftlist(---)
    #                       call prune_xml()
    #                   fill data with Buyer data
    #               else
    #                  fill data with Recipient data
    #
    #######################################################################################
    global BUYER_TREE
    with open(input_file) as giftlist_file:
        for line in giftlist_file:
            if line[15:25] == "0000000000":  # If New Buyer
                print('New Buyer')

                # If BUYER_TREE is populated, process a new gift list
                if len(ROOT) > 0:
                    print('Processing new gift list')
                    print('--- calling make_giftlist()')
                    make_giftlist()

                    print('--- calling email_giftlist()')
                    email_giftlist()

                    print('Pruning XML Tree')
                    print('--- calling prune_xml()')
                    prune_xml()

                # Fill in new Buyer data
                print('Populating root with new Buyer data')
                print('--- calling new_buyer(buyer_line)')
                new_buyer(buyer_line=line)

            else:  # We have a new recipient
                print('New Recipient')
                print('--- calling new_recipient(recipient_line)')
                new_recipient(recipient_line=line)

        # Finished process new data - need to process last Gift List
        if len(ROOT) > 0:
            print('Processing new gift list')
            print('--- calling make_giftlist()')
            make_giftlist()

            print('--- calling e-mail_giftlist()')
            email_giftlist()

            print('Pruning XML Tree')
            print('--- calling prune_xml()')
            prune_xml()


def make_giftlist():
    print('*** making the giftlist ***')
    global PATH_TO_TEMPLATES
    global BUYER_PAGE, RECIPIENT_PAGE, BACK_PAGE
    global ROOT
    giftlist = Document()

    # Print BUYER details on FRONT_PAGE
    page = BUYER_PAGE.__deepcopy__()
    giftlist.add_page(page)
    buyer = ROOT.find('buyer')
    paint_to(TextField(field_name="b_acct_num", value=buyer.get('acct_num'), font_size=Decimal(8),
                       border_top=False, border_right=False, border_bottom=False, border_left=False),
             page, 0.6647, 10.5129, 1.5)
    paint_to(TextField(field_name="b_key_code", value=buyer.get('key_code'), font_size=Decimal(8),
                       border_top=False, border_right=False, border_bottom=False, border_left=False),
             page, 2.9798, 10.5129, 0.6976)
    paint_to(TextField(field_name="b_name", value=buyer.get('name'), font_size=Decimal(8),
                       border_top=False, border_right=False, border_bottom=False, border_left=False),
             page, 0.275, 9.4222, 3.4183)
    buyer_address = [buyer.get('company_name'),
                     buyer.get('address_1'),
                     buyer.get('address_2'),
                     f'{buyer.get("city")}, {buyer.get("state")} {buyer.get("zip")}']
    buyer_address = [x for x in buyer_address if x]
    for _ in range(len(buyer_address), 4):
        buyer_address.append('')
    for i in range(len(buyer_address)):
        paint_to(TextField(field_name=f"b_address_{i + 1}", value=buyer_address[i], font_size=Decimal(8),
                           border_top=False, border_right=False, border_bottom=False, border_left=False),
                 page, 0.275, 9.2889 - i*0.1333, 3.4183)

    # Print RECIPIENT details to FRONT_PAGE
    recip_list = ROOT.findall('recip')
    num_recip = len(recip_list)
    for i in range(5):
        print('Printing recipient data on FRONT_PAGE')

        # Printing recipient data to next box
        try:
            recip = recip_list.pop()
        except IndexError:
            recip_dict = {
                'acct_num': '',
                'name': '',
                'address_1': '',
                'address_2': '',
                'city': '',
                'state': '',
                'zip': '',
                'item_desc_page': '',
                'greeting_1': '',
                'greeting_2': '',
                'greeting_3': '',
                'company_name': ''
            }
            recip = Element('null', attrib=recip_dict)
        paint_to(TextField(field_name=f"pb_r{i+1}name", value=recip.get('name'), font_size=Decimal(8),
                           border_top=False, border_right=False, border_bottom=False, border_left=False),
                 page, 0.275, 7.55 - i * 1.485, 2.1)
        paint_to(TextField(field_name=f"pb_r{i+1}address_1", value=recip.get('address_1'), font_size=Decimal(8),
                           border_top=False, border_right=False, border_bottom=False, border_left=False),
                 page, 0.275, 7.4167 - i * 1.485, 2.1)
        al2 = f"{recip.get('city')}, {recip.get('state')} {recip.get('zip')}"
        paint_to(TextField(field_name=f"pb_r{i+1}address_2", value=al2, font_size=Decimal(8),
                           border_top=False, border_right=False, border_bottom=False, border_left=False),
                 page, 0.275, 7.2834 - i * 1.485, 2.1)
        paint_to(TextField(field_name=f"pb_r{i+1}acct_num", value=recip.get('acct_num'), font_size=Decimal(8),
                           border_top=False, border_right=False, border_bottom=False, border_left=False),
                 page, 2.65, 7.55 - i * 1.485, 1.05)
        paint_to(TextField(field_name=f"pb_r{i+1}item_desc", value=recip.get('item_desc_page'), font_size=Decimal(8),
                           border_top=False, border_right=False, border_bottom=False, border_left=False),
                 page, 0.275, 6.75 - i * 1.485, 3.42)
        paint_to(TextField(field_name=f"pb_r{i+1}greeting_1", value=recip.get('greeting_1'), font_size=Decimal(8),
                           border_top=False, border_right=False, border_bottom=False, border_left=False),
                 page, 0.275, 6.6167 - i * 1.485, 3.42)
        paint_to(TextField(field_name=f"pb_r{i+1}greeting_2", value=recip.get('greeting_2'), font_size=Decimal(8),
                           border_top=False, border_right=False, border_bottom=False, border_left=False),
                 page, 0.275, 6.4834 - i * 1.485, 3.42)
        paint_to(TextField(field_name=f"pb_r{i+1}greeting_3", value=recip.get('greeting_3'), font_size=Decimal(8),
                           border_top=False, border_right=False, border_bottom=False, border_left=False),
                 page, 0.275, 6.3501 - i * 1.485, 3.42)

    # FRONT_PAGE is complete!

    # Print RECIPIENT details to RECIPIENT_PAGEs
    num_pages = math.ceil((num_recip - 5) / 6)
    for p in range(num_pages):
        print('Acquiring new copy of RECIPIENT_PAGE')
        page = RECIPIENT_PAGE.__deepcopy__()
        giftlist.add_page(page)

        for i in range(6):
            print('Printing recipient data on page')

            # Printing recipient data to next box
            try:
                recip = recip_list.pop()
            except IndexError:
                recip_dict = {
                    'acct_num': '',
                    'name': '',
                    'address_1': '',
                    'address_2': '',
                    'city': '',
                    'state': '',
                    'zip': '',
                    'item_desc_page': '',
                    'greeting_1': '',
                    'greeting_2': '',
                    'greeting_3': '',
                    'company_name': ''
                }
                recip = Element('null', attrib=recip_dict)

            paint_to(
                TextField(field_name=f"p{p}_r{i+1}name", value=recip.get('name'), font_size=Decimal(8),
                          border_top=False, border_right=False, border_bottom=False, border_left=False),
                page, 0.275, 9.77 - i * 1.607, 2.1)
            paint_to(
                TextField(field_name=f"p{p}_r{i+1}address_1", value=recip.get('address_1'), font_size=Decimal(8),
                          border_top=False, border_right=False, border_bottom=False, border_left=False),
                page, 0.275, 9.6367 - i * 1.607, 2.1)
            al2 = f"{recip.get('city')}, {recip.get('state')} {recip.get('zip')}"
            paint_to(
                TextField(field_name=f"p{p}_r{i+1}address_2", value=al2, font_size=Decimal(8),
                          border_top=False, border_right=False, border_bottom=False, border_left=False),
                page, 0.275, 9.5034 - i * 1.607, 2.1)
            paint_to(
                TextField(field_name=f"p{p}_r{i+1}acct_num", value=recip.get('acct_num'), font_size=Decimal(8),
                          border_top=False, border_right=False, border_bottom=False, border_left=False),
                page, 2.65, 9.77 - i * 1.607, 1.05)
            paint_to(
                TextField(field_name=f"p{p}_r{i+1}item_desc", value=recip.get('item_desc_page'), font_size=Decimal(8),
                          border_top=False, border_right=False, border_bottom=False, border_left=False),
                page, 0.275, 8.97 - i * 1.607, 3.42)
            paint_to(
                TextField(field_name=f"p{p}_r{i+1}greeting_1", value=recip.get('greeting_1'), font_size=Decimal(8),
                          border_top=False, border_right=False, border_bottom=False, border_left=False),
                page, 0.275, 8.8367 - i * 1.607, 3.42)
            paint_to(
                TextField(field_name=f"p{p}_r{i+1}greeting_2", value=recip.get('greeting_2'), font_size=Decimal(8),
                          border_top=False, border_right=False, border_bottom=False, border_left=False),
                page, 0.275, 8.7034 - i * 1.607, 3.42)
            paint_to(
                TextField(field_name=f"p{p}_r{i+1}greeting_3", value=recip.get('greeting_3'), font_size=Decimal(8),
                          border_top=False, border_right=False, border_bottom=False, border_left=False),
                page, 0.275, 8.5701 - i * 1.607, 3.42)

    print("Adding copy of BACK_PAGE to Gift List doc")
    giftlist.add_page(BACK_PAGE.__deepcopy__())

    print("Saving Gift List to new PDF file")
    output_file_name = f"GiftList_for_Acct_{buyer.get('acct_num')}.pdf"
    output_path = (PATH_TO_TEMPLATES / output_file_name)
    with open(str(output_path), "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, giftlist)

    print("The Gift List Order Form for this buyer is complete!")


def email_giftlist():
    print('*** emailing the giftlist ***')
    global ROOT

    # Getting buyer data
    buyer = ROOT.find('buyer')

    # Getting body of e-mail message
    is_corporate = buyer.get('is_corporate')
    letter_path = (PATH_TO_TEMPLATES / ('letter_corporate.txt' if is_corporate else 'letter_noncorporate.txt'))
    with open(str(letter_path), 'r') as letter_file:
        letter_body = letter_file.read()

    # Getting attachment details
    attachment_name = f"GiftList_for_Acct_{buyer.get('acct_num')}.pdf"
    attachment_path = (PATH_TO_TEMPLATES / attachment_name)
    with open(str(attachment_path), "rb") as pdf_file:
        attachment_content = base64.b64encode(pdf_file.read()).decode('utf-8')

    # Setting e-mail details
    message = {
        "from_email": "giftlist@priesters.com",
        "from_name": "Priester's Pecans",
        "subject": "Gift List Order Form",
        "text": f"{buyer.get('salutation')}{chr(10)}{chr(10)}{letter_body}",
        "to": [
            {
                "email": buyer.get('email'),
                "type": "to"

            },
            {
                "email": "mphillips@multivaluecentral.com",
                "type": "bcc"
            }
        ],
        "attachments": [
            {
                "type": 'application/pdf',
                "name": attachment_name,
                "content": attachment_content
            }
        ]
    }

    try:
        mailchimp = MailchimpTransactional.Client(MAILCHIMP_API_KEY)
        response = mailchimp.messages.send({"message": message})
        print('API called successfully: {}'.format(response))
    except ApiClientError as error:
        print('An exception occurred: {}'.format(error.text))


def prune_xml():
    global BUYER_TREE
    BUYER_TREE.getroot().clear()


def new_buyer(buyer_line: str):
    global ROOT

    # Pull Buyer data from line
    buyer_line = buyer_line.rstrip()
    assert len(buyer_line) <= 412
    buyer_line += ' ' * (412 - len(buyer_line))
    buyer_dict = {
        'acct_num': buyer_line[5:15].strip(),
        'key_code': buyer_line[27:32],
        'name': buyer_line[33:63].strip(),
        'address_1': buyer_line[63:93].strip(),
        'address_2': buyer_line[93:123].strip(),
        'city': buyer_line[123:138].strip(),
        'state': buyer_line[138:140].strip(),
        'zip': buyer_line[0:5].strip(),
        'salutation': buyer_line[145:175].strip(),
        'company_name': buyer_line[336:366].strip(),
        'email': buyer_line[366:412].strip(),
        'is_corporate': (buyer_line[175] == 'Y')
    }

    # Add 'buyer' node to ROOT
    SubElement(ROOT, 'buyer', attrib=buyer_dict)


def new_recipient(recipient_line: str):
    global ROOT

    # Pull Recipient data from line
    recipient_line = recipient_line.rstrip()
    assert len(recipient_line) <= 412
    recipient_line += ' ' * (412 - len(recipient_line))  # Enforce that the line is 366 characters long
    recip_dict = {
        'acct_num': recipient_line[15:25].strip(),
        'name': recipient_line[33:63].strip(),
        'address_1': recipient_line[63:93].strip(),
        'address_2': recipient_line[93:123].strip(),
        'city': recipient_line[123:138].strip(),
        'state': recipient_line[138:140].strip(),
        'zip': recipient_line[0:5].strip(),
        'item_desc_page': recipient_line[176:216].strip(),
        'greeting_1': recipient_line[216:256].strip(),
        'greeting_2': recipient_line[256:296].strip(),
        'greeting_3': recipient_line[296:336].strip(),
        'company_name': recipient_line[336:366].strip()
    }
    # If a recipient has a 'company_name' and no 'name' then move 'company_name' to 'name'
    if recip_dict['name'] == '':
        recip_dict['name'] = recip_dict['company_name']
    # Add recipient node to ROOT
    SubElement(ROOT, 'recip', attrib=recip_dict)


def paint_to(text_field: TextField, p: Page, left: float, bottom: float, width: float):
    # floats are in inches; multiply by 72 to get proper Decimal units
    rect: Rectangle = Rectangle(
        Decimal(left * 72),
        Decimal(bottom * 72),
        Decimal(width * 72),
        Decimal(0.1333 * 72)
    )
    text_field.paint(p, rect)


if __name__ == '__main__':
    input_file_path = (
        Path.home()
        / "PycharmProjects"
        / "giftlist"
        / "test_data_with_email.txt"
    )
    main_loop(input_file=str(input_file_path))
