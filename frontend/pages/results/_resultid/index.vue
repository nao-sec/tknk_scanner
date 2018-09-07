<template>
<div class="result-container">
  <div class="progress-message" v-if="is_processing">
    <i class="fas fa-spinner fa-spin fa-10x"></i>
    <p>Now analyzing ...</p>
  </div>
  <div class="result-message" v-if="!is_processing">
    <b-container>
      <b-row>
        <b-col>
          <h1>Result</h1>
        </b-col>
      </b-row>
      <b-row>
        <b-col sm="7" class="status">
          <div class="status-success" v-if="is_success">
            <i class="fas fa-check-circle fa-10x"></i>
            <h2>Success!</h2>
          </div>
          <div class="status-fail" v-else>
            <i class="fas fa-times-circle fa-10x"></i>
            <h2>Failed</h2>
          </div>
        </b-col>
        <b-col sm="5">
          <b-table :items="status_summary" class="summary-table" stacked></b-table>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-table :items="dropped_files" class="summary-table">
            <template slot="detect_rule" slot-scope="data">
              <b-badge variant="danger" v-for="(l, k) in data.value" :key="k" class="detect-label">{{ l }}</b-badge>
            </template>
          </b-table>
        </b-col>
      </b-row>
    </b-container>
  </div>
</div>
</template>

<script>
  export default {
    name: "result-index",
    data() {
      return {
        interval: null
      }
    },
    computed: {
      is_processing () {
        return this.$store.state.result.status_code === 1 || this.$store.state.result.status_code === null;
      },
      is_success() {
        return this.$store.state.result.result.is_success;
      },
      status_summary() {
        return [
          { Mode: this.$store.state.result.mode,
            Detail: this.$store.state.result.result.detail,
            "Running Time": this.$store.state.result.run_time,
            Timestamp: this.$store.state.result.timestamp
          }
        ]
      },
      dropped_files() {
        return this.$store.state.result.scans;
      }
    },
    validate({ params }){
      return /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/.test(params.resultid);
    },
    created () {
      this.fetch_data();
      this.interval = setInterval(this.fetch_data, 5000);
    },
    methods: {
      async fetch_data() {
        if (this.$store.state.result.status_code === null || this.$store.state.result.status_code === 1) {
          let res = await this.$axios.$get('/results/' + this.$route.params.resultid).catch(e => {
            clearInterval(this.interval);
          });
          if(res.status_code !== 1) {
            this.$store.commit('result/set_result', res);
          }
        } else {
          clearInterval(this.interval);
        }
      }
    },
    beforeDestroy() {
      clearInterval(this.interval);
      this.$store.commit('result/destoroy')
    },
  }
</script>

<style lang="stylus" scoped>
  .progress-message
    text-align center
    i
      color #00ff00
  .result-container
    height calc(100% - 60px)
    display flex
    justify-content center
    align-items center
  .result-message
    height calc(100% - 60px)
    min-width 80%
    max-width 80%
    .status
      text-align center
      .status-success
        color #00ff00
      .status-fail
        color #ff3300
  .detect-label
    margin 0 0.5em
</style>
<style lang="stylus">
  .table
    td
      border-top none
</style>
