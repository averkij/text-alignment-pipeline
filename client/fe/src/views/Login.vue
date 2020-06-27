<template>
  <v-card width="400" class="mx-auto mt-5">
    <v-card-title>Привет, 你好, Szia, Hallo, Ahoj!</v-card-title>
    <v-card-text>
      <v-form>
        <v-text-field label="Username" prepend-icon="mdi-account-circle" />
      </v-form>
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions>
      <!-- <v-btn color="success">Register</v-btn>
          <v-spacer></v-spacer> -->
      <v-btn color="info" v-on:click="say('hi')">Login</v-btn>
    </v-card-actions>
  </v-card>
</template>