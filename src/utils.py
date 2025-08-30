from pathlib import Path
import yaml
import os

def load_cfg(path: str = "config.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    api_key = os.getenv("YOUTUBE_API_KEY")
    if api_key:
        cfg.setdefault("youtube", {})["api_key"] = api_key
    p = cfg["paths"]
    for k in ["data_dir", "raw_videos", "frames", "transcripts", "annotations", "reports"]:
        Path(p[k]).mkdir(parents=True, exist_ok=True)
    return cfg
