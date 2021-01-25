<template>
  <b-table :items="fileSummary" :fields="fields" class="summary-table" stacked fixed small>
    <template slot="file_name" slot-scope="file_name">
      <div class="filename">
        {{ file_name.value }}
      </div>
    </template>
    <template slot="magic" slot-scope="magic">
      <div class="magic">
        {{ magic.value }}
      </div>
    </template>
    <template slot="md5" slot-scope="md5">
      <hash :hash="md5.value" />
    </template>
    <template slot="sha1" slot-scope="sha1">
      <hash :hash="sha1.value" />
    </template>
    <template slot="sha256" slot-scope="sha256">
      <hash :hash="sha256.value" />
    </template>
  </b-table>
</template>

<script>
import Hash from "~/components/results/summary/Hash"

export default {
  name: "FileSummary",
  components: {
    Hash,
  },
  props: ["fileSummary"],
  computed: {
    fields() {
      return [
        { key: "file_name", label: "File Name" },
        { key: "size", label: "Size" },
        { key: "magic", label: "Magic" },
        { key: "md5", label: "MD5" },
        { key: "sha1", label: "SHA-1" },
        { key: "sha256", label: "SHA-256" },
      ]
    },
  },
}
</script>

<style lang="stylus" scoped>
.magic
.filename
  word-break break-all
</style>
