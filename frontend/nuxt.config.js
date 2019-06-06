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
      { hid: 'description', name: 'description', content: 'tknk_scanner is community-based integrated malware identification system' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },
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
    extend (config, { isDev, isClient }) {
      if (isDev && isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/
        })
      }
    },
    vendor: ['vue-clipboard2']
  },
  modules: [
    '@nuxtjs/axios',
    'bootstrap-vue/nuxt',
    '@nuxtjs/proxy',
  ],
  plugins: [
    '~/plugins/vue-clipboard2'
  ],
  axios: {
    baseURL: "/api",
  },
  proxy: {
    '/api/': {
      'target': 'https://tknk.svr.pink',
      'auth': 'nao_sec:PntdquE1R2H]W@p5'
    }
    // '/api/': {
    //   'target': 'http://localhost:8000/',
    //   'pathRewrite': {
    //     '^/api': '/'
    //   }
    // }
  },
  css: [
    '@fortawesome/fontawesome-free-webfonts',
    '@fortawesome/fontawesome-free-webfonts/css/fa-brands.css',
    '@fortawesome/fontawesome-free-webfonts/css/fa-regular.css',
    '@fortawesome/fontawesome-free-webfonts/css/fa-solid.css',
  ]
};

