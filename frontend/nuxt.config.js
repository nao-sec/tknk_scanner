module.exports = {
  /*
   ** Headers of the page
   */
  mode: 'spa',
  head: {
    title: 'tknk_Scanner',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content: 'tknk_scanner is community-based integrated malware identification system'
      }
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }]
  },
  css: [
    '@fortawesome/fontawesome-svg-core/styles.css'
  ],
  /*
   ** Customize the progress bar color
   */
  loading: { color: '#3B8070' },
  /*
   ** Build configuration
   */
  build: {
    /*
     ** Run ESLint on save
     */
    extend(config, { isDev, isClient }) {
      if (isDev && isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/,
          options: {
            fix: true
          }
        })
      }
    }
  },
  modules: [
    '@nuxtjs/axios',
    'bootstrap-vue/nuxt',
    '@nuxtjs/proxy'
  ],
  plugins: [
    '~plugins/vue-clipboard2',
    '~plugins/fontawesome'
  ],
  axios: {
    baseURL: '/api'
  },
  proxy: {
    '/api/': {
      target: process.env.TKNK_DEVELOP_URL,
      auth: process.env.TKNK_DEVELOP_AUTH,
      'pathRewrite': {
        '^/api': '/'
      }
    }
  }
}
