# Uniform Codebook (v0.1)

## Visual elements
- **Pink ratio**: % of pixels in HSV ranges approximating pink/magenta or red‑pink; averaged across sampled frames.
- **Blue ratio**: % of pixels in HSV blue range; averaged.
- **Pastel ratio**: % pixels with low saturation (S<80) and high value (V>180); averaged.
- **Dark ratio**: % pixels with V<40; averaged.
- **Toy/Activity cues (optional)**: CLIP zero‑shot probabilities for labels in `config.yaml` averaged across frames.

## Character roles & interactions
- **Co‑presence rate**: % frames with ≥2 faces.
- **Pronoun balance**: female vs male pronouns in transcript.
- **Manual fields**: `lead_character_presented_gender`, `decision_maker`.

## Messages about gender
- **Lexicon hits per 1k words**: domestic/adventurous counts per 1,000 transcript words.
- **Manual fields**: `problem_solving_style`, `emotional_valence`.
