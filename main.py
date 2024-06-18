from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import abi, address_contract
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract = w3.eth.contract(address=address_contract, abi=abi)
# print(w3.eth.get_balance('0x662Bde9ee2CD1027b6C4B0C0E03f95660cAC6bF1')) - банк

# авторизация
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            public_key = request.form.get('public_key')
            password = request.form.get('password')
            w3.geth.personal.unlock_account(public_key, password)
            return redirect(url_for("menu", account = public_key))
        except Exception as e:
            return render_template("login.html",  error=True)
    else:
         return render_template("login.html", error=False)

# регистрация
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        try:
            password = request.form.get('password')
            if (len(password) < 12
                and any(char.isupper() for char in password)
                and any(char.islower() for char in password) 
                and any(char.isdigit() for char in password)
                and any(char in "!@#$%^&*()-=+;:?.," for char in password)
                and any(easy in password.lower()
                           for easy in ["qwerty", "ytrewq", "123", "321", "1234", "4321", "111", "password"])):
                return render_template("registration.html",  error=True)
            else:
                public_key = w3.geth.personal.new_account(password)
                w3.geth.personal.unlock_account(public_key, password)
                return redirect(url_for("menu", account = public_key))
        except Exception as e:
            return render_template("registration.html",  error=True)
    else:
         return render_template("registration.html", error=False)

# меню пользователя
@app.route('/menu/<account>')
def menu(account):
    return render_template("index.html", account = account)

# меню для создания недвижимости
@app.route('/menu/Create-Estate/<account>', methods=['GET', 'POST'])
def createEst(account):
    if request.method == 'POST':
        try:
            size = int(request.form.get('size'))
            addressEstate = request.form.get('address')
            esType = int(request.form.get('gridRadios'))
            contract.functions.createEstate(size, addressEstate, esType).transact({
                "from": account
            })
            return render_template("create-est.html", account = account, error = False, completed = True)
        except Exception as e:
            return render_template("create-est.html", account = account, error=True, er = e)
    else:
        return render_template("create-est.html", account = account, error = False)

# меню для создания объявления
@app.route('/menu/Create-Ad/<account>', methods=['GET', 'POST'])
def createAd(account):
    if request.method == 'POST':
        try:
            buyer = request.form.get('public_key')
            amount = int(request.form.get('amount'))
            id_est = int(request.form.get('id_est'))
            contract.functions.createAduint(buyer, amount, id_est).transact({
                "from": account
            })
            return render_template("create-ad.html", account = account, error = False, completed = True)        
        except Exception as e:
            return render_template("create-ad.html", account = account, error=True, er = e)
    else:
        return render_template("create-ad.html", account = account, error = False)

# изменение статуса недвижимости
@app.route('/menu/Change-Estate/<account>', methods=['GET', 'POST'])
def changeEst(account):
    if request.method == 'POST':
        try:
            id_est = int(request.form.get('id_est'))
            contract.functions.updateEstateStatus(id_est).transact({
                "from": account
            })
            return render_template("change-est.html", account = account, error = False, completed = True)        
        except Exception as e:
            return render_template("change-est.html", account = account, error=True, er = e)
    else:
        return render_template("change-est.html", account = account, error = False)

# изменение статуса объявления
@app.route('/menu/Change-Ad/<account>', methods=['GET', 'POST'])
def changeAd(account):
    if request.method == 'POST':
        try:
            id_est = int(request.form.get('id_est'))
            id_ad = int(request.form.get('id_ad'))
            contract.functions.updateAdStatus(id_est, id_ad).transact({
                "from": account
            })
            return render_template("change-ad.html", account = account, error = False, completed = True)        
        except Exception as e:
            return render_template("change-ad.html", account = account, error=True, er = e)
    else:
        return render_template("change-ad.html", account = account, error = False)

# покупка недвижимости
@app.route('/menu/Buy-Estate/<account>', methods=['GET', 'POST'])
def buyEst(account):
    if request.method == 'POST':
        try:
            id_ad = int(request.form.get('id_ad'))
            value = int(request.form.get('value'))
            contract.functions.buyEstate(id_ad).transact({
                "from": account,
                "value": value * 1000000000000000000
            })
            return render_template("buy-est.html", account = account, error = False, completed = True)        
        except Exception as e:
            return render_template("buy-est.html", account = account, error=True, er = e)
    else:
        return render_template("buy-est.html", account = account, error = False)

# получение баланса
@app.route('/menu/Balance/<account>')
def balance(account):
    try:
        dapps_balance = contract.functions.getBalance().call({"from": account}) / 1000000000000000000
        wallet_balance = str(w3.eth.get_balance(account) / 1000000000000000000)
        return render_template("balance.html", account = account, dapps_balance = dapps_balance, wallet_balance = wallet_balance, error = False, completed = True)
    except Exception as e:
         return render_template("balance.html", account = account, dapps_balance = dapps_balance, wallet_balance = wallet_balance, error = True)

# снятие средств со смарт контракта    
@app.route('/menu/Withdraw/<account>', methods=['GET', 'POST'])
def withDraw(account):
    if request.method == 'POST':
        try:
            amount = int(request.form.get('amount'))
            to = request.form.get('public_key')
            tx_hash = contract.functions.withDraw(to, amount).transact({
                "from": account
            })
            return render_template("withdraw.html", account = account, error = False, completed = True)        
        except Exception as e:
            return render_template("withdraw.html", account = account, error=True, er = e)
    else:
        return render_template("withdraw.html", account = account, error = False)

# покупка эфира
@app.route('/menu/Send-Eth/<account>', methods=['GET', 'POST'])
def sendEth(account):
    if request.method == 'POST':
        try:
            value = int(request.form.get('value'))
            to = request.form.get('public_key')
            card = int(request.form.get('card'))
            cvv = int(request.form.get('cvv'))
            tx_hash = w3.eth.send_transaction({
                'to': to,
                'from': "0x662Bde9ee2CD1027b6C4B0C0E03f95660cAC6bF1",
                'value': value * 1000000000000000000
            })
            return render_template("sendeth.html", account = account, error = False, completed = True)        
        except Exception as e:
            return render_template("sendeth.html", account = account, error=True, er = e)
    else:
        return render_template("sendeth.html", account = account, error = False)

# список доступной недвижимости
@app.route('/menu/Estate-Info/<account>')
def estInfo(account):
    estates = contract.functions.getEstate().call()
    formatted_est = []
    for estate in estates:
        formatted_est.append({
            "ID:": estate[5],  
            "Размер:": estate[0],  
            "Адрес:": estate[1],  
            "Владелец:": estate[2] if account != estate[2] else "Вы",  
            "Тип:": estate[3],  
            "Активность:": "Активна" if estate[4] else "Неактивна"
        })
    return render_template("get-est.html", account = account, estates = formatted_est)

# список доступных объявлений
@app.route('/menu/Ad-Info/<account>')
def adInfo(account):
    ads = contract.functions.getAds().call()
    formatted_ads = []
    for ad in ads:
        formatted_ads.append({
            "ID объявления:": ad[4],
            "ID недвижимости:": ad[3],
            "Владелец:": ad[0],
            "Покупатель:": ad[1] if account != ad[1] else "Вы",
            "Цена:": ad[2] / 1000000000000000000,
            "Статус:": "Активна" if ad[6] == 0 else "Неактивна"
        })
    return render_template("get-ad.html", account = account, ads = formatted_ads)

if __name__ == "__main__":
    app.run(debug=True)






