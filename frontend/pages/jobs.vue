<template>
  <b-container fluid>
    <b-row class="tasks">
      <b-col>
        <h1>Current</h1>
        <list :jobs="current" />
      </b-col>
    </b-row>
    <b-row class="tasks">
      <b-col>
        <h1>Queued</h1>
        <list :jobs="jobs.queued" />
      </b-col>
    </b-row>
    <b-row class="tasks">
      <b-col>
        <h1>Finished</h1>
        <list :jobs="jobs.finished" />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
  import List from '~/components/jobs/List'
  import { mapState } from 'vuex'

  export default {
    name: "jobs",
    components: {
      List
    },
    computed: {
      current() {
        if(this.jobs.current === null) {
          return []
        } else {
          return [ this.jobs.current ];
        }
      },
      ... mapState([ 'jobs' ])
    }

  }
</script>

<style lang="stylus" scoped>
  .tasks
    padding-bottom 1em
  hr
    background-color white
</style>
