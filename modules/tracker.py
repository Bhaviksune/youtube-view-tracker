import os
from datetime import datetime, timezone

from dotenv import load_dotenv

from modules.youtube import (
    get_channel_id,
    get_latest_video_info
)

from modules.state import (
    load_state,
    save_state
)

from modules.sheets import (
    connect_sheet,
    append_row
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

    state = load_state()

    minutes = calculate_minutes(
        latest["published_at"]
    )

    # Stop after 24 Hours
    if (
        state.get("video_id") == latest["video_id"]
        and minutes >= 1440
    ):
        print("Tracking Completed (24 Hours)")
        return

    hour = calculate_hour_decimal(minutes)

    # View Increase
    if latest["video_id"] == state.get("video_id"):
        increase = latest["views"] - state.get("last_views", 0)
    else:
        increase = 0
        print("New Video Detected")

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

    save_state({
        "video_id": latest["video_id"],
        "video_title": latest["title"],
        "published_at": latest["published_at"],
        "last_views": latest["views"],
        "last_collection_time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "tracking_status": "TRACKING"
    })

    print("Saved Successfully")