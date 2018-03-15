const isArray = function (v) {
  if (!v)
    return false;
  else
    return Object.prototype.toString.apply(v) === '[object Array]';
}

const curFun = function (text, max) {
  if (text && text.length > max)
    return text.substring(0, max) + "...";
  else
    return text;
}

const deepCopy = function (source) {
  var result = {};
  for (var key in source) {
    result[key] = typeof source[key] === 'object' ? deepCopy(source[key]) : source[key];
  }
  return result;
}

const getNullString = function (str) {
  return str ? str : "";
}

function getParams(params) {
  let p = "?";
  for (var par in params)
    p += par + "=" + params[par] + "&";
  // if (p.length == 1)
  //   p = 't=' + fGetRandom();
  // else
  //   p += 't=' + fGetRandom();
  if (p.length>0)
    p = p.substring(0,p.length-1);
  return p;
}

function fGetRandom() {
  return Date.now().toString().substring(8);
}

const getLengthNum = function (str, num) {
  while (str.length < num) {
    str = '0' + str;
  }
  return str;
}

const trim = function (str) {
  return str.replace(/(^\s*)|(\s*$)/g, '');
}

const sendMessage = function (type, data) {
  window.parent.postMessage({type: type, data: data}, '*');
}

const combineToA = function (arr1, arr2) {
  arr2.forEach(it => {
    arr1.push(it);
  })
  return arr1;
}

const combineToB = function (arr1, arr2) {
  arr1.forEach(it => {
    arr2.push(it);
  })
  return arr2;
}

const initTreeVal = function (tree, props, value) {
  tree.forEach(it => {
    it[props] = value;
    if (isArray(it.nodes))
      initTreeVal(it.nodes, props, value);
  })
}

/**
 * 对Date的扩展，将 Date 转化为指定格式的String
 * 月(M)、日(d)、12小时(h)、24小时(H)、分(m)、秒(s)、周(E)、季度(q) 可以用 1-2 个占位符
 * 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字)
 * eg:
 * (new Date()).pattern("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423
 * (new Date()).pattern("yyyy-MM-dd E HH:mm:ss") ==> 2009-03-10 二 20:09:04
 * (new Date()).pattern("yyyy-MM-dd EE hh:mm:ss") ==> 2009-03-10 周二 08:09:04
 * (new Date()).pattern("yyyy-MM-dd EEE hh:mm:ss") ==> 2009-03-10 星期二 08:09:04
 * (new Date()).pattern("yyyy-M-d h:m:s.S") ==> 2006-7-2 8:9:4.18
 */
const dateFormat = function (date, fmt) {
  //author: meizz
  var o = {
    "M+": date.getMonth() + 1,                 //月份
    "d+": date.getDate(),                    //日
    "h+": date.getHours(),                   //小时
    "m+": date.getMinutes(),                 //分
    "s+": date.getSeconds(),                 //秒
    "q+": Math.floor((date.getMonth() + 3) / 3), //季度
    "S": date.getMilliseconds()             //毫秒
  };
  if (/(y+)/.test(fmt))
    fmt = fmt.replace(RegExp.$1, (date.getFullYear() + "").substr(4 - RegExp.$1.length));
  for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt))
      fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
  return fmt;
}
const getDateByMillisecond = function (ms, formate) {
  let d = new Date();
  d.setTime(ms);
  if (!formate)
    return d;
  else
    return dateFormat(d, formate);
}

const stringToDate = function (str) {
  return new Date(Date.parse(str.replace(/-/g, "/")));
}

const isNull = function (obj) {
  if (obj) {
    let res = true;
    for (let i in obj)
      res = false;
    return res;
  }
  return true;
}

const checkObj = function (obj) {
  for (let i in obj) {
    if (obj[i].flag)
      return false;
  }
  return true;
}

const clearNullVal = function (obj) {
  for (let i in obj) {
    if (!obj[i] || String(obj[i]).length == 0)
      delete obj[i];
  }
}

/**
 * 将以base64的图片url数据转换为Blob
 * @param urlData
 *            用url方式表示的base64图片数据
 */
const convertBase64UrlToBlob = function (urlData) {

  var bytes = window.atob(urlData.split(',')[1]);        //去掉url的头，并转换为byte

  //处理异常,将ascii码小于0的转换为大于0
  var ab = new ArrayBuffer(bytes.length);
  var ia = new Uint8Array(ab);
  for (var i = 0; i < bytes.length; i++) {
    ia[i] = bytes.charCodeAt(i);
  }

  return new Blob([ab], {type: 'image/jpg'});
}
//和当前时间做比较
const comp = function (date) {
  let now = new Date;
  let d = new Date(date);
  if (now > d) {
    return 'front'    //"之前的日期"
  } else if (now < d) {
    return 'after'       //"之后的日期";
  } else {
    return 'same'        //"一样的日期";
  }
}


// Generator start -------
const Thunk = function (fn) {
  return function (...args) {
    return function (callback) {
      return fn.call(this, ...args, callback);
    }
  };
};
const run_thunk = function (fn) {
  var gen = fn();

  function next(data) {
    var result = gen.next(data);
    if (result.done) return;
    result.value(next);
  }

  next();
}

// var readFile = Thunk(fs.readFile);
// function* g() {
//   var f1 = yield readFile('fileA');
//   var f2 = yield readFile('fileB');
//   // ...
//   var fn = yield readFile('fileN');
// }
// run_thunk(g);

function run_promise(gen) {
  var g = gen();

  function next(data) {
    var result = g.next(data);
    if (result.done) return result.value;
    result.value.then(function (data) {
      next(data);
    }, function () {
      throw '获取数据超时！';
    });
  }

  next();
}

// var fs = require('fs');

// var readFile = function (fileName){
//   return new Promise(function (resolve, reject){
//     fs.readFile(fileName, function(error, data){
//       if (error) return reject(error);
//       resolve(data);
//     });
//   });
// };

// var gen = function* (){
//   var f1 = yield readFile('/etc/fstab');
//   var f2 = yield readFile('/etc/shells');
//   console.log(f1.toString());
//   console.log(f2.toString());
// };

// run_promise(gen);


// -----------co


// var co = require('co');
// co(gen);
// co(gen).then(function (){
//   console.log('Generator 函数执行完成');
// });

//------------co end

// Generator end -------

var dispatch = function (ele, type) {
  if (document.all) {
    // IE浏览器支持fireEvent方法
    ele.fireEvent('on' + type, evt)
  } else {
    // 其他标准浏览器使用dispatchEvent方法
    var evt = document.createEvent('HTMLEvents');
    // initEvent接受3个参数：
    // 事件类型，是否冒泡，是否阻止浏览器的默认行为
    evt.initEvent(type, true, true);
    ele.dispatchEvent(evt);
  }
};

var cutStr = function (str, len) {
  if (str.length > len)
    return str.substring(0, len) + "...";
  else
    return str;

}

var getUrlParams = function () {
  var url = window.document.location.href.toString();
  var u = url.split("?");
  if (typeof(u[1]) == "string") {
    u = u[1].split("&");
    var get = {};
    for (var i in u) {
      if (isNaN(i))
        continue;
      var j = u[i].split("=");
      get[j[0]] = j[1];
    }
    return get;
  } else {
    return {};
  }
}

var arrIndex = function (list, attr, item) {
  if (!isArray(list))
    return -1;
  for (let i = 0; i < list.length > 0; i++)
    if (list[i][attr] == item[attr])
      return i;
  return -1;
}

var translatSecond = function (count) {
  return formatNumber(Math.floor(count/86400)) + '天 ' + formatNumber(Math.floor(count / 3600)%24) + ':' + formatNumber(Math.floor(count / 60) % 60) + ':' +
    formatNumber(count % 60);
}

var DatetoSecond = function (date){
  if ( typeof date == "string" )
    return Math.round(Date.parse(date)/1000)
  else
    return Math.round(date.getTime()/1000)
}
function formatNumber(num) {
  return num < 10 ? ('0' + num) : String(num);
}

// ---------------------  提示 start
function showWarning(vue, message, title) {
  vue.$Notice.warning({
    title: title,
    desc: message
  });
}
function showSuccess(vue, message, title) {
  vue.$Notice.success({
    title: title,
    desc: message
  });
}
function showInfo(vue, message, title) {
  vue.$Notice.info({
    title: title,
    desc: message
  });
}
function showError(vue, message, title) {
  vue.$Notice.error({
    title: title,
    desc: message
  });
}

function dataURLtoBlob(dataurl) {
  var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
    bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }
  return new Blob([u8arr], {type: mime});
}

function resizeImg(src, width, height, callback) {
  var img = new Image();
  img.width = width;
  img.height = height;
  img.onload = function () {
    let can = document.createElement('canvas');
    let ctx = can.getContext("2d");
    ctx.drawImage(img, 0, 0, img.width, img.height);
    can.width = width;
    can.height = height;
    callback(can.toDataURL("image/png"));
  };
  img.src = src;
}

function arrayIndex(list, val, key) {
  for (var i = 0; i < list.length; i++) {
    if (list[i][key] == val[key])
      return i;
  }
  return -1;
}

function arrayAdd(list, item, key) {
  var index = arrayIndex(list, item, key);
  if (index < 0) {
    list.push(item);
  }
}

function arrayRemove(list, item, key) {
  var index = arrayIndex(list, item, key);
  if (index > -1) {
    list.splice(index, 1);
  }
}

// ------------------------   提示 end
export {
  fGetRandom, resizeImg, dataURLtoBlob,
  showSuccess, showWarning, showInfo, showError,
  translatSecond, arrIndex, getUrlParams, checkObj, clearNullVal,
  dispatch, Thunk, run_thunk, run_promise, isArray, curFun, deepCopy,
  getNullString, getParams, getLengthNum, trim, sendMessage, combineToA,
  combineToB, initTreeVal, dateFormat, isNull, convertBase64UrlToBlob,
  stringToDate, getDateByMillisecond, comp, arrayIndex, arrayAdd, arrayRemove,
  DatetoSecond
}
