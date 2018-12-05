<template>
  <div v-if="this.jobs.length !== 0">
    <b-table :items="items">
      <template slot="Status" slot-scope="data">
        <job-status :id="data.item.Status" />
      </template>
    </b-table>
  </div>
  <div class="empty" v-else>
    <p>Empty :)</p>
  </div>
</template>

<script>
  import JobStatus from '~/components/jobs/JobStatus'

  export default {
    name: "List",
    props: [
      'jobs'
    ],
    components: {
      JobStatus
    },
    computed: {
      items() {
        return this.jobs.map(o => {
          return {
            "File Name": o.config.target_file,
            "Mode": o.config.mode,
            "Running Time": o.config.time,
            "Status": o.id
          }
        });
      }
    }
  }
</script>

<style lang="stylus" scoped>
  .empty
    font-style italic
    padding-left 1em
</style>
