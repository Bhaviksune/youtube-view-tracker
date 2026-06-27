from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

youtube = build(
    "youtube",
    "v3",
    developerKey=os.getenv("YOUTUBE_API_KEY")
)


def get_channel_id(username):

    request = youtube.search().list(
        part="snippet",
        q=username,
        type="channel",
        maxResults=1
    )

    response = request.execute()

    if response["items"]:
        return response["items"][0]["snippet"]["channelId"]

    return None

def get_latest_video(channel_id):

    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="date",
        type="video",
        maxResults=1
    )

    response = request.execute()

    if not response["items"]:
        return None

    video = response["items"][0]

    return {
        "video_id": video["id"]["videoId"],
        "title": video["snippet"]["title"],
        "published_at": video["snippet"]["publishedAt"]
    }

def get_video_statistics(video_id):

    request = youtube.videos().list(
        part="statistics",
        id=video_id
    )

    response = request.execute()

    if not response["items"]:
        return None

    stats = response["items"][0]["statistics"]

    return {
        "views": int(stats.get("viewCount", 0)),
        "likes": int(stats.get("likeCount", 0)),
        "comments": int(stats.get("commentCount", 0))
    }

def get_latest_video_info(channel_id):

    video = get_latest_video(channel_id)

    if video is None:
        return None

    stats = get_video_statistics(video["video_id"])

    return {
        "video_id": video["video_id"],
        "title": video["title"],
        "published_at": video["published_at"],
        "views": stats["views"],
        "likes": stats["likes"],
        "comments": stats["comments"]
    }