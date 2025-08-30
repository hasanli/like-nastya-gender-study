import subprocess
from pathlib import Path

def sample_frames(video_path: str, out_dir: str, every_seconds: int = 3, max_frames: int = 400):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-i", video_path, "-vf", f"fps=1/{every_seconds}", f"{out_dir}/%05d.jpg"
    ]
    subprocess.run(cmd, check=True)
    frames = sorted(Path(out_dir).glob("*.jpg"))
    for p in frames[max_frames:]:
        p.unlink()
