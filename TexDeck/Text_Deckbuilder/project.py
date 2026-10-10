#I gotta come up with somthing
#I could do minecraft datapacks again, it's been a bit since I've done that
#Or the deck of cards thing
#We're working on this

#imports
import random
import copy
from time import sleep
from art import tprint

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
Player_block = 0

#classes
class Card:
    def __init__(self, d, b, n, desc, id):
        self.dmg = d
        self.block = b
        self.name = n
        self.description = desc
        self.id = id
        Card_Library.append(self)
    
    def playcard(self):
        global Player_block
        global Player_HP
        if self.id[0] == "a":
            #attacks
            if self.id[1] == '0':
                current_enemy.takedamage(1)
            elif self.id[1] == '1':
                            current_enemy.takedamage(2)
            pass
        elif self.id[0] == "d":
            #defensive cards
            if self.id[1] == '0':
                Player_block += 2
            pass
        elif self.id[0] == 's':
            #skills
            if self.id[1] == '0':
                current_enemy.skipturn = True
            pass
        discard.append(hand.pop(hand.index(self)))
        

class Enemy:
    def __init__(self, h, n, desc, ID):
        self.health = h
        self.name = n
        self.description = desc
        self.defense = 0
        self.id = ID
        self.skipturn = False
        Enemy_Library.append(self)

    def attack_desc(self):
        if self.id == 0:
            print ("The dummy looks pitiful. You feel tempted to spontaniously take 1 damage out of pity.")
            self.intended_atk = 0
        elif self.id == 1:
            print ("The dragon looks like there is somthing caught in its throat.")
            self.intended_atk = 0

    def attack_effect(self):
        if not self.skipturn == True:
            if self.id == 0:
                if self.intended_atk == 0:
                    print ('You give in to the temptation.')
                    damageplayer(1)
            elif self.id == 1:
                if self.intended_atk == 0:
                    print ("Turns out, the thing in its throat was fire.")
                    damageplayer(15)
    
        else:
            self.skipturn = False
            print (f"{self.name}'s Turn was lost as they stared at the centaur-taur in confustion. What's wrong with that thing?")
            pass

    def takedamage(self, dmgval):
        if self.defense > 0:
            if self.defense > dmgval:
                self.defense -= dmgval
                dmgval = 0
            elif self.defense < dmgval:
                dmgval -= self.defense
                self.defense = 0
            elif self.defense == dmgval:
                self.defense = 0
                dmgval = 0
        elif self.defense < 0:
            dmgval += self.defense
        
        self.health -= dmgval
        print (f"After armor, your attack dealt {dmgval} damage!")



#functions
def draw_cards(num):
    for x in range(num):
        if len(draw) > 0:
            card = draw.pop(0)
            hand.append(card)
        else:
            print ('Out of cards to draw. Shuffling discard into draw pile')
            draw.extend(discard)
            discard.clear()
            random.shuffle(draw)
            draw_cards(1)

def damageplayer(dmgval):
    global Player_HP
    global Player_block
    if Player_block > 0:
        if Player_block > dmgval:
            Player_block -= dmgval
            dmgval = 0
        elif Player_block < dmgval:
            dmgval -= Player_block
            Player_block = 0
        elif Player_block == dmgval:
            Player_block = 0
            dmgval = 0
    elif Player_block < 0:
        dmgval += Player_block
    
    Player_HP -= dmgval
    print (f"You take {dmgval} damage!")

def start_fight():
    #initialize the deck
    global draw
    draw = deck[:]

    #pick an enemy
    global current_enemy
    current_enemy = copy.deepcopy(Enemy_Library[random.randrange(len(Enemy_Library))])

    #Display the enemy
    print(f"You begin combat with a {current_enemy.name}. {current_enemy.description}")

    #start the first turn
    print ('----------------------------------------------------------------------------------------')
    combat_turn()

def combat_turn():
    sleep(1)
    #List enemies current stats
    print (f"The {current_enemy.name} has {current_enemy.health} HP remaining, and has {current_enemy.defense} shield.")
    sleep(1)
    #Get enemy's attack
    current_enemy.attack_desc()
    print()
    sleep(1)
    #draw to hand size
    draw_cards(draw_size-len(hand))

    #Display Player's stats
    print (f"You have {Player_HP} Health and {Player_block} defence remaining.")
    print()
    sleep(1)
    #List players Hand
    print("Hand:")
    card_num = 0
    for card in hand:
        card_num += 1
        print (f"{card_num}) {card.name}\n \t {card.description}")
    print()

    #list deck stats
    print(f"Draw Pile: {len(draw)}\t Discard Pile: {len(discard)}")

    #Ask what they want to do
    while True:
        selected_card_index = input(f"Type a number 1-{len(hand)} to select a card, then hit enter to confirm.\n")
        try:
            selected_card_index = int(selected_card_index)
        except ValueError:
            print ("That is not a number. Please try again.")
        else:
            if not selected_card_index in range(1,len(hand)+1):
                print ("You do not have a card in that slot. Please Select one of the presented options.")
            else:
                break

    #Apply player card effects
    selected_card = hand[selected_card_index-1]
    selected_card.playcard()

    #Apply enemy card effects & next turn/end combat
    if current_enemy.health > 0:
        current_enemy.attack_effect()
        print ('----------------------------------------------------------------------------------------')
        if Player_HP > 0:
            combat_turn()
        else:
            tprint("You Died") 
    else:
        print (f"You have slain the {current_enemy.name}. Glory to thee, saviour of the realm!")

#Defining things
Knife = Card (1, 0, "Hot flamey sword", "Stabs people for one damage", 'a0')
Knife2 = Card (2, 0, "Super hot flamey sword", "Stabs people for two damage", 'a1')
Shield = Card (0, 2, "Shield of Shielding", 'Blocks 2 damage', 'd0')
Confuse = Card (0, 0, "Centaur-taur", 'Confuses the enemy', 's0')

Target_Dummy = Enemy(5, "Practice Dummy", "Hit the dummy, dummy.", 0)
Dragon = Enemy(25, "Red Dragon", "Run while you still can.", 1)

#setup
startercards = [Knife, Knife2, Shield, Confuse]

for x in range (2):
    for card in startercards:
        deck.append(copy.deepcopy(card))
random.shuffle(draw)

#testing
start_fight()