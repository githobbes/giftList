from pathlib import Path
from xml.etree.ElementTree import ElementTree, Element, SubElement
from borb.pdf import Document, PDF

# Defining constants
ROOT = Element('root')
BUYER_TREE = ElementTree(ROOT)
PATH_TO_TEMPLATES = (Path.home() / "PycharmProjects" / "giftlist" / "data")
PATH_FRONT_PAGE = (PATH_TO_TEMPLATES / "buyer_page.pdf")
PATH_MIDDLE_PAGE = (PATH_TO_TEMPLATES / "middle_page.pdf")
PATH_BACK_PAGE = (PATH_TO_TEMPLATES / "back_page.pdf")
# Use borb to open pdf_form_example.pdf
with open(str(PATH_FRONT_PAGE), "rb") as file:
    FRONT_PAGE = PDF.loads(file)
with open(str(PATH_MIDDLE_PAGE), "rb") as file:
    MIDDLE_PAGE = PDF.loads(file)
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
                if BUYER_TREE.getroot() is not None:
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


def make_giftlist():
    print('*** making the giftlist ***')
    global FRONT_PAGE, MIDDLE_PAGE, BACK_PAGE
    global ROOT

    # Print BUYER details on FRONT_PAGE
    page = FRONT_PAGE.get_page(0)
    buyer = ROOT.find('buyer')
    page.set_form_field_value('b_acct_number', buyer.get('acct_no'))
    page.set_form_field_value('b_key_code', buyer.get('key_code'))
    page.set_form_field_value('b_name', buyer.get('name'))
    buyer_address = [buyer.get('company_name'),
                     buyer.get('address_line_1'),
                     buyer.get('address_line_2'),
                     f'{buyer.get("city")}, {buyer.get("state")} {buyer.get("zip")}']
    buyer_address = [x for x in buyer_address if x]
    if len(buyer_address) == 4:  # Company Name is option and only displayed if there is available space
        buyer_address.pop(0)
    for i in range(buyer_address):
        page.set_form_field_value('b_address_'+str(i+1), buyer_address[i])

    # Print RECIPIENT details to FRONT_PAGE
    recip_list = ROOT.findall('recip')
    num_recip = len(recip_list)
    for _ in range(min(5, num_recip)):
        print('Printing recipient data on FRONT_PAGE')

    # FRONT_PAGE is complete! Let's save it.
    print('Saving front page...')
    doc = Document().add_page(page)
    doc_path = (PATH_TO_TEMPLATES / ('front_page_'+buyer.get('acct_no')+'.pdf'))
    with open(str(doc_path), "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc)

    # Print RECIPIENT details to BACK_PAGE
    page = BACK_PAGE.get_page(0)
    for _ in range(min(5 + 6, num_recip)):
        print('Printing recipient data on BACK_PAGE')

    # BACK_PAGE is complete! Let's save it.
    print('Saving back page...')
    doc = Document().add_page(page)
    doc_path = (PATH_TO_TEMPLATES / ('back_page_'+buyer.get('acct_no')+'.pdf'))
    with open(str(doc_path), "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc)

    ### What I've done so far isn't bad, but it's not great
    ### I should be developing the pages and adding them to the document, NOT saving each page as its own document
    print("The Gift List Order Form for this buyer is complete!")


def email_giftlist():
    print('*** emailing the giftlist ***')


def prune_xml():
    global BUYER_TREE
    BUYER_TREE.getroot().clear()


def new_buyer(buyer_line: str):
    global ROOT

    # Pull Buyer data from line
    buyer_dict = {
        'acct_no': buyer_line[5:15].strip(),
        'key_code': buyer_line[27:32],
        'name': buyer_line[33:63].stip(),
        'address_line_1': buyer_line[63:93].strip(),
        'address_line_2': buyer_line[93:123].strip(),
        'city': buyer_line[123:138].strip(),
        'state': buyer_line[138:140].strip(),
        'zip': buyer_line[140:145].strip(),
        'salutation': buyer_line[145:175].strip(),
        'company_name': buyer_line[337:366].strip(),
        'email': buyer_line[366:412].strip()
    }

    # Add 'buyer' node to ROOT
    SubElement(ROOT, 'buyer', attrib=buyer_dict)


def new_recipient(recipient_line: str):
    global ROOT

    # Pull Recipient data from line
    recip_dict = {
        'acct_no': recipient_line[15:25].strip(),
        'name': recipient_line[33:63].strip(),
        'address_line_1': recipient_line[63:93].strip(),
        'address_line_2': recipient_line[93:123].strip(),
        'city': recipient_line[123:138].strip(),
        'state': recipient_line[138:140].strip(),
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

