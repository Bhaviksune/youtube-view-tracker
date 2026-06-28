import os

credentials = os.getenv("GOOGLE_CREDENTIALS")

with open("credentials.json", "w", encoding="utf-8") as f:
    f.write(credentials)

from modules.tracker import collect_data

collect_data()