from sqlalchemy.orm import Session
from models import Metrics
from schemas import MetricsResponse
from collections.abc import Hashable

class MetricsController:
    def __init__(self, db: Session):
        self.db = db

    def get_active_reach(self, posts):
        total_likes = sum(post['like_count'] for post in posts)
        total_comments = sum(post['comment_count'] for post in posts)
        total_views = sum(post['view_count'] for post in posts if 'view_count' in post)
        total_posts = len(posts)
        return (total_likes + total_comments + total_views) / total_posts if total_posts else 0

    def get_emv(self, followers, posts):
        comments = sum(post['comment_count'] for post in posts)
        likes = sum(post['like_count'] for post in posts)
        plays = sum(post['play_count'] for post in posts if 'play_count' in post)
        return (followers / 1000 * 2.1) + (comments * 4.19) + (likes * 0.09) + (plays * 0.11)

    def get_average_fields(self, posts):
        total_engagements = sum(post['like_count'] + post['comment_count'] + post.get('share_count', 0) + post.get('save_count', 0) for post in posts)
        video_views = [post['view_count'] for post in posts if 'view_count' in post]
        story_reach = [post['story_reach'] for post in posts if 'story_reach' in post]
        story_engagements = [post['story_engagements'] for post in posts if 'story_engagements' in post]
        story_views = [post['story_views'] for post in posts if 'story_views' in post]
        saves = [post['saves'] for post in posts if 'saves' in post]
        likes = [post['like_count'] for post in posts]
        comments = [post['comment_count'] for post in posts]
        shares = [post['share_count'] for post in posts if 'share_count' in post]

        return {
            'engagements' : total_engagements / len(posts) if posts else 0,
            'video_views': sum(video_views)/len(video_views) if video_views else 0,
            'story_reach': sum(story_reach)/len(story_reach) if story_reach else 0,
            'story_engagements': sum(story_engagements)/len(story_engagements) if story_engagements else 0,
            'story_views': sum(story_views)/len(story_views) if story_views else 0,
            'saves': sum(saves)/len(saves) if saves else 0,
            'likes': sum(likes)/len(likes) if likes else 0,
            'comments': sum(comments)/len(comments) if comments else 0,
            'shares': sum(shares)/len(shares) if shares else 0,
        }
    
    def get_profile_fields(self, profile):
        return {
            'country': profile['country'],
            'followers': profile['followers'],
            'profile_url': profile['profile_url'],
            'username': profile['username'],
        }

    async def store_metrics(self, recentPosts: list[dict[Hashable, any]], profileData: dict[Hashable, any]):
        profile_id = profileData['sila_id']
        active_reach = self.get_active_reach(recentPosts)
        emv = self.get_emv(profileData['followers'], recentPosts)
        postCount=len(recentPosts)

        averageFields = self.get_average_fields(recentPosts)
        profileFields = self.get_profile_fields(profileData)

        # Store all metrics at once
        metricsData = {
            "id" : profileData["user_id"],
            'active_reach': active_reach,
            "post_count":postCount,
            'emv': emv,
            **averageFields,
            **profileFields
        }

        new_metrics = Metrics(
            username=metricsData.get("username"),
            profile_url=metricsData.get("profile_url"),
            country=metricsData.get("country"),
            followers=metricsData.get("followers"),
            emv=metricsData.get('emv'),
            post_count=metricsData.get("post_count"),
            active_reach=metricsData.get('active_reach'),

            engagements=metricsData.get('engagements'),
            video_views=metricsData.get('video_views'),
            story_reach=metricsData.get('story_reach'),
            story_engagements=metricsData.get('story_engagements'),
            story_views=metricsData.get('story_views'),
            saves=metricsData.get('saves'),
            likes=metricsData.get('likes'),
            comments=metricsData.get('comments'),
            shares=metricsData.get('shares'),
            )
        self.db.add(new_metrics)
        self.db.commit()
        return new_metrics

    def classify_posts(self, posts):
        # Classify posts as 'Paid' or 'Organic'
        for post in posts:
            description = str(post.get('description', ''))  # Convert description to string, default to empty if missing
            if '@' in description or 'اعلان' in description:
                post['content_type'] = 'Paid'
            else:
                post['content_type'] = 'Organic'
        return posts

    def compute_metrics_by_category(self, profile ,posts):
        # Classify posts
        posts = self.classify_posts(posts)

        # Divide posts into categories
        paid_posts = [post for post in posts if post['content_type'] == 'Paid']
        organic_posts = [post for post in posts if post['content_type'] == 'Organic']

        # Calculate metrics for each category
        metrics_paid = self.get_all_metrics(profile,paid_posts)
        metrics_organic = self.get_all_metrics(profile,organic_posts)
        return metrics_paid, metrics_organic

    async def get_metrics_by_username(self, username: str):
        metrics = self.db.query(Metrics).filter(Metrics.username == username).all()
        return [MetricsResponse.model_validate(metric) for metric in metrics] if metrics else []

    async def get_all_metrics_from_db(self):
        metrics = self.db.query(Metrics).all()
        return [MetricsResponse.model_validate(metric) for metric in metrics] if metrics else []
    
    def get_all_metrics(self,profile,posts):
        total_followers =  profile['followers']
        averageFields = self.get_average_fields(posts)
        return {
            'active_reach': self.get_active_reach(posts),
            'emv': self.get_emv(total_followers, posts),
            **averageFields
        }