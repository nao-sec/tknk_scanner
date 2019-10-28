<template>
  <div>
    <b-modal ref="errorModal" hide-footer title="Error" class="error-modal">
      <div class="d-block text-center">
        <p class="my-4">
          {{ error_message }}
        </p>
      </div>
      <b-btn class="mt-3" variant="outline-danger" block @click="close_error_modal">
        Close
      </b-btn>
    </b-modal>
    <b-form v-if="show" @submit="upload">
      <b-form-group id="upload-file" label="File:" label-for="uploadFileInput" description="accept only PE binary">
        <b-form-file id="uploadFileInput" v-model="form.file" :state="Boolean(form.file)" placeholder="Select file" required />
      </b-form-group>
      <b-form-group id="scan-mode" label="Scan Mode:" label-for="scanModeSelect" description="select dump tool">
        <b-form-select v-model="form.mode" :options="scan_mode" placeholder="Select running mode" required />
      </b-form-group>
      <b-form-group id="time-input" label="Running Time:" label-for="timeInput">
        <b-form-input id="timeInput" v-model="form.time" type="number" placeholder="seconds" required />
      </b-form-group>
      <b-button type="submit" :variant="get_variant" :disabled="!can_upload">
        <template v-if="is_uploading">
          Uploading...
        </template>
        <template v-else>
          Upload
        </template>
      </b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  name: "UploadForm",
  data() {
    return {
      form: {
        file: null,
        mode: null,
        time: 120,
      },
      scan_mode: [
        { value: "hollows_hunter", text: "hollows_hunter" },
        { value: "procdump", text: "procdump" },
        { value: "diff", text: "diff" },
        { value: "scylla", text: "scylla" },
      ],
      error_message: null,
      is_uploading: false,
      show: true,
    }
  },
  computed: {
    can_upload() {
      return !this.is_uploading && (this.form.file !== null && this.form.mode !== null && this.form.time !== null)
    },
    get_variant() {
      return this.is_uploading ? "secondary" : "success"
    },
  },
  methods: {
    close_error_modal() {
      this.$refs.errorModal.hide()
    },
    async upload(e) {
      e.preventDefault()

      const data = new FormData()
      data.append("file", this.form.file)

      const conf = {
        onUploadProgress: () => {
          this.is_uploading = true
        },
      }
      const res = await this.$axios.$post("/upload", data, conf).catch(e => {
        this.form = {
          file: null,
          mode: null,
          time: 120,
        }
        this.is_uploading = false
        if (e.response.data && e.response.data.status_code && e.response.data.status_code !== 0) {
          this.error_message = e.response.data.message
        } else {
          this.error_message = "Unknown Upload Error"
        }
        this.$refs.errorModal.show()
        this.show = false
        this.$nextTick(() => {
          this.show = true
        })
        throw e
      })

      const analyze = await this.$axios
        .$post(
          "/analyze",
          {
            path: res.path,
            mode: this.form.mode,
            time: parseInt(this.form.time, 10),
          },
          conf,
        )
        .catch(e => {
          this.form = {
            file: null,
            mode: null,
            time: 120,
          }
          this.is_uploading = false
          if (e.response.data && e.response.data.status_code && e.response.data.status_code !== 0) {
            this.error_message = e.response.data.message
          } else {
            this.error_message = "Unknown Analyze Error"
          }
          this.$refs.errorModal.show()
          this.show = false
          this.$nextTick(() => {
            this.show = true
          })
          throw e
        })

      this.$router.push({
        name: "results-resultid",
        params: { resultid: analyze.UUID },
      })
    },
  },
}
</script>

<style lang="stylus" scoped>
.fileupload
  width auto
.error-modal
  color black
</style>
