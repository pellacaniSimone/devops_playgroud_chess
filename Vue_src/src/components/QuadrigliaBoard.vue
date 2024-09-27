<template>
  <nav class="navbar navbar-dark bg-dark navbar-bigger" style="background-color: #ccffcc">
                <div class="container-fluid">
                    <router-link to="/" class="navbar-brand" href="#">
                        <img src="../assets/logo.png" 
                                width="30" 
                                height="30" 
                                class="d-inline-block align-top" 
                                alt="">
                        The Chess
                    </router-link>
                  </div>
  </nav>

    <div class="laterale">

          <!--Chatbox code from Sara-->
          <div id="wrapper">
              <div id="menu">
                  <p class="welcome">Welcome, <b></b></p>
              </div>
              <div id="chatbox">
                <ul v-for="messaggio in messaggi" :key="messaggio">
                  <il>{{messaggio}}</il>
                </ul>
              </div>
              <form name="message" action="" @submit.prevent="sendMessage">
                  <input name="usermsg" type="text" id="usermsg" v-model="messaggio"/>
                  <input name="submitmsg" type="submit" id="submitmsg" value="Send" />
              </form>
          </div>

        <div class="scacchiere" >
            <div :class="[turno]" > 
              <TheChessboard
              @board-created="(api) => (boardAPI = api)"
              @move="handleMove"
              @checkmate="handleCheckmate"
              />
            </div> 
            <div class="separatore"></div>
            <div div :class="[turno2]">
              <TheChessboard
              @board-created="(api) => (boardAPI2 = api)"
              @move="handleMove2"
              @checkmate="handleCheckmate"
              />   
            </div> 
        </div>  
      </div>  
            <h1 > {{ this.user }}</h1>
    <div>
      <select v-model="pezzo.type">
            <option disabled value="">pezzo da selezionare</option>
            <option v-for="(pezzi, index) in pezziCatturati"  :key="index">{{ pezzi }}</option>
        </select>
      <select v-model="selectedLetter">
            <option disabled value="">Please Select</option>
            <option v-for="(caselle, index) in lettereCaselle" :value="index" :key="index">{{ caselle }}</option>
        </select>
        <select v-model="selectedNumber">
            <option disabled value="">Please Select</option>
            <option v-for="(caselle, index) in numeriCaselle" :value="index" v-bind:key="index">{{ caselle }}</option>
        </select>
      </div> 
    
      <button ref="Fen" @click="this.scacchiera1=boardAPI?.getFen()">getFen</button>
      <button ref="mossavuota" @click="this.scacchiera1=boardAPI?.move(this.messaggio)">mossa vuota</button>
      <button ref="calibro" @click="boardAPI?.setPosition(this.scacchiera1)">spero funzioni</button>
      <button ref="orientamento" @click="boardAPI?.toggleOrientation()">orientamento</button>
      <button ref="Fen2" @click="this.scacchiera2=boardAPI2?.getFen()">getFen2</button>
      <button ref="mossavuota2" @click="this.scacchiera2=boardAPI2?.move(this.messaggio)">mossa vuota2</button>
      <button ref="calibro2" @click="boardAPI2?.setPosition(this.scacchiera2)">spero funzioni2</button>
      <button ref="orientamento2" @click="boardAPI2?.toggleOrientation()">orientamento2</button>
      <button ref="inserimento" @click="boardAPI?.putPiece( this.pezzo, this.lettereCaselle[selectedLetter]+this.numeriCaselle[selectedNumber]  )">inserimento</button>
      <button ref="inserimento2" @click="boardAPI2?.putPiece( this.pezzo, this.lettereCaselle[selectedLetter]+this.numeriCaselle[selectedNumber]  )">inserimento2</button>

      <button v-if="this.turno2=='altraSquadra'" class="visibile" ref="scacchiera1Pezzo" @click="inserire">inserimento</button>
      <button v-if="this.turno=='altraSquadra'" class="visibile" ref="scacchiera1Pezzo2" @click="inserire2">inserimento</button>
    

      <div v-if="this.codice.length!=0">
        <h1 >questo è il codice della stanza</h1>
        <h2>{{ this.codice }}</h2>
      </div>
    </template>
    
<script>
    import { TheChessboard } from "vue3-chessboard";
    import "vue3-chessboard/style.css";
    import io from "socket.io-client"
    import axios from "axios"
    import api from "../const"; 
    const socket = io()
   

    import { ref } from 'vue';
    import { Alert } from "bootstrap";
    const boardAPI = ref();
    console.log(boardAPI)
    const boardAPI2 = ref();
    console.log(boardAPI2)

    
    
    export default {
      name: "QuadrigliaBoard",
  
  
      components: {
        TheChessboard,
      },
      data(){
        return{
           scacchiera1 : "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1",
           scacchiera2 : "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1",
           user : 0,
           codice: "",
           isTabClosed: false,                      // se chiusa, nessuna mossa --> nuovo avversario; altrimenti hai vinto
           colore: "w",
           turno: "turnoMio",                       //"turnoMio" | "turnoAltro"
           turno2: "altraSquadra",
           messaggi:[],
           messaggio:"",
           pezzo: {
            color: this.colore,
            type: "",
           },
           mosse:[],
           pezziCatturati:["p"],
           lettereCaselle:{ 0:"a", 1:"b", 2:"c",3:"d",4:"e",5:"f",6:"g",7:"h"},
           numeriCaselle:{0:"1",1:"2",2:"3",3:"4",4:"5",5:"6",6:"7",7:"8"},
           selectedLetter:"",
           selectedNumber:"",
           squadra:true
        }
    
      },
      created(){
        socket.emit("connection");
        socket.emit("connect_quadriglia");
        window.addEventListener("beforeunload", this.leaving);
        socket.on("nero", (data) => {
          this.$refs.orientamento.click();
          this.colore=data
          this.turno= "turnoAltro"
        });
        socket.on("nero2", (data) => {
          console.log(data)
          this.$refs.orientamento2.click();
          this.colore=data
          this.squadra=false
          this.turno= "altraSquadra"
          this.turno2="turnoAltro"
        });
        socket.on("squadra", (data) => {
          console.log(data)
          this.turno= "altraSquadra"
          this.turno2="turnoMio"
        });
    
      },
      beforeUnmount() {
        socket.emit("disconnessione","quadriglia")
      },
      mounted(){
  
       socket.on("conta", (data) => {
          //console.log("sono entrato e quindi un utente in più");
          console.log(data);
          this.user=data;
        });
  
        socket.on("codice", (data) => {
          //console.log("sono entrato e quindi un utente in più");
          
          this.codice=data;
        });
  
        socket.on("scacchiera", (data) => {
          console.log("sono data chissa se funziono");
          console.log(this.scacchiera1);
          this.scacchiera1=data;
          this.$refs.calibro.click();
          if(this.turno=="turnoMio")
            this.turno="turnoAltro"
          else if(this.turno!="altraSquadra")
            this.turno="turnoMio"
        });

        socket.on("scacchiera2", (data) => {
          console.log("ho ricevuto dati sulla seconda scacchiera");
          console.log(this.scacchiera2);
          this.scacchiera2=data;
          this.$refs.calibro2.click();
          if(this.turno2=="turnoMio")
            this.turno2="turnoAltro"
          else if(this.turno2!="altraSquadra")
            this.turno2="turnoMio"
        });
  
      /*  socket.on("abbandono", ()=>{
          let route = this.$router.resolve({name: 'home'});
          window.open(route.href, '_blank');
          //Qui non è molto elegante perché chiude la pagina senza avvisare l'utente
        });*/
  
        socket.on("elencoMosse",(data)=>{
          this.mosse.push(data);
        });
        socket.on("message",(data)=>{
          this.messaggi.push(data);
        });
        socket.on("pezzoPreso",(pezzo, colore)=>{
          if(this.turno!="altraSquadra")  return false
          console.log(colore)
          if(colore==this.colore)
            this.pezziCatturati.push(pezzo);
        });
        socket.on("pezzoPreso2",(pezzo, colore)=>{
          if(this.turno2!="altraSquadra")  return false
          console.log(colore)
          if(colore==this.colore)
            this.pezziCatturati.push(pezzo);
        });
        
    },
      methods: {
        inserire(){ 
            let risposta= "2"
         //   let scacchiera
            if (this.turno=="turnoAltro")
                return false
            else if (this.pezziCatturati.length<1)
                return false 
            else if(this.pezzo.type==null)
                return false    
   /*         if(this.turno=="altraSquadra")  //if fatto per capire la schacchiera da prendere in considerazione 
                scacchiera=this.scacchiera2   
            else
                scacchiera=this.scacchiera1    */
            axios.post(api.backendScacchi+"verificaInserimento", {
              fen: this.scacchiera1,
              colonna: this.selectedLetter,
              riga: this.selectedNumber,  
            })   
            .then(function (response){
              response.data;
              console.log(response.data)  
              if(response.data== true ){
                risposta= true
              }  
              else   
                return false     
              }).finally(()=>{
                if(risposta==true){         
                  this.pezzo.color=this.colore
                 console.log(this.pezzo.type)
                  this.$refs.inserimento.click();
                  this.$refs.Fen.click();
                  const index = this.pezziCatturati.indexOf(this.pezzo.type);
                  this.pezziCatturati.splice(index, 1);
                  this.pezzo.type=null
                  socket.emit("inserire", this.scacchiera1, this.codice);
                }
              }) ;  
              console.log("mi sa che la risposta arriva in ritardo "+risposta)   
 
        },
        inserire2(){ 
          let risposta= "2"
            if (this.turno2=="turnoAltro")
                return false
            else if (this.pezziCatturati.length<1)
                return false 
            else if(this.pezzo.type==null)
                return false    
   /*         if(this.turno=="altraSquadra")  //if fatto per capire la schacchiera da prendere in considerazione 
                scacchiera=this.scacchiera2   
            else
                scacchiera=this.scacchiera1    */
            axios.post(api.backendScacchi+"verificaInserimento", {
              fen: this.scacchiera2,
              colonna: this.selectedLetter,
              riga: this.selectedNumber,  
            })   
            .then(function (response){
              response.data;
              console.log(response.data)  
              if(response.data== true ){
                risposta= true
              }  
              else   
                return false     
              }).finally(()=>{
                if(risposta==true){         
                  this.pezzo.color=this.colore
                 console.log(this.pezzo.type)
                  this.$refs.inserimento2.click();
                  this.$refs.Fen2.click();
                  const index = this.pezziCatturati.indexOf(this.pezzo.type);
                  this.pezziCatturati.splice(index, 1);
                  this.pezzo.type=null
                  socket.emit("inserire2", this.scacchiera2, this.codice);
                }
              }) ;  
              console.log("mi sa che la risposta arriva in ritardo "+risposta)   
 
        },
         handleMove(move) {
          console.log(move);
          this.$refs.Fen.click();
          socket.emit("mossa", this.scacchiera1, move, this.codice);
        },
        handleMove2(move) {
          console.log(move);
          this.$refs.Fen2.click();
          socket.emit("mossa2", this.scacchiera2, move, this.codice);
        },
        sendMessage() {
            if(this.messaggio.length>1){
              socket.emit('message', this.messaggio, this.codice);
              this.messaggio = '';
            }
            else
              return false
          },
        handleCheckmate(isMated) {
          console.log("checkmate per qualcuno")
          if (isMated === 'w') {
            alert('Black wins!');
          } else {
            alert('White wins!');
          }
        },
        leaving(){
        socket.emit("disconnessione","quadriglia")
      }
      },
      watch: {
        isTabClosed(newValue) {
              // This watch will be triggered when the isTabClosed data property changes
              if (newValue) {
                // Add your code here to handle the beforeunload event
                Alert("l'avversario ha abbandonato, scollegati");
              }
            },
        user: function (){
              
  
            }
        }
    
    
      }
    
    
  </script>
    
    <style>
    #app {
      font-family: Avenir, Helvetica, Arial, sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      text-align: center;
    }
    .moveTable {
      width: 100%;
      max-height: 250px;
      overflow: auto;
  }
  
    .laterale{
      display: flex;
      flex-direction: row;
      background-color: #ffffff;
      justify-content:space-between
    }
    .scacchiere{
        display: flex;
        flex-direction: row;
    }
    .turnoMio{
      pointer-events: auto;
    }
    .turnoAltro, .altraSquadra{
      pointer-events: none;
    }
    .listaApi{
      display: flex;
      flex-direction: row;
    }
    button{
      display: none;
    }
    .visibile{
      display:initial;
    }
    .separatore{
      height:100%;
      width:3px;
      border:3px solid #000;
      background:#000;
    }
  
    .scrollarea{
      min-height: 500px;
    }

    * {
    margin: 0;
    padding: 0;
  }
  
  body {
    
    font-family: "Lato";
    font-weight: 300;
  }
  
  form {
    padding: 15px 25px;
    display: flex;
    gap: 10px;
    justify-content: center;
  }
  
  form label {
    font-size: 1.5rem;
    font-weight: bold;
  }
  
  input {
    font-family: "Lato";
  }
  
  a {
    color: #0000ff;
    text-decoration: none;
  }
  
  a:hover {
    text-decoration: underline;
  }
  
  #wrapper,
  #loginform {
    margin: 0 auto;
    padding-bottom: 25px;
    background: #212529;
    width: 300px;
    max-width: 100%;
    border: 2px solid #212121;
    border-radius: 4px;
  }
  
  #loginform {
    padding-top: 18px;
    text-align: center;
  }
  
  #loginform p {
    padding: 15px 25px;
    font-size: 1.4rem;
    font-weight: bold;
  }
  
  #chatbox {
    text-align: left;
    margin: 0 auto;
    margin-bottom: 25px;
    padding: 10px;
    background: #fff;
    height: 200px;
    width: 290px;
    border: 1px solid #a7a7a7;
    overflow: auto;
    border-radius: 4px;
    border-bottom: 4px solid #a7a7a7;
  }
  
  #usermsg {
    flex: 1;
    border-radius: 4px;
    border: 1px solid #000000;
  }
  
  #name {
    border-radius: 4px;
    border: 1px solid #ff9800;
    padding: 2px 8px;
  }
  
  #submitmsg,
  #enter{
    background: #b88c64;
    border: 2px solid #212121;
    color: white;
    padding: 4px 10px;
    font-weight: bold;
    font-family : Arial, Helvetica, sans-serif;
    border-radius: 4px;
  }
  
  .error {
    color: #ff0000;
  }
  
  #menu {
    padding: 15px 25px;
    display: flex;
  }
  
  #menu p.welcome {
    flex: 1;
    font-weight: bold;
    color: white;
  }
  
  a#exit {
    color: white;
    background: #c62828;
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: bold;
  }
  
  .msgln {
    margin: 0 0 5px 0;
  }
  
  .msgln span.left-info {
    color: orangered;
  }
  
  .msgln span.chat-time {
    color: #666;
    font-size: 60%;
    vertical-align: super;
  }
  
  .msgln b.user-name, .msgln b.user-name-left {
    font-weight: bold;
    background: #546e7a;
    color: white;
    padding: 2px 4px;
    font-size: 90%;
    border-radius: 4px;
    margin: 0 5px 0 0;
  }
  
  .msgln b.user-name-left {
    background: orangered;
  }

  .col-sm-6{
    flex: 0 0 auto;
    width: 20%;
  }

  .navbar-bigger{
    max-width: 100%;
  }
</style>
    
