import database
from xml.etree import ElementTree as ET
import os
import time
bank_database_folder = "database/users/banks/"

blank_bank_obj = {
    "bankname":"MyBank",
    "description":"My first bank!",
    "credit_percent":"5",
    "debit_percent":"5",
    "time_to_pay":"60"
}
blank_user_obj = {
    "name":"newusername2",
    "type":"credit",
    "money":"1000",
    "blacklist":"0",
}

def isBankExist(username):
    return os.path.exists(bank_database_folder+username+".xml")
def createSubElement(element, name, value):
    elem = ET.SubElement(element, name)
    if value is not None:
        elem.text = value
    elem.tail = "\n\t\t"
    return elem
def createBankEntry(username, bank_obj):
    username = username.replace("@", "")
    root_entry = ET.Element("bank")
    root_entry.tail = "\n\t"
    root_entry.text = "\n\t\t"
    createSubElement(root_entry, "bankname", str(bank_obj["bankname"]))
    createSubElement(root_entry, "money", str(10000))
    createSubElement(root_entry, "description", str(bank_obj["description"]))
    createSubElement(root_entry, "credit_percent", str(bank_obj["credit_percent"]))
    createSubElement(root_entry, "debit_percent", str(bank_obj["debit_percent"]))
    createSubElement(root_entry, "time_to_pay", str(bank_obj["time_to_pay"]))
    createSubElement(root_entry, "bank_users", None)
    createSubElement(root_entry, "blacklist", None)
    root_entry[-1].tail = "\n"
    tree = ET.ElementTree(root_entry)
    tree.write(bank_database_folder+username+".xml")
def addNewUserToBank(ownerid, user_obj):
    file = ET.parse(bank_database_folder + ownerid + ".xml")
    time.sleep(0.01)
    user = ET.Element("user", id=user_obj["name"], type=user_obj["type"])
    user.text = user_obj["money"]
    user.tail = "\n\t\t\t\t"
    root = file.find(".//bank_users")
    root.tail = "\n\t\t"
    root.append(user)
    root[-1].tail = "\n\t\t"
    file.write(bank_database_folder + ownerid + ".xml")
    pass
def getBankValue(bankowner, key):
    file = ET.parse(bank_database_folder + bankowner + ".xml")
    time.sleep(0.01)
    element = file.find(".//"+key)
    if element is not None:
        return element.text
def setBankValue(bankowner, key, value):
    file = ET.parse(bank_database_folder + bankowner + ".xml")
    time.sleep(0.01)
    element = file.find(".//"+key)
    if element is not None:
        element.text = value
        file.write(bank_database_folder + bankowner + ".xml")
def getBankList():
    out = []
    for filename in os.listdir(bank_database_folder):
        if "xml" in filename:
            bankid = filename.replace(".xml", "")
            out.append([getBankValue(bankid, "bankname"), getBankValue(bankid, "credit_percent"), getBankValue(bankid, "debit_percent"), bankid])
    return out
def getBankUsers(bankowner):
    out = []
    file = ET.parse(bank_database_folder + bankowner + ".xml")
    time.sleep(0.01)
    users = file.findall(".//bank_users/")
    if users is not None:
        for user in users:
            out.append([user.attrib["id"], user.attrib["type"], user.text])
    return out
def setBankUserValue(bankowner, bankuser, value):
    file = ET.parse(bank_database_folder + bankowner + ".xml")
    time.sleep(0.01)
    users = file.findall(".//bank_users/")
    if users is not None:
        for user in users:
            if user.attrib["id"] == bankuser:
                user.text = str(value)
                file.write(bank_database_folder + bankowner + ".xml")
def getValueByPercent(percent, value):
    return float(percent) / 100 * float(value)

def makeMoney():
    for bank in getBankList():
        bankOwner = bank[3]
        bank_money = int(getBankValue(bankOwner, "money"))
        credit_p = int(getBankValue(bankOwner, "credit_percent"))
        dedit_p = int(getBankValue(bankOwner, "debit_percent"))
        for user in getBankUsers(bankOwner):
            bank_user_name = user[0]
            bank_user_money = int(user[2])
            user_money = int(database.getDBValue(bank_user_name, "eco", "money"))
            if user_money < 0:
                database.setDBValue(bank_user_name, "users", "banned", "1")
            if bank_user_money > 0:
                if user[1] == "credit":
                    summ = round(getValueByPercent(credit_p, bank_user_money))
                    user_money = user_money - summ
                    database.setDBValue(bank_user_name, "eco", "money", str(user_money))
                    setBankValue(bankOwner, "money", str(bank_money + summ))
                    setBankUserValue(bankOwner, bank_user_name, str(bank_user_money - summ))
                    pass
                elif user[1] == "debit":
                    pass
                else:
                    pass
            else:
                print("Skip, user money in bank = 0")
    pass
