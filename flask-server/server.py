from datetime import datetime
import copy
from game import Game
from player import *
import json
import random
from flask import *
from flask_socketio import SocketIO,emit
from flask_cors import CORS
import mysql.connector
"""globals"""
open_games_ins = {}
connected_users = {}
num_of_open_games = 0

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app,cors_allowed_origins="*")


@socketio.on('update_oppenents')
def update_oppenents(data):
    global open_games_ins
    game:Game = open_games_ins[data]
    opponents = game.get_players_names()
    for user in game.players:
        emit('update_oppenents', {'opponents' : opponents}, room=connected_users[user.name])      
        if user.is_ready:
            for p in game.players:
                if p.name != user.name:
                    socketio.emit('opponent_ready', {'opponent' : user.name}, room=connected_users[p.name])



@app.route("/join_game", methods=['POST'])
def join_game():
    global connected_users, open_games_ins
    data = json.loads(request.data)
    game:Game = open_games_ins[data['gameId']]
    game.add_player(Player(data['username']))
    print("join_game(event call)",game.get_players_names())
    #initial connection to database
    mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'arik',
        password = 'abcdef',
        database = 'mydb'
    )
    players = " ".join(game.get_players_names())
    query = "UPDATE games SET current_players = %s WHERE id = %s"
    cursor = mydb.cursor()
    cursor.execute(query,(players, game.id))
    mydb.commit()
    cursor.execute("SELECT * FROM games")
    socketio.emit('update_games', cursor.fetchall(), broadcast=True)
    
    #close connection
    cursor.close()
    mydb.close()
    return {'id' : game.id}

  

@socketio.on("user_connect")
def connected(username):
    """event listener when client connects to the server"""
    if not username in connected_users.keys():
        connected_users[username] = request.sid
        print(username," has connected\t id:", request.sid)
        mydb = mysql.connector.connect(
            host = 'localhost',
            user = 'arik',
            password = 'abcdef',
            database = 'mydb'
        )
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM games")
        games = cursor.fetchall()
        #close connection
        cursor.close()
        mydb.close()
        socketio.emit('update_games', games, broadcast=True)

@app.route('/opponent_leaveing', methods=['POST'])
def opponent_leaveing():
    data = json.loads(request.data)
    game:Game = open_games_ins[data['gameId']]
    game.remove_player(data['player_name'])
    print("opponent_leaveing: ", game.get_players_names())
    #initial connection to database
    mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'arik',
        password = 'abcdef',
        database = 'mydb'
    )
    cursor = mydb.cursor()
    if game.number_of_players == 0:
        cursor.execute("DELETE from games WHERE id = %s", (data['gameId'],))
        open_games_ins.pop(game.id)
    else:
        query = "UPDATE games SET current_players = %s, number_of_players = %s WHERE id = %s"
        cursor.execute(query,(" ".join(game.get_players_names()),game.number_of_players ,game.id))
    
    cursor.execute("SELECT * FROM games")
    games = cursor.fetchall()

    #close connection    
    mydb.commit()
    cursor.close()
    mydb.close()
    socketio.emit('update_games', games, broadcast=True)

    return {}

@app.route('/ready_to_start', methods=['POST'])
def ready_to_start():
    global connected_users, open_games_ins
    data = json.loads(request.data)
    game:Game = open_games_ins[data['gameId']]
    all_ready = 0
    for p in game.players:
        if p.name == data['username']:
            p.is_ready = True
        else:
            socketio.emit('opponent_ready', {'opponent' : data['username']}, room=connected_users[p.name])
        if p.is_ready:
            all_ready += 1
    if all_ready == 4:

        game.reset_ruond()
        player_start = game.get_players_names()[random.randint(0,3)]
        for p in game.players:
            socketio.emit('reset_cards', {'cards' : p.hand, 'curr_player' : player_start}, room=connected_users[p.name])
    return {}


@app.route('/sign_up',methods=['POST'])
def sign_up():
    data = json.loads(request.data)
    #initial connection to database
    mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'arik',
        password = 'abcdef',
        database = 'mydb'
    )
    cursor = mydb.cursor()
    #check if user exist
    cursor.execute("SELECT name from users")
    for name in cursor:
        if name == data['username']:
            cursor.close()
            mydb.close()
            return {'user_exist': True}
    #insert new user
    cursor.execute("SELECT count(*) FROM users")
    num_of_users = int(cursor.fetchone()[0] + 1)
    insert_new_user = ("INSERT INTO users VALUES(%s, %s, %s, %s, %s)")
    cursor.execute(insert_new_user, (num_of_users, data['username'], data['password'], 0, 0))
    #save changes
    mydb.commit()
    #close connection
    cursor.close()
    mydb.close()
    return {'user_exist': False}
@app.route('/login', methods=['POST', 'GET'])
def login():
    global  connected_users
    data = json.loads(request.data)
    user_exsit = False
    #initial connection to database
    mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'arik',
        password = 'abcdef',
        database = 'mydb'
    )
    cursor = mydb.cursor()
    #check if user exist and matching password
    cursor.execute("SELECT name, password From users")
    for (name, password) in cursor:
        user_exsit = (name == data['username'] and password == data['password'])
        if user_exsit: break 
           
    #insert new user
    #close connection
    cursor.fetchall()
    cursor.close()
    mydb.close()
    return {'isValidUser' : user_exsit}




@app.route("/create_game", methods=['POST'])
def create_game():
    global num_of_open_games, connected_users, open_games_ins
    num_of_open_games += 1
    data = json.loads(request.data)
    player = Player(data['username'])
    game = Game(player, num_of_open_games)
    open_games_ins[num_of_open_games] = game
    #initial connection to database
    mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'arik',
        password = 'abcdef',
        database = 'mydb'
    )
    cursor = mydb.cursor()
    insert_new_game = ("INSERT INTO games VALUES(%s, %s, %s, %s, %s)")
    players = ", ".join(game.get_players_names())
    cursor.execute(insert_new_game, (
            num_of_open_games, 
            data['username'], 
            datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 
            players, 
            game.number_of_players
        ))
    cursor.execute("SELECT count(*) FROM games")
    is_created = int(cursor.fetchone()[0]) == num_of_open_games+1
    cursor.execute("SELECT * FROM games")
    games = cursor.fetchall()
    print(games)
    socketio.emit('update_games', games, broadcast=True)
    #close connection    
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"is_created" : is_created, "id" : game.id}




@app.route("/reset_round",methods=['POST', 'GET'])
def reset_round():
    global open_games_ins
    data = json.loads(request.data)
    print(data)
    game:Game = open_games_ins[data['gameId']]
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
    game:Game = open_games_ins[data['gameId']]
    game.reset_game()
    return {}

@app.route("/yaniv_called", methods=["POST"])
def yaniv_called():
    global open_games_ins
    data = json.loads(request.data)
    game:Game = open_games_ins[data['gameId']]
    score = game.get_score(data['username'])
    for p in game.get_players_names():
        socketio.emit('yaniv', score, room=connected_users[p])
    return {}

@app.route("/get_card_deck",methods=["POST", "GET"])
def get_card_deck():
    global open_games_ins
    data = json.loads(request.data)
    game:Game = open_games_ins[data['gameId']]
    card = game.pull_card_from_deck(data['username'])
    is_yaniv = game.is_yaniv(data['username'])
    players = game.get_players_names()
    next_player = players.index(data['username'])
    for p in players:
        socketio.emit('update_center',{ 'current_player':players[(next_player+1) % 4], 
        'last_cards' : game.last_cards_thrown, 'pile' : game.pile[-5::]},
         room=connected_users[p])
    return{'card' : card, 'is_yaniv' : is_yaniv}

    
@app.route("/get_card_pile", methods=["POST", "GET"])
def get_card_pile():
    global open_games_ins
    data = json.loads(request.data)
    game:Game = open_games_ins[data['gameId']]
    game.pull_card_from_pile(data['username'], data['card'])
    is_yaniv = game.is_yaniv(data['username'])
    players = game.get_players_names()
    next_player = players.index(data['username'])
    for p in players:
        socketio.emit('update_center',{ 'current_player':players[(next_player+1) % 4], 
        'last_cards' : game.last_cards_thrown, 'pile' : game.pile[-5::]},
         room=connected_users[p])
    return{'is_yaniv' : is_yaniv}


@app.route("/check_legal_move", methods=["POST", "GET"])
def check_legale_move():
    global open_games_ins
    data = json.loads(request.data)
    game:Game = open_games_ins[data['gameId']]
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