import pandas as pd
from .youtube_client import YouTubeClient

def select_videos(cfg) -> pd.DataFrame:
    yt = YouTubeClient(cfg["youtube"]["api_key"])
    rows = []
    keywords = [k.lower() for k in cfg["youtube"]["include_keywords"]]
    for chq in cfg["youtube"]["channels"]:
        cid = yt.resolve_channel_id(chq["query"])
        vids = yt.list_channel_videos(cid, max_results=200)
        meta = yt.hydrate_videos(vids)

        def hit(t: str) -> bool:
            t = (t or "").lower()
            return any(k in t for k in keywords)

        for it in meta:
            stats = it.get("statistics", {})
            views = int(stats.get("viewCount", 0))
            snip = it["snippet"]
            title = snip.get("title", "")
            desc  = snip.get("description", "")
            if views >= cfg["youtube"]["min_views"] and (hit(title) or hit(desc)):
                rows.append({
                    "channel": snip.get("channelTitle"),
                    "channel_id": it["snippet"]["channelId"],
                    "video_id": it["id"],
                    "title": title,
                    "description": desc,
                    "publishedAt": snip.get("publishedAt"),
                    "viewCount": views,
                    "duration": it["contentDetails"].get("duration", ""),
                    "url": f"https://www.youtube.com/watch?v={it['id']}"
                })
    df = pd.DataFrame(rows).sort_values("viewCount", ascending=False)
    df = df.groupby("channel", group_keys=False).head(cfg["youtube"]["max_videos_per_channel"])
    return df
