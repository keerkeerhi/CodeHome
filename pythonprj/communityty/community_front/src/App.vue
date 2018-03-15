<template>
  <section class="rootDiv">
    <section id="header" class="addShadow">
      <router-link tag="img" to="/Login" class="logo" :src="logo" />
      <router-link tag="img" to="/Home" class="logo" :src="logo" />
    </section>
    <div id="app">
      <router-view :style="{minHeight:cMinH}"/>
    </div>
    <section class="footer">

    </section>
  </section>
</template>

<script>
  import './App.scss'
  import logo from './assets/logo.png'

  export default {
    name: 'App',
    data() {
      return {
        logo,
        cMinH: 'auto'
      }
    },
    methods: {
      clickNav(url) {
        this.$router.push(url)
      }
    },
    created() {
      this.cMinH = document.documentElement.clientHeight - 198 + 'px'
      // window.onresize = ()=>{
      //   this.cMinH = document.documentElement.clientHeight - 198 + 'px'
      // }
    }
  }
</script>
