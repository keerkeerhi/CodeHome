<template>
    <div class="pageContent">
      <scrollcom></scrollcom>
    </div>
</template>

<script>
  import Scrollcom from './commen/Scrollcom.vue'

    export default {
        name: 'hello',
        components: {Scrollcom},
        data () {
            return {
                msg: 'Welcome to Your Vue.js App'
            }
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .pageContent {
        background: rgb(28, 36, 56);
    }
</style>
