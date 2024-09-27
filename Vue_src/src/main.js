import { createApp } from 'vue'
import App from './App.vue'
import {createRouter, createWebHistory} from 'vue-router'
//import VueSession from 'vue-session'


const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import( './components/Home.vue')
    }, 
    {
        path: '/gioca',
        name: 'TheChessboard',
        component: () => import( './components/ChessBoard.vue')
    },
    {
      path: '/UniMoreChess',
      name: 'chessUniMore',
      component: () => import( './components/ChessUniMore.vue')
  },
  {
    path: '/crazyHouse',
    name: 'CrazyHouse',
    component: () => import( './components/CrazyHouse.vue')

  },
  {
    path: '/quadriglia',
    name: 'QuadrigliaBoard',
    component: () => import( './components/QuadrigliaBoard.vue')

  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})
//App.use(router).mount('#app')
//App.use(VueSession)
createApp(App).use(router).mount('#app')
//createApp(App).use(VueSession) .prototype is undefined