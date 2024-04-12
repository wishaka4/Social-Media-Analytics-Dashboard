
# urls.py
from django.urls import path
from twitter_api.views import get_user_tweets,get_my_tweets

urlpatterns = [
    # path('profile/', get_profile_data, name='get_profile_data'),
    path('user_tweets/<str:user_id_or_username>/', get_user_tweets, name='user_tweets'),
    path('my_tweets/', get_my_tweets, name='my_tweets'),
]
