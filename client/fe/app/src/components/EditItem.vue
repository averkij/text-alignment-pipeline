<template>
  <div>
    <v-row justify="center" no-gutters>
      <v-col class="text-left" cols="6">
        <div class="d-table fill-height">
          <div
            class="d-table-cell grey lighten-4 pa-2 text-center font-weight-medium"
            style="min-width:45px"
          >
            {{ parseInt(item.line_id) + 1 }}
          </div>
          <v-divider class="d-table-cell" vertical></v-divider>
          <div class="d-table-cell pa-2">{{ item.text }}</div>
        </div>
      </v-col>
      <v-col class="text-left" cols="6">
        <div class="d-table fill-height">
          <v-divider class="d-table-cell" vertical></v-divider>
          <div
            class="d-table-cell grey lighten-5 text-center"
            style="min-width:45px"
          >
            <div
              class="fill-height lighten-5 d-flex flex-column justify-space-between"
              :class="{
                green: item.selected.sim > 0.5,
                yellow: (item.selected.sim <= 0.5) && (item.selected.sim > 0.3)
              }"
            >
              <div class="pa-2 font-weight-medium">
                {{ selectedLineId }}
              </div>
              <div class="text-caption pa-1">
                {{ item.selected.sim | numeral("0.00") }}
              </div>
            </div>
          </div>
          <v-divider class="d-table-cell" vertical></v-divider>
          <div class="d-table-cell pa-2">
            {{ item.selected.text }}
            <div v-for="(t,i) in linesTo" :key="i" class="yellow lighten-4">=> {{t.line_id}} [{{t.sim | numeral("0.00")}}] {{ t.text }}</div>
          </div>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import _ from 'lodash'
export default {
  name: "EditItem",
  props: ["item"],
  computed: {
    selectedLineId() {
      return parseInt(this.item.selected.line_id) + 1;
    },
    linesTo() {
      return _.orderBy(this.item.trans, 'line_id')
    }
  }
};
</script>
