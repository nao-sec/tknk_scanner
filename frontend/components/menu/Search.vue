<template>
  <b-nav-form @submit="submit">
    <b-form-input size="sm" :class="input_class" type="text" v-model="hash" ref="inputHash" placeholder="MD5, SHA-1 or SHA-256" />
    <b-button size="sm" variant="success" type="submit" class="mr-sm-5">Search</b-button>
    <b-tooltip :disabled.sync="disabled" :target="() => $refs.inputHash" ref="hintingTooltip">
      You should input md5, sha1 or sha256 hash ;P
    </b-tooltip>
  </b-nav-form>
</template>

<script>
  export default {
    name: "Search",
    data() {
      return {
        hash: '',
        disabled: true
      }
    },
    methods: {
      submit(evt) {
        evt.preventDefault();

        let type = '';
        if(/[a-f0-9]+/.test(this.hash)) {
          switch (this.hash.length) {
            case 32:
              type = "md5";
              break;
            case 40:
              type = "sha1";
              break;
            case 64:
              type = 'sha256';
              break;
          }
        }
        if(type === '') {
          this.$refs.hintingTooltip.$emit('open');
          return;
        }

        this.$router.push({ name: 'search-type-hash', params: { type: type, hash: this.hash } });
      },
    },
    computed: {
      input_class() {
        let css_class = ['mr-sm-2', 'hash'];

        if(this.hash !== '') {
          css_class.push('input');
        }

        return css_class;
      }
    },
    watch: {
      hash() {
        if(this.hash === ''){
          this.disabled = true;
          this.$refs.hintingTooltip.$emit('close');
        }
      }
    }
  }
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
