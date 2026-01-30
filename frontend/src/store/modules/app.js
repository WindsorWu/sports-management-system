export default {
  namespaced: true,
  state: {
    sidebar: {
      opened: localStorage.getItem('sidebarStatus') ? !!+localStorage.getItem('sidebarStatus') : true
    },
    device: 'desktop',
    loading: false
  },
  mutations: {
    TOGGLE_SIDEBAR(state) {
      state.sidebar.opened = !state.sidebar.opened
      if (state.sidebar.opened) {
        localStorage.setItem('sidebarStatus', '1')
      } else {
        localStorage.setItem('sidebarStatus', '0')
      }
    },
    CLOSE_SIDEBAR(state) {
      state.sidebar.opened = false
      localStorage.setItem('sidebarStatus', '0')
    },
    TOGGLE_DEVICE(state, device) {
      state.device = device
    },
    SET_LOADING(state, loading) {
      state.loading = loading
    }
  },
  actions: {
    toggleSideBar({ commit }) {
      commit('TOGGLE_SIDEBAR')
    },
    closeSideBar({ commit }) {
      commit('CLOSE_SIDEBAR')
    },
    toggleDevice({ commit }, device) {
      commit('TOGGLE_DEVICE', device)
    },
    setLoading({ commit }, loading) {
      commit('SET_LOADING', loading)
    }
  }
}
