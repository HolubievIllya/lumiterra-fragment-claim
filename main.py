from web3 import Web3
import json
from prettytable import PrettyTable
import random
import time

table = PrettyTable()
ronin_rpc_url = "https://api.roninchain.com/rpc"
web3 = Web3(Web3.HTTPProvider(ronin_rpc_url))
print(f"{web3.is_connected()}")

with open("abis/token_abi.json", "r") as file:
    token_abi = json.load(file)

with open("abis/fragment_abi.json", "r") as file:
    fragment_abi = json.load(file)

checksum_address_nft = web3.to_checksum_address("0xcc451977a4be9adee892f7e610fe3e3b3927b5a1")
nft_contract = web3.eth.contract(checksum_address_nft, abi=fragment_abi)
checksum_address_ron = web3.to_checksum_address("0x19f70ecd63f40f11716c3ce2b50a6d07491c12fe")
contract = web3.eth.contract(checksum_address_ron, abi=token_abi)


def claim_fragment(receiver_address: str, private_key: str):
    receiver_address = Web3.to_checksum_address(receiver_address)
    nonce = web3.eth.get_transaction_count(receiver_address)
    gas_price = web3.eth.gas_price

    txn = contract.functions.mint("cbt").build_transaction(
        {
            "chainId": web3.eth.chain_id,
            "gas": 127610,
            "gasPrice": gas_price,
            "nonce": nonce,
            "from": receiver_address,
        }
    )
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    web3.eth.wait_for_transaction_receipt(tx_hash)

    return


with open("data.txt", "r") as file:
    lines = file.readlines()
table.field_names = ["Wallet address", "Ronin balance", "Fragment balance"]
for i in lines:
    try:
        claim_fragment(i.split(",")[0].strip(), i.split(",")[1].strip())
        table.add_row(
            [
                i.split(",")[0].strip(),
                web3.from_wei(
                    web3.eth.get_balance(web3.to_checksum_address(i.split(",")[0].strip())),
                    "ether",
                ),
                nft_contract.functions.balanceOf(
                    web3.to_checksum_address(i.split(",")[0].strip()), 268650256
                ).call(),
            ]
        )
        print(f"{i.split(',')[0].strip()} has done")
    except Exception as e:
        print(f"{i.split(',')[0].strip()} error {e}")
    sleep_time = random.randint(1, 100)
    print(f"Sleep for {sleep_time}")
    time.sleep(sleep_time)

print(table)
