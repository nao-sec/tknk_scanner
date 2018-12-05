export const state = () => ({
  current: null,
  finished: [],
  queued: []
});

export const mutations = {
  push_queued_jobs(state, jobs) {
    jobs.sort((a, b) => {return a.timestamp - b.timestamp;});
    state.queued = jobs;
  },
  change_current(state, new_current_jobs) {
    // stop unnecessary changing
    if ((state.current === null && new_current_jobs === null) || (new_current_jobs !== null && state.current !== null && new_current_jobs.id === state.current.id)) return null;

    if (state.current !== null) state.finished.push(state.current);
    state.current = new_current_jobs;
  }
};
