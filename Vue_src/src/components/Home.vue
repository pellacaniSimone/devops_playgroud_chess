<template>
    <title>Home</title>
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
        
                    <form class="d-flex">
                            <a href="http://sonardom.ddns.net:12110/logout"><button 
                                class="btn btn-outline-primary space-right" 
                                type="button"
                            >Logout</button></a>
                    </form>
                </div>
    </nav>

    <div class="screen-center">
                <router-link to="/gioca" class="button-24" role="button">
                    Classico
                </router-link >
            <br>
            <br>
                <router-link to="/UniMoreChess" class="button-24" role="button">
                    UniMOREchess
                </router-link >
            <br>
            <br>    
                <router-link to="/crazyHouse" class="button-24" role="button">
                    Crazy House
                </router-link >
            <br>
            <br>    
                <router-link to="/quadriglia" class="button-24" role="button">
                    Quadriglia
                </router-link >         
            </div>

            

</template>

<script>

import axios from "axios"
import 'bootstrap/dist/css/bootstrap.css'
//import UserData from "./UserData.vue"
const path = "http://sonardom.ddns.net:12110/";
export default {
    name: "HomePage",
    mounted() {
            axios.get(path+"utente").then((response) => {
            localStorage.id_user = response.data.id_user;
            localStorage.username = response.data.username;
            console.log(response.data)
            console.log(localStorage.id_user)
            console.log(localStorage.username)
            })
        }
    }
    
</script>


<style>
    .screen-center{
            text-align: center;
            margin-top: 5%;
        }
    .registration-button{
        margin-right: 2%;
    }
    .button-24 {
        background: #FF4742;
        border: 1px solid #FF4742;
        border-radius: 5%;
        box-shadow: rgba(0, 0, 0, 0.1) 2% 4% 8%;
        box-sizing: border-box;
        color: #FFFFFF;
        cursor: pointer;
        display: inline-block;
        font-family: nunito,roboto,proxima-nova,"proxima nova",sans-serif;
        font-size: 300%;
        font-weight: 800;
        line-height: 20%;
        min-height: 40px;
        outline: 0;
        padding: 3% 10%;
        text-align: center;
        text-decoration: none;
        text-rendering: geometricprecision;
        text-transform: none;
        user-select: none;
        -webkit-user-select: none;
        touch-action: manipulation;
        vertical-align: middle;
    }
    .button-24:hover,
    .button-24:active {
    background-color: initial;
    background-position: 0 0;
    color: #FF4742;
    }
    .button-24:active {
    opacity: .5;
    }

    </style>

