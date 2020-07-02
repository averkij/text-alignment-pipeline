import {
    ItemsService
} from "@/common/api.service"

import {
    FETCH_ITEMS,
    UPLOAD_FILES,
    GET_SPLITTED
} from "./actions.type"

import {
    SET_ITEMS,
    SET_SPLITTED
} from "./mutations.type"

const initialState = {
    items: {
        ru: [],
        zh: []
    },
    splitted: {
        ru: [],
        zh: []
    }
}

export const state = {
    ...initialState
};

export const actions = {
    async [FETCH_ITEMS](context, username) {
        const {
            data
        } = await ItemsService.list(username);
        context.commit(SET_ITEMS, data.items);
        return data;
    },
    // params {file, username, langCode}
    async [UPLOAD_FILES](context, params) {
        await ItemsService.upload(params);
        context.dispatch(FETCH_ITEMS, params.username);
        return;
    },
    // params {fileId, username, langCode, lines}
    async [GET_SPLITTED](context, params) {
        const {
            data
        } = await ItemsService.getSplitted(params)
        context.commit(SET_SPLITTED, data.items)
    }
}

export const mutations = {
    [SET_ITEMS](state, items) {
        state.items = items;
    },
    [SET_SPLITTED](state, items) {
        if (items.ru) {
            state.splitted.ru = items.ru
        }
        if (items.zh) {
            state.splitted.zh = items.zh
        }
    }
}

const getters = {
    items(state) {
        return state.items;
    },
    splitted(state) {
        return state.splitted;
    }
}

export default {
    state,
    actions,
    mutations,
    getters
}