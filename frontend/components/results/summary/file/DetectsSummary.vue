<template>
  <b-table :items="detectsSummary" class="summary-table" stacked fixed small>
    <template slot="DIE Indicators" slot-scope="die">
      <b-badge v-for="(v, k) in die.value" :key="k" variant="info" class="die">
        {{ v }}
      </b-badge>
    </template>
    <template slot="detect_rules" slot-scope="rules">
      <div class="badges">
        <template v-if="rules.value.length !== 0">
          <yara v-for="(l, k) in rules['value']" :key="k" :yara="l" />
        </template>
        <b-badge v-if="rules.value.length === 0" variant="secondary">
          No rule detects
        </b-badge>
      </div>
    </template>
    <template slot="AVClass" slot-scope="avclass">
      <template v-if="avclass.item.AVClass.data.length !== 0">
        <b-badge
          v-for="(cls, key) in avclass.item.AVClass.data"
          :key="key"
          variant="primary"
          class="avclass"
        >
          {{ cls.family_name }}
          <b-badge variant="light" class="num">
            {{ cls.count }}
          </b-badge>
        </b-badge>
      </template>
      <b-badge v-if="avclass.item.AVClass.data.length === 0" variant="secondary">
        No AVClass detects
      </b-badge>
    </template>
  </b-table>
</template>

<script>
import Yara from '~/components/Yara'
export default {
  name: 'DetectsSummary',
  components: {
    Yara
  },
  props: ['detectsSummary']
}
</script>

<style lang="stylus" scoped>
.die
.avclass
  word-break break-all
  margin 0 0.5em 0 0
.badges
  word-break break-word
</style>
