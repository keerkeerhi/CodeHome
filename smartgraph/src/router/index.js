import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Home from '../components/Home.vue'
import Demo1 from '@/components/Demo1'
import scroll from '@/components/Scroll'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/Home',
      name: 'Home',
      component: Home
    },
    {
      path: '/Demo1',
      name: 'Demo1',
      component: Demo1
    },
    {
      path: '/scroll',
      name: 'scroll',
      component: scroll
    }
  ]
})
