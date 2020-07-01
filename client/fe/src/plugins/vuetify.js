import '@mdi/font/css/materialdesignicons.css'
import Vue from "vue";
import Vuetify from "vuetify/lib";

Vue.use(Vuetify);

export default new Vuetify({
    icons: {
        iconfont: 'mdi'
    } 
});

// npm install @mdi/font -D
// npm install @mdi/js -D
