import gspread
from oauth2client.service_account import ServiceAccountCredentials
import glob
import csv
import os
from loguru import logger
from datetime import datetime

# use creds to create a client to interact with the Google Drive API
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
client = gspread.authorize(creds)

# export single csvfile to a spreadsheet
def export_single_csv(s_id, csvfile):
    content = open(csvfile, "r").read()
    client.import_csv(s_id, content)


# export multiple csvfiles to different worksheets
def export_multiple_csv(s_id, files):
    sh = client.open_by_key(s_id)
    for file in files:
        file_name = file.split("/")[-1].split(".")[0]
        f_name = file_name + "_" + str(datetime.date(datetime.now()))
        sheetName = sh.add_worksheet(title=f_name, rows="1000", cols="50")
        sh.values_update(
            sheetName.title,
            params={"valueInputOption": "USER_ENTERED"},
            body={"values": list(csv.reader(open(file)))},
        )


def main():
    spreadsheet_id = "1TvZHFhFDA9-l0DogBm825rbN8ZBlOealqhFTxvD3cAk"
    files = glob.glob(f"{os.getcwd()}/csvfiles/*.csv")
    logger.info(f"Exporting first file to first sheet of google spreadsheet!!")
    export_single_csv(spreadsheet_id, files[0])
    logger.info(f"Exporting all files to different worksheet of same spreadsheet!!")
    export_multiple_csv(spreadsheet_id, files)
    logger.success("DONE")


if __name__ == "__main__":
    main()
