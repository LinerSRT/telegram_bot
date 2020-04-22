import pickle
import os

class User:
    def __init__(self, user_id, username, name, admin=False, banned=False,
                 message_count=1, slog_played=0, sex_command_used=0):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.admin = admin
        self.banned = banned
        self.message_count = message_count
        self.slog_played = slog_played
        self.sex_command_used = sex_command_used
        self.economic = Economic()

    def stat(self):
        out = ""
        out += "user_id - "+str(self.user_id)+"\n"
        out += "username - "+str(self.username)+"\n"
        out += "name - "+str(self.name)+"\n"
        out += "admin - "+str(self.admin)+"\n"
        out += "banned - "+str(self.banned)+"\n"
        out += "message_count - "+str(self.message_count)+"\n"
        out += "slog_played - "+str(self.slog_played)+"\n"
        out += "sex_command_used - "+str(self.sex_command_used)+"\n"
        out += "user_money - "+str(self.economic.user_money)+"\n"
        out += "credit_money - "+str(self.economic.credit_money)+"\n"
        out += "debit_money - "+str(self.economic.debit_money)+"\n"
        out += "have_credit - "+str(self.economic.have_credit)+"\n"
        out += "have_debit - "+str(self.economic.have_debit)+"\n"
        out += "use_banks - "+str(self.economic.use_banks)+"\n"
        out += "bank - "+str(self.economic.bank)+"\n"
        out += "have_bank - "+str(self.economic.have_bank)+"\n"
        if self.economic.have_bank:
            out += "bank_id - "+str(self.economic.bank.bank_id)+"\n"
            out += "bank_name - "+str(self.economic.bank.bank_name)+"\n"
            out += "bank_description - "+str(self.economic.bank.bank_description)+"\n"
            out += "credit_percent - "+str(self.economic.bank.credit_percent)+"\n"
            out += "debit_percent - "+str(self.economic.bank.debit_percent)+"\n"
            out += "percent_limit - "+str(self.economic.bank.percent_limit)+"\n"
            out += "bank_users - "+str(self.economic.bank.bank_users)+"\n"
            out += "bank_money - "+str(self.economic.bank.bank_money)+"\n"
        return out

class Economic:
    def __init__(self, user_money=1000, have_credit=False, have_debit=False, credit_money=0, debit_money=0):
        self.user_money = user_money
        self.credit_money = credit_money
        self.debit_money = debit_money
        self.have_credit = have_credit
        self.have_debit = have_debit
        self.use_banks = []
        self.bank = None
        self.have_bank = False
        pass

    def getMoney(self, amount):
        self.user_money -= amount
        return amount

    def getCredit(self, amount, bank_id):
        for user in getAllUsers():
            if user.economic.have_bank:
                bank_obj = user.economic.bank
                if bank_id == bank_obj.bank_id:
                    if amount < bank_obj.bank_money:
                        user.economic.credit_money += amount
                        user.economic.user_money += amount
                        user.economic.use_banks.append(bank_obj)
                        user.economic.have_credit = True
                        bank_obj.bank_money -= amount
                        bank_obj.bank_users.append(user)
                        return 0
                    else:
                        return -1
                else:
                    return -2
            else:
                return -3
        return -4

    def buyBank(self, user, name, desc):
        bank_cost = 3
        if self.user_money > bank_cost:
            self.have_bank = True
            self.bank = Bank(user, name, desc)
            return 0
        else:
            return -1

class Bank:
    def __init__(self, bank_id, bank_name, bank_description, credit_percent=5, debit_percent=5, percent_limit=20):
        self.bank_id = bank_id
        self.bank_name = bank_name
        self.bank_description = bank_description
        self.credit_percent = credit_percent
        self.debit_percent = debit_percent
        self.percent_limit = percent_limit
        self.bank_users = []
        self.bank_money = 50000


def saveUser(user):
    with open("database/"+user.username+".ldb", 'wb') as f:
       pickle.dump(user, f)

def getUser(username):
    with open("database/"+username+".ldb", 'rb') as f:
       return pickle.load(f)

def isUserExist(username):
    return os.path.exists("database/"+username+".ldb")

def getAllUsers():
    out = []
    for filename in os.listdir("database/"):
        if "ldb" in filename:
            user = filename.replace(".ldb", "")
            out.append(getUser(user))
    return out

me = getUser("Llne_R")

print(me.economic.getCredit(500, 750117845))
print("---------------------")
saveUser(me)
print(getUser("Llne_R").stat())



#with open('data.xml', 'wb') as f:
#    pickle.dump(user, f)
#
#with open('data.xml', 'rb') as f:
#    test = pickle.load(f)