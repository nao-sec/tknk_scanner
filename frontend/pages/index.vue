<template>
  <section class="container">
    <div class="wrapper">
      <div class="title">
        <h1>tknk_scanner</h1>
      </div>
      <div class="form">
        <div class="form-wrapper">
          <upload-form />
        </div>
      </div>
      <div class="github">
        <div class="foot-wrapper">
          <a href="https://github.com/nao-sec/tknk_scanner">
            <font-awesome-icon :icon="['fab', 'github']" size="3x" />
            <p>Code on Github</p>
          </a>
        </div>
      </div>
      <div class="credit">
        <div class="foot-wrapper">
          <nuxt-link :to="{ name: 'credits' }">
            <font-awesome-icon icon="copyright" size="3x" />
            <p>Credits</p>
          </nuxt-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import UploadForm from "~/components/UploadForm"

export default {
  components: {
    UploadForm,
  },
}
</script>

<style lang="stylus" scoped>
.showcase
  display block
.container
  min-width 1000px
  max-width 1000px
  min-height 900px
  height calc(100% - 60px)
  display flex
  align-items center
  justify-content center
  .wrapper
    position relative
    width 1000px
    height 900px
    .title
      color #00ff00
      z-index 4
      background-color #2c2c2c
      display flex
      justify-content center
      align-items center
      position absolute
      top 0px
      right 0px
      width 350px
      height 350px
      border-radius 50%
    .form
      z-index 39
      background-color #444444
      position absolute
      display flex
      justify-content center
      align-items center
      left 120px
      top 130px
      width 600px
      height 600px
      border-radius 50%
      .form-wrapper
        display flex
        justify-content center
        align-items center
        width 400px
        height 400px
    .github
      z-index 1
      background-color #393939
      position absolute
      display flex
      justify-content center
      align-items center
      top 105px
      left 20px
      width 200px
      height 200px
      border-radius 50%
      .foot-wrapper
        text-align center
    .credit
      z-index 2
      background-color #3f3f3f
      position absolute
      display flex
      justify-content center
      align-items center
      bottom 90px
      right 300px
      width 150px
      height 150px
      border-radius 50%
      .foot-wrapper
        text-align center
    .credit
    .github
      a
        color #00ff00
      p
        margin-bottom 0
</style>
