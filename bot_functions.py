import threading
import time
import random
import bot as mainf
message_stack = []

class ReplyTo(threading.Thread):
    def __init__(self, argument, bot, message, text, stack=True, timeout=10):
        super(ReplyTo, self).__init__()
        self.argument = argument
        self.bot = bot
        self.message = message
        self.text = text
        self.stack = stack
        self.timeout = timeout

    def run(self):
        msg = self.bot.reply_to(self.message, self.text)
        if self.stack:
            message_stack.append(self.message)
            message_stack.append(msg)
        else:
            try:
                time.sleep(self.timeout)
                chat_id = self.message.chat.id
                self.bot.delete_message(chat_id, msg.message_id)
                self.bot.delete_message(chat_id, self.message.message_id)
            except:
                pass
            finally:
                pass
class SendMessage(threading.Thread):
    def __init__(self, argument, bot, message, text, stack=True, timeout=10):
        super(SendMessage, self).__init__()
        self.argument = argument
        self.bot = bot
        self.message = message
        self.text = text
        self.stack = stack
        self.timeout = timeout

    def run(self):
        msg = self.bot.send_message(self.message.chat.id, self.text)
        if self.stack:
            message_stack.append(self.message)
            message_stack.append(msg)
        else:
            try:
                time.sleep(self.timeout)
                chat_id = self.message.chat.id
                self.bot.delete_message(chat_id, msg.message_id)
                self.bot.delete_message(chat_id, self.message.message_id)
            except:
                pass
            finally:
                pass

class SlotGame(threading.Thread):
    ROLL_PRICE = 200
    FRUITS = ['🍌', '🍒', '🍐', '🍈', '🍇']
    COSTS = [50, 100, 120, 150, 200, 270]
    CHANCE = [120, 40, 40, 35, 5]

    def __init__(self, bot, message, usermoney, game_available=True, bet=1):
        self.bot = bot
        self.message = message
        if game_available:
            super(SlotGame, self).__init__()
            self.argument = str(message.from_user.id)
            self.start()
        else:
            msg = self.bot.reply_to(self.message, "Сейчас не доступно, 1 раз в 10 секунд")
            time.sleep(2)
            chat_id = self.message.chat.id
            self.bot.delete_message(chat_id, msg.message_id)
            self.bot.delete_message(chat_id, self.message.message_id)

    def getLine(self):
        return [random.choices(self.FRUITS, self.CHANCE)[0] for i in range(3)]

    def lineWin(self, line):
        return line[0] == line[1] == line[2]

    def diagonalLineWin(self, lines, reverse=False):
        if reverse:
            return lines[2][0] == lines[1][1] == lines[0][2]
        else:
            return lines[0][0] == lines[1][1] == lines[2][2]

    def getLinePrize(self, item):
        for index, fruit in enumerate(self.FRUITS):
            if fruit == item:
                return self.COSTS[index]
        return 0

    def processUI(self, rows):
        DISPLAY_STATE1 = "↘  ᅠ  ᅠ  ᅠ  ᅠ   ↙\n" \
                         "ᅠ  [ᅠ  ] [ᅠ  ] [ᅠ  ]\n" \
                         "▶[ᅠ  ] [ᅠ  ] [ᅠ  ]◀\n" \
                        "ᅠ  [ᅠ  ] [ᅠ  ] [ᅠ  ]\n" \
                        "↗  ᅠ  ᅠ  ᅠ  ᅠ   ↖\n"
        DISPLAY_STATE2 ="↘  ᅠ  ᅠ  ᅠ  ᅠ   ↙\n" \
                        "ᅠ  [ᅠ  ] [ᅠ  ] [ᅠ  ]\n" \
                        "▶[ᅠ  ] [ᅠ  ] [ᅠ  ]◀\n" \
                        "ᅠ  ["+rows[2][0]+"] ["+rows[2][1]+"] ["+rows[2][2]+"]\n" \
                        "↗  ᅠ  ᅠ  ᅠ  ᅠ   ↖\n"

        DISPLAY_STATE3 = "↘  ᅠ  ᅠ  ᅠ  ᅠ   ↙\n" \
                        "ᅠ  [ᅠ  ] [ᅠ  ] [ᅠ  ]\n" \
                        "▶["+rows[1][0]+"] ["+rows[1][1]+"] ["+rows[1][2]+"]◀\n" \
                        "ᅠ  ["+rows[2][0]+"] ["+rows[2][1]+"] ["+rows[2][2]+"]\n"\
                        "↗  ᅠ  ᅠ  ᅠ  ᅠ   ↖\n"
        DISPLAY_STATE4 = "↘  ᅠ  ᅠ  ᅠ  ᅠ   ↙\n" \
                        "ᅠ  ["+rows[0][0]+"] ["+rows[0][1]+"] ["+rows[0][2]+"]\n" \
                        "▶["+rows[1][0]+"] ["+rows[1][1]+"] ["+rows[1][2]+"]◀\n" \
                        "ᅠ  ["+rows[2][0]+"] ["+rows[2][1]+"] ["+rows[2][2]+"]\n"\
                        "↗  ᅠ  ᅠ  ᅠ  ᅠ   ↖\n"
        return [DISPLAY_STATE1, DISPLAY_STATE2, DISPLAY_STATE3, DISPLAY_STATE4]

    def run(self):
        msg = self.bot.reply_to(self.message, "⏳")
        time.sleep(2)
        line = self.getLine()
        line2 = self.getLine()
        line3 = self.getLine()
        DISP = self.processUI([line, line2, line3])
        for i in range(4):
            time.sleep(0.3)
            UI = "Рулетка 🚢Три корабля🚢 подкручивает шансы и вот ваша игра:\n\n"
            UI += DISP[i]
            if i == 3:
                won = 0
                if self.lineWin(line2):
                    won += self.getLinePrize(line2[1])
                if self.diagonalLineWin([line, line2, line3]):
                    won += self.getLinePrize(line2[1])
                if self.diagonalLineWin([line, line2, line3], reverse=True):
                    won += self.getLinePrize(line2[1])
                if won != 0:
                    UI += "\nВы выиграли! 😎"
                    UI += "\nВаш приз составил: "+str(won)+"💵"
                else:
                    UI += "\nУдача не на вашей стороне 😄"
            self.bot.edit_message_text(UI, msg.chat.id, msg.message_id)
        time.sleep(15)
        chat_id = self.message.chat.id
        self.bot.delete_message(chat_id, msg.message_id)
        self.bot.delete_message(chat_id, self.message.message_id)


