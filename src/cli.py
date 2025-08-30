import argparse
from pathlib import Path
import pandas as pd
import json

from .utils import load_cfg
from .select_videos import select_videos
from .nlp_messages import transcript_features_for_video
from .color_analysis import aggregate_color_stats
from .roles_interactions import co_presence_rate
from .clip_zeroshot import ZeroShot
from .frame_sampler import sample_frames
from .download import download_video

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["select","analyze","summarize"], required=True)
    ap.add_argument("--config", default="config.yaml")
    args = ap.parse_args()

    cfg = load_cfg(args.config)
    paths = cfg["paths"]

    if args.mode == "select":
        df = select_videos(cfg)
        out = Path(paths["data_dir"]) / "videos.csv"
        df.to_csv(out, index=False)
        print("Saved:", out)
        return

    if args.mode == "analyze":
        df = pd.read_csv(Path(paths["data_dir"]) / "videos.csv")
        zs = None
        if cfg["clip"]["enabled"]:
            zs = ZeroShot(cfg["clip"]["model_name"], cfg["clip"]["pretrained"], cfg["clip"]["labels"])

        rows = []
        for _, r in df.iterrows():
            video_id = r["video_id"]
            url = r["url"]

            nlp_feats = transcript_features_for_video(video_id, cfg)

            color_feats = {"pink_ratio": None, "blue_ratio": None, "pastel_ratio": None, "dark_ratio": None}
            copres = None
            zs_feats = {}

            if cfg["analysis"]["allow_downloads"]:
                vp = download_video(url, paths["raw_videos"])
                frames_dir = str(Path(paths["frames"]) / video_id)
                sample_frames(vp, frames_dir, cfg["analysis"]["frame_sample_seconds"], cfg["analysis"]["max_frames_per_video"])
                color_feats = aggregate_color_stats(frames_dir)
                copres = co_presence_rate(frames_dir)
                if zs:
                    zs_feats = zs.aggregate_over_dir(frames_dir)

            row = {
                "video_id": video_id,
                "channel": r["channel"],
                "title": r["title"],
                "url": r["url"],
                "viewCount": r["viewCount"],
                **nlp_feats,
                **color_feats,
                "faces_co_presence_rate": copres,
                **zs_feats,
            }
            rows.append(row)

        # Merge manual annotations if present
        ann_dir = Path(paths["annotations"])
        if ann_dir.exists():
            for row in rows:
                vid = row["video_id"]
                for jf in ann_dir.glob(f"{vid}_*.json"):
                    try:
                        with open(jf, "r", encoding="utf-8") as f:
                            ann = json.load(f)
                        for k in ["lead_character_presented_gender","decision_maker","problem_solving_style","emotional_valence","coder_id","confidence_1_5","notes"]:
                            if k in ann and ann[k] is not None:
                                row[k] = ann[k]
                    except Exception:
                        pass

        out = Path(paths["reports"]) / "per_video_metrics.csv"
        pd.DataFrame(rows).to_csv(out, index=False)
        print("Saved per_video_metrics:", out)
        return

    if args.mode == "summarize":
        from .summarizer import summarize
        summarize(str(Path(paths["reports"]) / "per_video_metrics.csv"), paths["reports"])

if __name__ == "__main__":
    main()
