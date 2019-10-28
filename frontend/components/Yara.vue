<template>
  <div>
    <b-badge variant="danger" to="#" @click="show_detail">
      {{ yara }}
    </b-badge>
    <b-modal ref="ruleDetail" class="detail" size="lg" hide-footer :title="yara">
      <template slot="modal-title" slot-scope="data">
        <span class="title">{{ data.value }}</span>
      </template>
      <pre v-if="rule !== null" class="d-block rule">{{ rule }}</pre>
      <div v-else class="b-block text-center">
        <i class="fas fa-spinner fa-spin fa-5x" />
      </div>
      <b-btn class="mt-3" variant="outline-danger" block @click="hide_detail">
        Close
      </b-btn>
    </b-modal>
  </div>
</template>

<script>
export default {
  name: "Yara",
  props: ["yara"],
  data() {
    return {
      rule: null,
    }
  },
  methods: {
    show_detail() {
      this.fetch_rule()
      this.$refs.ruleDetail.show()
    },
    hide_detail() {
      this.$refs.ruleDetail.hide()
    },
    fetch_rule() {
      this.$axios
        .get(`/yara/${this.yara}`, { progress: false })
        .then(res => {
          this.rule = res.data.rule
        })
        .catch(e => {
          console.log(`Fetching rule error: ${e}`)
          this.rule = "Rule Not Found"
        })
    },
  },
}
</script>

<style lang="stylus" scoped>
span
  margin 0 0.5em 0 0
.title
  word-break break-all
.detail
  color black
.rule
  max-height 40vh
  font-size 10px
</style>
