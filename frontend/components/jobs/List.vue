<template>
  <div v-if="jobs_length !== 0">
    <b-table :items="items">
      <template slot="Status" slot-scope="data">
        <job-status :report-id="data.item.Status"></job-status>
      </template>
    </b-table>
  </div>
  <div v-else class="empty">
    <p>Empty :)</p>
  </div>
</template>

<script lang="ts">
import { computed, createComponent, PropType } from "@vue/composition-api"
import JobStatus from "~/components/jobs/JobStatus.vue"
import { Job } from "~/types/tknk"

export default createComponent({
  name: "jobs-list",
  components: {
    JobStatus,
  },
  props: {
    jobs: {
      type: Array as PropType<Job[]>,
      required: true,
    },
  },
  setup({ jobs }) {
    const jobs_length = computed(() => jobs.length)

    const items = computed(() => {
      return jobs.map(job => ({
        "File Name": job.config.target_file,
        Mode: job.config.mode,
        "Running Time": job.config.time,
        Status: job.id,
      }))
    })

    return {
      items,
      jobs_length,
    }
  },
})
</script>

<style lang="stylus" scoped>
.empty
  font-style italic
  padding-left 1em
</style>
