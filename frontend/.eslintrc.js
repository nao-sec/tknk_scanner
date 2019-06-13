module.exports = {
  root: true,
  env: {
    browser: true,
    node: true
  },
  parserOptions: {
    parser: '@typescript-eslint/parser'
  },
  extends: [
    'plugin:vue/recommended',
    '@nuxtjs',
  ],
  plugins: [
    'vue',
    '@typescript-eslint',
  ],
  rules: {
    '@typescript-eslint/no-unused-vars': 'error',
    'no-console': 0,
    "vue/html-self-closing": ["error", {
      "html": {
        "void": "always",
      }
    }],
  }
};
