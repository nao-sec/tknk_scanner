<template>
  <b-navbar toggleable="md" type="dark" class="navbar">
    <b-navbar-brand :to="{'name': 'index'}">
      <img src="~/assets/tknk.png" class="d-inline-block align-top" alt="BV" />
      tknk_scanner
    </b-navbar-brand>
    <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
    <b-collapse is-nav id="nav_collapse">

      <b-navbar-nav>
        <b-nav-item :to="{'name': 'index'}">Scan</b-nav-item>
      </b-navbar-nav>

    </b-collapse>
  </b-navbar>
</template>

<script>
  export default {
    name: "Menu"
  }
</script>

<style lang="stylus" scoped>
  .navbar
    height 60px
    min-width 100%
    background-color #2c2c2c
    border-bottom 1px solid #00ff00
    img
        height 30px
    .navbar-brand
      color #00ff00
</style>
