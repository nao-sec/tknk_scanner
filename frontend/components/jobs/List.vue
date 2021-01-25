<template>
  <div v-if="!isEmpty">
    <b-table :items="items">
      <template v-slot:cell(Status)="data">
        <job-status :report-id="data.item.Status" @job-finish="pulse"></job-status>
      </template>
    </b-table>
  </div>
  <div v-else class="empty">
    <p>Empty :)</p>
  </div>
</template>

<script lang="ts">
import Vue, { PropOptions } from "vue"
import JobStatus from "~/components/jobs/JobStatus.vue"
import { Job } from "~/types/tknk"

export default Vue.extend({
  name: "JobsList",
  components: {
    JobStatus,
  },
  props: {
    jobs: {
      type: Array,
      required: true,
    } as PropOptions<Job[]>,
  },
  computed: {
    isEmpty(): boolean {
      return this.jobs.length === 0
    },
    items(): any[] {
      return this.jobs.map(job => ({
        "File Name": job.config.target_file,
        Mode: job.config.mode,
        "Running Time": job.config.time,
        Status: job.id,
      }))
    },
  },
  methods: {
    pulse() {
      this.$emit("job-finish")
    },
  },
})
</script>

<style lang="stylus" scoped>
.empty
  font-style italic
  padding-left 1em
</style>
