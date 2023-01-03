import React, { Component } from 'react';
import './popup.css'
class PopUp extends Component {
  constructor(props){
    super(props)
    this.state = {
      playersNames : this.props.value.players_names,
      playersHand : this.props.value.plyers_hands,
      playersScore : this.props.value.players_score,
      playersTotleScore : this.props.value.players_totle_score,
      playerCalled : this.props.value.how_called,
      playerWon : this.props.value.round_winner,
      gameLeader : this.props.value.game_leader,
      isGameOver : this.props.value.is_game_over,
    }

  }
  componentDidMount(){
    console.log("popup", this.state);
  }
  render() {
    const {playerCalled, playersHand, playersScore, playersTotleScore, gameLeader, playersNames, playerWon} = this.state; 
    return (
      <div className='popup'>
        <div className='popup-inner'>
          <p>{playerCalled + " calles yaniv"}</p>
          <p>{this.isAsaf()}</p>
          <p>{playerWon + " won this round"}</p>
          <p>{gameLeader + " is leading the score"}</p>
        <style>{`
          table, th, td{
          border-bottom: 1px solid #ddd;
          padding: 15px;
          text-align: left;
          }
        `}</style>
          <table>
            <thead>
              <tr>
                <th></th>
                <th>{playersNames[0]}</th>
                <th>{playersNames[1]}</th>
                <th>{playersNames[2]}</th>
                <th>{playersNames[3]}</th>
              </tr>
            </thead>
            <tbody key="tbodyPopUp">
              <tr>
                <th>this round score</th>
                <td>{playersScore[0]}</td>
                <td>{playersScore[1]}</td>
                <td>{playersScore[2]}</td>
                <td>{playersScore[3]}</td>
              </tr>
              <tr>
                <th>totle score</th>
                <td>{playersTotleScore[0]}</td>
                <td>{playersTotleScore[1]}</td>
                <td>{playersTotleScore[2]}</td>
                <td>{playersTotleScore[3]}</td>
              </tr>
              <tr>
                <th>players cards</th>
                <td>{playersHand[0].map((item, i) =>
                    <img src={require('../images/'+item + '.png')} 
                    key={item + i} alt='' id={"playerCardImg"} width={60} height={90} 
                    style={{margin: "2px"}}>
                    </img>

                )}</td>
                <td>{playersHand[1].map((item, i) =>
                    <img src={require('../images/'+item + '.png')} 
                    key={item + i} alt='' id={"playerCardImg"} width={60} height={90} 
                    style={{margin: "2px"}}>
                    </img>

                )}</td>
                <td>{playersHand[2].map((item, i) =>
                    <img src={require('../images/'+item + '.png')} 
                    key={item + i} alt='' id={"playerCardImg"} width={60} height={90} 
                    style={{margin: "2px"}}>
                    </img>

                )}</td>
                <td>{playersHand[3].map((item, i) =>
                    <img src={require('../images/'+item + '.png')} 
                    key={item + i} alt='' id={"playerCardImg"} width={60} height={90} 
                    style={{margin: "2px"}}>
                    </img>

                )}</td>
              </tr>
            </tbody>
          </table>
          <button className='btn btn-success m-2 lr' onClick={this.props.onClick}>restart</button>
        </div>
      </div>

    );
  }
  isAsaf(){
    if( this.state.playerCalled !== this.state.playerWon){
      return this.state.playerWon + " called Asaf!!!";
    }
    return "";
  }
}
 
export default PopUp;

