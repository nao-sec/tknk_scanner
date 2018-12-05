<template>
  <b-row>
    <b-col sm="2" class="status">
      <status :status="report.result.is_success" />
    </b-col>
    <b-col sm="8" offset-sm="2">
      <scan-summary :scan-summary="scan_summary" />
    </b-col>
  </b-row>
</template>

<script>
  import { mapState, mapGetters } from 'vuex'
  import Status from '~/components/results/summary/scan/Status'
  import ScanSummary from '~/components/results/summary/scan/ScanDetail'

  export default {
    name: "Summary",
    components: {
      Status,
      ScanSummary,
    },
    computed: {
      ...mapState([ 'report' ]),
      ... mapGetters({
        'scan_summary': 'report/scan_summary',
      })
    }
  }
</script>

<style lang="stylus" scoped>
  .download-wrapper
    width 100%
    text-align center
</style>
