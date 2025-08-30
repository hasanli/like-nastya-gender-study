from .transcripts import fetch_transcript, nlp_message_features

def transcript_features_for_video(video_id: str, cfg) -> dict:
    text = fetch_transcript(video_id, languages=tuple(cfg["nlp"]["languages"]))
    feats = nlp_message_features(text, cfg)
    feats.update({"transcript_chars": len(text)})
    return feats
