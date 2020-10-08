inverter_ip = "192.168.0.4"
inverter_port = 502
device="arens"
# Slave Defaults
# Sungrow: 0x01
# SMA: 3
slave = 0x01
model = "sungrow-sh5k"
timeout = 3
scan_interval = 10
# Optional:
#dweepy_uuid = "random-uuid"
# Optional:
influxdb_ip = ""
influxdb_port = 8086
influxdb_user = ""
influxdb_password = ""
influxdb_database = ""
influxdb_ssl = False # True
influxdb_verify_ssl = False
# Optional
#mqtt_server = "192.168.1.128"
#mqtt_port = 1883
#mqtt_topic = "inverter/stats"
