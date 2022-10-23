

import copy

import json

from flask import *
import random

"""globals"""
pile = []
last_cards_thrown = []
player1 = []
player2 = []
player3 = []
player4 = []
legalty = "true"
cards = [
    '02_of_clubs', 
    '03_of_clubs', 
    '04_of_clubs', 
    '05_of_clubs', 
    '06_of_clubs', 
    '07_of_clubs', 
    '08_of_clubs', 
    '09_of_clubs', 
    '10_of_clubs', 
    '11_of_clubs', 
    '12_of_clubs', 
    '13_of_clubs', 
    '01_of_clubs', 

    '02_of_hearts', 
    '03_of_hearts', 
    '04_of_hearts', 
    '05_of_hearts', 
    '06_of_hearts', 
    '07_of_hearts', 
    '08_of_hearts', 
    '09_of_hearts', 
    '10_of_hearts', 
    '11_of_hearts', 
    '12_of_hearts', 
    '13_of_hearts', 
    '01_of_hearts', 

    '02_of_diamonds', 
    '03_of_diamonds', 
    '04_of_diamonds', 
    '05_of_diamonds', 
    '06_of_diamonds', 
    '07_of_diamonds', 
    '08_of_diamonds', 
    '09_of_diamonds', 
    '10_of_diamonds', 
    '11_of_diamonds', 
    '12_of_diamonds', 
    '13_of_diamonds', 
    '01_of_diamonds', 

    '02_of_spades', 
    '03_of_spades', 
    '04_of_spades', 
    '05_of_spades', 
    '06_of_spades', 
    '07_of_spades', 
    '08_of_spades', 
    '09_of_spades', 
    '10_of_spades', 
    '11_of_spades', 
    '12_of_spades', 
    '13_of_spades', 
    '01_of_spades',
    'red_joker',
    'black_joker'
]

def get_card_from_pile():
    pass

def get_card_from_deck():
    global cards, pile
    for c in last_cards_thrown: pile.append(c)
    last_cards_thrown.clear()
    if len(cards) < 2:
        cards = pile[:]
        pile.clear()
    i = random.randint(0, len(cards)-1)
    card = cards[i]
    cards.remove(card)
    return card


app = Flask(__name__)
@app.route("/reset_player1_hand")
def reset_player1_hand():
    player1.sort()
    return {"members": player1}

@app.route("/get_card_deck")
def get_card_deck():
    return {"card": get_card_from_deck()}

@app.route("/get_card_pile", methods=['POST'])
def get_card_pile():
    global pile
    request_data = json.loads(request.data)
    player1.append(request_data['card'])
    pile.remove(request_data['card'])
    return ''

def get_card_deck():
    card = get_card_from_deck()
    player1.append(card)
    return {"card": card}


@app.route("/get_last_cards_thrown")
def get_last_cards_thrown():
    return {"cards" : last_cards_thrown}


@app.route("/get_legalty")
def get_legalty():
    return {'legalty' : legalty}

@app.route("/check_legal_move", methods=["POST"])
def check_legale_move():
    global legalty
    request_data = json.loads(request.data)
    data = list(request_data['cards']).sort() 
    rank = int(str(request_data['cards'][0]).split('_')[0])
    shape = str(request_data['cards'][0]).split('_')[2]
    legalty = "true"
    pair_or_straight = ""
    joker = 0
    if "red_joker" in data or "black_joker" in data:
        joker = 1
    for card in data[1::]:
        card_propertis = card.split('_')
        if pair_or_straight == "":
            if rank == int(card_propertis[0]):
                pair_or_straight = "pair"
            elif shape == card_propertis[2] and 2 >= (int(card_propertis[0]) - rank) >= 1 and len(data) > 2:
                if int(card_propertis[0]) - rank == 2:
                    joker = 0
                    rank += 1
                rank += 1
                pair_or_straight = 'straight' 
            else:
                legalty = 'false'
                break
            continue
        if pair_or_straight == 'pair':  
            if int(card_propertis[0]) == rank:
                continue
            else:
                legalty = 'false'
                break
        elif pair_or_straight == 'straight':
            if joker == 1 and shape == card_propertis[2] and rank - int(card_propertis[0]) == -2:
                joker = 0
                rank += 2
            elif shape == card_propertis[2] and rank - int(card_propertis[0]) == -1:
                rank +=1
                continue
            else:
                legalty = 'false'
                break
    if legalty == "true":
        for c in last_cards_thrown: pile.append(c)
        for c in data : player1.remove(c)
        last_cards_thrown = data
    return legalty



def reset_game():
    for _ in range(5):
        player1.append(get_card_from_deck())
        player2.append(get_card_from_deck())
        player3.append(get_card_from_deck())
        player4.append(get_card_from_deck())

if __name__ == "__main__":
    reset_game()

    app.run(debug=True)