import time
import database
import fileio
import config
import bot_functions as bf
import bank_func

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




#print(test("pay_tt"))

def showUserStat(bot, username, message):
    UI = "📈 Статистика пользователя @"+username+"👨\n\n"
    if isUserAdmin(username):
        UI += "👑 Это администратор: да"+"\n"
    else:
        UI += "👑 Это администратор: нет"+"\n"
    credit_stat = bank_func.getUserCreditPAndAmount(username)
    UI += "📝 Сообщений написано: " + database.getDBValue(username, "stats", "message_count") + "\n"
    UI += "🎰 Игры сыграно в рулетку: " + str(database.getDBValue(username, "stats", "slot_gamed_count")) + " раз(а)\n"
    UI += "🍓 Использовано 18+ команд: " + str(database.getDBValue(username, "stats", "sex_command_count")) + " раз(а)\n"
    time.sleep(0.1)
    UI += "💶 Баланс: " + database.getDBValue(username, "eco", "money") + "\n"
    UI += "🤑 Кредит: " + credit_stat[1] + "\n"
    UI += "% Процент по кредиту: " + credit_stat[0] + "\n"
    UI += "Взят в банке: " + credit_stat[3] + " | @"+credit_stat[2]+"\n"
    time.sleep(0.1)
    UI += "📈💶 Заработано на питомцах: " + database.getDBValue(username, "stats", "money_pet_produced") + "💶\n"
    UI += "📉💶Потрачено на рулетку: " + database.getDBValue(username, "stats", "money_lost_in_slot") + "💶\n"
    UI += "📉💶Потрачено на питомцев: " + database.getDBValue(username, "stats", "money_lost_in_pet") + "💶\n"
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
