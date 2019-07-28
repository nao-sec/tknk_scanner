<template>
  <div class="message-container">
    <div id="message-content">
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  name: "Message",
}
</script>

<style lang="stylus" scoped>
.message-container
  display flex
  justify-content center
  align-items center
  min-height calc(100vh - 60px)
</style>
