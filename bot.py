import telebot
import time
import threading
import random
import bot_functions as bf
TOKEN = '1203682284:AAGhxzP6PLAOFkGOgb0W3Naq3nJpSiINTZ4'
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
        print("-------------")
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


@bot.message_handler(commands=["rullet"])
def answer(message):
    global GAME_AVAILABLE
    #bf.SendMessage("test", bot, message, "Слоты").start()
    bf.SlotGame(bot, message, 1000, game_available=GAME_AVAILABLE)
    GAME_AVAILABLE = False

    pass

if __name__ == '__main__':
    threading.Thread(name="botUpdater", target=bot_updater, args=()).start()
    threading.Thread(name="secondLoop", target=second_loop, args=()).start()
    threading.Thread(name="rullet_loop", target=rullet_loop, args=()).start()
    threading.Thread(name="minuteLoop", target=minute_loop, args=()).start()
    threading.Thread(name="hourLoop", target=hour_loop, args=()).start()

