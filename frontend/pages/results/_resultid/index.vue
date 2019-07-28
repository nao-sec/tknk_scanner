<template>
  <div>
    <Message v-if="is_processing" class="progress-message">
      <i class="fas fa-spinner fa-spin fa-10x" />
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

<script>
import { mapState } from "vuex"
import Message from "~/components/ui/Message"
import ScanSummary from "~/components/results/summary/scan/Summary"
import FileSummary from "~/components/results/summary/file/Summary"
import Files from "~/components/results/files/Files"

export default {
  name: "ResultIndex",
  components: {
    ScanSummary,
    FileSummary,
    Message,
    Files
  },
  data() {
    return {
      interval: null
    }
  },
  computed: {
    is_processing() {
      return this.report.status_code === 1 || this.report.status_code === null
    },
    ...mapState(["report"])
  },
  validate({ params }) {
    return /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/.test(
      params.resultid
    )
  },
  created() {
    this.fetch_data()
    this.interval = setInterval(this.fetch_data, 5000)
  },
  beforeDestroy() {
    clearInterval(this.interval)
    this.$store.commit("report/destoroy")
  },
  methods: {
    async fetch_data() {
      if (this.report.status_code === null || this.report.status_code === 1) {
        const res = await this.$axios
          .$get("/results/" + this.$route.params.resultid, { progress: false })
          .catch(e => {
            clearInterval(this.interval)
            throw this.$root.error(e)
          })
        if (res.status_code !== 1) {
          this.$store.commit("report/set_result", res)
        }
      } else {
        clearInterval(this.interval)
      }
    }
  }
}
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
