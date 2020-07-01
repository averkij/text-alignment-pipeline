import {
    ItemsService
} from "@/common/api.service"

import {
    FETCH_ITEMS,
    UPLOAD_FILES
} from "./actions.type"

import {
    SET_ITEMS
} from "./mutations.type"

const initialState = {
    items: {
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
        } = await ItemsService.get(username);
        context.commit(SET_ITEMS, data.items);
        return data;
    },
    // params {file, username, langCode}
    async [UPLOAD_FILES](context, params) {
        await ItemsService.upload(params);
        context.dispatch(FETCH_ITEMS, params.username);
        return;
    }
}

export const mutations = {
    [SET_ITEMS](state, items) {
        state.items = items;
    }
}

const getters = {
    items(state) {
        return state.items;
    }
}

export default {
    state,
    actions,
    mutations,
    getters
}