from django.shortcuts import render
from requests_oauthlib import OAuth1Session
from django.http import JsonResponse
import requests

def fetch_user_tweets(url, oauth_session):
    try:
        response = oauth_session.get(url)
        if response.status_code == 200:
            # Successful request
            return response.json()  # Assuming the response is JSON
        else:
            # Failed request
            error_message = f"Failed to fetch user tweets. Status code: {response.status_code}"
            error_details = response.json()
            return {"error_message": error_message, "error_details": error_details}
    except Exception as e:
        # Exception occurred
        error_message = f"An error occurred: {e}"
        return {"error_message": error_message}

def get_profile_data(request):
    url = 'https://api.twitter.com/2/users/me'
    consumer_key = 'consumer_key'
    consumer_secret = 'consumer_secret'
    access_token = 'access_token'
    access_token_secret = 'access_token_secret'

    oauth_session = OAuth1Session(consumer_key, client_secret=consumer_secret, resource_owner_key=access_token, resource_owner_secret=access_token_secret)

    tweets_data = fetch_user_tweets(url, oauth_session)
    
    if tweets_data.get("error_message"):
        # If there's an error message, return it as JSON response or handle as needed
        return render(request, 'error.html', {'error_message': tweets_data["error_message"]})
    else:
        tweets = tweets_data.get("data", [])
        return render(request, 'tweets.html', {'tweets': tweets})


def get_my_tweets(request):
    url = 'https://api.twitter.com/2/tweets'
    headers = {
        'Authorization': 'Bearer ACCESS_TOKEN'
    }
    params = {
        'max_results': 10,  # Number of tweets to retrieve, adjust as needed
        'tweet.fields': 'created_at',  # You can specify which tweet fields you want to retrieve
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        # Process the response data here
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Failed to fetch tweets'}, status=response.status_code)


def get_user_tweets(request, user_id_or_username):
    url = f'https://api.twitter.com/2/users/{user_id_or_username}/tweets'
    headers = {
        'Authorization': 'Bearer ACCESS_TOKEN'
    }
    params = {
        'max_results': 10,  # Number of tweets to retrieve, adjust as needed
        'tweet.fields': 'created_at',  # You can specify which tweet fields you want to retrieve
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        # Process the response data here
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Failed to fetch user tweets'}, status=response.status_code)
