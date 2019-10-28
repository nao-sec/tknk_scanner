<template>
  <div>
    <b-navbar-nav>
      <b-nav-item :to="{ name: 'jobs' }" :active="isActive">
        Processing:
        <length-badge :elements="currentJobs"></length-badge> / Queued:
        <length-badge :elements="queuedJobs"></length-badge>
      </b-nav-item>
    </b-navbar-nav>
  </div>
</template>

<script lang="ts">
import Vue, { PropOptions } from "vue"
import LengthBadge from "@/components/atoms/length-badge.vue"
import { Jobs, Job } from "~/types/tknk"

export default Vue.extend({
  name: "Queue",
  components: {
    LengthBadge,
  },
  props: {
    jobs: {
      type: Object,
      required: true,
    } as PropOptions<Jobs>,
  },
  computed: {
    isActive(): boolean {
      return this.jobs.current_job !== null || this.jobs.queued_jobs.length !== 0
    },
    currentJobs(): Job[] {
      return this.jobs.current_job === null ? [] : [this.jobs.current_job]
    },
    queuedJobs(): Job[] {
      return this.jobs.queued_jobs
    },
  },
})
</script>
