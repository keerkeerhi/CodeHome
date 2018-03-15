<template>
  <section>
    Login..............
  </section>
</template>

<script>
  export default {
    name: 'Login',
    data() {
      return {
        msg: 'welcome to login'
      }
    },
    created() {

    },
    methods: {

    },
    beforeDestroy() {
      console.log('--------------离开之前销毁定时器')
    },
  }
</script>

<style lang="scss" scoped>
  @import "../../assets/css/sass-base";

</style>
