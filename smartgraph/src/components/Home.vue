<template>
    <div class="pageContent">
      <svg xmlns="http://www.w3.org/2000/svg"
           width="600" height="600" >
        <g id="mysvg">
          <circle cx="300" cy="300"
                  r="300" stroke="black" fill="#FF6600" ></circle>
          <line class="line" v-for="i in number"
                x1="300" y1="300" x2="0" y2="300"
                stroke="black" ></line>
          <!--<animateTransform id="ab" attributeName="transform" attributeType="XML"-->
                            <!--values="0 300 300;360 300 300"-->
                            <!--keySplines="1 0 1 0"-->
                            <!--calcMode="spline"-->
                            <!--type="rotate" begin="0s" dur="3s"-->
                            <!--fill="freeze" />-->
          <!--<animateTransform attributeName="transform" attributeType="XML"-->
                            <!--type="rotate" begin="ab.end" dur="15s"-->
                            <!--from="360 300 300"-->
                            <!--to="2400 300 300"-->
                            <!--fill="freeze" />-->
        </g>
      </svg>
    </div>
</template>

<script>
    import * as d3 from 'd3'
    export default {
        name: 'hello',
        data () {
            return {
                msg: 'Welcome to Your Vue.js App',
                number: 9
            }
        },
        mounted(){
          let svg = d3.select("#mysvg")
          let ar = Array(9).fill('1').map((v,i)=>i)
          svg.selectAll('line').data(ar).attr("transform",(d)=>{
              return "rotate("+d*(360/this.number)+",300,300)"
          })
          // svg.transition()
          //   .duration(3000)
          //   .attrTween("transform", ()=>{
          //     return function(t) {
          //       let rt = 360*t*t
          //       return "rotate("+ rt +", 300, 300)";
          //     }
          //   })
            svg.transition().delay(3000).duration(30000)
            .attrTween("transform", ()=>{
              return function(t) {
                console.log(t)
                let rt = 240*30*t
                // console.log(rt)
                return "rotate("+ rt +", 300, 300)";
              }
            });
//          console.log(svg.transition().duration(3000).attr("width",1000))
//          svg.transition().delay(1000).duration(3000).attr("transform","rotate(" + 359 + ",300,300)")
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .pageContent {
      background: #ccc;
      height:100%;
      color: #FFF;
    }
</style>
