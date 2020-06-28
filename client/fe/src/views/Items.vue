<template>
    <v-card width="400" height="400" class="mx-auto mt-5">Hi, {{username}}

        <div v-for="item in items.ru" :key="item">
            {{item}}
        </div>

        <div v-for="item in items.zh" :key="item">
            {{item}}
        </div>

    </v-card>

</template>

<script>
    import {
        mapGetters
    } from "vuex";

    import {
        FETCH_ITEMS
    } from "@/store/actions.type";

    export default {
        mounted() {
            this.$store.dispatch(FETCH_ITEMS, this.$route.params.username);
        },
        computed: {
            ...mapGetters(["items"]),
            username() {
                return this.$route.params.username
            }
        }
    }
</script>