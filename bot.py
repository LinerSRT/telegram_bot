import telebot
import time
import threading
import bot_functions as bf
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
    if len(message.text.split()) < 2:
        bf.SlotGame(bot, message, game_available=GAME_AVAILABLE)
        return
    bet = int(message.text.split()[1])
    bf.SlotGame(bot, message, game_available=GAME_AVAILABLE, game_bet=bet)
    GAME_AVAILABLE = False
@bot.message_handler(commands=["source"])
def answer(message):
    bf.ReplyTo(bot, message, "Исодный код - [GitHub](https://github.com/LinerSRT/telegram_bot)", use_markdown=True)























if __name__ == '__main__':
    threading.Thread(name="botUpdater", target=bot_updater, args=()).start()
    threading.Thread(name="secondLoop", target=second_loop, args=()).start()
    threading.Thread(name="rullet_loop", target=rullet_loop, args=()).start()
    threading.Thread(name="minuteLoop", target=minute_loop, args=()).start()
    threading.Thread(name="hourLoop", target=hour_loop, args=()).start()

