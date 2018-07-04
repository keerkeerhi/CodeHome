// pages/words/words.js
const bussev = require('../../service/bussev.js')
Page({

  /**
   * 页面的初始数据
   */
  data: {
    resList: []
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    if (!options.info)
      return
    let {openid,img} = JSON.parse(options.info)
    console.log('params==>', openid,img)
    wx.showLoading({
      title: '识别中',
    })

    bussev.upload_img(img, openid).then(res => {
      let ds = JSON.parse(res.data)
      wx.hideLoading()
      if (ds.words_result.length > 0) {
        this.setData({ resList: ds.words_result})
      }
      else
      {
        wx.navigateBack({
          delta: 1
        })
      }
    }, rej => {
      console.log(rej)
      wx.showToast({
        title: "服务器超时",
        icon: "none"
      })
    })
  },
  copyWords(){
    let words = ''
    this.data.resList.forEach(it=>{
      words = words + it.words +'\r'
    })
    wx.setClipboardData({
      data: words,
      success: function (res) {
        wx.showToast({
          title: '复制成功',
        })
      }
    })
  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
  
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
  
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
  
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
  
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
  
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
  
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
  
  }
})