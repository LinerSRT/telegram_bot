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
    elif type_name == "pets":
        filename = fileio.pets_database_folder+username+".xml"
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




def addPet(username, petname, petid):
    if fileio.isPetsExist(username):
        pet = ET.Element("pet", id=petid)
        pet.tail = "\n\t"
        pet.text = "\n\t\t"
        fileio.createSubElement(pet, "pet_name", petname)
        fileio.createSubElement(pet, "pet_avatar", "🐱")
        fileio.createSubElement(pet, "pet_food", "100")
        fileio.createSubElement(pet, "pet_food_auto", "0")
        fileio.createSubElement(pet, "pet_water", "100")
        fileio.createSubElement(pet, "pet_water_auto", "0")
        fileio.createSubElement(pet, "pet_have_house", "0")
        fileio.createSubElement(pet, "pet_house_level", "1")
        fileio.createSubElement(pet, "pet_passive_produce", "200")
        fileio.createSubElement(pet, "pet_passive_produce_timeout_m", "60")
        fileio.createSubElement(pet, "pet_exp", "0")
        fileio.createSubElement(pet, "pet_level", "1")
        fileio.createSubElement(pet, "pet_unique_treasure", "0")
        fileio.createSubElement(pet, "pet_died", "0")
        pet[-1].tail = "\n\t"
        file = ET.parse(fileio.pets_database_folder+username+".xml")
        time.sleep(0.01)
        root = file.getroot()
        root.append(pet)
        file.write(fileio.pets_database_folder+username+".xml")

def getPetValue(username, petid, key):
    if not fileio.isPetsExist(username):
        return
    file = ET.parse(fileio.pets_database_folder + username + ".xml")
    time.sleep(0.01)
    element = file.find(".//pet[@id=\""+petid+"\"]/"+key)
    return element.text


def setPetValueByPos(username, position, key, value):
    if not fileio.isPetsExist(username):
        return
    file = ET.parse(fileio.pets_database_folder + username + ".xml")
    time.sleep(0.01)
    element = file.find(".//pet[@id=\""+position+"\"]/"+key)
    if element is None:
        return False
    element.text = value
    file.write(fileio.pets_database_folder+username+".xml")
    return True

def isPetExist(username, petid):
    file = ET.parse(fileio.pets_database_folder + username + ".xml")
    time.sleep(0.01)
    return file.find(".//pet[@id=\""+petid+"\"]")


def getListPetsByUserName(username):
    out_list = []
    file = ET.parse(fileio.pets_database_folder + username + ".xml")
    time.sleep(0.01)
    element = file.findall(".//pet")
    if element is None:
        return None
    for item in element:
        if item is not None:
            petID = item.attrib["id"]
            petName = item.find("pet_name").text
            out_list.append([petID, petName])
    return out_list


#addPet("Llne_R", "tes2t", "2")
#print((getPetValue("Llne_R", "2", "pet_name")))
#setPetValueByPos("Llne_R", "2", "pet_name", "name_Testtttt")
#print((getPetValue("Llne_R", "2", "pet_name")))


#print(getUserValue("Llne_R", "user", "admin"))
#setUserValue("Llne_R", "user", "admin", "1")
#print(getUserValue("Llne_R", "user", "admin"))