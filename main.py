# pip install cairocffi pycairo PyPDF2
# brew install cairo  && brew install pango or sudo apt-get install libcairo2 libcairo2-dev

import os
import random
import string
from pprint import pprint
from random import randint, choice

import cairosvg
from PyPDF2 import PdfReader, PdfWriter
from eth_account import Account
from qrcode.main import QRCode
from web3 import Web3
import base64
from io import BytesIO


def replace_content_in_file(file_path, replacements):
    with open(file_path, 'r') as file:
        content = file.read()

    for key, value in replacements.items():
        content = content.replace(key, value)

    return content


def text_to_qr_base64(text):
    qr = QRCode(version=1, box_size=10, border=5)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffered = BytesIO()
    img.save(buffered)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str


def password_generator(param):
    uppercase_loc = randint(1, 4)
    symbol_loc = randint(5, 6)
    lowercase_loc = randint(7, 12)
    _password = ""

    pool = string.ascii_letters + string.punctuation

    for i in range(param):
        if i == uppercase_loc:
            _password += choice(string.ascii_uppercase)

        elif i == lowercase_loc:
            _password += choice(string.ascii_lowercase)

        elif i == symbol_loc:
            _password += choice(string.punctuation)

        else:
            _password += choice(pool)

    return _password
def generate_security_suffix(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def main(address_not:str,note:str , use_passphrase:bool):
    # Create a Web3 instance
    web3 = Web3()
    web3.eth.account.enable_unaudited_hdwallet_features()

    security_suffix = ''
    if use_passphrase:
        security_suffix = generate_security_suffix(3)

    # Create an account with a mnemonic
    account, mnemonic = Account.create_with_mnemonic(passphrase=security_suffix,num_words=24)

    qr_code_base64 = text_to_qr_base64(mnemonic)

    print(f"***  Private key  {account.key.hex()}")

    # Define file paths
    template_file_path = 'template.svg'
    svg_file_path = './file.svg'

    name = note.replace(' ', '_').lower().replace('!', '').replace('?', '').replace(',', '').replace('.', '')
    pdf_file_path = './main_'+ name+ '.pdf'
    encrypt_pdf_file = 'encrypt_' + name+ '.pdf'

    words = mnemonic.split()

    replacements = {
        '##ADDRESS_NOT': address_not,
        '##NOTE_BOX': note,
        '##ADDRESS_BOX': account.address,
        '#T1#' : words[0],
        '#T2#' : words[1],
        '#T3#' : words[2],
        '#T4#' : words[3],
        '#T5#' : words[4],
        '#T6#' : words[5],
        '#T7#' : words[6],
        '#T8#' : words[7],
        '#T9#' : words[8],
        '#T10#' : words[9],
        '#T11#' : words[10],
        '#T12#' : words[11],
        '#T13#' : words[12],
        '#T14#' : words[13],
        '#T15#' : words[14],
        '#T16#' : words[15],
        '#T17#' : words[16],
        '#T18#' : words[17],
        '#T19#' : words[18],
        '#T20#' : words[19],
        '#T21#' : words[20],
        '#T22#' : words[21],
        '#T23#' : words[22],
        '#T24#' : words[23],
        '#qr_code_base64#' :qr_code_base64
    }

    # Replace content in the SVG file
    modified_content = replace_content_in_file(template_file_path, replacements)

    # Write the modified content back to the file
    with open('file.svg', 'w') as file:
        file.write(modified_content)
    cairosvg.svg2pdf(url=svg_file_path, write_to=pdf_file_path, unsafe=True)

    reader = PdfReader(pdf_file_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    password = password_generator(8)
    writer.encrypt(password)

    with open(encrypt_pdf_file, 'wb') as f:
        writer.write(f)
    os.remove(svg_file_path)
    pprint(f"Passphrase: {security_suffix}")
    pprint(f"PDF file has been generated and saved to {pdf_file_path} with  password: {password}")


if __name__ == '__main__':
    note = input("Enter the note: ")
    address_not = input("Enter the address_not: ")
    passphrase_input = input("Use BIP39 Passphrase? (yes/no): ").strip().lower()
    use_passphrase = (passphrase_input == 'yes') or (passphrase_input == 'y')


    main(address_not, note, use_passphrase)