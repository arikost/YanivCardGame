import React, { Component } from 'react';
import "../App.css";
import Game from './game';
import { io } from "socket.io-client";

var socket;

class Lobby extends Component {
   
    constructor(props){    
        super(props)
        this.state = { 
        userName : this.props.value,
        currentUsers : [],
        currentGames : [],
        gameId: 0,
        inGame : false,
        }
        socket = io("localhost:5001/", {
            transports: ["websocket"],
            cors: {
            origin: "http://localhost:3000/",
            },
        });
    }
    componentDidMount(){
        console.log("lobby mounted");
        socket.emit('user_connect', this.state.userName);
        socket.on('update_games', (data)=>{
            console.log("update_games",data)
            this.setState({
                currentGames: data
            });
        });
        
    }
    render() { 
        const {currentGames, userName, inGame, gameId} = this.state;
        if(inGame){
            return(
                <Game id={gameId} value={userName} onDelete={() =>{
                    this.setState({inGame: false});
                    fetch('opponent_leaveing',{
                        'method': 'POST',
                        headers : {
                          'Content-Type':'application/json'
                        },
                        body: JSON.stringify({
                          player_name : this.state.userName,
                          gameId : this.state.gameId,
                        })
                    })
                }}></Game>
            )
        }
        return (
            <div className='sign-up'>
                <div className='sign-up-inner'>
                <h3>{"Welcome  "+userName}</h3>
                <div>
                    <button className='btn btn-primary lr' onClick={this.createNewGame.bind(this)}>Create New Game</button>
                    <button className='btn btn-primary m-2 lr' hidden={true}>Play against the computer</button>
                </div>
                <style>{`
                    table, th, td{
                    border-bottom: 1px solid #ddd;
                    padding: 15px;
                    text-align: left;
                    }
                `}</style>
                <table >
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Created By</th>
                        <th>In Time</th>
                        <th>Players</th>
                        <th></th>
                    </tr>
                </thead>
                
                    {currentGames.map((game) =>
                    <tbody>
                    <tr>
                        <td>{game[0]}</td>
                        <td>{game[1]}</td>
                        <td>{game[2]}</td>
                        <td>{game[3]}</td>
                        <td><button key={game[0]} className='btn btn-primary m-2 sm'
                                disabled={game[4] === 4}
                                onClick={() => this.joinGame(game[0])}
                            >join
                            </button>
                            </td>
                    </tr>
                </tbody>
                )}
                </table>
                </div>
            </div>
        );
    }
    createNewGame(){
        fetch('/create_game', {
            'method' : 'POST',
            headers : {
                'Content-Type':'application/json'
            },
            body: JSON.stringify({
                username: this.state.userName
            })
        }).then(
            response => response.json()
        ).catch(error => console.log(error)).then(
            (response) =>{
                console.log("creatNewGame response", response);
                this.setState({
                    gameId : response.id,
                    inGame : true
                });
            }
        )
    }
    joinGame(gameId){
        fetch('/join_game', {
            'method': 'POST',
            headers : {
            'Content-Type':'application/json'
            },
            body: JSON.stringify({
                username : this.state.userName,
                gameId : gameId
            })
        }).then(
            response => response.json()
        ).catch(error => console.log(error))
        this.setState({
            gameId : gameId,
            inGame : true
        })    
    }
}
 
export {Lobby, socket};
