<template>
  <b-table v-if="hasItems" :items="tableItems" :fields="tableHeaders" class="dropped-file-table">
    <template slot="detect_rules" slot-scope="data" class="detect-rules">
      <div class="badges">
        <template v-if="data.item.detect_rules.length !== 0">
          <yara v-for="(l, k) in data.item.detect_rules" :key="k" variant="danger" :yara="l" />
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

<script lang="ts">
import { computed, createComponent, PropType } from "@vue/composition-api"
import { DumpedFilesScanReport } from "~/types/tknk"
import Yara from "~/components/Yara.vue"

export default createComponent({
  name: "Files",
  components: {
    Yara,
  },
  props: {
    dumpedFilesScanReport: {
      type: Array as PropType<DumpedFilesScanReport[]>,
      required: true,
    },
  },
  setup({ dumpedFilesScanReport }) {
    const tableHeaders = computed(() => [
      {
        key: "file_name",
        label: "File Name",
      },
      {
        key: "size",
        label: "Size",
      },
      {
        key: "detect_rules",
        label: "Detect Rule",
      },
      {
        key: "magic",
        label: "Magic",
      },
    ])
    const tableItems = computed(() => dumpedFilesScanReport)
    const hasItems = computed(() => dumpedFilesScanReport.length !== 0)

    return {
      tableHeaders,
      tableItems,
      hasItems,
    }
  },
})
</script>

<style lang="stylus">
.dropped-file-table
  td
    border-top 1px solid gray
</style>
