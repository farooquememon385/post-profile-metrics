from sqlalchemy import Column, Integer, Float, String, Date, Boolean, create_engine
from database import Base

class Metrics(Base):
    __tablename__ = 'metrics'
    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String)
    profile_url = Column(String)
    country = Column(String)
    
    media_type = Column(String)  # Either 'Photo' or 'Video'
    followers = Column(Integer)
    emv = Column(Float)  # Earned Media Value (EMV)
    active_reach = Column(Float)
    content_type = Column(String) # Organic or Paid if containe @ or ailan
    post_count = Column(Integer)

    # Average metrics for the last 3 months
    engagements = Column(Float)
    video_views = Column(Float)
    story_reach = Column(Float)
    story_engagements = Column(Float)
    story_views = Column(Float)
    saves = Column(Float)
    likes = Column(Float)
    comments = Column(Float)
    shares = Column(Float)

