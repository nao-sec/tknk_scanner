<template>
  <b-button
    variant="success"
    :href="'/api/download/' + id"
    size="sm"
  >
    Download
  </b-button>
</template>

<script>
export default {
  name: 'Download',
  props: ['id']
}
</script>

<style scoped></style>
