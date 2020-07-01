import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
import { API_URL } from "@/common/config";

const ApiService = {
    init() {
      Vue.use(VueAxios, axios);
      Vue.axios.defaults.baseURL = API_URL;
    },
  
    query(resource, params) {
      return Vue.axios.get(resource, params).catch(error => {
        throw new Error(`[TAP] ApiService ${error}`);
      });
    },
  
    get(resource, slug = "") {
      return Vue.axios.get(`${resource}/${slug}`).catch(error => {
        throw new Error(`[TAP] ApiService ${error}`);
      });
    },
  
    post(resource, slug, params) {
      return Vue.axios.post(`${resource}/${slug}`, params);
    },
  
    update(resource, slug, params) {
      return Vue.axios.put(`${resource}/${slug}`, params);
    },
  
    put(resource, params) {
      return Vue.axios.put(`${resource}`, params);
    },
  
    delete(resource) {
      return Vue.axios.delete(resource).catch(error => {
        throw new Error(`[TAP] ApiService ${error}`);
      });
    }
  };
  
  export default ApiService;

  export const ItemsService = {
      get(slug) {
          return ApiService.get("items", slug);
      },
      upload(params) {
        let form = new FormData()
        form.append(params.langCode, params.file)
        return ApiService.post("items", params.username, form);
      }
  }