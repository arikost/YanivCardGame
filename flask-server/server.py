from datetime import datetime
import copy
from game import Game
from player import *
import json
import time
import csv
from flask import *
from flask_socketio import SocketIO,emit
from flask_cors import CORS
import random
"""globals"""
fieldnames = ['userName', 'password', 'totle_wins']
open_games_props = []
open_games_ins = {}
connected_users = []
num_of_open_games = 0

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app,cors_allowed_origins="*")


@socketio.on('opponent_join')
def opponent_join(data):
    global open_games_ins
    print(data)
    game = open_games_ins[data[1]]
    opponents = game.get_players_names()
    emit('opponent_join', {'opponents' : opponents, 'gameId': data[1]}, broadcast=True)
@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print(request.sid)
    print("client has connected")
    emit("connect",{"data":f"id: {request.sid} is connected"})

def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect",f"user {request.sid} disconnected",broadcast=True)

@app.route('/sign_up',methods=['POST'])
def sign_up():
    global fieldnames
    data = json.loads(request.data)
    with open('users.csv', 'a', newline='') as dataFile:
        writer = csv.DictWriter(dataFile, fieldnames=fieldnames)
        writer.writerow({'userName' : data['username'], 'password': data['password'], 'totle_wins': 0})
        dataFile.close()
    return {}
@app.route('/login', methods=['POST', 'GET'])
def login():
    global fieldnames, connected_users
    data = json.loads(request.data)
    user_exsit = False
    with open('users.csv', newline='') as dataFile:
        reader = csv.reader(dataFile)
        for row in reader:
            if row[0] == data['username'] and row[1] == data['password']:
                user_exsit = True
                break
    if user_exsit:
        connected_users.append(data['username'])
    return {'isValidUser' : user_exsit}

@app.route('/get_lobby_data', methods=['POST', 'GET'])
def get_lobby_data():
    global open_games_props, connected_users
    return{'games' : open_games_props, 'users' : connected_users}



@app.route("/create_game", methods=['POST'])
def create_game():
    global num_of_open_games, connected_users, open_games_props, open_games_ins
    num_of_open_games += 1
    data = json.loads(request.data)
    player = Player(data['username'])
    game = Game(player, num_of_open_games)
    open_games_ins[num_of_open_games] = game
    game_props = {"id" : game.id, "created_by" : player.name, "time_date" : datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "number_of_players" : 1, }
    open_games_props.append(game_props)
    return {"newGame" : game_props}



@app.route("/join_game", methods=['POST'])
def join_game():
    global connected_users, open_games_ins, open_games_props
    data = json.loads(request.data)
    game = open_games_ins[data['gameId']]

    game.add_player(Player(data['username']))
    if game.number_of_players == 4:
        game.reset_game()
    for game in open_games_props:
        if game['id'] == data['gameId']:
            game['number_of_players'] += 1 
    return {}

@app.route("/reset_round",methods=['POST', 'GET'])
def reset_round():
    global open_games_ins
    data = json.loads(request.data)
    print(data)
    game = open_games_ins[data['gameId']]
    print(game.get_players_names())
    for player in game.players:
        print(player.name)
        if player.name == data['username']:
            print(player.hand)
            return {'cards' : player.hand}

@app.route("/reset_game",methods=['POST'])
def reset_game():
    global open_games_ins
    data = json.loads(request.data)
    game = open_games_ins[data['gameId']]
    game.reset_game()
    return {}

@app.route("/is_yaniv",methods=['POST', 'GET'])
def is_yaniv():
    global open_games_ins
    data = json.loads(request.data)
    game = Game(open_games_ins[data['gameId']])
    return {'answer' : game.is_yaniv(data['username'])}




@app.route("/get_score",methods=['POST', 'GET'])
def get_score():
    pass

@app.route("/get_card_deck",methods=["POST", "GET"])
def get_card_deck():
    global open_games_ins
    data = json.loads(request.data)
    game = Game(open_games_ins[data['gameId']])
    game.pull_card_from_deck(data['username'])
    return{}

    
@app.route("/get_card_pile", methods=["POST", "GET"])
def get_card_pile():
    global open_games_ins
    data = json.loads(request.data)
    game = Game(open_games_ins[data['gameId']])
    game.pull_card_from_pile(data['username'], data['card'])
    return{}


@app.route("/get_pile",methods=["POST", "GET"])
def get_pile():
    global open_games_ins
    data = json.loads(request.data)
    game = Game(open_games_ins[data['gameId']])
    return {'pile' : game.pile}



@app.route("/check_legal_move", methods=["POST", "GET"])
def check_legale_move():
    global open_games_ins
    data = json.loads(request.data)
    game = Game(open_games_ins[data['gameId']])
    legalety = game.check_legal_move(data['username'], data['cards'])
    return {'legalety' : legalety}
    
if __name__ == "__main__":
    # game_test = Game(Player('arik1'), 1)
    # game_test.add_player(Player('arik2'))
    # game_test.add_player(Player('arik3'))
    # game_test.add_player(Player('arik4'))
    # game_test.reset_game()
    # for p in game_test.players:
    #     print(p.hand)
    
    socketio.run(app, debug=True,port=5001)
