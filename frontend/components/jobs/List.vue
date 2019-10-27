<template>
  <div v-if="this.jobs.length !== 0">
    <b-table :items="items">
      <template slot="Status" slot-scope="data">
        <job-status :id="data.item.Status" />
      </template>
    </b-table>
  </div>
  <div v-else class="empty">
    <p>Empty :)</p>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator"
import JobStatus from "~/components/jobs/JobStatus"

@Component({
  components: {
    JobStatus,
  },
})
export default class List extends Vue {
  // props
  @Prop({ type: [Object] })
  jobs: Job[] = []

  get items() {
    return this.jobs.map(o => {
      return {
        "File Name": o.config.target_file,
        Mode: o.config.mode,
        "Running Time": o.config.time,
        Status: o.id,
      }
    })
  }
}
</script>

<style lang="stylus" scoped>
.empty
  font-style italic
  padding-left 1em
</style>
