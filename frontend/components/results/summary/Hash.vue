<template>
  <div id="hash">
    <div>
      <i :class="icon" ref="copyIcon" @click="copy"></i>
      <b-tooltip :show.sync="does_show_tooltip" triggers="click" :target="() => $refs.copyIcon" placement="bottom">{{ message }}</b-tooltip>
    </div>
    <div>{{ hash }}</div>
  </div>
</template>

<script>
  import clipboard from 'clipboard'

  export default {
    name: "Hash",
    props: [
      'hash'
    ],
    data() {
      return {
        does_show_tooltip: false,
        has_copy_error: false
      }
    },
    methods: {
      copy() {
        this.$copyText(this.hash).then(e => {
          this.does_show_tooltip = true;
          this.has_copy_error = false;
        }).catch(e => {
          this.does_show_tooltip = true;
          this.has_copy_error = true;
        });
        setTimeout(() => {this.does_show_tooltip = false;}, 1000);
      }
    },
    computed: {
      message() {
        if (this.has_copy_error) {
          return "Copy failed, Is your browser newest?";
        } else {
          return "Copied";
        }
      },
      icon() {
        if (!this.does_show_tooltip) {
          return ['fas', 'fa-clipboard'];
        } else {
          return ['fas', 'fa-clipboard-check'];
        }
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
