<template>
  <div>
    <b-navbar-nav>
      <b-nav-item
        :to="{ name: 'jobs' }"
        :active="current_length !== 0 || jobs.queued.length !== 0"
      >
        Processing:
        <length-badge :elements="[jobs.current_job]"></length-badge> / Queued:
        <length-badge elements="jobs.queued_jobs"></length-badge>
      </b-nav-item>
    </b-navbar-nav>
  </div>
</template>

<script lang="ts">
import { createComponent, onMounted, PropType } from "@vue/composition-api"
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
  setup() {
    onMounted(() => {
      this.$accessor.registerFetchJobsWorker()
    })
  },
})
</script>
