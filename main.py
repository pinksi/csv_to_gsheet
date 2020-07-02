import gspread
from oauth2client.service_account import ServiceAccountCredentials
import glob
import csv
import os


# use creds to create a client to interact with the Google Drive API
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
client = gspread.authorize(creds)

# export single csvfile to a spreadsheet
spreadsheet_id = "1TvZHFhFDA9-l0DogBm825rbN8ZBlOealqhFTxvD3cAk"
# content = open("test.csv", "r").read()
# client.import_csv(spreadsheet_id, content)

# export multiple csvfiles to different worksheets
sh = client.open_by_key(spreadsheet_id)
files = glob.glob(f"{os.getcwd()}/csvfiles/*.csv")
for i, file in enumerate(files):
    file_name = file.split("/")[-1].split(".")[0]
    sheetName = sh.add_worksheet(title=file_name, rows="1000", cols="50")
    sh.values_update(
        sheetName.title,
        params={"valueInputOption": "USER_ENTERED"},
        body={"values": list(csv.reader(open(file)))},
    )

