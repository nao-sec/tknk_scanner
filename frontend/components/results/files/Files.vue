<template>
  <b-table :items="report.scans" v-if="report.scans.length !== 0" :fields="headers" class="dropped-file-table">
    <template slot="detect_rules" slot-scope="data" class="detect-rules">
      <div class="badges">
        <template v-if="data.item.detect_rule.length !== 0">
          <yara variant="danger" v-for="(l, k) in data.item.detect_rule" :key="k" :yara="l" />
        </template>
        <b-badge variant="secondary" v-if="data.item.detect_rule.length === 0">No rule detects</b-badge>
      </div>
    </template>
  </b-table>
  <div class="no-dropped" v-else>
    <p>No file dropped.</p>
  </div>
</template>

<script>
  import { mapState } from 'vuex'
  import Yara from '~/components/Yara'

  export default {
    name: "Files",
    components: {
      Yara
    },
    computed: {
      headers() {
        return [
          {
            key: 'file_name',
            label: 'File Name'
          },
          {
            key: 'size',
            label: 'Size'
          },
          {
            key: 'detect_rules',
            label: 'Detect Rule'
          },
        ]
      },
      ... mapState([ 'report' ])
    }
  }
</script>

<style lang="stylus">
  .dropped-file-table
    td
      border-top 1px solid gray
</style>
