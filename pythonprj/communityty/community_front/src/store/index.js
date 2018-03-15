import Vue from 'vue'
import Vuex from 'vuex'
// 光引用不成，还得使用
Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    wallet: 0
  },
  mutations: {
    setWallet(state, wallet) {
      state.wallet = wallet
    }
  }
})

export default store
