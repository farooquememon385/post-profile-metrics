from pydantic import BaseModel
from typing import Optional

class MetricsBase(BaseModel):
    username: str
    profile_url: Optional[str]
    country: Optional[str]
    media_type: Optional[str]
    followers: Optional[int]
    emv: Optional[float]
    active_reach:  Optional[float]
    content_type:  Optional[str]
    post_count: Optional[int]

    # Average metrics for the last 3 months
    engagements: Optional[float]
    video_views: Optional[float]
    story_reach: Optional[float]
    story_engagements: Optional[float]
    story_views: Optional[float]
    saves: Optional[float]
    likes: Optional[float]
    comments: Optional[float]
    shares: Optional[float]

class MetricsCreate(MetricsBase):
    pass

class MetricsResponse(MetricsBase):
    id: int
    
    class Config:
        orm_mode = True