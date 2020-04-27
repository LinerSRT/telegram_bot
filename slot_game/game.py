import random
import time
import threading


def gameLoop():
    while True:
        time.sleep(1)
        myPet.life()
        myPet.makeHunger()

def inputLoop():
    while True:
        command = input("Select command [0-5]")
        if command == "1":
            myPet.test(20)
            print(myPet.food)

class Pet:
    def __init__(self, name, avatar, food=100, drink=100, sleep=100, died=False, usage=0):
        self.name = name
        self.avatar = avatar
        self.food = food
        self.drink = drink
        self.sleep = sleep
        self.died = died
        self.usage = usage
        self.life_time = 0

    def makeHunger(self):
        if random.randint(0, 5) == 5:
            self.food -= random.randint(0, 5)

    def test(self, amount):
        self.food += amount
        self.usage += 1

    def life(self):
        self.life_time += 1


myPet = Pet("Pidor", "@")

threading.Thread(name="gameLoop", target=gameLoop, args=()).start()
threading.Thread(name="inputLoop", target=inputLoop, args=()).start()
