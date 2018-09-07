export const state = () => ({
  uuid: null,
  mode: null,
  result: null,
  run_time: null,
  scans: null,
  timestamp: null,
  status_code: null
});

export const mutations = {
  set_result(state, d) {
    state.uuid = d.result.uuid;
    state.mode = d.result.mode;
    state.result = d.result.result;
    state.run_time = d.result.run_time;
    state.scans = d.result.scans;
    state.timestamp = d.result.timestamp;
    state.status_code = d.status_code;
  },
  destoroy(state) {
    state.uuid = null;
    state.mode = null;
    state.result = null;
    state.run_time = null;
    state.scans = null;
    state.timestamp = null;
    state.status_code = null;
  }
};
