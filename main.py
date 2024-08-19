# pip install cairosvg PyPDF2
# brew install cairo or sudo apt-get install libcairo2 libcairo2-dev

import os
import string
from random import randint, choice

import cairosvg
from PyPDF2 import PdfReader, PdfWriter
from eth_account import Account
from web3 import Web3


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


# Create a Web3 instance
web3 = Web3()
web3.eth.account.enable_unaudited_hdwallet_features()

# Create an account with a mnemonic
account, mnemonic = Account.create_with_mnemonic(num_words=24)

print(account.key.hex())
# Define file paths
template_file_path = 'template.svg'
svg_file_path = './file.svg'
pdf_file_path = './file.pdf'

# Split mnemonic into indexed words
words = mnemonic.split()
indexed_words = [f"{i + 1}.{word}" for i, word in enumerate(words)]

# Divide indexed words into parts
n = len(indexed_words)
part1 = indexed_words[:n // 4]
part2 = indexed_words[n // 4:n // 2]
part3 = indexed_words[n // 2:3 * n // 4]
part4 = indexed_words[3 * n // 4:]


def replace_content_in_file(file_path, replacements):
    with open(file_path, 'r') as file:
        content = file.read()

    for key, value in replacements.items():
        content = content.replace(key, value)

    return content


# Define replacements for content modification
replacements = {
    '##ADDRESS_BOX': account.address,
    '##MNEMONIC_L1': ' '.join(part1),
    '##MNEMONIC_L2': ' '.join(part2),
    '##MNEMONIC_L3': ' '.join(part3),
    '##MNEMONIC_L4': ' '.join(part4)
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

with open('output.pdf', 'wb') as f:
    writer.write(f)
os.remove(svg_file_path)
# os.remove(pdf_file_path)

print(f"PDF file has been generated and saved to {pdf_file_path} with  password: {password}")
