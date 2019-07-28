<template>
  <div>
    <b-navbar-nav>
      <b-nav-item
        :to="{ name: 'jobs' }"
        :active="current_length !== 0 || jobs.queued.length !== 0"
      >
        Processing: <span :class="current_class">{{ current_length }}</span> /
        Queued:
        <span :class="queued_class">{{ jobs.queued.length }}</span>
      </b-nav-item>
    </b-navbar-nav>
  </div>
</template>
<script>
import { mapState, mapMutations } from "vuex"

export default {
  name: "Queue",
  data() {
    return {
      paused: false,
    }
  },
  mounted() {
    this.next_tick()
  },
  computed: {
    current_length() {
      return this.jobs.current !== null ? 1 : 0
    },
    current_class() {
      return this.current_length === 0 ? null : ["working"]
    },
    queued_class() {
      return this.jobs.queued.length === 0 ? null : ["working"]
    },
    ...mapState(["jobs"]),
  },
  methods: {
    next_tick() {
      this.fetch_jobs()
      if (!this.paused) {
        if (this.jobs.current !== null) {
          setTimeout(this.next_tick, 5000)
        } else {
          setTimeout(this.next_tick, 10000)
        }
      }
    },
    fetch_jobs() {
      this.$axios
        .get("/jobs", { progress: false })
        .then(res => {
          if (res.data.status_code === 0) {
            this.change_current(res.data.current_job)
            this.push_queued_jobs(res.data.queued_jobs)
          }
        })
        .catch(e => {
          console.error(`Fetching jobs caused a error: ${e}`)
          this.paused = true
        })
    },
    ...mapMutations({
      change_current: "jobs/change_current",
      push_queued_jobs: "jobs/push_queued_jobs",
    }),
  },
}
</script>

<style lang="stylus" scoped>
.working
  color #0f0
</style>
