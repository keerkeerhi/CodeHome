<template>
    <section>
      <svg width="300px" height="300px" xmlns="http://www.w3.org/2000/svg">
        <line x1="0" y1="0" x2="0" y2="110" style="stroke: gray;"/>
        <line x1="0" y1="0" x2="100" y2="0" style="stroke: gray;"/>
        <line x1="30" y1="0" x2="30" y2="110" style="stroke: red;"/>
        <line x1="0" y1="20" x2="100" y2="20" style="stroke: red;"/>

        <!--<rect x="0" y="0" height="30" width="60"-->
              <!--transform="translate(30, 20) scale(3)"-->
              <!--style="fill: gray;"/>-->

        <rect x="0" y="0" width="30" height="60" fill-opacity="0.2"
              transform="translate(10,10) scale(0,-1)"
              style="fill: black;"/>
      </svg>
    </section>
</template>

<script>
    export default {
        name: "demo1"
    }
</script>
