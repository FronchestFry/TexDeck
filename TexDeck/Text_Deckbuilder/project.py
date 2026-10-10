#I gotta come up with somthing
#I could do minecraft datapacks again, it's been a bit since I've done that
#Or the deck of cards thing
#We're working on this

#imports
import random
import copy

#list and var establishment
deck = []
hand = []
draw = []
discard = []
startercards = []
Enemy_Library = []
Card_Library = []

draw_size = 5
Player_HP = 20

#classes
class Card:
    def __init__(self, d, b, n, desc):
        self.dmg = d
        self.block = b
        self.name = n
        self.description = desc
        Card_Library.append(self)

class Enemy:
    def __init__(self, h, n, desc):
        self.health = h
        self.name = n
        self.description = desc
        self.defense = 0
        Enemy_Library.append(self)

    def attack_desc(self):
        if self.name == "Practice Dummy":
            print ("It's a dummy, it totally won't attack you.")
            self.intended_atk = 1
        elif self.name == "Red Dragon":
            print ("It looks like it wants you to die in a fireball.")
            self.intended_atk = 1

    def attack_effect(self):
        if self.name == "Practice Dummy":
            if self.intended_atk == 1:
                #TODO player health -1
                pass


#functions
def draw_cards(num):
    for x in range(num):
        card = draw.pop(random.randrange(len(draw)))
        hand.append(card)

def start_fight():
    #draw a hand of cards
    global draw
    draw = deck[:]
    draw_cards(draw_size)
    #pick an enemy
    global current_enemy
    current_enemy = copy.deepcopy(Enemy_Library[random.randrange(len(Enemy_Library))])
    #Display the enemy
    print(f"You begin combat with a {current_enemy.name}. {current_enemy.description}")
    combat_turn()

def combat_turn():
    #List enemies current stats
    print (f"The {current_enemy.name} has {current_enemy.health} HP remaining, and has {current_enemy.defense} shield.")
    #Get enemy's attack
    current_enemy.attack_desc()
    print()
    #List players Hand
    print("Hand:")
    card_num = 0
    for card in hand:
        card_num += 1
        print (f"{card_num}) {card.name}\n \t {card.description}")
    print()
    #Ask what they want to do
    while True:
        selected_card = input(f"Type a number 1-{len(hand)} to select a card, then hit enter to confirm.\n")
        try:
            selected_card = int(selected_card)
        except ValueError:
            print ("That is not a number. Please try again.")
        else:
            if not selected_card in range(1,len(hand)):
                print ("You do not have a card in that slot. Please Select one of the presented options.")
            else:
                break

    #Apply player card effects
    #Apply enemy card effects/end combat
    #Next turn
    pass

#Defining things
Knife = Card (1, 0, "Hot flamey sword", "Stabs people for one damage")
Knife2 = Card (2, 0, "Super hot flamey sword", "Stabs people for two damage")
Shield = Card (0, 2, "Shield of Shielding", 'Blocks 2 damage')
Confuse = Card (0, 0, "Centaur-taur", 'Confuses the enemy')

Target_Dummy = Enemy(5, "Practice Dummy", "Hit the dummy, dummy.")
Dragon = Enemy(25, "Red Dragon", "Run while you still can.")

#setup
startercards = [Knife, Knife2, Shield, Confuse]

for x in range (2):
    for card in startercards:
        deck.append(copy.deepcopy(card))

#testing
start_fight()