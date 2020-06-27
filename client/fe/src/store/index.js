import Vue from "vue";
import Vuex from "vuex";

import auth from "./auth.module" 
import upload from "./upload.module" 

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth,
    upload
  }
});
