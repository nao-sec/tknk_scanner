<template>
  <b-table
    v-if="report.scans.length !== 0"
    :items="report.scans"
    :fields="headers"
    class="dropped-file-table"
  >
    <template slot="detect_rules" slot-scope="data" class="detect-rules">
      <div class="badges">
        <template v-if="data.item.detect_rule.length !== 0">
          <yara v-for="(l, k) in data.item.detect_rule" :key="k" variant="danger" :yara="l" />
        </template>
        <b-badge v-if="data.item.detect_rule.length === 0" variant="secondary">
          No rule detects
        </b-badge>
      </div>
    </template>
  </b-table>
  <div v-else class="no-dropped">
    <p>No file dropped.</p>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Yara from '~/components/Yara'

export default {
  name: 'Files',
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
        }
      ]
    },
    ...mapState(['report'])
  }
}
</script>

<style lang="stylus">
.dropped-file-table
  td
    border-top 1px solid gray
</style>
