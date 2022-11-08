import copy

class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.hand = []
        self.current_score = 0
        self.totle_score = 0
    
def simulate(player_hand:list):
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
    pair = check_for_pairs(player_hand)
    #check for straight
    straight = check_for_straghit(player_hand)
    if len(straight) > 2:
        straight.sort()
        sort_straghit(straight)
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
        options = [opt_for_pair1, opt_for_str1]
        if len(last_cards_thrown) > 1:
            player_hand_copy.append(last_cards_thrown[-1])
            player_hand_copy.sort()
       
            opt_for_pair2 = check_for_pairs(player_hand_copy)
            opt_for_str2 = check_for_straghit(player_hand_copy)
            player_hand_copy.remove(last_cards_thrown[-1])
            options.append( opt_for_pair2)
            options.append( opt_for_str2)
        final_opt = options[0]
        max_sum = 0
        for opt in options:
            x = get_sum(opt)
            if x > max_sum:
                max_sum = x
                final_opt = opt
        if max_sum == 0:
            decision['cards_to_throw'] = [player_hand[-1]]
            if int(last_cards_thrown[0][:2]) < 2:
                decision['pile_or_deck'] = last_cards_thrown[0]
            else:
                decision['pile_or_deck'] = "deck"
        else:
            for card in player_hand_copy:
                if card in final_opt:
                    final_opt.remove(card)
                else:
                    decision['cards_to_throw'] = [card]
            
            
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
        
        if len(current_straghit) == 2 and joker_red == 1:
            current_straghit.add("00_red_joker")
        elif len(current_straghit) == 2 and joker_black == 1:
            current_straghit.add("00_black_joker")
        if len(current_straghit) > 2 and len(current_straghit) > len(straight):
            straight = copy.copy(current_straghit)
        current_straghit.clear()
    return list(straight)

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
        return list(pair1)
    else:
        return list(pair2)
def sort_straghit(straghit:list):
    straghit.sort()
    ms = find_missing_cards_for_straghit(straghit)
    print(ms)
    if len(ms) == 1:
        if (straghit[0] == '00_red_joker' or  straghit[0] == '00_black_joker') and straghit[1][:2] == "01":
            temp = straghit[2]
            straghit[2] = straghit[0]
            straghit[0] = temp
        else:
            temp = straghit[1] 
            straghit[1] = straghit[0]
            straghit[0] = temp
    elif len(ms) == 2:
        temp = straghit[2] 
        straghit[2] = straghit[0]
        straghit[0] = temp

def find_missing_cards_for_straghit(straghit):
    card_list = list(straghit)
    card_list.sort()
    return_val = []
    for i in range(len(card_list)-1):
        if int(card_list[i][:2]) == 0:
            continue
        if int(card_list[i][:2]) == int(card_list[i+1][:2])-2:
            rank = int(card_list[i][:2])+1
            if rank < 10:
                return_val.append("0"+str(rank)+ card_list[i][2::])
            else:
                return_val.append(str(rank)+ card_list[i][2::])

        if int(card_list[i][:2]) == int(card_list[i+1][:2])-3:
            rank = int(card_list[i][:2])+1
            if rank < 10:
                return_val.append("0"+str(rank)+ card_list[i][2::])
            else:
                return_val.append(str(rank)+ card_list[i][2::])
            if rank < 9:
                return_val.append("0"+str(rank+1)+ card_list[i][2::])
            elif rank < 13:
                return_val.append(str(rank+1)+ card_list[i][2::])
    if int(card_list[0][:2]) == 0 and int(card_list[1][:2]) == 1:
        rank = int(card_list[-1][:2])
        if rank < 9:
            return_val.append("0"+str(rank+1)+ card_list[-1][2::])
        elif rank < 13:
            return_val.append(str(rank+1)+ card_list[-1][2::])
    elif int(card_list[0][:2]) == int(card_list[1][:2])-1 and int(card_list[0][:2]) != 0:
        rank = int(card_list[0][:2])
        if rank != 0:
            if rank < 11:
                return_val.append("0"+str(rank-1)+ card_list[0][2::])
            else:
                return_val.append(str(rank-1)+ card_list[0][2::])
        if rank < 8:
            return_val.append("0"+str(rank+2)+ card_list[0][2::])
        elif rank < 12:
            return_val.append(str(rank+2)+ card_list[0][2::])

    return return_val
