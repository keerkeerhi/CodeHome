<template>
  <div id="app">
    <ul>
      <router-link to="/Demo1" tag="li" >
        Demo1
      </router-link>
      <router-link to="/" tag="li" >
        Home
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
  margin-top: 60px;
}
ul{
  display: inline-block;
  list-style: none;
  margin-bottom: 20px;
}
  ul>li{
    float: left;
    cursor: pointer;
    background: green;
    margin: 10px;
  }
</style>
