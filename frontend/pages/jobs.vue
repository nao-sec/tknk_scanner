<template>
  <b-container fluid>
    <b-row class="tasks">
      <b-col>
        <h1>Current</h1>
        <list :jobs="current" @job-finish="currentFinish"></list>
      </b-col>
    </b-row>
    <b-row class="tasks">
      <b-col>
        <h1>Queued</h1>
        <list :jobs="queued"></list>
      </b-col>
    </b-row>
  </b-container>
</template>

<script lang="ts">
import Vue from "vue"
import List from "~/components/jobs/List.vue"

export default Vue.extend({
  name: "Jobs",
  components: {
    List,
  },
  computed: {
    current() {
      const c = (this as any).$accessor.currentJobs.current_job
      if (c === null) {
        return []
      }
      return [c]
    },
    queued() {
      return (this as any).$accessor.currentJobs.queued_jobs
    },
    finished() {
      return (this as any).$accessor.finishedJobs
    },
  },
  methods: {
    currentFinish() {
      return (this as any).$accessor.jobFinish(this.current[0])
    },
  },
})
</script>

<style lang="stylus" scoped>
.tasks
  padding-bottom 1em
hr
  background-color white
</style>
