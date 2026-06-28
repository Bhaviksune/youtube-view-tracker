import os
from datetime import datetime, timezone

from dotenv import load_dotenv

from modules.youtube import (
    get_channel_id,
    get_latest_video_info
)

from modules.sheets import (
    connect_sheet,
    append_row,
    get_last_row
)

load_dotenv()


def calculate_minutes(published_at):
    published = datetime.strptime(
        published_at,
        "%Y-%m-%dT%H:%M:%SZ"
    ).replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)

    minutes = int((now - published).total_seconds() / 60)

    return max(minutes, 0)


def calculate_hour_decimal(minutes):
    return round(minutes / 60, 2)


def collect_data():

    sheet = connect_sheet(
        os.getenv("SPREADSHEET_ID")
    )

    channel_id = get_channel_id(
        os.getenv("CHANNEL_USERNAME")
    )

    latest = get_latest_video_info(channel_id)

    minutes = calculate_minutes(
        latest["published_at"]
    )

    # Stop after 24 hours
    if minutes >= 1440:
        print("Tracking Completed")
        return

    hour = calculate_hour_decimal(minutes)

    last_row = get_last_row(sheet)

    increase = 0

    if last_row:
        try:
            last_video = last_row[1]
            last_views = int(last_row[7])

            if last_video == latest["video_id"]:
                increase = latest["views"] - last_views
        except:
            increase = 0

    row = [
        datetime.now().strftime("%d-%m-%Y"),
        latest["video_id"],
        latest["title"],
        latest["published_at"],
        datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        hour,
        minutes,
        latest["views"],
        increase,
        "TRACKING"
    ]

    append_row(sheet, row)

    print("Saved Successfully")