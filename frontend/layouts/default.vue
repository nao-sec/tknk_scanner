<template>
  <div id="app-view">
    <Menu class="menu" />
    <page class="page">
      <nuxt />
    </page>
  </div>
</template>

<script lang="ts">
import { createComponent, onMounted } from "@vue/composition-api"
import Page from "~/components/ui/Page.vue"
import Menu from "~/components/menu/Menu.vue"

export default createComponent({
  components: {
    Menu,
    Page,
  },
  setup(props, { root }) {
    onMounted(async () => {
      await (root as any).$accessor.registerFetchJobsWorker()
    })
  },
})
</script>

<style lang="stylus">
body
  height 100vh
  background-color #1d1d1d
  color white
a
  color #1a88ff
  &:hover
    color #73b6ff
.table
  color white
</style>

<style lang="stylus" scoped>
#app-view
  height 100vh
.menu
  z-index 139
.page
  z-index 3
</style>
