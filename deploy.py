from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./calculation.sol", "r") as file:
    cal_file = file.read()

    compile_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"demo.sol": {"content": cal_file}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]},
                },
            },
        },
        solc_version="0.8.0",
    )

with open("calculation.json", "w") as file:
    json.dump(compile_sol, file)

bytecode = compile_sol["contracts"]["demo.sol"]["practice"]["evm"]["bytecode"]["object"]

abi = compile_sol["contracts"]["demo.sol"]["practice"]["abi"]


w3 = Web3(
    Web3.HTTPProvider("HTTP://127.0.0.1:7545")
)
chain_id = 1337
my_address = "0xF3228116aDD63F55cB3c96b483C0193260852F45"
private_key = os.getenv("PRIVATE_KEY")


# create contract
calculation = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(my_address)
print(nonce)

transaction = calculation.constructor().build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# sign transation
sign_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)


# send transaction to testserver
tx_hash = w3.eth.send_raw_transaction(sign_txn.rawTransaction)
# print(tx_hash)
# print("*********************************************")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
# print(tx_receipt)


calculate_1 = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)


# Intract with calcuation contract
store_transaction = calculate_1.functions.calculate(22, 45, "*").build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
sign_transaction = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

# get output of calculate function
print(calculate_1.functions.viewAns().call())
