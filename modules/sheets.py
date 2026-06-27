import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SERVICE_ACCOUNT_FILE = "credentials.json"


def connect_sheet(spreadsheet_id):
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )

    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key(spreadsheet_id)

    return spreadsheet.sheet1

def append_row(sheet, row):

    all_rows = sheet.get_all_values()

    if len(all_rows) > 1:
        last = all_rows[-1]

        if (
            last[1] == row[1] and
            last[4] == row[4]
        ):
            print("Duplicate Skipped")
            return

    sheet.append_row(
        row,
        value_input_option="USER_ENTERED"
    )

    print("Row Added")