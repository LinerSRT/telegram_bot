import random

ROLL_PRICE = 200
FRUITS = ['🍌', '🍒', '🍐', '🍈', '🍇']
COSTS = [50, 100, 120, 150, 200, 270]
CHANCE = [120, 40, 40, 35, 5]

def getLine():
    return [random.choices(FRUITS, CHANCE) for i in range(3)]

def getPrice(fruit):
    for index, item in enumerate(FRUITS):
        if item[0] == fruit:
            return COSTS[index]
    return 0

def getLinePrize(line, bet):
    out = 0
    if line[0][0] == line[1][0] == line[2][0]:
        out += getPrice(line[0][0])
    return round(out * bet)

def getUI(lines):
    UI = ""
    for line in lines:
        UI += ">"+str(line[0][0])+"<  >"+str(line[1][0])+"<  >"+str(line[2][0])+"<\n"
    return UI

def roll(usermoney, bet_multiplier):
    bet = round(ROLL_PRICE*bet_multiplier)
    if bet > usermoney:
        return -1
    line1 = getLine()
    line2 = getLine()
    line3 = getLine()
    usermoney = usermoney - bet
    won = getLinePrize(line1, bet_multiplier) + getLinePrize(line2, bet_multiplier) + getLinePrize(line3, bet_multiplier)
    usermoney = usermoney + won
    return [usermoney, won, [line1, line2, line3]]

def start(username, usermoney, bet_multiplier):
    game = roll(usermoney, bet_multiplier)
    #print(game)
    return game[1]
    #if game != -1:
    #    UI = "Привет, @" + username + " вы сделали спин стоимостью " + str(round(ROLL_PRICE * bet_multiplier)) + "\n"
    #    if game[1] <= 0:
    #        UI += "Но удача не на вашей стороне и вы потеряли "+str(round(ROLL_PRICE * bet_multiplier))+"\n"
    #        UI += getUI(game[2])
    #    elif game[1] > 0:
    #        UI += "Похоже на то, что вам повезло в этот раз. Ваш приз составил "+str(game[1])+"\n"
    #        UI += getUI(game[2])
    #    else:
    #        pass
    #    print(UI)

counter = 0
game_count = 10000
for i in range(game_count):
    print(i)
    if start("Test", 1000, 2) > 0:
        counter += 1
print("Из "+str(game_count)+" выигранных партий "+str(counter))
