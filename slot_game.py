import database
import user_func
import random
import time
import config
import bot

slot_items = [
    "🍏",
    "🍋",
    "🍇",
    "🍒",
    "7️⃣"
]
items_spawn_rate = [
    80,
    40,
    30,
    10,
    5
]

def randomizeItem(items, spawn_rate):
    return random.choices(items, spawn_rate)

def makeLines():
    line1 = [randomizeItem(slot_items,items_spawn_rate),randomizeItem(slot_items,items_spawn_rate),randomizeItem(slot_items,items_spawn_rate)]
    line2 = [randomizeItem(slot_items,items_spawn_rate),randomizeItem(slot_items,items_spawn_rate),randomizeItem(slot_items,items_spawn_rate)]
    line3 = [randomizeItem(slot_items,items_spawn_rate),randomizeItem(slot_items,items_spawn_rate),randomizeItem(slot_items,items_spawn_rate)]
    return [line1, line2, line3]

def calculatePrize(lines, bet):
    out1 = 0
    out2 = 0
    out3 = 0
    out4 = 0
    out5 = 0
    slot_line1 = lines[0]
    slot_line2 = lines[1]
    slot_line3 = lines[2]
    #For line 1
    if slot_line1[0][0] == slot_items[0] and slot_line1[1][0] == slot_items[0] and slot_line1[2][0] == slot_items[0]:
        #win 50
        out1 = config.global_economic["slot_item1_cost"]*bet
    if slot_line1[0][0] == slot_items[1] and slot_line1[1][0] == slot_items[1] and slot_line1[2][0] == slot_items[1]:
        #win 100
        out1 = config.global_economic["slot_item2_cost"]*bet
    if slot_line1[0][0] == slot_items[2] and slot_line1[1][0] == slot_items[2] and slot_line1[2][0] == slot_items[2]:
        #win 250
        out1 = config.global_economic["slot_item3_cost"]*bet
    if slot_line1[0][0] == slot_items[3] and slot_line1[1][0] == slot_items[3] and slot_line1[2][0] == slot_items[3]:
        #win 600
        out1 = config.global_economic["slot_item4_cost"]*bet
    if slot_line1[0][0] == slot_items[4] and slot_line1[1][0] == slot_items[4] and slot_line1[2][0] == slot_items[4]:
        #win 2000
        out1 = config.global_economic["slot_item5_cost"]*bet

    #For line 2
    if slot_line2[0][0] == slot_items[0] and slot_line2[1][0] == slot_items[0] and slot_line2[2][0] == slot_items[0]:
        #win 50
        out2 = config.global_economic["slot_item1_cost"]*bet
    if slot_line2[0][0] == slot_items[1] and slot_line2[1][0] == slot_items[1] and slot_line2[2][0] == slot_items[1]:
        #win 100
        out2 = config.global_economic["slot_item2_cost"]*bet
    if slot_line2[0][0] == slot_items[2] and slot_line2[1][0] == slot_items[2] and slot_line2[2][0] == slot_items[2]:
        #win 250
        out2 = config.global_economic["slot_item3_cost"]*bet
    if slot_line2[0][0] == slot_items[3] and slot_line2[1][0] == slot_items[3] and slot_line2[2][0] == slot_items[3]:
        #win 600
        out2 = config.global_economic["slot_item4_cost"]*bet
    if slot_line2[0][0] == slot_items[4] and slot_line2[1][0] == slot_items[4] and slot_line2[2][0] == slot_items[4]:
        #win 2000
        out2 = config.global_economic["slot_item5_cost"]*bet

    # For line 3
    if slot_line3[0][0] == slot_items[0] and slot_line3[1][0] == slot_items[0] and slot_line3[2][0] == slot_items[0]:
        #win 50
        out3 = config.global_economic["slot_item1_cost"]*bet
    if slot_line3[0][0] == slot_items[1] and slot_line3[1][0] == slot_items[1] and slot_line3[2][0] == slot_items[1]:
        #win 100
        out3 = config.global_economic["slot_item2_cost"]*bet
    if slot_line3[0][0] == slot_items[2] and slot_line3[1][0] == slot_items[2] and slot_line3[2][0] == slot_items[2]:
        #win 250
        out3 = config.global_economic["slot_item3_cost"]*bet
    if slot_line3[0][0] == slot_items[3] and slot_line3[1][0] == slot_items[3] and slot_line3[2][0] == slot_items[3]:
        #win 600
        out3 = config.global_economic["slot_item4_cost"]*bet
    if slot_line3[0][0] == slot_items[4] and slot_line3[1][0] == slot_items[4] and slot_line3[2][0] == slot_items[4]:
        #win 2000
        out3 = config.global_economic["slot_item5_cost"]*bet


    #1 diagonal
    if slot_line1[0][0] == slot_items[0] and slot_line2[1][0] == slot_items[0] and slot_line3[2][0] == slot_items[0]:
        out4 = config.global_economic["slot_item1_cost"]*bet
    if slot_line1[0][0] == slot_items[1] and slot_line2[1][0] == slot_items[1] and slot_line3[2][0] == slot_items[1]:
        out4 = config.global_economic["slot_item2_cost"]*bet
    if slot_line1[0][0] == slot_items[2] and slot_line2[1][0] == slot_items[2] and slot_line3[2][0] == slot_items[2]:
        out4 = config.global_economic["slot_item3_cost"]*bet
    if slot_line1[0][0] == slot_items[3] and slot_line2[1][0] == slot_items[3] and slot_line3[2][0] == slot_items[3]:
        out4 = config.global_economic["slot_item4_cost"]*bet
    if slot_line1[0][0] == slot_items[4] and slot_line2[1][0] == slot_items[4] and slot_line3[2][0] == slot_items[4]:
        out4 = config.global_economic["slot_item5_cost"]*bet


    #2 diagonal
    if slot_line1[2][0] == slot_items[0] and slot_line2[1][0] == slot_items[0] and slot_line3[0][0] == slot_items[0]:
        out4 = config.global_economic["slot_item1_cost"]*bet
    if slot_line1[2][0] == slot_items[1] and slot_line2[1][0] == slot_items[1] and slot_line3[0][0] == slot_items[1]:
        out4 = config.global_economic["slot_item2_cost"]*bet
    if slot_line1[2][0] == slot_items[2] and slot_line2[1][0] == slot_items[2] and slot_line3[0][0] == slot_items[2]:
        out4 = config.global_economic["slot_item3_cost"]*bet
    if slot_line1[2][0] == slot_items[3] and slot_line2[1][0] == slot_items[3] and slot_line3[0][0] == slot_items[3]:
        out4 = config.global_economic["slot_item4_cost"]*bet
    if slot_line1[2][0] == slot_items[4] and slot_line2[1][0] == slot_items[4] and slot_line3[0][0] == slot_items[4]:
        out4 = config.global_economic["slot_item5_cost"]*bet


    return out1 + out2 + out3 + out4 + out5


def getSlotState(bet):
    lines = makeLines()
    prize = calculatePrize(lines, bet)
    return [prize, lines]

def playGAME(bot, message):
    try:
        message_to_delete = message.message_id
        userName = message.from_user.username.replace("@", "")
        if userName is None:
                msg = bot.reply_to(message, "У тебя нет никнейма, что бы играть")
                bot.message_stack.append(msg)
                return
        userMoney = int(database.getDBValue(userName, "eco", "money"))
        user_slot_gamed_count = int(database.getDBValue(userName, "stats", "slot_gamed_count"))
        user_money_lost_in_slot = int(database.getDBValue(userName, "stats", "money_lost_in_slot"))
        if userMoney < 0:
            delete = bot.reply_to(message, "У тебя нет денег, возьми кредит /banks")
            time.sleep(15)
            bot.delete_message(message.chat.id, delete.message_id)
        else:
            command = message.text.split()
            bet = 1
            if len(command) > 1:
                if command[1] == "0":
                    bet = 1
                bet = int(command[1])

            if bet > 25:
                delete = bot.reply_to(message, "Максимальная ставка - х25🕹")
                time.sleep(4)
                bot.delete_message(message.chat.id, delete.message_id)
                return
            user_slot_gamed_count += 1
            user_money_lost_in_slot = user_money_lost_in_slot + (config.global_economic["slot_spin_cost"]*bet)
            slotState = getSlotState(bet)
            prize = int(slotState[0])
            slot_line1 = slotState[1][0]
            slot_line2 = slotState[1][1]
            slot_line3 = slotState[1][2]
            won = userMoney + prize
            if prize == 0:
                won = userMoney - (config.global_economic["slot_spin_cost"]*bet)
            UI = ""
            #UI = "👨: @" + userName + "\n"
            UI += "\n⚖️Баланс: " + str(won) + "💲\n"
            UI += "\n🕹Cтавка: "+str((config.global_economic["slot_spin_cost"]*bet))+"💶\n\n"
            UI += "3x🍏 = "+str(config.global_economic["slot_item1_cost"]*bet)+"\n3x🍋 = "+str(config.global_economic["slot_item2_cost"]*bet)+"\n3x🍇 = "+str(config.global_economic["slot_item3_cost"]*bet)+"\n3x🍒 = "+str(config.global_economic["slot_item4_cost"]*bet)+"\n3x7️⃣ = "+str(config.global_economic["slot_item5_cost"]*bet)+" \n"
            UI += "----------------------------\n"
            UI += "[ -" + slot_line1[0][0] + "-   -" + slot_line1[1][0] + "-   -" + slot_line1[2][0] + "- ]\n"
            UI += "[ -" + slot_line2[0][0]+ "-   -" + slot_line2[1][0] + "-   -" + slot_line2[2][0] + "- ]\n"
            UI += "[ -" + slot_line3[0][0]+ "-   -" + slot_line3[1][0] + "-   -" + slot_line3[2][0] + "- ]\n"
            UI += "----------------------------\n"
            if prize == 0:
                UI += "\nТы потерял свои несчастные: " + str(config.global_economic["slot_spin_cost"]*bet) + "💲 и ничего не выиграл\n"
            else:
                UI += "\n🎉 Выигрыш: " + str(prize) + "💲\n"

            database.setDBValue(userName, "eco", "money", str(won))
            database.setDBValue(userName, "stats", "slot_gamed_count", str(user_slot_gamed_count))
            database.setDBValue(userName, "stats", "money_lost_in_slot", str(user_money_lost_in_slot))
            show_ui = bot.reply_to(message, UI)
            time.sleep(10)
            bot.delete_message(message.chat.id, show_ui.message_id)
            bot.delete_message(message.chat.id, message_to_delete)

    except:
        #msg = bot.send_message(message.chat.id, "Попробуй еще раз, что-то сломалось")
        #bot.message_stack.append(msg)
        pass

def getSlotTotalMoney(bot, message):
    values = database.getListUsersWhereValue("stats", "money_lost_in_slot", None)
    out = 0
    for item in values:
        out += int(item[1])
    UI = "Рулетка заработала на пользователях: "+str(out)+"💶"
    msg = bot.reply_to(message, UI)
    bot.message_stack.append(msg)