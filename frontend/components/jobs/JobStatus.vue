<template>
  <div class="status">
    <job-status-badge :is-success="isSuccess" :status="statusCode" :report-id="reportId"></job-status-badge>
  </div>
</template>

<script lang="ts">
import Vue from "vue"
import JobStatusBadge from "~/components/atoms/job-status-badge.vue"
import { ReportResponse } from "~/types/tknk"

export default Vue.extend({
  components: {
    JobStatusBadge,
  },
  props: {
    reportId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      paused: false,
      statusCode: -1,
      isSuccess: false,
    }
  },
  mounted() {
    const loop = () => {
      this.fetchResult()
      if (!this.paused) {
        window.setTimeout(loop, 9000)
      }
    }
    loop()
  },

  beforeDestroy() {
    this.paused = true
  },
  methods: {
    // methods
    async fetchResult() {
      const res: ReportResponse | null = await (this as any).$axios.$get(`/result/${this.reportId}`).catch(() => {
        this.paused = true
      })
      if (res !== null && res.status_code !== undefined) {
        this.statusCode = res.status_code
      }
      if (!(res === null || res.report === undefined || res.report === null)) {
        this.isSuccess = res.report.meta.is_dumped && res.report.meta.is_matched
        this.$emit("job-finish")
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
