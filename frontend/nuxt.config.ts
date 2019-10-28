import { Configuration } from "@nuxt/types"
import { config as dConfig } from "dotenv"

dConfig()

const config: Configuration = {
  mode: "spa",
  head: {
    title: "tknk_Scanner",
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      {
        hid: "description",
        name: "description",
        content: "tknk_scanner is community-based integrated malware identification system",
      },
    ],
    link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
  },
  css: ["@fortawesome/fontawesome-svg-core/styles.css"],
  /*
   ** Customize the progress bar color
   */
  loading: { color: "#3B8070" },
  /*
   ** Build configuration
   */
  build: {
    transpile: [/nuxt-typed-vuex/],
    /*
     ** Run ESLint on save
     */
    extend(config, { isDev, isClient }) {
      if (isDev && isClient) {
        if (!config.module) return
        config.module.rules.push({
          enforce: "pre",
          test: /\.(js|vue)$/,
          loader: "eslint-loader",
          exclude: /(node_modules)/,
          options: {
            fix: true,
          },
        })
      }
    },
  },
  buildModules: ["@nuxt/typescript-build", "nuxt-typed-vuex"],
  typescript: {
    typeCheck: true,
    ignoreNotFoundWarnings: true,
  },
  modules: ["@nuxtjs/axios", "bootstrap-vue/nuxt", "@nuxtjs/proxy"],
  plugins: ["~plugins/vue-clipboard2", "~plugins/fontawesome", "@/plugins/composition-api"],
  axios: {
    baseURL: "/api",
  },
  proxy: {
    "/api/": {
      target: process.env.TKNK_DEVELOP_URL,
      auth: process.env.TKNK_DEVELOP_AUTH,
    },
  },
}

export default config
