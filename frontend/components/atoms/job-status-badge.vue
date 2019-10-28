<template>
  <div class="status">
    <font-awesome-icon :icon="statusIcon" :class="statusClass" :spin="status === 1" size="xs" />
    <nuxt-link v-if="status === 0" :to="{ name: 'results-resultid', params: { resultid: reportId } }">
      Results
    </nuxt-link>
  </div>
</template>

<script lang="ts">
import { computed, createComponent } from "@vue/composition-api"

export default createComponent({
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

  setup({ isSuccess, status, reportId }) {
    const statusIcon = computed(() => {
      if (status === 1) {
        // processing
        return "spinner"
      } else if (status === 0 && isSuccess) {
        // done and scanning success
        return "check-circle"
      } else if (status === 0 && !isSuccess) {
        // done, but fail scanning
        return "times-circle"
      } else {
        // not implemented state
        return "question-circle"
      }
    })

    const statusClass = computed(() => {
      if (status === 0 && isSuccess) {
        // done and scanning success
        return ["success"]
      } else if (status === 0 && !isSuccess) {
        // done, but fail scanning
        return ["fail"]
      } else {
        // not implemented state
        return ["unknown"]
      }
    })

    return {
      statusIcon,
      statusClass,
      reportId,
    }
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
