<template>
    <div class="pageContent" id="word-content">
      <label id="page-words">asdfasdfasdfasdafsdfasdfasdfasdfasdfasdf</label>
    </div>
</template>

<script>
    import * as d3 from 'd3'
    export default {
        name: 'hello',
        data () {
            return {
                msg: 'Welcome to Your Vue.js App'
            }
        },
        // 利用d3的 transtion 控制label的定时（根据宽度定时间）移动
        // 完全不显示之后回来重新开始移动  easy
        mounted(){

          let content = document.getElementById('word-content')
          let sw = content.offsetWidth
          console.log('=====>',content)
          let wd = document.getElementById('page-words')
          console.log('--------->>',sw,wd.offsetWidth)
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .pageContent {
      background: #fff;
        width: 100%;
        overflow: hidden;
    }
</style>
