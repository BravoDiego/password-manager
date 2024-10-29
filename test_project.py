from project import *

path: str = "data_test.csv"

def test_title():
    assert(title("This is not a message")) == None
    assert(title("Not a message", font="digital")) == None

def test_generate_password():
    random.seed(0)
    assert(generate_password()) == "X1fH$!ZM9T-B#rK"

def test_menu():
    assert(menu("menu")) == ["[1] Register", "[2] Login", "[3] Display Account registered", "[4] Quit System"]
    assert(menu("login")) == ["[1] Show passwords", "[2] Account information", "[3] Delete Account", "[4] Quit Account"]
    assert(menu("password")) == ["[1] Add password", "[2] Modify password", "[3] Search password", "[4] Delete password", "[5] Quit password Interface"]

    assert(menu("account")) == "Un problème est survenu"
    assert(menu(3)) == "Un problème est survenu"

def test_data_recovery():
    global path
    assert(data_recovery(path)) == [{'name': 'Ricardo', 'date of birth': '13/06/1995', 'country': 'Spain', 'email': 'ricardo.marquez@gmail.com', 'password': 'QWERTY'}]

def test_store_csv():
    global path
    store_csv([{'name': 'Maria', 'date of birth': '26/09/2001', 'country': 'Ireland', 'email': 'maria.mccarthy@gmail.com', 'password': 'AA'}], path)
    assert(data_recovery(path)) == [{'name': 'Ricardo', 'date of birth': '13/06/1995', 'country': 'Spain', 'email': 'ricardo.marquez@gmail.com', 'password': 'QWERTY'}, {'name': 'Maria', 'date of birth': '26/09/2001', 'country': 'Ireland', 'email': 'maria.mccarthy@gmail.com', 'password': 'AA'}]
    store_csv([{'name': 'Ricardo', 'date of birth': '13/06/1995', 'country': 'Spain', 'email': 'ricardo.marquez@gmail.com', 'password': 'QWERTY'}], path, modify=True)
    assert(data_recovery(path)) == [{'name': 'Ricardo', 'date of birth': '13/06/1995', 'country': 'Spain', 'email': 'ricardo.marquez@gmail.com', 'password': 'QWERTY'}]

def test_match():
    global path
    ricardo = {'name': 'Ricardo', 'date of birth': '13/06/1995', 'country': 'Spain', 'email': 'ricardo.marquez@gmail.com', 'password': 'QWERTY'}
    assert(match({'name': 'Ricardo', 'password': 'QWERTY'}, path, login=True)) == [ricardo]
    assert(match({'email': 'ricardo.marquez@gmail.com', 'password': 'QWERTY'}, path, login=True)) == [ricardo]

    account = {'name': 'Eric', 'date of birth': '01/11/1989', 'country': 'India', 'email': 'eric.wilkersona@gmail.com', 'password': 'INDIA'}
    store_csv([account, account], path)
    assert(match(account, path)) == [account, account]
    for _ in range(2): #repeat 2 times to delete all eric's account informations
        delete(path, data_to_delete=account)

    assert(match({"name":"Ricardo"}, path)) == [ricardo]
    assert(match({}, path)) == []

def test_delete():
    global path
    store_csv([{'name': 'Jessica', 'date of birth': '23/01/1973', 'country': 'USA', 'email': 'jessica.thomas@gmail.com', 'password': 'jessica'}], path)
    assert(delete(path, data_to_delete={'name': 'Jessica', 'date of birth': '23/01/1973', 'country': 'USA', 'email': 'jessica.thomas@gmail.com', 'password': 'jessica'})) == None

def test_register(monkeypatch):
    global path
    information = [
        "Todd Harris",
        "10/03/2008",
        "Solomon Islands",
        "johnsonpatrick@example.net",
        "QSD"
    ]
    inputs = iter(information)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert register(path, store=False) == [{'name': 'Todd Harris', 'date of birth': '10/03/2008', 'country': 'Solomon Islands', 'email': 'johnsonpatrick@example.net', 'password': 'QSD'}]
