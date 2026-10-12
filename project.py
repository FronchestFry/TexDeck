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
Easy_Enemy_Library = []
Medium_Enemy_Library = []
Hard_Enemy_Library = []
Card_Library = []

draw_size = 5
Player_HP = 20
Player_block = 0

#classes
class Card:
    def __init__(self, n, desc, id):
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
                current_enemy.takedamage(3)
            elif self.id[1] == '1':
                current_enemy.takedamage(5)
            pass
        elif self.id[0] == "d":
            #defensive cards
            if self.id[1] == '0':
                Player_block += 5
            pass
        elif self.id[0] == 's':
            #skills
            if self.id[1] == '0':
                current_enemy.skipturn = True
            pass
        discard.append(hand.pop(hand.index(self)))
        

class Enemy:
    def __init__(self, h, n, desc, ID, dificulty):
        self.health = h
        self.name = n
        self.description = desc
        self.defense = 0
        self.id = ID
        self.skipturn = False
        if dificulty == "easy":
            Easy_Enemy_Library.append(self)
        if dificulty == "mid":
            Medium_Enemy_Library.append(self)
        if dificulty == "hard":
            Hard_Enemy_Library.append(self)

    def attack_desc(self):
        atkchoice = random.randint(1,10)
        if self.id == 0:
            if atkchoice < 10:
                print ("The dummy looks pitiful. You feel tempted to poke yourself for 1 damage out of pity.")
                self.intended_atk = 0
            else:
                print ("A menacing look crosses the dummy's face. You feel your skin crawl.")
                self.intended_atk = 1
        elif self.id == 1:
            if atkchoice < 4:
                print ("The dragon looks like there is somthing caught in its throat.")
                self.intended_atk = 0
            else:
                print ("The dragon's hind legs tense")
                self.intended_atk = 1
        elif self.id == 2:
            if atkchoice < 5:
                print ("The goblin waves its sword threateningly.")
                self.intended_atk = 0
            else:
                print ("The goblin pulls back a bow at you.")
                self.intended_atk = 1
        elif self.id == 3:
            if atkchoice in range(1,4):
                print ("The slime inflates with air.")
                self.intended_atk = 0
            elif atkchoice in range (5,7):
                print ("The slime makes a wet noise.")
                self.intended_atk = 1
            else:
                print ("The slime gathers its mass to lunge")
                self.intended_atk = 2
        elif self.id == 4:
            if atkchoice < 7:
                print ("The slime gathers its mass to lunge")
                self.intended_atk = 0
            else:
                print ("The slime ripples and swells.")
                self.intended_atk = 1


    def attack_effect(self):
        global Player_block
        if not self.skipturn == True:
            if self.id == 0:
                if self.intended_atk == 0:
                    print ('You poke yourself.')
                    damageplayer(1)
                elif self.intended_atk == 1:
                    print('A grave chill settles on your heart.')
                    damageplayer(6, True)
            elif self.id == 1:
                if self.intended_atk == 0:
                    print ("Turns out, the thing in its throat was fire.")
                    damageplayer(10)
                elif self.intended_atk == 1:
                    print ("The dragon lunges forward, raking its claws across you.")
                    damageplayer(7)
            elif self.id == 2:
                if self.intended_atk == 0:
                    print ("The goblin slashes you with it's blade.")
                    damageplayer(5)
                elif self.intended_atk == 1:
                    print("The goblin fires its arrow.")
                    damageplayer(4)
            elif self.id == 3:
                if self.intended_atk == 0:
                    print ("The slime bursts, spraying acid.")
                    Player_block -= 1
                    damageplayer(1)
                elif self.intended_atk == 1:
                    print("The slime spits a glob of acid, eating through your armor.")
                    Player_block -= 7
                elif self.intended_atk == 2:
                    print("The slime slams into you.")
                    damageplayer(4)
            elif self.id == 4:
                if self.intended_atk == 0:
                    print ('The slime bumps you.')
                    damageplayer(self.health)
                elif self.intended_atk == 1:
                    print('The slime begins to grow in size.')
                    self.health += 5


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
            dmgval += 0-self.defense
        
        self.health -= dmgval
        if dmgval > 0:
            print (f"After armor, your attack dealt {dmgval} damage!")
        if dmgval == 0:
            print (f"They blocked the attack! They have {self.defense} block left.")

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

def damageplayer(dmgval, bypass_armor = False):
    global Player_HP
    global Player_block
    if bypass_armor:
        print("The special nature of the attack ignores your shield.")
        Player_HP -= dmgval
        print (f"You take {dmgval} damage.")
    else:
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
        if dmgval > 0:
            print (f"After armor, their attack dealt {dmgval} damage!")
        if dmgval == 0:
            print (f"You blocked the attack! You have {Player_block} defense left.")

def start_fight(dificulty):
    #initialize the deck
    global draw
    draw = deck[:]

    #pick an enemy
    global current_enemy
    if dificulty == "easy":
        current_enemy = copy.deepcopy(Easy_Enemy_Library[random.randrange(len(Easy_Enemy_Library))])
    elif dificulty == "mid":
        current_enemy = copy.deepcopy(Medium_Enemy_Library[random.randrange(len(Medium_Enemy_Library))])
    elif dificulty == "hard":
        current_enemy = copy.deepcopy(Hard_Enemy_Library[random.randrange(len(Hard_Enemy_Library))])

    #Display the enemy
    print(f"You begin combat with a {current_enemy.name}. {current_enemy.description}")

    #start the first turn
    print ('----------------------------------------------------------------------------------------')
    combat_turn()

def combat_turn():
    sleep(.5)
    #List enemies current stats
    print (f"The {current_enemy.name} has {current_enemy.health} HP remaining, and has {current_enemy.defense} shield.")
    sleep(.5)
    #Get enemy's attack
    current_enemy.attack_desc()
    print()
    sleep(.5)
    #draw to hand size
    draw_cards(draw_size-len(hand))

    #Display Player's stats
    global Player_block
    print (f"You have {Player_HP} Health and {Player_block} defence remaining.")
    print()
    sleep(.5)
    #List players Hand
    print("Hand:")
    card_num = 0
    for card in hand:
        card_num += 1
        print (f"{card_num}) {card.name}\n \t {card.description}")
        sleep(.25)
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
    sleep(.5)

    #Apply enemy card effects & next turn/end combat
    if current_enemy.health > 0:
        current_enemy.attack_effect()
        print ('----------------------------------------------------------------------------------------')
        if Player_HP > 0:
            combat_turn()
        else:
            tprint("You Died") 
            quit()
    else:
        print (f"You have slain the {current_enemy.name}. Glory to thee!")
        draw.clear()
        hand.clear()
        discard.clear()
        Player_block = 0

def pickcards():
    print ('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    sleep(.5)
    print ("Welcome to the shop! Here you will be able to pick new cards to add to your deck.")
    sleep(.5)
    options = random.sample(Card_Library,3)
    card_num = 0
    for card in options:
            card_num += 1
            print (f"{card_num}) {card.name}\n \t {card.description}")
            sleep(.5)
    print()
    while True:
        selected_card_index = input(f"Type a number 1-{len(options)} to select a card, then hit enter to confirm.\n")
        try:
            selected_card_index = int(selected_card_index)
        except ValueError:
            print ("That is not a number. Please try again.")
        else:
            if not selected_card_index in range(1,len(options)+1):
                print ("There is not a card option in that slot. Please Select one of the presented options.")
            else:
                break

    #Apply player card effects
    selected_card = options[selected_card_index-1]
    print(f"You have chosen to add the {selected_card.name} to your deck. I hope you make good use of it.")
    deck.append(copy.deepcopy(selected_card))
    print ('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    sleep(.5)

#Defining things
Knife = Card ("Hot flamey sword", "Stabs people for three damage", 'a0')
Knife2 = Card ("Super hot flamey sword", "Stabs people for five damage", 'a1')
Shield = Card ("Shield of Shielding", 'Gain five block', 'd0')
Taur = Card ("Centaur-taur", 'Confuses the enemy', 's0')

Target_Dummy = Enemy(6, "Practice Dummy", "Hit the dummy, dummy.", 0, 'easy')
Dragon = Enemy(15, "Red Dragon", "Run while you still can.", 1, 'hard')
Goblin = Enemy(10, "Goblin", "The default fantasy creature", 2, 'mid')
Slime1 = Enemy(6, "Green Slime", "It reeks of acid", 3, 'mid')
Slime2 = Enemy(4, "Red Slime", "Cut them down to size", 4, 'easy')

#setup
startercards = [Knife, Knife, Knife, Knife2, Shield, Shield, Shield, Taur]


for card in startercards:
    deck.append(copy.deepcopy(card))
random.shuffle(draw)

#testing
start_fight('easy')
pickcards()
start_fight('mid')
pickcards()
start_fight('hard')
tprint("Congratulations!")
print("You're our BIG WINNER! You have slain all the monsters! Great job!")
