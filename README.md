# Like Nastya Gender Study — Pipeline

End‑to‑end, reproducible toolkit to select videos, analyze the **videos themselves**, code findings uniformly, and create summary aligned with the three criteria.

## Quick start

1. Put your YouTube API key in `config.yaml` or export env var `YOUTUBE_API_KEY`.
2. Install deps:
   ```bash
   pip install -r requirements.txt
   ```
3. Select videos (Like Nastya + Like Nastya TR, views ≥ 1M + gender-relevant keywords):
   ```bash
   python -m src.cli --mode select
   ```
   Saves `data/videos.csv`.
4. Analyze (API‑only default: transcripts/NLP; no downloads):
   ```bash
   python -m src.cli --mode analyze
   ```
   Saves `reports/per_video_metrics.csv`.
6. Manual coding UI (uniform 3‑criteria coding):
   ```bash
   streamlit run ui/manual_coder.py
   ```
   Saves JSON annotations to `data/annotations/`.
7. Summarize findings:
   ```bash
   python -m src.cli --mode summarize
   ```
   Outputs CSV tables in `reports/`.