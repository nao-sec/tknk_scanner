interface SuricataEvent {
  event_type: string
  timestamp: string
  alert: SuricataAlert
  proto: string
  dest_ip: string
  dest_port: number
  src_ip: string
  src_port: number
  http: SuricataHttp | null
}
