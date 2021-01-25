<template>
  <span :class="{ working: isActive }">{{ len }}</span>
</template>

<script lang="ts">
import Vue, { PropOptions } from "vue"
export default Vue.extend({
  name: "LengthBadge",
  props: {
    elements: {
      type: Array,
      required: true,
    } as PropOptions<any[]>,
  },
  computed: {
    len(): number {
      return this.elements.length
    },
    isActive(): boolean {
      return this.elements.length !== 0
    },
  },
})
</script>

<style lang="stylus" scoped>
.working
  color #0f0
</style>
