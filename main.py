from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import abi, address_contract

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract = w3.eth.contract(address=address_contract, abi=abi)
# print(w3.eth.get_balance('0x662Bde9ee2CD1027b6C4B0C0E03f95660cAC6bF1')) - банк
# print(w3.eth.get_balance('0x20f4b94e0a287D64374582c6d183f88fb5Eb850a'))
# print(w3.eth.get_balance('0x5F285Bc8Cf72fad41be85D1a10254B7605B3c4Db'))
# print(w3.eth.get_balance('0x26e8b8B9204F58b05B9bB9bfFD8771480FDb8399'))
# print(w3.eth.get_balance('0x02eEd092311a3672aB76F09FF497735960de3a97'))

# функции входа/регистрации
def login():
    try:
        public_key = input("Введите публичный ключ: ")
        password = input("Введите пароль: ")
        w3.geth.personal.unlock_account(public_key, password)
        return public_key
    except Exception as e:
        print(f"Ошибка авторизации: {e}")
        return None

def registration():
    try:
        while True:
            password = input("Введите пароль: ")
            if len(password) < 12:
                print("Ваш пароль должен быть не менее 12-и символов.")
                continue
            if not any(char.isupper() for char in password):
                print("Ваш пароль должен содержать хотя бы 1-у заглавную букву.")
                continue
            if not any(char.islower() for char in password):
                print("Ваш пароль должен содержать хотя бы 1-у строчную букву.")
                continue
            if not any(char.isdigit() for char in password):
                print("Ваш пароль должен содержать хотя бы 1-у цифру.")
                continue
            if set("!@#$%^&*()-=+;:?.,").isdisjoint(password):
                print("Ваш пароль должен содержать хотя бы 1 спецсимвол.")
                continue
            if any(easy in password.lower() 
                   for easy in ["qwerty", "ytrewq", "123", "321", "1234", "4321", "111", "password"]):
                print("Ваш пароль часто встречаемый.")
                continue
            password_repeat = input("Введите пароль повторно: ")
            if password != password_repeat:
                print("Пароли не совпадают.")
                continue
            account = w3.geth.personal.new_account(password)
            print(f"Ваш аккаунт: {account}")
            break

    except Exception as e:
        print(f"Ошибка регистрации: {e}")

# функция переводов
def send_eth(account):
    try:
        value = int(input("Введите кол-во переводимого эфира: "))
        card = int(input("Введите номер карты: "))
        cvv = int(input("Введите CVV код: "))
        tx_hash = w3.eth.send_transaction({
            'to': account,
            'from': "0x662Bde9ee2CD1027b6C4B0C0E03f95660cAC6bF1",
            'value': value * 1000000000000000000
        })
        print(f"Транзакция отправлена успешно:  {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка отправки эфира: {e}")

def withdraw(account):
    try:
        amount = int(input("Введите кол-во переводимого эфира: "))
        to = input("Введите публичный адресс: ")
        tx_hash = contract.functions.withDraw(to, amount).transact({
            "from": account
        })
        print(f"Снятие успешно:  {tx_hash.hex()}")
    except Exception as e:
        print(f"Ошибка вывода средств: {e}")

# функции получения
def get_balance(account):
    try:
        balance = contract.functions.getBalance().call({
            "from": account
        })
        print(f"Баланс на смартконтракте: {balance}")
    except Exception as e:
        print(f"Ошибка получения баланса смартконтракта: {e}")

def get_estate():
    try:
        estates = contract.functions.getEstate().call()
        for estate in estates:
            if estate[-2]:
                print(f"{estate[-1]}. Недвижимость - адресс: {estate[1]}")
    except Exception as e:
        print(f"Ошибка получения списка доступных недвижимостей: {e}") 

def get_ads(account):
    try:
        ads = contract.functions.getAds().call()
        for ad in ads:
            if not ad[-1]:
                if account != ad[1]:
                    print(f"{ad[-3]}. Объявление - id недвижимости: {ad[-4]} - цена {ad[2]}")
                else:
                    print(f"{ad[-3]}. Объявление - id недвижимости: {ad[-4]} - цена {ad[2]} - вы покупатель")
    except Exception as e:
        print(f"Ошибка получения списка доступных объявлений: {e}")   

# функции создания
def create_estate(account):
    try:
        size = int(input("Введите размер недвижимости: "))
        addressEstate = input("Введите адрес недвижимости: ")
        esType = int(input("Введите тип недвижимости: "))
        contract.functions.createEstate(size, addressEstate, esType).transact({
            "from": account
        })
        print(f"Недвижимость - {addressEstate} создана!")
    except Exception as e:
        print(f"Ошибка создания недвижимости: {e}")

def create_ad(account):
    try:
        buyer = input("Введите публичный адрес покупателя: ")
        amount = int(input("Введите цену: "))
        id_est = int(input("Введите id недвижимости: "))
        contract.functions.createAduint(buyer, amount, id_est).transact({
            "from": account
        })
        print(f"Объявление создано!")
    except Exception as e:
        print(f"Ошибка создания объявления: {e}")    

# функции обновления
def update_estate_status(account):
    try:
        id_est = int(input("Введите номер недвижимости: "))
        contract.functions.updateEstateStatus(id_est).transact({
            "from": account
        })
        print(f"Недвижимость и все ее активные объявления были закрыты!")
    except Exception as e:
        print(f"Ошибка закрытия недвижимости: {e}")

def update_ad_status(account):
    try:
        id_est = int(input("Введите номер недвижимости: "))
        id_ad = int(input("Введите номер объявления: "))
        contract.functions.updateAdStatus(id_est, id_ad).transact({
            "from": account
        })
        print(f"Объявление было закрыто!")
    except Exception as e:
        print(f"Ошибка закрытия объявления: {e}")

# функция покупки
def buy_estate(account):
    try:
        id_ad = int(input("Введите номер объявления: "))
        value = int(input("Введите сколько вы хотите перевести с аккаунта на смартконтракт: "))
        contract.functions.buyEstate(id_ad).transact({
            "from": account,
            "value": value * 1000000000000000000
        })
        print(f"Недвижимость была приобретена вами, поздравляем с покупкой!")
    except Exception as e:
        print(f"Ошибка покупки недвижимости: {e}")  

# меню
def main():
    account = ""
    while True:
        try:
            if account == "" or account == None:
                choice = int(input("Выберите \n1.Авторизация \n2.Регистрация\n"))
                match choice:
                    case 1:
                        account = login() # 0x47C61F5ff0f86C1a96FdcBb70caBaB77Cc1216d1 - 124Alex4678!
                    case 2:
                        registration()
                    case _:
                        print("Введите конкретное число!")
            else:
                choice = int(input("Выберите:\
                                    \n1. Вывести баланс на смартконтракте\
                                    \n2. Вывести баланс аккаунта\
                                    \n3. Вывести средства\
                                    \n4. Создать недвижимость\
                                    \n5. Создать объявление\
                                    \n6. Изменить статус недвижимости\
                                    \n7. Изменить статус объявления\
                                    \n8. Покупка недвижимости\
                                    \n9. Доступные недвижимости\
                                    \n10. Доступные объявления\
                                    \n11. Зачислить средства на аккаунт\
                                    \n12. Выход\n"))
                match choice:
                    case 1:
                        get_balance(account) 
                    case 2:
                        print(f"Баланс на аккаунте: {w3.eth.get_balance(account)}")
                    case 3:
                        withdraw(account)
                    case 4:
                        create_estate(account)
                    case 5:
                        create_ad(account)
                    case 6:
                        update_estate_status(account)
                    case 7:
                        update_ad_status(account)
                    case 8:
                        buy_estate(account)
                    case 9:
                        get_estate()
                    case 10:
                        get_ads(account)
                    case 11:
                        send_eth(account)
                    case 12:
                        account = "" 
                    case _:
                        print("Введите конкретное число!")

        except Exception as e:
            print(f"Ошибка меню: {e}") 

if __name__ == "__main__":
    main()






