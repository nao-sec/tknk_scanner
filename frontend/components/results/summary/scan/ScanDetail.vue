<template>
  <b-table
    :items="scanSummary"
    :fields="fields"
    class="summary-table"
    stacked
    fixed
    small
  >
    <template slot="uuid" slot-scope="uuid">
      <download :id="uuid.value" />
    </template>
  </b-table>
</template>

<script>
import Download from "~/components/results/summary/scan/Download"

export default {
  name: "ScanSummary",
  components: {
    Download,
  },
  props: ["scanSummary"],
  computed: {
    fields() {
      return [
        {
          key: "mode",
          label: "Mode",
        },
        {
          key: "detail",
          label: "Detail",
        },
        {
          key: "running_time",
          label: "Running Time",
        },
        {
          key: "timestamp",
          label: "Timestamp",
        },
        {
          key: "uuid",
          label: "Download dumped file",
        },
      ]
    },
  },
}
</script>

<style lang="stylus" scoped></style>
