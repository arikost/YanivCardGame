import React, { Component } from 'react';
import "../App.css";
import PopUp from './PopUp';
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
            player1Ready : false,
            player2Ready : false,
            player3Ready : false,
            player4Ready : false,
            pile : [],
            myCards : [],
            selectsedCards : [],
            cardBtnStyle : {backgroundColor:'antiquewhite', borderWidth: 0},
            throwCardsPressed : true,
            isYaniv : true,
            isYanivCalled : false,
            score : {},
        }
    }
    componentDidMount(){
        socket.on("update_oppenents", (data) => {
            console.log('players', data);
            this.reArangeOpponentsOrder(data.opponents);
        });
        socket.on('opponent_ready', (data) =>{
            console.log('opponent_ready', data);
            if(data.opponent === this.state.opponents.player2){
                this.setState({
                    player2Ready : true
                });
            }
            else if(data.opponent === this.state.opponents.player3){
                this.setState({
                    player3Ready : true
                });
            }
            else if(data.opponent === this.state.opponents.player4){
                this.setState({
                    player4Ready : true
                });
            }
        })
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
                currentPlayer : data.curr_player,
                pile : [],
                selectsedCards : [],
                lastThrown : []
            });
        });
        socket.on('yaniv', (data) =>{
            console.log('yaniv:', data);
            this.setState({
                isYanivCalled : true,
                score : data,
            });
        })
        socket.emit('update_oppenents', this.state.gameId);
    }
    render() { 
        const {userName, 
            opponents, 
            myCards, 
            currentPlayer, 
            lastThrown, 
            pile, 
            throwCardsPressed, 
            isYaniv,
            isYanivCalled,
            score,
            player1Ready, 
            player2Ready, 
            player3Ready, 
            player4Ready} = this.state;
        if(!(player1Ready & player2Ready & player3Ready & player4Ready)){
            return (
                <div className='background-game'>
                    <div className='player1'>
                        <h3>{userName}</h3>
                        <button className='btn btn-primary m-2 lr' onClick={this.props.onDelete}>Leave Game</button>
                        <button className='btn btn-success m-2 lr'  onClick={this.readyToRestart.bind(this)}
                        disabled={player1Ready}>Ready</button>
                    </div>
                    <div className='player2'>
                        <h4>{opponents.player2}</h4>
                        <p className={this.getClassPlayerReady(player2Ready)} >Ready</p>
                    </div>
                    <div className='player3'>
                        <h4>{opponents.player3}</h4>
                        <p className={this.getClassPlayerReady(player3Ready)} >Ready</p>
                    </div>
                    <div className='player4'>
                        <h4>{opponents.player4}</h4>
                        <p className={this.getClassPlayerReady(player4Ready)} >Ready</p>
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
                            disabled={throwCardsPressed || (i !== 0 & i !== lastThrown.length-1)}>
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
                            disabled={currentPlayer !== userName & throwCardsPressed}
                            >throw away selected cards</button>
                            <button className='btn btn-primary m-2 lr' onClick={this.resetSelectedCards.bind(this)}
                            disabled={currentPlayer !== userName & throwCardsPressed}
                            >reset selected cards</button>
                            <button className='btn btn-success m-2 lr' 
                            hidden={isYaniv} disabled={currentPlayer !== userName & throwCardsPressed} 
                            onClick={this.yanivClickEvent.bind(this)} >you can call Yaniv!!!</button>
                        </div>
                        {myCards.map((item, i) => 
                        <button className='btn btn-light m-1' key={i} id={"card"+i} onClick={() => this.cardSelcted(i)}  
                        disabled={currentPlayer !== userName & throwCardsPressed}>
                        <img key={100 + i} src={require('../images/'+item + '.png')} alt='' id={"cardImg"+i} width={150} height={200}></img>
                        </button>
                        )}        
                    </div>
                    {isYanivCalled ?  <PopUp  id='pupupId' value={score} onClick={this.readyToRestart.bind(this)}></PopUp>: null}
                </div>
            )
        }
    }
    readyToRestart(){
        fetch('/ready_to_start',{
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
            (response) => {
                socket.emit('update_oppenents', this.state.gameId);
                this.setState({
                    player1Ready : true, 
                    isYanivCalled: false,
                })
            }
          )
    }
    yanivClickEvent(){
        fetch('/yaniv_called',{
            'method': 'POST',
            headers : {
              'Content-Type':'application/json'
            },
            body: JSON.stringify({
              username : this.state.userName,
              gameId : this.state.gameId,
          })
          }).catch(error => console.log(error))
    }
    getClassPlayer(player){
        if(player === this.state.currentPlayer){
            return {backgroundColor : 'LightCoral'};
        }
        return {backgroundColor: "lightblue"};
    }
    getClassPlayerReady(isReady){
        if(isReady){
            return "ready"
        }
        return 'not-ready'
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
                this.resetSelectedCards();
                this.setState({
                    throwCardsPressed : false,

                })
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
          document.getElementById("cardImg"+i).style.width = 150;
          document.getElementById("cardImg"+i).style.height = 200;
          document.getElementById("cardImg"+i).style.opacity = 1;
          document.getElementById("card"+i).style.backgroundColor = '#f8f9fa';
        }
    }
    cardSelcted(i){
        if( !this.state.selectsedCards.includes(this.state.myCards[i])){
            this.state.selectsedCards.push(this.state.myCards[i]);
            document.getElementById("cardImg"+i).style.width = 152;
            document.getElementById("cardImg"+i).style.height = 204;
            document.getElementById("cardImg"+i).style.opacity = 0.5;
            document.getElementById("card"+i).style.backgroundColor = '#F2D4D4';

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