<template lang="html">
  <!-- display tags -->
  <div v-if="field.type === 'tags'" :class="field.name">
    <span v-for="tag in getFieldValue"
          v-bind:key="tag.name"
          class="badge m-1"
          v-bind:class="{'badge-secondary': !tag.fresh, 'badge-primary': tag.fresh}">
      {{tag.name}}
    </span>
  </div>

  <!-- display generic arrays as a list of tags -->
  <span v-else-if="field.type === 'list'" :class="field.name">
    <span v-for="v in getFieldValue"
          v-bind:key="v"
          class="badge m-1 badge-primary">
      {{v}}
    </span>
  </span>

  <div v-else-if="field.type == 'killchain'" :class="field.name">
    <span v-for="v in getFieldValue"
          v-bind:key="v.phase_name"
          class="badge m-1 badge-primary"
          :title="v.kill_chain_name">
          {{v.phase_name}}
    </span>
  </div>

  <div v-else-if="field.type === 'datetime'" :class="field.name">
    <span>{{ formatDateString(getFieldValue) }}</span>
  </div>

  <div v-else-if="field.type === 'code'" :class="field.name">
    <code>{{getFieldValue}}</code>
  </div>

  <div v-else-if="field.type === 'pre'" :class="field.name">
    <pre>{{getFieldValue}}</pre>
  </div>

  <div v-else-if="field.type === 'boolean'" :class="field.name">
    <input type="checkbox" name=""> <!-- implement me! -->
  </div>

  <div v-else-if="field.type === 'action'" :class="field.name">
    <button type="button" class="btn btn-outline-primary btn-sm" @click="field.calls(elt)"> {{field.label}}</button>
  </div>

  <!-- fall back to displaying a normal field.name -->
  <span v-else>
    {{getFieldValue}}
  </span>

</template>

<script>
import moment from 'moment-timezone'

// Expected input format: 2018-04-16T16:18:25.179482+00:00
const inputDateTimeFormat = 'YYYY-MM-DDTHH:mm:ss.SSSSSSZZ'
// Wanted output format: 2018-04-16 18:18:25 +0200 (to localtime)
const outputDateTimeFormat = 'YYYY-MM-DD HH:mm:ss ZZ'

export default {
  props: ['field', 'elt'],
  methods: {
    formatDateString (string) {
      return moment(string, inputDateTimeFormat).format(outputDateTimeFormat)
    }
  },
  computed: {
    getFieldValue () {
      return this.elt[this.field.name]
    }
  }
}
</script>

<style lang="css">

.badge {
  font-size: 90%;
}

code {
  white-space: pre-wrap;
}
</style>
