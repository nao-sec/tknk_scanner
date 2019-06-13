<template>
  <div class="status">
    <div v-if="status" class="status-success">
      <i class="fas fa-check-circle fa-10x" />
      <h2>Success!</h2>
    </div>
    <div v-else class="status-fail">
      <i class="fas fa-times-circle fa-10x" />
      <h2>Failed</h2>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Status',
  props: ['status']
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
