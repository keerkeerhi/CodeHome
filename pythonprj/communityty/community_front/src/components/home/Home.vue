<template>
  <div>
    This is home
  </div>
</template>

<script>
import marketService from '../../service/bolosev'
import {isArray} from "../common/Util"

export default {
  name: 'home',
  data () {
    return {
      dataList: []
    }
  },
  created(){
    // 只支持hot
    marketService.query_market({t_type:'all'}).then(res => {
      if (isArray(res.data))
        this.dataList = res.data
    })
  },
  methods: {
  }
}
</script>

<style lang="scss" scoped>
  @import '../../assets/css/sass-base';

</style>
