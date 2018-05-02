import {base_url} from './baseconfig.js'
const upload_img = base_url + 'api/upload_img/';

module.exports = {
  upload_img(img,openid){
    return new Promise((resolve, reject)=>{
      wx.uploadFile({
        url: upload_img,
        filePath: img,
        name: 'image',
        formData: {openid},
        success: function (result) {
          
        },
        fail(e) {
          wx.showToast({
            title: "服务器超时",
            icon: "none"
          })
        }
      })
    })
  }
} 