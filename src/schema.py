from pydantic import BaseModel, Field
from typing import Optional

class PerVideoMetrics(BaseModel):
    video_id: str
    channel: str
    title: str
    url: str
    viewCount: int

    pink_ratio: Optional[float] = None
    blue_ratio: Optional[float] = None
    pastel_ratio: Optional[float] = None
    dark_ratio: Optional[float] = None

    faces_co_presence_rate: Optional[float] = None

    female_pronoun_rate: Optional[float] = None
    male_pronoun_rate: Optional[float] = None
    pronoun_total: int = 0
    domestic_hits_k: float = 0.0
    adventurous_hits_k: float = 0.0

    lead_character_presented_gender: Optional[str] = Field(None, description="F/M/Mixed/Other")
    decision_maker: Optional[str] = None
    problem_solving_style: Optional[str] = None
    emotional_valence: Optional[str] = None
    coder_id: Optional[str] = None
    confidence_1_5: Optional[int] = None
    notes: Optional[str] = None
