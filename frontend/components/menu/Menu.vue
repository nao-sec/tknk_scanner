<template>
  <b-navbar toggleable="md" type="dark" class="navbar">
    <b-navbar-brand :to="{ name: 'index' }">
      <img src="~/assets/tknk.png" class="d-inline-block align-top" alt="tknk_scanner" />
      tknk_scanner
    </b-navbar-brand>
    <b-navbar-toggle target="nav_collapse" />
    <b-collapse id="nav_collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item :to="{ name: 'index' }" active><font-awesome-icon icon="bug" /> Scan </b-nav-item>
        <b-nav-item :to="{ name: 'page-page', params: { page: 1 } }" active><font-awesome-icon icon="clock" /> Recent </b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav class="ml-auto">
        <search />
        <queue :jobs="jobs" right />
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script lang="ts">
import { computed, createComponent } from "@vue/composition-api"
import Queue from "~/components/menu/queue/Queue.vue"
import Search from "~/components/menu/Search.vue"

export default createComponent({
  name: "Menu",
  components: {
    Queue,
    Search,
  },
  setup() {
    return {
      jobs: computed(() => {
        return (this as any).$accessor.currentJobs
      }),
    }
  },
})
</script>

<style lang="stylus" scoped>
.navbar
  position fixed
  height 60px
  min-width 100%
  background-color #2c2c2c
  border-bottom 1px solid #00ff00
  img
      height 30px
  .navbar-brand
    color #00ff00
</style>
