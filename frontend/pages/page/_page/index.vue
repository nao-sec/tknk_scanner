<template>
  <b-container fluid>
    <b-row>
      <b-col>
        <h1>Recent</h1>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <reports-summary :items="scope_results" />
        <b-pagination
          align="center"
          :total-rows="max_pages * 50"
          v-model="current_page"
          :per-page="50"></b-pagination>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
  import ReportsSummary from '~/components/ReportsSummary'

  export default {
    name: "page-index",
    components: {
      ReportsSummary
    },
    validate({ params }) {
      return /\d+/.test(params.page);
    },
    data() {
      return {
        scope_results: [],
        current_page: 0,
        max_pages: 0
      }
    },
    async mounted() {
      let {data} = await this.$axios.get(`/page/${this.$route.params.page}`).catch(e => {
        console.error(`Page fetching error: ${e}`);
        this.$root.error(e);
      });
      this.current_page = parseInt(this.$route.params.page, 10);
      this.max_pages = data.page_size;
      this.scope_results = data.page;
    },
    watch: {
      'current_page': function(next, current) {
        if(current !== 0){
          this.$router.push({ name: 'page-page', params: { page: next}});
        }
      }
    }
  }
</script>

<style scoped>

</style>
