<template>
    <div>
        <v-row justify="center" no-gutters>
            <v-col class="text-left" cols="6">
                <div class="d-table fill-height">
                    <div class="d-table-cell grey lighten-4 pa-2">{{ item.line_ids[0] }}</div>
                    <div class="d-table-cell pa-2">{{ item.text }}</div>
                </div>
            </v-col>
            <v-col class="text-left" cols="6">
                <div class="d-table fill-height">
                    <div class="d-table-cell grey lighten-4 pa-2">{{ item.trans[0].line_ids[0] }}</div>
                    <div class="d-table-cell pa-2">{{ item.trans[0].text }}</div>
                </div>
            </v-col>
        </v-row>
    </div>
</template>

<script>
    export default {
        name: "PreviewItem",
        props: ['item']
    }
</script>