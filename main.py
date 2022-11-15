import math
import base64
from pathlib import Path
from xml.etree.ElementTree import ElementTree, Element, SubElement
from borb.pdf import Document, PDF, Page
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
    BUYER_PAGE = PDF.loads(file)
with open(str(PATH_RECIPIENT_PAGE), "rb") as file:
    RECIPIENT_PAGE = PDF.loads(file)
with open(str(PATH_BACK_PAGE), "rb") as file:
    BACK_PAGE = PDF.loads(file)


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
    with open(input_file) as file:
        for line in file:
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
    page = BUYER_PAGE.get_page(0)
    buyer = ROOT.find('buyer')
    page.set_form_field_value('b_acct_num', buyer.get('acct_num'))
    page.set_form_field_value('b_key_code', buyer.get('key_code'))
    page.set_form_field_value('b_name', buyer.get('name'))
    buyer_address = [buyer.get('company_name'),
                     buyer.get('address_line_1'),
                     buyer.get('address_line_2'),
                     f'{buyer.get("city")}, {buyer.get("state")} {buyer.get("zip")}']
    buyer_address = [x for x in buyer_address if x]
    for i in range(len(buyer_address)):
        page.set_form_field_value('b_address_'+str(i+1), buyer_address[i])

    # Print RECIPIENT details to FRONT_PAGE
    recip_list = ROOT.findall('recip')
    num_recip = len(recip_list)
    for i in range(min(5, num_recip)):
        print('Printing recipient data on FRONT_PAGE')

        # Printing recipient data to next box
        recip = recip_list.pop()
        page.set_form_field_value(f'r{i+1}_name', recip.get('name'))
        page.set_form_field_value(f'r{i+1}_acct_num', recip.get('acct_num'))
        page.set_form_field_value(f'r{i+1}_address_1', recip.get('address_line_1'))
        al2 = f"{recip.get('city')}, {recip.get('state')} {recip.get('zip')}"
        page.set_form_field_value(f'r{i+1}_address_2', al2)
        page.set_form_field_value(f'r{i+1}_item_desc', recip.get('item_desc_page'))
        page.set_form_field_value(f'r{i+1}_greeting_1', recip.get('greeting_1'))
        page.set_form_field_value(f'r{i+1}_greeting_2', recip.get('greeting_2'))
        page.set_form_field_value(f'r{i+1}_greeting_3', recip.get('greeting_3'))

    # FRONT_PAGE is complete! Let's save it.
    print('Adding completed FRONT_PAGE to Gift List doc')
    giftlist.add_page(page)

    # Print RECIPIENT details to BACK_PAGE
    num_pages = math.ceil((num_recip - 5) / 6)
    recips_left = len(recip_list)
    for p in range(num_pages):
        print('Acquiring new copy of RECIPIENT_PAGE')
        page = RECIPIENT_PAGE.get_page(0)

        for i in range(min(6, recips_left)):
            print('Printing recipient data on page')

            # Printing recipient data to next box
            recip = recip_list.pop()
            page.set_form_field_value(f'r{i + 1}_name', recip.get('name'))
            page.set_form_field_value(f'r{i + 1}_acct_num', recip.get('acct_num'))
            page.set_form_field_value(f'r{i + 1}_address_1', recip.get('address_line_1'))
            al2 = f"{recip.get('city')}, {recip.get('state')} {recip.get('zip')}"
            page.set_form_field_value(f'r{i + 1}_address_2', al2)
            page.set_form_field_value(f'r{i + 1}_item_desc', recip.get('item_desc_page'))
            page.set_form_field_value(f'r{i + 1}_greeting_1', recip.get('greeting_1'))
            page.set_form_field_value(f'r{i + 1}_greeting_2', recip.get('greeting_2'))
            page.set_form_field_value(f'r{i + 1}_greeting_3', recip.get('greeting_3'))

        recips_left = len(recip_list)
        print('Adding copy of completed RECIPIENT_PAGE to Gift List doc')
        giftlist.add_page(page)

    print("Adding copy of BACK_PAGE to Gift List doc")
    giftlist.add_page(BACK_PAGE.get_page(0))

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
        'address_line_1': buyer_line[63:93].strip(),
        'address_line_2': buyer_line[93:123].strip(),
        'city': buyer_line[123:138].strip(),
        'state': buyer_line[138:140].strip(),
        'zip': buyer_line[0:5].strip(),
        'salutation': buyer_line[145:175].strip(),
        'company_name': buyer_line[337:366].strip(),
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
        'address_line_1': recipient_line[63:93].strip(),
        'address_line_2': recipient_line[93:123].strip(),
        'city': recipient_line[123:138].strip(),
        'state': recipient_line[138:140].strip(),
        'zip': recipient_line[0:5].strip(),
        'item_desc_page': recipient_line[176:216].strip(),
        'greeting_1': recipient_line[216:256].strip(),
        'greeting_2': recipient_line[256:296].strip(),
        'greeting_3': recipient_line[296:336].strip(),
        'company_name': recipient_line[337:366].strip()
    }

    # Add recipient node to ROOT
    SubElement(ROOT, 'recip', attrib=recip_dict)


if __name__ == '__main__':
    input_file_path = (
        Path.home()
        / "PycharmProjects"
        / "giftlist"
        / "test_data_with_email.txt"
    )
    main_loop(input_file=str(input_file_path))
