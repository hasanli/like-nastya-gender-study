import torch
import open_clip
from PIL import Image
from pathlib import Path
import numpy as np

class ZeroShot:
    def __init__(self, model_name: str, pretrained: str, labels: dict):
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(model_name, pretrained=pretrained)
        self.tokenizer = open_clip.get_tokenizer(model_name)
        self.labels = {k: v for k, v in labels.items()}
        self._label_tokens = {k: self.tokenizer([f"a photo of {x}" for x in v]) for k, v in self.labels.items()}

    def scores_for_frame(self, img_path: str) -> dict:
        img = self.preprocess(Image.open(img_path)).unsqueeze(0)
        with torch.no_grad(), torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
            img_feats = self.model.encode_image(img)
            out = {}
            for group, toks in self._label_tokens.items():
                text_feats = self.model.encode_text(toks)
                logits = (img_feats @ text_feats.T).softmax(dim=-1).cpu().numpy()[0]
                out.update({f"{group}_{label.replace(' ', '_')}": float(logits[i]) for i, label in enumerate(self.labels[group])})
            return out

    def aggregate_over_dir(self, frames_dir: str) -> dict:
        paths = sorted(Path(frames_dir).glob("*.jpg"))
        if not paths:
            return {}
        acc = None
        n = 0
        keys = None
        for p in paths[:200]:
            s = self.scores_for_frame(str(p))
            if keys is None:
                keys = list(s.keys())
            v = np.array(list(s.values()), dtype=float)
            acc = v if acc is None else acc + v
            n += 1
        avg = acc / max(1, n)
        return {k: float(avg[i]) for i, k in enumerate(keys)}
