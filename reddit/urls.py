
from django.urls import include, path
from .views import reddit_auth, reddit_callback,demographics1,fetch_latest_posts,fetch_posts_by_author,demographics,display_posts,display_data_with_demographics,display_data_with_pandas

urlpatterns = [
    path('reddit/auth/', reddit_auth, name='reddit_auth'),
    path('reddit/callback/', reddit_callback, name='reddit_callback'),
    # path('reddit/latest_posts/<str:subreddit_name>/', fetch_latest_posts, name='fetch_latest_posts'),
    path('reddit/latest_posts/', fetch_latest_posts, name='fetch_latest_posts'),
    path('fetch_posts_by_author/<str:author_name>/', fetch_posts_by_author, name='fetch_posts_by_author'),
    path('table/', display_posts, name='display_posts'),
    path('display_data/', display_data_with_pandas, name='display_data'),
    path('display_data_with_demographics/', display_data_with_demographics, name='display_data_with_demographics'),
    path('demographics/', demographics, name='demographics'),
    path('demographics1/', demographics1, name='demographics1'),
    
    
]