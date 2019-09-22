<template>
  <div class="status">
    <font-awesome-icon
      :icon="statusIcon"
      :class="statusClass"
      :spin="status === 1"
      size="xs"
    />
    <nuxt-link
      v-if="status === 0"
      :to="{ name: 'results-resultid', params: { resultid: id } }"
    >
      Results
    </nuxt-link>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop, Emit } from "vue-property-decorator"

@Component
export default class JobStatus extends Vue {
  // data
  status: any = null
  isSuccess: boolean = false
  paused: boolean = false

  // props
  @Prop({ type: String })
  id: string = ""

  // computed
  get statusIcon(): string {
    if (this.status === 1) {
      // processing
      return "spinner"
    } else if (this.status === 0 && this.isSuccess) {
      // done and scanning success
      return "check-circle"
    } else if (this.status === 0 && !this.isSuccess) {
      // done, but fail scanning
      return "times-circle"
    } else {
      // not implemented state
      return "question-circle"
    }
  }

  get statusClass(): string[] {
    if (this.status === 0 && this.isSuccess) {
      // done and scanning success
      return ["success"]
    } else if (this.status === 0 && !this.isSuccess) {
      // done, but fail scanning
      return ["fail"]
    } else {
      // not implemented state
      return ["unknown"]
    }
  }

  // methods
  @Emit()
  fetchResult() {
    this.$axios
      .get(`/results/${this.id}`)
      .then(res => {
        this.status = res.data.status_code
        if (res.data.status_code === 0) {
          this.isSuccess = res.data.report.result.is_success
        }
      })
      .catch(e => {
        console.error(`Fetching result error: ${e}`)
        this.paused = true
      })
  }

  @Emit()
  nextTick() {
    this.fetchResult()
    if ((this.status === null || this.status !== 0) && !this.paused) {
      setTimeout(this.nextTick, 9000)
    }
  }

  // life cycle
  mounted() {
    this.nextTick()
  }
}
</script>

<style lang="stylus" scoped>
.status
  height 1em
.success
  color #00ff00
.fail
  color #ff3300
</style>
