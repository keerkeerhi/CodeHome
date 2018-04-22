<template>
  <div id="app">
    <ul>
      <router-link to="/Home" tag="li" >Home</router-link>
      <router-link to="/Demo1" tag="li" >
        Demo1
      </router-link>
      <router-link to="/" tag="li" >
        Home
      </router-link>
      <router-link to="/scroll" tag="li" >
        Scroll
      </router-link>
    </ul>
    <router-view style="background: #F3F3F3;" />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height:100%;
}
  ul{
    list-style: none;
    height: 40px;
    line-height:40px;
  }
  ul>li{
    cursor: pointer;
    width: 200px;
    float: left;
  }
  html,body{
    margin:0;
    padding: 0;
    height: 100%;
  }
</style>
