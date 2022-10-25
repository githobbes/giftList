from pathlib import Path
from xml.etree.ElementTree import ElementTree, Element, SubElement

ROOT = Element('root')
BUYER_TREE = ElementTree(ROOT)


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
    SubElement(ROOT, 'recip_'+recip_dict['acct_no'], attrib=recip_dict)


if __name__ == '__main__':
    input_file_path = (
        Path.home()
        / "PycharmProjects"
        / "giftlist"
        / "test_data_with_email.txt"
    )
    main_loop(input_file=str(input_file_path))

