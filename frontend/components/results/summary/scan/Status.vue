<template>
  <div class="status">
    <div class="status-success" v-if="status">
      <i class="fas fa-check-circle fa-10x"></i>
      <h2>Success!</h2>
    </div>
    <div class="status-fail" v-else>
      <i class="fas fa-times-circle fa-10x"></i>
      <h2>Failed</h2>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Status",
    props: [
      'status'
    ]
  }
</script>

<style lang="stylus" scoped>
  .status
    text-align center
    .status-success
      color #00ff00
    .status-fail
      color #ff3300
</style>
