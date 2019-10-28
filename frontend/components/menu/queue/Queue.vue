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
import { computed, createComponent, PropType } from "@vue/composition-api"
import LengthBadge from "@/components/atoms/length-badge.vue"

export default createComponent({
  name: "Queue",
  components: {
    LengthBadge,
  },
  props: {
    jobs: {
      type: Object as PropType<Jobs>,
      required: true,
    },
  },
  setup({ jobs }) {
    const isActive = computed(() => jobs.current_job !== null || jobs.queued_jobs.length !== 0)
    return {
      isActive,
      currentJobs: computed(() => [jobs.current_job]),
      queuedJobs: computed(() => jobs.queued_jobs),
    }
  },
})
</script>
