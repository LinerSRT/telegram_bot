import telebot
import time
import threading
import bot_functions as bf
import fileio
import database as db
import banned_func
import user_func
import bank_func
import config
import urllib
import urllib.request
from urllib.request import Request
import re
import random
import user as uf

TOKEN = "1203682284:AAH25R_QUIzaUi5SyIWuzDM1Oc404E2bFLk"
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=8)
uptime = {
    "sec":0,
    "min":0,
    "hour":0
}
GAME_AVAILABLE = True
def bot_updater():
    try:
        bot.polling(True)
    except:
        pass
def rullet_loop():
    global GAME_AVAILABLE
    while True:
        time.sleep(10)
        GAME_AVAILABLE = True
def second_loop():
    while True:
        time.sleep(1)
        uptime["sec"] += 1
def minute_loop():
    while True:
        time.sleep(60)
        uptime["min"] += 1
        for item in bf.message_stack:
            try:
                bot.delete_message(item.chat.id, item.message_id)
            except:
                pass
def hour_loop():
    while True:
        time.sleep(3600)
        uptime["hour"] += 1

def userListener(messages):
    for message in messages:
        username = message.from_user.username
        if username is not None:
            username = username.replace("@", "")
            try:
                if not fileio.isLogExist(username):
                    with open(fileio.logs_database_folder+username+".txt", "w+", encoding='utf8') as logfile:
                        TO_LOG = str(message.chat.first_name) + " [" + str(message.chat.id) + "]: " + message.text
                        logfile.write(TO_LOG+"\n")
                else:
                    with open(fileio.logs_database_folder+username+".txt", "a", encoding='utf8') as logfile:
                        TO_LOG = str(message.chat.first_name) + " [" + str(message.chat.id) + "]: " + message.text
                        logfile.write(TO_LOG + "\n")
                if not fileio.isUserExist(username):
                    user_obj = fileio.blank_user_obj
                    user_obj["id"] = message.from_user.id
                    user_obj["username"] = username
                    user_obj["name"] = message.from_user.first_name
                    fileio.insertUserObj(user_obj)
            except:
                pass
def banListener(messages):
    for message in messages:
        username = message.from_user.username
        if username is not None:
            username = username.replace("@", "")
            if fileio.isUserExist(username):
                if db.getDBValue(username, "user", "banned") == "1":
                    banned_func.processUser(username, bot, message)
                    pass
def messageCounter(messages):
    for message in messages:
        username = message.from_user.username
        if username is not None:
            username = username.replace("@", "")
            if username == "PepegroundBot":
                print("222")
                bot.delete_message(message.chat.id, message.message_id)
            else:
                if fileio.isUserExist(username):
                    if db.getDBValue(username, "user", "banned") != "1":
                        try:
                            target_message_count = int(db.getDBValue(username, "stats", "message_count"))
                            target_message_count += 1
                            db.setDBValue(username, "stats", "message_count", str(target_message_count))
                        except:
                            pass
def newUserListener(messages):
    for message in messages:
        if message.content_type == "new_chat_members":
            chatID = message.chat.id
            newUserID = message.new_chat_member.id
            newUserName = message.new_chat_member.username
            newUserNameT = message.new_chat_member.first_name
            isNewUserBot = message.new_chat_member.is_bot
            if newUserName != "PepegroundBot":
                if bool(isNewUserBot):
                    UI = "Новый бот детектед!  БЛЯДАЖАА\n"
                    UI += "Имя бота: "+newUserNameT+"\n"
                    UI += "Ник бота: @"+newUserName+"\n"
                    bf.SendMessage(bot, message, UI, stack=False, timeout=10)
                    bf.SendMessage(bot, message, "Нам пидоры не нужны, ПАШОЛ НАХУЙ", stack=False, timeout=10)
                    bot.kick_chat_member(chatID, newUserID)

bot.set_update_listener(userListener)
bot.set_update_listener(banListener)
bot.set_update_listener(messageCounter)
bot.set_update_listener(newUserListener)
##################################################################################
@bot.message_handler(content_types=["text"])
def answer(message):
    username = message.from_user.username.replace("@", "")
    print(username)
    if username == "PepegroundBot":
        bot.delete_message(message.chat.id, message.message_id)



##################################################################################
@bot.message_handler(commands=["test2"])
def answer(message):
    username = message.from_user.username.replace("@", "")
    if not user_func.isOwner(username):
        return
    UI = ""
    for item in db.getListUsersWhereValue("eco", "money", None):
        UI += "User: "+item[0]+" | money "+str(item[1])+"\n"
    bf.ReplyTo(bot, message, UI, stack=False, timeout=30)


##################################################################################
@bot.message_handler(commands=["reset"])
def answer(message):
    username = message.from_user.username.replace("@", "")
    if not user_func.isOwner(username):
        return
    UI = ""
    for user in fileio.getUserList():
        db.setDBValue(user, "eco", "money", "1000")
    for item in db.getListUsersWhereValue("eco", "money", None):
        UI += "User: "+item[0]+" | money "+str(item[1])+"\n"
    bf.ReplyTo(bot, message, UI, stack=False, timeout=30)



##################################################################################
@bot.message_handler(commands=["rullet"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    global GAME_AVAILABLE
    if len(message.text.split()) < 2:
        bf.SlotGame(bot, message, game_available=GAME_AVAILABLE)
        GAME_AVAILABLE = False
        return
    bet = int(message.text.split()[1])
    bf.SlotGame(bot, message, game_available=GAME_AVAILABLE, game_bet=bet).start()
    GAME_AVAILABLE = False
##################################################################################
@bot.message_handler(commands=["source"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    bf.ReplyTo(bot, message, "Исодный код - [GitHub](https://github.com/LinerSRT/telegram_bot)", use_markdown=True)
##################################################################################
@bot.message_handler(commands=["newbank"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    username = message.from_user.username.replace("@", "")
    current_user_money = int(db.getDBValue(username, "eco", "money"))
    bank_cost = config.global_economic["bank_cost"]
    if current_user_money < bank_cost:
        bf.ReplyTo(bot, message, "Не хватает денег, заказать банк стоит "+str(bank_cost), stack=False, timeout=3)
        return
    new_bank = bank_func.blank_bank_obj
    db.setDBValue(username, "eco", "money", str(current_user_money - bank_cost))
    bank_func.createBankEntry(username, new_bank)
    UI = "🏦Новый банк создан!\n"
    UI += "\t\tНазвание банка: "+new_bank["bankname"]+"\n"
    UI += "📝Описание банка: "+new_bank["description"]+"\n"
    UI += "💵Процент по кредиту банка: "+new_bank["credit_percent"]+"%\n"
    UI += "💵Процент по дебету банка: "+new_bank["debit_percent"]+"%\n"
    UI += "⏱Время сбора процентов: "+new_bank["time_to_pay"]+"м\n"
    bf.ReplyTo(bot, message, UI, stack=False, timeout=20)
##################################################################################
@bot.message_handler(commands=["setbank"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    username = message.from_user.username.replace("@", "")
    if bank_func.isBankExist(username):
        command = message.text.split()
        if len(command) < 3:
            UI = "Список ключей\n"
            UI += "name - Имя банка\n"
            UI += "desc - Описание банка\n"
            UI += "credit_p - Кредитный процент банка\n"
            UI += "debit_p - Дебетовый процент банка\n"
            UI += "\n\nКоманда /setbank [ключ] [значение]"
            bf.ReplyTo(bot, message, UI, stack=False, timeout=5)
            return
        key = command[1]
        value = command[2]
        if key == "name":
            bank_func.setBankValue(username, "bankname", value)
            pass
        elif key == "desc":
            bank_func.setBankValue(username, "description", value)
            pass
        elif key == "credit_p":
            bank_func.setBankValue(username, "credit_percent", value)
            pass
        elif key == "debit_p":
            bank_func.setBankValue(username, "debit_percent", value)
            pass
        else:
            UI = "Список ключей\n\n"
            UI += "name - Имя банка\n"
            UI += "desc - Описание банка\n"
            UI += "credit_p - Кредитный процент банка\n"
            UI += "debit_p - Дебетовый процент банка\n"
            UI += "\n\nКоманда /setbank [ключ] [значение]"
            bf.ReplyTo(bot, message, UI, stack=False, timeout=20)
            return
        UI = "🏦Ваш банк изменен!\n"
        UI += "\t\tНазвание банка: "+bank_func.getBankValue(username, "bankname")+"\n"
        UI += "📝Описание банка: "+bank_func.getBankValue(username, "description")+"\n"
        UI += "💵Процент по кредиту банка: "+bank_func.getBankValue(username, "credit_percent")+"%\n"
        UI += "💵Процент по дебету банка: "+bank_func.getBankValue(username, "debit_percent")+"%\n"
        bf.ReplyTo(bot, message, UI, stack=False, timeout=20)
    else:
        bf.ReplyTo(bot, message, "Вы не владете банком", stack=False, timeout=3)
##################################################################################
@bot.message_handler(commands=["banks"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    UI = "Список банков:\n"
    for bank in bank_func.getBankList():
        UI += "\n🏦"+bank[0]+" | Кредит под "+bank[1]+"% | Дебет под "+bank[2]+"% | Владелец @"+bank[3]+"\n"
    bf.ReplyTo(bot, message, UI, stack=False, timeout=20)
##################################################################################
@bot.message_handler(commands=["bank_info"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    command = message.text.split()
    if len(command) < 2:
        bf.ReplyTo(bot, message, "Команда введена не правильно. /bank [владелец]. Список банков /banks", stack=False, timeout=5)
        return
    owner = command[1].replace("@", "")
    if bank_func.isBankExist(owner):
        UI = "\t\tНазвание банка: " + bank_func.getBankValue(owner, "bankname") + "\n"
        UI += "📝Описание банка: " + bank_func.getBankValue(owner, "description") + "\n"
        UI += "💵Процент по кредиту банка: " + bank_func.getBankValue(owner, "credit_percent") + "%\n"
        UI += "💵Процент по дебету банка: " + bank_func.getBankValue(owner, "debit_percent") + "%\n"
        UI += "⏱Время сбора процентов: " + bank_func.getBankValue(owner, "time_to_pay") + "м\n"
        bf.ReplyTo(bot, message, UI, stack=False, timeout=20)
    else:
        bf.ReplyTo(bot, message, "Пользователь не владеет банком!", stack=False, timeout=3)
##################################################################################
@bot.message_handler(commands=["mybank"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    username = message.from_user.username.replace("@", "")
    if bank_func.isBankExist(username):
        UI = "\t\tНазвание банка: " + bank_func.getBankValue(username, "bankname") + "\n"
        UI += "📝Описание банка: " + bank_func.getBankValue(username, "description") + "\n"
        UI += "💵Процент по кредиту банка: " + bank_func.getBankValue(username, "credit_percent") + "%\n"
        UI += "💵Процент по дебету банка: " + bank_func.getBankValue(username, "debit_percent") + "%\n"
        UI += "⏱Время сбора процентов: " + bank_func.getBankValue(username, "time_to_pay") + "м\n"
        UI += "💵Баланс банка: " + bank_func.getBankValue(username, "money") + "💵\n"
        UI += "👥Количество пользователей: " + str(len(bank_func.getBankUsers(username))) + "\n"
        if int(len(bank_func.getBankUsers(username))) > 0:
            for user in bank_func.getBankUsers(username):
                UI += "\t\t\t\t👤 @" + str(user[0])
                if user[1] == "credit":
                    UI += " | Кредитный | Сумма "+str(user[2])+"💵"
                else:
                    UI += " | Дебетовый | Баланс "+str(user[2])+"💵"
                UI += "\n"
        bf.ReplyTo(bot, message, UI, stack=False, timeout=20)
    else:
        bf.ReplyTo(bot, message, "У вас нет банка, купить /newbank", stack=False, timeout=3)
##################################################################################
@bot.message_handler(commands=["paytobank"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    username = message.from_user.username.replace("@", "")
    command = message.text.split()
    if len(command) < 3:
        bf.ReplyTo(bot, message, "Команда введена не правильно. /paytobank [владелец] [сумма]. Список банков /banks", stack=False, timeout=5)
        return
    usermoney = int(db.getDBValue(username, "eco", "money"))
    owner = command[1].replace("@", "")
    amount = int(command[2])
    if amount > usermoney:
        bf.ReplyTo(bot, message, "У вас не хватает денег. Ваш баланс: "+str(usermoney)+"💵", stack=False, timeout=5)
        return
    if bank_func.isBankExist(owner):
        bank_money = int(bank_func.getBankValue(owner, "money"))
        if username == owner:
            bank_money = bank_money + amount
            UI = "Вы внесли в свой банк 🏦" + bank_func.getBankValue(owner, "bankname") + " деньги на сумму: "+str(amount)+"💵\n"
            UI += "Баланс вашего банка: "+str(bank_money)+"💵"
            bank_func.setBankValue(owner, "money", str(bank_money))
            db.setDBValue(username, "eco", "money", str(usermoney-amount))
            bf.ReplyTo(bot, message, UI, stack=False, timeout=20)
            return
        if int(len(bank_func.getBankUsers(owner))) > 0:
            for user in bank_func.getBankUsers(owner):
                if username == user[0]:
                    if user[1] == "credit":
                        credit_money = int(user[2])
                        credit_percent = int(bank_func.getBankValue(owner, "credit_percent"))
                        credit_money = credit_money - (amount - round(bank_func.getValueByPercent(credit_percent, amount)))
                        bank_money = bank_money + amount + round(bank_func.getValueByPercent(credit_percent, amount))
                        usermoney = usermoney - (amount - round(bank_func.getValueByPercent(credit_percent, amount)))
                        bank_func.setBankValue(owner, "money", str(bank_money))
                        if credit_money < 0:
                            credit_money = 0
                        bank_func.setBankUserValue(owner, username, credit_money)
                        db.setDBValue(username, "eco", "money", str(usermoney))
                        UI = "Вы заплатили в банк 🏦 @"+owner+"\n"
                        UI += "Платеж: "+str(amount)+"💵 плюс кредит банка "+str(credit_percent)+"% итого списано - "+str(amount - round(bank_func.getValueByPercent(credit_percent, amount)))+"💵\n"
                        UI += "Спасибо что пользуетесь услугами банка: 🏦"+bank_func.getBankValue(owner, "bankname")
                        bf.ReplyTo(bot, message, UI, stack=False, timeout=20)
                        return
                    else:
                        debet_money = int(user[2])
                        debet_money = debet_money + amount
                        bank_money = bank_money + amount
                        usermoney = usermoney - amount
                        bank_func.setBankValue(owner, "money", str(bank_money))
                        bank_func.setBankUserValue(owner, username, debet_money)
                        db.setDBValue(username, "eco", "money", str(usermoney))
                        UI = "Вы внесли в банк 🏦 @"+owner+"\n"
                        UI += "Платеж: "+str(amount)+"💵\n"
                        UI += "Спасибо что пользуетесь услугами банка: 🏦"+bank_func.getBankValue(owner, "bankname")
                        bf.ReplyTo(bot, message, UI, stack=False, timeout=20)
                        return

        UI = "Вы не являетесь пользователем банка 🏦 "+bank_func.getBankValue(owner, "bankname")+" и не можете платить банку"
        bf.ReplyTo(bot, message, UI, stack=False, timeout=5)
    else:
        bf.ReplyTo(bot, message, "Пользователь не владеет банком!", stack=False, timeout=3)
##################################################################################
@bot.message_handler(commands=["getcredit"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    username = message.from_user.username.replace("@", "")
    command = message.text.split()
    if len(command) < 2:
        bf.ReplyTo(bot, message, "Команда введена не правильно. /getcredit [владелец] [сумма]. Список банков /banks", stack=False, timeout=5)
        return
    usermoney = int(db.getDBValue(username, "eco", "money"))
    owner = command[1].replace("@", "")
    amount = int(command[2])
    if bank_func.isBankExist(owner):
        bank_money = int(bank_func.getBankValue(owner, "money"))
        if amount > bank_money:
            bf.ReplyTo(bot, message, "Банк не может выдать вам кредит, у банка нет нужной суммы!", stack=False, timeout=5)
            return
        if username == owner:
            bf.ReplyTo(bot, message, "Вы не можете взять кредит у своего банка", stack=False, timeout=5)
            return
        if int(len(bank_func.getBankUsers(owner))) > 0:
            for user in bank_func.getBankUsers(owner):
                if username == user[0]:
                    if user[1] == "credit":
                        credit_money = int(user[2])
                        credit_percent = int(bank_func.getBankValue(owner, "credit_percent"))
                        credit_money = credit_money + (amount + round(bank_func.getValueByPercent(credit_percent, amount)))
                        bank_money = bank_money - amount
                        usermoney = usermoney + (amount - round(bank_func.getValueByPercent(credit_percent, amount)))
                        bank_func.setBankValue(owner, "money", str(bank_money))
                        bank_func.setBankUserValue(owner, username, credit_money)
                        db.setDBValue(username, "eco", "money", str(usermoney))
                        UI = "Вы успешно взяли кредит в банке 🏦 @"+owner+"\n"
                        UI += "Затребовано: "+str(amount)+"💵\nКредит банка "+str(credit_percent)+"% \nИтого получено - "+str(amount - round(bank_func.getValueByPercent(credit_percent, amount)))+"💵\n"
                        UI += "Спасибо что пользуетесь услугами банка: 🏦"+bank_func.getBankValue(owner, "bankname")+"\n\n"
                        UI += "Ваш баланс: " + str(usermoney) + "💵\n"
                        bf.ReplyTo(bot, message, UI, stack=False, timeout=20)
                        return

        credit_percent = int(bank_func.getBankValue(owner, "credit_percent"))
        credit_money = amount + round(bank_func.getValueByPercent(credit_percent, amount))
        bank_money = bank_money - amount
        usermoney = usermoney + (amount - round(bank_func.getValueByPercent(credit_percent, amount)))
        new_bank_user = bank_func.blank_user_obj
        new_bank_user["name"] = username
        new_bank_user["money"] = str(credit_money)
        bank_func.setBankValue(owner, "money", str(bank_money))
        bank_func.setBankUserValue(owner, username, credit_money)
        db.setDBValue(username, "eco", "money", str(usermoney))
        bank_func.addNewUserToBank(owner, new_bank_user)
        UI = "Вы успешно взяли кредит в банке 🏦 @" + owner + " и стали его участником\n"
        UI += "Затребовано: " + str(amount) + "💵\nКредит банка " + str(credit_percent) + "% \nИтого получено - " + str(
            amount - round(bank_func.getValueByPercent(credit_percent, amount))) + "💵\n"
        UI += "Спасибо что пользуетесь услугами банка: 🏦" + bank_func.getBankValue(owner, "bankname")+"\n\n"
        UI += "Ваш баланс: " + str(usermoney)+"💵\n"
        bf.ReplyTo(bot, message, UI, stack=False, timeout=20)
    else:
        bf.ReplyTo(bot, message, "Такого банка не существует. /getcredit [владелец] [сумма]. Список банков /banks", stack=False, timeout=3)
##################################################################################
@bot.message_handler(commands=["corona"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    req = Request("https://www.worldometers.info/coronavirus", headers={'User-Agent': 'Mozilla/5.0'})
    resource = urllib.request.urlopen(req)
    content =  resource.read().decode(resource.headers.get_content_charset())
    corona_cases_count = re.search(r'Coronavirus Cases:[a-zA-Z<>\": 0-9\/\n=\-#]*>([0-9, ]*)<', content).group(1)
    corona_death_count = re.search(r'Deaths:[a-zA-Z<>\": 0-9\/\n=\-#]*>([0-9, ]*)<', content).group(1)
    corona_survive_count = re.search(r'Recovered:[a-zA-Z<>\": 0-9\/\n=\-#]*>([0-9, ]*)<', content).group(1)
    result = "Ситуация в 🌎 мире на данный момент\n"
    result += "🦠 Заражено: "+corona_cases_count+"\n"
    result += "☠ Умерло: "+corona_death_count+"\n"
    result += "＋ Выздоровело: "+corona_survive_count+"\n"
    result += "-----------\n"
    result += "НАМ ВСЕМ ПИЗДА!\n"
    bf.ReplyTo(bot, message, result, stack=False, timeout=20)
##################################################################################
@bot.message_handler(commands=["corona_uk"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    req = Request("https://www.worldometers.info/coronavirus/country/ukraine", headers={'User-Agent': 'Mozilla/5.0'})
    resource = urllib.request.urlopen(req)
    content =  resource.read().decode(resource.headers.get_content_charset())
    corona_cases_count = re.search(r'Coronavirus Cases:[a-zA-Z<>\": 0-9\/\n=\-#]*>([0-9, ]*)<', content).group(1)
    corona_death_count = re.search(r'Deaths:[a-zA-Z<>\": 0-9\/\n=\-#]*>([0-9, ]*)<', content).group(1)
    corona_survive_count = re.search(r'Recovered:[a-zA-Z<>\": 0-9\/\n=\-#]*>([0-9, ]*)<', content).group(1)
    result = "Ситуация в 🇺🇦 Украине на данный момент\n"
    result += "🦠 Заражено: "+corona_cases_count+"\n"
    result += "☠ Умерло: "+corona_death_count+"\n"
    result += "＋ Выздоровело: "+corona_survive_count+"\n"
    bf.ReplyTo(bot, message, result, stack=False, timeout=20)
##################################################################################
@bot.message_handler(commands=["corona_ru"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    req = Request("https://www.worldometers.info/coronavirus/country/russia", headers={'User-Agent': 'Mozilla/5.0'})
    resource = urllib.request.urlopen(req)
    content =  resource.read().decode(resource.headers.get_content_charset())
    corona_cases_count = re.search(r'Coronavirus Cases:[a-zA-Z<>\": 0-9\/\n=\-#]*>([0-9, ]*)<', content).group(1)
    corona_death_count = re.search(r'Deaths:[a-zA-Z<>\": 0-9\/\n=\-#]*>([0-9, ]*)<', content).group(1)
    corona_survive_count = re.search(r'Recovered:[a-zA-Z<>\": 0-9\/\n=\-#]*>([0-9, ]*)<', content).group(1)
    result = "Ситуация в 🇷🇺 России на данный момент\n"
    result += "🦠 Заражено: "+corona_cases_count+"\n"
    result += "☠ Умерло: "+corona_death_count+"\n"
    result += "＋ Выздоровело: "+corona_survive_count+"\n"
    bf.ReplyTo(bot, message, result, stack=False, timeout=20)
##################################################################################
@bot.message_handler(commands=['showgif'])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    if user_func.isUserAdmin(message.from_user.username):
        try:
            req = Request("http://www.gifporntube.com/gifs/"+str(random.randint(20, 2000))+".html", headers={'User-Agent': 'Mozilla/5.0'})
            resource = urllib.request.urlopen(req)
            content = resource.read().decode(resource.headers.get_content_charset())
            urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+([/a-z_0-9]*.mp4)', content)
            markdown = "[ᅠ](http://www.gifporntube.com" + str(urls[0]) + ")"
            usage_count = int(db.getDBValue(message.from_user.username, "stats", "sex_command_count"))
            usage_count += 1
            db.setDBValue(message.from_user.username, "stats", "sex_command_count", str(usage_count))
            bot.delete_message(message.chat.id, message.message_id)
            bf.ReplyTo(bot, message, markdown, stack=False, timeout=6)
        except:
            bf.ReplyTo(bot, message, "Временно не доступно", stack=False, timeout=3)
    else:
        bf.ReplyTo(bot, message, "Достпуно только для админов, соси бибу", stack=False, timeout=3)
##################################################################################
@bot.message_handler(commands=['showpic'])
def send_photo(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    if user_func.isUserAdmin(message.from_user.username):
        try:
            usage_count = int(db.getDBValue(message.from_user.username, "stats", "sex_command_count"))
            usage_count += 1
            db.setDBValue(message.from_user.username, "stats", "sex_command_count", str(usage_count))
            markdown = "[ᅠ](https://www.scrolller.com/media/" + str(random.randint(20, 2000)) + ".jpg)"
            usage_count = int(db.getDBValue(message.from_user.username, "stats", "sex_command_count"))
            usage_count += 1
            db.setDBValue(message.from_user.username, "stats", "sex_command_count", str(usage_count))
            bot.delete_message(message.chat.id, message.message_id)
            bf.ReplyTo(bot, message, markdown, stack=False, timeout=6)
        except:
            bf.ReplyTo(bot, message, "Временно не доступно", stack=False, timeout=3)
    else:
        bf.ReplyTo(bot, message, "Достпуно только для админов, соси бибу", stack=False, timeout=3)
##################################################################################
@bot.message_handler(commands=["balance"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    username = message.from_user.username.replace("@", "")
    bf.ReplyTo(bot, message, "💵 Ваш баланс - "+str(db.getDBValue(username, "eco", "money")), stack=False, timeout=20)
##################################################################################
@bot.message_handler(commands=["rullet_bank"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    values = db.getListUsersWhereValue("stats", "money_lost_in_slot", None)
    out = 0
    for item in values:
        out += int(item[1])
    UI = "Рулетка заработала на пользователях: " + str(out) + "💶"
    bf.ReplyTo(bot, message, UI, stack=False, timeout=20)
##################################################################################
@bot.message_handler(commands=["total_messages"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    values = db.getListUsersWhereValue("stats", "message_count", None)
    out = 0
    for item in values:
        out += int(item[1])
    UI = "Всего сообщений получено ботом: "+str(out)+"🧾"
    bf.ReplyTo(bot, message, UI, stack=False, timeout=20)
##################################################################################
@bot.message_handler(commands=["set"])
def answer(message):
    if user_func.isOwner(message.from_user.username.replace("@", "")):
        target = message.text.split(maxsplit=4)[1].replace("@", "")
        obj = message.text.split(maxsplit=4)[2]
        key = message.text.split(maxsplit=4)[3]
        value = message.text.split(maxsplit=4)[4]
        if fileio.isUserExist(target):
            db.setDBValue(target, obj, key, value)
            bf.ReplyTo(bot, message, "Значение "+key+" у "+target+" теперь - "+value, stack=False, timeout=3)
        else:
            bf.ReplyTo(bot, message, "Данного пользователя нет в базе данных", stack=False, timeout=3)
    else:
        bf.ReplyTo(bot, message, "Доступно только создателю", stack=False, timeout=3)
##################################################################################
@bot.message_handler(commands=['help'])
def command_help(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    help_text = "\n"
    for key in config.commands:
        help_text += key + "   :  "
        help_text += config.commands[key] + "\n"
    help_text += "\n\n▫ - доступно всем \n🔸 - доступно только админам\n🔺 - доступно только создателю"
    help_text += "\n\n ❗️❗️❗️❗️❗️АХТУНГ! ВАРНИНГ! Если вы взяли кредит в банке и не можете его оплатить вовремя, вы попадете в БАН БОТА. Подумайте перед тем как брать кредит!!!"
    bf.ReplyTo(bot, message, "Привет, @" + str(message.from_user.username) + " рад снова тебя видеть. Вот что я могу:\n" + help_text)
##################################################################################
@bot.message_handler(commands=["uptime"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    bf.ReplyTo(bot, message, "Ебашу на благо общества уже:  ⏱ "+str(uptime["sec"])+" секунд(ы) или "+""+str(uptime["min"])+" минут(ы)", stack=False, timeout=10)
##################################################################################
@bot.message_handler(commands=["ban_user"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    try:
        user_func.banUser(bot, message)
    except:
        bf.ReplyTo(bot, message,  "Команда введена не правильно. /ban_user [никнейм]", stack=False, timeout=3)
##################################################################################
@bot.message_handler(commands=["unban_user"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    try:
        user_func.unBanUser(bot, message)
    except:
        bf.ReplyTo(bot, message,  "Команда введена не правильно. /unban_user [никнейм]", stack=False, timeout=3)
##################################################################################
@bot.message_handler(commands=["add_admin"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    try:
        user_func.addAdmin(bot, message)
    except:
        bf.ReplyTo(bot, message,  "Команда введена не правильно. /add_admin [никнейм]", stack=False, timeout=3)
##################################################################################
@bot.message_handler(commands=["del_admin"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    try:
        user_func.delAdmin(bot, message)
    except:
        bf.ReplyTo(bot, message,  "Команда введена не правильно. /del_admin [никнейм]", stack=False, timeout=3)
##################################################################################
@bot.message_handler(commands=["admin_list"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    try:
        bf.ReplyTo(bot, message,  "Список администраторов:\n"+user_func.getAdminList(), stack=False, timeout=20)
    except:
        pass
##################################################################################
@bot.message_handler(commands=["banlist"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    try:
        bf.ReplyTo(bot, message, "Список забаненых:\n"+user_func.getBanList(), stack=False, timeout=20)
    except:
        pass
##################################################################################
@bot.message_handler(commands=["prices"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    help_text = "\n"
    for key in config.global_economic_desc:
        help_text += key + ":  "
        help_text += config.global_economic_desc[key] + "\n\n"
    bf.ReplyTo(bot, message, "Привет, @" + str(message.from_user.username) + " рад снова тебя видеть. \nВот актуальные цены бота:\n" + help_text, stack=False, timeout=20)
##################################################################################
@bot.message_handler(commands=["my_stat"])
def answer(message):
    username = message.from_user.username
    if username is not None:
        if not user_func.userCanUseCommand(message.from_user.username):
            bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
            return
        user_func.showUserStat(bot, username, message)
    else:
        bf.ReplyTo(bot, message, "У вас нет никнейма, установите его себе в настройках", stack=False, timeout=3)
##################################################################################
@bot.message_handler(commands=["stat_for"])
def answer(message):
    username = message.from_user.username
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    if not user_func.isUserAdmin(username):
        bf.ReplyTo(bot, message, "Доступно только администраторам", stack=False, timeout=3)
        return
    try:
        target = message.text.split(maxsplit=1)[1].replace("@", "")
        user_func.showUserStat(bot, target, message)
    except:
        bf.ReplyTo(bot, message, "Команда введена не правильно. /stat_for [никнейм]", stack=False, timeout=3)
##################################################################################
@bot.message_handler(commands=["payto"])
def answer(message):
    username = message.from_user.username.replace("@", "")
    if not user_func.userCanUseCommand(username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    try:
        current_user = username.replace("@", "")
        amount = int(message.text.split()[2])
        target_user = message.text.split()[1].replace("@", "")
        current_user_money = int(db.getDBValue(current_user, "eco", "money"))
        target_user_money = int(db.getDBValue(target_user, "eco", "money"))
        if current_user_money < amount:
            bf.ReplyTo(bot, message, "Не достаточно денег, ваш баланс 💵"+str(current_user_money), stack=False, timeout=5)
            return
        if current_user == target_user:
            bf.ReplyTo(bot, message, "Нельзя отправить деньги самому себе", stack=False, timeout=5)
            return
        else:
            if not fileio.isUserExist(target_user):
                bf.ReplyTo(bot, message, "Такого пользователя нет в базе!", stack=False, timeout=5)
                return
            try:
                db.setDBValue(current_user, "eco", "money", str(current_user_money - amount))
                db.setDBValue(target_user, "eco", "money", str(target_user_money + amount))
                UI = "Отправка денег @"+target_user+"\n"
                UI += " -> Отправлено: "+str(amount)+"\n"
                UI += "💵 Ваш баланс: "+str(current_user_money-amount)
                bf.ReplyTo(bot, message, UI, stack=False, timeout=20)
            except:
                bf.ReplyTo(bot, message, "Ошибка, попробуй позже", stack=False, timeout=3)
    except:
        bf.ReplyTo(bot, message, "Команда введена не правильно, /payto [кому] [сколько]", stack=False, timeout=3)

##################################################################################
@bot.message_handler(commands=["give_money"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    try:
        username = message.from_user.username.replace("@", "")
        if user_func.isOwner(username):
            command = int(message.text.split()[1])
            for user in fileio.getUserList():
                current_money = int(db.getDBValue(username, "eco", "money"))
                db.setDBValue(user, "eco", "money", str(current_money+command))
            bf.ReplyTo(bot, message, "Все пользователи получили +"+str(command)+"💵", stack=False, timeout=20)
    except:
        bf.ReplyTo(bot, message,  "Команда введена не правильно. /make_money", stack=False, timeout=3)
##################################################################################
@bot.message_handler(commands=["grab_money"])
def answer(message):
    if not user_func.userCanUseCommand(message.from_user.username):
        bf.ReplyTo(bot, message, "Соси бибу, ты забанен", stack=False, timeout=3)
        return
    try:
        username = message.from_user.username.replace("@", "")
        if user_func.isOwner(username):
            command = int(message.text.split()[1])
            for user in fileio.getUserList():
                current_money = int(db.getDBValue(username, "eco", "money"))
                db.setDBValue(user, "eco", "money", str(current_money-command))
            bf.ReplyTo(bot, message, "Все пользователи потеряли -"+str(command)+"💵", stack=False, timeout=20)
    except:
        bf.ReplyTo(bot, message,  "Команда введена не правильно. /make_money", stack=False, timeout=3)
##################################################################################




















if __name__ == '__main__':
    threading.Thread(name="botUpdater", target=bot_updater, args=()).start()
    threading.Thread(name="secondLoop", target=second_loop, args=()).start()
    threading.Thread(name="rullet_loop", target=rullet_loop, args=()).start()
    threading.Thread(name="minuteLoop", target=minute_loop, args=()).start()
    threading.Thread(name="hourLoop", target=hour_loop, args=()).start()

