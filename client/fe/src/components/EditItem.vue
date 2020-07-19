<template>
    <div>

        <v-row justify="center" no-gutters>
            <v-col class="text-left" cols="6">
                <div class="d-table fill-height">
                    <div class="d-table-cell grey lighten-4 pa-2 text-center" style="min-width:45px">
                        {{ item.line_ids[0] + 1 }}
                    </div>
                    <div class="d-table-cell pa-2">{{ item.text }}</div>
                </div>
            </v-col>
            <v-col class="text-left" cols="6">
                <div class="d-table fill-height">
                    <div class="d-table-cell grey lighten-4 text-center" style="min-width:45px">
                        <div class="fill-height lighten-4 d-flex flex-column justify-space-between"
                            :class="{green: item.selected.sim>0.5}">
                            <div class="pa-2">{{ item.selected.line_ids[0] + 1 }}</div>
                            <div class="text-caption pa-1">{{ item.selected.sim | numeral('0.00') }}</div>
                        </div>
                    </div>
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
        props: ['item']
    }
</script>