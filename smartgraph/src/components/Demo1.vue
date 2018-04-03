<template>
    <section>
      <svg width="300px" height="300px" xmlns="http://www.w3.org/2000/svg">
        <g transform="translate(10,110) scale(1,-1)" >
          <line x1="0" y1="0" x2="0" y2="110" style="stroke: gray;"/>
          <line x1="0" y1="0" x2="100" y2="0" style="stroke: gray;"/>
          <line x1="30" y1="0" x2="30" y2="110" style="stroke: red;"/>
          <line x1="0" y1="20" x2="100" y2="20" style="stroke: red;"/>
          <rect x="10" y="10" width="30" height="60" fill-opacity="0.2"
                style="fill: black;"/>
        </g>
        <!--<rect x="0" y="0" height="30" width="60"-->
              <!--transform="translate(30, 20) scale(3)"-->
              <!--style="fill: gray;"/>-->


      </svg>
    </section>
</template>

<script>
    export default {
        name: "demo1",
      created(){
          console.log('===============>>>',SVGAnimatedLength)
          console.log(SVGLength.SVG_LENGTHTYPE_EMS)
      }
    }
</script>
