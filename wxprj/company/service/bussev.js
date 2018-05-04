import {base_url} from './baseconfig.js'
const upload_img = base_url + 'api/upload/';
const login_ses = base_url + 'api/login_ses/';

module.exports = {
  upload_img(img,openid){
    return new Promise((resolve, reject)=>{
      wx.uploadFile({
        url: upload_img,
        filePath: img,
        name: 'image',
        formData: {openid},
        success: function (result) {
          resolve(result)
        },
        fail(e) {
          reject()
        }
      })
    })
  }
} 