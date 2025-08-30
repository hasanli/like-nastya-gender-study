import subprocess
from pathlib import Path

def download_video(url: str, out_dir: str) -> str:
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    cmd = [
        "yt-dlp",
        "-f", "mp4[height<=360]/best[ext=mp4]/best",
        "-o", f"{out_dir}/%(id)s.%(ext)s",
        url,
    ]
    subprocess.run(cmd, check=True)
    return str(next(Path(out_dir).glob("*.mp4")))
