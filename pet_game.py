import database
import fileio
import time
import random
import config
import os



counter = 0

def gameLoop():
    global counter
    counter += 1
    if counter >= 10:
        for users in os.listdir(fileio.pets_database_folder):
            if "xml" in users:
                username = users.replace(".xml", "")
                for pet in database.getListPetsByUserName(username):
                    petID = pet[0]
                    pet_food = int(database.getPetValue(username, petID, "pet_food"))
                    pet_food_auto = int(database.getPetValue(username, petID, "pet_food_auto"))
                    pet_water = int(database.getPetValue(username, petID, "pet_water"))
                    pet_water_auto = int(database.getPetValue(username, petID, "pet_water_auto"))
                    pet_have_house = int(database.getPetValue(username, petID, "pet_have_house"))
                    pet_house_level = int(database.getPetValue(username, petID, "pet_house_level"))
                    pet_passive_produce = int(database.getPetValue(username, petID, "pet_passive_produce"))
                    pet_passive_produce_timeout_m = int(database.getPetValue(username, petID, "pet_passive_produce_timeout_m"))
                    pet_exp = int(database.getPetValue(username, petID, "pet_exp"))
                    pet_level = int(database.getPetValue(username, petID, "pet_level"))
                    pet_unique_treasure = int(database.getPetValue(username, petID, "pet_unique_treasure"))
                    pet_died = int(database.getPetValue(username, petID, "pet_died"))
                    UI = "\n\n Pet "+str(petID)+" for "+username+"\n"
                    UI += "pet_food: "+str(pet_food)+"\n"
                    UI += "pet_food_auto: "+str(pet_food_auto)+"\n"
                    UI += "pet_water: "+str(pet_water)+"\n"
                    UI += "pet_water_auto: "+str(pet_water_auto)+"\n"
                    UI += "pet_have_house: "+str(pet_have_house)+"\n"
                    UI += "pet_house_level: "+str(pet_house_level)+"\n"
                    UI += "pet_passive_produce: "+str(pet_passive_produce)+"\n"
                    UI += "pet_passive_produce_timeout_m: "+str(pet_passive_produce_timeout_m)+"\n"
                    UI += "pet_exp: "+str(pet_exp)+"\n"
                    UI += "pet_level: "+str(pet_level)+"\n"
                    UI += "pet_unique_treasure: "+str(pet_unique_treasure)+"\n"



                    #print(UI)
                #database.getPetValue()
                pass
        counter = 0


    print("game loop")
    pass

