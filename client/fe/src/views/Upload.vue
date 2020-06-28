<template>
    <v-card width="400" height="400" class="mx-auto mt-5">Hi, {{username}}</v-card>

</template>

<script>
export default {
    computed: {
        username() {
            return this.$route.params.username
        }
    }
}
</script>