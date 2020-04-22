import os
from xml.etree import ElementTree as ET

users_database_folder = "database/users/"
economic_database_folder = users_database_folder+"economic/"
pets_database_folder = users_database_folder+"pets/"
stats_database_folder = users_database_folder+"stats/"
logs_database_folder = users_database_folder+"logs/"

blank_user_obj = {
    "id":"0",
    "username":"0",
    "name":"0"
}

def createSubElement(element, name, value):
    elem = ET.SubElement(element, name)
    if value is not None:
        elem.text = value
    elem.tail = "\n\t\t"
    return elem

def createUserEntry(user_obj):
    root_entry = ET.Element("user")
    root_entry.tail = "\n\t"
    root_entry.text = "\n\t\t"
    createSubElement(root_entry, "id", str(user_obj["id"]))
    createSubElement(root_entry, "username", user_obj["username"])
    createSubElement(root_entry, "name", user_obj["name"])
    createSubElement(root_entry, "banned", "0")
    createSubElement(root_entry, "admin", "0")
    root_entry[-1].tail = "\n"
    tree = ET.ElementTree(root_entry)
    tree.write(users_database_folder+user_obj["username"]+".xml")

def createEconomicEntry(username):
    root_entry = ET.Element("economic")
    root_entry.tail = "\n\t"
    root_entry.text = "\n\t\t"
    createSubElement(root_entry, "money", "500")
    createSubElement(root_entry, "treasures", "0")
    createSubElement(root_entry, "credit", "0")
    createSubElement(root_entry, "credit_percent", "0")
    createSubElement(root_entry, "credit_timeout_m", "60")
    root_entry[-1].tail = "\n"
    tree = ET.ElementTree(root_entry)
    tree.write(economic_database_folder + username + ".xml")

def createPetsEntry(username):
    root_entry = ET.Element("pets")
    tree = ET.ElementTree(root_entry)
    tree.write(pets_database_folder + username + ".xml")

def createStatsEntry(username):
    root_entry = ET.Element("stat")
    root_entry.tail = "\n\t"
    root_entry.text = "\n\t\t"
    createSubElement(root_entry, "message_count", "0")
    createSubElement(root_entry, "slot_gamed_count", "0")
    createSubElement(root_entry, "sex_command_count", "0")
    createSubElement(root_entry, "money_average_slot_income", "0")
    createSubElement(root_entry, "money_pet_produced", "0")
    createSubElement(root_entry, "money_lost_in_slot", "0")
    createSubElement(root_entry, "money_lost_in_pet", "0")
    root_entry[-1].tail = "\n"
    tree = ET.ElementTree(root_entry)
    tree.write(stats_database_folder + username + ".xml")

def insertUserObj(user_obj):
    if not os.path.exists(users_database_folder+user_obj["username"]+".xml"):
        createUserEntry(user_obj)
        createStatsEntry(user_obj["username"])
        createEconomicEntry(user_obj["username"])
        createPetsEntry(user_obj["username"])
        print("\n\tNew entry for: "+user_obj["username"]+" created SUCCESS!")
    else:
        pass

def getUserList():
    out = []
    for filename in os.listdir(users_database_folder):
        if "xml" in filename:
            user = filename.replace(".xml", "")
            out.append(user)
    return out



def isUserExist(username):
    return os.path.exists(users_database_folder+username+".xml")
def isStatExist(username):
    return os.path.exists(stats_database_folder+username+".xml")
def isEconomicExist(username):
    return os.path.exists(economic_database_folder+username+".xml")
def isPetsExist(username):
    return os.path.exists(pets_database_folder+username+".xml")
def isLogExist(username):
    return os.path.exists(logs_database_folder+username+".txt")
