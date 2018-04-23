<template>
  <div class="scrollpage" id="word-content">
    <label>{{label}}</label>
  </div>
</template>

<script>
  import * as d3 from 'd3'

  export default {
    name: 'hello',
    props: ['label'],
    data() {
      return {
        msg: 'Welcome to Your Vue.js App',
        wd: null,
        lw: null,
        cw: null,
        timer: 0
      }
    },
    // 利用d3的 transtion 控制label的定时（根据宽度定时间）移动
    // 完全不显示之后回来重新开始移动  easy
    methods: {
      scrollFun(length, time) {
        this.wd.style("left", this.cw + 'px')
        this.wd.transition().ease(d3.easeLinear).duration(time * 1000)
          .styleTween("transform", () => {
            return function (t) {
              let rt = length * t
              return "translateX(-" + rt + "px)";
            }
          })
      },
      beginFun(){
        let content = d3.select("#word-content")
        let wd = content.select('label')
        this.wd = wd
        let cWidth = content._groups[0][0].offsetWidth
        let lWidth = wd._groups[0][0].offsetWidth
        this.lw = lWidth
        this.cw = cWidth
        let v = 100
        let time = (lWidth + 20) / v
        let tim2 = (lWidth + cWidth + 20) / v
        console.log('-----lWidth',lWidth,cWidth)
        if (lWidth > cWidth) {
          wd.style("left", 0)
          let ve = this
          wd.transition().ease(d3.easeLinear).duration(time * 1000)
            .styleTween("transform", () => {
              return function (t) {
                let rt = (lWidth + 20) * t
                if (t == 1) {
                  ve.scrollFun(lWidth + cWidth + 20, tim2)
                  ve.timer = setInterval(() => {
                    ve.scrollFun(lWidth + cWidth + 20, tim2)
                  }, tim2 * 1000)
                }
                return "translateX(-" + rt + "px)";
              }
            })
        }
        else
          wd.style("left", (cWidth - lWidth) / 2 + 'px')
      }
    },
    watch: {
      label(val) {
        if (val) {
          clearInterval(this.timer)
          this.$nextTick(() => {
            this.beginFun()
          })
        }
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .scrollpage {
    background: none;
    width: 100%;
    height: 60px;
    overflow: hidden;
    position: relative;
    text-align: center;
  }

  .scrollpage > label {
    /*background: none;*/
    height: 60px;
    line-height: 60px;
    position: absolute;
    white-space: nowrap;
  }
</style>
