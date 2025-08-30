import cv2
from pathlib import Path

CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def faces_in_frame(img) -> int:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = CASCADE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
    return len(faces)

def co_presence_rate(frames_dir: str) -> float:
    paths = sorted(Path(frames_dir).glob('*.jpg'))
    if not paths:
        return None
    co = 0
    total = 0
    for p in paths:
        img = cv2.imread(str(p))
        if img is None:
            continue
        n = faces_in_frame(img)
        if n >= 2:
            co += 1
        total += 1
    return round(co / max(1, total), 4)
