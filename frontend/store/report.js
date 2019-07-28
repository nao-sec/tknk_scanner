export const state = () => ({
  uuid: null,
  mode: null,
  result: null,
  run_time: null,
  scans: null,
  timestamp: null,
  status_code: null,
  target_scan: null,
  avclass: null,
  die: null,
})

export const getters = {
  is_in_vt(state) {
    return state.avclass === null ? false : state.avclass.flag
  },
  sha256(state) {
    return state.target_scan === null ? null : state.target_scan.sha256
  },
  file_name(state) {
    return state.target_scan === null ? null : state.target_scan.file_name
  },
  detects_summary(state) {
    return [
      {
        AVClass: state.avclass,
        "DIE Indicators": state.die,
        detect_rules:
          state.target_scan === null ? null : state.target_scan.detect_rule,
      },
    ]
  },
  scan_summary(state) {
    return [
      {
        mode: state.mode,
        detail: state.result === null ? "" : state.result.detail,
        running_time: state.run_time,
        timestamp: state.timestamp,
        uuid: state.uuid,
      },
    ]
  },
  file_summary(state) {
    if (state.target_scan === null) {
      return [
        {
          file_name: null,
          size: null,
          magic: null,
          md5: null,
          sha1: null,
          sha256: null,
        },
      ]
    } else {
      return [
        {
          file_name: state.target_scan.file_name,
          size: state.target_scan.size,
          magic: state.magic,
          md5: state.target_scan.md5,
          sha1: state.target_scan.sha1,
          sha256: state.target_scan.sha256,
        },
      ]
    }
  },
}

export const mutations = {
  set_result(state, d) {
    state.uuid = d.report.UUID
    state.mode = d.report.mode
    state.result = d.report.result
    state.run_time = d.report.run_time
    state.scans = d.report.scans
    state.timestamp = d.report.timestamp
    state.status_code = d.status_code
    state.target_scan = d.report.target_scan
    state.avclass = d.report.avclass
    state.die = d.report.die
    state.magic = d.report.magic
  },
  destoroy(state) {
    state.uuid = null
    state.mode = null
    state.result = null
    state.run_time = null
    state.scans = null
    state.timestamp = null
    state.status_code = null
    state.target_scan = null
    state.avclass = null
    state.die = null
    state.magic = null
  },
}
