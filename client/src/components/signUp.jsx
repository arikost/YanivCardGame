import React, { Component } from 'react';
import "../App.css";

class Sginup extends Component {
    state = { 
        user : null,
        password: null,
        passwordConfirmation: null,
     } 
    render() { 
        
        return (
            <div className='sign-up'>
                <div className='sign-up-inner'  action="#" method="post">
                    <h3>Welcom to YANIV Card game</h3>
                    <div className='input-form'>
                    <input 
                    placeholder='User Name'
                    onChange={(event) =>{
                        this.setState({user: event.target.value})
                    }}
                    ></input>
                    </div>
                    <div className={this.getClass()}>
                    <input 
                    className="form_input" type="password"
                    placeholder='Password'
                    onChange={(event) =>{
                        this.setState({password: event.target.value})
                    }}
                    ></input>
                    </div>
                    <div className={this.getClass()}>
                    <input
                    className="form_input" type="password"
                    placeholder='Password Confirmation'
                    
                    onChange={(event) =>{
                        this.setState({passwordConfirmation: event.target.value})
                    }}
                    ></input>
                      </div>
                    <button className='btn btn-dark btn-lg'  onClick={this.confimUserData.bind(this)} 
                    disabled={this.disableBtn()}>Sign Up</button>
                </div>
                <div>
                </div>

            </div>
        );
    }
    confimUserData(){
        fetch("/sign_up", {
            'method' : 'POST',
            headers : {
                'Content-Type':'application/json'
            },
            body : JSON.stringify({
                username : this.state.user,
                password : this.state.password
            })
        });
        this.props.onClick();
    }
    getClass(){
        if(this.state.passwordConfirmation === null){
            return 'input-form';
        }
        else if(this.state.passwordConfirmation === this.state.password ){
            return 'input-form-ok';
        }
        else{
            return 'input-form-bad';
        }
    }
    disableBtn(){
        var s = this.getClass();
        if(s ==='input-form-ok'){
            return false;
        }
        else{ return true;}
    }
}
 
export default Sginup;