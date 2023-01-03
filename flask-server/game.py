import random
import copy
from player import *
"""globals"""
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




class Game:

    def __init__(self, user:Player, id) -> None:
        self.id = id
        self.pile = []
        self.last_cards_thrown_buff = []
        self.last_cards_thrown = []
        self.card_deck = []
        self.number_of_players = 1
        self.players = [user]
        
    def add_player(self, player:Player):
        self.players.append(player)
        self.number_of_players += 1
    def remove_player(self, player_name:str):
        for player in self.players:
            if player.name == player_name:
                self.players.remove(player)
                self.number_of_players -= 1
                break
    def get_player(self, player_name):
        for p in self.players:
            if p.name == player_name:
                return p
        return None
    def get_players_names(self):
        players_names = []
        for p in self.players:
            players_names.append(p.name)
        return players_names
    
    def reset_game(self):
        for p in self.players:
            p.totle_score = 0
        self.reset_ruond()

    def reset_ruond(self):
        self.card_deck.clear()
        self.last_cards_thrown.clear()
        self.pile.clear()
        self.card_deck = copy.copy(cards)
        for player in self.players:
            player.hand.clear()
            player.current_score = 0
            player.is_ready = False
            for _ in range(5):
                player.hand.append(self.get_card_from_deck())
            player.hand.sort()

    def get_card_from_deck(self):
        if len(self.card_deck) < 2:
            self.card_deck = self.pile[:]
            self.pile.clear()
        i = random.randint(0, len(self.card_deck)-1)
        card = self.card_deck[i]
        self.card_deck.remove(card)
        return card
    
    def check_legal_move(self, player_name, cards:list):
        cards.sort()
        check1 = check_for_straghit(cards)
        check2 = check_for_pairs(cards)
        if len(check1) == len(cards) or len(check2) == len(cards) or len(cards) == 1:
            if len(check1) == len(cards) and len(check2) == 0:
                sort_straghit(cards)
                print("1::",cards)
            legalty = True
            for p in self.players:
                if p.name == player_name:  
                    self.last_cards_thrown_buff.clear()
                    for card in cards:
                        p.hand.remove(card)
                        self.last_cards_thrown_buff.append(card)
            print("2::",self.last_cards_thrown_buff)         
        else:
            legalty = False
       
        return legalty
    
    def pull_card_from_pile(self, player_name, card):
        for p in self.players:
            if p.name == player_name:
                p.hand.append(card)
        self.last_cards_thrown.remove(card)
        for c in self.last_cards_thrown:
            self.pile.append(c)
        self.last_cards_thrown = copy.copy(self.last_cards_thrown_buff)
        self.last_cards_thrown_buff.clear()
    
    def pull_card_from_deck(self, player_name):
        card = self.get_card_from_deck()
        print("pull_card_from_deck: ", card)
        for p in self.players:
            if p.name == player_name:
                p.hand.append(card)
                
        for c in self.last_cards_thrown:
            self.pile.append(c)
        self.last_cards_thrown = copy.copy(self.last_cards_thrown_buff)
        print("3::", self.last_cards_thrown)
        self.last_cards_thrown_buff.clear()
        return card
    
    def is_yaniv(self, player_name):
        for p in self.players:
            if p.name == player_name:
                return get_sum(p.hand) <=7
    def get_score(self, player_called_yaniv):
        """
        return value = {
            game_leader:string(player_name),
            how_called_yeniv = string(player_name),
            round_winner = string(player name)
            players_names = [list of names]
            players_score : [list of players score],
            players_totle_score: [list of players totle score],
            is_game_over : boolean(if one of the players has 150 points),
            players_hands: [list of players hands]
        }
        """
        retVal = {'how_called' : player_called_yaniv}
        players_score = []
        players_totle_score =[]
        game_leader = ""
        plyers_hands = []
        is_game_over = False
        round_winner = player_called_yaniv
        best_score = get_sum(self.get_player(player_called_yaniv).hand)
        #culcolating score and check for asaf
        for p in self.players:
            p.current_score = get_sum(p.hand)
            plyers_hands.append(p.hand)
            if p.current_score < best_score :
                best_score = p.current_score
                round_winner = p.name
        if round_winner != player_called_yaniv:
            self.get_player(player_called_yaniv).current_score +=30
        #initial return value data
        best_totle_score = 150
        for p in self.players:
            p.totle_score += p.current_score
            if p.totle_score < best_totle_score:
                game_leader = p.name
                best_totle_score = p.totle_score
            if p.totle_score >= 150:
                is_game_over = True
            players_score.append(p.current_score)
            players_totle_score.append(p.totle_score)
        retVal['players_score'] = players_score
        retVal['players_totle_score'] = players_totle_score
        retVal['plyers_hands'] = plyers_hands
        retVal['game_leader'] = game_leader
        retVal['is_game_over'] = is_game_over
        retVal['players_names'] = self.get_players_names()
        retVal['round_winner'] = round_winner
        return retVal