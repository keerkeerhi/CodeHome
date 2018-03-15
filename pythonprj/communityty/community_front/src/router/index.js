import Vue from 'vue'
import Router from 'vue-router'
Vue.use(Router)

// 入口
// const Index = r => require.ensure([], () => r(require('../components/Index')), 'Index')

// 首页
const Home = r => require.ensure([], () => r(require('../components/home/Home')), 'Home')
// 登录
const Login = r => require.ensure([], () => r(require('../components/login/Login')), 'Login')

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/Home'
    },
    {
      path: '/Home',
      name: 'Home',
      component: Home
    },
    {
      path: '/Login',
      name: 'Login',
      component: Login
    }
  ]
})
