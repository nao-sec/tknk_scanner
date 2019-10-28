<template>
  <span :class="{ working: isActive }">{{ len }}</span>
</template>

<script lang="ts">
import { computed, createComponent, PropType } from "@vue/composition-api"
export default createComponent({
  name: "LengthBadge",
  props: {
    elements: {
      type: Array as PropType<any[]>,
      required: true,
    },
  },
  setup({ elements }) {
    const len = computed(() => {
      return elements.length
    })
    const isActive = computed(() => {
      return elements.length !== 0
    })

    return {
      len,
      isActive,
    }
  },
})
</script>

<style lang="stylus" scoped>
.working
  color #0f0
</style>
