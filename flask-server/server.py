

import copy

import json
from pydoc import describe

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
    '00_red_joker',
    '00_black_joker'
]


def get_card_from_deck():
    global cards, pile
    if len(cards) < 2:
        cards = pile[:]
        pile.clear()
    i = random.randint(0, len(cards)-1)
    card = cards[i]
    cards.remove(card)
    return card


app = Flask(__name__)


@app.route("/get_score")
def get_score():
    global player1, player2, player3, player4
     
    score = {
        "player1" : get_sum(player1),
        "player2" : get_sum(player2),
        "player3" : get_sum(player3),
        "player4" : get_sum(player4)
        }
    return score

@app.route("/reset_player1_hand")
def reset_player1_hand():
    player1.sort()
    return {"members": player1}

@app.route("/get_card_deck")
def get_card_deck():
    card = get_card_from_deck()
    player1.append(card)
    return {"card": card}

@app.route("/get_card_pile", methods=['POST'])
def get_card_pile():
    global pile
    request_data = json.loads(request.data)
    player1.append(request_data['card'])
    pile.remove(request_data['card'])
    return ''

@app.route("/get_pile")
def get_pile():
    return {"cards" : pile}


@app.route("/get_legalty")
def get_legalty():
    return {'legalty' : legalty}

@app.route("/check_legal_move", methods=["POST"])
def check_legale_move():
    global legalty, last_cards_thrown
    request_data = json.loads(request.data)
    data = list(request_data['cards']) 
    data.sort()
    rank = int(str(data[0]).split('_')[0])
    shape = str(data[0]).split('_')[2]
    legalty = "true"
    pair_or_straight = ""
    joker = 0
    if "00_red_joker" in data or "00_black_joker" in data:
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
        last_cards_thrown.clear()
        for x in data : 
            player1.remove(x)
            last_cards_thrown.append(x)
        for c in last_cards_thrown: 
            pile.append(copy.copy(c))
        print("pile : -----", pile)
    return legalty
@app.route("/sim_player2")
def sim_player2():
    global last_cards_thrown, pile, player2
    dec = simulate(player2)
    dec['cards_to_throw'] = list(dec['cards_to_throw'])

    if dec['yaniv']:
        return dec
    print(dec)
    print(last_cards_thrown)

    if dec["pile_or_deck"] == 'deck':
        player2.append(get_card_from_deck())
    else:
        last_cards_thrown.remove(dec['pile_or_deck'])
        player2.append(dec['pile_or_deck'])
    print("last_cards_thrown: ---", last_cards_thrown)
    for c in last_cards_thrown: 
        pile.append(copy.copy(c))
    for card in dec['cards_to_throw']:
        player2.remove(card)
    last_cards_thrown = copy.copy(dec['cards_to_throw'])
    print("pile : -----", pile)

    return dec
@app.route("/sim_player3")
def sim_player3():
    global last_cards_thrown, pile, player3
    dec = simulate(player3)
    dec['cards_to_throw'] = list(dec['cards_to_throw'])
    if dec['yaniv']:
        return dec
    print(dec)
    print("last_cards_thrown: ---", last_cards_thrown)

    if dec["pile_or_deck"] == 'deck':
        player3.append(get_card_from_deck())
    else:
        last_cards_thrown.remove(dec['pile_or_deck'])
        player3.append(dec['pile_or_deck'])
    for c in last_cards_thrown: 
        pile.append(copy.copy(c))
    for card in dec['cards_to_throw']:
        player3.remove(card)
    last_cards_thrown = copy.copy(dec['cards_to_throw'])
    print("pile : -----", pile)
    return dec

@app.route("/sim_player4")
def sim_player4():
    global last_cards_thrown, pile, player4
    dec = simulate(player4)
    dec['cards_to_throw'] = list(dec['cards_to_throw'])
    if dec['yaniv']:
        return dec
    print(dec)
    print("last_cards_thrown: ---", last_cards_thrown)

    if dec["pile_or_deck"] == 'deck':
        player4.append(get_card_from_deck())
    else:
        last_cards_thrown.remove(dec['pile_or_deck'])
        player4.append(dec['pile_or_deck'])
    for c in last_cards_thrown: 
        pile.append(copy.copy(c))
    for card in dec['cards_to_throw']:
        player4.remove(card)
    last_cards_thrown = copy.copy(dec['cards_to_throw'])
    print("pile : -----", pile)

    return dec



def simulate(player_hand:list):
    global last_cards_thrown
    decision = {'cards_to_throw' : [],
                'pile_or_deck' : "",
                'yaniv' : False
    }
    sum_cards = 0
    for card in player_hand:
        card_prop = str(card).split('_')        
        sum_cards += int(card_prop[0])
    if sum_cards <= 7:
        decision['yaniv'] = True
        return decision 
    player_hand.sort()
    #check fo pairs
    pair = set(check_for_pairs(player_hand))
    #check for straight
    straight = set(check_for_straghit(player_hand))
    print(player_hand)
    dispute_card = "" # a card that exist in both straghit and pair
    completing_card_for_straghit = ""# a card that can complite a straghit and is draweble
    completing_card_for_pair = ""# a card that can complite a pair and is draweble
    missing_cards_for_straghit = [] #cards that can replace a joker in a strghit
    if len(straight) != 0 and len(pair) != 0:
        
        missing_cards_for_straghit = find_missing_cards_for_straghit(straight)
        for card in pair:
            if card in straight:
                dispute_card = copy.copy(card)
        
        if last_cards_thrown[0] in missing_cards_for_straghit:
            completing_card_for_straghit = copy.copy(last_cards_thrown[0])
        elif last_cards_thrown[-1] in missing_cards_for_straghit:
            completing_card_for_straghit = copy.copy(last_cards_thrown[-1])
        for card in player_hand:
            if card[:2] == last_cards_thrown[0][:2]:
                completing_card_for_pair = last_cards_thrown[0]
            if card[:2] == last_cards_thrown[-1][:2]:
                completing_card_for_pair = last_cards_thrown[-1]
    
    if get_sum(pair) > 6 and completing_card_for_straghit != "":
        print("in case get_sum(pair) > 6 and completing_card_for_straghit != """)

        decision['cards_to_throw'] = pair
        decision['pile_or_deck'] = completing_card_for_straghit
    elif get_sum(straight) > get_sum(pair):
        print("in case get_sum(straight) > get_sum(pair)")

        decision['cards_to_throw'] = straight
        copy_hand = [card for card in player_hand if not card in straight]
        copy_hand.append(last_cards_thrown[0])
        copy_hand.sort()
        opt1 = get_sum(check_for_pairs(copy_hand))
        copy_hand.remove(last_cards_thrown[0])
        copy_hand.append(last_cards_thrown[-1])
        copy_hand.sort
        opt2 = get_sum(check_for_pairs(copy_hand))
        if  opt1 > opt2:
            decision['pile_or_deck'] = last_cards_thrown[0]
        elif opt1 < opt2:
            decision['pile_or_deck'] = last_cards_thrown[-1]
        elif opt2 == 0:
            decision['pile_or_deck'] = 'deck'
        else:
            decision['pile_or_deck'] = last_cards_thrown[0]
    elif len(straight) == 0 and get_sum(pair) > 4:
        print("in case len(straight) == 0 and get_sum(pair) > 4")
        decision['cards_to_throw'] = pair
        if int(last_cards_thrown[0][:2]) > 5:
            decision['pile_or_deck'] = last_cards_thrown[0] 
        elif int(last_cards_thrown[-1][:2]) > 5:
            decision['pile_or_deck'] = last_cards_thrown[-1] 
        else:
            decision['pile_or_deck'] = 'deck'
    elif len(pair) == 0 and len(straight) == 0:
        print("in case no pair no straghit")
        player_hand_copy = copy.copy(player_hand)
        player_hand_copy.append(last_cards_thrown[0])
        player_hand_copy.sort()
        opt_for_pair1 = check_for_pairs(player_hand_copy)
        opt_for_str1 = check_for_straghit(player_hand_copy)
        player_hand_copy.remove(last_cards_thrown[0])
        player_hand_copy.append(last_cards_thrown[-1])
        player_hand_copy.sort()
        opt_for_pair2 = check_for_pairs(player_hand_copy)
        opt_for_str2 = check_for_straghit(player_hand_copy)
        player_hand_copy.remove(last_cards_thrown[-1])
        options = [opt_for_pair1, opt_for_pair2, opt_for_str1, opt_for_str2]
        final_opt = options[0]
        max_sum = 0
        for opt in options:
            x = get_sum(opt)
            if x > max_sum:
                max_sum = x
                final_opt = opt
        if max_sum == 0:
            decision['cards_to_throw'] = [player_hand[-1]]
            decision['pile_or_deck'] = "deck"
        else:
            for card in player_hand_copy:
                if card in final_opt:
                    player_hand_copy.remove(card)
                    final_opt.remove(card)
            decision['cards_to_throw'] = [player_hand_copy[-1]]
            decision['pile_or_deck'] = final_opt.pop()

    return decision

def get_sum(cards_set):
    cards_sum = 0
    for card in cards_set:
        cards_sum += int(card[:2])
    return cards_sum

def check_for_straghit(player_hand):
    straight = set()
    current_straghit = set()
    joker_red = 0
    joker_black = 0
    if "00_red_joker" in player_hand:
        joker_red += 1
    if "00_black_joker" in player_hand:
        joker_black += 1
    start_index = joker_red + joker_black
    for i in range(start_index, len(player_hand)-1):
        card_i_prop = str(player_hand[i]).split('_')        
        for j in range(i+1, len(player_hand)):
            card_j_prop = str(player_hand[j]).split('_')
            if int(card_i_prop[0]) == int(card_j_prop[0])-1 and card_i_prop[2] == card_j_prop[2]:
                current_straghit.add('_'.join(card_i_prop))
                current_straghit.add('_'.join(card_j_prop))
                card_i_prop = card_j_prop
            else:
                if joker_black == 1:
                    if int(card_i_prop[0]) == int(card_j_prop[0])-2 and card_i_prop[2] == card_j_prop[2]:
                        current_straghit.add("00_black_joker")
                        current_straghit.add('_'.join(card_i_prop))
                        current_straghit.add('_'.join(card_j_prop))
                        card_i_prop = card_j_prop
                if joker_red == 1:
                    if int(card_i_prop[0]) == int(card_j_prop[0])-2 and card_i_prop[2] == card_j_prop[2]:
                        current_straghit.add("00_red_joker")
                        current_straghit.add('_'.join(card_i_prop))
                        current_straghit.add('_'.join(card_j_prop))
                        card_i_prop = card_j_prop
                if joker_red == 1 and joker_black == 1:
                    if int(card_i_prop[0]) == int(card_j_prop[0])-3 and card_i_prop[2] == card_j_prop[2]:
                        current_straghit.add("00_red_joker")
                        current_straghit.add("00_black_joker")
                        current_straghit.add('_'.join(card_i_prop))
                        current_straghit.add('_'.join(card_j_prop))
                        card_i_prop = card_j_prop

    
        if len(current_straghit) > 2:
            straight = copy.copy(current_straghit)
        current_straghit.clear()
    return straight

def check_for_pairs(player_hand):
    pair1 = set()
    pair2 = set()
    for i in range(len(player_hand)-1):
        if player_hand[i][:2] == player_hand[i+1][:2]:
            if len(pair1) == 0:
                pair1.add(player_hand[i])
                pair1.add(player_hand[i+1])
            elif player_hand[i] in pair1:
                pair1.add(player_hand[i+1])
            else:
                pair2.add(player_hand[i])
                pair2.add(player_hand[i+1])
    
    if get_sum(pair1) >= get_sum(pair2):
        return pair1
    else:
        return pair2


def find_missing_cards_for_straghit(straghit):
    card_list = list(straghit)
    card_list.sort()
    return_val = []
    for i in range(len(card_list)-1):
        if int(card_list[i][:2]) == 0:
            continue
        if int(card_list[i][:2]) == int(card_list[i+1][:2])-2:
            rank = int(card_list[i][:2])+1
            return_val.append(str(rank)+ card_list[i][2::])
        if int(card_list[i][:2]) == int(card_list[i+1][:2])-3:
            rank = int(card_list[i][:2])+1
            return_val.append(str(rank)+ card_list[i][2::])
            return_val.append(str(rank+1)+ card_list[i][2::])
        
    return return_val
def reset_game():
    for _ in range(5):
        player1.append(get_card_from_deck())
        player2.append(get_card_from_deck())
        player3.append(get_card_from_deck())
        player4.append(get_card_from_deck())

if __name__ == "__main__":
    reset_game()
    app.run(debug=True)