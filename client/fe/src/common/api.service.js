import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";
import {
  API_URL
} from "@/common/config";

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
  download(resource, slug = "") {
    return Vue.axios.get(`${resource}/${slug}`, {
      responseType: 'blob'
    }).catch(error => {
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
  list(slug) {
    return ApiService.get("items", slug);
  },
  upload(params) {
    //check filesize
    if (!params.file | (params.file.size > 5 * 1024 * 1024)) {
      alert("File is too big (> 5MB)");
      return;
    }
    let form = new FormData();
    form.append(params.langCode, params.file);
    return ApiService.post("items", params.username, form);
  },
  downloadSplitted(params) {
    return ApiService.get(
      "items",
      `${params.username}/splitted/${params.langCode}/${params.fileId}/download`
    ).then((response) => {
      console.log(response)
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', params.fileName);
      document.body.appendChild(link);
      link.click();
    });
  },
  getSplitted(params) {
    return ApiService.get(
      "items",
      `${params.username}/splitted/${params.langCode}/${params.fileId}/${params.linesCount}/${params.page}`
    );
  },
  getAligned(params) {
    return ApiService.get(
      "items",
      `${params.username}/aligned/${params.langCode}/${params.fileId}/${params.linesCount}`
    );
  },
  getProcessing(params) {
    return ApiService.get(
      "items",
      `${params.username}/processing/${params.fileId}/${params.linesCount}/${params.page}`
    );
  },
  alignSplitted(params) {
    return ApiService.get(
      "items",
      `${params.username}/align/${params.fileIds.ru}/${params.fileIds.zh}`
    );
  }
};