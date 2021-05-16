import nicehash
import pygsheets
import datetime
import json

gc = pygsheets.authorize(service_file='config/google-sa.json')

with open("config/nicehash.json") as f:
  nh_config = json.load(f)

def write_to_gsheet(row_values):
    sheet = gc.open(nh_config["googleSheetName"])
    worksheet_name = "Balance"
    try:
        wks = sheet.worksheet_by_title(worksheet_name)
    except pygsheets.exceptions.WorksheetNotFound:
        wks = sheet.add_worksheet(worksheet_name)
    cells = wks.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
    last_row = len(cells)
    if last_row == 1:
        wks.update_row(1, values=["Date", "BTC balance"])
    wks.insert_rows(last_row, number=1, values=row_values)

nh_private_api = nicehash.private_api(nh_config["host"], nh_config["organisationId"], nh_config["key"], nh_config["secret"])

now_date_str = '{date:%Y-%m-%d}'.format(date=datetime.datetime.now())
print(now_date_str + ": Starting nicehash info collection...")
account = nh_private_api.get_accounts_for_currency("BTC")
btc_available = account["available"]
print("Writing to the Google Sheets: " + str(btc_available))
write_to_gsheet([now_date_str, btc_available])
