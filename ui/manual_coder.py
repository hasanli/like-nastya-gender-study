import streamlit as st
import pandas as pd
from pathlib import Path
import json

st.set_page_config(page_title="Like Nastya Gender Coding UI", layout="wide")

DATA = Path("data")
VIDEOS = DATA / "videos.csv"
ANN = DATA / "annotations"
ANN.mkdir(parents=True, exist_ok=True)

st.title("Uniform Coding — Like Nastya Study")

if not VIDEOS.exists():
    st.error("videos.csv not found. Run: python -m src.cli --mode select")
    st.stop()

videos = pd.read_csv(VIDEOS)
idx = st.number_input("Video index", min_value=0, max_value=len(videos)-1, value=0, step=1)
row = videos.iloc[int(idx)]

st.subheader(row.title)
st.write(row.url)
st.video(row.url)

st.markdown("### 3 Criteria Fields")

col1, col2 = st.columns(2)
with col1:
    lead = st.selectbox("Lead character presented gender", ["", "F", "M", "Mixed", "Other"])
    deci = st.selectbox("Primary decision maker", ["", "F", "M", "Mixed", "NA"])
    prob = st.selectbox("Problem-solving style", ["", "Independent", "Collaborative", "Assisted"])
with col2:
    emo  = st.selectbox("Emotional valence", ["", "Positive", "Neutral", "Negative"]) 
    coder = st.text_input("Coder ID", value="rater1")
    conf  = st.slider("Confidence (1–5)", 1, 5, 4)

notes = st.text_area("Notes (brief, objective)")

if st.button("Save annotation"):
    out = {
        "video_id": row.video_id,
        "lead_character_presented_gender": lead or None,
        "decision_maker": deci or None,
        "problem_solving_style": prob or None,
        "emotional_valence": emo or None,
        "coder_id": coder or None,
        "confidence_1_5": int(conf),
        "notes": notes or None,
    }
    with open(ANN / f"{row.video_id}_{coder}.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    st.success("Saved.")

st.info("Annotations are saved per video_id & coder. The summarizer will merge them with automated metrics.")
