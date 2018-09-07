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
      <div class="foot">
        <div class="foot-wrapper">
          <a href="https://github.com/nao-sec/tknk_scanner">
            <i class="fab fa-github fa-3x"></i>
            <p>Code on Github</p>
          </a>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import UploadForm from '~/components/UploadForm'

  export default {
    components: {
      UploadForm
    }
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
      width 850px
      height 850px
      .title
        color #00ff00
        z-index 4
        background-color #2c2c2c
        display flex
        justify-content center
        align-items center
        position absolute
        top 0px
        right 30px
        width 350px
        height 350px
        border-radius 50%
      .form
        z-index 39
        background-color #3f3f3f
        position absolute
        display flex
        justify-content center
        align-items center
        top 115px
        width 600px
        height 600px
        border-radius 50%
        .form-wrapper
          display flex
          justify-content center
          align-items center
          width 400px
          height 400px
      .foot
        z-index 1
        background-color #6e6e6e
        position absolute
        display flex
        justify-content center
        align-items center
        bottom 0px
        left 300px
        width 200px
        height 200px
        border-radius 50%
        .foot-wrapper
          text-align center
          a
            color #7fdfff
</style>

