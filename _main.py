from web3 import Web3
from eth_account import Account
import json
import string
import random


# import qrcode


class BColors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def password_generator(length):
    """Function that generates a password given a length"""

    uppercase_loc = random.randint(1, 4)  # random location of lowercase
    symbol_loc = random.randint(5, 6)  # random location of symbols
    lowercase_loc = random.randint(7, 12)  # random location of uppercase

    password = ""  # empty string for password

    pool = string.ascii_letters + string.punctuation  # the selection of characters used

    for i in range(length):
        if i == uppercase_loc:  # this is to ensure there is at least one uppercase
            password += random.choice(string.ascii_uppercase)

        elif i == lowercase_loc:  # this is to ensure there is at least one uppercase
            password += random.choice(string.ascii_lowercase)

        elif i == symbol_loc:  # this is to ensure there is at least one symbol
            password += random.choice(string.punctuation)

        else:  # adds a random character from pool
            password += random.choice(pool) 

    return password  # returns the string


w3 = Web3()
w3.eth.account.enable_unaudited_hdwallet_features()
acc, mnemonic = Account.create_with_mnemonic(num_words=24)
print(mnemonic)

password = password_generator(13)
print(f"🚀Private key :\n{BColors.FAIL}{w3.to_hex(acc.key)}{BColors.ENDC}")
print(f"\nAccount address :\n{BColors.OKBLUE}{acc.address}{BColors.ENDC}")

encrypted = Account.encrypt(w3.to_hex(acc.key), password)

encrypted_json = json.dumps(encrypted)
file_name = f"{acc.address}.json"

with open(file_name, "w") as file:
    file.write(encrypted_json)

print(f"\n{BColors.HEADER}🫣\tEncrypted account information has been saved to {file_name}.{BColors.ENDC}")
print(f"\n{BColors.HEADER}\tPassword file :{BColors.ENDC}")
print(f"\n{BColors.WARNING}\t{password}{BColors.ENDC}\n")

# qr = qrcode.QRCode()
# qr.add_data(encrypted_json)
# qr.make()
# qr.print_ascii()