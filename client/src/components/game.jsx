import React, { Component } from 'react';
import "../App.css";
import {socket} from "./lobby";

class Game extends Component {
    constructor(props){
        super(props)
        this.state = {
            userName: this.props.value,
            gameId : this.props.id,
            pile : [],
            lastThrown : [],
            showPopUp : false,
            popupInnetText : [],
            currentPlayer : "",
            players: [],
            myCards : [],
            selectsedCards : [],
            cardBtnStyle : {backgroundColor:'antiquewhite', borderWidth: 0},
        }
    }
    componentDidMount(){
        socket.emit('opponent_join', this.state.gameId);
        socket.on("opponent_join", (data) => {
            this.setState({
                players : [...data.opponents]
            })
            if(this.state.players.length === 4){
                fetch('/reset_round', {
                    'method' : 'POST',
                    headers : {
                        'Content-Type':'application/json'
                    },
                    body: JSON.stringify({
                        username: this.state.userName,
                        gameId : this.state.gameId
                    })
                }).then(
                    response => response.json()
                ).catch(error => console.log(error)).then(
                    (response) =>{
                        console.log('cards', response)
                        this.setState({
                            myCards : [...response.cards]                        
                        });
                    }
                )
            }
        });
        socket.on('opponent_leave', (data) =>{
            this.setState({players: this.state.players.filter((player) => {
                return player !== data.player
            })});
        });

    }
    render() { 
        const {userName, players, myCards} = this.state;
        if(players.length < 4){
            return (
                <React.Fragment>
                    <div className='center'>
                        <h2>{"User Name: "+userName}</h2>
                        <button className='btn btn-primary m-2 lr' onClick={this.props.onDelete}>Leave Game</button>
                        <h4>Waiting For Other Players To Join...</h4>
                        <h2>Current Players:</h2>
                        
                        {players.map((opp) => 
                            <h3 key={opp}>{opp+ ' - has joined the game'}</h3>
                        )}
                    </div>
                </React.Fragment>
            );
        }else{
            return(
                <div className='sign-up'>
                    <div className='center'></div>
                    <div className='playerHand'>
                        <div>
                            <button className='btn btn-primary m-2 lr' onClick={this.throwSelectedCards.bind(this)}
                            >throw away selected cards</button>
                            <button className='btn btn-primary m-2 lr' onClick={this.resetSelectedCards.bind(this)}
                            >reset selected cards</button>
                        </div>
                        {myCards.map((item, i) => 
                        <button className='btn btn-light m-1' key={i} id={"card"+i} onClick={() => this.cardSelcted(i)}>
                        <img key={100 + i} src={require('../images/'+item + '.png')} alt='' id={"cardImg"+i} width={150} height={200}></img>
                        </button>
                        )}        
                    </div>
                </div>
            )
        }
    }
    throwSelectedCards(){
        //send to server to check if the move is legale
        fetch('check_legal_move',{
          'method': 'POST',
          headers : {
            'Content-Type':'application/json'
          },
          body: JSON.stringify({
            username : this.state.userName,
            gameId : this.state.gameId,
            cards: this.state.selectsedCards
        })
        }).then(
          response => response.json()
        ).catch(error => console.log(error)).then(
          (response) => {
            //update data if legale
            
          },
        )
    }
    deleteItems(items){
      const newItems = this.state.myCards.filter(c => !(items.includes(c)));
      this.setState({myCards : newItems});
    }
    resetSelectedCards(){
        this.setState({selectsedCards : []});
        for(var i=0; i< this.state.myCards.length; i++){
          document.getElementById("card"+i).style.backgroundColor = this.state.cardBtnStyle.backgroundColor;
          document.getElementById("card"+i).style.borderColor = this.state.cardBtnStyle.borderColor;
          document.getElementById("cardImg"+i).width = 150;
          document.getElementById("cardImg"+i).height = 200;
          document.getElementById("cardImg"+i).style.opacity = 1;
        }
        console.log(this.state.selectsedCards);
    }
    cardSelcted(i){
        if( !this.state.selectsedCards.includes(this.state.myCards[i])){
            this.state.selectsedCards.push(this.state.myCards[i]);
            document.getElementById("card"+i).style.backgroundColor = '#A2BABD';
            document.getElementById("cardImg"+i).width = 152;
            document.getElementById("cardImg"+i).height = 204;
            document.getElementById("cardImg"+i).style.opacity = 0.5;
        }
        console.log(this.state.selectsedCards);
    }
}
 
export default Game;