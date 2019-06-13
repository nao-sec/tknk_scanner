<template>
  <div id="page-container">
    <b-container id="page-content">
      <slot />
    </b-container>
  </div>
</template>

<script>
export default {
  name: 'Page'
}
</script>

<style lang="stylus" scoped>
#page-container
  display flex
  justify-content center
  min-height 100vh
  padding-top 70px
  #page-content
    height calc(100vh - 70px)
    min-width 80vw
    width 80vw
</style>
