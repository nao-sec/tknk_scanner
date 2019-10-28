<template>
  <div class="status">
    <job-status-badge :is-success="state.isSuccess" :status="state.statusCode" :report-id="state.reportID"></job-status-badge>
  </div>
</template>

<script lang="ts">
import { createComponent, onBeforeUnmount, onMounted, reactive } from "@vue/composition-api"
import JobStatusBadge from "~/components/atoms/job-status-badge.vue"

export default createComponent({
  components: {
    JobStatusBadge,
  },
  props: {
    reportId: {
      type: String,
      required: true,
    },
  },
  setup({ reportId }) {
    // data
    const state = reactive({
      paused: false,
      statusCode: -1,
      isSuccess: false,
    })

    // methods
    const fetchResult = async () => {
      const res: ReportResponse | null = await (this as any).$axios.$get(`/result/${reportId}`).catch(() => {
        state.paused = true
      })
      if (res === null || res.report === null) return
      state.statusCode = res.status_code
      state.isSuccess = res.report.meta.is_dumped && res.report.meta.is_matched
    }
    onMounted(() => {
      const loop = () => {
        fetchResult()
        if (!state.paused) {
          window.setTimeout(loop, 9000)
        }
      }
      loop()
    })

    onBeforeUnmount(() => {
      state.paused = true
    })

    return {
      state,
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
