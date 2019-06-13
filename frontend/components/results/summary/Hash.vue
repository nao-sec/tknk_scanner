<template>
  <div id="hash">
    <div>
      <span ref="copyIcon"><font-awesome-icon :icon="icon" @click="copy" /></span>
      <b-tooltip
        :show.sync="does_show_tooltip"
        triggers="click"
        :target="() => $refs.copyIcon"
        placement="bottom"
      >
        {{ message }}
      </b-tooltip>
    </div>
    <div>{{ hash }}</div>
  </div>
</template>

<script>
export default {
  name: 'Hash',
  props: ['hash'],
  data() {
    return {
      does_show_tooltip: false,
      has_copy_error: false
    }
  },
  computed: {
    message() {
      if (this.has_copy_error) {
        return 'Copy failed, Is your browser newest?'
      } else {
        return 'Copied'
      }
    },
    icon() {
      if (!this.does_show_tooltip) {
        return 'clipboard'
      } else {
        return 'clipboard-check'
      }
    }
  },
  methods: {
    copy() {
      this.$copyText(this.hash)
        .then(() => {
          this.does_show_tooltip = true
          this.has_copy_error = false
        })
        .catch(() => {
          this.does_show_tooltip = true
          this.has_copy_error = true
        })
      setTimeout(() => {
        this.does_show_tooltip = false
      }, 1000)
    }
  }
}
</script>

<style lang="stylus" scoped>
#hash
  display flex
  word-break break-all
  i
    padding-right 0.25em
</style>
