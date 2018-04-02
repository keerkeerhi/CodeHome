//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    motto: 'Hello World',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    imgSrc:""
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  },
  uploadImg(img){
    return;
    wx.uploadFile({
      url: '',
      filePath: '',
      name: '',
    })
  },
  chooseImg(){
    let _this = this;
    let count = 1;
    wx.showActionSheet({
      itemList: ['拍照片', '我的相册'],
      success(e) {
        switch (e.tapIndex) {
          case 0: {
            wx.chooseImage({
              count,
              sizeType: ['original'],
              sourceType: ['camera'],
              success: function (res) {
                let imgSrc = res.tempFilePaths[0];
                _this.setData({ imgSrc });
                _this.uploadImg(imgSrc)
              },
            })
          }
            break;
          case 1: {
            wx.chooseImage({
              count,
              sizeType: ['original'],
              success: function (res) {
                let imgSrc = res.tempFilePaths[0];
                _this.setData({ imgSrc });
                _this.uploadImg(imgSrc)
              },
            })
          }
            break;
        }
      },
      fail(e) {
        console.log('--fal=>', e)
      }
    })
  }
})
