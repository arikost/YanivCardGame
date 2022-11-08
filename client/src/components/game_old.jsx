import React, { Component} from 'react';
import PopUp from "./PopUp"; 
import "../App.css";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      items: [],
      selectedItems: [],
      disabledCenterFlag : true,
      pile : [],
      lastThrown : [],
      cardBtnStyle : {backgroundColor:'antiquewhite', borderWidth: 0},
      showPopUp : false,
      popupInnetText : [],
      currentPlyer : 1,
      disabledResetRoundBtn : true,
      disabledRestartGameBtn : true,
      isYaniv : false,
      playersResult : []
    };
  }
togglePop() {
    this.setState({
     showPopUp: !this.state.showPopUp
    });
};
componentDidMount() {
    fetch('/reset_player1_hand')
      .then(res => res.json())
      .then(
        (result) => {
          console.log('res ',result);
          this.setState({
            isLoaded: true,
            items: result.members,
            disabledResetRoundBtn: true,
            disabledRestartGameBtn : true
          });
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
      console.log('mount', this.state.items);
      this.isPasibleYaniv();
  }
render() { 
   
    const { error, isLoaded, items, pile, lastThrown, popupInnetText, playersResult} = this.state;
    if (error) {
        return <div>Error: {error.message}</div>;
      } else if (!isLoaded) {
        return <div>Loading...</div>;
      } else {
        return (
            <React.Fragment>
            <div className='center'>
              <button className='btn btn-primary m-2 lr' id='getCardFromDeckBtn' 
              onClick={this.getCardFromDeck.bind(this)} disabled={this.disabledCenter1()} >get card from deck</button>
              
              {lastThrown.map((item, i) => 
            <button className='btn btn-light m-1' key={i + 10} id={"pileCard"+i} onClick={() => this.pileCardSelcted(i)} 
            style={this.state.cardBtnStyle} disabled={this.disabledCenter2(i)}>
            <img  src={require('../images/'+item + '.png')} alt='' id={"lastThrowenCardImg"+i} width={90} height={120}></img>
            </button>
            )
            }  
            <div>
              {pile.map((item, i) =>
                <img  src={require('../images/'+item + '.png')} key={i + 20} alt='' id={"pilecardImg"} width={60} height={90} style={{margin: "2px"}}></img>
              
              )}
              </div>     
            </div>
            <div className='playerHand'>
            
            <div>
                <button className='btn btn-primary m-2 lr' onClick={this.throwSelectedCards.bind(this)}
                >throw away selected cards</button>
                <button className='btn btn-primary m-2 lr' onClick={this.resetSelectedCards.bind(this)}
                >reset selected cards</button>
                <button className='btn btn-success m-2 lr-btn' disabled={!this.state.isYaniv} onClick = {this.yaniv.bind(this)}>Yaniv</button>
            </div>
            {items.map((item, i) => 
            <button className='btn btn-light m-1' key={i} id={"card"+i} onClick={() => this.cardSelcted(i)} 
            style={this.state.cardBtnStyle} >
            <img key={100 + i} src={require('../images/'+item + '.png')} alt='' id={"cardImg"+i} width={150} height={200}></img>
            </button>
            )}        
          </div>
          {
            
            <PopUp trigger={this.state.showPopUp}  id="popup">
              <div>
                {popupInnetText.map((item, i) =>
                  <h4 key={"line" + i}>{item}</h4>
                )}
              </div>
              <button className="btn btn-success m-2 lr-btn" onClick={this.simulatesPlayers.bind(this)} id="nextBtn"
              disabled={!this.state.disabledResetRoundBtn || !this.state.disabledRestartGameBtn}
              hidden={!this.state.disabledResetRoundBtn || !this.state.disabledRestartGameBtn}>next</button>
              
                {playersResult.map((player, i) =>
                <div className='player-res'>
                  <h5 key={"player"+i} >{"player"+(i+1)+": "}</h5>
                  {player.map((item) =>
                    <img src={require('../images/'+item + '.png')} key={item + i} alt='' id={"playerCardImg"} width={60} height={90} style={{margin: "2px"}}></img>
                  )}
                </div>
                )}
                <div className="d-grid gap-2 d-md-flex justify-content-md-end">
                <button className="btn btn-primary me-md-2" type="butten" id="resetRound" onClick={this.resetRound.bind(this)}
                disabled={this.state.disabledResetRoundBtn} hidden={this.state.disabledResetRoundBtn} >Next Round</button>
                <button className="btn btn-primary" type="butten" id="restartGame" onClick={this.restartGame.bind(this)}
                disabled={this.state.disabledRestartGameBtn} hidden={this.state.disabledRestartGameBtn}>Restart Game</button>
              </div>            </PopUp>
          }
          </React.Fragment>);
    }
}
resetRound(){
  fetch("/reset_round")
  this.componentDidMount();
  this.setState({
    selectedItems: [],
    disabledCenterFlag : true,
    pile : [],
    lastThrown : [],
    showPopUp : false,
    popupInnetText : [],
    currentPlyer : 0,
    disabledResetRoundBtn : true,
    disabledRestartGameBtn : true,
    isYaniv : false,
    playersResult : []
  })
  this.updatePile();
  this.togglePop();
}
restartGame(){
  fetch("/reset_game")
  this.resetRound()
}
yaniv(){
  var playerName = "player"+this.state.currentPlyer;
  var totleScoreBoard = [];
  var game_leader = "";
  var round_winner = "";
  var gameOver = false;
  var text = [];
  fetch('/yaniv',{
    'method': 'POST',
    headers : {
      'Content-Type':'application/json'
    },
    body: JSON.stringify({player: playerName})
  }).then(
    response => response.json()
  ).catch(error => console.log(error))
  
  fetch("/get_score").then(
    res => res.json()
  ).then(
    (result) => {
      console.log("get_score: ",result)
      round_winner = result.round_winner;
      game_leader = result.game_leader;
      totleScoreBoard = [...result.totle_score];
      gameOver = result.game_over;
      text.push(playerName + " called YANIV");
      if(round_winner !== playerName){
        text.push("ASAF!!!!! called by " + round_winner);
      }
      text.push("totle score:");
      text.push("player1: "+totleScoreBoard[0] + "|  player2: "+totleScoreBoard[1] + "|  player3: "+totleScoreBoard[2] + "|  player4: "+totleScoreBoard[3]);
      if(gameOver){
        text.push(game_leader+ " won the game");
        this.setState({disabledRestartGameBtn : false})
      }else{
        this.setState({disabledResetRoundBtn : false})
      }
      this.setState({
        popupInnetText : text,
        showPopUp : true,
        playersResult : [...result.players_cards]
      })

    }
  )
}
isPasibleYaniv(){
  fetch("/is_yaniv").then(
    res => res.json()
  ).then(
    (result) => {
        console.log("is_yaniv", result);
        this.setState({
          isYaniv : result.answer
        })
    }
  )
}
simulatesPlayers(){ 
    fetch('/sim_player'+this.state.currentPlyer).then(
      res => res.json()
    ).then(
      (result) => {
        console.log("sim result", result);
        
        if(result.yaniv){
          this.yaniv()
        }else{
        this.setState({
            lastThrown : [...result.cards_to_throw]
        });
        this.updatePile();
      }
      }
    )
}
disabledCenter1(){
  if(this.state.disabledCenterFlag){
    return true;
  }
  else{
    return false;
  }
}
disabledCenter2(i){
  if( this.state.disabledCenterFlag){
    return true;
  }else{
    if(i === 0 || i === this.state.lastThrown.length -1){return false ;}
    else{return true ;}
  }
}
pileCardSelcted(i){
  this.state.selectedItems.sort((a, b) => a.localeCompare(b));
  fetch('get_card_pile',{
    'method': 'POST',
    headers : {
      'Content-Type':'application/json'
    },
    body: JSON.stringify({card: this.state.lastThrown[i]})
  }).then(
    response => response.json()
  ).catch(error => console.log(error))
  var temp = [...this.state.items];
  temp.push(this.state.lastThrown[i]);
  temp.sort((a, b) => a.localeCompare(b));
  this.setState({
    items : temp,
    lastThrown : [...this.state.selectedItems]
  });
  this.resetSelectedCards();
  this.setState({
    disabledCenterFlag : true,
  });
  this.updatePile();
  this.togglePop();

}
getCardFromDeck(){
  console.log('befor get card', this.state);
  this.state.selectedItems.sort((a, b) => a.localeCompare(b));
  fetch('/get_card_deck').then(
    res => res.json()
  ).then(
    (result) =>{
      var temp = [...this.state.items];
      temp.push(result.card);
      temp.sort((a, b) => a.localeCompare(b));
      this.setState({
        items : temp,
        lastThrown : [...this.state.selectedItems],
      });
      this.resetSelectedCards();
      console.log('after get card', this.state);
    }
  );
  this.setState({
    disabledCenterFlag : true,
  });
  this.updatePile();
  this.togglePop();

}
updatePile(){
  fetch('/get_pile').then(
    res => res.json()
  ).then(
    (result) =>{
      console.log("pile", result);
      if(this.state.currentPlyer !== 4){
        this.setState({
          pile : [...result.cards],
          currentPlyer : (this.state.currentPlyer + 1),
          popupInnetText: ["Press next to simulate player" + (this.state.currentPlyer+1)]
        });
      }else{
        this.setState({
          pile : [...result.cards],
          currentPlyer : 1,
        })
        this.isPasibleYaniv();
        this.togglePop();  
      }
    }
  )
}
throwSelectedCards(){
    //send to server to check if the move is legale
    fetch('check_legal_move',{
      'method': 'POST',
      headers : {
        'Content-Type':'application/json'
      },
      body: JSON.stringify({cards: this.state.selectedItems})
    }).then(
      response => response.json()
    ).catch(error => console.log(error)).then(
      (response) => {
        console.log("get_legalty:",response)
        if(response.legalty){
          var array = [...this.state.selectedItems];
          this.deleteItems(array);
          this.setState({
            disabledCenterFlag : false,
            isYaniv : false
          });
        }
      },
    )
}
deleteItems(items){
  const newItems = this.state.items.filter(c => !(items.includes(c)));
  this.setState({items : newItems});
}
resetSelectedCards(){
    this.setState({selectedItems : []});
    for(var i=0; i< this.state.items.length; i++){
      document.getElementById("card"+i).style.backgroundColor = this.state.cardBtnStyle.backgroundColor;
      document.getElementById("card"+i).style.borderColor = this.state.cardBtnStyle.borderColor;
      document.getElementById("cardImg"+i).width = 150;
      document.getElementById("cardImg"+i).height = 200;
      document.getElementById("cardImg"+i).style.opacity = 1;
    }
    console.log(this.state.selectedItems);
}
cardSelcted(i){
    if( !this.state.selectedItems.includes(this.state.items[i])){
        this.state.selectedItems.push(this.state.items[i]);
        document.getElementById("card"+i).style.backgroundColor = '#A2BABD';
        document.getElementById("cardImg"+i).width = 152;
        document.getElementById("cardImg"+i).height = 204;
        document.getElementById("cardImg"+i).style.opacity = 0.5;
    }
    console.log(this.state.selectedItems);
}
}

export default App;

