import React, { Component} from 'react';
import PopUp from "./components/PopUp"; 
import "./App.css";

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
      popupInnetText : "",
      currentPlyer : 2,
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
            items: result.members
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
      
  }
render() { 
   
    const { error, isLoaded, items, pile, lastThrown} = this.state;
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
              <div>
              {lastThrown.map((item, i) => 
            <button className='btn btn-light m-1' key={i + 10} id={"pileCard"+i} onClick={() => this.pileCardSelcted(i)} 
            style={this.state.cardBtnStyle} disabled={this.disabledCenter2(i)}>
            <img  src={require('./images/'+item + '.png')} alt='' id={"lastThrowenCardImg"+i} width={90} height={120}></img>
            </button>
            )
            } </div>  
            <div>
              {pile.map((item, i) =>
                <img  src={require('./images/'+item + '.png')} key={i + 20} alt='' id={"pilecardImg"} width={60} height={90} style={{margin: "2px"}}></img>
              
              )}
              </div>     
            </div>
            <div className='playerHand'>
            
            <div>
                <button className='btn btn-primary m-2 lr' onClick={this.throwSelectedCards.bind(this)}
                >throw away selected cards</button>
                <button className='btn btn-primary m-2 lr' onClick={this.resetSelectedCards.bind(this)}
                >reset selected cards</button>
            </div>
            {items.map((item, i) => 
            <button className='btn btn-light m-1' key={i} id={"card"+i} onClick={() => this.cardSelcted(i)} 
            style={this.state.cardBtnStyle} >
            <img  src={require('./images/'+item + '.png')} alt='' id={"cardImg"+i} width={150} height={200}></img>
            </button>
            )}        
          </div>
          {
            
            <PopUp trigger={this.state.showPopUp} onChange={this.simulatesPlayers.bind(this)} id="popup">
              <h3>{this.state.popupInnetText}</h3>

            </PopUp>
          }
          </React.Fragment>);
    }
}
simulatesPlayers(){ 
    fetch('/sim_player'+this.state.currentPlyer).then(
      res => res.json()
    ).then(
      (result) => {
        console.log("sim result", result);
        this.updatePile();
        if(result.yaniv){
          console.log('yaniv');
        }else{
        this.setState({
            lastThrown : [...result.cards_to_throw],
        });
        
      }
      }
    )
    if(this.state.currentPlyer !== 4){
      this.setState({ 
        currentPlyer: this.state.currentPlyer +1,
        popupInnetText : "Press next to simulate player"+this.state.currentPlyer
      });
    }else{
      this.setState({ 
        currentPlyer: 2,
        popupInnetText : "Your Turn To Play"
      });
      this.togglePop();
    }
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
  fetch('get_card_pile',{
    'method': 'POST',
    headers : {
      'Content-Type':'application/json'
    },
    body: JSON.stringify({cards: this.state.lastThrown[i]})
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
    popupInnetText : "Press next to simulate player"+this.state.currentPlyer
  });
  this.updatePile();
  this.togglePop();

}
getCardFromDeck(){
  console.log('befor get card', this.state);

  fetch('/get_card_deck').then(
    res => res.json()
  ).then(
    (result) =>{
      var temp = [...this.state.items];
      temp.push(result.card);
      temp.sort((a, b) => a.localeCompare(b));
      this.setState({
        items : temp,
        lastThrown : [...this.state.selectedItems]
      });
      this.resetSelectedCards();
      console.log('after get card', this.state);
    }
  );
  this.setState({
    disabledCenterFlag : true,
    currentPlyer : 2,
    popupInnetText : "Press next to simulate player"+this.state.currentPlyer
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
      this.setState({
        pile : [...result.cards]
      });
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
    ).catch(error => console.log(error))
    
    fetch('/get_legalty')
      .then(res => res.json())
      .then(
        (result) => {
          if(result.legalty === 'true'){
            var array = [...this.state.selectedItems];
            this.deleteItems(array);
          }
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
      this.setState({
        disabledCenterFlag : false
      });
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

