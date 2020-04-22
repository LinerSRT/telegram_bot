import time
import random

banned_text = [
    "ты в бане, пиздуй отсюда",
    "еблан, теперь ты забанен",
    "заткнись, тебе слова не давали",
    "чмо ебаное",
    "умоляй, что бы я тебя разбанил",
    "чмрина ебаная",
    "шакал ебаный",
    "ублюдок вонючий",
    "я твой рот ебал",
    "мразь",
    "сучара конченная",
    "в жопу ебали олени",
    "идет нахуй",
    "все еще сосет бибу",
    "вытяни хуй изо рта",
    "я ломал твой еблет",
    "пидрила",
    "ублюдок мелкий",
    "этот еблан так и не понял что он теперь сосет",
    "да у тебя рак... Мозга нахуй",
    "System has been destroyed!",
    "вытащи хуй изо рта, прежде чем говорить",
    "тупой дебил",
    "долбоеб, ты забанен"]

def processUser(username, bot, message):
    rofl = bot.send_message(message.chat.id, "@" + username + ", " + random.choice(banned_text))
    bot.delete_message(message.chat.id, message.message_id)
    time.sleep(3)
    bot.delete_message(message.chat.id, rofl.message_id)