import {baseURL} from '../components/common/globaldata'
import axios from 'axios'
import {getParams} from '../components/common/Util'

// 查询市场列表 用来查询市场中的菠萝列表，包括类型、筛选、排序、分页等，目前仅支持类型中的所有，其余暂不支持。
const query_market = baseURL + 'query_market/'

export default {
  query_market(params) {
    // let formdata = new FormData();
    // formdata.append('wallet',this.userInfo.wallet);
    // formdata.append('email',this.userInfo.email);
    // formdata.append('nickname',this.userInfo.nickname);
    // formdata.append('avatar',this.userInfo.avatar)
    // axios.post(saveData,formdata)
    return new Promise((resolve, reject) => {
      axios.get(query_market + getParams(params)).then(res => {
        resolve(res.data)
      })
    })
  }
}
