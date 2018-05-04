import {base_url} from './baseconfig.js'
const login_url = base_url + 'api/login/';
const result_list = base_url + 'api/result_list/';

module.exports = {
  login(data){
    return new Promise((resolve, reject)=>{
      // 发送 res.code 到后台换取 openId, sessionKey, unionId
      wx.request({
        url: login_url, //仅为示例，并非真实的接口地址
        data,
        header: {
          'content-type': 'application/json' // 默认值
        },
        success: function (res) {
          resolve(res)
        }
      })
    })
  },
  result_list(data) {
    return new Promise((resolve, reject) => {
      // 发送 res.code 到后台换取 openId, sessionKey, unionId
      wx.request({
        url: result_list+'?openid='+data.openid, //仅为示例，并非真实的接口地址
        header: {
          'content-type': 'application/json' // 默认值
        },
        method: 'GET',
        success: function (res) {
          resolve(res)
        }
      })
    })
  },
} 