import React, { Component } from 'react';
import "../App.css";
import Game from './game';
import { io } from "socket.io-client";

class Lobby extends Component {
   
    constructor(props){    
        super(props)
        this.state = { 
        userName : this.props.value,
        currentUsers : [],
        currentGames : [],
        gameId: 0,
        inGame : false,
        socket : null
        } 
    }
    componentDidMount(){
        fetch('/get_lobby_data').then(
            res => res.json()
        ).then(
            (result) => {
                console.log(result);
                this.setState({
                    currentGames : result.games,
                    currentUsers : result.users
                })
            }
        )
        console.log(this.state)
    }
    render() { 
        const {currentGames, userName, inGame, gameId, socket} = this.state;
        if(inGame){
            return(
                <Game id={gameId} value={userName} socket={socket}></Game>
            )
        }
        return (
            <div className='sign-up'>
                <div className='sign-up-inner'>
                <h3>{"Welcome  "+userName}</h3>
                <div>
                    <button className='btn btn-primary lr' onClick={this.createNewGame.bind(this)}>Create New Game</button>
                    <button className='btn btn-primary m-2 lr'>Play against the computer</button>
                    <button className='btn btn-secondary' onClick={this.componentDidMount.bind(this)}>Update List</button>

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
                        <th>Number Of Players</th>
                        <th></th>
                    </tr>
                </thead>
                
                    {currentGames.map((game) =>
                    <tbody>
                    <tr>
                        <td>{game.id}</td>
                        <td>{game.created_by}</td>
                        <td>{game.time_date}</td>
                        <td>{game.number_of_players}</td>
                        <td><button key={game.id} className='btn btn-primary m-2 sm'
                                disabled={game.number_of_players === 4}
                                onClick={() => this.joinGame(game.id)}
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
                this.setState({
                    gameId : response.newGame.id,
                    inGame : true
                });
            }
        )
        const socket = io("localhost:5001/", {
            transports: ["websocket"],
            cors: {
              origin: "http://localhost:3000/",
            },
        });
        socket.on("connect", (data) => {
            console.log(data);
        });
        this.setState({socket : socket});
        socket.on("disconnect", (data) => {
            console.log(data);
        });
        return function cleanup() {
            socket.disconnect();
        };
    
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
        const socket = io("localhost:5001/", {
            transports: ["websocket"],
            cors: {
              origin: "http://localhost:3000/",
            },
        });
        socket.on("connect", (data) => {
            console.log(data);
        });
        this.setState({socket : socket});
        socket.on("disconnect", (data) => {
            console.log(data);
        });
        return function cleanup() {
            socket.disconnect();
        };
    
    }
}
 
export default Lobby;
