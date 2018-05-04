//logs.js
const util = require('../../utils/util.js')
const app = getApp()
const loginsev = require('../../service/loginsev.js')

Page({
  data: {
    content:''
  },
  onLoad: function () {
    let openid = app.globalData.openid
    loginsev.result_list({openid}).then(res=>{
      console.log('---res=>',res)
      this.setData({content:res.data.content})
    })
  }
})
