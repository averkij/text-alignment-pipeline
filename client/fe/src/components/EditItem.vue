<template>
    <div>
        <v-row justify="center" no-gutters>
            <v-col class="text-left" cols="6">
                <div class="d-table fill-height">
                    <div class="d-table-cell grey lighten-4 pa-2 text-center" style="min-width:45px">
                        {{ item.line_ids[0] + 1 }}
                    </div>
                    <v-divider class="d-table-cell" vertical></v-divider>
                    <div class="d-table-cell pa-2">{{ item.text }}</div>
                </div>
            </v-col>
            <v-col class="text-left" cols="6">
                <div class="d-table fill-height">
                    <v-divider class="d-table-cell" vertical></v-divider>
                    <div class="d-table-cell grey lighten-5 text-center" style="min-width:45px">
                        <div class="fill-height lighten-5 d-flex flex-column justify-space-between"
                            :class="{green: item.selected.sim>0.5, yellow: item.selected.sim<=0.5 & item.selected.sim>0.3}">
                            <div class="pa-2">
                                {{ selectedLineId }}
                            </div>
                            <div class="text-caption pa-1">{{ item.selected.sim | numeral('0.00') }}</div>
                        </div>
                    </div>
                    <v-divider class="d-table-cell" vertical></v-divider>
                    <div class="d-table-cell pa-2">
                        {{ item.selected.text }}
                        <!-- <span class="yellow lighten-4">{{ item.trans }}</span> -->
                    </div>
                </div>
            </v-col>
        </v-row>
    </div>
</template>

<script>
    export default {
        name: "EditItem",
        props: ['item'],
        computed: {
            selectedLineId() {
                if (this.item.selected.line_ids.length > 0) {
                    return this.item.selected.line_ids[0] + 1;
                }
                return "x"
            }
        }
    }
</script>