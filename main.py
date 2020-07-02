import gspread
from oauth2client.service_account import ServiceAccountCredentials
import glob
import csv
import os
from loguru import logger
from datetime import datetime


class ExportToSheet:
    def __init__(self, spreadsheet_id):
        # use creds to create a client to interact with the Google Drive API
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "client_secret.json", scope
        )
        self.client = gspread.authorize(creds)
        self.spreadsheet_id = spreadsheet_id

    # export single csvfile to a spreadsheet
    def export_single_csv(self, csvfile):
        try:
            logger.info(f"Exporting single file to first sheet of google spreadsheet!!")
            sh = self.client.open_by_key(self.spreadsheet_id)
            file_name = csvfile.split("/")[-1].split(".")[0]
            f_name = file_name + "_" + str(datetime.date(datetime.now()))
            sheetName = sh.add_worksheet(title=f_name, rows="1000", cols="50")
            sh.values_update(
                sheetName.title,
                params={"valueInputOption": "USER_ENTERED"},
                body={"values": list(csv.reader(open(csvfile)))},
            )
        except Exception as e:
            logger.error(f"Error: Exception {e} occurred!")
            pass

    # export multiple csvfiles to different worksheets
    def export_multiple_csv(self, files):
        logger.info(f"Exporting all files to different worksheet of same spreadsheet!!")
        for file in files:
            self.export_single_csv(file)


def main():
    spreadsheet_id = "1TvZHFhFDA9-l0DogBm825rbN8ZBlOealqhFTxvD3cAk"
    files = glob.glob(f"{os.getcwd()}/csvfiles/*.csv")
    obj = ExportToSheet(spreadsheet_id)
    obj.export_single_csv(files[0])
    obj.export_multiple_csv(files)
    logger.success("DONE")


if __name__ == "__main__":
    main()
