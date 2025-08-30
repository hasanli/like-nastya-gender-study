import re
from collections import Counter
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

def fetch_transcript(video_id: str, languages=("en","tr","ru")) -> str:
    try:
        tr = YouTubeTranscriptApi.get_transcript(video_id, languages=list(languages))
        return "\n".join([x["text"] for x in tr])
    except TranscriptsDisabled:
        return ""
    except Exception:
        return ""

def pronoun_counts(text: str, female_words, male_words) -> dict:
    tokens = re.findall(r"[a-zA-Z']+", text.lower())
    c = Counter(tokens)
    f = sum(c[w] for w in female_words)
    m = sum(c[w] for w in male_words)
    total = max(1, f + m)
    return {
        "female_pronoun_rate": f / total,
        "male_pronoun_rate": m / total,
        "pronoun_total": f + m,
    }

def stereotype_hits(text: str, lexicon: list) -> int:
    tokens = re.findall(r"[a-zA-Z']+", text.lower())
    return sum(1 for t in tokens if t in set(lexicon))

def nlp_message_features(text: str, cfg) -> dict:
    if not text:
        return {
            "female_pronoun_rate": None,
            "male_pronoun_rate": None,
            "pronoun_total": 0,
            "domestic_hits_k": 0.0,
            "adventurous_hits_k": 0.0,
        }
    pr = pronoun_counts(text, cfg["nlp"]["pronouns"]["female"], cfg["nlp"]["pronouns"]["male"])
    dom = stereotype_hits(text, cfg["nlp"]["stereotype_lexicons"]["domestic"])
    adv = stereotype_hits(text, cfg["nlp"]["stereotype_lexicons"]["adventurous"])
    words = max(1, len(text.split()))
    return {
        **pr,
        "domestic_hits_k": 1000.0 * dom / words,
        "adventurous_hits_k": 1000.0 * adv / words,
    }
