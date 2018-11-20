import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {

  constructor(){
    super();
    this.state={
      logueado : false,
      codigoUsuario : "",
      nombreUsuario : "",
      numAsistencias : 0,
      numTardanzas : 0,
      numFaltas : 0,
    }
    this.login = this.login.bind(this);
    this.logout = this.logout.bind(this);
    this.cambiarcodigo = this.cambiarcodigo.bind(this);
    this.fetchUsuario = this.fetchUsuario.bind(this);
  }

  login(){
    this.setState({ logueado : true })
  }

  logout(){
    this.setState({ logueado : false })
  }

  cambiarcodigo(event){
    this.setState({ codigoUsuario : event.target.value })
  }

  fetchUsuario(event){
    console.log(this.state.codigoUsuario);
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
           {this.state.logueado?
               (
                   <div>
                        <h1>HOLA+{this.state.nombreUsuario}</h1>
                        <label>Tienes+{this.state.numAsistencias}+ Asistencias</label>
                        <label>Tienes+{this.state.numTardanzas}+ Tardanzas</label>
                        <label>Tienes+{this.state.numFaltas}+ Faltas</label>
                   </div>
               ):(
                   <div>
                       <label>Insertar tu codigo:</label>
                       <input type="number" value={this.state.codigo} onChange={this.cambiarcodigo}/>
                       <button onClick={this.fetchUsuario}>ENTRAR</button>
                   </div>
               )
           }
        </header>
      </div>
    );
  }
}

export default App;
