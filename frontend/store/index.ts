import { getAccessorType, actionTree, mutationTree } from "nuxt-typed-vuex"
import { Jobs, Job } from "~/types/tknk"

export const state = () => ({
  currentJobs: { current_job: null, queued_jobs: [] } as Jobs,
  finishedJobs: [] as Job[],
  isPausedFetchJobs: false as boolean,
})

export const mutations = mutationTree(state, {
  setCurrentJobs(state, newJobs: Jobs) {
    state.currentJobs = newJobs
  },
  jobFinish(state, finishedJob: Job) {
    state.finishedJobs.push(finishedJob)
  },
  pauseFetchJobs(state) {
    state.isPausedFetchJobs = true
  },
  resumeFetchJobs(state) {
    state.isPausedFetchJobs = false
  },
})

export const actions = actionTree(
  { state, mutations },
  {
    async fetchJobs({ commit }) {
      const jobs: Jobs = await this.$axios.$get("/jobs").catch(() => {
        commit("pauseFetchJobs")
      })
      commit("setCurrentJobs", jobs)
    },
    async registerFetchJobsWorker({ state }) {
      await this.app.$accessor.fetchJobs
      if (state.currentJobs.current_job !== null) {
        setInterval(() => {
          this.app.$accessor.registerFetchJobsWorker()
        }, 5000)
      } else {
        setInterval(() => {
          this.app.$accessor.registerFetchJobsWorker()
        }, 10000)
      }
    },
  },
)

export const accessorType = getAccessorType({
  state,
  mutations,
  actions,
})
