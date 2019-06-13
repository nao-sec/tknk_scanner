<template>
  <b-container fluid>
    <b-row>
      <b-col>
        <h1>Search</h1>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <reports-summary :items="results" />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import ReportsSummary from '~/components/ReportsSummary'

export default {
  name: 'SearchIndex',
  components: {
    ReportsSummary
  },
  data() {
    return {
      results: []
    }
  },
  validate({ params }) {
    // is it hash strings?
    if (!/[0-9a-f]+/.test(params.hash)) {
      return false
    }

    // is it truly length?
    const length = params.hash.length
    switch (params.type) {
      case 'md5':
        return length === 32
      case 'sha1':
        return length === 40
      case 'sha256':
        return length === 64
      default:
        return false
    }
  },
  async mounted() {
    const { data } = await this.$axios
      .get(`/search/${this.$route.params.type}/${this.$route.params.hash}`)
      .catch((e) => {
        console.error(`Page fetching error: ${e}`)
        this.$root.error(e)
      })

    this.results = data.results
  }
}
</script>

<style scoped></style>
