/**
 * @type {import('@vue/cli-service').ProjectOptions}
 */
module.exports = {
    publicPath: '',
    devServer: {
      proxy: {
        '^/v1': {
            target: 'http://localhost:1337',
            changeOrigin: true,
            secure:false,
            pathRewrite: {'^/v1': '/v1'},
            logLevel: 'debug' 
        }
      }
    }
  }