import nicehash
import pygsheets
import datetime
import json

gc = pygsheets.authorize(service_file='config/google-sa.json')

with open("config/nicehash.json") as f:
  nh_config = json.load(f)

def get_gpu_temperature(encoded_temperature):
    # See https://github.com/nicehash/NiceHashQuickMiner/issues/146
    return encoded_temperature % 65536

def write_to_gsheet(rig_id, rig_name, device_id, device_name, row_values):
    sheet = gc.open(nh_config["googleSheetName"])
    worksheet_name = rig_name + "[" + rig_id + "]" + " - " + device_name + "[" + device_id + "]"
    try:
        wks = sheet.worksheet_by_title(worksheet_name)
    except pygsheets.exceptions.WorksheetNotFound:
        wks = sheet.add_worksheet(worksheet_name)
    cells = wks.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
    last_row = len(cells)
    if last_row == 1:
        wks.update_row(1, values=["Time", "GPU temperature, ℃", "Power useage, Watt", "Fan speed, percentage"])
    wks.insert_rows(last_row, number=1, values=row_values)

nh_private_api = nicehash.private_api(nh_config["host"], nh_config["organisationId"], nh_config["key"], nh_config["secret"])

now_str = '{date:%Y-%m-%d %H:%M:%S}'.format(date=datetime.datetime.now())
print(now_str + ": Starting nicehash info collection...")
rigs_info = nh_private_api.get_rigs()
rigs = rigs_info["miningRigs"]
for rig in rigs:
    rig_id = rig["rigId"]
    rig_name = rig["name"]
    rig_status = rig["minerStatus"]
    if rig_status != "MINING":
        print("Skipping rig " + rig_id + " - " + rig_name + " [" + rig_status + "]")
        continue
    print("Gathering information about rig " + rig_id + " - " + rig_name + " [" + rig_status + "]")
    for device in rig["devices"]:
        device_name = device["name"]
        device_id = device["id"]
        device_status = device["status"]["enumName"]
        if device_status != "MINING":
            print("Skipping device " + device_id + " - " + device_name + " [" + device_status + "]")
            continue
        print("Gathering information about device " + device_id + " - " + device_name + " [" + device_status + "]")
        gpu_temperature = get_gpu_temperature(device["temperature"])
        powerUsage = device["powerUsage"]
        fan_percentage = device["revolutionsPerMinutePercentage"]
        row_values = [now_str, gpu_temperature, powerUsage, fan_percentage]
        print("Writing to the Google Sheets: " + str(row_values))
        write_to_gsheet(rig_id, rig_name, device_id, device_name, row_values)

print("Finished")
