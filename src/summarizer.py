import pandas as pd
from pathlib import Path

def summarize(per_video_csv: str, out_dir: str):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(per_video_csv)

    visual = df[["pink_ratio", "blue_ratio", "pastel_ratio", "dark_ratio"]].describe().round(3)
    visual.to_csv(Path(out_dir, "visual_summary.csv"))

    roles = df[["faces_co_presence_rate", "female_pronoun_rate", "male_pronoun_rate"]].describe().round(3)
    roles.to_csv(Path(out_dir, "roles_summary.csv"))

    df[["domestic_hits_k", "adventurous_hits_k"]].describe().round(3).to_csv(Path(out_dir, "messages_lexicon_summary.csv"))

    for c in ["problem_solving_style", "decision_maker", "lead_character_presented_gender", "emotional_valence"]:
        if c in df.columns:
            vc = df[c].value_counts(dropna=True, normalize=True).round(3)
            vc.to_csv(Path(out_dir, f"{c}_distribution.csv"))

    if 'channel' in df.columns:
        ch = df.groupby('channel')[['pink_ratio','blue_ratio','pastel_ratio','dark_ratio','domestic_hits_k','adventurous_hits_k']].mean().round(3)
        ch.to_csv(Path(out_dir, "by_channel_means.csv"))

    df.to_csv(Path(out_dir, "per_video_metrics.csv"), index=False)
    print("Saved summaries to:", out_dir)
