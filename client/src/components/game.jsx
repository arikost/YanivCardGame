import React, { Component } from 'react';
import "../App.css";
import {socket} from "./lobby";

class Game extends Component {
    constructor(props){
        super(props)
        this.state = {
            userName: this.props.value,
            gameId : this.props.id,
            lastThrown : [],
            currentPlayer : "",
            opponents: {
                player2 : "waiting for player to join",
                player3 : "waiting for player to join",
                player4 : "waiting for player to join",
            },
            numberOfPlayers : 0,
            pile : [],
            myCards : [],
            selectsedCards : [],
            cardBtnStyle : {backgroundColor:'antiquewhite', borderWidth: 0},
            throwCardsPressed : true,
            isYaniv : true,
        }
    }
    componentDidMount(){
        socket.on("update_oppenents", (data) => {
            console.log('players', data);
            this.setState({
                numberOfPlayers : data.opponents.length
            });
            this.reArangeOpponentsOrder(data.opponents);
        });
        socket.on('update_center', (data) =>{
            console.log('update_center', data);
            this.setState({
                lastThrown : [...data.last_cards],
                pile : [...data.pile],
                currentPlayer : data.current_player
            });
        })
        socket.on('reset_cards' , (data) => {
            console.log("reset_cards", data);
            this.setState({
                myCards : [...data.cards],
                currentPlayer : data.curr_player
            });
        });
        socket.emit('update_oppenents', this.state.gameId);
    }
    render() { 
        const {userName, 
            opponents, 
            myCards, 
            numberOfPlayers, 
            currentPlayer, 
            lastThrown, 
            pile, 
            throwCardsPressed, 
            isYaniv} = this.state;
        if(numberOfPlayers < 4){
            return (
                <div className='background-game'>
                    <div className='player1'>
                        <h3>{userName}</h3>
                        <button className='btn btn-primary m-2 lr' onClick={this.props.onDelete}>Leave Game</button>
                    </div>
                    <div className='player2'>
                        <h4>{opponents.player2}</h4>
                    </div>
                    <div className='player3'>
                        <h4>{opponents.player3}</h4>
                    </div>
                    <div className='player4'>
                        <h4>{opponents.player4}</h4>
                    </div>
                </div>
            );
        }else{
            return(
                <div className='background-game'>
                    <div className='player2' style={this.getClassPlayer(opponents.player2)}>
                        <h4>{opponents.player2}</h4>
                    </div>
                    <div className='player3' style={this.getClassPlayer(opponents.player3)}>
                        <h4>{opponents.player3}</h4>
                    </div>
                    <div className='player4' style={this.getClassPlayer(opponents.player4)}>
                        <h4>{opponents.player4}</h4>
                    </div>
                    <div className='center'>
                        <button className='get-card-from-deck' onClick={this.getCardFromDeck.bind(this)} disabled={throwCardsPressed}>Deck</button>
                        {lastThrown.map((item, i) => 
                            <button className='btn btn-light m-1' key={i + 10} id={"pileCard"+i}  
                            style={this.state.cardBtnStyle} onClick={() => this.getCardFromTop(item)} 
                            disabled={throwCardsPressed & (i !== 0 || i !== lastThrown.length)}>
                            <img  src={require('../images/'+item + '.png')} alt='' id={"lastThrowenCardImg"+i} width={90} height={120}></img>
                            </button>
                        )}
                        <h5>Discarded cards</h5>
                        <div className='pile'>
                        {pile.map((item, i) =>
                            <img  src={require('../images/'+item + '.png')} key={i + 20} alt='' id={"pilecardImg"} width={60} height={90} style={{margin: "2px"}}></img>
                        )}
                        </div>    
                    </div>
                    <div className='playerHand' >
                        <div>
                            <button className='btn btn-primary m-2 lr' onClick={this.throwSelectedCards.bind(this)}
                            disabled={currentPlayer !== userName}
                            >throw away selected cards</button>
                            <button className='btn btn-primary m-2 lr' onClick={this.resetSelectedCards.bind(this)}
                            disabled={currentPlayer !== userName}
                            >reset selected cards</button>
                            <button className='btn btn-sucess m-2 lr' hidden={isYaniv}>you can call Yaniv!!!</button>
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
    getClassPlayer(player){
        if(player === this.state.currentPlayer){
            return {backgroundColor : 'LightCoral'};
        }
        return {backgroundColor: "lightblue"};
    }
    throwSelectedCards(){
        //send to server to check if the move is legale
        fetch('/check_legal_move',{
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
            if(response.legalety){
                this.deleteItems(this.state.selectsedCards);
                this.setState({throwCardsPressed : false})
            }
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
          document.getElementById("cardImg"+i).width = 150;
          document.getElementById("cardImg"+i).height = 200;
          document.getElementById("cardImg"+i).style.opacity = 1;
        }
    }
    cardSelcted(i){
        if( !this.state.selectsedCards.includes(this.state.myCards[i])){
            this.state.selectsedCards.push(this.state.myCards[i]);
            document.getElementById("card"+i).style.backgroundColor = '#A2BABD';
            document.getElementById("cardImg"+i).width = 152;
            document.getElementById("cardImg"+i).height = 204;
            document.getElementById("cardImg"+i).style.opacity = 0.5;
        }
    }
    getCardFromDeck(){
        fetch('/get_card_deck', {
            'method': 'POST',
          headers : {
            'Content-Type':'application/json'
            },
          body: JSON.stringify({
            username : this.state.userName,
            gameId : this.state.gameId,
            })
        }).then(
            response => response.json()
          ).catch(error => console.log(error)).then(
            (response) =>{
                console.log('get card from deck response:', response);
                var temp = this.state.myCards;
                temp.push(response.card);
                temp.sort((a, b) => a.localeCompare(b));
                this.setState({
                    myCards : temp,
                    throwCardsPressed : true,
                    isYaniv : !response.is_yaniv
                });
                this.resetSelectedCards();
            }
          )
    }
    getCardFromTop(item){
        fetch('/get_card_pile', {
            'method': 'POST',
            headers : {
              'Content-Type':'application/json'
              },
            body: JSON.stringify({
              username : this.state.userName,
              gameId : this.state.gameId,
              card : item
              })  
        }).then(
            response => response.json()
          ).catch(error => console.log(error)).then(
            (response) =>{
                var temp = this.state.myCards;
                temp.push(item);
                temp.sort((a, b) => a.localeCompare(b));
                this.setState({
                    myCards : temp,
                    throwCardsPressed : true,
                    isYaniv : !response.is_yaniv
                });
                this.resetSelectedCards();
            }
          )
    }
    reArangeOpponentsOrder(opp){
        let userIndex = opp.findIndex(p => p === this.state.userName);
        var temp = {
            player2 : 'waiting for player to join',
            player3 : 'waiting for player to join',
            player4 : 'waiting for player to join',
        }
        if(userIndex+1 < opp.length){
            temp.player2 = opp[userIndex+1];
        }
        if(userIndex+2 < opp.length){
            temp.player3 = opp[userIndex+2];
        }
        if(userIndex+3 < opp.length){
            temp.player4 = opp[userIndex+3];
        }
        if(userIndex > 0){
            temp.player4 = opp[userIndex-1];
        }
        if(userIndex-1 > 0){
            temp.player3 = opp[userIndex-2];
        }
        if(userIndex-2 > 0){
            temp.player2 = opp[userIndex-3];
        }
        this.setState({opponents : temp})
    }
}
 
export default Game;