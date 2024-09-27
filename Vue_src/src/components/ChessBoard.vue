<template>
  <nav class="navbar navbar-dark bg-dark" style="background-color: #ccffcc">
                <div class="container-fluid">
                    <router-link to="/" class="navbar-brand">
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
      <div  :class="[turno]">
        <TheChessboard
          @board-created="(api) => (boardAPI = api)"
          @move="handleMove"
          @checkmate="handleCheckmate"
        />
        <h1 > {{ this.user }}</h1>
      </div>
      <div class="col-xs-12 col-sm-6">
          <div id="secondWindow">
              <h3><span id="status">White to move</span></h3>
              <div id="moveTable">
                  <table class="table table-striped table-condensed" id="pgn">
                      <thead>
                          <tr>
                              <th>#</th>
                              <th>From</th>
                              <th>To</th>
                          </tr>
                      </thead>
                      <tbody>
                        <tr v-for="mossa in mosse" :key="mossa.id">
                          <td>{{mossa.id}}</td>
                          <td>{{mossa.from}}</td>
                          <td>{{mossa.to}}</td>

                        </tr>
                      </tbody>
                  </table>
              </div>
            </div>  
        </div>
  </div>
    <button ref="Fen" @click="this.info=boardAPI?.getFen()">getFen</button>
    <button ref="cambio" @click="visualizza">visualizza</button>
    <button ref="calibro" @click="boardAPI?.setPosition(this.info)">spero funzioni</button>
    <button ref="orientamento" @click="boardAPI?.toggleOrientation()">orientamento</button>
    <div v-if="this.codice.length!=0">
      <h1 >questo è il codice della partita</h1>
      <h2>{{ this.codice }}</h2>
    </div>
  </template>
  
<script>
  import 'bootstrap/dist/css/bootstrap.css'
  import { TheChessboard } from "vue3-chessboard";
  import "vue3-chessboard/style.css";
  import io from "socket.io-client";

  const socket = io()

  import { ref } from 'vue';
  const boardAPI = ref();
  console.log(boardAPI)

  import axios from "axios"
  const path = "http://sonardom.ddns.net:12100/";

  const id_user = localStorage.getItem("id_user")
  const username = localStorage.getItem("username")

  export default {
    name: "ChessBoard",
    components: { 
      TheChessboard,  
    },
    data(){
      return{
         info : "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1",
         user : 0,
         codice: "",
         isTabClosed: false,                      // se chiusa, nessuna mossa --> nuovo avversario; altrimenti hai vinto
         colore: "white",
         turno: "turnoMio",                       //"turnoMio" | "turnoAltro"
         messaggi:[],
         messaggio:" ",
         mosse:[]
      }
  
    },
    created(){
      socket.emit("connection", "normale")
      window.addEventListener("beforeunload", this.leaving);
      socket.on("nero", (data) => {
        this.$refs.orientamento.click();
        this.colore=data
        this.turno= "turnoAltro"
      });
  
    },
    beforeUnmount() {
      alert("vuoi uscire?")
      socket.emit("disconnessione","normale")
    },
    mounted(){
      console.log("inizio debug")
      console.log(localStorage)
      console.log("singoli dati")
      console.log(id_user)
      console.log(username)
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
        console.log(this.info);
        this.info=data;
        this.$refs.calibro.click();
        if(this.turno=="turnoMio")
          this.turno="turnoAltro"
        else
          this.turno="turnoMio"
      });

      socket.on("abbandono", ()=>{
        let route = this.$router.resolve({name: 'home'});
        window.open(route.href, '_blank');
        //Qui non è molto elegante perché chiude la pagina senza avvisare l'utente
      });

      socket.on("elencoMosse",(data)=>{
        this.mosse.push(data);
      });
      socket.on("message",(data)=>{
        this.messaggi.push(data);
      });
      
  },
    methods: {
      aggiorna(){
        this.$refs.Fen.click();
        this.$refs.cambio.click();
        socket.emit("mossa", this.info, this.codice);
        //this.$refs.calibro.click();  
      },
      fine_partita(){
            console.log("entrato");
            console.log(this.mosse.length)
            console.log(this.colore)
            axios.post(path+"fine_partita",{
        Nmosse: this.mosse.length,
        colore: this.colore,
        modalita: "Standard",
        id_user: id_user,
        username: username
            }).then(function (response){
              response.data;
              console.log(response.data)
        })
        },
       handleMove(move) {
        console.log(move);
        this.$refs.Fen.click();
        this.$refs.cambio.click();
        socket.emit("mossa", this.info, move, this.codice);
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
        console.log("perché tu non funzioni?")
        this.fine_partita();
        if (isMated === 'b') {
          alert('white wins!');
        } else {
          alert('black wins!');
        }
      },
      handleCheck(isMated) {
        console.log("checkmate per qualcuno")
       alert(`${isMated} is mated`);
      },
      leaving(){
        socket.emit("disconnessione","normale")
      }
    },
    watch: {
      isTabClosed(newValue) {
            // This watch will be triggered when the isTabClosed data property changes
            if (newValue) {
              // Add your code here to handle the beforeunload event
              socket.emit("disconnessione","normale")
              alert("l'avversario ha abbandonato, scollegati");
            }
          },
        }, 
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

  .col-sm-6{
    flex: 0 0 auto;
    width: 20%;
  }

  .laterale{
    margin: 20px auto;
    display: flex;
    flex-direction: row;
    background-color: #ffffff;
    justify-content:space-between
  }
  .turnoMio{
    pointer-events: auto;
  }
  .turnoAltro{
    pointer-events: none;
  }
  button{
    display: none;
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
    width: 600px;
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
    width: 400px;
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
  
  #exit {
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

</style>
  