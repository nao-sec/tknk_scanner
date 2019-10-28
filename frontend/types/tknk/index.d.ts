export interface Avclass {
  flag: string
  detects: Detect[]
}

export interface Connection {
  remote_address: string
  remote_port: number
  state: string
  pid: number
  process_name: string
  path: string
}

export interface Detect {
  family_name: string
  count: number
}

export interface DumpedFilesSanReport {
  detect_rules: string[]
  file_name: string
  size: string
  magic: string
}

export interface Job {
  config: JobConf
  id: string
}

export interface JobConf {
  target_file: string
  mode: string
  time: number
  timestamp: number
}

export interface Jobs {
  current_job: Job | null
  queued_jobs: Job[]
}

export interface Meta {
  uuid: string
  timestamp: string
  setting: Setting
  is_dumped: boolean
  is_matched: boolean
  comment: string
  plugins: PluginsConf
}

export interface Plugins {
  avclass: Avclass
  suricata: SuricataEvent[]
  die: string
}

export interface PluginsConf {
  avclass: boolean
  die: boolean
  suricata: boolean
}

export interface Report {
  meta: Meta
  result: Result
}

export interface ReportResponse {
  status_code: number
  report: Report | null
}

export interface Result {
  dumped_files_scan: DumpedFilesSanReport[]
  upload_file_scan: UploadedFleScanReport
  plugins: Plugins
  connections: Connection[]
}

export interface Setting {
  mode: string
  runt_time: number
}

export interface SuricataAlert {
  category: string
  signature: string
  signature_id: number
}

export interface SuricataEvent {
  event_type: string
  timestamp: string
  alert: SuricataAlert
  proto: string
  dest_ip: string
  dest_port: number
  src_ip: string
  src_port: number
  http?: SuricataHttp
}

export interface SuricataHttp {
  hostname: string
  http_method: string
  http_user_agent: string
  length: string
  protocol: string
  url: string
}

export interface UploadedFleScanReport {
  md5: string
  sha1: string
  sha256: string
  detect_rules: string[]
  file_name: string
  size: string
  magic: string
}
