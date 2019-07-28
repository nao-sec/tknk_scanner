<template>
  <b-row>
    <b-col sm="2" class="status">
      <status :status="report.result.is_success" />
    </b-col>
    <b-col sm="3">
      <scan-summary :scan-summary="scan_summary" />
    </b-col>
    <b-col sm="4">
      <detects-summary :detects-summary="detects_summary" />
    </b-col>
    <b-col sm="4">
      <file-summary :file-summary="file_summary" />
    </b-col>
  </b-row>
</template>

<script>
import { mapState, mapGetters } from "vuex"
import Status from "~/components/results/summary/Status"
import ScanSummary from "~/components/results/summary/ScanSummary"
import FileSummary from "~/components/results/summary/FileSummary"
import DetectsSummary from "~/components/results/summary/DetectsSummary"

export default {
  name: "Summary",
  components: {
    Status,
    ScanSummary,
    FileSummary,
    DetectsSummary
  },
  computed: {
    ...mapState(["report"]),
    ...mapGetters({
      file_summary: "report/file_summary",
      scan_summary: "report/scan_summary",
      detects_summary: "report/detects_summary"
    })
  }
}
</script>

<style lang="stylus" scoped></style>
