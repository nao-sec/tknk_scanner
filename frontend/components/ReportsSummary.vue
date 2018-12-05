<template>
  <b-table :items="reports_summary" :fields="fields">
    <template slot="file_name" slot-scope="data">
      <div class="filename"> {{ data.value }}</div>
    </template>
    <template slot="detect_rules" slot-scope="data">
      <yara v-for="(rule, key) in data.value" :key="key" :yara="rule" />
    </template>
    <template slot="is_in_vt" slot-scope="data">
      <b-badge :variant="data.value ? 'primary' : 'warning'">{{ data.value ? 'Found' : 'Not Found'}}</b-badge>
    </template>
    <template slot="uuid" slot-scope="data">
      <nuxt-link :to="{ name: 'results-resultid', params: { resultid: data.value }}">Result</nuxt-link>
    </template>
  </b-table>
</template>

<script>
  import Yara from '~/components/Yara'

  export default {
    name: "ReportsSummary",
    props: [
      'items'
    ],
    components: {
      Yara
    },
    computed: {
      fields() {
        return [
          { key: 'file_name', label: 'FileName' },
          { key: 'size', label: 'Size' },
          { key: 'mode', label: 'Mode' },
          { key: 'run_time', label: 'Run Time' },
          { key: 'detect_rules', label: 'Detect Rules' },
          { key: 'is_in_vt', label: 'VirusTotal'},
          { key: 'timestamp', label: 'Timestamp' },
          { key: 'uuid', label: 'Results'},
        ]
      },
      reports_summary() {
        return this.items.map(report => {
          let detect_rules = [];

          if(report.scans !== null && report.scans !== undefined && report.scans.length !== 0) {
            report.scans.forEach(scan => {
              detect_rules = detect_rules.concat(scan.detect_rule);
            });
          }

          if(report.target_scan !== null && report.target_scan !== undefined && report.target_scan.detect_rule.length !== 0){
            detect_rules = detect_rules.concat(report.target_scan.detect_rule);
          }

          // remove duplicates
          detect_rules = Array.from(new Set(detect_rules));

          return {
            file_name: report.target_scan === undefined || report.target_scan === null ? null : report.target_scan.file_name,
            mode: report.mode,
            run_time: report.run_time === null || report.run_time === undefined ? null : parseInt(report.run_time, 10),
            detect_rules: detect_rules,
            size: report.target_scan === undefined || report.target_scan === null? null : report.target_scan.size,
            is_in_vt: report.avclass === undefined || report.avclass === null ? false : report.avclass.flag,
            timestamp: report.timestamp,
            uuid: report.UUID,
          }
        });
      }
    }
  }
</script>

<style lang="stylus" scoped>
  .filename
    word-break break-all
</style>
