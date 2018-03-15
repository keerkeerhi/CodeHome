const Domain = {
  location: window.location,
  href: window.location.href,
  protocol: window.location.protocol,
  host: window.location.host,
  hostname: window.location.hostname,
  port: window.location.port,
  search: window.location.search,
  hash: window.location.hash
}

let baseURL

// 配置开发环境和线上生产环境的切换
if (process.env.NODE_ENV === 'development') {
  baseURL = '/api/'
} else if (process.env.NODE_ENV === 'production') {
  baseURL = '/api/'
}

export {Domain, baseURL}
