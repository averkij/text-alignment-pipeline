<template>
  <div>
    <v-row justify="center" no-gutters>
      <v-col class="text-left" cols="6">
        <div class="d-table fill-height">
          <div class="d-table-cell grey lighten-5 pa-2 text-center font-weight-medium" style="min-width:45px">
            {{ parseInt(item.line_id) + 1 }}
          </div>
          <v-divider class="d-table-cell" vertical></v-divider>
          <div class="d-table-cell pa-2">{{ item.text }}</div>
        </div>
      </v-col>
      <v-col class="text-left" cols="6">
        <div class="d-table fill-height fill-width">
          <v-divider class="d-table-cell" vertical></v-divider>
          <div class="d-table-cell lighten-5 text-center" style="min-width:45px" :class="{
                grey: item.selected.sim <= 0.3,
                green: item.selected.sim > 0.5,
                yellow: (item.selected.sim <= 0.5) && (item.selected.sim > 0.3)
              }">
            <div class="fill-height lighten-5 d-flex flex-column justify-space-between">
              <div class="pa-2 font-weight-medium">
                {{ selectedLineId }}
              </div>
              <div class="text-caption pa-1">
                {{ item.selected.sim | numeral("0.00") }}
              </div>
            </div>
          </div>
          <v-divider class="d-table-cell" vertical></v-divider>

          <div class="d-table-cell" style="width:100%">
            <v-expansion-panels flat accordion>
              <v-expansion-panel>
                <v-expansion-panel-header>{{ item.selected.text }}</v-expansion-panel-header>
                <v-expansion-panel-content>
                  <div v-for="(t,i) in linesTo" :key="i">
                    <v-divider></v-divider>
                    <div class="d-table">
                      <div class="d-table-cell lighten-5 pa-2 text-center font-weight-medium" style="min-width:45px"
                        :class="[{green: t.line_id==item.selected.line_id}, {grey: t.line_id!=item.selected.line_id}]">
                        {{ t.line_id + 1 }}
                      </div>
                      <v-divider class="d-table-cell" vertical></v-divider>
                      <div class="d-table-cell pa-2">{{ t.text }}</div>
                    </div>
                  </div>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
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
        let sid = this.item.selected.line_id;
        let wnd = 3;
        return _(this.item.trans)
          .filter(function (tr) {
            return tr.line_id < sid + wnd && tr.line_id > sid - wnd
          })
          .orderBy('line_id');
      }
    }
  };
</script>