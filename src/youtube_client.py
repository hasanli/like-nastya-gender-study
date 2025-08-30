from googleapiclient.discovery import build
from typing import Dict, List

class YouTubeClient:
    def __init__(self, api_key: str):
        self.yt = build("youtube", "v3", developerKey=api_key)

    def resolve_channel_id(self, query: str) -> str:
        resp = self.yt.search().list(part="snippet", q=query, type="channel", maxResults=5).execute()
        items = resp.get("items", [])
        if not items:
            raise RuntimeError(f"No channel found for query: {query}")
        best = None
        best_subs = -1
        for it in items:
            cid = it["snippet"]["channelId"]
            ch = self.yt.channels().list(part="snippet,statistics", id=cid).execute()
            ch_item = ch["items"][0]
            subs = int(ch_item["statistics"].get("subscriberCount", 0))
            if subs > best_subs:
                best, best_subs = ch_item, subs
        return best["id"]

    def list_channel_videos(self, channel_id: str, max_results: int = 50) -> List[str]:
        video_ids = []
        page_token = None
        while len(video_ids) < max_results:
            resp = self.yt.search().list(
                part="id",
                channelId=channel_id,
                maxResults=min(50, max_results - len(video_ids)),
                order="date",
                type="video",
                pageToken=page_token,
            ).execute()
            ids = [it["id"]["videoId"] for it in resp.get("items", []) if it["id"].get("videoId")]
            video_ids.extend(ids)
            page_token = resp.get("nextPageToken")
            if not page_token:
                break
        return video_ids

    def hydrate_videos(self, video_ids: List[str]) -> List[Dict]:
        out = []
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i+50]
            resp = self.yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(batch)).execute()
            out.extend(resp.get("items", []))
        return out
