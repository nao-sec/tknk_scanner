<template>
  <div>
    <i :class="status_icon" />
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
      const templates = ['fas']
      if (this.status === 1) {
        // processing
        return templates.concat(['fa-spinner', 'fa-spin'])
      } else if (this.status === 0 && this.is_success) {
        // done and scanning success
        return templates.concat(['fa-check-circle', 'success'])
      } else if (this.status === 0 && !this.is_success) {
        // done, but fail scanning
        return templates.concat(['fa-times-circle', 'fail'])
      } else {
        // not implemented state
        return templates.concat(['fa-question-circle', 'unknown'])
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
.success
.fail
.unknown
  padding-right 1em
.success
  color #00ff00
.fail
  color #ff3300
</style>
