import cv2
import numpy as np
from pathlib import Path

PINK_1 = ((160, 80, 60), (179, 255, 255))
REDLIKE = ((0, 80, 120), (10, 255, 255))
BLUE   = ((100, 80, 60), (130, 255, 255))

def mask_ratio(hsv, lower, upper):
    mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
    return float(mask.mean()) / 255.0

def color_stats_for_frame(img_bgr) -> dict:
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    total = hsv.shape[0] * hsv.shape[1]
    pink = max(mask_ratio(hsv, *PINK_1), mask_ratio(hsv, *REDLIKE))
    blue = mask_ratio(hsv, *BLUE)
    pastel = float(((s < 80) & (v > 180)).sum()) / total
    dark = float((v < 40).sum()) / total
    return {
        "pink_ratio": round(pink, 4),
        "blue_ratio": round(blue, 4),
        "pastel_ratio": round(pastel, 4),
        "dark_ratio": round(dark, 4),
    }

def aggregate_color_stats(frames_dir: str) -> dict:
    paths = sorted(Path(frames_dir).glob("*.jpg"))
    if not paths:
        return {k: None for k in ["pink_ratio", "blue_ratio", "pastel_ratio", "dark_ratio"]}
    vals = []
    for p in paths:
        img = cv2.imread(str(p))
        if img is None:
            continue
        vals.append(color_stats_for_frame(img))
    if not vals:
        return {k: None for k in ["pink_ratio", "blue_ratio", "pastel_ratio", "dark_ratio"]}
    return {k: round(float(np.mean([d[k] for d in vals])), 4) for k in vals[0].keys()}
