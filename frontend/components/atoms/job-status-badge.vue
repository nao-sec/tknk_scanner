<template>
  <div class="status">
    <font-awesome-icon :icon="statusIcon" :class="statusClass" :spin="status === 1" size="xs" />
    <nuxt-link v-if="status === 0" :to="{ name: 'results-resultid', params: { resultid: reportId } }">
      Results
    </nuxt-link>
  </div>
</template>

<script lang="ts">
import Vue from "vue"

export default Vue.extend({
  name: "JobStatusBadge",
  props: {
    isSuccess: {
      type: Boolean,
      required: true,
    },
    status: {
      type: Number,
      required: true,
    },
    reportId: {
      type: String,
      required: true,
    },
  },

  computed: {
    statusIcon() {
      if (this.status === 1) {
        // processing
        return "spinner"
      } else if (this.status === 0 && this.isSuccess) {
        // done and scanning success
        return "check-circle"
      } else if (this.status === 0 && !this.isSuccess) {
        // done, but fail scanning
        return "times-circle"
      } else {
        // not implemented state
        return "question-circle"
      }
    },

    statusClass() {
      if (this.status === 0 && this.isSuccess) {
        // done and scanning success
        return ["success"]
      } else if (this.status === 0 && !this.isSuccess) {
        // done, but fail scanning
        return ["fail"]
      } else {
        // not implemented state
        return ["unknown"]
      }
    },
  },
})
</script>

<style lang="stylus" scoped>
.status
  height 1em
.success
  color #00ff00
.fail
  color #ff3300
</style>
