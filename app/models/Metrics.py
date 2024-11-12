from sqlalchemy import Column, Integer, Float, String, Date, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

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

    def calculate_active_reach(self, total_comments, total_likes, total_views, total_posts):
        """ Calculate active reach. """
        if total_posts > 0:
            self.active_reach = (total_comments + total_likes + total_views) / total_posts
        else:
            self.active_reach = 0

    def calculate_emv(self, followers, comments, likes, plays):
        """ Calculate EMV based on formula. """
        self.emv = (followers / 1000 * 2.1) + (comments * 4.19) + (likes * 0.09) + (plays * 0.11)

    def determine_content_type(self, caption):
        """ Determine if content is paid or organic based on the caption. """
        if '@' in caption or 'اعلان' in caption:
            self.content_type = 'Paid'
        else:
            self.content_type = 'Organic'

# Example of setting up a SQLite in-memory database and creating the table.
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
