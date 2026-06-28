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


def get_last_row(sheet):
    rows = sheet.get_all_values()

    if len(rows) <= 1:
        return None

    return rows[-1]


def append_row(sheet, row):
    sheet.append_row(
        row,
        value_input_option="USER_ENTERED"
    )

    print("Row Added")