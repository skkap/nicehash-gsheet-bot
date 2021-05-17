import nicehash
import datetime
import json


with open("config/nicehash.json") as f:
  nh_config = json.load(f)

nh_private_api = nicehash.private_api(nh_config["host"], nh_config["organisationId"], nh_config["key"], nh_config["secret"])

rigs_info = nh_private_api.get_rigs()
rigs = rigs_info["miningRigs"]
for rig in rigs:
    print(rig["rigId"] + " - " + rig["name"] + " [" + rig["minerStatus"] + "]")
    for device in rig["devices"]:
        status = device["status"]
        print(" ->  " + device["id"] + " - " + device["name"] + " (" + status["enumName"] + ")")
