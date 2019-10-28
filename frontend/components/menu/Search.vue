<template>
  <b-nav-form @submit="submit">
    <b-form-input id="search-input-hash" v-model="hash" size="sm" :class="inputClass" type="text" placeholder="MD5, SHA-1 or SHA-256" />
    <b-button size="sm" variant="success" type="submit" class="mr-sm-5">
      Search
    </b-button>
    <b-tooltip id="hintingTooltip" target="search-input-hash" :disabled="state.disabled">
      You should input md5, sha1 or sha256 hash ;P
    </b-tooltip>
  </b-nav-form>
</template>

<script lang="ts">
import { createComponent, reactive, watch, ref, computed } from "@vue/composition-api"

export default createComponent({
  name: "Search",
  setup(props, { root }) {
    const hash = ref("")
    const state = reactive({
      hash,
      disabled: true,
    })

    const inputClass = computed(() => {
      const css_class = ["mr-sm-2", "hash"]
      if (state.hash !== "") {
        css_class.push("input")
      }
      return css_class
    })

    const submit = (evt: Event) => {
      evt.preventDefault()

      let type = ""
      if (/[a-f0-9]+/.test(state.hash)) {
        switch (state.hash.length) {
          case 32:
            type = "md5"
            break
          case 40:
            type = "sha1"
            break
          case 64:
            type = "sha256"
            break
        }
      }
      if (type === "") {
        state.disabled = false
        root.$emit("bv::show::tooltip", "hintingTooltip")
        return
      }

      root.$router.push({
        name: "search-type-hash",
        params: { type: type, hash: state.hash },
      })
    }

    watch(
      () => state.hash,
      () => {
        if (state.hash === "") {
          root.$emit("bv::hide::tooltip", "hintingTooltip")
          state.disabled = true
        }
      },
    )

    return {
      state,
      submit,
      hash,
      inputClass,
    }
  },
})
</script>

<style lang="stylus" scoped>
.hash
  width 10em
  transition all 200ms 0s cubic-bezier(0.4, 0, 1, 1)
  &:focus
    width 32em
.input
  width 32em
</style>
