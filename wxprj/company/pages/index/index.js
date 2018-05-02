//index.js
//获取应用实例
const app = getApp()
const bussev = require('../../service/bussev.js')
const loginsev = require('../../service/loginsev.js')

Page({
  data: {
    motto: 'Hello World',
    userInfo: null,
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    imgSrc:""
  },
  //事件处理函数
  bindViewTap: function() {
    console.log('----clickimg')
    wx.navigateTo({
      url: '../words/words'
    })
  },
  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
      this.loginFun()
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        console.log('---->>', res.userInfo)
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
        this.loginFun()
      }
    } else {
      this.checkUser()
    }
  },
  checkUser(){
    // 在没有 open-type=getUserInfo 版本的兼容处理
    wx.getUserInfo({
      success: res => {
        app.globalData.userInfo = res.userInfo
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
        this.loginFun()
      }
    })
  },
  loginFun(){
    // 登录
    wx.login({success: res => {
      let { nickName, country } = this.data.userInfo
      loginsev.login({code:res.code,nickName,country}).then(res=>{
        console.log('====>>resback',res)
      })
    }})
  },
  uploadImg(img){
    console.log('----upload=>',img)
    bussev.upload_img(img,this.openid)
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
  },
  accredit(e) {
    console.log('----->>userInfo', e)
    let errMsg = e.detail.errMsg;
    // 验证成功
    if(errMsg.indexOf('fail') < 0) {
      this.checkUser()
    }
    // 验证失败
    else
    {
      console.log('---->err', errMsg.indexOf('fail'))
    }
  },
})
