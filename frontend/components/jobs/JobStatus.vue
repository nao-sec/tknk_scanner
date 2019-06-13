<template>
  <div class="status">
    <font-awesome-icon :icon="status_icon" :class="status_class" :spin="status === 1" size="xs" />
    <nuxt-link v-if="status === 0" :to="{ name: 'results-resultid', params: { resultid: id } }">
      Results
    </nuxt-link>
  </div>
</template>

<script>
export default {
  name: 'JobStatus',
  props: ['id'],
  data() {
    return {
      status: null,
      is_success: false,
      paused: false
    }
  },
  computed: {
    status_icon() {
      if (this.status === 1) {
        // processing
        return 'spinner'
      } else if (this.status === 0 && this.is_success) {
        // done and scanning success
        return 'check-circle'
      } else if (this.status === 0 && !this.is_success) {
        // done, but fail scanning
        return 'times-circle'
      } else {
        // not implemented state
        return 'question-circle'
      }
    },
    status_class() {
      if (this.status === 0 && this.is_success) {
        // done and scanning success
        return ['success']
      } else if (this.status === 0 && !this.is_success) {
        // done, but fail scanning
        return ['fail']
      } else {
        // not implemented state
        return ['unknown']
      }
    }
  },
  mounted() {
    this.next_tick()
  },
  methods: {
    fetch_result() {
      this.$axios
        .get(`/results/${this.id}`, { progress: false })
        .then((res) => {
          this.status = res.data.status_code
          if (res.data.status_code === 0) {
            this.is_success = res.data.report.result.is_success
          }
        })
        .catch((e) => {
          console.error(`Fetching result error: ${e}`)
          this.paused = true
        })
    },
    next_tick() {
      this.fetch_result()
      if ((this.status === null || this.status !== 0) && !this.paused) {
        setTimeout(this.next_tick, 9000)
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
.status
  height 1em
.success
  color #00ff00
.fail
  color #ff3300
</style>
