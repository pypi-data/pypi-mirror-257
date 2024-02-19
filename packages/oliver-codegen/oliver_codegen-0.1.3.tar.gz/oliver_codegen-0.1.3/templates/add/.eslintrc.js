module.exports = {
  // 继承哪些配置
  extends: ['eslint:recommended', 'plugin:prettier/recommended'],
  env: {
    node: true, // 启用node中全局变量
    browser: true // 启用浏览器中全局变量
  },
  // 解析选项
  parserOptions: {
    ecmaVersion: 6, // ES 语法版本
    sourceType: 'module' // ES 模块化
  },
  plugins: ['prettier'],
  // 具体规则
  // "off" 或者 0 关闭这个规则
  // "warn" 或者 1 打开这个规则, 出错报警告
  // "error" 或者 2 开启这个规则, 出错报错误
  rules: {
    'prettier/prettier': ['error', {}, { usePrettierrc: true }],
    'no-var': 'error'
  }
}
