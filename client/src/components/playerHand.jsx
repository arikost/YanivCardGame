import React, { Component} from 'react';


class PlayerHand extends Component {
    constructor(props) {
        super(props);
        this.state = {
          error: null,
          isLoaded: false,
          items: [],
          selectedItems: [],
          disabledCenterFlag : true,
          pile : [],
          cardBtnStyle : {backgroundColor:'#A0A7A8', borderColor: '#A0A7A8'},
        };
      }
    
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
        var left = 400 + 'px';
        var top = 500 + 'px';
        var padding = 50 + 'px';
       
        const { error, isLoaded, items, pile } = this.state;
        if (error) {
            return <div>Error: {error.message}</div>;
          } else if (!isLoaded) {
            return <div>Loading...</div>;
          } else {
            return (
                <React.Fragment>
                <div style={{padding, left : '500px', top:'100px',position:'absolute', alignItems: 'center' }}>
                  <button className='btn btn-primary m-2 lr' id='getCardFromDeckBtn' 
                  onClick={this.getCardFromDeck.bind(this)} disabled={this.disabledCenter1()} >get card from deck</button>
                  <div>
                  {pile.map((item, i) => 
                <button className='btn btn-light m-1' key={i + 5} id={"pileCard"+i} onClick={() => this.pileCardSelcted(i)} 
                style={this.state.cardBtnStyle} disabled={this.disabledCenter2(i)}>
                <img  src={require('../images/'+item + '.png')} alt='' id={"pilecardImg"+i} width={150} height={200}></img>
                </button>
                )
                } </div>       
                </div>
                <div style={{padding, left, top,position:'absolute', alignItems: 'center' 
                ,border: '3px groove #1A6870', borderRadius : '30px', backgroundColor: '#A0A7A8'}}>
                
                <div>
                    <button className='btn btn-primary m-2 lr' onClick={this.throwSelectedCards.bind(this)}>throw away selected cards</button>
                    <button className='btn btn-primary m-2 lr' onClick={this.resetSelectedCards.bind(this)}>reset selected cards</button>
                </div>
                {items.map((item, i) => 
                <button className='btn btn-light m-1' key={i} id={"card"+i} onClick={() => this.cardSelcted(i)} 
                style={this.state.cardBtnStyle}>
                <img  src={require('../images/'+item + '.png')} alt='' id={"cardImg"+i} width={150} height={200}></img>
                </button>
                )}        
              </div>
              </React.Fragment>);
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
        if(i === 0 || i === this.state.pile.length -1){return false ;}
        else{return true ;}
      }
    }
    pileCardSelcted(i){
      fetch('get_card_pile',{
        'method': 'POST',
        headers : {
          'Content-Type':'application/json'
        },
        body: JSON.stringify({cards: this.state.pile[i]})
      }).then(
        response => response.json()
      ).catch(error => console.log(error))
      var temp = [...this.state.items];
      temp.push(this.state.pile[i]);
      temp.sort((a, b) => a.localeCompare(b));
      this.setState({
        items : temp,
        pile : [...this.state.selectedItems]
      });
      this.resetSelectedCards();
      this.setState({
        disabledCenterFlag : true
      });
      
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
            pile : [...this.state.selectedItems]
          });
          this.resetSelectedCards();
          console.log('after get card', this.state);
        }
      );
      this.setState({
        disabledCenterFlag : true
      });

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
 
export default PlayerHand;
