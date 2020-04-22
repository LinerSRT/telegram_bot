import time
import database
import fileio
import config
import bot_functions as bf

def userCanUseCommand(username):
    if database.getDBValue(username, "user", "banned") == "1":
        return False
    else:
        return True

def isUserAdmin(username):
    if database.getDBValue(username, "user", "admin") == "1":
        return True
    else:
        return False

def banUser(bot, message):
    username = message.from_user.username.replace("@", "")
    target = message.text.split(maxsplit=1)[1].replace("@", "")
    if isUserAdmin(username):
        database.setDBValue(target, "user", "banned", "1")
        bf.ReplyTo(bot, message, "Теперь @*" + target + "* сосет бибу", stack=False, timeout=3, use_markdown=True)
    else:
        bf.ReplyTo(bot, message, "Доступно только администраторам", stack=False, timeout=3, use_markdown=True)

def unBanUser(bot, message):
    username = message.from_user.username.replace("@", "")
    target = message.text.split(maxsplit=1)[1].replace("@", "")
    if isUserAdmin(username):
        database.setDBValue(target, "user", "banned", "0")
        bf.ReplyTo(bot, message, "Теперь @*" + target + "* не будет сосет бибу", stack=False, timeout=3, use_markdown=True)
    else:
        bf.ReplyTo(bot, message, "Доступно только администраторам", stack=False, timeout=3, use_markdown=True)


def addAdmin(bot, message):
    username = message.from_user.username.replace("@", "")
    target = message.text.split(maxsplit=1)[1].replace("@", "")
    if isUserAdmin(username):
        database.setDBValue(target, "user", "admin", "1")
        bf.ReplyTo(bot, message, "Теперь 👑 *" + target + "* администратор", stack=False, timeout=3, use_markdown=True)
    else:
        bf.ReplyTo(bot, message, "Доступно только администраторам", stack=False, timeout=3)

def delAdmin(bot, message):
    username = message.from_user.username.replace("@", "")
    target = message.text.split(maxsplit=1)[1].replace("@", "")
    if isOwner(username):
        database.setDBValue(target, "user", "admin", "0")
        bf.ReplyTo(bot, message, "Теперь *" + target + "* больше не администратор", stack=False, timeout=3, use_markdown=True)
    else:
        bf.ReplyTo(bot, message, "Доступно только администраторам", stack=False, timeout=3)


def showUserStat(bot, username, message):
    if not fileio.isUserExist(username):
        warn_message = bot.reply_to(message, "Пользователя еще нет в базе")
        time.sleep(3)
        bot.delete_message(message.chat.id, warn_message.message_id)
        return

    UI = "📈 Статистика пользователя @"+username+"👨\n\n"
    if isUserAdmin(username):
        UI += "👑 Это администратор: да"+"\n"
    else:
        UI += "👑 Это администратор: нет"+"\n"
    UI += "📝 Сообщений написано: " + database.getDBValue(username, "stats", "message_count") + "\n"
    UI += "🎰 Игры сыграно в рулетку: " + str(database.getDBValue(username, "stats", "slot_gamed_count")) + " раз(а)\n"
    UI += "🍓 Использовано 18+ команд: " + str(database.getDBValue(username, "stats", "sex_command_count")) + " раз(а)\n"
    time.sleep(0.1)
    UI += "💶 Баланс: " + database.getDBValue(username, "eco", "money") + "\n"
    UI += "🤑 Кредит: " + database.getDBValue(username, "eco", "credit") + "\n"
    UI += "% Процент по кредиту: " + database.getDBValue(username, "eco", "credit_percent") + "\n"
    time.sleep(0.1)
    UI += "📈💰 Заработано на питомцах: " + database.getDBValue(username, "stats", "money_pet_produced") + "💶\n"
    UI += "📉💰Потрачено на рулетку: " + database.getDBValue(username, "stats", "money_lost_in_slot") + "💶\n"
    UI += "📉💰Потрачено на питомцев: " + database.getDBValue(username, "stats", "money_lost_in_pet") + "💶\n"
    bf.ReplyTo(bot, message, UI, stack=False, timeout=20)

def getBanList():
    output = ""
    for user in database.getListUsersWhereValue("user", "banned", "1"):
            output += "💀 @" + user[0]+"\n"
    return output


def getAdminList():
    output = ""
    for user in database.getListUsersWhereValue("user", "admin", "1"):
            output += "👑 " + user[0]+"\n"
    return output


def isOwner(user):
    if user == "Llne_R":
        return True
    else:
        return False


def getUserPets(bot, message):
    username = message.from_user.username.replace("@", "")
    UI = "Ваши питомцы: \n\n"
    if len(database.getListPetsByUserName(username)) == 0:
        bf.ReplyTo(bot, message, "У вас нет питомцев, купить /buy_pet [ид питомца] [имя питомца]", stack=False, timeout=3)
        return
    for pet in database.getListPetsByUserName(username):
        UI += "ID["+pet[0]+"] "+str(database.getPetValue(username, str(pet[0]), "pet_avatar"))+" "+str(pet[1])+"\n"
    bf.ReplyTo(bot, message, UI, stack=False, timeout=10)


def getPetStat(bot, message):
    username = message.from_user.username.replace("@", "")
    try:
        target_pet_id = message.text.split()[1]
        if len(database.getListPetsByUserName(username)) != 0:
            if database.isPetExist(username, target_pet_id) is not None:
                UI = "Состояние \n\n"
                UI += "Владелец: @" + str(username) + "\n"
                UI += "▫️Аватар питомца: " + str(
                    database.getPetValue(username, target_pet_id, "pet_avatar")) + "\n"
                UI += "▫️Имя питомца: " + str(database.getPetValue(username, target_pet_id, "pet_name")) + "\n"
                UI += "🍗 Еда питомца: " + str(database.getPetValue(username, target_pet_id, "pet_food")) + "\n"
                UI += "💧 Вода питомца: " + str(database.getPetValue(username, target_pet_id, "pet_water")) + "\n"
                UI += "🍗🍗🍗 Избыток еды: " + str(
                    database.getPetValue(username, target_pet_id, "pet_food_auto")) + "\n"
                UI += "💧💧💧 Избыток воды: " + str(
                    database.getPetValue(username, target_pet_id, "pet_water_auto")) + "\n"
                UI += "🏠 У питомца есть дом: " + str(
                    database.getPetValue(username, target_pet_id, "pet_have_house")) + "\n"
                UI += "🏠📊 Уровень дома питомца: " + str(
                    database.getPetValue(username, target_pet_id, "pet_house_level")) + "\n"
                UI += "💵 Пассивный доход с питомца: " + str(
                    database.getPetValue(username, target_pet_id, "pet_passive_produce")) + "\n"
                UI += "⏱💵 Тайм-аут дохода в минутах: " + str(
                    database.getPetValue(username, target_pet_id, "pet_passive_produce_timeout_m")) + "\n"
                UI += "📊 Уровень питомца: " + str(
                    database.getPetValue(username, target_pet_id, "pet_level")) + "\n"
                UI += "🌟 Опыт питомца: " + str(database.getPetValue(username, target_pet_id, "pet_exp")) + "\n"
                UI += "💎 Найдено сокровищ питомцем: " + str(
                    database.getPetValue(username, target_pet_id, "pet_unique_treasure")) + "\n"
                bf.ReplyTo(bot, message, UI, stack=False, timeout=10)
            else:
                bf.ReplyTo(bot, message, "Такого питомца не существует, посмотреть список питомцев /mypets", stack=False, timeout=3)
        else:
            bf.ReplyTo(bot, message, "У вас нет ни одного питомца, купить /buy_pet [ид питомца] [имя питомца]", stack=False, timeout=3)
    except:
        bf.ReplyTo(bot, message, "Команда введена не правильно. /pet [ид]", stack=False, timeout=3)

def buyPet(bot, message):
    username = message.from_user.username.replace("@", "")
    if fileio.isUserExist(username):
        user_money = int(database.getDBValue(username, "eco", "money"))
        pet_cost = config.global_economic["pet_cost"]
        if user_money < pet_cost:
            UI = "У вас не достаточно денег для покупки!\n"
            UI += "Цена нового питомца составляет: "+str(pet_cost)+"💵\n"
            UI += "💰Ваш баланс: "+str(user_money)+"\n"
            bf.ReplyTo(bot, message, UI, stack=False, timeout=10)
            return
        try:
            target_pet_id = message.text.split()[1]
            target_pet_name = message.text.split()[2]
            pet_count = len(database.getListPetsByUserName(username))
            if pet_count == 0:
                pet_count = 1
            user_money = user_money - (pet_cost*pet_count)
            database.setDBValue(username,"user", "money", str(user_money))
            database.addPet(username, target_pet_name, target_pet_id)
            time.sleep(1)
            UI = "Вы успешно купили нового питомца 👍\n"
            UI += "💵 Списано со счета "+str((pet_cost*pet_count))+" \n\n"
            UI += "💵 Цена = количество * стандартная цена (3000💵 ) \n"
            UI += "💰 Баланс " + str(database.getDBValue(username, "money")) + " \n"
            UI += "Состояние \n\n"
            UI += "Владелец: @" + str(username) + "\n"
            UI += "▫️Аватар питомца: " + str(database.getPetValue(username, target_pet_id, "pet_avatar")) + "\n"
            UI += "▫️Имя питомца: " + str(database.getPetValue(username, target_pet_id, "pet_name")) + "\n"
            UI += "🍗 Еда питомца: " + str(database.getPetValue(username, target_pet_id, "pet_food")) + "\n"
            UI += "💧 Вода питомца: " + str(database.getPetValue(username, target_pet_id, "pet_water")) + "\n"
            UI += "🍗🍗🍗 Избыток еды: " + str(database.getPetValue(username, target_pet_id, "pet_food_auto")) + "\n"
            UI += "💧💧💧 Избыток воды: " + str(
                database.getPetValue(username, target_pet_id, "pet_water_auto")) + "\n"
            UI += "🏠 У питомца есть дом: " + str(
                database.getPetValue(username, target_pet_id, "pet_have_house")) + "\n"
            UI += "🏠📊 Уровень дома питомца: " + str(
                database.getPetValue(username, target_pet_id, "pet_house_level")) + "\n"
            UI += "💵 Пассивный доход с питомца: " + str(
                database.getPetValue(username, target_pet_id, "pet_passive_produce")) + "\n"
            UI += "⏱💵 Тайм-аут дохода в минутах: " + str(
                database.getPetValue(username, target_pet_id, "pet_passive_produce_timeout_m")) + "\n"
            UI += "📊 Уровень питомца: " + str(database.getPetValue(username, target_pet_id, "pet_level")) + "\n"
            UI += "🌟 Опыт питомца: " + str(database.getPetValue(username, target_pet_id, "pet_exp")) + "\n"
            UI += "💎 Найдено сокровищ питомцем: " + str(database.getPetValue(username, target_pet_id, "pet_unique_treasure")) + "\n"
            bf.ReplyTo(bot, message, UI, stack=False, timeout=10)
        except:
            bf.ReplyTo(bot, message, "Команда введена не правильно. /buy_pet [ид питомца] [имя питомца]\n ID используется для обращения к конкретному питомцу", stack=False, timeout=3)

def setPetName(bot, message):
    username = message.from_user.username.replace("@", "")
    try:
        target_pet_id = message.text.split()[1]
        target_value = message.text.split()[2]
        if len(database.getListPetsByUserName(username)) != 0:
            if database.isPetExist(username, target_pet_id) is not None:
                user_money = int(database.getDBValue(username, "eco", "money"))
                change_name_cost = config.global_economic["pet_change_name_cost"]
                UI = ""
                if user_money < change_name_cost:
                    UI = "У вас не достаточно денег для смены имени!\n"
                    UI += "Цена смены составляет: " + str(change_name_cost) + "💵\n"
                    UI += "💰 Ваш баланс: " + str(user_money) + "\n"
                    bf.ReplyTo(bot, message, UI, stack=False, timeout=10)
                    return
                lost_current = int(database.getDBValue(username, "stats", "money_lost_in_pet"))
                lost = lost_current + (config.global_economic["pet_change_name_cost"])
                database.setDBValue(username, "stats", "money_lost_in_pet", str(lost))
                user_money = user_money - change_name_cost
                database.setDBValue(username, "eco", "money", str(user_money))
                database.setPetValueByPos(username, target_pet_id, "pet_name", target_value)
                UI += "Изменено:\n"
                UI += "▫️Имя питомца: " + str(database.getPetValue(username, target_pet_id, "pet_name")) + "\n"
                bf.ReplyTo(bot, message, UI, stack=False, timeout=10)
            else:
                bf.ReplyTo(bot, message, "Такого питомца не существует, посмотреть список питомцев /mypets", stack=False, timeout=3)
        else:
            bf.ReplyTo(bot, message, "У вас нет ни одного питомца, купить /buy_pet [ид питомца] [имя питомца]", stack=False, timeout=3)
    except:
        bf.ReplyTo(bot, message, "Команда введена не правильно. /pet_setname [ид] [имя]", stack=False, timeout=3)

def setPetAvatar(bot, message):
    username = message.from_user.username.replace("@", "")
    try:
        target_pet_id = message.text.split()[1]
        target_value = message.text.split()[2]
        if len(database.getListPetsByUserName(username)) != 0:
            if database.isPetExist(username, target_pet_id) is not None:
                user_money = int(database.getDBValue(username, "eco", "money"))
                change_name_cost = config.global_economic["pet_change_avatar_cost"]
                UI = ""
                if user_money < change_name_cost:
                    UI = "У вас не достаточно денег для смены аватара!\n"
                    UI += "Цена смены составляет: " + str(change_name_cost) + "💵\n"
                    UI += "💰 Ваш баланс: " + str(user_money) + "\n"
                    bf.ReplyTo(bot, message, UI, stack=False, timeout=10)
                    return
                lost_current = int(database.getDBValue(username, "stats", "money_lost_in_pet"))
                lost = lost_current + (config.global_economic["pet_change_avatar_cost"])
                database.setDBValue(username, "stats", "money_lost_in_pet", str(lost))
                user_money = user_money - change_name_cost
                database.setDBValue(username, "eco", "money", str(user_money))
                database.setPetValueByPos(username, target_pet_id, "pet_avatar", target_value)

                UI += "Изменено:\n"
                UI += "▫ Аватар питомца: " + str(database.getPetValue(username, target_pet_id, "pet_avatar")) + "\n"
                bf.ReplyTo(bot, message, UI, stack=False, timeout=10)
            else:
                bf.ReplyTo(bot, message, "Такого питомца не существует, посмотреть список питомцев /mypets", stack=False, timeout=3)
        else:
            bf.ReplyTo(bot, message, "У вас нет ни одного питомца, купить /buy_pet [ид питомца] [имя питомца]", stack=False, timeout=3)
    except:
        bf.ReplyTo(bot, message, "Команда введена не правильно. /pet_setavatar [ид] [смайл]", stack=False, timeout=3)
