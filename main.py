from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import abi, address_contract

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract = w3.eth.contract(address=address_contract, abi=abi)
print(w3.eth.get_balance('0x662Bde9ee2CD1027b6C4B0C0E03f95660cAC6bF1'))
print(w3.eth.get_balance('0x20f4b94e0a287D64374582c6d183f88fb5Eb850a'))
print(w3.eth.get_balance('0x5F285Bc8Cf72fad41be85D1a10254B7605B3c4Db'))
print(w3.eth.get_balance('0x26e8b8B9204F58b05B9bB9bfFD8771480FDb8399'))
print(w3.eth.get_balance('0x02eEd092311a3672aB76F09FF497735960de3a97'))

# def login():
#     try:
#         public_key = input("Введите публичный ключ: ")
#         password = input("Введите пароль: ")
#         w3.geth.personal.unlock_account(public_key, password)
#         return public_key
#     except Exception as e:
#         print(f"Ошибка авторизации: {e}")
#         return None

# def registration():
#     try:
#         password = input("Введите пароль: ")
#         account = w3.geth.personal.new_account(password)
#         print(f"Ваш аккаунт: {account}")
#     except Exception as e:
#         print(f"Ошибка регистрации: {e}")

# def send_eth(account):
#     try:
#         value = int(input("Введите кличество эфира для отправки"))
#         tx_hash = contract.functions.sendEth().transact({
#             "value": value,
#             "from": account
#         })
#         print(f"Транзакция отправлена успешно:  {tx_hash.hex()}")
#     except Exception as e:
#         print(f"Ошибка отправки эфира: {e}")

# def get_balance(account):
#     try:
#         balance = contract.functions.getBalance().call({
#             "from": account
#         })
#         print(f"Баланс аккаунта: {balance}")
#     except Exception as e:
#         print(f"Ошибка получения баланса аккаунта: {e}") 

# def withdraw(account):
#     try:
#         pass
#     except Exception as e:
#         print(f"Ошибка вывода средств: {e}")

# def main():
#     account = ""
#     while True:
#         if account == "" or account == None:
#             choice = int(input("Выберите \n1.Авторизация \n2.Регистрация\n"))
#             match choice:
#                 case 1:
#                     login()
#                 case 2:
#                     registration()
#                 case _:
#                     print("Введите конкретное число")
#         else:
#             choice = int(input("Выберите: \n1. Отправить эфир \n2. Вывести свой баланс \n3. Вывести баланс аккаунта \n4. Вывести средства \n5. Выход\n"))
#             match choice:
#                 case 1:
#                     send_eth(account)
#                 case 2:
#                     get_balance(account)
#                 case 3:
#                     pass
#                 case 4:
#                     withdraw(account)
#                 case 5:
#                     account = ""
#                 case _:
#                     print("Введите конкретное число")

# if __name__ == "__main__":
#     main()






