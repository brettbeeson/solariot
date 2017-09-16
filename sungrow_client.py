#!/usr/bin/env python

from pymodbus.client.sync import ModbusTcpClient
import time
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import config

client = ModbusTcpClient(config.inverter_ip, timeout=3, port=502)
client.connect()

slave = 0x01
inverter = {}

modmap = {"5008":  "internal_temp_10",
          "5011":  "pv1_voltage_10",
          "5012":  "pv1_current_10",
          "5013":  "pv2_voltage_10",
          "5014":  "pv1_current_10",
          "5017":  "total_pv_power",
          "5019":  "grid_voltage_10",
          "5022":  "inverter_current_10",
          "5031":  "consumption?",
          "5036":  "grid_frequency_10",
          "13003": "total_pv_energy",
          "13006": "total_export_energy_10",
          "13008": "load_power",
          "13010": "export_power",
          "13011": "grid_import_or_export",
          "13013": "total_charge_energy",
          "13015": "co2_emission_reduction",
          "13018": "total_use_energy",
          "13020": "battery_voltage_10",
          "13022": "battery_power",
          "13023": "battery_level_10",
          "13024": "battery_health_10",
          "13025": "battery_temp_10",
          "13027": "total_discharge_energy_10",
          "13029": "use_power",
          "13034": "pv_power"
         }

def load_registers(start,COUNT=100):
  try:
    rr = client.read_input_registers(start, count=COUNT, unit=slave)
    for num in range(0, COUNT):
      run = start + num + 1
      if modmap.get(str(run)):
        if '_10' in modmap.get(str(run)):
          inverter[modmap.get(str(run))[:-3]] = float(rr.registers[num])/10
        else:
          inverter[modmap.get(str(run))] = rr.registers[num]
  except Exception as err:
    print "[ERROR] %s" % err
  time.sleep(1)

def my_publish_callback(envelope, status):
  print envelope, status

pnconfig = PNConfiguration()
pnconfig.subscribe_key = config.subscribe_key
pnconfig.publish_key = config.publish_key

pubnub = PubNub(pnconfig)

while True:
  try:
    load_registers(5000,100) 
    load_registers(13000,100) 
    # Work out if the grid power is being imported or exported
    if inverter['grid_import_or_export'] == 65535:
      export_power = (65535 - inverter['export_power']) * -1
      inverter['export_power'] = export_power
    print inverter
    pubnub.publish().channel("test_channel").message(inverter).async(my_publish_callback)
    time.sleep(1)
  except Exception as err:
    print "[ERROR] %s" % err
client.close()
