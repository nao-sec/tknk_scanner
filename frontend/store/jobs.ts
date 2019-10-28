export const state = () => ({
  current: null,
  finished: [],
  queued: [],
})

export const mutations = {
  push_queued_jobs(state, jobs) {
    jobs.sort((a, b) => {
      return a.timestamp - b.timestamp
    })
    state.queued = jobs
  },
  change_current(state, newCurrentJobs) {
    // stop unnecessary changing
    if ((state.current === null && newCurrentJobs === null) || (newCurrentJobs !== null && state.current !== null && newCurrentJobs.id === state.current.id)) {
      return null
    }

    if (state.current !== null) state.finished.push(state.current)
    state.current = newCurrentJobs
  },
}
