import nicehash
import datetime
import json
from newrelic import push_metric


with open("config/nicehash.json") as f:
    nh_config = json.load(f)


def get_gpu_temperature(encoded_temperature):
    # See https://github.com/nicehash/NiceHashQuickMiner/issues/146
    return encoded_temperature % 65536

nh_private_api = nicehash.private_api(
    nh_config["host"], nh_config["organisationId"], nh_config["key"], nh_config["secret"])

now_str = '{date:%Y-%m-%d %H:%M:%S}'.format(date=datetime.datetime.now())
print(now_str + ": Starting nicehash metrics collection...")
devices_mining = 0
rigs_mining = 0
rigs_info = nh_private_api.get_rigs()

print(json.dumps(rigs_info))

rigs = rigs_info["miningRigs"]
for rig in rigs:
    rig_id = rig["rigId"]
    rig_name = rig["name"]
    rig_status = rig["minerStatus"]
    if rig_status != "MINING":
        print("Skipping rig " + rig_id + " - " +
              rig_name + " [" + rig_status + "]")
        continue
    rigs_mining = rigs_mining + 1
    print("Gathering information about rig " + rig_id +
          " - " + rig_name + " [" + rig_status + "]")
    for device in rig["devices"]:
        device_name = device["name"]
        device_id = device["id"]
        device_status = device["status"]["enumName"]
        if device_status != "MINING":
            print("Skipping device " + device_id + " - " +
                  device_name + " [" + device_status + "]")
            continue
        devices_mining = devices_mining + 1
        print("Gathering information about device " + device_id +
              " - " + device_name + " [" + device_status + "]")
        gpu_temperature = get_gpu_temperature(device["temperature"])
        power_usage = device["powerUsage"]
        fan_percentage = device["revolutionsPerMinutePercentage"]
        print("Recording metrics ...")
        
        device1_speed = 0
        device_speeds = device["speeds"]
        if (len(device_speeds)) > 0:
            device1_speed = float(device_speeds[1]["speed"])

        push_metric("nicehash.gpu_temperature", gpu_temperature, {"rigId": rig_id, "deviceId": device_id}, nh_config["newrelicInsertApiKey"])
        push_metric("nicehash.power_usage", power_usage, {"rigId": rig_id, "deviceId": device_id}, nh_config["newrelicInsertApiKey"])
        push_metric("nicehash.fan_percentage", fan_percentage, {"rigId": rig_id, "deviceId": device_id}, nh_config["newrelicInsertApiKey"])
        push_metric("nicehash.speed", device1_speed, {"rigId": rig_id, "deviceId": device_id}, nh_config["newrelicInsertApiKey"])

push_metric("nicehash.device.mining", devices_mining, {}, nh_config["newrelicInsertApiKey"])
push_metric("nicehash.rig.mining", rigs_mining, {} , nh_config["newrelicInsertApiKey"])

print("Finished")
