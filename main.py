# pip install cairosvg PyPDF2
# brew install cairo or sudo apt-get install libcairo2 libcairo2-dev

import os

import cairosvg
from PyPDF2 import PdfReader, PdfWriter
from eth_account import Account
from web3 import Web3

w3 = Web3()
w3.eth.account.enable_unaudited_hdwallet_features()
acc, mnemonic = Account.create_with_mnemonic(num_words=24)

file_path = 'template.svg'
svg_file_path = './file.svg'
pdf_file_path = './file.pdf'

words = mnemonic.split()
indexed_words = [f"{i + 1}.{word}" for i, word in enumerate(words)]

n = len(indexed_words)
part1 = indexed_words[:n // 4]
part2 = indexed_words[n // 4:n // 2]
part3 = indexed_words[n // 2:3 * n // 4]
part4 = indexed_words[3 * n // 4:]

# Read the content of the file
with open(file_path, 'r') as file:
    content = file.read()

# Replace ##ADDRESS_BOX with 12113
modified_content = content.replace('##ADDRESS_BOX', acc.address)
modified_content = modified_content.replace('##MNEMONIC_L1', '  '.join(part1))
modified_content = modified_content.replace('##MNEMONIC_L2', ' '.join(part2))
modified_content = modified_content.replace('##MNEMONIC_L3', ' '.join(part3))
modified_content = modified_content.replace('##MNEMONIC_L4', ' '.join(part4))

# Write the modified content back to the file
with open('file.svg', 'w') as file:
    file.write(modified_content)
cairosvg.svg2pdf(url=svg_file_path, write_to=pdf_file_path, unsafe=True)

reader = PdfReader(pdf_file_path)
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)
password = "your_password"
writer.encrypt(password)

with open('output.pdf', 'wb') as f:
    writer.write(f)
os.remove(svg_file_path)
os.remove(pdf_file_path)


print(f"PDF file has been generated and saved to {pdf_file_path}")
