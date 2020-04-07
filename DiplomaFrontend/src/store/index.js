//Скрипт лежит просто для примера кода, уже не работает

import Vue from 'vue'
import Vuex from 'vuex'
import { Foundation } from '../api/foundations'
import {
    ADD_FOUNDATION,
    REMOVE_FOUNDATION,
    SET_FOUNDATION
} from './mutation-types'

Vue.use(Vuex)

const state = {
    foundations: [] //список
}

//геттеры типа
const getters = {
    foundations: state => state.foundations
}

const mutations = {
    [ADD_FOUNDATION](state, foundation) {
        state.foundations = [foundation, ...state.foundations]
    },
    [REMOVE_FOUNDATION](state,{ id }) {
        state.foundations = state.foundations.filter(foundation => {
            return foundation.id !== id
        })
    },
    [SET_FOUNDATION](state, { foundations }) {
        state.foundations = foundations
    }
}

const actions = {
    createFoundation ({ commit }, foundationData) {
        Foundation.create(foundationData).then(foundation => {
            commit(ADD_FOUNDATION, foundation)
        })
    },
    deleteFoundation({ commit }, foundation) {
        Foundation.delete(foundation).then(response => {
            commit(REMOVE_FOUNDATION, foundation)
        })
    },
    getFoundations({ commit }) {
        Foundation.list().then(foundations => {
            commit(SET_FOUNDATION, { foundations })
        })
    }
}

export default new Vuex.Store({
    state,
    getters,
    actions,
    mutations
})