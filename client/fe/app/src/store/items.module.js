import {
  ItemsService
} from "@/common/api.service";

import {
  FETCH_ITEMS,
  FETCH_ITEMS_PROCESSING,
  UPLOAD_FILES,
  DOWNLOAD_SPLITTED,
  DOWNLOAD_PROCESSING,
  GET_SPLITTED,
  GET_PROCESSING,
  GET_ALIGNED,
  ALIGN_SPLITTED
} from "./actions.type";

import {
  SET_ITEMS,
  SET_ITEMS_PROCESSING,
  SET_SPLITTED,
  SET_PROCESSING,
  SET_ALIGNED
} from "./mutations.type";

const initialState = {
  items: {
    ru: [],
    zh: []
  },
  itemsProcessing: {
    ru: [],
    zh: []
  },
  splitted: {
    ru: {
      lines: [],
      meta: {}
    },
    zh: {
      lines: [],
      meta: {}
    }
  },
  processing: {
    items: [],
    meta: {}
  },
  aligned: {
    ru: [],
    zh: []
  }
};

export const state = {
  ...initialState
};

export const actions = {
  async [FETCH_ITEMS](context, params) {
    const {
      data
    } = await ItemsService.fetchItems(params);
    context.commit(SET_ITEMS, {
      items: data.items,
      langCode: params.langCode
    });
    return data;
  },
  async [FETCH_ITEMS_PROCESSING](context, params) {
    const {
      data
    } = await ItemsService.fetchItemsProcessing(params);
    context.commit(SET_ITEMS_PROCESSING, {
      items: data.items,
      langCode: params.langCode
    });
    return data;
  },
  // params {file, username, langCode}
  async [UPLOAD_FILES](context, params) {
    await ItemsService.upload(params);
    await context.dispatch(FETCH_ITEMS, params.username);
    return;
  },
  // params {fileId, username, langCode, fileName}
  async [DOWNLOAD_SPLITTED](context, params) {
    await ItemsService.downloadSplitted(params);
    return;
  },
  // params {fileId, username, langCode, fileName}
  async [DOWNLOAD_PROCESSING](context, params) {
    await ItemsService.downloadProcessing(params);
    return;
  },
  // params {fileId, username, langCode, count, page}
  async [GET_SPLITTED](context, params) {
    const {
      data
    } = await ItemsService.getSplitted(params);
    context.commit(SET_SPLITTED, data);
    return;
  },
  // params {fileId, username}
  async [GET_PROCESSING](context, params) {
    await ItemsService.getProcessing(params).then(
      function (response) {
        context.commit(SET_PROCESSING, response.data);
      },
      function () {
        console.log(`Didn't find processing document.`);
      }
    );
    return;
  },
  async [ALIGN_SPLITTED](context, params) {
    const {
      data
    } = await ItemsService.alignSplitted(params);
    context.commit(SET_ALIGNED, data.items);
    return;
  },
  async [GET_ALIGNED](context, params) {
    const {
      data
    } = await ItemsService.getAligned(params);
    context.commit(SET_ALIGNED, data.items);
    return;
  }
};

export const mutations = {
  [SET_ITEMS](state, params) {
    state.items[params.langCode] = params.items[params.langCode];
  },
  [SET_ITEMS_PROCESSING](state, params) {
    state.itemsProcessing[params.langCode] = params.items[params.langCode];
  },
  [SET_SPLITTED](state, data) {
    if (data.items.ru) {
      state.splitted.ru.lines = data.items.ru;
    }
    if (data.items.zh) {
      state.splitted.zh.lines = data.items.zh;
    }
    if (data.meta.ru) {
      state.splitted.ru.meta = data.meta.ru;
    }
    if (data.meta.zh) {
      state.splitted.zh.meta = data.meta.zh;
    }
  },
  [SET_PROCESSING](state, data) {
    state.processing = data;
  },
  [SET_ALIGNED](state, items) {
    if (items.ru) {
      state.aligned.ru = items.ru;
    }
    if (items.zh) {
      state.aligned.zh = items.zh;
    }
  }
};

const getters = {
  items(state) {
    return state.items;
  },
  itemsProcessing(state) {
    return state.itemsProcessing;
  },
  splitted(state) {
    return state.splitted;
  },
  processing(state) {
    return state.processing;
  },
  aligned(state) {
    return state.aligned;
  }
};

export default {
  state,
  actions,
  mutations,
  getters
};