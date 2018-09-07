<template>
  <div id="app-view">
    <Menu/>
    <nuxt/>
  </div>
</template>

<script>
  import Menu from '~/components/Menu.vue'

  export default {
    components: {
      Menu
    }
  }
</script>

<style lang="stylus">
body
  height 100vh
  background-color #1d1d1d
  color white
</style>

<style lang="stylus" scoped>
  #app-view
    height 100vh
</style>
