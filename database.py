import fileio
import os
import time
from xml.etree import ElementTree as ET


def getDBValue(username, type_name, key):
    if type_name == "user":
        filename = fileio.users_database_folder+username+".xml"
    elif type_name == "eco":
        filename = fileio.economic_database_folder+username+".xml"
    elif type_name == "stats":
        filename = fileio.stats_database_folder+username+".xml"
    elif type_name == "pets":
        filename = fileio.pets_database_folder+username+".xml"
    else:
        return
    file = ET.parse(filename)
    time.sleep(0.01)
    element = file.find(".//"+key)
    if element is None:
        return
    return element.text
def setDBValue(username, type_name, key, value):
    if type_name == "user":
        filename = fileio.users_database_folder+username+".xml"
    elif type_name == "eco":
        filename = fileio.economic_database_folder+username+".xml"
    elif type_name == "stats":
        filename = fileio.stats_database_folder+username+".xml"
    else:
        return
    file = ET.parse(filename)
    time.sleep(0.01)
    element = file.find(".//"+key)
    if element is None:
        return
    element.text = value
    file.write(filename)

def getListUsersWhereValue(type_name, key, value):
    list = []
    if type_name == "user":
        directory = fileio.users_database_folder
    elif type_name == "eco":
        directory = fileio.economic_database_folder
    elif type_name == "stats":
        directory = fileio.stats_database_folder
    elif type_name == "pets":
        directory = fileio.pets_database_folder
    else:
        return
    for filename in os.listdir(directory):
        if "xml" in filename:
            file = ET.parse(directory+filename)
            time.sleep(0.01)
            element = file.find(".//" + key)
            if element is not None:
                if value is not None:
                    if element.text == value:
                        list.append([filename.replace(".xml", ""), element.text])
                else:
                    list.append([filename.replace(".xml", ""), element.text])
    return list