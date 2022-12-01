import React, { Component } from 'react';
import SignUp from './signUp';
import {Lobby} from './lobby';

class Login extends Component {
    state = { 
        user : null,
        password: null,
        isLogin : false,
        isSignUpPressed : false,
        msg : ""
     } 
    render() { 
        const {msg, isLogin, isSignUpPressed} = this.state;
        if(isLogin){
            return(
                <Lobby value={this.state.user}/>
            )
        }
        if(isSignUpPressed){
            return(
                <SignUp onDelete={() => this.setState({
                    isSignUpPressed : !isSignUpPressed,
                    msg : "SignUp Successfuly"
                    })}></SignUp>
            )
        }
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
                    <div className='input-form'>
                    <input 
                    className="form__input" type="password"
                    placeholder='Password'
                    onChange={(event) =>{
                        this.setState({password: event.target.value})
                    }}
                    ></input>
                   
                    </div>

                    <button className='btn btn-dark mr-2'  onClick={this.confimUserData.bind(this)} disabled={isLogin}>Login</button>
                   
                    <button className='btn btn-dark mr-2' onClick={() => this.setState({isSignUpPressed : !isSignUpPressed})}>Sign Up</button>
                        <h6>{msg}</h6>
                    
                </div>
            </div>
        
        );
    }
    confimUserData(){
        fetch('/login',{ 
            'method' : 'POST',
            headers : {
                'Content-Type':'application/json'
            },
            body : JSON.stringify({
                username : this.state.user,
                password : this.state.password
            })
            }
        ).then( response => response.json())
        .catch(error => console.log(error))
        .then(
            (response) => {
                console.log(response);
                if(!response.isValidUser){
                    this.setState({
                        msg : "login failed check your username or password"
                    })
                }else{
                    this.setState({
                        isLogin : response.isValidUser,
                        msg : "Login Successfuly"
                    })
                }
            }
        )
    }    
}
 
export default Login;