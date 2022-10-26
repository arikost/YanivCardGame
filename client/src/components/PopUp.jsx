import React from "react";
import './popup.css'
function PopUp(props){
  
  return (props.trigger) ? (
    <div className="popup" >
      <div className="popup-inner" >
        {props.children}
        <button className="btn btn-success m-2 lr-btn" onClick={props.onChange}>next</button>
      </div>
    </div>
  ) : "";
}
export default PopUp

