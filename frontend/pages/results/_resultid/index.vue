<template>
  <div>
    <Message v-if="is_processing" class="progress-message">
      <font-awesome-icon icon="spinner" spin size="10x" />
      <p>Now analyzing ...</p>
    </Message>
    <div v-if="!is_processing">
      <b-container fluid>
        <b-row class="row">
          <b-col>
            <h1>Result</h1>
          </b-col>
        </b-row>
        <scan-summary />
        <b-row class="row">
          <b-col>
            <h2>Submit File</h2>
          </b-col>
        </b-row>
        <file-summary />
        <b-row class="row">
          <b-col>
            <h2>Dump Files</h2>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <files />
          </b-col>
        </b-row>
      </b-container>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue"
import Message from "~/components/ui/Message.vue"
import ScanSummary from "~/components/results/summary/scan/Summary.vue"
import FileSummary from "~/components/results/summary/file/Summary.vue"
import Files from "~/components/results/files/Files.vue"
import { ReportResponse } from "~/types/tknk"

export default Vue.extend({
  name: "ResultIndex",
  components: {
    ScanSummary,
    FileSummary,
    Message,
    Files,
  },
  data() {
    return {
      interval: -1,
      reportResponse: {} as ReportResponse,
      statusCode: -1,
    }
  },
  computed: {
    isProcessing(): boolean {
      return this.reportResponse.status_code === null || this.reportResponse.status_code === 1
    },
  },
  validate({ params }) {
    return /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/.test(params.resultid)
  },
  created() {
    this.fetch_data()
    this.interval = window.setInterval(this.fetch_data, 5000)
  },
  methods: {
    async fetch_data() {
      if (this.reportResponse.status_code === null || this.reportResponse.status_code === 1) {
        const res: ReportResponse = await (this as any).$axios.$get("/result/" + this.$route.params.resultid, { progress: false }).catch(e => {
          clearInterval(this.interval)
          throw (this.$root as any).error(e)
        })
        if (res.status_code !== 1) {
          this.reportResponse = res
          this.statusCode = res.status_code
        }
      } else {
        clearInterval(this.interval)
      }
    },
  },
})
</script>

<style lang="stylus" scoped>
.progress-message
  text-align center
  i
    color #00ff00
.row
  margin-top 1em
</style>

<style lang="stylus">
.table
  td
    border-top none
</style>
