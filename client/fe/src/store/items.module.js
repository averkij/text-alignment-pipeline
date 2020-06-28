import {
    ItemsService
} from "@/common/api.service"

import {
    FETCH_ITEMS
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
    async [FETCH_ITEMS](context, itemsSlug) {
        const {
            data
        } = await ItemsService.get(itemsSlug);
        context.commit(SET_ITEMS, data.items);
        return data;
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