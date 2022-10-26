

import copy

import json
import time

from flask import *
import random

"""globals"""
pile = []
last_cards_thrown_buff = []
last_cards_thrown = []
player1 = []
player2 = []
player3 = []
player4 = []
score = {
    "player1" : 0,
    "player2" : 0,
    "player3" : 0,
    "player4" : 0
    }
totle_score = {
    "player1" : 0,
    "player2" : 0,
    "player3" : 0,
    "player4" : 0
    }
legalty = bool()
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
card_deck = []

def get_card_from_deck():
    global card_deck, pile
    if len(card_deck) < 2:
        card_deck = pile[:]
        pile.clear()
    i = random.randint(0, len(card_deck)-1)
    card = card_deck[i]
    card_deck.remove(card)
    return card


app = Flask(__name__)
@app.route("/is_yaniv")
def is_yaniv():
    return {"answer" : get_sum(player1) <= 7}

@app.route("/reset_round", methods=['POST'])
def reset_round():
    reset_ruond_helper()
    return ""
@app.route("/reset_game", methods=['POST'])
def reset_game():
    global totle_score
    totle_score['player1'] = 0
    totle_score['player2'] = 0
    totle_score['player3'] = 0
    totle_score['player4'] = 0
    reset_ruond_helper()
    return ""


@app.route("/yaniv", methods=['POST'])
def yaniv():
    global score, totle_score
    request_data = json.loads(request.data)
    player = request_data['player']
    print(player)
    player_score = get_sum(eval(player))
    for k in score.keys():
        if k == player:
            continue
        p = get_sum(eval(k))
        if p <= player_score:
            score[player] = 35
        score[k] = p
        totle_score[k] += p
    return ""


@app.route("/get_score")
def get_score():
    global score, totle_score
    print(score)
    print(totle_score)
    for k in score.keys():
        totle_score[k] += score[k] 
    game_over = False
    for v in totle_score.values():
        if v > 150:
            game_over = True

    round_winner = ""
    game_leader = ""

    best_score = 150
    for k in totle_score.keys():
        if totle_score[k] < best_score:
            best_score = totle_score[k]
            game_leader = k   
    best_score = 50
    for k in score.keys():
        if score[k] < best_score:
            best_score = score[k]
            round_winner = k   
    print("---------------------------------")
    return {"score": [score['player1'], score['player2'], score['player3'], score['player4']], 
            "totle_score" : [totle_score['player1'], totle_score['player2'], totle_score['player3'], totle_score['player4']], 
            "game_over" : game_over,
            "game_leader" : game_leader, 
            "round_winner" : round_winner
            }

@app.route("/reset_player1_hand")
def reset_player1_hand():
    player1.sort()
    return {"members": player1}

@app.route("/get_card_deck")
def get_card_deck():
    global last_cards_thrown_buff, last_cards_thrown
    card = get_card_from_deck()
    player1.append(card)
    for c in last_cards_thrown:
        pile.append(c)
    last_cards_thrown = copy.copy(last_cards_thrown_buff)
    return {"card": card}

@app.route("/get_card_pile", methods=['POST'])
def get_card_pile():
    global pile, last_cards_thrown
    request_data = json.loads(request.data)
    card = request_data['card']
    player1.append(card)
    last_cards_thrown.remove(card)
    for c in last_cards_thrown:
        pile.append(c)
    last_cards_thrown = copy.copy(last_cards_thrown_buff)


    print("pile: ---", pile)
    return ''

@app.route("/get_pile")
def get_pile():
    return {"cards" : pile}



@app.route("/check_legal_move", methods=["POST", "GET"])
def check_legale_move():
    global legalty, last_cards_thrown
    request_data = json.loads(request.data)
    data = list(request_data['cards']) 
    
    data.sort()
    check1 = check_for_straghit(data)
    check2 = check_for_pairs(data)
    if len(check1) == len(data) or len(check2) == len(data) or len(data) == 1:
        legalty = True
    else:
        legalty = False
    if legalty:
        last_cards_thrown_buff.clear()
        for x in data : 
            player1.remove(x)
            last_cards_thrown_buff.append(x)
        
        print("pile : -----", pile)
    return {'legalty' : legalty}
@app.route("/sim_player2")
def sim_player2():
    global last_cards_thrown, pile, player2
    dec = simulate(player2)
    dec['cards_to_throw'] = list(dec['cards_to_throw'])
    print(dec)

    if dec['yaniv']:
        return dec

    if dec["pile_or_deck"] == 'deck':
        player2.append(get_card_from_deck())
        last_cards_thrown.clear()
    else:
        last_cards_thrown.remove(dec['pile_or_deck'])
        player2.append(dec['pile_or_deck'])
        for c in last_cards_thrown: 
            pile.append(copy.copy(c))
    for card in dec['cards_to_throw']:
        player2.remove(card)
    last_cards_thrown = copy.copy(dec['cards_to_throw'])

    return dec
@app.route("/sim_player3")
def sim_player3():
    global last_cards_thrown, pile, player3
    dec = simulate(player3)
    dec['cards_to_throw'] = list(dec['cards_to_throw'])
    print(dec)

    if dec['yaniv']:
        return dec

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

    return dec

@app.route("/sim_player4")
def sim_player4():
    global last_cards_thrown, pile, player4
    dec = simulate(player4)
    dec['cards_to_throw'] = list(dec['cards_to_throw'])
    print(dec)

    if dec['yaniv']:
        return dec

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
    completing_card_for_straghit = ""# a card that can complite a straghit and is draweble
    completing_card_for_pair = ""# a card that can complite a pair and is draweble
    missing_cards_for_straghit = [] #cards that can replace a joker in a strghit
    if len(straight) != 0 and len(pair) != 0:
        
        missing_cards_for_straghit = find_missing_cards_for_straghit(straight)
        
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
    elif get_sum(straight) > 6 and completing_card_for_pair != "":
        decision['cards_to_throw'] = straight
        decision['pile_or_deck'] = completing_card_for_pair
    elif get_sum(straight) < get_sum(pair):
        decision['cards_to_throw'] = pair
        copy_hand = [card for card in player_hand if not card in pair]
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
    
    elif len(straight) == 0 and get_sum(pair) > 0:
        print("in case len(straight) == 0 and get_sum(pair) > 4")
        decision['cards_to_throw'] = pair
        if int(last_cards_thrown[0][:2]) > 5:
            decision['pile_or_deck'] = last_cards_thrown[0] 
        elif int(last_cards_thrown[-1][:2]) > 5:
            decision['pile_or_deck'] = last_cards_thrown[-1] 
        else:
            decision['pile_or_deck'] = 'deck'
    elif get_sum(pair) == 0 and get_sum(straight) == 0:
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
            if int(last_cards_thrown[0][:2]) < 4:
                decision['pile_or_deck'] = last_cards_thrown[0]
            else:
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
def reset_ruond_helper():
    global card_deck, cards, player1, player2, player3, player4, score
    card_deck = copy.copy(cards)
    score['player1'] = 0
    score['player2'] = 0
    score['player3'] = 0
    score['player4'] = 0
    for _ in range(5):
        player1.append(get_card_from_deck())
        player2.append(get_card_from_deck())
        player3.append(get_card_from_deck())
        player4.append(get_card_from_deck())

if __name__ == "__main__":
    reset_ruond_helper()
    app.run(debug=True)