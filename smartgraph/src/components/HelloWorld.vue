<template>
  <div class="hello">
    <svg width="150px" height="150px"
         xmlns="http://www.w3.org/2000/svg"
         xmlns:xlink="http://www.w3.org/1999/xlink"
    >
      <defs>
        <!-- 一条线 -->
        <path id="wordPath" d="M 0 75 A 75 75 180 1 0 150 75"/>
      </defs>
      <text font-family="Verdana" font-size="20">
        <textPath xlink:href="#wordPath">
          2018.12.31
        </textPath>
      </text>
    </svg>
  </div>
</template>

<script>
  import * as d3 from 'd3'
  import logo from '../assets/logo.png'
export default {
  name: 'HelloWorld',
  data () {
    return {
      logo,
      msg: 'Welcome to Your Vue.js App',
      data:['a','b','c','d']
    }
  },
  mounted(){
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
svg{
  background: url("../assets/logo.png") no-repeat center;
  transform: rotate(-30deg);
}
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
